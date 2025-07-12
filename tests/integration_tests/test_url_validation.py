import pytest
from app.url.helpers.url_heuristics import sensitive_patterns, allowed_file_extensions  # noqa: E402
from app.url.url_validation import validate_string_for_url  # noqa: E402
from app.crawler.crawler_helpers import get_registered_domain

"""Integration test for URL validation functions.
These tests check the validation of URLs based on a set of heuristics and domain settings.
The tests cover both absolute and relative URLs..
It DOES NOT test wether URLs are formatted correctly, but rather if the code applies correctly
the heuristics.
"""


domain = "www.example.com"
registered_domain= get_registered_domain(domain)
valid_external_domains = ("github.com",)
max_path_depth = 1


valid_absolute_urls = (
    "https://example.com/a",
    "https://example.com/bb/a/3f/sf.txt", 
    "//example.com/a/b/c.js", 
    "//example.com/a/b/fsf/c.git",
    "example.com/a",
    "https://example.com/fe/s/afe/safesa/dashboard",
    "https://example.com/test",
    "https://github.com/private/repo/example",
    "https://example.com/a/b/dashboard",
    "https://testing.example.com/a/b/dashboard"
)
invalid_absolute_urls = (
    "https://example.com/a/b/",
    "https://cdn.example.com/libs/jquery.min.js",
    "https://example.com/jquery.min.js",
    "https://example.com/a/b",
    "https://example.com/a/b/c#section",
    "https://youtube.com/a/b/c",
    "https://youtube.com",
    "//example.com/a/b/c.html",
    "example.com/a/b/c.htm",
    "fes ojfeio oiejfisofjesio",
    "https is a internet protocol",
    "https://www.youtube.com/embed/ZipKoVUSWlY?rel=0&modestbranding=1&wmode=opaque"
)

# Relative URLs that should give Trueish and Falsy for this crawl settings.
valid_relative_urls = (
    "/a/b/c.js?query=1111", # failed
    "/a/b/c.txt", # failed
    "/afesfesf",
    "/?q=user/login",
    "/esfes/private?query"
    )

invalid_relative_urls = (
    "/a/b/c", 
    "/a/b/c*extra", 
    "/fesfs/fesfe/fesfefs/v",
    "/ fesioj ifoesjifoe"
    )

# Test Trueish URLs
total_valid_urls = valid_absolute_urls + valid_relative_urls
@pytest.mark.parametrize("possible_url", total_valid_urls)
def test_trueish_url_validation(possible_url: str):
    result, _ = validate_string_for_url(
        possible_url=possible_url,
        domain=domain,
        registered_domain=registered_domain,
        allowed_file_extensions=allowed_file_extensions,
        max_path_depth=max_path_depth,
        sensitive_patterns=sensitive_patterns,
        valid_external_domains=valid_external_domains
    )
    assert bool(result) is True

# Test Falsy URLs
total_invalid_urls = invalid_absolute_urls + invalid_relative_urls
@pytest.mark.parametrize("possible_url", total_invalid_urls)
def test_falsy_url_validation(possible_url: str):
    result, _ = validate_string_for_url(
        possible_url=possible_url,
        domain=domain,
        registered_domain=registered_domain,
        allowed_file_extensions=allowed_file_extensions,
        max_path_depth=max_path_depth,
        sensitive_patterns=sensitive_patterns,
        valid_external_domains=valid_external_domains
    )
    assert not result
