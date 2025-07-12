from lxml import html, etree  # type: ignore


def get_html_dom(body: str) -> html.HtmlElement:
    """Get the DOM from a string containing HTML content.
    This function parses the HTML content with lxml and returns the root element of the DOM tree.
    In case of parsing failure, return None.
    """

    try:
        return html.fromstring(body)
    except (etree.ParserError, etree.XMLSyntaxError, TypeError, ValueError):
        return None
