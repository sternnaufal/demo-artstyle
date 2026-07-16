import os, glob, re

folder = r'D:\14_project_naufalrakha\demo-artstyle'
domain = 'https://demo.naufalrakha.my.id'

favicon_block = '''  <link rel="icon" type="image/x-icon" href="favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" sizes="48x48" href="favicon-48x48.png">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
  <link rel="apple-touch-icon" href="favicon-180x180.png">'''

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

    # Skip index.html - it already has some OG tags, handle manually
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
    # Generate description from title
    desc = f"{title} — Lihat demo art style ini di Gallery Demo Artstyle Naufal Rakha."

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
    print(f'UPDATED: {fn}')
