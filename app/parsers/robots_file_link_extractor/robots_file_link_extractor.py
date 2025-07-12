def extract_links_from_robots_file(robots_body: str) -> list[str]:
    """
    Extract all absolute and relative URLs from robots.txt files from disallow,
    allow and sitemap directives. Returns a list with the extracted
    URLs (not validated or resolved. That's carried out it url/url_validation.py)
    """

    urls_from_robots: list[str] = []

    for line in robots_body.splitlines():
        clean_line = line.strip()
        if not line or line.startswith("#"):
            continue

        clean_line = clean_line.lower()

        if clean_line.startswith(("disallow:", "allow:", "sitemap:")):
            try:
                directive, value = clean_line.split(":", 1)
                value = value.strip()
                if not value:
                    continue
                    
                # Handle sitemap URLs (usually full URLs)
                if directive == "sitemap":
                    urls_from_robots.append(value)

                # Handle Allow/Disallow paths
                else:
                    # Only add if it seems like a valid path
                    if value.startswith('/'):
                        urls_from_robots.append(value)
            except IndexError:
                continue

    return urls_from_robots 
