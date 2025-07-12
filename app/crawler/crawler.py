from pydantic import BaseModel, Field
from typing import Any
import asyncio
import time


from app.crawler.crawler_helpers import (
    extract_urls,
    send_request,
    get_registered_domain,
    get_initial_urls,
    handle_stored_urls,
)
from app.url.url_validation import validate_string_for_url


class CrawlerConfiguration(BaseModel):
    headers: dict[str, str]
    sensitive_patterns: tuple[str, ...]
    allowed_file_extensions: tuple[str, ...]
    max_workers: int = Field(gt=0, default=2)
    max_time: int = Field(gt=0, default=60)
    valid_external_domains: tuple[str, ...] = Field(default=("github.com",))
    max_path_depth: int = Field(gt=0, lt=21, default=3)
    max_crawl_depth: int = Field(gt=0, lt=21, default=15)
    breadth_first_search: bool = Field(default=True)


class Crawler:
    def __init__(self, domain: str, config: CrawlerConfiguration):
        # Crawler configuration
        self.domain = domain
        self.config = config

        # Instance crawl parameters and data
        self.urls_queue: asyncio.Queue | asyncio.LifoQueue = asyncio.Queue() if self.config.breadth_first_search else asyncio.LifoQueue()  # (URL, crawl depth, URL extension)
        self.stored_urls: dict[str, list[Any]] = dict()  # URL: (URL_depth, Comment, Status_Code).
        self.deduplicator: set[str] = set()
        self.start_time = time.time()
        self.stop_reason: str = "Undefined"
        self.registered_domain: str = get_registered_domain(self.domain)

        # Specific workers data
        self.waiting_workers = 0
        self.active_workers = 0

    def run(self) -> dict[str, Any]:
        """
        This function will start crawling the given domain. First it invokes and waits for the
        workers to finish, then prepares results in specific format.

        Returns:
            e.g:
            {
                "domain": www.example.co.uk,
                "stop_reason": Ran out of time,
                "crawling_time": 120.9 s,
                "number_of_urls": 102,
                "urls": {

                            "successful_requests": 
                                URL: [url_depth, comment, status_code],
                                URL: [url_depth, comment, status_code]

                            "unsuccessful_requests": 
                                URL: [url_depth, comment, status_code],
                                URL: [url_depth, comment, status_code],

                            "not_requested":,
                        }
                }
        """

        asyncio.run(self._crawling_loop())
        crawler_results = {
            "domain": self.domain,
            "stop_reason": self.stop_reason,
            "crawling_time": round(time.time() - self.start_time, 1),
            "number_of_urls": len(self.stored_urls),
            "urls": handle_stored_urls(self.stored_urls),
        }

        return crawler_results

    async def _crawling_loop(self):
        """
        This function will start a pool of a number of max_workers workers to crawl the website.
        Each worker is processing one URL at a time, consuming URLs from self.urls_queue.
        The first worker to leave the crawling will place a sentinel Value of None in the Queue
        Returns None
        """

        initial_urls = get_initial_urls(self.domain, self.registered_domain)
        for url in initial_urls:
            await self.urls_queue.put(url)

        workers_pool = (self._worker() for _ in range(self.config.max_workers))
        return await asyncio.gather(*workers_pool)

    async def _worker(self) -> None:
        """
        This is the worker used to consume URLs from the crawled website.
        It will:
            1.- get a URL from self.urls_queue
            2.- crawl URL and extract links from it adding them to Queue. if URL is from max depth,
                it will just store it, but not in Queue
            3.- save it as crawled in self.stored_urls
            4.- stop crawling in case of: timeout, empty queue or [429 status code of a single request] 
            5.- exit the crawling loop and add a sentinel value None into the queue to stop all other workers
        """

        self.active_workers += 1
        # Worker loop until: empty Queue, time limit hit or a single 429 status hits
        while True:

            # Check that we are on schedule
            if time.time() - self.start_time > self.config.max_time:
                self.stop_reason = "Ran out of time"
                break

            # (1/5) Join the Queue line to get a URL. Before joining check if all other workers are waiting and Queue
            # is empty; that means no more URLs left to crawl.
            self.waiting_workers += 1
            if self.active_workers == self.waiting_workers and self.urls_queue.empty():
                self.stop_reason = "Empty Queue"
                break
            url, url_depth, url_extension = await self.urls_queue.get()
            self.waiting_workers -= 1
            if not url:  # sentinel value hit
                break

            # (3/5) Send the actual request to the URL and await the body content. Now we can update the URL stats
            body, status_code = await send_request(url, headers=self.config.headers)
            self.stored_urls[url] = [url_depth + 1, "Crawled", status_code]
            if status_code == 429:
                self.stop_reason = "429 status code"
                break
            if not body:
                self.stored_urls[url][1] = "Failed to get body"
                continue

            # (4/5) Extract all URLs from the body and try add them to Queue
            urls = extract_urls(body=body, url=url, url_extension=url_extension)
            if urls:
                await self._put_urls_in_queue(urls, url_depth)
            continue

        # (5/5) End crawling by adding sentinel value None for each other active worker. This action is only performed
        # by the first worker to quit the loop
        self.active_workers -= 1
        self.waiting_workers -= 1
        # If this is the first worker to exit, add sentinel values for other workers
        if self.active_workers == self.config.max_workers - 1:
            for _ in range(self.active_workers):
                await self.urls_queue.put((None, None, None))  # type: ignore

        return

    async def _put_urls_in_queue(self, urls: list[str], url_depth: int) -> None:
        """
        Validate the URLs and if not valid, skip. If valid and they are of max depth, store them
        and don't add them to queue. If there's no max depth limit hit, add them to queue.
        """

        for url in urls:
            valid_url, url_extension = self._valid_url(url)
            if not valid_url or valid_url in self.deduplicator:
                continue

            self.deduplicator.add(valid_url)
            
            # If they are of max depth, just store them, no queue
            if url_depth + 1 >= self.config.max_crawl_depth:
                self.stored_urls[valid_url] = [url_depth + 1,"max_crawl_depth_reached",900,]
            else:
                await self.urls_queue.put((valid_url, url_depth + 1, url_extension))

    def _valid_url(self, url: str) -> tuple[str | None, str | None]:
        """
        Validate a string for a URL with the url/url_validation.py module.
        Handles deduplication.
        Returns:
          (url, url_extension).
        """

        
        valid_url, extension = validate_string_for_url(
            possible_url=url,
            domain=self.domain,
            registered_domain=self.registered_domain,
            allowed_file_extensions=self.config.allowed_file_extensions,
            max_path_depth=self.config.max_path_depth,
            sensitive_patterns=self.config.sensitive_patterns,
            valid_external_domains=self.config.valid_external_domains,
        )
        
        return valid_url, extension
            