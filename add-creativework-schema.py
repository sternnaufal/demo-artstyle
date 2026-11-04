"""Tambahkan schema CreativeWork/WebPage ke setiap halaman gaya demo.

Data diambil dari <script id="designData"> yang sudah ada di tiap halaman.
Idempotent: halaman yang sudah punya schema CreativeWork akan dilewati.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://demo.naufalrakha.my.id"
COLLECTION_URL = f"{SITE}/"
CREATOR = {
    "@type": "Person",
    "name": "Naufal Rakha Putra",
    "url": "https://www.naufalrakha.my.id/",
}

pattern = re.compile(
    r'<script type="application/json" id="designData">(.*?)</script>',
    re.DOTALL,
)

updated = 0
skipped = 0

for path in sorted(ROOT.glob("*.html")):
    html = path.read_text(encoding="utf-8")
    match = pattern.search(html)
    if not match:
        continue

    if '"@type": "CreativeWork"' in html or '"CreativeWork"' in html:
        skipped += 1
        continue

    data = json.loads(match.group(1))
    url = f"{SITE}/{path.name}"

    schema = {
        "@context": "https://schema.org",
        "@type": ["WebPage", "CreativeWork"],
        "name": data.get("title") or path.stem,
        "description": data.get("description", ""),
        "url": url,
        "inLanguage": "id",
        "genre": "Web Design",
        "keywords": ", ".join(
            filter(
                None,
                [
                    "web design",
                    "art style",
                    data.get("title", ""),
                    data.get("best", ""),
                ],
            )
        ),
        "creator": CREATOR,
        "isPartOf": {
            "@type": "CollectionPage",
            "name": "Demo Style Gallery",
            "url": COLLECTION_URL,
        },
        "image": f"{SITE}/og-image.png",
    }

    tag = (
        '  <script type="application/ld+json">\n'
        f'    {json.dumps(schema, ensure_ascii=False, indent=4).replace(chr(10), chr(10) + "    ")}\n'
        "  </script>\n"
    )
    html = html.replace("</head>", f"{tag}</head>", 1)
    path.write_text(html, encoding="utf-8")
    updated += 1

print(f"OK: added CreativeWork schema to {updated} pages ({skipped} already had it).")
