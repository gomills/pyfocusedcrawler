from urllib.parse import urlparse
import os


def get_path_and_extension(url: str) -> tuple[str, str]:
    """Extract the path and extension from an absolute URL.
    Return url_path, url_ext"""

    url_path = urlparse(url).path
    _, url_ext = os.path.splitext(url_path)
    return url_path, url_ext


def get_path_depth(url_path: str) -> int:
    """Calculate the depth of a URL path."""

    return len([seg for seg in url_path.split("/") if seg])