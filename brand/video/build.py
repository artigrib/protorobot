"""Video overlays for PROTO ROBOT #0 in the site's system (Archivo, #FF5A00, black rectangles, duotone photos).
Renders PNGs into brand/video/<format>/: intro cards per talk, end cards CZ/EN, lower thirds per speaker,
a subtitle plate sample. Lower thirds and the subtitle plate have transparent backgrounds."""
import asyncio, pathlib, shutil, sys

REPO = pathlib.Path(sys.argv[1])
WORK = pathlib.Path(sys.argv[2])
FONTS = pathlib.Path(sys.argv[3])
OUT = REPO / "brand" / "video"

FMT = {"9x16": (1080, 1920), "1x1": (1080, 1080), "16x9": (1920, 1080)}

TALKS = [
    # slug, name, org, title on the intro card, background photo, logos (white versions)
    ("konecny", "Tomáš Konečný", "Robotservice", "Běžné problémy servisních robotů", "8129", []),
    ("vitek", "Lukáš Vítek", "Integra Robotics", "Physical AI a humanoidi v průmyslu", "8202", ["logo-integra-light.svg"]),
    ("danieau", "Fabien Danieau", "Pollen Robotics / Hugging Face", "Reachy Mini: open-source desk robot", "8357", ["logo-pollen.webp", "logo-hf.svg"]),
    ("bruna", "Ondřej Bruna", "Spoluautor a vývojář KORDu", "KORD: Lessons Learned", "8397", []),
]
DEMOS = [("reachy-demo", "Reachy Mini · live demo", "Pollen Robotics / Hugging Face", "8370")]

