from lxml import etree  # type: ignore
from typing import Any

from app.parsers.parsers_heuristics import INTERESTING_ELEMENTS_ATTRIBUTES_MAP
from app.url.helpers.url_heuristics import absolute_url_pattern


def extract_links_from_tag(tag: etree._Comment | Any, found_urls: list[str]) -> None:
    """
    Extracts URLs from an HTML tag or comment node and appends them to the provided list.

    - If the tag is an lxml comment node, URLs are extracted from the comment text using a regex pattern.
    - If the tag is an element and its tag name is present in INTERESTING_ELEMENTS_ATTRIBUTES_MAP,
      URLs are extracted from the specified attributes:
        - For elements like 'button', 'script', or 'a', attribute values may contain URLs directly or within parentheses (e.g., JavaScript handlers).
          In such cases, URLs are extracted either by direct value or by regex if parentheses are present.
        - For other elements, attribute values are treated as direct URLs.

    All found URLs are appended to the passed-in found_urls list if not already present.

    Args:
        tag: An lxml element or comment node.
        found_urls: A list to which discovered URLs will be appended.

    Returns:
        None
    """

    if isinstance(tag, etree._Comment):
        _extract_urls_from_comment(tag, found_urls)
    else:
        _extract_url_from_element(tag, found_urls)


def _extract_url_from_element(element, found_urls: list[str]) -> None:
    """Extract URLs from an HTML element's attributes based on INTERESTING_ELEMENTS_ATTRIBUTES_MAP.
    Applies regex if a complex scenario is expected, else treat attribute value directly as a URL
    """

    element_type = element.tag

    if element_type not in INTERESTING_ELEMENTS_ATTRIBUTES_MAP:
        return
    else:
        
        interesting_attributes_for_this_element = INTERESTING_ELEMENTS_ATTRIBUTES_MAP[element_type]

        if element_type in ("button", "script", "a"):

            for attribute in interesting_attributes_for_this_element:
                attribute_value = element.get(attribute, None)
                if attribute_value is None:
                    continue
                if "(" in attribute_value:
                    extract_url_from_parenthesis_in_attribute(attribute_value, found_urls)
                elif attribute_value not in found_urls:
                    found_urls.append(attribute_value)

        else:
            for attribute in interesting_attributes_for_this_element:
                found_url = element.get(attribute, None)
                if found_url and found_url not in found_urls:
                    found_urls.append(found_url)

def extract_url_from_parenthesis_in_attribute(attribute_value: str, found_urls: list[str]) -> None:
    """Extract URLs from cases like this: onclick='window.open('URL')'"""
    # Use regex to find URLs instead of just parentheses content
    urls = absolute_url_pattern.findall(attribute_value)
    for url in urls:
        if url and url not in found_urls:
            found_urls.append(url)


def _extract_urls_from_comment(comment: etree._Comment, found_urls: list[str]) -> None:
    """Extract all absolute URLs from an HTML comment node using the absolute_url_pattern regex."""

    comment_text = str(comment)
    regexed_absolute_urls = absolute_url_pattern.findall(comment_text)
    if regexed_absolute_urls:
        for url in regexed_absolute_urls:
            if url and url not in found_urls:
                found_urls.append(url)
