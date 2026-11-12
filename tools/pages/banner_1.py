#!/usr/bin/env python3
"""Covers for #1 Brno. Portrait cards come from tools/pages/cutouts_1.py (brand/speakers-1/*.png).
Square 1200 for Luma, 1920x1080 for LinkedIn/og. Run from repo root: python3 tools/pages/banner_1.py .
Layout: service line (series, mark, rule, date) / headline of the evening / meta / talks row / panel row. 12-col grid, margin 48, gutter 24.
"""
import base64, io, pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
CUT = root / 'brand/speakers-1'
TALKS = [('filipensky', 'Petr Filipenský', 'FN u sv. Anny, da Vinci'), ('borek', 'Kamil Bořek', 'Promedica, Versius')]
PANEL = [('vidovicova', 'Lucie Vidovićová', 'FSS MU'), ('cerny', 'David Černý', 'AV ČR'), ('mikesova', 'Jana Mikešová', 'FN Brno'), ('orlova', 'Zhenya Orlova', 'REVEL')]
DATE, META = 'čtvrtek 26. 11. 2026', '19:00, aula C33, Filozofická fakulta MU, Arna Nováka 1, Brno'
HEAD = 'roboti<br>v&nbsp;laboratořích<br>a&nbsp;nemocnicích'

def b64(k):
    b = io.BytesIO(); Image.open(CUT / f'{k}.png').convert('RGB').save(b, 'JPEG', quality=92)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def tile(k, n, o, big):
    return f'<figure class="{"big" if big else "sm"} k-{k}"><img src="{b64(k)}" alt=""><figcaption><b>{n}</b><span>{o}</span></figcaption></figure>'

talks = ''.join(tile(*t, True) for t in TALKS); panel = ''.join(tile(*t, False) for t in PANEL)

BASE = '''*{margin:0;padding:0;box-sizing:border-box}
body{position:relative;background:#fff;color:#000;font-family:Inter;overflow:hidden}
.top{position:absolute;display:flex;align-items:center;gap:24px;font-size:24px;font-weight:500;letter-spacing:-.01em}
.top b{width:56px;height:56px;border-radius:50%;background:#E8360A;color:#fff;font-size:24px;font-weight:700;display:grid;place-items:center}
.top i{flex:1;height:8px;background:#E8360A}
.top .d{margin-left:-4px;font-size:20px;text-transform:uppercase;letter-spacing:.06em;font-weight:500}
h1{position:absolute;font-weight:700;letter-spacing:-.05em;line-height:.9}
.meta{position:absolute;font-size:24px;line-height:30px}
.lab{position:absolute;font-size:20px;line-height:24px;text-transform:uppercase;letter-spacing:.06em;font-weight:500}
.row{position:absolute;display:grid;gap:24px}
figure{position:relative;background:#E8360A;overflow:hidden}
figure img{width:100%;height:100%;object-fit:contain;object-position:50% 0;display:block}
.big img{object-fit:cover;object-position:50% 48%}
.sm img{transform:translateY(-10px)}
figcaption{position:absolute;left:0;right:0;bottom:0;background:#000;color:#fff;padding:16px}
.big figcaption b{font-size:24px;line-height:30px;font-weight:600;letter-spacing:-.01em}
.big figcaption span{font-size:24px;line-height:30px}
.big figcaption span::before{content:', '}
.sm figcaption{padding:10px 16px 11px}
.sm figcaption b{font-size:24px;line-height:28px;font-weight:500;display:block;letter-spacing:-.01em}
.sm figcaption span{display:block;font-size:18px;line-height:22px}
'''

SQUARE = f'''<!doctype html><meta charset="utf-8"><style>{BASE}
body{{width:1200px;height:1200px}}
.top{{left:48px;right:48px;top:48px}}
h1{{left:48px;right:48px;top:150px;font-size:96px}}
.meta{{left:48px;top:428px}}
.lab{{left:48px}}
.row{{left:48px;right:48px}}
.r1{{top:536px;grid-template-columns:repeat(2,1fr);height:320px}}
.r2{{top:940px;grid-template-columns:repeat(4,1fr);height:212px}}
</style><body>
<div class="top"><span>proto robot</span><b>#1</b><i></i><span class="d">{DATE}</span></div>
<h1>{HEAD}</h1>
<div class="meta">{META}</div>
<div class="lab" style="top:500px">přednášky</div>
<div class="row r1">{talks}</div>
<div class="lab" style="top:904px">panel: roboti v péči</div>
<div class="row r2">{panel}</div>
'''

