# Web Crawler

A multi-threaded asynchronous web crawler built with Python that systematically crawls websites focused on useful URLs. Focused on security, aims to discover all URLs that characterize a website and its most direct vulnerabilities (important subpages and all scripts).

Stops at first 429 status code, time limit or empty Queue. Won't bypass antibot measures such as 
captcha.


## 🚀 Usage

### 1. Install Dependencies

```bash
uv sync
```

### 2. Run Tests

```bash
pytest
```

### 3. Configure the Crawler

Edit `main.py` to set up your crawling parameters using the `CrawlerConfiguration` model:

```python
from crawler.config import CrawlerConfiguration

crawl_config = CrawlerConfiguration(
    headers={"User-Agent": "MyCrawler/1.0"},
    sensitive_patterns=("admin", "login", "config"),
    allowed_file_extensions=("html", "js", "php"),
    max_workers=4,
    max_time=120,
    valid_external_domains=("github.com", "docs.python.org"),
    max_path_depth=5,
    max_crawl_depth=10,
    breadth_first_search=True
)
```

- **headers**: HTTP headers sent with each request
- **sensitive_patterns**: these will bypass the path depth limit
- **allowed_file_extensions**: File types to crawl (e.g., `"html"`, `"js"`)
These have default set, but can be modified:
- **max_workers**: Number of concurrent async workers
- **max_time**: Maximum crawl duration (seconds)
- **valid_external_domains**: External domains allowed for crawling
- **max_path_depth**: Maximum URL path segments
- **max_crawl_depth**: Maximum crawl recursion depth
- **breadth_first_search**: Use BFS (`True`) or DFS (`False`)

### 4. Start Crawling

Specify your target domains in `main.py`:

```python
line 36: for domain in ("example1.com", "example2.com", "example3.com"):
```

Run the crawler:

```bash
python main.py
```

### 5. View Results

Crawl results are saved in the `results/` directory as JSON files, one per domain. Each file contains:

- Discovered URLs (successful, unsuccessful, not requested)
- Crawl statistics (duration, stop reason, etc.)

---

**Tip:** Adjust configuration parameters to fit your target website and crawling goals.
```
## Architecture Overview

```
Domain Input → Initial URLs → Queue → Worker Pool → URL Validation → HTTP Request → Link Extraction → Queue
                                 ↓
                            Stored URLs (Results)
```

## 🔧 Core Components

### CrawlerConfiguration

Pydantic model defining crawler parameters:

    headers: dict[str, str]                      # HTTP headers for requests
    sensitive_patterns: tuple[str, ...]          # URL patterns to prioritize even beyond max depth
    allowed_file_extensions: tuple[str, ...]     # File extensions to crawl
    max_workers: int = Field(gt=0, default=2)    # Number of async workers
    max_time: int = Field(gt=0, default=60)      # Maximum crawling time in seconds
    valid_external_domains: tuple[str, ...] = Field(default=("github.com",))  # External domains to crawl
    max_path_depth: int = Field(gt=0, lt=21, default=3)     # Maximum URL path depth
    max_crawl_depth: int = Field(gt=0, lt=21, default=15)   # Maximum crawling depth
    breadth_first_search: bool = Field(default=True)        # BFS vs DFS crawling strategy

### Crawler Class

Main crawler orchestrator managing:

- **Worker pool**: Async workers consuming URLs from shared queue
- **URL state tracking**: Dictionary storing `[depth, status, http_code]` per URL
- **Queue management**: Async queue of `(url, depth, extension)` tuples
- **Stop conditions**: Time limits, rate limiting (429), empty queue

## 👷 Worker Behavior

Each worker performs the following operations:

1. Consumes URLs from shared async queue
2. Sends HTTP requests with configured headers
3. Extracts links from response body
4. Validates and queues new URLs (if within depth limits)
5. Updates URL state in shared storage
6. **Stops on**: timeout, 429 status, or empty queue
7. Sends sentinel values to terminate other workers

## ✨ Key Features

- **Modern framework**: asyncio and aiohttp for efficient asynchronous HTTP requests
- **I-O bound**: crawling speed mostly depends on network waiting time
- **High configurability**: path depth, crawling depth, sensitive patterns, extensions, external URLs control
- **Targeted crawling**: with lxml and Tree Sitter parsing of HTML and JS, it targets places where URLs are most commonly found
- **Smart URL extraction**: Specialized parsers for HTML, JavaScript and robots.txt. Other scripts are just regexed for absolute URLs
- **Domain awareness**: Respects domain boundaries with configurable external domain allowlist
- **Intelligent URL validation**: Filters URLs based on extensions, path depth, and sensitive patterns
- **Flexible search strategies**: Supports both breadth-first and depth-first crawling


## 📤 Output Format

```json
{
    "domain": "example.com",
    "stop_reason": "Empty Queue",
    "crawling_time": 45.2,
    "number_of_urls": 120,
    "urls": {
        "successful_requests": {
            "https://example.com/": [1, "Crawled", 200],
            "https://example.com/about": [2, "Crawled", 200]
        },
        "unsuccessful_requests": {
            "https://example.com/missing": [2, "Crawled", 404]
        },
        "not_requested": {
            "https://example.com/too-deep": [11, "max_crawl_depth_reached", 900]
        }
    }
}
```

### Stop Reason Values
- `"Ran out of time"`: Crawler reached the configured maximum time limit
- `"Empty Queue"`: No more URLs to crawl
- `"429 status code"`: Rate limiting detected (server returned a single HTTP 429, crawler stops at the first)

## 🔍 URL Validation

The crawler validates URLs through multiple steps:

1. **Domain validation**: Determines if URL is local or external to the target domain
2. **Local URL validation**: Checks file extensions, path depth and sensitive patterns
3. **External URL validation**: Verifies against the allowed external domains list