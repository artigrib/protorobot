#!/usr/bin/env python3
"""One-off transform of /0/ and /en/0/: programme and speaker sections fold into the recordings block.
Each talk is one card (uncropped speaker photo as poster, play, duration, name, company, title, note).
Run once from repo root: python3 tools/pages/redesign_0.py .
"""
import re, sys, pathlib

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
DUR = {'01-konecny-robot-issues': '16:54', '02-vitek-humanoids': '36:35', '03-danieau-reachy-mini': '21:54', '04-bruna-kord': '20:02'}
IDS = list(DUR)

L = {
 'cs': dict(page='0', nav='<a class="pill" href="#recordings">Záznamy</a>\n      <a class="pill" href="#photos">Fotky</a>\n      <a class="pill" href="/">#1</a>',
            facts_old=['<a href="#programme">Program</a>', '<a href="#recordings">Přednášky</a>'], facts_new='<a href="#recordings">Záznamy</a>',
            play='Přehrát', lede='Čtyři přednášky z PROTO ROBOT #0 v pořadí, jak zazněly. Kapitoly vedou rovnou na dané místo.',
            foot_old='<a href="#photos">Fotky</a>', foot_new='<a href="#recordings">Záznamy</a>\n  <a href="#photos">Fotky</a>'),
 'en': dict(page='en/0', nav='<a class="pill" href="#recordings">Recordings</a>\n      <a class="pill" href="#photos">Photos</a>\n      <a class="pill" href="/en/">#1</a>',
            facts_old=['<a href="#programme">Program</a>', '<a href="#recordings">Talks</a>'], facts_new='<a href="#recordings">Recordings</a>',
            play='Play', lede='The four talks from PROTO ROBOT #0 in the order they were given. Chapters jump straight to the spot.',
            foot_old='<a href="#photos">Photos</a>', foot_new='<a href="#recordings">Recordings</a>\n  <a href="#photos">Photos</a>'),
}

CSS = '''
/* ---------- recordings: one card per talk, the card is the speaker ---------- */
.rec-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--s3) var(--g);margin-top:var(--s3)}
@media (max-width:1000px){.rec-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.rec-grid{grid-template-columns:minmax(0,1fr);gap:var(--s3)}}
.rec.is-on{display:none}
.vp__now a{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.12em;text-decoration-color:transparent}.vp__now a:hover,.vp__now a:focus-visible{text-decoration-color:currentColor}
.vp__note{font-size:15px;line-height:1.35;margin:6px 0 var(--s2)}
.rec{display:grid;align-content:start}
.rec__play{all:unset;box-sizing:border-box;display:block;width:100%;cursor:pointer}
.rec__play:focus-visible .photo{outline:3px solid var(--black);outline-offset:3px}
.rec .photo{display:block;aspect-ratio:16/9}
.rec .photo img{transition:opacity .65s var(--ease-out),transform .9s var(--ease-out)}
.rec:hover .photo img{transform:scale(1.03)}
.rec__ico{position:absolute;z-index:3;left:50%;top:50%;width:64px;height:64px;margin:-32px 0 0 -32px;border-radius:50%;background:var(--white);display:grid;place-items:center;transition:transform .25s var(--ease-out),background .2s}
.rec__ico svg{width:26px;height:26px;fill:var(--black);margin-left:3px}
.rec:hover .rec__ico{transform:scale(1.08);background:var(--orange)}
.rec__dur{position:absolute;z-index:3;right:var(--s1);bottom:var(--s1);background:var(--black);color:var(--white);font:600 13px/1 var(--font);padding:7px 9px;letter-spacing:.02em}
.rec .spk__name{margin-top:var(--s2)}
@media (max-width:640px){.rec .spk__name{font-size:26px}.rec__ico{width:48px;height:48px;margin:-24px 0 0 -24px}.rec__ico svg{width:20px;height:20px}.rec__dur{right:6px;bottom:6px}}
</style>'''

PLAY_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'

