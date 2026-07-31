# regen-index.py — rebuild index.html gallery grid with consistent descriptions + search
import os, re, glob

FOLDER = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(FOLDER, 'index.html')

DESCRIPTIONS = {
    'acid': 'Gradien neon ekstrem, blur glow, bentuk cair psychedelic',
    'aero_frutiger': 'Efek transparan, gradien aqua, estetika mid-2000an futuristik',
    'art_deco': 'Geometri sunburst, emas-hitam-ivory, kemewahan 1920-an',
    'art_nouveau': 'Kurva whiplash, motif flora, palet sage-emas organik',
    'barbiecore': 'Hot pink bold, feminin, dan playful',
    'bauhaus': 'Bentuk geometris murni, warna primer, tipografi sans-serif',
    'bento_ui': 'Layout grid bento asimetris',
    'biopunk': 'Bioluminesensi, hijau neon, tekstur biomassa',
    'brutalism': 'Mentah tanpa dekorasi, border kasar, tipografi sistem',
    'candy_pop': 'Palet cerah pastel, bentuk rounded manis',
    'claymorphism': 'Efek 3D lembut seperti tanah liat',
    'constructivism': 'Diagonal tajam, merah-hitam, komposisi agresif',
    'corporate_memphis': 'Ilustrasi blobby flat, warna pastel cerah',
    'cyberpunk': 'Neon cyan-magenta, glitch, grid perspektif dystopia',
    'dada': 'Anti-art absurd, kolase chaos',
    'dark_minimal': 'Gelap bersih, satu aksen, tipografi ringan fokus konten',
    'de_stijl': 'Neoplasticism: garis, kotak merah-biru-kuning',
    'editorial': 'Layout majalah, headline serif besar, grid ketat',
    'flat_design': 'Warna solid cerah, bentuk sederhana, tanpa bayangan',
    'glassmorphism': 'Efek kaca transparan dengan backdrop-blur',
    'gothic': 'Lengkung lancip, warna gelap, emas, tekstur batu',
    'grunge': 'Tekstur kotor, noise, font tangan, nuansa vintage',
    'isometric': 'Ilustrasi 3D axonometric',
    'liminal_space': 'Estetika The Backrooms: koridor kosong',
    'manga': 'Gaya komik Jepang: panel, speedline, tipografi bold',
    'maximalism': 'Penuh warna, layer bertumpuk, tekstur berlebihan',
    'medieval': 'Huruf Gothic, tekstur perkamen, warna tanah dan emas',
    'memphis': 'Pola geometris 80-an, warna neon, bentuk abstrak',
    'material_design': 'Elevation shadow, kartu, warna primary bold ala Google',
    'minimal_horror': 'Minimalis seram: gelap, whitespace kosong',
    'minimalistic_futuristic': 'UI futuristik bersih: gradien gelap, garis neon',
    'mystical_forest': 'Hutan ajaib: hijau tua, cahaya firefly',
    'neumorphism': 'Soft UI dengan shadow ganda timbul',
    'oceanic': 'Tema laut: gradien biru, tekstur air',
    'old_web': 'Nostalgia 2000-an: marquee, tabel, background GIF',
    'pixelated': 'Retro gaming: sprite, font bitmap, grid pixel',
    'pop_art': 'Andy Warhol: warna neon, dot pattern Ben-Day',
    'psychedelic': 'Summer of Love: gradien pelangi, bentuk cair',
    'rococo': 'Ornamen emas, lengkungan organik, detail berlebih',
    'saccharine': 'Manis berlebihan: pastel pink-ungu, nuansa dongeng',
    'skeuomorphism': 'Tekstur kulit jahitan, tombol timbul 3D, highlight glossy',
    'slasher': 'Horror film: darah merah, font serif tebal',
    'solarpunk': 'Masa depan hijau cerah: panel surya, taman vertikal, energi bersih',
    'surreal': 'Gaya mimpi: objek tidak masuk akal',
    'swiss_style': 'Grid-based, Helvetica, hierarki bersih, minimal',
    'terminal': 'CLI: monospace hijau di atas hitam, teks ASCII',
    'techno_baroque': 'Ornamen Baroque klasik + elemen digital futuristic',
    'typodriven': 'Tipografi sebagai elemen visual utama',
    'ukiyo_e': 'Cetak Jepang: garis tegas, warna earthy, tema alam',
    'vaporwave': 'Retro-future 80-90an: pink-ungu, kolom Romawi, glitch',
    'western': 'Koboi: tekstur kayu, slab serif, palet cokelat',
    'y2k': 'Millennium: gradien metallic, chrome, kilauan',
}

