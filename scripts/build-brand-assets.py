#!/usr/bin/env python3
"""Build GitHub brand assets from the existing Fluxzero website vectors and fonts."""
import argparse
import html
import re
import shutil
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

parser = argparse.ArgumentParser()
parser.add_argument('--website', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
out = root / 'assets/brand/2026-09'
out.mkdir(parents=True, exist_ok=True)
version = re.search(r"fluxzeroBrandVersion = '([^']+)'", (args.website / 'src/config/brand.mjs').read_text()).group(1)
source = args.website / 'public/assets/fluxzero/brand' / version
for name in ['fluxzero-logo.svg', 'fluxzero-mark.svg']:
    shutil.copyfile(source / name, out / name)
fonts = {
    'display': TTFont(args.website / 'public/fonts/google-sans-flex/GoogleSansFlex-Black.ttf'),
    'body': TTFont(args.website / 'public/fonts/inter/Inter-Regular.ttf'),
}

def text(value, x, y, size, font='body', fill='#F4F7FF'):
    f = fonts[font]
    glyphs = f.getGlyphSet()
    cmap = f.getBestCmap()
    scale = size / f['head'].unitsPerEm
    paths = []
    offset = 0
    for char in value:
        name = cmap.get(ord(char), '.notdef')
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        paths.append(f'<path transform="translate({offset},0)" d="{pen.getCommands()}"/>')
        offset += glyphs[name].width
    return f'<g aria-label="{html.escape(value, quote=True)}" fill="{fill}" transform="translate({x},{y}) scale({scale},-{scale})">'+''.join(paths)+'</g>'

def vector(name, x, y, width):
    content = (source/name).read_text()
    vb = re.search(r'viewBox="([^"]+)"', content).group(1).split()
    inner = content[content.index('>\n', content.index('<svg'))+1:content.rindex('</svg>')]
    return f'<g transform="translate({x},{y}) scale({width/float(vb[2])})">{inner}</g>'

def svg(height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" viewBox="0 0 1280 {height}" role="img" aria-labelledby="title">
<title id="title">{html.escape(title)}</title>
<defs><radialGradient id="glow"><stop stop-color="#17456b" stop-opacity=".8"/><stop offset="1" stop-color="#05070b" stop-opacity="0"/></radialGradient><linearGradient id="line"><stop stop-color="#3582bc" stop-opacity="0"/><stop offset=".6" stop-color="#84bfdc" stop-opacity=".48"/><stop offset="1" stop-color="#3582bc" stop-opacity="0"/></linearGradient></defs>
<rect width="1280" height="{height}" rx="18" fill="#05070B"/>
<ellipse cx="1010" cy="{height*.65}" rx="600" ry="{height*1.1}" fill="url(#glow)"/>
<path d="M650 {height} Q900 {height*.12} 1350 {height*.65}" stroke="url(#line)" stroke-width="1.5" fill="none"/>
{body}</svg>'''

hero = vector('fluxzero-logo.svg',64,42,240)
hero += text('The European cloud',64,210,76,'display')
hero += text('for AI-built apps',64,306,76,'display','#C4E5F6')
hero += text('Everything your product needs to run',67,385,25)
hero += text('fluxzero.io',1060,76,22,fill='#A7B4C8')
(out/'organization-hero.svg').write_text(svg(440,'Fluxzero — The European cloud for AI-built apps',hero))
header = vector('fluxzero-logo.svg',52,42,226)
header += text('The European cloud',52,173,52,'display')
header += text('for AI-built apps',665,174,49,'display','#C4E5F6')
header += text('fluxzero.io',1070,75,22,fill='#A7B4C8')
(out/'repository-header.svg').write_text(svg(224,'Fluxzero — The European cloud for AI-built apps',header))
compact = vector('fluxzero-logo.svg',40,27,180)
compact += text('Platform engineering',805,59,23,fill='#A7B4C8')
(out/'engineering-header.svg').write_text(svg(96,'Fluxzero — Platform engineering',compact))
mark = vector('fluxzero-mark.svg',105,91,302)
(out/'avatar.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect width="512" height="512" fill="#05070B"/>'+mark+'</svg>')
labels = {'.github': 'Everything your product needs to run', 'fluxzero-agent-plugins': 'Agent plugins', 'fluxzero-cli': 'CLI', 'fluxzero-sdk-java': 'Java & Kotlin SDK', 'fluxzero-dev-server': 'Dev Server', 'fluxzero-site': 'Website & documentation', 'fluxzero-deploy-action': 'Deploy Action', 'fluxzero-jwt-action': 'JWT Action', 'homebrew-tap': 'Homebrew tap'}
(out/'social').mkdir(exist_ok=True)
for repo,label in labels.items():
    body = vector('fluxzero-logo.svg',64,50,255)
    body += text('The European cloud',64,245,77,'display')
    body += text('for AI-built apps',64,350,77,'display','#C4E5F6')
    body += '<path d="M64 434 H1216" stroke="#263A50"/>'
    body += text(label,64,510,31)
    body += text('fluxzero.io',64,585,23,fill='#A7B4C8')
    (out/'social'/f'{repo}.svg').write_text(svg(640,f'Fluxzero — {label}',body))
print(f'Built assets from website brand {version}')

# The public profile uses a compact hero and real linked image buttons. New filenames
# keep the currently published profile stable while this revision is being previewed.
profile = out / 'profile'
profile.mkdir(exist_ok=True)

def center(value, y, size, font='body', fill='#F4F7FF', width=1280):
    f = fonts[font]
    glyphs = f.getGlyphSet()
    cmap = f.getBestCmap()
    advance = sum(glyphs[cmap.get(ord(char), '.notdef')].width for char in value)
    return text(value, (width - advance * size / f['head'].unitsPerEm) / 2, y, size, font, fill)

body = vector('fluxzero-logo.svg', 525, 32, 230)
body += center('The European cloud', 163, 64, 'display')
body += center('for AI-built apps', 238, 64, 'display', '#C4E5F6')
(profile / 'hero.svg').write_text(svg(292, 'Fluxzero — The European cloud for AI-built apps', body))

icons = {
    'cli': '<rect x="2" y="3" width="26" height="22" rx="4"/><path d="m8 10 5 4-5 4m9 0h5"/>',
    'agents': '<rect x="4" y="8" width="22" height="18" rx="5"/><path d="M15 3v5m-5 8h.1m9.9 0h.1M10 21h10M0 15h4m22 0h4"/><circle cx="15" cy="2" r="1"/>',
    'sdk': '<path d="m10 6-8 9 8 9m10-18 8 9-8 9m-3-22-4 26"/>',
}
for key, label, caption in [('cli', 'CLI', 'Create and run projects'), ('agents', 'Agent plugins', 'For your coding agent'), ('sdk', 'SDK', 'Java and Kotlin')]:
    for theme, caption_color in [('dark', '#A7B4C8'), ('light', '#59636e')]:
        content = '<rect x="10" y="6" width="340" height="92" rx="16" fill="#0A0F17" stroke="#315474" stroke-width="2"/>'
        content += f'<g transform="translate(36,36)" stroke="#A9D5F0" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round">{icons[key]}</g>'
        content += text(label, 92, 62, 27)
        content += '<path d="M307 46h14m-6-6 6 6-6 6" stroke="#83A6C5" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        content += center(caption, 139, 22, fill=caption_color, width=360)
        title = html.escape(f'{label} — {caption}')
        (profile / f'{key}-{theme}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="164" viewBox="0 0 360 164" role="img"><title>{title}</title>{content}</svg>')
