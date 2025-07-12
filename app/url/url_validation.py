from typing import Literal

from app.url.url_validate_external import validate_external_url
from app.crawler.crawler_helpers import get_registered_domain
from app.url.url_validate_local import validate_local_url

def validate_string_for_url(
        possible_url: str, 
        domain: str, 
        registered_domain: str,
        allowed_file_extensions: tuple[str, ...],
        max_path_depth: int,
        sensitive_patterns: tuple[str, ...],
        valid_external_domains: tuple[str, ...]
        ) -> tuple[str | None, str | None]:
    """Validate a string as a URL. Returns (valid and formatted url | None, url extension)."""

    # Begin cleaning by stripping whitespaces
    possible_url = possible_url.strip()

    # Carry out an initial check to discard obvious non-urls, such as random strings, normal text and malformed strings
    if not _pass_initial_check(possible_url):
        return None, None

    # All (possibly) URLs are cleaned, sanitized and converted to absolute URLs here for simplicity's sake. No more relative or incomplete URLs from here on.
    cleaned_url, is_local = _convert_string_to_url(possible_url, domain, registered_domain)

    if is_local:
        return validate_local_url(cleaned_url, allowed_file_extensions, max_path_depth, sensitive_patterns)
    else:
        return validate_external_url(cleaned_url, valid_external_domains)


def _pass_initial_check(possible_url: str) -> bool:
    """Heuristic check for possible random strings. Discard URL if:
    - too short or too long
    - contains whitespaces
    - has mailto string
    """

    if len(possible_url) < 3 or len(possible_url) > 300:
        return False
    elif " " in possible_url or possible_url.startswith("mailto") or "\n" in possible_url:
        return False
    else:
        return True


def _convert_string_to_url(possible_url: str, domain: str, registered_domain:str) -> tuple[str, bool]:
    """Clean and resolve a string as an absolute URL. Return the definitive URL and True if it's local"""

    cleaned_url = _clean_url(possible_url)
    return _solve_url(cleaned_url, domain, registered_domain)


def _clean_url(possible_url: str) -> str:
    """Remove fragments, asterisks, and add protocol if missing."""

    # remove url context, #(···)
    hashtag_index = possible_url.find("#")
    if hashtag_index != -1:
        possible_url = possible_url[0:hashtag_index]

    # remove *(···)
    asterisk_index = possible_url.find("*")
    if asterisk_index != -1:
        possible_url = possible_url[0:asterisk_index]

    # add protocol if missing
    if possible_url.startswith("//"):
        possible_url = "https:" + possible_url

    # Maybe this should be skipped? stripping trailing slash. Could conflict with path depth calculation
    cleaned_url = possible_url.rstrip("/")
    return cleaned_url


def _solve_url(possible_url: str, domain: str, registered_domain: str) -> tuple[str, bool]:
    """Determine if URL is relative or absolute and resolve it."""

    if possible_url.startswith("/"):
        return _handle_relative_url(possible_url, domain)
    else:
        return _handle_absolute_url(possible_url, registered_domain)


def _handle_relative_url(relative_url: str, domain: str) -> tuple[str, Literal[True]]:
    """Solve a relative URL to absolute using the domain. Return solved URL and True because it's local."""

    solved_url = "https://" + domain + relative_url
    return solved_url, True


def _handle_absolute_url(possible_url: str, registered_domain: str) -> tuple[str, bool]:
    """Ensure absolute URL has protocol and check if it is local. Return complete URL and a bool if it's local or external"""

    if not possible_url.startswith("http"):
        possible_url = "https://" + possible_url

    found_url_registered_domain = get_registered_domain(possible_url)
    
    return possible_url, found_url_registered_domain == registered_domain
