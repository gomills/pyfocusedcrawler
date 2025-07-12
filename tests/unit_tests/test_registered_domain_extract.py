import pytest
from app.crawler.crawler_helpers import get_registered_domain

@pytest.mark.parametrize("input_url, base_domain, expected_match", [
    ("https://www.googletagmanager.com/gtag/js?id=G-FESFSF3F", "www.exampling.org", False),
    ("http://www.facebook.com/sharer.php?u=https%3A%25sggd5dfg5dftvstd5g%C3%ADa", "facebook.com", True),
    ("example.com", "example.com", True),
    ("www.example.com", "example.com", True),
    ("api.example.com", "example.com", True),
    ("dev.example.com", "example.com", True),
    ("mail.api.example.com", "example.com", True),
    ("www.example.co.uk", "example.co.uk", True),
    ("news.example.co.uk", "example.co.uk", True),
    ("www.fakeexample.com", "example.com", False),
    ("example.com.evil.com", "example.com", False),
    ("example.org", "example.com", False),
    ("", "example.com", False),
])
def test_registered_domain_match(input_url, base_domain, expected_match):
    normalized_input = get_registered_domain(input_url)
    normalized_base = get_registered_domain(base_domain)
    assert (normalized_input == normalized_base) == expected_match