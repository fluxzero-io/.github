#!/usr/bin/env python3
"""Build GitHub brand assets from the existing Fluxzero website vectors and fonts."""
import argparse
import html
import re
import shutil
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

parser = argparse.ArgumentParser()
parser.add_argument('--website', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
out = root / 'assets/brand/2026-10'
out.mkdir(parents=True, exist_ok=True)
version = re.search(r"fluxzeroBrandVersion = '([^']+)'", (args.website / 'src/config/brand.mjs').read_text()).group(1)
source = args.website / 'public/assets/fluxzero/brand' / version
for name in ['fluxzero-logo.svg', 'fluxzero-mark.svg']:
    shutil.copyfile(source / name, out / name)
fonts = {
    'display': TTFont(args.website / 'public/fonts/poppins/Poppins-500-latin.woff2'),
    'body': TTFont(args.website / 'public/fonts/poppins/Poppins-400-latin.woff2'),
}

def text(value, x, y, size, font='body', fill='#F4F7FF', accent_after=None):
    f = fonts[font]
    glyphs = f.getGlyphSet()
    cmap = f.getBestCmap()
    scale = size / f['head'].unitsPerEm
    paths = []
    combined = SVGPathPen(glyphs)
    offset = 0
    for index, char in enumerate(value):
        name = cmap.get(ord(char), '.notdef')
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        glyphs[name].draw(TransformPen(combined, (1, 0, 0, 1, offset, 0)))
        color = ' fill="#C4E5F6"' if accent_after is not None and index >= accent_after else ''
        paths.append(f'<path{color} transform="translate({offset},0)" d="{pen.getCommands()}"/>')
        offset += glyphs[name].width
    if fill.startswith('url('):
        paths = [f'<path d="{combined.getCommands()}"/>']
    return f'<g aria-label="{html.escape(value, quote=True)}" fill="{fill}" transform="translate({x},{y}) scale({scale},-{scale})">'+''.join(paths)+'</g>'

def vector(name, x, y, width):
    content = (source/name).read_text()
    vb = re.search(r'viewBox="([^"]+)"', content).group(1).split()
    inner = content[content.index('>\n', content.index('<svg'))+1:content.rindex('</svg>')]
    return f'<g transform="translate({x},{y}) scale({width/float(vb[2])})">{inner}</g>'

def center(value, y, size, font='body', fill='#F4F7FF', width=1280):
    f = fonts[font]
    glyphs = f.getGlyphSet()
    cmap = f.getBestCmap()
    advance = sum(glyphs[cmap.get(ord(char), '.notdef')].width for char in value)
    return text(value, (width - advance * size / f['head'].unitsPerEm) / 2, y, size, font, fill)


def svg(height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" viewBox="0 0 1280 {height}" role="img" aria-labelledby="title">
<title id="title">{html.escape(title)}</title>
<defs>
<clipPath id="banner-clip"><rect width="1280" height="{height}" rx="18"/></clipPath>
<radialGradient id="glow"><stop stop-color="#ffe79c" stop-opacity=".28"/><stop offset=".4" stop-color="#ffbb52" stop-opacity=".12"/><stop offset="1" stop-color="#ff8432" stop-opacity="0"/></radialGradient>
<linearGradient id="planet" x2="0" y2="1"><stop stop-color="#060709"/><stop offset="1" stop-color="#1e1e22"/></linearGradient>
<linearGradient id="title-blue"><stop stop-color="#d9f5ff"/><stop offset="1" stop-color="#2f7fba"/></linearGradient>
<filter id="rim"><feGaussianBlur stdDeviation="18"/></filter>
</defs>
<g clip-path="url(#banner-clip)">
<rect width="1280" height="{height}" fill="#0a0a0a"/>
<ellipse cx="640" cy="{height*.7}" rx="680" ry="{height*.8}" fill="url(#glow)"/>
<ellipse cx="640" cy="{height*2.94}" rx="1800" ry="{height*2}" fill="none" stroke="#ffe79c" stroke-opacity=".24" stroke-width="4" filter="url(#rim)"/>
<ellipse cx="640" cy="{height*2.94}" rx="1800" ry="{height*2}" fill="url(#planet)"/>
{body}</g></svg>'''

hero = vector('fluxzero-logo.svg', 525, 32, 230)
hero += center('The cloud that works', 180, 58, 'display')
hero += center('for your agent.', 250, 58, 'display', 'url(#title-blue)')
(out/'organization-hero.svg').write_text(svg(320, 'Fluxzero — The cloud that works for your agent.', hero))
header = vector('fluxzero-logo.svg',52,42,226)
header += text('The cloud that works for your agent.',52,173,52,'display',accent_after=len('The cloud that works '))
header += text('fluxzero.io',1070,75,22,fill='#A7B4C8')
(out/'repository-header.svg').write_text(svg(224,'Fluxzero — The cloud that works for your agent.',header))
compact = vector('fluxzero-logo.svg',40,27,180)
compact += text('Platform engineering',805,59,23,fill='#A7B4C8')
(out/'engineering-header.svg').write_text(svg(96,'Fluxzero — Platform engineering',compact))
mark = vector('fluxzero-mark.svg',105,91,302)
(out/'avatar.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect width="512" height="512" fill="#05070B"/>'+mark+'</svg>')
labels = {'.github': '', 'fluxzero-agent-plugins': 'Agent plugins', 'fluxzero-cli': 'CLI', 'fluxzero-sdk-java': 'Java & Kotlin SDK', 'fluxzero-dev-server': 'Dev Server', 'fluxzero-site': 'Website & documentation', 'fluxzero-deploy-action': 'Deploy Action', 'fluxzero-jwt-action': 'JWT Action', 'homebrew-tap': 'Homebrew tap'}
(out/'social').mkdir(exist_ok=True)
for repo,label in labels.items():
    body = vector('fluxzero-logo.svg', 512, 48, 256)
    body += center('The cloud that works', 260, 76, 'display')
    body += center('for your agent.', 354, 76, 'display', 'url(#title-blue)')
    if label:
        body += text(label, 64, 572, 28)
    body += text('fluxzero.io', 1030, 572, 23, fill='#A7B4C8')
    (out/'social'/f'{repo}.svg').write_text(svg(640,f'Fluxzero — The cloud that works for your agent. — {label}' if label else 'Fluxzero — The cloud that works for your agent.',body))
print(f'Built assets from website brand {version}')

# Compact organization hero and linked tool buttons.
profile = out / 'profile'
profile.mkdir(exist_ok=True)


body = vector('fluxzero-logo.svg', 525, 32, 230)
body += center('The cloud that works', 162, 54, 'display')
body += center('for your agent.', 228, 54, 'display', 'url(#title-blue)')
(profile / 'hero.svg').write_text(svg(292, 'Fluxzero — The cloud that works for your agent.', body))