# 1920x1080: 12 cols of 132 + 11 gutters of 24 = 1848, margin 36. Text cols 1-5 (756), tiles cols 6-12 (1068).
def logo(path, h):
    path = root / path
    if path.suffix == '.svg':
        return f'<img src="data:image/svg+xml;base64,{base64.b64encode(path.read_bytes()).decode()}" style="height:{h}px" alt="">'
    b = io.BytesIO(); Image.open(path).convert('RGBA').save(b, 'PNG')
    return f'<img src="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}" style="height:{h}px" alt="">'
PARTNERS = (f'<div><span>partneři</span><p><em>Filozofická fakulta MU</em>{logo("brand/duotone/revel_duotone.png", 36)}'
            f'{logo("brand/black/promedica_black.png", 30)}{logo("brand/black/cmr_black.png", 36)}{logo("brand/black/printedrobotics_black.svg", 36)}</p></div>')
WIDE = f'''<!doctype html><meta charset="utf-8"><style>{BASE}
body{{width:1920px;height:1080px}}
.top{{left:36px;right:36px;top:36px}}
h1{{left:36px;width:756px;top:150px;font-size:112px}}
.top{{top:36px}}
.meta{{left:36px;width:760px;top:488px;font-size:40px;line-height:50px;letter-spacing:-.02em}}
.meta b{{font-weight:700;display:block}}
.lab{{left:816px}}
.row{{left:816px;right:36px}}
.r1{{top:190px;grid-template-columns:repeat(2,1fr);height:310px}}
.r2{{top:570px;grid-template-columns:repeat(4,1fr);height:310px}}
figcaption{{height:72px;padding:0 16px}}
.big figcaption{{white-space:nowrap;padding-top:19px}}
.sm figcaption{{padding-top:9px}}
.big figcaption b,.big figcaption span{{font-size:26px;line-height:34px}}
.sm figcaption b{{font-size:26px;line-height:30px}} .sm figcaption span{{font-size:20px;line-height:24px}}
.sm img{{transform:none}}
.partners{{position:absolute;left:36px;right:36px;bottom:36px;display:flex;gap:72px;align-items:flex-end}}
.partners div{{display:flex;flex-direction:column;gap:14px}} .partners p{{display:flex;align-items:center;gap:56px;height:36px}}
.partners span{{font-size:18px;line-height:22px;text-transform:uppercase;letter-spacing:.06em;font-weight:500}}
.partners img{{display:block}}
.partners em{{font-style:normal;font-size:26px;line-height:36px;font-weight:600;letter-spacing:-.02em;white-space:nowrap}}
.url{{position:absolute;left:36px;top:640px;font-size:32px;line-height:40px;font-weight:700;color:#E8360A;letter-spacing:-.02em}}
</style><body>
<div class="top"><span>proto robot</span><b>#1</b><i></i><span class="d">{DATE}</span></div>
<h1>{HEAD}</h1>
<div class="meta"><b>čt 26. 11. 2026, 19:00</b>aula C33, FF MU, Arna Nováka 1, Brno</div>
<div class="partners">{PARTNERS}</div>
<div class="url">protorobot.cz</div>
<div class="lab" style="top:154px">přednášky</div>
<div class="row r1">{talks}</div>
<div class="lab" style="top:534px">panel: roboti v péči</div>
<div class="row r2">{panel}</div>
'''

out = root / 'brand/banners'
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, html, w, h in (('1_luma_1200x1200', SQUARE, 1200, 1200), ('1_cover_1920x1080', WIDE, 1920, 1080)):
        pg = b.new_page(viewport={'width': w, 'height': h}); pg.set_content(html); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out / f'{name}.png')); print('wrote', out / f'{name}.png')
    b.close()
Image.open(out / '1_cover_1920x1080.png').convert('RGB').resize((1200, 675), Image.LANCZOS).save(root / 'img/1/og.jpg', 'JPEG', quality=86)
Image.open(out / '1_luma_1200x1200.png').resize((320, 320), Image.LANCZOS).save(out / '1_luma_320.png')
print('wrote img/1/og.jpg')
