import os, glob, re

FOLDER = os.path.dirname(os.path.abspath(__file__))
files = sorted(f for f in glob.glob(os.path.join(FOLDER, '*.html')) if os.path.basename(f) not in ('index.html','about.html','contact.html','privacy.html'))

checks = {
    'nav': r'<nav',
    'hero': r'class="[^"]*hero|class="[^"]*cover|class="[^"]*masthead',
    'h1': r'<h1',
    'features': r'class="[^"]*(features|cards|essays|principles|feature|card)',
    'specs': r'class="[^"]*(specs|spec)',
    'cta': r'class="[^"]*(cta|btn|quote)',
    'footer': r'<footer|footer-text',
    'links_network': r'demo\.naufalrakha\.my\.id" class="current"',
    'gtag': r'G-R6Y4Y3XVGQ',
    'canonical': r'rel="canonical"',
    'description': r'name="description"',
    'lang_id': r'<html lang="id"',
}

report = {}
for f in files:
    fn = os.path.basename(f)
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        content = fh.read()
    missing = [name for name, pat in checks.items() if not re.search(pat, content)]
    report[fn] = missing

# Print pages with issues
issues = {fn: m for fn, m in report.items() if m}
print(f"Total style pages: {len(files)}")
print(f"Pages with 0 issues: {len(files) - len(issues)}")
print(f"\n--- Pages with issues ({len(issues)}) ---")
for fn, m in sorted(issues.items()):
    print(f"{fn}: missing {', '.join(m)}")
