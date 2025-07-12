from app.url.helpers.url_path_operations import get_path_and_extension


def validate_external_url(url: str, allowed_external_domains: tuple) -> tuple[str | None, str | None]:
    """
    Validate a external URL by checking if it's from an allowed external domain.
    """
    
    _, url_extension = get_path_and_extension(url)
    for domain in allowed_external_domains:
        if domain in url:
            return url, url_extension
    return None, None
