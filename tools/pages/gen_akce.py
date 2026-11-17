#!/usr/bin/env python3
"""Generate /akce/ and /en/akce/ (upcoming events). Run from repo root: python3 tools/pages/gen_akce.py ."""
import sys, os, html, re

root = sys.argv[1] if len(sys.argv) > 1 else "."
LUMA_EVT = "https://luma.com/sxk08o64"
LUMA_CAL = "https://luma.com/user/protorobot"

granty = open(os.path.join(root, "granty/index.html"), encoding="utf-8").read()
dilny = open(os.path.join(root, "dilny/index.html"), encoding="utf-8").read()
# shared tokens, reset, pills and header from the grants page
base_css = granty.split("<style>", 1)[1].split("/* page: grants list */", 1)[0]
foot_css = "\n".join(l for l in dilny.splitlines() if l.startswith(".foot"))
icon = re.search(r'<link rel="icon"[^>]*>', granty).group(0)

PAGE_CSS = """
/* page: upcoming events */
main{padding:var(--s3) var(--gt) var(--s5)}
.hero{padding-bottom:var(--s2);border-bottom:2px solid var(--black)}
.kicker{font-size:14px;text-transform:uppercase;letter-spacing:.04em;display:flex;align-items:center;gap:10px}
.kicker svg{width:56px;height:14px}
h1{font-weight:300;font-size:clamp(48px,9vw,140px);line-height:.88;letter-spacing:-.05em;margin-top:var(--s2);text-wrap:balance}
h1 b{font-weight:700}
.lede{font-size:clamp(20px,2vw,28px);line-height:1.25;letter-spacing:-.015em;max-width:34em;margin-top:var(--s2);text-wrap:pretty}
.ev{list-style:none;margin-top:var(--s3);display:grid;gap:10px}
.e{display:grid;grid-template-columns:minmax(150px,240px) minmax(0,1fr) auto;gap:var(--s1) var(--s3);align-items:start;background:var(--white);border-radius:24px;padding:var(--s3)}
.e--now{background:var(--black);color:var(--white)}
.when{font-size:clamp(28px,3vw,44px);font-weight:700;letter-spacing:-.04em;line-height:.95}
.e--now .when{color:var(--orange)}
.city{display:block;margin-top:8px;font-size:14px;font-weight:400;letter-spacing:.02em;text-transform:uppercase;color:var(--grey-text)}
.e--now .city{color:rgba(255,255,255,.7)}
.e h2{font-weight:600;font-size:clamp(24px,2.4vw,34px);line-height:1.05;letter-spacing:-.03em;text-wrap:balance}
.e p{margin-top:10px;font-size:18px;line-height:1.4;max-width:40em;text-wrap:pretty}
.tag{display:inline-flex;align-items:center;height:32px;padding:0 14px;border-radius:999px;border:2px solid currentColor;font-size:13px;text-transform:uppercase;letter-spacing:.02em;white-space:nowrap}
.e--now .tag{border-color:var(--orange);background:var(--orange);color:var(--black)}
.acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:var(--s2)}
.e--now .pill{background:var(--white);color:var(--black)} .e--now .pill:hover{background:var(--grey-pill)}
.e--now .pill--orange{background:var(--orange)} .e--now .pill--orange:hover{background:var(--white)}
@media (max-width:820px){.e{grid-template-columns:1fr auto;padding:var(--s2)}.e>div:nth-child(2){grid-column:1/-1;grid-row:2}.tag{grid-column:2;grid-row:1;justify-self:end}}
.join{margin-top:var(--s4);display:grid;grid-template-columns:minmax(0,1fr) auto;gap:var(--s2);align-items:end;border-top:2px solid var(--black);padding-top:var(--s2)}
.join p{font-size:clamp(20px,2vw,28px);line-height:1.25;letter-spacing:-.015em;max-width:30em}
@media (max-width:700px){.join{grid-template-columns:1fr}}
"""

