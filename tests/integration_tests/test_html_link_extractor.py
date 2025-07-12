from app.parsers.html_link_extractor.html_link_extractor import extract_links_from_html

test_simple_html = """
<html>
  <body>
    <a href="https://example.com/test-url1"></a>
    <script 
      src="https://example.com/test-url2"
      content="https://example.com/test-url3"
      href="https://example.com/test-url4"
      onclick="https://example.com/test-url5"
      action="https://example.com/test-url6"
      formaction="https://example.com/test-url7"
      codebase="https://example.com/test-url8">
    </script>
    <link href="https://example.com/test-url9" src="https://example.com/test-url10">
    <form action="https://example.com/test-url11"></form>
    <object data="https://example.com/test-url12"></object>
    <button onclick="https://example.com/test-url13"></button>
    <embed src="https://example.com/test-url14"></embed>
    <iframe src="https://example.com/test-url15"></iframe>
  </body>
</html>
"""

test_semi_realistic_html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Deep Test Page</title>
    <link rel="stylesheet" href="https://example.com/test-url1" />
    <script src="https://example.com/test-url2"></script>
  </head>
  <body>
    <header>
      <div class="top-bar">
        <nav>
          <ul>
            <li><a href="https://example.com/test-url3">Dashboard</a></li>
          </ul>
        </nav>
      </div>
    </header>

    <main>
      <section id="content">
        <article>
          <form action="https://example.com/test-url4">
            <fieldset>
              <legend>Contact Us</legend>
              <div class="form-row">
                <button type="submit" onclick="https://example.com/test-url5">Send</button>
              </div>
            </fieldset>
          </form>
        </article>
        <article>
          <div class="media">
            <object data="https://example.com/test-url6">
              <embed src="https://example.com/test-url7" />
            </object>
            <div class="video-container">
              <iframe src="https://example.com/test-url8" width="560" height="315"></iframe>
            </div>
          </div>
        </article>
      </section>
    </main>

    <aside>
      <div class="resources">
        <link href="https://example.com/test-url9" rel="alternate" />
        <script
          content="https://example.com/test-url10"
          href="https://example.com/test-url11"
          onclick="https://example.com/test-url12"
          action="https://example.com/test-url13"
          formaction="https://example.com/test-url14"
          codebase="https://example.com/test-url15">
        </script>
      </div>
    </aside>

    <footer>
      <p>&copy; 2025 Example Co.</p>
    </footer>

    <!-- Note: archived endpoint https://example.com/test-url16 -->
  </body>
</html>
"""

test_realistic_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechNews - Latest Technology Updates</title>
    
    <!-- CSS and external resources -->
    <link rel="stylesheet" href="https://cdn.example.com/css/bootstrap.min.css">
    <link rel="alternate" type="application/rss+xml" href="https://technews.example.com/feed.xml">
    
    <!-- Analytics and tracking scripts -->
    <script src="https://analytics.google.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
</head> 
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-brand">
            <a href="https://technews.example.com">TechNews</a>
        </div>
        <ul class="nav-menu">
            <li><a href="https://technews.example.com/categories/ai">AI News</a></li>
        </ul>
    </nav>

    <!-- Main content -->
    <main>
        <article class="featured-article">
            <h1>Breaking: New AI Model Released</h1>
            <div class="article-meta">
                <a href="https://technews.example.com/authors/john-doe">By John Doe</a>
                <time datetime="2025-07-10">July 10, 2025</time>
            </div>
            
            <!-- Embedded media -->
            <div class="media-container">
                <iframe src="https://youtube.com/embed/dQw4w9WgXcQ" 
                        width="560" height="315" frameborder="0"></iframe>
            </div>
            
            <!-- Social sharing -->
            <div class="social-share">
                <button onclick="window.open('https://twitter.com/intent/tweet?url=https://technews.example.com/ai-model-release', '_blank')">
                    Share on Twitter
                </button>
                <button onclick="shareOnFacebook('https://facebook.com/sharer/sharer.php?u=https://technews.example.com/ai-model-release')">
                    Share on Facebook
                </button>
            </div>
        </article>

        <!-- Comment form -->
        <section class="comments">
            <h3>Leave a Comment</h3>
            <form action="https://technews.example.com/api/comments" method="post">
                <textarea name="comment" placeholder="Your thoughts..."></textarea>
                <button type="submit" formaction="https://technews.example.com/api/comments/submit">
                    Post Comment
                </button>
            </form>
        </section>

        <!-- Related articles -->
        <aside class="sidebar">
            <h3>Related Articles</h3>
            <div class="related-links">
                <a href="https://technews.example.com/articles/machine-learning-trends">ML Trends 2025</a>
            </div>
            
            <!-- Advertisement -->
            <div class="ad-container">
                <object data="https://ads.example.com/banner.swf" type="application/x-shockwave-flash">
                    <embed src="https://ads.example.com/fallback-banner.swf" 
                           type="application/x-shockwave-flash">
                </object>
            </div>
        </aside>
    </main> 

    <!-- Footer -->
    <footer>
        <div class="footer-links">
            <a href="https://technews.example.com/about">About Us</a>
            <a href="https://technews.example.com/contact">Contact</a>
        </div>
        
        <!-- Newsletter signup -->
        <form action="https://technews.example.com/newsletter/subscribe" class="newsletter">
            <input type="email" name="email" placeholder="Enter your email">
            <button type="submit">Subscribe</button>
        </form>
    </footer>

    <!-- External scripts with various attributes -->
    <script src="https://cdn.example.com/js/main.js" 
            content="https://technews.example.com/js/content.js"
            href="https://technews.example.com/js/backup.js"
            codebase="https://cdn.example.com/js/lib/">
    </script>

    <!-- Hidden legacy links and deprecated endpoints -->
    <!-- 
        Legacy API endpoints for reference:
        https://technews.example.com/api/v1/users
        Old CDN: https://old-cdn.example.com/assets/
    -->
    
    <!-- Analytics tracking -->
    <!-- Google Analytics: https://analytics.google.com/collect -->
</body>
</html>
"""




