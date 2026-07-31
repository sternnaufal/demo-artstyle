import os, glob, re

FOLDER = r'D:\14_project_naufalrakha\demo-artstyle'
files = sorted(f for f in glob.glob(FOLDER + r'\*.html') if f.split('\\')[-1] not in ('index.html','about.html','contact.html','privacy.html'))

BACK_LINK = '''<a href="index.html" title="Kembali ke Gallery" style="position:fixed;top:12px;left:12px;z-index:9999;display:inline-flex;align-items:center;gap:6px;padding:7px 14px;border-radius:50px;background:rgba(0,0,0,0.5);color:#fff;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);font-family:sans-serif;font-size:13px;font-weight:600;text-decoration:none;box-shadow:0 2px 10px rgba(0,0,0,0.3);transition:all .2s;">&#8592; Gallery</a>'''

count = 0
for f in files:
    fn = f.split('\\')[-1]
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    if 'Kembali ke Gallery" style="position:fixed' in content:
        print(f'SKIP {fn} (already has top back link)')
        continue
    # Insert right after <body> tag
    m = re.search(r'<body[^>]*>', content)
    if not m:
        print(f'!! no body tag: {fn}')
        continue
    content = content[:m.end()] + '\n' + BACK_LINK + content[m.end():]
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(content)
    count += 1
    print(f'OK {fn}')

print(f'\nDone! {count} pages updated.')
