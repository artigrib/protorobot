#!/usr/bin/env python3
"""Build /1/ and /en/1/ (PROTO ROBOT #1 Brno) from the /0/ pages: same head, CSS and scripts, new body.
Run from repo root: python3 tools/pages/gen_1.py .
Names and places appear only with written confirmation; everything else is a labelled placeholder.
"""
import re, sys, pathlib

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
LUMA = 'https://luma.com/user/protorobot'  # TODO: replace with the #1 event link on go

T = {
 'cs': dict(
  lang='cs', path='1', other='en/1',
  title='PROTO ROBOT #1 Brno, 26. listopadu 2026: roboti v laboratořích a nemocnicích',
  desc='PROTO ROBOT #1 Brno: otevřený večer o robotech v laboratořích a nemocnicích. Čtvrtek 26. 11. 2026, aula C33 FF MU, Arna Nováka 1. Vstup zdarma, registrace nutná.',
  og_title='PROTO ROBOT #1 Brno: roboti v laboratořích a nemocnicích',
  og_desc='Čtvrtek 26. 11. 2026 od 19:00, FF MU, Arna Nováka 1. Přednášky, panel a ukázky robotů. Vstup zdarma.',
  og_alt='PROTO ROBOT #1 Brno, 26. 11. 2026',
  skip='Přeskočit na obsah', menu='Menu', sections='Sekce',
  nav=[('#programme','Program'),('#speakers','Řečníci'),('#where','Kde'),('/0/','#0')],
  lang_btn='EN', lang_label='English', cta='Registrace',
  hero_label='Proto Robot #1 Brno',
  faces=['#1 Brno', 'čt 26. 11. 2026', 'FF MU, Arna Nováka 1'],
  faces_vh='#1 Brno, čtvrtek 26. 11. 2026, FF MU, Arna Nováka 1',
  cos_label='Téma', cos=['Roboti v laboratořích a nemocnicích'],
  nums=[('26. 11.','čtvrtek'),('19:00','otevřeno od'),('150','míst v sále'),('0 Kč','vstup')],
  nums_label='#1 v číslech',
  h1='PROTO ROBOT #1 Brno',
  intro=('Roboti už v&nbsp;Česku operují pacienty, pomáhají lidem znovu chodit a&nbsp;ulehčují práci sestrám. '
         'Uvidíte, jak jsou zavedená existující řešení, a&nbsp;potkáte lidi z&nbsp;praxe pro budoucí piloty vlastních produktů.'),
  facts=[('#programme','Program'),('#speakers','Řečníci'),('#where','Kde')], facts_cta='Registrovat se',
  prog_h='Program',
  prog=[
   ('19:00','Dveře','Příchod, občerstvení ve foyer'),
   ('19:30','Úvod','PROTO ROBOT #1 Brno'),
   ('19:40','Robotická chirurgie v praxi: da Vinci ve FNUSA','prim. MUDr. Petr Filipenský, Fakultní nemocnice u&nbsp;sv. Anny'),
   ('19:55','Jak se robot zavádí do nemocnice: Versius ve FN Brno','Řečníka upřesníme'),
   ('20:10','Panel: Technologie v péči. Kdo je přijme a co je etické?','Lucie Vidovićová (FSS MU), David Černý (ÚSP AV ČR) a&nbsp;praktik z&nbsp;nemocnice, upřesníme. Moderuje Arti'),
   ('20:35','Otázky z publika',''),
   ('20:40','Lightning: ukaž svůj projekt','5 × 2 minuty, přihlášky v&nbsp;registraci'),
   ('20:50','Shrnutí',''),
   ('21:00','Networking a demo stoly','Do 22:00. VR simulátor chirurgického robota, exoskelet pro zvedání břemen'),
  ],
  prog_note='Program doplňujeme, jména zveřejňujeme po potvrzení. Přednášky česky, demo i&nbsp;anglicky.',
  demo1='Konzole chirurgického robota', demo1s='VR simulátor, vyzkoušíte si řízení ramen',
  demo2='Exoskelet pro zvedání', demo2s='Nasadíte si ho a&nbsp;zvednete břemeno, pro sestry a&nbsp;pečovatele',
  spk_h='Řečníci',
  spk=[dict(img='filipensky', name='Petr Filipenský', org='Fakultní nemocnice u sv. Anny v Brně', talk='Robotická chirurgie v praxi: da Vinci ve FNUSA', note='Primář. FNUSA operuje na robotu da Vinci od roku 2023, v&nbsp;roce 2025 to bylo kolem 269 výkonů.'),
       dict(img='vidovicova', name='Lucie Vidovićová', org='Fakulta sociálních studií MU', talk='Panel: Technologie v péči', note='Socioložka stárnutí. Etika asistivních technologií v&nbsp;sociálních službách a&nbsp;to, jak lidé roboty v&nbsp;péči přijímají.'),
       dict(img='cerny', name='David Černý', org='Ústav státu a práva AV ČR', talk='Panel: Technologie v péči', note='Etik AI a&nbsp;robotů, spolueditor knihy Autonomous Vehicle Ethics (Oxford, 2022).')],
  spk_more='Další řečníky doplníme.',
  where_h='Kde', where_name='Aula C33, Filozofická fakulta Masarykovy univerzity', where_addr='Arna Nováka 1, Brno, budova C, 3. patro',
  where_note='Asi 15 minut pěšky od FNUSA, hned po konferenci BioTech jak Brno. Bezbariérový přístup výtahem. Občerstvení a&nbsp;nealko, bez alkoholu podle pravidel fakulty.',
  where_map='Otevřít mapu',
  who_h='Pro koho', who='Inženýři a&nbsp;vývojáři robotiky, lékaři, sestry, fyzioterapeuti, laboranti, studenti VUT (FEKT, FSI, FIT) a&nbsp;MUNI (FI, LF), zakladatelé medtech startupů.',
  tix_h='Vstup zdarma, registrace nutná', tix_lede='Kapacita sálu je 150 míst. Zaregistrujte se na Lumě, ať víme, s&nbsp;kolika lidmi počítat.',
  tix_cta='Registrovat se na Lumě',
  prev_h='#0 Praha', prev_lede='Jak proběhl nultý díl: program, fotky a&nbsp;záznamy všech čtyř přednášek.', prev_cta='#0: program, fotky a&nbsp;záznamy',
  foot=[('/0/','#0'),('/dilny/','Kde stavět'),('/granty/','Granty')], foot_luma='Sledovat na Lumě', foot_meta='© 2026 PROTO ROBOT. Máme toho hodně. A&nbsp;proto robot.',
  ld_name='PROTO ROBOT #1 Brno: roboti v laboratořích a nemocnicích', ld_desc='Otevřený večer o robotech v laboratořích a nemocnicích. Přednášky, panel a ukázky robotů.',
 ),
 'en': dict(
  lang='en', path='en/1', other='1',
  title='PROTO ROBOT #1 Brno, 26 November 2026: robots in labs and hospitals',
  desc='PROTO ROBOT #1 Brno: an open evening on robots in labs and hospitals. Thursday 26 Nov 2026, lecture hall C33, Faculty of Arts MU, Arna Nováka 1. Free entry, registration required.',
  og_title='PROTO ROBOT #1 Brno: robots in labs and hospitals',
  og_desc='Thursday 26 Nov 2026 from 19:00, Faculty of Arts MU, Arna Nováka 1. Talks, a panel and robot demos. Free entry.',
  og_alt='PROTO ROBOT #1 Brno, 26 Nov 2026',
  skip='Skip to content', menu='Menu', sections='Sections',
  nav=[('#programme','Programme'),('#speakers','Speakers'),('#where','Where'),('/en/0/','#0')],
  lang_btn='CZ', lang_label='Česky', cta='Register',
  hero_label='Proto Robot #1 Brno',
  faces=['#1 Brno', 'Thu 26 Nov 2026', 'FA MU, Arna Nováka 1'],
  faces_vh='#1 Brno, Thursday 26 Nov 2026, Faculty of Arts MU, Arna Nováka 1',
  cos_label='Topic', cos=['Robots in labs and hospitals'],
  nums=[('26 Nov','Thursday'),('19:00','doors'),('150','seats'),('free','entry')],
  nums_label='#1 in numbers',
  h1='PROTO ROBOT #1 Brno',
  intro=('Robots already operate on patients in Czechia, help people walk again and take load off nurses. '
         'See how existing solutions are deployed, and meet the people from practice you will need to pilot your own product.'),
  facts=[('#programme','Programme'),('#speakers','Speakers'),('#where','Where')], facts_cta='Register',
  prog_h='Programme',
  prog=[
   ('19:00','Doors','Arrival, refreshments in the foyer'),
   ('19:30','Opening','PROTO ROBOT #1 Brno'),
   ('19:40','Robotic surgery in practice: da Vinci at FNUSA','Petr Filipenský, MD, head of department, St. Anne\'s University Hospital Brno'),
   ('19:55','Bringing a robot into a hospital: Versius at FN Brno','Speaker to be confirmed'),
   ('20:10','Panel: Technology in care. Who accepts it, and what is ethical?','Lucie Vidovićová (FSS MU), David Černý (Institute of State and Law, CAS) and a clinician, to be confirmed. Moderated by Arti'),
   ('20:35','Audience questions',''),
   ('20:40','Lightning: show your project','5 × 2 minutes, sign up at registration'),
   ('20:50','Wrap-up',''),
   ('21:00','Networking and demo tables','Until 22:00. VR simulator of a surgical robot, a lifting exoskeleton'),
  ],
  prog_note='Programme in progress; names go up once confirmed. Talks in Czech, demo tables also in English.',
  demo1='Surgical robot console', demo1s='VR simulator, try steering the arms yourself',
  demo2='Lifting exoskeleton', demo2s='Put it on and lift a load, built for nurses and carers',
  spk_h='Speakers',
  spk=[dict(img='filipensky', name='Petr Filipenský', org="St. Anne's University Hospital Brno", talk='Robotic surgery in practice: da Vinci at FNUSA', note='Head of department. FNUSA has operated with a da Vinci robot since 2023, about 269 procedures in 2025.'),
       dict(img='vidovicova', name='Lucie Vidovićová', org='Faculty of Social Studies, Masaryk University', talk='Panel: Technology in care', note='Sociologist of ageing. Ethics of assistive technologies in social care and how people accept robots.'),
       dict(img='cerny', name='David Černý', org='Institute of State and Law, Czech Academy of Sciences', talk='Panel: Technology in care', note='Ethicist of AI and robots, co-editor of Autonomous Vehicle Ethics (Oxford, 2022).')],
  spk_more='More speakers to be announced.',
  where_h='Where', where_name='Lecture hall C33, Faculty of Arts, Masaryk University', where_addr='Arna Nováka 1, Brno, building C, 3rd floor',
  where_note='About 15 minutes on foot from the FNUSA hospital, right after the BioTech jak Brno conference. Step-free access by lift. Refreshments and soft drinks; no alcohol, faculty rules.',
  where_map='Open map',
  who_h='Who it is for', who='Robotics engineers and developers, clinicians, nurses, physiotherapists, lab staff, students of VUT (FEKT, FSI, FIT) and MUNI (FI, LF), founders of medtech startups.',
  tix_h='Free entry, registration required', tix_lede='The hall seats 150. Register on Luma so we know how many people to expect.',
  tix_cta='Register on Luma',
  prev_h='#0 Prague', prev_lede='How edition #0 went: programme, photos and recordings of all four talks.', prev_cta='#0: programme, photos and recordings',
  foot=[('/en/0/','#0'),('/en/dilny/','Where to build'),('/en/granty/','Grants')], foot_luma='Follow on Luma', foot_meta='© 2026 PROTO ROBOT. We have a lot on our hands. Hence the robot.',
  ld_name='PROTO ROBOT #1 Brno: robots in labs and hospitals', ld_desc='An open evening on robots in labs and hospitals. Talks, a panel and robot demos.',
 ),
}

