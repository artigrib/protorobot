"""Plates for LinkedIn clips 1080x1350: top band 0..371, video 371..979, bottom band 979..1350. Transparent PNG.
python3 plate.py key  -> <key>_plate.png
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

SPK = {
 'k': dict(name='Tomáš Konečný', talk='Robotservice. Běžné problémy servisních robotů: prosba konstruktérům', minutes='17'),
 'v': dict(name='Vítek', talk='', minutes=''),
}
k = sys.argv[1] if len(sys.argv) > 1 else 'k'
s = SPK[k]
html = f'''<!doctype html><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:transparent;font-family:Inter;color:#fff;position:relative}}
.band{{position:absolute;left:0;right:0;background:#000}}
.t{{top:0;height:371px;padding:44px 48px 0}}
.b{{top:979px;bottom:0;padding:48px 48px 0}}
.row{{display:flex;align-items:center;gap:20px;font-size:28px;font-weight:500;letter-spacing:-.01em;white-space:nowrap}}
.row b{{width:48px;height:48px;border-radius:50%;background:#E8360A;font-size:22px;font-weight:700;display:grid;place-items:center;flex:none}}
.row i{{flex:1;height:6px;background:#E8360A;min-width:40px}}
.row .d{{font-size:22px;text-transform:uppercase;letter-spacing:.06em;font-weight:500}}
h1{{margin-top:44px;font-size:64px;font-weight:700;letter-spacing:-.04em;line-height:1}}
h2{{margin-top:16px;font-size:30px;line-height:38px;font-weight:400;color:#ddd;letter-spacing:-.01em}}
.b p{{font-size:30px;line-height:40px;color:#ddd}}
.b .u{{font-size:40px;line-height:50px;font-weight:700;color:#E8360A;letter-spacing:-.02em;margin:6px 0 14px}}
</style><body>
<div class="band t">
<div class="row"><span>proto robot</span><b>#0</b><i></i><span class="d">Praha, 23. 10.</span></div>
<h1>{s['name']}</h1><h2>{s['talk']}</h2>
</div>
<div class="band b">
<p>Celý záznam, {s['minutes']} minut, s kapitolami:</p>
<div class="u">protorobot.cz/0</div>
<p>Další díl: čtvrtek 26. 11., Brno.<br>Roboti v laboratořích a nemocnicích.</p>
</div>
'''
out = pathlib.Path(__file__).parent / f'{k}_plate.png'
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350}); pg.set_content(html); pg.wait_for_timeout(300)
    pg.screenshot(path=str(out), omit_background=True); b.close()
print('wrote', out)
