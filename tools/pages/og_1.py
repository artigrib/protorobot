#!/usr/bin/env python3
"""og:image for #1 in the #0 style: type block left, orange duotone photo right, logo strip below. 1200x630.
Run from repo root: python3 tools/pages/og_1.py .   Needs Archivo variable woff2 (ARCHIVO env or ./brand/fonts/archivo-wdth-italic.woff2).
"""
import base64, io, os, pathlib, sys
from PIL import Image, ImageOps
from playwright.sync_api import sync_playwright

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
FONT = pathlib.Path(os.environ.get('ARCHIVO', root / 'brand/fonts/archivo-wdth-italic.woff2'))
ORANGE = (232, 54, 10)

def duo(path, box):
    im = Image.open(path).convert('L'); im = ImageOps.fit(im, box, Image.LANCZOS, centering=(0.62, 0.5))
    im = ImageOps.autocontrast(im, cutoff=1).point(lambda v: max(0, min(255, int((v - 20) * 255 / 235))))
    im = ImageOps.colorize(im, black=(0, 0, 0), white=ORANGE)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=92); return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def logo(p, h):
    p = root / p
    if p.suffix == '.svg': return f'<img src="data:image/svg+xml;base64,{base64.b64encode(p.read_bytes()).decode()}" style="height:{h}px">'
    b = io.BytesIO(); Image.open(p).convert('RGBA').save(b, 'PNG'); return f'<img src="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}" style="height:{h}px">'

font_b64 = base64.b64encode(FONT.read_bytes()).decode()
font_ext = base64.b64encode((FONT.parent / 'archivo-wdth-italic-ext.woff2').read_bytes()).decode()
photo = duo(root / 'img/1/h-1.webp', (600, 500))
LOGOS = (f'<span class="l">{logo("brand/duotone/revel_duotone.png", 30)}</span>'
         f'<span class="l">{logo("brand/black/promedica_black.png", 24)}</span>'
         f'<span class="l">{logo("brand/black/technologiezdravi_black.png", 15)}</span>'
         f'<span class="l">{logo("brand/black/printedrobotics_black.svg", 24)}</span>'
         f'<span class="l">{logo("brand/black/prgai_black.svg", 24)}</span>')

def html(lang):
    T = dict(cs=dict(tag='MEETUP #1 BRNO', d='26. 11. 2026, 18:30', w='FF MU, AULA C33, BRNO', topic='ROBOTI V LABORATOŘÍCH A NEMOCNICÍCH'),
             en=dict(tag='MEETUP #1 BRNO', d='26 NOV 2026, 18:30', w='FF MU, HALL C33, BRNO', topic='ROBOTS IN LABS AND HOSPITALS'))[lang]
    return f'''<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:"ArchivoW";src:url(data:font/woff2;base64,{font_ext}) format("woff2");font-weight:100 900;font-stretch:62% 125%;font-style:italic;unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}
@font-face{{font-family:"ArchivoW";src:url(data:font/woff2;base64,{font_b64}) format("woff2");font-weight:100 900;font-stretch:62% 125%;font-style:italic;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#f3f3f1;position:relative;overflow:hidden;font-family:Inter,sans-serif;color:#000}}
.photo{{position:absolute;left:600px;top:0;width:600px;height:500px;background:#E8360A}}
.photo img{{width:100%;height:100%;display:block}}
.tag{{position:absolute;left:44px;top:40px;background:#000;color:#fff;font-weight:600;font-size:22px;letter-spacing:.04em;padding:10px 16px}}
.title{{position:absolute;left:40px;top:150px;font-family:ArchivoW;font-style:italic;font-weight:900;font-stretch:125%;font-size:108px;line-height:.86;letter-spacing:-.05em}}
.title span{{display:block}}
.topic{{position:absolute;left:44px;top:372px;font-size:20px;font-weight:600;letter-spacing:.04em;width:520px;line-height:1.25}}
.pills{{position:absolute;left:44px;top:432px;display:flex;gap:16px}}
.pills span{{border:2px solid #000;border-radius:999px;padding:11px 22px;font-size:20px;font-weight:500;letter-spacing:.01em;white-space:nowrap}}
.bar{{position:absolute;left:0;right:0;top:500px;height:130px;background:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 44px}}
.bar .l{{display:flex;align-items:center}}
.bar img{{display:block;width:auto}}
</style><body>
<div class="photo"><img src="{photo}"></div>
<div class="tag">{T['tag']}</div>
<h1 class="title"><span>PROTO</span><span>ROBOT</span></h1>
<div class="topic">{T['topic']}</div>
<div class="pills"><span>{T['d']}</span><span>{T['w']}</span></div>
<div class="bar">{LOGOS}</div>
'''

with sync_playwright() as p:
    b = p.chromium.launch()
    for lang, out in (('cs', 'img/1/og.jpg'), ('en', 'img/1/og-en.jpg')):
        pg = b.new_page(viewport={'width': 1200, 'height': 630}); pg.set_content(html(lang)); pg.wait_for_timeout(400)
        png = pg.screenshot(); Image.open(io.BytesIO(png)).convert('RGB').save(root / out, 'JPEG', quality=88); print('wrote', out)
    b.close()
