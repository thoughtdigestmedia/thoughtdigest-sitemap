import feedparser
from datetime import datetime, timedelta
from xml.sax.saxutils import escape

# CONFIG
RSS_FEED_URL = "https://www.thoughtdigestmedia.com.au/news-feed.xml"
SITE_NAME = "Thought Digest Media"
LANGUAGE = "en-AU"
OUTPUT_FILE = "news-sitemap.xml"
MAX_ARTICLES = 100  # Keep it under 1000 for Google News
DAYS_LIMIT = 2      # Google News requires 48-hour recency

# FETCH ARTICLES (only last 48 hours)
def fetch_articles():
    feed = feedparser.parse(RSS_FEED_URL)
    recent_cutoff = datetime.utcnow() - timedelta(days=DAYS_LIMIT)
    fresh_entries = [
        entry for entry in feed.entries
        if hasattr(entry, 'published_parsed') and
        datetime(*entry.published_parsed[:6]) > recent_cutoff
    ]
    return fresh_entries[:MAX_ARTICLES]

# FORMAT SINGLE ENTRY
def format_article(entry):
    title = escape(entry.title)
    link = escape(entry.link)
    pub_date = datetime(*entry.published_parsed[:6]).isoformat() + "+00:00"

    # Optional fallbacks
    author = escape(entry.get("author", "Thought Digest Media"))
    category = escape(entry.get("tags", [{}])[0].get("term", "News")) if entry.get("tags") else "News"

    return f"""
  <url>
    <loc>{link}</loc>
    <news:news>
      <news:publication>
        <news:name>{SITE_NAME}</news:name>
        <news:language>{LANGUAGE}</news:language>
      </news:publication>
      <news:publication_date>{pub_date}</news:publication_date>
      <news:title>{title}</news:title>
    </news:news>
  </url>"""

# GENERATE FULL SITEMAP
def generate_sitemap():
    articles = fetch_articles()
    items = "\n".join(format_article(entry) for entry in articles)

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
{items}
</urlset>
"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"Generated {OUTPUT_FILE} with {len(articles)} articles.")

if __name__ == "__main__":
    generate_sitemap()
