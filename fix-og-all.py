import os, glob, re

folder = r'D:\14_project_naufalrakha\demo-artstyle'
domain = 'https://demo.naufalrakha.my.id'

favicon_block = '''  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="icon" type="image/x-icon" href="favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" sizes="192x192" href="favicon-192x192.png">
  <link rel="icon" type="image/png" sizes="48x48" href="favicon-48x48.png">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
  <link rel="apple-touch-icon" href="favicon-180x180.png">'''

# Deskripsi unik per halaman (key = nama file tanpa .html)
DESCRIPTIONS = {
    'about': 'Tentang Demo Artstyle — galeri 41 gaya desain web interaktif oleh Naufal Rakha Putra.',
    'contact': 'Kontak Naufal Rakha Putra — pembuat Demo Artstyle Gallery. Tersedia untuk kolaborasi desain web.',
    'privacy': 'Kebijakan Privasi Demo Artstyle Gallery. Data kunjungan tidak disimpan atau dibagikan.',
    # Art style pages
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
    'grunge': 'Gruge — estetika kasar: tekstur kotor, noise, font tangan, dan palet gelap bernuansa vintage.',
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
    'art_deco': 'Art Deco - kemewahan geometric 1920-an: pola sunburst, emas-hitam-ivory, dan tipografi serif dekoratif.',
    'art_nouveau': 'Art Nouveau - lekukan organik ala awal 1900-an: kurva whiplash, motif flora, palet sage-emas, dan ornamen halus.',
    'cyberpunk': 'Cyberpunk - dystopia neon: cyan-magenta menyala, efek glitch, grid perspektif, dan tipografi techy.',
    'flat_design': 'Flat Design - warna solid cerah tanpa gradien, bentuk sederhana, tanpa bayangan, dan tipografi bersih.',
    'skeuomorphism': 'Skeuomorphism - UI meniru objek nyata: tekstur kulit jahitan, tombol timbul 3D, dan highlight mengkilap ala era iOS lama.',
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

def build_og_block(title, desc, canonical):
    return f'''  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="https://demo.naufalrakha.my.id/og-image.png">
  <meta property="og:locale" content="id_ID">
  <meta property="og:site_name" content="Demo Artstyle Gallery">
  <meta property="og:logo" content="https://demo.naufalrakha.my.id/logo-512.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://demo.naufalrakha.my.id/og-image.png">'''

files = glob.glob(os.path.join(folder, '*.html'))
for f in sorted(files):
    fn = os.path.basename(f)
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()

    # Skip index.html - handle manually
    if fn == 'index.html':
        print(f'SKIP (index.html - manual): {fn}')
        continue

    # Remove any existing OG/twitter/favicon tags
    for pat in [
        r'<meta property="og:[^>]*>\n?',
        r'<meta name="twitter:[^>]*>\n?',
        r'<link rel="icon[^>]*>\n?',
        r'<link rel="apple-touch-icon[^>]*>\n?',
        r'<!-- Open Graph -->\n?',
        r'<!-- Twitter Card -->\n?',
    ]:
        content = re.sub(pat, '', content)

    canonical = domain + '/' + fn
    m_t = re.search(r'<title>(.*?)</title>', content)
    title = m_t.group(1) if m_t else fn.replace('.html', '').replace('_', ' ').title()

    # Look up description from mapping, fallback to generic
    base = fn.replace('.html', '')
    if base in DESCRIPTIONS:
        desc = DESCRIPTIONS[base]
    else:
        desc = f"Demo art style {title} — koleksi desain web interaktif di Demo Artstyle Gallery."

    full_block = favicon_block + '\n\n' + build_og_block(title, desc, canonical) + '\n'

    # Insert after <title> tag
    m = re.search(r'<title>[^<]*</title>', content)
    if m:
        insert_at = m.end()
        content = content[:insert_at] + '\n' + full_block + content[insert_at:]
    else:
        print(f'SKIP (no title tag): {fn}')
        continue

    # Ensure proper break after head
    content = content.replace('</title>\n\n  <style>', '</title>\n  <style>', 1)

    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print(f'UPDATED: {fn} — {desc[:60]}...')