T = {
 "cs": dict(
  path="akce/", other="/en/akce/", other_lang="en", other_label="EN", other_aria="English",
  title="Co chystáme | PROTO ROBOT",
  desc="Další setkání PROTO ROBOT: Brno 26. 11., v prosinci open-source robotický stack, v lednu venture workshop pro zakladatele, v únoru robotický hackathon v Praze.",
  skip="Přeskočit na obsah", kicker="Komunita PROTO ROBOT",
  h1="<b>Co</b> chystáme",
  lede="Otevřená setkání lidí z&nbsp;robotiky v&nbsp;Praze a&nbsp;Brně. Vstup zdarma, přesné termíny a&nbsp;registrace vždy nejdřív na Lumě.",
  nav=[("/1/", "#1"), ("/0/", "#0"), ("/dilny/", "Mapa"), ("/granty/", "Granty")], here="Akce", follow="Sledovat",
  events=[
   dict(now=True, when="26.&nbsp;11.", city="Brno · FF MU, aula C33", tag="Registrace otevřená",
        name="#1 Roboti v&nbsp;laboratořích a&nbsp;nemocnicích",
        text="Robotická chirurgie z&nbsp;praxe, laboratorní robot openTube, panel o&nbsp;robotech v&nbsp;péči a&nbsp;demo stoly. Od&nbsp;18:30.",
        acts=[(LUMA_EVT, "Registrace", True, True), ("/1/", "Program", False, False)]),
   dict(when="Prosinec", city="Praha", tag="Termín upřesníme",
        name="Open-source robotický stack",
        text="Workshop o&nbsp;otevřeném softwaru pro roboty: co dnes funguje od simulace po reálný hardware a&nbsp;jak s&nbsp;tím začít."),
   dict(when="Leden", city="Praha", tag="Termín upřesníme",
        name="Venture workshop pro robotické zakladatele",
        text="Jak získat první peníze na hardware a&nbsp;robotiku: co investoři sledují, jak vypadá dobrý pitch a&nbsp;kde hledat podporu."),
   dict(when="26.–28.&nbsp;2.", city="Praha · 2027", tag="Plánujeme",
        name="Robotický hackathon",
        text="Víkend stavění na reálném hardwaru: týmy, mentoři, porota a&nbsp;v&nbsp;neděli veřejné finále s&nbsp;demy."),
  ],
  join="Chcete se zapojit jako řečník, mentor, partner nebo tým na hackathon? Sledujte nás na Lumě a&nbsp;napište nám tam nebo na LinkedInu.",
  join_btn="Sledovat na Lumě",
  foot=[("/", "Domů"), ("/1/", "#1"), ("/0/", "#0"), ("/dilny/", "Kde stavět"), ("/granty/", "Granty")],
  foot_other="English", meta="© 2026 PROTO ROBOT. Máme toho hodně. A&nbsp;proto robot.",
 ),
 "en": dict(
  path="en/akce/", other="/akce/", other_lang="cs", other_label="CZ", other_aria="Česky",
  title="Upcoming events | PROTO ROBOT",
  desc="Next PROTO ROBOT events: Brno on 26 Nov, an open-source robotics stack workshop in December, a venture workshop for founders in January and a robotics hackathon in Prague in February.",
  skip="Skip to content", kicker="PROTO ROBOT community",
  h1="<b>What's</b> next",
  lede="Open meetups for people in robotics in Prague and Brno. Free entry; exact dates and registration always land on Luma first.",
  nav=[("/en/1/", "#1"), ("/en/0/", "#0"), ("/en/dilny/", "Map"), ("/en/granty/", "Grants")], here="Events", follow="Follow",
  events=[
   dict(now=True, when="26&nbsp;Nov", city="Brno · Faculty of Arts MU, C33", tag="Registration open",
        name="#1 Robots in labs and hospitals",
        text="Robotic surgery in practice, the openTube lab robot, a panel on robots in care and demo tables. From 18:30. Talks in Czech, demos and networking in English.",
        acts=[(LUMA_EVT, "Register", True, True), ("/en/1/", "Programme", False, False)]),
   dict(when="December", city="Prague", tag="Date TBA",
        name="Open-source robotics stack",
        text="A workshop on open software for robots: what works today, from simulation to real hardware, and how to get started."),
   dict(when="January", city="Prague", tag="Date TBA",
        name="Venture workshop for robotics founders",
        text="How to raise your first money for hardware and robotics: what investors look for, what a good pitch looks like and where to find support."),
   dict(when="26–28&nbsp;Feb", city="Prague · 2027", tag="Planned",
        name="Robotics hackathon",
        text="A weekend of building on real hardware: teams, mentors, a jury and a public finale with demos on Sunday."),
  ],
  join="Want to join as a speaker, mentor, partner or hackathon team? Follow us on Luma and message us there or on LinkedIn.",
  join_btn="Follow on Luma",
  foot=[("/en/", "Home"), ("/en/1/", "#1"), ("/en/0/", "#0"), ("/en/dilny/", "Where to build"), ("/en/granty/", "Grants")],
  foot_other="Česky", meta='© 2026 PROTO ROBOT. <span lang="cs">Máme toho hodně. A&nbsp;proto robot.</span>',
 ),
}