for lang, t in L.items():
    p = root / t['page'] / 'index.html'
    s = p.read_text(encoding='utf-8')

    # A. nav
    s = re.sub(r'(<div class="city__nav" id="cityNav">\n)(?:\s*<a class="pill"[^\n]*\n)+', r'\1      ' + t['nav'] + '\n', s)
    # B. intro facts
    for old in t['facts_old']:
        s = s.replace(old, '')
    s = s.replace('<p class="facts">', '<p class="facts">' + t['facts_new'], 1)
    # C. pull speaker articles out, then drop programme, speakers, next sections
    arts = re.findall(r'<article class="spk">.*?</article>', s, flags=re.S)
    assert len(arts) == 4, len(arts)
    for sid in ('programme', 'speakers', 'next'):
        s = re.sub(r'<section class="mod[^"]*" id="%s">.*?</section>\n\n' % sid, '', s, flags=re.S)
    # D. cards from the articles
    cards = []
    for i, (a, vid) in enumerate(zip(arts, IDS)):
        name = re.search(r'aria-label="([^",]+),', a).group(1)
        rest = re.sub(r'<div class="photo">.*?</div>\n', '', a, count=1, flags=re.S)
        rest = rest.replace('<article class="spk">', '').replace('</article>', '').strip('\n')
        photo = (f'      <button class="rec__play" type="button" aria-label="{t["play"]}: {name}"><span class="photo">'
                 f'<img src="/img/0/vp-{vid}.webp" alt="" width="1600" height="900" decoding="async">'
                 f'<span class="rec__ico" aria-hidden="true">{PLAY_SVG}</span><span class="rec__dur">{DUR[vid]}</span></span></button>')
        cards.append(f'    <article class="rec" data-i="{i}" id="rec-{vid}">\n{photo}\n{rest}\n    </article>')
    grid = '  <div class="rec-grid" id="recGrid">\n' + '\n'.join(cards) + '\n  </div>'
    s = re.sub(r'  <h3 class="vp__label vp__label--list">[^<]*</h3>\n  <ol class="vp__list"></ol>', grid, s)
    s = re.sub(r'(<section class="mod rec" id="recordings">\n  <h2>[^<]*</h2>\n  <p class="lede">)[^<]*(</p>)', r'\g<1>' + t['lede'] + r'\2', s)
    # E. CSS
    s = s.replace('</style>', CSS, 1)
    # F. player JS: cards instead of the generated list, local poster
    s = re.sub(r"  const ulC = q\('\.vp__chapters'\), ulL = document\.querySelector\('\.vp__list'\);",
               "  const ulC = q('.vp__chapters'), cards = [...document.querySelectorAll('#recGrid .rec')];", s)
    s = re.sub(r"  list\.forEach\(\(l, i\) => \{\n.*?\n  \}\);\n\n  function load", '''  cards.forEach((c, i) => {
    c.querySelector('.rec__play').addEventListener('click', () => { load(i, 0, true); root.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
  });

  function load''', s, flags=re.S)
    s = s.replace("v.poster = `${base}${l.id}.jpg`;", "v.poster = `/img/0/vp-${l.id}.webp`;")
    s = s.replace("q('.vp__spk').textContent = `${l.speaker} · ${l.org}`; q('.vp__ttl').textContent = l.title;",
                  "const card = cards[i], li = card && card.querySelector('.spk__name a'); q('.vp__spk').innerHTML = ''; if (li) { const a = document.createElement('a'); a.href = li.href; a.target = '_blank'; a.rel = 'noopener'; a.textContent = l.speaker; q('.vp__spk').append(a, ` · ${l.org}`); } else q('.vp__spk').textContent = `${l.speaker} · ${l.org}`; q('.vp__ttl').textContent = l.title; const nt = card && card.querySelector('.spk__note'); q('.vp__note').textContent = nt ? nt.textContent : '';")
    s = s.replace('<p class="vp__now"><b class="vp__spk"></b><span class="vp__ttl"></span></p>', '<p class="vp__now"><b class="vp__spk"></b><span class="vp__ttl"></span></p>\n      <p class="vp__note"></p>')
    s = s.replace("[...ulL.children].forEach((li, k) => li.classList.toggle('is-on', k === i));", "cards.forEach((c, k) => c.classList.toggle('is-on', k === i));")
    # G. footer
    s = re.sub(r'(<footer class="foot">\n  <a href="[^"]*">#1</a>\n  )' + re.escape(t['foot_old']), lambda m: m.group(1) + t['foot_new'], s, count=1)
    assert 'ulL' not in s and '#programme' not in s and 'id="speakers"' not in s
    p.write_text(s, encoding='utf-8')
    print('ok', p, len(s))