HERO_H = ['h-1','h-2','h-3']
HERO_V = ['v-1','v-2','v-3','v-4']
MAP = 'https://mapy.cz/zakladni?q=Arna%20Nov%C3%A1ka%201%2C%20Brno'

def ld(t):
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "{t['ld_name']}",
  "description": "{t['ld_desc']}",
  "startDate": "2026-11-26T19:00:00+01:00",
  "endDate": "2026-11-26T22:00:00+01:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "isAccessibleForFree": true,
  "location": {{
    "@type": "Place",
    "name": "Filozofická fakulta Masarykovy univerzity, aula C33",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "Arna Nováka 1",
      "addressLocality": "Brno",
      "addressCountry": "CZ"
    }}
  }},
  "image": [
    "https://protorobot.cz/img/og.jpg"
  ],
  "organizer": {{
    "@type": "Organization",
    "name": "PROTO ROBOT",
    "url": "https://protorobot.cz/",
    "sameAs": [
      "{LUMA}"
    ]
  }},
  "inLanguage": [
    "cs",
    "en"
  ],
  "url": "https://protorobot.cz/{t['path']}/"
}}
</script>'''

def body(t):
    slides = lambda ids: '\n'.join(
        f'    <div class="slide{" is-on" if i==0 else ""}"><img src="/img/1/{s}.webp" alt=""{" fetchpriority=\"high\"" if i==0 else " loading=\"lazy\" decoding=\"async\""}></div>'
        for i, s in enumerate(ids))
    nav = ''.join(f'\n      <a class="pill" href="{h}">{l}</a>' for h, l in t['nav'])
    faces = str(t['faces']).replace("'", '"')
    cos = ''.join(f'<span class="co">{c}</span>' for c in t['cos'])
    nums = ''.join(f'<li><b>{b}</b><span>{s}</span></li>' for b, s in t['nums'])
    facts = ''.join(f'<a href="{h}">{l}</a>' for h, l in t['facts'])
    prog = '\n'.join(
        f'    <li><time datetime="2026-11-26T{tm}+01:00">{tm}</time><div><b>{b}</b>{"<span>"+s+"</span>" if s else ""}</div></li>'
        for tm, b, s in t['prog'])
    photo = lambda s: (f'<div class="photo"><img src="/img/1/sp-{s["img"]}.webp" alt="{s["name"]}" width="600" height="600" loading="lazy" decoding="async"></div>' if s.get('img') else '<div class="photo photo--empty" aria-hidden="true"></div>')
    spk = '\n'.join(f'''    <article class="spk">
      {photo(s)}
      <h3 class="spk__name">{s['name']}</h3>
      <p class="spk__org">{s['org']}</p>
      <p class="spk__talk">{s['talk']}</p>
      <p class="spk__note">{s['note']}</p>
    </article>''' for s in t['spk'])
    foot = ''.join(f'\n  <a href="{h}">{l}</a>' for h, l in t['foot'])
    return f'''<body>