def page(lang):
    t = T[lang]
    url = "https://protorobot.cz/" + t["path"]
    nav = "\n".join(f'    <a class="pill" href="{h}">{l}</a>' for h, l in t["nav"])
    nav += f'\n    <a class="pill" href="{url}" aria-current="page">{t["here"]}</a>'
    evs = []
    for e in t["events"]:
        acts = ""
        if e.get("acts"):
            acts = '<div class="acts">' + "".join(
                f'<a class="pill{" pill--orange" if o else ""}" href="{h}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}>{l}</a>'
                for h, l, o, ext in e["acts"]) + "</div>"
        evs.append(f'''  <li class="e{" e--now" if e.get("now") else ""}">
    <div><div class="when">{e["when"]}</div><span class="city">{e["city"]}</span></div>
    <div><h2>{e["name"]}</h2><p>{e["text"]}</p>{acts}</div>
    <span class="tag">{e["tag"]}</span>
  </li>''')
    foot = "".join(f'<a href="{h}">{l}</a>' for h, l in t["foot"])
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t["title"]}</title>
<meta name="description" content="{html.escape(t["desc"])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="cs" href="https://protorobot.cz/akce/">
<link rel="alternate" hreflang="en" href="https://protorobot.cz/en/akce/">
<link rel="alternate" hreflang="x-default" href="https://protorobot.cz/akce/">
<meta name="theme-color" content="#FF5A00">
<meta name="color-scheme" content="light">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{t["title"]}">
<meta property="og:description" content="{html.escape(t["desc"])}">
<meta property="og:image" content="https://protorobot.cz/img/og.jpg?v=4">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{icon}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap">
<style>{base_css}{foot_css}
{PAGE_CSS}</style>
</head>
<body>
<a class="skip" href="#main">{t["skip"]}</a>
<header class="top">
  <nav aria-label="Menu">
{nav}
  </nav>
  <div class="top__right">
    <a class="pill top__lang" href="{t["other"]}" hreflang="{t["other_lang"]}" lang="{t["other_lang"]}" aria-label="{t["other_aria"]}">{t["other_label"]}</a>
    <a class="pill pill--orange" href="{LUMA_CAL}" target="_blank" rel="noopener">{t["follow"]}</a>
  </div>
</header>

<main id="main">
<div class="hero">
  <div class="kicker"><svg viewBox="0 0 560 140" aria-hidden="true"><rect x="0" y="58" width="372" height="24" fill="#FF5A00"/><circle cx="442" cy="70" r="70" fill="#FF5A00"/></svg>{t["kicker"]}</div>
  <h1>{t["h1"]}</h1>
  <p class="lede">{t["lede"]}</p>
</div>

<ol class="ev">
{chr(10).join(evs)}
</ol>

<div class="join"><p>{t["join"]}</p><a class="pill pill--orange" href="{LUMA_CAL}" target="_blank" rel="noopener">{t["join_btn"]}</a></div>
</main>

<footer class="foot">
  {foot}
  <a href="{LUMA_CAL}" target="_blank" rel="noopener">Luma</a>
  <a href="{t["other"]}" hreflang="{t["other_lang"]}" lang="{t["other_lang"]}">{t["foot_other"]}</a>
  <div class="foot__meta">{t["meta"]}</div>
</footer>
</body>
</html>
'''

for lang in ("cs", "en"):
    out = os.path.join(root, T[lang]["path"], "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(page(lang))
    print("wrote", out)
