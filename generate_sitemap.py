import feedparser
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

RSS_FEED = "https://www.thoughtdigestmedia.com.au/blog-feed.xml"
SITEMAP_PATH = Path("news-sitemap.xml")
MAX_ITEMS = 10

def fetch_latest_rss_items():
    feed = feedparser.parse(RSS_FEED)
    items = []
    for entry in feed.entries:
        pub_date = datetime(*entry.published_parsed[:6])
        items.append({
            'title': entry.title,
            'link': entry.link,
            'pub_date': pub_date,
        })
    items.sort(key=lambda x: x['pub_date'], reverse=True)
    return items[:MAX_ITEMS]

def generate_sitemap(items):
    NSMAP = {
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'xmlns:news': 'http://www.google.com/schemas/sitemap-news/0.9',
    }
    urlset = ET.Element("urlset", NSMAP)

    for item in items:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = item['link']

        news = ET.SubElement(url, "news:news")
        pub = ET.SubElement(news, "news:publication")
        ET.SubElement(pub, "news:name").text = "Thought Digest"
        ET.SubElement(pub, "news:language").text = "en"

        ET.SubElement(news, "news:publication_date").text = item['pub_date'].isoformat()
        ET.SubElement(news, "news:title").text = item['title']

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    tree.write(SITEMAP_PATH, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_sitemap(fetch_latest_rss_items())
