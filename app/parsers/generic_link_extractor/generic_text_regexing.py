from app.url.helpers.url_heuristics import absolute_url_pattern

def regex_text_for_links(body: str) -> list[str] | None:
    """Extracts all absolute URLs from the given text body using a regex.
    Returns:
     list with all found urls, else None
     """
    
    return absolute_url_pattern.findall(body)
    