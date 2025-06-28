import feedparser
from datetime import datetime
from xml.sax.saxutils import escape

RSS_FEED_URL = "https://www.thoughtdigestmedia.com.au/news-feed.xml"
SITE_NAME = "Thought Digest Media"
LANGUAGE = "en-AU"

def fetch_articles():
    feed = feedparser.parse(RSS_FEED_URL)
    return feed.entries[:10]  # Limit to latest 10 articles

def format_article(entry):
    title = escape(entry.title)
    link = escape(entry.link)
    pub_date = datetime(*entry.published_parsed[:6]).isoformat() + "+00:00"
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

def generate_sitemap():
    articles = fetch_articles()
    items = "\n".join(format_article(entry) for entry in articles)

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
{items}
</urlset>
"""
    with open("news-sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)

if __name__ == "__main__":
    generate_sitemap()
