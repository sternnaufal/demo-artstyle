# fix-seo-all.py — demo-artstyle: GA4 + meta description + canonical + lang fix + regenerate sitemap
import os, glob, re, datetime

FOLDER = os.path.dirname(os.path.abspath(__file__))
DOMAIN = 'https://demo.naufalrakha.my.id'
GA_ID = 'G-R6Y4Y3XVGQ'

GTAG = f'''  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA_ID}');
  </script>'''

DESCRIPTIONS = {
    'about': 'Tentang Demo Artstyle — galeri 42 gaya desain web interaktif oleh Naufal Rakha Putra.',
    'contact': 'Kontak Naufal Rakha Putra — pembuat Demo Artstyle Gallery. Tersedia untuk kolaborasi desain web.',
    'privacy': 'Kebijakan Privasi Demo Artstyle Gallery. Data kunjungan tidak disimpan atau dibagikan.',
    'aero_frutiger': 'Aero Frutiger — gaya desain web dengan efek transparan, gradien aqua, dan estetika mid-2000an yang futuristik.',
    'barbiecore': 'Barbiecore — estetika hot pink bold, feminin, dan playful untuk landing page modern.',
    'bauhaus': 'Bauhaus — desain web minimalis dengan bentuk geometris murni, warna primer, dan tipografi sans-serif.',
    'bento_ui': 'Bento UI — layout asimetris berbentuk grid bento yang populer di dashboard dan landing page.',
    'biopunk': 'Biopunk — estetika futuristik organic dengan elemen bioluminesensi, hijau neon, dan tekstur biomassa.',
    'brutalism': 'Brutalism — desain web mentah tanpa dekorasi: warna default, border kasar, dan tipografi sistem.',
    'candy_pop': 'Candy Pop — palet warna cerah pastel dengan bentuk rounded yang manis dan playful.',
    'claymorphism': 'Claymorphism — UI dengan efek 3D lembut seperti tanah liat, shadow dalam, dan corner radius besar.',
    'constructivism': 'Constructivism — desain web avant-garde dengan diagonal tajam, merah-hitam, dan komposisi agresif.',
    'corporate_memphis': 'Corporate Memphis — ilustrasi blobby flat, warna pastel cerah, dan ilustrasi orang stylized.',
    'dada': 'Dada — desain web anti-art yang absurd, kolase chaos, dan tipografi yang sengaja rusak.',
    'de_stijl': 'De Stijl — neoplasticism web: garis horizontal-vertikal, kotak merah-biru-kuning-putih-hitam.',
    'glassmorphism': 'Glassmorphism — efek kaca transparan dengan backdrop-blur, border semi-transparent, dan gradien halus.',
    'gothic': 'Gothic — arsitektur Gotik di web: lengkung lancip, warna gelap, emas, dan tekstur batu.',
    'grunge': 'Grunge — estetika kasar: tekstur kotor, noise, font tangan, dan palet gelap bernuansa vintage.',
    'isometric': 'Isometric — ilustrasi 3D axonometric yang dipakai untuk UI dan elemen visual web.',
    'liminal_space': 'Liminal Space — estetika The Backrooms: koridor kosong, cahaya fluorescent, nuansa aneh.',
    'manga': 'Manga / Anime — gaya web bergaya komik Jepang: panel, speedline, dan tipografi bold.',
    'maximalism': 'Maximalism — desain web penuh warna, layer bertumpuk, tekstur berlebihan, dan tipografi eklektik.',
    'medieval': 'Medieval — estetika abad pertengahan: huruf Gothic, tekstur perkamen, warna tanah dan emas.',
    'memphis': 'Memphis — pola geometris berulang, warna neon 80-an, dan bentuk abstrak playful.',
    'minimal_horror': 'Minimal Horror — desain minimalis dengan nuansa seram: warna gelap, tipografi seram, dan whitespace kosong.',
    'minimalistic_futuristic': 'Minimalistic Futuristic — UI futuristik bersih: gradien gelap, garis tipis neon, dan ruang luas.',
    'mystical_forest': 'Mystical Forest — estetika hutan ajaib: hijau tua, cahaya firefly, tekstur daun dan kayu.',
    'neumorphism': 'Neumorphism — soft UI dengan shadow ganda yang menciptakan efek timbul halus pada elemen.',
    'oceanic': 'Oceanic — tema laut: gradien biru, tekstur air, elemen organik laut, dan tipografi clean.',
    'old_web': 'Old Web — nostalgia era 2000-an: marquee, tabel, background GIF, dan warna mencolok.',
    'pixelated': 'Pixelated — estetika retro gaming: sprite, font bitmap, grid pixel, dan palet terbatas.',
    'pop_art': 'Pop Art — gaya Andy Warhol: warna neon bold, dot pattern Ben-Day, dan konten mass culture.',
    'psychedelic': 'Psychedelic — Summer of Love: gradien pelangi, bentuk cair, tipografi melengkung, dan warna psychedelic.',
    'rococo': 'Rococo — kemewahan dekoratif: ornamen emas, lengkungan organik, warna pastel kaya, dan detail berlebih.',
    'saccharine': 'Saccharine — estetika manis berlebihan: pastel pink-ungu, dekorasi ribet, dan nuansa dongeng.',
    'slasher': 'Slasher — horror film estetika: darah merah, font serif tebal, tekstur goresan, dan nuansa gelap.',
    'surreal': 'Surreal — gaya mimpi: objek tidak masuk akal, gradien aneh, dan komposisi yang membingungkan.',
    'swiss_style': 'Swiss Style — tipografi grid-based, Helvetica, struktur hierarki bersih, dan warna minimal.',
    'terminal': 'Terminal — estetika CLI: font monospace hijau di atas hitam, cursor berkedip, dan teks ASCII.',
    'techno_baroque': 'Techno Baroque — perpaduan ornamen Baroque klasik dengan elemen digital futuristic.',
    'typodriven': 'Typodriven — desain web yang sepenuhnya dibangun dari tipografi: font sebagai elemen visual utama.',
    'ukiyo_e': 'Ukiyo-e — cetak kaya Jepang: gradien flat, garis outline tegas, warna earthy, dan tema alam.',
    'vaporwave': 'Vaporwave — retro-future 80an-90an: gradien pink-ungu, kolom Romawi, dan estetika glitch.',
    'western': 'Western — estetika koboi: tekstur kayu, font slab serif, palet tanah cokelat, dan nuansa frontier.',
    'y2k': 'Y2K — estetika millennium: gradien metallic, bentuk geometris membulat, chrome, dan kilauan.',
}

