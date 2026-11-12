#!/usr/bin/env python3
"""Banners for #1 Brno: Luma cover 1200x1200, LinkedIn/og 1920x1080. Portraits from img/1/sp-*.webp in duotone.
Run from repo root: python3 tools/pages/banner_1.py . -> brand/banners/1_cover_*.png, img/1/og.jpg
"""
import base64, io, pathlib, sys
from PIL import Image, ImageOps
from playwright.sync_api import sync_playwright

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
ORANGE = (232, 54, 10)
SPK = [('filipensky', 'Petr Filipenský', 'FN u sv. Anny'), ('borek', 'Kamil Bořek', 'Promedica, Versius'), ('vidovicova', 'Lucie Vidovićová', 'FSS MU'),
       ('cerny', 'David Černý', 'ÚSP AV ČR'), ('mikesova', 'Jana Mikešová', 'FN Brno'), ('orlova', 'Zhenya Orlova', 'REVEL Robotics')]
CUT = root / 'brand/speakers-1'  # cards from tools/pages/cutouts_1.py (rembg + face-normalised)

def b64(path):
    b = io.BytesIO(); Image.open(path).convert('RGB').save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

cards = ''.join(f'<figure><img src="{b64(CUT / f"{k}.png")}" alt=""><figcaption><b>{n}</b><span>{o}</span></figcaption></figure>' for k, n, o in SPK)

CSS = '''*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,sans-serif;background:#fff;color:#000;width:var(--w);height:var(--h);overflow:hidden;position:relative}
.logo{font-weight:700;letter-spacing:-.05em;line-height:.86}
.rule{position:absolute;display:flex;align-items:center}
.rule i{display:block;height:14px;background:#E8360A;flex:1}
.rule b{width:140px;height:140px;border-radius:50%;background:#E8360A;color:#fff;font-weight:700;font-size:56px;display:grid;place-items:center;letter-spacing:-.04em}
.when{font-weight:700;line-height:1.05;letter-spacing:-.03em}
.meta{font-weight:400}
.url{color:#E8360A;font-weight:700}
.grid{display:grid;gap:22px}
figure{display:grid;grid-template-rows:1fr auto;min-height:0}
figure img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;min-height:0}
figcaption{padding-top:14px;line-height:1.15;letter-spacing:-.02em}
figcaption b{display:block;font-weight:700;font-size:30px}
figcaption span{display:block;font-weight:400;font-size:22px;color:#555;margin-top:3px}
'''

WIDE = f'''<!doctype html><meta charset="utf-8"><style>{CSS}
body{{--w:1920px;--h:1080px}}
.logo{{position:absolute;left:72px;top:90px;font-size:150px}}
.rule{{left:0;top:450px;width:510px}}
.when{{position:absolute;left:72px;top:640px;font-size:56px}}
.meta{{position:absolute;left:72px;top:780px;font-size:36px;line-height:1.3}}
.url{{position:absolute;left:72px;top:950px;font-size:40px}}
.grid{{position:absolute;left:672px;top:72px;width:1176px;height:936px;gap:40px 28px;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr)}}
</style><body>
<div class="logo">proto<br>robot</div>
<div class="rule"><i></i><b>#1</b></div>
<div class="when">čtvrtek<br>26. listopadu</div>
<div class="meta">19:00 až 22:00<br>Filozofická fakulta MU<br>Arna Nováka 1, Brno</div>
<div class="url">protorobot.cz</div>
<div class="grid">{cards}</div>
'''

SQUARE = f'''<!doctype html><meta charset="utf-8"><style>{CSS}
body{{--w:1200px;--h:1200px}}
.logo{{position:absolute;left:56px;top:56px;font-size:118px}}
.rule{{right:0;top:84px;width:470px;flex-direction:row-reverse}}
.rule b{{width:120px;height:120px;font-size:48px}}
.when{{position:absolute;right:56px;top:250px;font-size:40px;text-align:right}}
.meta{{position:absolute;left:56px;top:300px;font-size:28px;line-height:1.3}}
.url{{position:absolute;left:56px;top:390px;font-size:30px}}
.grid{{position:absolute;left:56px;top:470px;width:1088px;height:674px;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr);gap:18px}}
figcaption b{{font-size:25px}} figcaption span{{font-size:18px}} figcaption{{padding-top:10px}}
</style><body>
<div class="logo">proto<br>robot</div>
<div class="rule"><i></i><b>#1</b></div>
<div class="when">čtvrtek<br>26. listopadu</div>
<div class="meta">19:00 až 22:00<br>Filozofická fakulta MU, Arna Nováka 1, Brno</div>
<div class="url">protorobot.cz</div>
<div class="grid">{cards}</div>
'''

out = root / 'brand/banners'
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, html, w, h in (('1_cover_1920x1080', WIDE, 1920, 1080), ('1_luma_1200x1200', SQUARE, 1200, 1200)):
        pg = b.new_page(viewport={'width': w, 'height': h})
        pg.set_content(html); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out / f'{name}.png'))
        print('wrote', out / f'{name}.png')
    b.close()
Image.open(out / '1_cover_1920x1080.png').convert('RGB').resize((1200, 675), Image.LANCZOS).save(root / 'img/1/og.jpg', 'JPEG', quality=86)
print('wrote img/1/og.jpg')
