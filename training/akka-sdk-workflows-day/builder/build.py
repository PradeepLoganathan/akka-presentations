#!/usr/bin/env python3
import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'builder'
SHELL = ROOT / 'shell'
GEN = ROOT / 'generated'
PRESENTERS = ROOT / 'presenters'

parser = argparse.ArgumentParser(description='Build training deck')
parser.add_argument('--mode', default='overview', choices=['overview', 'shareable'])
parser.add_argument('--out', default=None)
parser.add_argument('--presenter', default=None,
    help='Presenter JSON file stem in presenters/ (omit for an unpersonalised build)')
args = parser.parse_args()

out_path = Path(args.out) if args.out else GEN / args.mode / 'index.html'
registry = json.loads((BASE / 'slide-registry.json').read_text(encoding='utf-8'))
shell = (SHELL / 'shell.html').read_text(encoding='utf-8')
shared_css = (SHELL / 'shared.css').read_text(encoding='utf-8')
nav_js = (SHELL / 'nav.js').read_text(encoding='utf-8')
kiosk_js = (SHELL / 'kiosk.js').read_text(encoding='utf-8')

presenter = {}
if args.presenter:
    pfile = PRESENTERS / f'{args.presenter}.json'
    if pfile.exists():
        presenter = json.loads(pfile.read_text(encoding='utf-8'))
    else:
        print(f'Warning: presenter file not found: {pfile}')

css_parts = []
html_parts = []
js_parts = []
for entry in registry['slides']:
    slide_dir = ROOT / entry['folder']
    meta = json.loads((slide_dir / 'meta.json').read_text(encoding='utf-8'))
    if args.mode not in meta.get('include_in', ['overview']):
        continue
    css_parts.append('/* ' + entry['id'] + ' */\n' + (slide_dir / 'slide.css').read_text(encoding='utf-8'))
    html_parts.append((slide_dir / 'slide.html').read_text(encoding='utf-8'))
    js = (slide_dir / 'slide.js').read_text(encoding='utf-8')
    if js.strip():
        js_parts.append('/* ' + entry['id'] + ' */\n' + js)

slides_html_combined = '\n\n'.join(html_parts)

if presenter:
    # Keep the block, strip the marker comments, then substitute placeholders.
    slides_html_combined = re.sub(
        r'<!--\s*PRESENTER-BLOCK\s*-->|<!--\s*/PRESENTER-BLOCK\s*-->', '', slides_html_combined)
    for key, value in presenter.items():
        slides_html_combined = slides_html_combined.replace(f'{{{{PRESENTER_{key.upper()}}}}}', value)
else:
    # No presenter: strip the entire block (markers and their content) so nothing leaks.
    slides_html_combined = re.sub(
        r'<!--\s*PRESENTER-BLOCK\s*-->.*?<!--\s*/PRESENTER-BLOCK\s*-->',
        '', slides_html_combined, flags=re.DOTALL)
    slides_html_combined = re.sub(r'\{\{PRESENTER_[A-Z_]+\}\}', '', slides_html_combined)

result = shell.replace('{{SHARED_CSS}}', shared_css)
result = result.replace('{{SLIDES_CSS}}', '\n\n'.join(css_parts))
result = result.replace('{{SLIDES_HTML}}', slides_html_combined)
result = result.replace('{{SLIDES_JS}}', '\n\n'.join(js_parts))
result = result.replace('{{NAV_JS}}', nav_js)
result = result.replace('{{KIOSK_JS}}', kiosk_js)

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(result, encoding='utf-8', newline='\n')

assets = ROOT / 'assets'
if assets.exists():
    for name in ['images', 'logos']:
        src = assets / name
        dst = out_path.parent / name
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

print(f'Output:    {out_path}')
print(f'Size:      {out_path.stat().st_size // 1024} KB')
if presenter:
    print(f'Presenter: {presenter.get("name", args.presenter)}')
