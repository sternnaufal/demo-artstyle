"""Generate sitemap.xml untuk demo.naufalrakha.my.id dari daftar file HTML."""
import os
import re
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://demo.naufalrakha.my.id"
TODAY = date.today().isoformat()

SKIP = {"index.html", "about.html", "contact.html", "privacy.html"}

PRIORITY = {
    "index.html": ("1.0", "weekly"),
    "about.html": ("0.6", "monthly"),
    "contact.html": ("0.5", "monthly"),
    "privacy.html": ("0.3", "yearly"),
}

html_files = sorted(
    f for f in os.listdir(BASE)
    if f.endswith(".html") and os.path.isfile(os.path.join(BASE, f))
)

urls = []
for f in html_files:
    loc = f"{SITE}/" if f == "index.html" else f"{SITE}/{f}"
    priority, changefreq = PRIORITY.get(f, ("0.7", "monthly"))
    urls.append((loc, priority, changefreq))

xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for loc, priority, changefreq in urls:
    xml += "  <url>\n"
    xml += f"    <loc>{loc}</loc>\n"
    xml += f"    <lastmod>{TODAY}</lastmod>\n"
    xml += f"    <changefreq>{changefreq}</changefreq>\n"
    xml += f"    <priority>{priority}</priority>\n"
    xml += "  </url>\n"
xml += "</urlset>\n"

out = os.path.join(BASE, "sitemap.xml")
with open(out, "w", encoding="utf-8") as fh:
    fh.write(xml)

print(f"Generated sitemap with {len(urls)} URLs -> sitemap.xml")
