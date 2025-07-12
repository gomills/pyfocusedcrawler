from pydantic import ValidationError
import asyncio
import json
import sys
import os

from app.url.helpers.url_heuristics import allowed_file_extensions, sensitive_patterns  # type: ignore
from app.crawler.crawler import Crawler, CrawlerConfiguration


def load_config(domain):
    crawl_config = {
        "max_time": 120,
        "sensitive_patterns": sensitive_patterns,
        "allowed_file_extensions": allowed_file_extensions,
        "max_path_depth": 5,
        "max_crawl_depth": 10,
        "depth_first_search": False,
        "headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"
            )
        },
    }

    validated_config = CrawlerConfiguration.model_validate(crawl_config)

    results_saving_path = os.path.join(os.path.dirname(__file__), f"results\\{domain}_results.json")
    os.makedirs(os.path.dirname(results_saving_path), exist_ok=True)
    
    return domain, validated_config, results_saving_path


def main():
    try:
        for domain in ("example1.com", "example2.com", "example3.com"):

            domain, crawl_config, results_path = load_config(domain)

            crawler = Crawler(domain=domain, config=crawl_config)
            results = crawler.run()

            with open(results_path,"w",) as file:
                json.dump(results, file, indent=1)

            print(f"🎉 Finished crawling {domain}")

        print("🪙 Finished crawling all domains")

    except ValidationError as e:
        print(f"Input couldn't be verified:\n{e}")


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
