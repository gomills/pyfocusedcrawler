from aiohttp import ClientSession, ClientConnectorError, ClientConnectorDNSError
import tldextract
from typing import Any

from app.parsers.robots_file_link_extractor.robots_file_link_extractor import extract_links_from_robots_file  # type: ignore
from app.parsers.generic_link_extractor.generic_text_regexing import regex_text_for_links

from app.parsers.html_link_extractor.html_link_extractor import extract_links_from_html  # type: ignore
from app.parsers.js_link_extractor.js_link_extractor import extract_links_from_js


def get_initial_urls(domain: str, registered_domain: str) -> tuple[tuple[str, int, str], ...]:
    """
    This function constructs and returns the initial
    URLs to begin crawling with. The expected format for URLs in
    the queue is: (URL, crawl depth, extension)
    """

    return (
        (f"https://{domain}/", 0, ".html"),
        (f"https://{domain}/robots.txt", 0, ".txt"),
        (f"https://{domain}/sitemap.xml", 0, ".xml"),
        (f"https://dev.{registered_domain}", 0, ".html"),
        (f"https://staging.{registered_domain}", 0, ".html"),
        (f"https://admin.{registered_domain}", 0, ".html"),
        (f"https://test.{registered_domain}", 0, ".html"),
        (f"https://internal.{registered_domain}", 0, ".html"),
    )


def extract_urls(body: str, url: str, url_extension: str | None) -> list[str] | None:
    """
    Call URL finding functions on the body of the request. We take advantage of the stored URL_extension
    to call the appropiate parser (html, js or others).
    .html and .js have their own dedicated parsers and extractors. Other scripts extensions are just regexed
    with an absolute regex pattern (relative support may be added later).
    Returns:
      all found URLs in a list[str, ...] or None
    """

    if url_extension == ".html":
        return extract_links_from_html(body)
    elif url_extension == ".js":
        return extract_links_from_js(body)
    elif url_extension == ".txt":
        return _handle_txt_files(body, url)
    else:
        return regex_text_for_links(body)


async def send_request(url: str, headers: dict) -> tuple[str | None, int]:
    """
    Send an async request with aiohttp to url and return the status code and body of response.
    Returns:
     (url, status_code) or (None, None) in case of DNS or Timeout error"""

    try:
        async with ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                text = await response.text(errors="replace")
                return text, response.status

    except (ClientConnectorDNSError, ClientConnectorError):
        return None, 400

    except Exception:
        # Catch-all for anything else (timeouts, SSL, etc.)
        return None, 400


def get_registered_domain(url_or_domain: str) -> str:
    """
    Extracts the registered domain (e.g., 'www.example.com' -> 'example.com') from a URL or domain.
    Leverages the tldextract python library.
    Handles subdomains and complex domain extensions flawlessly thanks to the tldextract library.
    """

    extracted = tldextract.extract(url_or_domain)
    if extracted.domain and extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}"
    return ""


def _handle_txt_files(body: str, url: str) -> list[str] | None:
    """
    We have to pay attention to .txt files because if it's the robots we need
    to handle it differently with its dedicated parser (app/parsers/robots_file)
    """

    if url.endswith(("robots.txt", "robots.txt/")):
        return extract_links_from_robots_file(body)
    else:
        return regex_text_for_links(body=body)


def handle_stored_urls(stored_urls: dict[str, list[Any]]) -> dict[str, Any]:
    """
    This function receives:

    stored_urls = {
        URL: [url_depth, comment, status_code],
        URL: [url_depth, comment, status_code],
        (...)
        }

    And returns a dict with URLs sorted by length and status code.
    """

    # URL: (URL_depth, Comment, Status_Code)
    successful_requests = {}
    unsuccessful_requests = {}
    not_requested = {}

    # Sort by URL depth (stats[0])
    ordered_stored_urls = dict(sorted(stored_urls.items(), key=lambda x: len(x[0])))

    for url, stats in ordered_stored_urls.items():
        if stats[2] < 300:
            successful_requests[url] = stats
        elif stats[2] == 900:
            not_requested[url] = stats
        else:  # >= 300 and != 900 (includes redirects, client errors, server errors)
            unsuccessful_requests[url] = stats

    return {
        "successful_requests": successful_requests,
        "unsuccessful_requests": unsuccessful_requests,
        "not_requested": not_requested,
    }