<a class="skip" href="#main">{t['skip']}</a>

<header class="top">
  <nav class="city" id="city" aria-label="{t['sections']}">
    <button class="city__name" type="button" id="cityBtn" aria-controls="cityNav" aria-expanded="true" aria-label="{t['menu']}"><span class="burger" aria-hidden="true"></span></button>
    <div class="city__nav" id="cityNav">{nav}
    </div>
  </nav>
  <div class="top__right">
    <a class="pill top__lang" href="/{t['other']}/" hreflang="{'en' if t['lang']=='cs' else 'cs'}" lang="{'en' if t['lang']=='cs' else 'cs'}" aria-label="{t['lang_label']}">{t['lang_btn']}</a>
    <a class="pill pill--orange top__cta" href="{LUMA}" target="_blank" rel="noopener">{t['cta']}</a>
  </div>
</header>

<div class="page" id="page">
<main id="main">

<section class="hero" id="top" aria-label="{t['hero_label']}">
  <div class="hero__bg">
    <div class="hero__track hero__track--h" data-track>
{slides(HERO_H)}
    </div>
    <div class="hero__track hero__track--v" data-track>
{slides(HERO_V)}
    </div>
  </div>
  <div class="hero__type" id="type" aria-hidden="true"><div class="hero__type__in"><span>PROTO</span><span>ROBOT</span></div></div>
  <div class="badge" id="badge" data-faces='{faces}'><span class="vh">{t['faces_vh']}</span><div class="badge__flip" aria-hidden="true"><span class="f-a">{t['faces'][0]}</span><span class="f-b" aria-hidden="true"></span></div></div>
  <div class="hero__cos"><span class="hero__cos__label">{t['cos_label']}</span>{cos}</div>