NAMES = {
    'acid': 'Acid', 'aero_frutiger': 'Aero Frutiger', 'art_deco': 'Art Deco', 'art_nouveau': 'Art Nouveau',
    'barbiecore': 'Barbiecore', 'bauhaus': 'Bauhaus',
    'bento_ui': 'Bento UI', 'biopunk': 'Biopunk', 'brutalism': 'Brutalism',
    'candy_pop': 'Candy Pop', 'claymorphism': 'Claymorphism', 'constructivism': 'Constructivism',
    'corporate_memphis': 'Corporate Memphis', 'cyberpunk': 'Cyberpunk', 'dada': 'Dada',
    'dark_minimal': 'Dark Mode Minimal', 'de_stijl': 'De Stijl',
    'editorial': 'Editorial', 'flat_design': 'Flat Design', 'glassmorphism': 'Glassmorphism', 'gothic': 'Gothic', 'grunge': 'Grunge',
    'isometric': 'Isometric', 'liminal_space': 'Liminal Space', 'manga': 'Manga / Anime',
    'maximalism': 'Maximalism', 'medieval': 'Medieval', 'memphis': 'Memphis',
    'material_design': 'Material Design', 'minimal_horror': 'Minimal Horror', 'minimalistic_futuristic': 'Minimalistic Futuristic',
    'mystical_forest': 'Mystical Forest', 'neumorphism': 'Neumorphism', 'oceanic': 'Oceanic',
    'old_web': 'Old Web', 'pixelated': 'Pixelated', 'pop_art': 'Pop Art',
    'psychedelic': 'Psychedelic', 'rococo': 'Rococo', 'saccharine': 'Saccharine',
    'skeuomorphism': 'Skeuomorphism', 'slasher': 'Slasher', 'solarpunk': 'Solarpunk', 'surreal': 'Surreal', 'swiss_style': 'Swiss Style',
    'terminal': 'Terminal', 'techno_baroque': 'Techno Baroque', 'typodriven': 'Typodriven',
    'ukiyo_e': 'Ukiyo-e', 'vaporwave': 'Vaporwave', 'western': 'Western', 'y2k': 'Y2K',
}

# Discover actual style files (skip index/about/contact/privacy)
style_files = sorted(
    os.path.basename(f).replace('.html', '')
    for f in glob.glob(os.path.join(FOLDER, '*.html'))
    if os.path.basename(f) not in ('index.html', 'about.html', 'contact.html', 'privacy.html')
)

total = len(style_files)

def build_grid():
    cards = []
    for slug in style_files:
        name = NAMES.get(slug, slug.replace('_', ' ').title())
        desc = DESCRIPTIONS.get(slug, '')
        cards.append(f'''    <a href="{slug}.html" class="demo">
      <div class="name">{name}</div>
      <div class="info">{desc}</div>
    </a>''')
    return '\n'.join(cards)

cards_html = build_grid()

new_grid = f'''  <div style="max-width:720px;margin:0 auto 1.5rem;">
    <input type="text" id="styleSearch" placeholder="Cari style... (misal: neon, minimal, gelap)" style="width:100%;padding:0.75rem 1rem;border:2px solid #ddd;border-radius:10px;font-family:'Inter',sans-serif;font-size:0.95rem;outline:none;" oninput="filterStyles(this.value)">
  </div>
  <div class="grid animate__animated animate__fadeInUp" id="styleGrid">
{cards_html}
  </div>
  <div id="noResults" class="animate__animated animate__fadeIn" style="display:none;text-align:center;padding:3rem;color:#888;font-family:'Inter',sans-serif;">
    <p style="font-size:1.2rem;font-weight:600;margin-bottom:0.5rem;">Tidak ada style yang cocok</p>
    <p style="font-size:0.85rem;">Coba kata kunci lain</p>
  </div>
  <script>
  function filterStyles(q){{
    q = (q||'').toLowerCase().trim();
    var grid = document.getElementById('styleGrid');
    var cards = grid.querySelectorAll('a.demo');
    var visible = 0;
    cards.forEach(function(c){{
      var ok = !q || c.textContent.toLowerCase().indexOf(q) !== -1;
      c.style.display = ok ? '' : 'none';
      if (ok) visible++;
    }});
    document.getElementById('noResults').style.display = (visible === 0 && q) ? 'block' : 'none';
  }}
  </script>'''

with open(INDEX, 'r', encoding='utf-8') as fh:
    content = fh.read()

# Replace grid section: from the search div to the sites-network div
m = re.search(r'  <div style="max-width:720px;margin:0 auto 1\.5rem;">.*?(?=<div style="text-align:center;padding:1\.5rem)', content, re.S)
if not m:
    raise SystemExit('Grid section not found!')

content = content[:m.start()] + new_grid + '\n' + content[m.end():]

# Update counts in title/desc/og
content = content.replace(f'{total-5} Desain Web Art Style', f'{total} Desain Web Art Style') if False else content
content = re.sub(r'(\d+)\+? Desain Web Art Style', f'{total} Desain Web Art Style', content)
content = re.sub(r'Koleksi (\d+) gaya desain web', f'Koleksi {total} gaya desain web', content)
content = re.sub(r'Koleksi (\d+) landing page', f'Koleksi {total} landing page', content)

with open(INDEX, 'w', encoding='utf-8') as fh:
    fh.write(content)

print(f'Index rebuilt with {total} styles + search filter.')
