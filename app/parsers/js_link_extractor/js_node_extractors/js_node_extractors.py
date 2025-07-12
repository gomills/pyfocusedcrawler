from tree_sitter import Node

from app.parsers.generic_link_extractor.generic_text_regexing import regex_text_for_links


def extract_links_from_node(node: Node, found_urls: list[str], js_code: str) -> None:
    """
    Recursively extract links from JavaScript AST nodes. Only pays attention to 
    strings that are inside common-URL-containing blocks in .js (see _process_string_node()).

    Args:
        node (Node): The current AST node.
        found_urls (list[str]): List to collect found URLs.
        js_code (str): The JavaScript source code.

    Returns: None, the URLs are appended in-situ to the passed list
    """

    if not node:
        return

    # Check if the current node is a string (inside "" or '') or a template_string (inside ``)
    if node.type in ("string", "template_string"):
        # Check the parent node's type
        parent = node.parent
        _process_string_node(parent=parent, node=node, js_code=js_code, found_urls=found_urls)

    elif node.type == "comment":
        regexed_urls = _extract_urls_from_string(node, js_code)
        if regexed_urls:
            found_urls.extend(regexed_urls)

    # Recursively traverse children
    for child in node.children:
        extract_links_from_node(child, found_urls, js_code)

    return


def _process_string_node(parent: Node | None, node: Node, js_code: str, found_urls: list[str]) -> None:
    """
    Process string&template string nodes to extract URLs.
    Walks up the parent chain in the nodes' CST to check for 
    relevant block types, known for containing URLs in .js files.
    Returns: None, the URLs are appende to the passed list
    """

    if not parent:
        return

    # Walk up the parent chain to check for relevant types
    relevant_types = {
        "call_expression","arguments","import_statement",
        "pair","binary_expression","assignment_pattern",
        "variable_declarator","assignment_expression",
    }

    ancestor = parent
    while ancestor is not None:
        if ancestor.type in relevant_types:
            possible_urls = _extract_urls_from_string(node, js_code)
            if possible_urls:
                found_urls.extend(possible_urls)
            break
        ancestor = ancestor.parent  # type: ignore
    return


def _extract_urls_from_string(node: Node, js_code: str) -> list[str] | None:
    """Extract absolute URLs strings from a node, applying regex.

    Args:
        node: The string/template node
        js_code: The JavaScript source code
        is_template: Whether the node is a template string

    Returns:
        The extracted URL string or None if invalid
    """

    node_string = js_code[node.start_byte : node.end_byte].strip("\"'`").strip()

    if not node_string or len(node_string) >= 1000:
        return None

    return regex_text_for_links(node_string)