</section>

<section class="mod intro" id="about">
  <ul class="nums" aria-label="{t['nums_label']}">{nums}</ul>
  <h1 class="vh">{t['h1']}</h1>
  <p>{t['intro']}</p>
  <p class="facts">{facts}<a class="pill--orange" href="{LUMA}" target="_blank" rel="noopener">{t['facts_cta']}</a></p>
</section>

<section class="mod" id="programme">
  <h2>{t['prog_h']}</h2>
  <ol class="tl">
{prog}
  </ol>
  <p class="note">{t['prog_note']}</p>
  <div class="demo-grid">
    <figure class="demo"><div class="photo"><img src="/img/1/demo-versius.webp" alt="" loading="lazy" decoding="async"></div><figcaption><b>{t['demo1']}</b><span>{t['demo1s']}</span></figcaption></figure>
    <figure class="demo"><div class="photo"><img src="/img/1/demo-musclesuit.webp" alt="" loading="lazy" decoding="async"></div><figcaption><b>{t['demo2']}</b><span>{t['demo2s']}</span></figcaption></figure>
  </div>
</section>

<section class="mod speakers" id="speakers">
  <h2>{t['spk_h']}</h2>
  <div class="spk-grid">
{spk}
  </div>
  <p class="note">{t['spk_more']}</p>
