from app.parsers.generic_link_extractor.generic_text_regexing import regex_text_for_links

sample_text = """
# --- sample.xml ---
<?xml version="1.0" encoding="UTF-8"?>
<resources>
    <endpoint href="https://cdn.example.com/assets/script.js" />
</resources>

# --- config.php ---
<?php
$apiBase = "https://api.example.com/";
$authUrl = 'https://auth.example.com/login';
define("CDN_URL", "https://cdn.example.com/assets/");
?>

# --- data.json ---
{
  "api": "https://api.example.com/v2/data",
  "docs": "https://docs.example.com/spec",
  "fallback": "https://backup.example.com/service"
}

# --- .env ---
API_URL=https://env.example.com/api
CDN_ENDPOINT=https://env.example.com/static
AUTH_SERVICE_URL=https://env.example.com/auth

# --- config.yaml ---
api: https://yaml.example.com/api
cdn: https://yaml.example.com/assets/
docs: https://yaml.example.com/docs

"""
expected_urls= (
    "https://cdn.example.com/assets/script.js",
    "https://api.example.com/",
    'https://auth.example.com/login',
    "https://cdn.example.com/assets/",
    "https://api.example.com/v2/data",
    "https://docs.example.com/spec",
    "https://backup.example.com/service",
    "https://env.example.com/api",
    "https://env.example.com/static",
    "https://env.example.com/auth",
    "https://yaml.example.com/api",
    "https://yaml.example.com/assets/",
    "https://yaml.example.com/docs",
    )

def test_generic_text_regexing():

    urls = regex_text_for_links(sample_text)
    assert len(urls) == len(expected_urls), f"Expected {len(expected_urls)} URLs, got {len(urls)}"
    
    for url in expected_urls:
        assert url in urls, f"Expected URL '{url}' not found in extracted URLs"
    