def test_extract_links_from_simple_html():
    """Test that the HTML link extractor correctly extracts URLs from various HTML elements and comments."""
    
    # Extract URLs from the test HTML
    extracted_urls = extract_links_from_html(test_simple_html)
    
    # Assert that URLs were found
    assert extracted_urls is not None
    for i in range(1, len(extracted_urls) + 1):
        assert f"https://example.com/test-url{i}" in extracted_urls
    assert len(extracted_urls) == 15

def test_extract_links_from_semi_realistic_html():

    extracted_urls = extract_links_from_html(test_semi_realistic_html)

    # Assert that URLs were found
    assert extracted_urls is not None
    for i in range(1, len(extracted_urls) + 1):
        assert f"https://example.com/test-url{i}" in extracted_urls
    assert len(extracted_urls) == 16

def test_extract_links_from_realistic_html():

    extracted_urls = extract_links_from_html(test_realistic_html)

    assert extracted_urls is not None
    realistic_urls = [
        "https://analytics.google.com/collect",
        "https://technews.example.com/api/v1/users",
        "https://old-cdn.example.com/assets/",
        "https://cdn.example.com/js/main.js" ,
        "https://technews.example.com/js/content.js",
        "https://technews.example.com/js/backup.js",
        "https://cdn.example.com/js/lib/",
        "https://technews.example.com/newsletter/subscribe",
        "https://technews.example.com/about",
        "https://technews.example.com/contact",
        "https://ads.example.com/fallback-banner.swf" ,
        "https://ads.example.com/banner.swf" ,
        "https://technews.example.com/articles/machine-learning-trends",
        "https://analytics.google.com/gtag/js?id=GA_MEASUREMENT_ID" ,
        "https://technews.example.com/feed.xml" ,
        "https://cdn.example.com/css/bootstrap.min.css",
        "https://technews.example.com",
        "https://technews.example.com/categories/ai",
        "https://technews.example.com/authors/john-doe",
        "https://youtube.com/embed/dQw4w9WgXcQ" ,
        'https://twitter.com/intent/tweet?url=https://technews.example.com/ai-model-release',
        "https://facebook.com/sharer/sharer.php?u=https://technews.example.com/ai-model-release",
        "https://technews.example.com/api/comments/submit",
        "https://technews.example.com/api/comments"
        ]
    
    # Check that all expected URLs are found
    for url in realistic_urls:
        assert url in extracted_urls, f"Missing URL: {url}"

    for url in extracted_urls:
        assert url in realistic_urls, f"Malformed URL: {url}"
    
    # Check that we have the expected number of URLs
    assert len(extracted_urls) == len(realistic_urls)

def test_extract_links_from_empty_html():
    """Test that the extractor handles empty or invalid HTML gracefully."""
    
    # Test with empty string
    result = extract_links_from_html("")
    assert result is None
    
    # Test with whitespace only
    result = extract_links_from_html("   \n\t   ")
    assert result is None
    
    # Test with non-HTML content
    result = extract_links_from_html("This is just plain text with no HTML tags")
    assert result is None or len(result) == 0

def test_extract_links_from_minimal_html():
    """Test that the extractor works with minimal valid HTML."""
    
    minimal_html = '<html><body><a href="https://example.com">Link</a></body></html>'
    result = extract_links_from_html(minimal_html)
    
    assert result is not None
    assert "https://example.com" in result