</section>

<section class="mod where" id="where">
  <h2>{t['where_h']}</h2>
  <div class="where__grid">
    <div>
      <p class="lede"><b>{t['where_name']}</b><br>{t['where_addr']}</p>
      <p class="lede">{t['where_note']}</p>
      <div class="cta-row"><a class="pill" href="{MAP}" target="_blank" rel="noopener">{t['where_map']}</a></div>
    </div>
    <div class="photo where__photo"><img src="/img/1/kde-ffmu.webp" alt="" loading="lazy" decoding="async"></div>
  </div>
</section>

<section class="mod" id="who">
  <h2>{t['who_h']}</h2>
  <p class="lede">{t['who']}</p>
</section>

<section class="mod tix" id="tickets">
  <h2>{t['tix_h']}</h2>
  <p class="lede">{t['tix_lede']}</p>
  <div class="cta-row"><a class="pill pill--orange pill--lg" href="{LUMA}" target="_blank" rel="noopener">{t['tix_cta']}</a></div>
</section>

<section class="mod" id="prev">
  <h2>{t['prev_h']}</h2>
  <p class="lede">{t['prev_lede']}</p>
  <div class="cta-row"><a class="pill" href="/{'0' if t['lang']=='cs' else 'en/0'}/">{t['prev_cta']}</a></div>
</section>

</main>

