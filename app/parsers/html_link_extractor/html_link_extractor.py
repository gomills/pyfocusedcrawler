from lxml import html  # type: ignore

from app.parsers.html_link_extractor.html_tags_extractors.html_tags_extractors import extract_links_from_tag
from app.parsers.html_link_extractor.html_parser import get_html_dom


def extract_links_from_html(body: str) -> list[str] | None:
    """
    Parses the input HTML string using lxml and recursively searches for URLs within the resulting DOM tree.
    The extraction focuses on specific HTML elements as defined in parsers/parsers_heuristics.py.
    For most attributes, their content is directly treated as a URL. In more complex cases—such as when
    an attribute contains JavaScript code with embedded URLs (e.g., <button onclick="window.open('http...')")—
    a regular expression is used to extract absolute URLs (support for relative URLs may be added later).

    Returns:
        A list of all extracted URLs, or None if no URLs are found/parsing fails.
        Note: URL validation is not performed here; see url/url_validation.py for validation logic.
    """

    # Get the DOM from a supposedly HTML string
    html_dom = get_html_dom(body)
    if html_dom is None or len(html_dom) == 0:
        return None

    # Traverse the DOM in search of urls
    urls = _traverse_html_tree_for_links(html_dom)

    return urls

def _traverse_html_tree_for_links(html_tree: html.HtmlElement) -> list[str]:
    """Traverse the HTML tree and extract all URLs from it.
    This function iterates through all elements and comments in the HTML tree,
    extracting URLs from specific attributes and comments."""

    found_urls: list[str] = []
    for tag in html_tree.iter():
        extract_links_from_tag(tag, found_urls)
    return found_urls

