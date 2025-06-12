import feedparser
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

RSS_URL = "https://www.thoughtdigestmedia.com.au/blog-feed.xml"
MAX_ITEMS = 10
SITEMAP_FILE = "sitemap-news.xml"

feed = feedparser.parse(RSS_URL)

urlset = ET.Element("urlset", {
    "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "xmlns:news": "http://www.google.com/schemas/sitemap-news/0.9"
})

for entry in feed.entries[:MAX_ITEMS]:
    url = ET.SubElement(urlset, "url")
    loc = ET.SubElement(url, "loc")
    loc.text = entry.link

    news = ET.SubElement(url, "news:news")
    publication = ET.SubElement(news, "news:publication")

    name = ET.SubElement(publication, "news:name")
    name.text = "Thought Digest Media"

    language = ET.SubElement(publication, "news:language")
    language.text = "en-AU"

    pub_date = ET.SubElement(news, "news:publication_date")
    pub_date.text = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).isoformat()

    title = ET.SubElement(news, "news:title")
    title.text = entry.title

tree = ET.ElementTree(urlset)
tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)
