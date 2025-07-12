from app.parsers.robots_file_link_extractor.robots_file_link_extractor import extract_links_from_robots_file 

def test_extract_links_from_robots_file():
    robots_txt = """
    # Example robots.txt file

    User-agent: *
    Disallow: /private/
    Disallow: /tmp/
    Allow: /public/info.html
    Sitemap: https://example.com/sitemap.xml

    User-agent: Googlebot
    Disallow: /nogoogle/

    # Empty lines and random formatting
    Disallow:       /weird-path/
    Allow:/tight.html
    Sitemap:    https://example.com/sitemap2.xml
    """

    expected = [
        "/private/",
        "/tmp/",
        "/public/info.html",
        "https://example.com/sitemap.xml",
        "/nogoogle/",
        "/weird-path/",
        "/tight.html",
        "https://example.com/sitemap2.xml",
    ]

    result = extract_links_from_robots_file(robots_txt)
    assert result == expected

def test_extract_links_from_robots_file_empty_and_comments():
    # Empty robots.txt
    assert extract_links_from_robots_file("") == []
    # Only comments and whitespace
    robots_txt = """
    # This is a comment
    # Another comment
    
    """
    assert extract_links_from_robots_file(robots_txt) == []

def test_extract_links_from_robots_file_invalid_lines():
    # Lines with missing value after directive
    robots_txt = """
    Disallow:
    Allow:
    Sitemap:
    """
    assert extract_links_from_robots_file(robots_txt) == []

    # Lines with no colon
    robots_txt = """
    Disallow /no-colon
    Allow /no-colon
    Sitemap https://example.com/no-colon
    """
    assert extract_links_from_robots_file(robots_txt) == []
