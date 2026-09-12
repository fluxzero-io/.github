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
hero += text('Build, run, and scale your product.',67,385,25)
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
labels = {'.github': 'Build, run, and scale your product.', 'fluxzero-agent-plugins': 'Agent plugins', 'fluxzero-cli': 'CLI', 'fluxzero-sdk-java': 'Java & Kotlin SDK', 'fluxzero-dev-server': 'Dev Server', 'fluxzero-site': 'Website & documentation', 'fluxzero-deploy-action': 'Deploy Action', 'fluxzero-jwt-action': 'JWT Action', 'fluxzero-sample-gamerental': 'Game Rental sample', 'homebrew-tap': 'Homebrew tap'}
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
