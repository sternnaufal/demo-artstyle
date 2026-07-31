# add-design.py — inject into all art style pages:
#  - designData JSON (palette/best/css)
#  - visible "Cocok Untuk" section + Copy Design.md button
#  - back-to-gallery link + year JS fix
import os, glob, re, json
from style_data import DESIGN, BEST, CSS

FOLDER = os.path.dirname(os.path.abspath(__file__))
files = sorted(f for f in glob.glob(os.path.join(FOLDER, '*.html')) if os.path.basename(f) not in ('index.html','about.html','contact.html','privacy.html'))

COPY_BTN_SCRIPT = r'''
<!-- Design Spec Section -->
<section class="design-spec" style="max-width:760px;margin:2.5rem auto;padding:1.75rem;border:1px solid currentColor;border-radius:12px;font-family:inherit;">
  <a href="index.html" style="display:inline-block;margin-bottom:1rem;font-size:0.8rem;text-decoration:none;opacity:0.6;">&larr; Kembali ke Gallery</a>
  <div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:center;justify-content:space-between;">
    <div>
      <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.2em;opacity:0.5;">Cocok Untuk</div>
      <p id="cocokUntuk" style="margin:0.35rem 0 0;font-size:0.95rem;line-height:1.6;"></p>
    </div>
    <button type="button" onclick="copyDesignMD(this)" style="padding:0.7rem 1.4rem;border-radius:8px;border:1px solid currentColor;background:transparent;font-weight:600;font-size:0.85rem;cursor:pointer;transition:all .2s;">&#128209; Copy Design.md</button>
  </div>
</section>
<script type="application/json" id="designData">%JSON%</script>
<script>
function copyDesignMD(btn){
  var data = JSON.parse(document.getElementById('designData').textContent);
  var specs = '';
  document.querySelectorAll('.spec').forEach(function(s){
    var k = s.querySelector('h3'), v = s.querySelector('p');
    if (k && v) specs += '- **' + k.textContent + '**: ' + v.textContent + '\n';
  });
  var md = '# ' + data.title + '\n\n' + data.description + '\n\n## Palet Warna\n' +
    data.palette.map(function(c){ return '- `' + c + '`'; }).join('\n') + '\n' +
    (specs ? '\n## Spesifikasi\n' + specs : '') +
    '\n## Cocok Untuk\n' + data.best + '\n\n## Teknik CSS Kunci\n' + data.css + '\n';
  navigator.clipboard.writeText(md).then(function(){
    var old = btn.textContent; btn.textContent = '&#10003; Copied!';
    setTimeout(function(){ btn.textContent = old; }, 2000);
  }).catch(function(){ alert('Gagal menyalin'); });
}
</script>
'''

def inject(content, fn, slug):
    if 'id="designData"' in content:
        return content, False

    # Build design JSON
    m = re.search(r'<title>(.*?)</title>', content)
    title = m.group(1) if m else slug.replace('_', ' ').title()
    m = re.search(r'<meta name="description" content="([^"]*)"', content)
    desc = m.group(1) if m else ''
    palette = DESIGN.get(slug, ['#000000','#ffffff','#888888'])
    best = BEST.get(slug, '')
    css = CSS.get(slug, '')
    data = {"title": title, "description": desc, "palette": palette, "best": best, "css": css}
    json_str = json.dumps(data, ensure_ascii=False)

    block = COPY_BTN_SCRIPT.replace('%JSON%', json_str)

    # Insert before </body>
    if '</body>' in content:
        content = content.replace('</body>', block + '</body>')
    else:
        content += block

    # Set cocokUntuk text
    content = content.replace(
        '<p id="cocokUntuk" style="margin:0.35rem 0 0;font-size:0.95rem;line-height:1.6;"></p>',
        '<p id="cocokUntuk" style="margin:0.35rem 0 0;font-size:0.95rem;line-height:1.6;">' + best + '</p>'
    )

    # Fix year script
    if "getElementById('year')" not in content:
        year_script = "<script>document.getElementById('year').textContent=new Date().getFullYear()</script>"
        content = content.replace('</body>', year_script + '</body>')

    return content, True

count = 0
for f in files:
    fn = os.path.basename(f)
    slug = fn.replace('.html', '')
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    content, changed = inject(content, fn, slug)
    if changed:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        count += 1
        print(f'OK {fn}')
    else:
        print(f'SKIP {fn} (already has designData)')

print(f'\nDone! {count} pages updated.')