FONT_CSS = """
@font-face{font-family:A;font-style:normal;font-weight:100 900;font-stretch:62% 125%;src:url(f/archivo-latin-wdth-normal.woff2) format('woff2')}
@font-face{font-family:A;font-style:italic;font-weight:100 900;font-stretch:62% 125%;src:url(f/archivo-latin-wdth-italic.woff2) format('woff2')}
@font-face{font-family:A;font-style:normal;font-weight:100 900;font-stretch:62% 125%;src:url(f/archivo-latin-ext-wdth-normal.woff2) format('woff2');unicode-range:U+0100-024F,U+1E00-1EFF}
@font-face{font-family:A;font-style:italic;font-weight:100 900;font-stretch:62% 125%;src:url(f/archivo-latin-ext-wdth-italic.woff2) format('woff2');unicode-range:U+0100-024F,U+1E00-1EFF}
"""

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%(w)spx;height:%(h)spx;overflow:hidden;font-family:A,Arial,sans-serif;-webkit-font-smoothing:antialiased}
body{position:relative;--u:%(u)spx}
.title{font-weight:900;font-style:italic;font-stretch:125%%;line-height:.8;letter-spacing:-.05em;color:#fff;text-transform:uppercase;text-align:center;white-space:nowrap}
.title span{display:block}
.badge{display:inline-flex;align-items:center;justify-content:center;background:#000;color:#fff;text-transform:uppercase;letter-spacing:-.01em;white-space:nowrap}
.duo{position:absolute;inset:0;background:#5C1C00;overflow:hidden}
.duo img{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;filter:grayscale(1) contrast(1.15) brightness(1.15)}
.duo::before{content:"";position:absolute;inset:0;background:#FF5A00;mix-blend-mode:multiply;z-index:1}
.duo::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.15),rgba(0,0,0,.55));z-index:1}
.stack{position:absolute;left:0;right:0;z-index:2;display:flex;flex-direction:column;align-items:center}
.sub{color:#fff;text-align:center;font-weight:500;letter-spacing:-.01em}
"""


def page(w, h, body, extra=""):
    u = min(w, h) / 1080
    css = FONT_CSS + BASE % {"w": w, "h": h, "u": u} + extra
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>'


def intro(fmt, w, h, badge, line, photo, logos):
    tall = h > w
    size = {"9x16": 196, "1x1": 190, "16x9": 250}[fmt]
    top = {"9x16": 700, "1x1": 300, "16x9": 270}[fmt]
    bsize = {"9x16": 52, "1x1": 46, "16x9": 46}[fmt]
    lsize = {"9x16": 46, "1x1": 40, "16x9": 42}[fmt]
    logo_h = {"9x16": 56, "1x1": 48, "16x9": 52}[fmt]
    lg = "".join(f'<img src="logos/{l}" style="height:{logo_h}px">' for l in logos)
    body = f'''<div class="duo"><img src="photos/{photo}.webp"></div>
<div class="stack" style="top:{top}px">
  <div class="title" style="font-size:{size}px"><span>PROTO</span><span>ROBOT</span></div>
  <div class="badge" style="margin-top:{round(size*.22)}px;height:{round(bsize*1.9)}px;padding:0 {round(bsize*.9)}px;font-size:{bsize}px">{badge}</div>
  <div class="sub" style="margin-top:{round(bsize*1.1)}px;font-size:{lsize}px;max-width:{w-160}px;white-space:normal;line-height:1.15">{line}</div>
  <div style="display:flex;gap:{round(logo_h*.6)}px;align-items:center;margin-top:{round(bsize*1.1)}px">{lg}</div>
</div>'''
    return page(w, h, body)


def endcard(fmt, w, h, lang):
    t = dict(cs=("Na #0 mluvili", "Sledujte nás na Lumě", "#1 připravujeme"),
             en=("Spoke at #0", "Follow us on Luma", "#1 is in the works"))[lang]
    size = {"9x16": 118, "1x1": 104, "16x9": 120}[fmt]
    top = {"9x16": 520, "1x1": 150, "16x9": 150}[fmt]
    lh = {"9x16": 50, "1x1": 42, "16x9": 46}[fmt]
    body = f'''<div style="position:absolute;inset:0;background:#F0F0F0"></div>
<div class="stack" style="top:{top}px;color:#000">
  <div class="title" style="font-size:{round(size*1.6)}px;color:#000"><span>PROTO</span><span>ROBOT</span></div>
  <div class="badge" style="margin-top:{round(size*.35)}px;height:{round(size*.75)}px;padding:0 {round(size*.4)}px;font-size:{round(size*.38)}px">{t[2]}</div>
  <div style="margin-top:{round(size*.6)}px;font-size:{round(size*.2)}px;letter-spacing:.02em;text-transform:uppercase;color:#5c5c5c">{t[0]}</div>
  <div style="display:flex;gap:{round(lh*.8)}px;align-items:center;margin-top:{round(size*.15)}px;font-weight:600;font-size:{round(lh*.8)}px;letter-spacing:-.02em;white-space:nowrap">
    <span style="display:inline-flex;gap:12px;align-items:center"><img src="logos/logo-hf.svg" style="height:{lh}px;filter:grayscale(1) contrast(1.15)">Hugging Face</span>
    <span style="display:inline-flex;gap:12px;align-items:center"><img src="logos/logo-pollen.webp" style="height:{lh}px;filter:grayscale(1) contrast(1.15)">Pollen Robotics</span>
    {'' if fmt != '16x9' else f'<span style="display:inline-flex;gap:12px;align-items:center"><img src="logos/logo-integra.svg" style="height:{round(lh*1.1)}px;filter:grayscale(1)">Integra Robotics</span>'}
  </div>
  {'' if fmt == '16x9' else f'<div style="display:flex;gap:12px;align-items:center;margin-top:{round(lh*.5)}px;font-weight:600;font-size:{round(lh*.8)}px;letter-spacing:-.02em"><img src="logos/logo-integra.svg" style="height:{round(lh*1.1)}px;filter:grayscale(1)">Integra Robotics</div>'}
  <div style="margin-top:{round(size*.7)}px;font-weight:500;font-size:{round(size*.55)}px;letter-spacing:-.03em">protorobot.cz</div>
  <div style="margin-top:{round(size*.3)}px;display:inline-flex;align-items:center;height:{round(size*.7)}px;padding:0 {round(size*.45)}px;border-radius:999px;background:#FF5A00;color:#000;text-transform:uppercase;font-size:{round(size*.3)}px">{t[1]}</div>
</div>'''
    return page(w, h, body)


def lower(fmt, w, h, name, org, logos):
    # safe zones: phones keep clear of the bottom ~250px app UI
    x = {"9x16": 60, "1x1": 60, "16x9": 96}[fmt]
    bottom = {"9x16": 420, "1x1": 90, "16x9": 96}[fmt]
    nsize = {"9x16": 56, "1x1": 50, "16x9": 52}[fmt]
    lg = "".join(f'<img src="logos/{l}" style="height:{round(nsize*.62)}px">' for l in logos)
    body = f'''<div style="position:absolute;left:{x}px;bottom:{bottom}px;background:#000;color:#fff;padding:{round(nsize*.45)}px {round(nsize*.55)}px {round(nsize*.5)}px;display:flex;flex-direction:column;gap:{round(nsize*.22)}px">
  <div style="font-weight:500;font-size:{nsize}px;line-height:1;letter-spacing:-.03em;text-transform:uppercase;white-space:nowrap">{name}</div>
  <div style="display:flex;align-items:center;gap:{round(nsize*.3)}px;font-size:{round(nsize*.46)}px;letter-spacing:.03em;text-transform:uppercase;color:#BDBDBD;white-space:nowrap">{lg}<span>{org}</span></div>
</div>
<div style="position:absolute;left:{x}px;bottom:{bottom}px;width:{round(nsize*.18)}px;height:100%;max-height:{round(nsize*2.15)}px;background:#FF5A00;transform:translateX(-100%)"></div>'''
    return page(w, h, body, "html,body{background:transparent}")


def subtitle(fmt, w, h, text):
    size = {"9x16": 50, "1x1": 44, "16x9": 46}[fmt]
    bottom = {"9x16": 520, "1x1": 110, "16x9": 90}[fmt]
    body = f'''<div style="position:absolute;left:0;right:0;bottom:{bottom}px;display:flex;justify-content:center">
  <div style="background:#000;color:#fff;font-weight:600;font-size:{size}px;line-height:1.25;padding:{round(size*.25)}px {round(size*.45)}px;max-width:{w-160}px;text-align:center">{text}</div>
</div>'''
    return page(w, h, body, "html,body{background:transparent}")


async def main():
    from playwright.async_api import async_playwright
    if OUT.exists():
        shutil.rmtree(OUT)
    jobs = []
    for fmt, (w, h) in FMT.items():
        for slug, name, org, title, photo, logos in TALKS:
            jobs.append((f"{fmt}/intro_{slug}.png", intro(fmt, w, h, f"#0 · {name}", title, photo, logos), w, h, False))
            jobs.append((f"{fmt}/lower_{slug}.png", lower(fmt, w, h, name, org, logos), w, h, True))
        for slug, badge, line, photo in DEMOS:
            jobs.append((f"{fmt}/intro_{slug}.png", intro(fmt, w, h, f"#0 · {badge}", line, photo, ["logo-pollen.webp", "logo-hf.svg"]), w, h, False))
        for lang in ("cs", "en"):
            jobs.append((f"{fmt}/end_{lang}.png", endcard(fmt, w, h, lang), w, h, False))
        jobs.append((f"{fmt}/subtitle_sample.png", subtitle(fmt, w, h, "Can you be sad?"), w, h, True))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        for name, html, w, h, transparent in jobs:
            await pg.set_viewport_size({"width": w, "height": h})
            f = WORK / "page.html"
            f.write_text(html, encoding="utf-8")
            await pg.goto(f.as_uri())
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(150)
            out = OUT / name
            out.parent.mkdir(parents=True, exist_ok=True)
            await pg.screenshot(path=str(out), omit_background=transparent)
        await b.close()
    print(len(jobs), "files")


asyncio.run(main())
