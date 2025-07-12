from tree_sitter import Tree


from app.parsers.js_link_extractor.js_node_extractors.js_node_extractors import extract_links_from_node
from app.parsers.js_link_extractor.js_parser import get_js_tree

def extract_links_from_js(body: str) -> list[str] | None:
    """
    Extracts all URLs from a JavaScript source string.

    This function parses the input JavaScript code using Tree-Sitter, traverses the resulting CST,
    and extracts URLs from common URL-containing constructs (e.g., fetch(), XMLHttpRequest, etc.).
    For efficiency, only relevant (see js_node_extractors.py) code blocks are inspected to avoid
    regexing the whole document. Within these blocks, URLs are identified using regex patterns 
    that match both absolute and (not yet) relative URLs.

    Args:
        body (str): The JavaScript source code.

    Returns:
        list[str] | None: List of extracted URLs, or None if parsing fails or no URLs are found.
    """

    js_tree = get_js_tree(body) 
    if not js_tree:
        return None

    urls = _traverse_js_tree_for_links(js_tree, body)
    
    return urls

def _traverse_js_tree_for_links(js_tree: Tree, body: str) -> list[str]:
    """
    Traverse the JavaScript CST and extract links by processing the root node and its children
    (basically traversing the whole .js)

    Args:
        js_tree (Tree): The parsed JavaScript AST.
        body (str): The JavaScript source code.

    Returns:
        list[str]: List of extracted URLs.
    """

    found_urls: list[str] = []
    root_node = js_tree.root_node

    # Extract links from root node. Appending URLs to list is carried out by the function itself.
    extract_links_from_node(root_node, found_urls, body)

    return found_urls