<footer class="foot">{foot}
  <a href="{LUMA}" target="_blank" rel="noopener">{t['foot_luma']}</a>
  <a href="/{t['other']}/" hreflang="{'en' if t['lang']=='cs' else 'cs'}" lang="{'en' if t['lang']=='cs' else 'cs'}">{t['lang_label']}</a>
  <div class="foot__meta">{t['foot_meta']}</div>
</footer>
</div>
'''

EXTRA_CSS = '''.photo--empty{background:var(--orange-deep);background-image:repeating-linear-gradient(135deg,transparent 0 14px,rgba(0,0,0,.12) 14px 16px)}
.note{font-size:15px;opacity:.75;margin-top:var(--s2);max-width:34em}
.demo-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--g);margin-top:var(--s3)}
@media (max-width:640px){.demo-grid{grid-template-columns:minmax(0,1fr)}}
.demo{margin:0}.demo .photo{aspect-ratio:16/9}
.demo figcaption{margin-top:10px;font-size:15px;line-height:1.3}.demo figcaption b{display:block;font-size:17px}.demo figcaption span{color:var(--grey-text)}
.where__grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:var(--g);align-items:start}
.where__photo{aspect-ratio:3/2}
@media (max-width:760px){.where__grid{grid-template-columns:minmax(0,1fr)}.where__photo{display:none}}
.spk-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
@media (max-width:1100px){.demo-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--g);margin-top:var(--s3)}
@media (max-width:640px){.demo-grid{grid-template-columns:minmax(0,1fr)}}
.demo{margin:0}.demo .photo{aspect-ratio:16/9}
.demo figcaption{margin-top:10px;font-size:15px;line-height:1.3}.demo figcaption b{display:block;font-size:17px}.demo figcaption span{color:var(--grey-text)}
.where__grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:var(--g);align-items:start}
.where__photo{aspect-ratio:3/2}
@media (max-width:760px){.where__grid{grid-template-columns:minmax(0,1fr)}.where__photo{display:none}}
.spk-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:760px){.spk-grid{grid-template-columns:minmax(0,1fr)}}
</style>'''

for lang, t in T.items():
    src = (root / ('0' if lang == 'cs' else 'en/0') / 'index.html').read_text(encoding='utf-8')
    head, rest = src.split('<body>', 1)
    scripts = rest.split('</div>\n\n\n\n<script>', 1)[1]  # everything after the page div
    scripts = '<script>' + scripts
    # drop the lecture player script (third block)
    scripts = re.sub(r'<script>\n/\* Lecture recordings.*?</script>\n', '', scripts, flags=re.S)
    # head edits
    head = re.sub(r'<title>.*?</title>', f"<title>{t['title']}</title>", head)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{t["desc"]}">', head)
    head = head.replace('https://protorobot.cz/0/', f'https://protorobot.cz/{"1" if lang=="cs" else "en/1"}/')
    head = head.replace('https://protorobot.cz/en/0/', 'https://protorobot.cz/en/1/')
    head = head.replace('href="https://protorobot.cz/1/"', 'href="https://protorobot.cz/1/"')
    head = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{t["og_title"]}">', head)
    head = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{t["og_desc"]}">', head)
    head = re.sub(r'<meta property="og:image:alt" content=".*?">', f'<meta property="og:image:alt" content="{t["og_alt"]}">', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', ld(t), head, flags=re.S)
    head = head.replace('</style>', EXTRA_CSS, 1)
    # hreflang + canonical fix-ups (alternate cs must stay /1/)
    head = head.replace('<link rel="alternate" hreflang="cs" href="https://protorobot.cz/en/1/">', '<link rel="alternate" hreflang="cs" href="https://protorobot.cz/1/">')
    head = head.replace('<link rel="alternate" hreflang="x-default" href="https://protorobot.cz/en/1/">', '<link rel="alternate" hreflang="x-default" href="https://protorobot.cz/1/">')
    out = head + body(t) + '\n\n\n' + scripts
    dst = root / t['path'] / 'index.html'
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out, encoding='utf-8')
    print('wrote', dst, len(out))
