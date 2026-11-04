"""Ganti link internal 'index.html' menjadi '/' di semua halaman demo.

Tujuan: menghindari Google menemukan /index.html sebagai halaman alternatif.
"""
from pathlib import Path

updated = 0
for path in sorted(Path(__file__).resolve().parent.glob("*.html")):
    html = path.read_text(encoding="utf-8")
    if 'href="index.html"' not in html:
        continue
    path.write_text(html.replace('href="index.html"', 'href="/"'), encoding="utf-8")
    updated += 1

print(f"OK: updated {updated} files")
