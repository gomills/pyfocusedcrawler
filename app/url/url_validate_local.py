from app.url.helpers.url_path_operations import get_path_and_extension, get_path_depth
from app.url.helpers.url_heuristics import COMMON_JS_LIBRARY_FILE_REGEX


def validate_local_url(
    url: str,
    allowed_file_extensions: tuple,
    max_url_path_depth: int,
    sensitive_patterns: tuple,
) -> tuple[str | None, str | None]:
    """
    Validate a local URL based on allowed extensions, path depth, and sensitive patterns.

    If it's an allowed extension other than .html (aka, it's a script), return the URL directly.
    If it's .html and path depth is less than the maximum return directly. If it's more than the maximum, only
    return it if it contains a sensitive pattern

    Returns:
        url, url_extension
    """

    url_path, url_extension = get_path_and_extension(url)
    if url_extension and url_extension not in allowed_file_extensions:
        return None, None

    elif not url_extension or url_extension in (".html", ".htm"):
        return _handle_subpages(
            url, url_path, max_url_path_depth, sensitive_patterns
        ), ".html"

    elif url_extension == ".js":
        return _handle_javascript_urls(url, url_path), ".js"

    else:
        return url, url_extension


def _handle_subpages(
    url: str, url_path: str, max_url_path_depth: int, sensitive_patterns: tuple
) -> str | None:
    """Handle subpages by checking path depth and sensitive patterns."""

    url_path_depth = get_path_depth(url_path)
    if url_path_depth <= max_url_path_depth:
        return url
    elif _sensitive_pattern_found(url_path, sensitive_patterns):
        return url
    else:
        return None


def _handle_javascript_urls(url: str, url_path: str) -> str | None:
    """
    Handle javascript-files urls. We avoid most common javascript library files.
    Returns the url if it's not a common js library file, else None
    """

    return url if not COMMON_JS_LIBRARY_FILE_REGEX.search(url_path) else None


def _sensitive_pattern_found(url_path: str, sensitive_patterns: tuple) -> bool:
    """Check if any sensitive pattern is found in the URL path."""

    for pattern in sensitive_patterns:
        if pattern in url_path:
            return True
    return False