def inject_gtag(content):
    if 'googletagmanager.com/gtag/js' in content:
        return content, False
    # Insert after <head> or first <meta charset>
    m = re.search(r'<head>', content, re.I)
    if not m:
        return content, False
    pos = m.end()
    content = content[:pos] + '\n' + GTAG + content[pos:]
    return content, True

def fix_page(fn, content):
    base = fn.replace('.html', '')
    changed = False

    # 1. lang="en" -> lang="id"
    if re.search(r'<html[^>]*lang="en"', content):
        content = re.sub(r'<html([^>]*?)lang="en"', r'<html\1lang="id"', content, count=1)
        changed = True

    # 2. meta description
    if not re.search(r'<meta name="description"', content):
        desc = DESCRIPTIONS.get(base, f"Demo art style {base.replace('_',' ').title()} — koleksi desain web interaktif di Demo Artstyle Gallery.")
        # escape & and quotes for HTML
        desc = desc.replace('&', '&amp;').replace('"', '&quot;')
        meta = f'  <meta name="description" content="{desc}">'
        # insert after <title> line
        m = re.search(r'<title>[^<]*</title>', content)
        if m:
            content = content[:m.end()] + '\n' + meta + content[m.end():]
            changed = True
        else:
            print(f'  !! no title tag: {fn}')

    # 3. canonical
    if not re.search(r'<link rel="canonical"', content):
        canon = f'  <link rel="canonical" href="{DOMAIN}/{fn}">'
        m = re.search(r'<link rel="icon"', content) or re.search(r'<meta name="description"', content)
        anchor = m.start() if m else (re.search(r'<head>', content).end())
        content = content[:anchor] + canon + '\n' + content[anchor:]
        changed = True

    # 4. gtag
    content, g_changed = inject_gtag(content)
    changed = changed or g_changed

    return content, changed

# Process all html files
files = sorted(glob.glob(os.path.join(FOLDER, '*.html')))
total_changed = 0
for f in files:
    fn = os.path.basename(f)
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    content, changed = fix_page(fn, content)
    if changed:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        total_changed += 1
        print(f'FIXED {fn}')
    else:
        print(f'OK    {fn}')

# Fix index.html stale count 41 -> 42
idx = os.path.join(FOLDER, 'index.html')
with open(idx, 'r', encoding='utf-8') as fh:
    content = fh.read()
orig = content
content = content.replace('41 Desain Web Art Style', '42 Desain Web Art Style')
content = content.replace('41 gaya desain web', '42 gaya desain web')
content = content.replace('41 landing page', '42 landing page')
if content != orig:
    with open(idx, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print('FIXED index.html (count 41->42)')

# Regenerate sitemap.xml with ALL html files
today = datetime.date.today().isoformat()
urls = []
html_files = sorted([os.path.basename(f) for f in glob.glob(os.path.join(FOLDER, '*.html'))])
for fn in html_files:
    loc = DOMAIN + '/' + fn
    prio = '1.0' if fn == 'index.html' else ('0.6' if fn in ('about.html','contact.html','privacy.html') else '0.7')
    freq = 'weekly' if fn == 'index.html' else 'monthly'
    urls.append((loc, today, freq, prio))

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for loc, lastmod, freq, prio in urls:
    xml += f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>\n'
xml += '</urlset>\n'
with open(os.path.join(FOLDER, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
    fh.write(xml)
print(f'REGEN sitemap.xml ({len(urls)} URLs)')

print(f'\nDone! {total_changed} files updated.')
