import re,sys,html as H
lang,path=sys.argv[1],sys.argv[2]
s=open(path,encoding='utf-8').read()
oldcss=open('/workspace/build/player.css').read()
assert oldcss in s; s=s.replace(oldcss,'')
s,n=re.subn(r'<script>\n/\* Lecture recordings\..*?\n</script>\n','',s,flags=re.S); assert n==1
s,n=re.subn(r'<section class="mod rec" id="recordings">.*?</section>\n','',s,flags=re.S); assert n==1
s,n=re.subn(r'<section class="mod speakers" id="speakers">.*?</section>\n','',s,flags=re.S); assert n==1
EN_CH={"Úvod":"Intro","Největší problém: realita provozu":"The biggest problem: real-world operation","Lidé, kteří roboty obsluhují":"The people who operate robots","Extrémní případy":"Extreme cases","Prosba konstruktérům: přístup k dílům":"A plea to designers: access to parts","Dotazy z publika":"Audience Q&A","Dotaz: autonomie a centrální řízení":"Q: autonomy and central control","Dotaz: nasazení venku":"Q: outdoor deployment","Dotaz: robot umytý hadicí":"Q: a robot hosed down with water","Dotaz: krádeže a vandalismus":"Q: theft and vandalism","Dotaz: záruční a pozáruční servis":"Q: warranty and post-warranty service",
"Úvod: Integra Robotics":"Intro: Integra Robotics","Jak dnes fungují průmyslové roboty":"How industrial robots work today","Co je physical AI":"What is physical AI","VLA modely (vision-language-action)":"VLA models (vision-language-action)","Data: největší boj":"Data: the biggest struggle","Imitation learning v praxi":"Imitation learning in practice","Slabiny: generalizace, kontakt, zotavení":"Weak spots: generalization, contact, recovery","Spolehlivost: 99 % nestačí":"Reliability: 99% is not enough","Humanoidi v továrnách už dnes":"Humanoids in factories today","Hybridní řízení v Integra Robotics":"Hybrid control at Integra Robotics","Proč (ne)chodící robot?":"Why a (non-)walking robot?","Typické případy použití":"Typical use cases","Budoucnost: adaptace, ne tanec":"The future: adaptation, not dancing",
"Úvod: KORD a tři lekce":"Intro: KORD and three lessons","Robotický manipulátor od kontroleru po teach pendant":"A robot arm from controller to teach pendant","Zákazník chce rameno řídit napřímo":"The customer wants direct control of the arm","ROS, nebo vlastní řešení?":"ROS or a custom solution?","Open source a příliš široké API":"Open source and an overly broad API","„Ono to nefunguje“: první nasazení":"“It doesn't work”: the first deployment","Dokumentace a příklady":"Documentation and examples","Testování a CI":"Testing and CI","Zapisujte technická rozhodnutí":"Write down technical decisions","Zastavit se a splácet technický dluh":"Stop and pay down technical debt","Ptejte se na druhý názor":"Ask for a second opinion","Dotaz: real-time řízení a frekvence":"Q: real-time control and frequency","Dotaz: ROS, nebo vlastní protokol?":"Q: ROS or a custom protocol?"}
def ch(f):
    o=[]
    for l in open(f,encoding='utf-8'):
        l=l.strip()
        if l: t,nm=l.split(' ',1); m,sec=t.split(':'); nm=nm if lang=='cs' else EN_CH.get(nm,nm); o.append((int(m)*60+int(sec),t,nm))
    return o
def desc(f,first_is_cs):
    p=[x.strip() for x in open(f,encoding='utf-8').read().split('\n\n')]
    cs,en=(p[0],p[1]) if first_is_cs else (p[1],p[0])
    return cs if lang=='cs' else en
T='/workspace/src/txt/'
CS=lang=='cs'
talks=[
 dict(id='01-konecny-robot-issues',time='19:05',speaker='Tomáš Konečný',li='https://www.linkedin.com/in/tom%C3%A1%C5%A1-kone%C4%8Dn%C3%BD-360a63164/',photo='sp-konecny',
      org='Robotservice',title='Běžné problémy servisních robotů' if CS else 'Common facility robot issues',demo=False,ready=True,ch=ch(T+'a_chapters.txt'),d=desc(T+'a_description.md',1),lng='CZ'),
 dict(id='02-vitek-humanoids',time='19:15',speaker='Lukáš Vítek',li='https://www.linkedin.com/in/vitek-lukas/',photo='sp-vitek',
      org='Integra Robotics',title='Physical AI a humanoidi v průmyslu' if CS else 'Physical AI and humanoids in industry',demo=True,ready=True,ch=ch(T+'b_chapters.txt'),d=desc(T+'b_description.md',1),lng='CZ'),
 dict(id='03-danieau-reachy-mini',time='20:30',speaker='Fabien Danieau',li='https://www.linkedin.com/in/fabiendanieau/',photo='sp-danieau',
      org='Pollen Robotics / Hugging Face',title='Reachy Mini: open-source stolní robot' if CS else 'Reachy Mini: open-source desk robot',demo=True,ready=True,ch=ch(T+'d_chapters.txt'),d=desc(T+'d_description.md',0),lng='EN'),
 dict(id='04-bruna-kord',time='20:50',speaker='Ondřej Bruna',li='https://www.linkedin.com/in/ond%C5%99ej-bruna-1500a043/',photo='sp-bruna',
      org='Spoluautor a vývojář KORDu' if CS else 'Co-author and developer of KORD',title='KORD: Lessons Learned',demo=False,ready=True,ch=ch(T+'c_chapters.txt'),d=desc(T+'c_description.md',1),lng='CZ'),
]
S=dict(h='Přednášky',lede='Čtyři přednášky z 23. října, s&nbsp;videem a&nbsp;kapitolami.',play='Přehrát',pause='Pauza',mute='Ztlumit',fs='Celá obrazovka',speed='Rychlost',seek='Posun ve videu',chap='Kapitoly',soon='Video brzy',demo='Živé demo',li='LinkedIn',lang='Jazyk',vol='Hlasitost') if CS else \
  dict(h='Talks',lede='Four talks from 23 October. Each with video and chapters.',play='Play',pause='Pause',mute='Mute',fs='Fullscreen',speed='Speed',seek='Seek',chap='Chapters',soon='Video soon',demo='Live demo',li='LinkedIn',lang='Language',vol='Volume')
e=H.escape
arts=[]
for i,t in enumerate(talks,1):
    chs=''.join(f'<li><button type="button" data-t="{a}"><time>{b}</time><span>{e(c)}</span></button></li>' for a,b,c in t['ch'])
    meta=[t['time'],t['lng']]+([S['demo']] if t['demo'] else [])
    if t['ready']:
        media=f'<button class="talk__poster" type="button" data-play aria-label="{S["play"]}: {e(t["title"])}"><img loading="lazy" decoding="async" src="" data-src="{t["id"]}.webp" alt="" width="1280" height="720"><span class="talk__go pill pill--orange">{S["play"]}</span></button>'
    else:
        media=f'<div class="talk__poster is-soon"><img loading="lazy" decoding="async" src="/img/0/{t["photo"]}.webp" alt="{e(t["speaker"])}"><span class="talk__soon">{S["soon"]}</span></div>'
    arts.append(f'''    <article class="talk{' is-ready' if t['ready'] else ''}" id="{t['id']}" data-id="{t['id']}">
      <p class="talk__n">{i:02d}</p>
      <div class="talk__text">
        <p class="talk__meta">{' · '.join(meta)}</p>
        <h3 class="talk__title">{e(t['title'])}</h3>
        <div class="talk__who">
          <img class="talk__face" loading="lazy" decoding="async" src="/img/0/{t['photo']}.webp" alt="" width="64" height="64">
          <p><a href="{t['li']}" target="_blank" rel="noopener">{t['speaker']}</a><span>{e(t['org'])}</span></p>
        </div>
        <p class="talk__desc">{e(t['d'])}</p>
      </div>
      <div class="talk__media">{media}</div>
      <div class="talk__ch"><p class="talk__label">{S['chap']}</p><ol class="talk__chapters">{chs}</ol></div>
    </article>''')
sec=f'''<section class="mod talks" id="talks">
  <h2>{S['h']}</h2>
  <p class="lede">{S['lede']}</p>
  <div class="talk-list">
{chr(10).join(arts)}
  </div>
  <template id="vp-tpl">
    <div class="vp">
      <video class="vp__video" playsinline preload="metadata"></video>
      <div class="vp__bar">
        <button class="vp__btn vp__play" type="button" aria-label="{S['play']}"><svg viewBox="0 0 24 24" aria-hidden="true"><path class="i-play" d="M8 5v14l11-7z"/><path class="i-pause" d="M7 5h4v14H7zm6 0h4v14h-4z"/></svg></button>
        <input class="vp__seek" type="range" min="0" max="1000" value="0" step="1" aria-label="{S['seek']}">
        <span class="vp__time">0:00 / 0:00</span>
        <button class="vp__btn vp__mute" type="button" aria-label="{S['mute']}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9z"/><path class="i-vol" d="M16 8.5a5 5 0 0 1 0 7"/><path class="i-x" d="M16 9l5 6m0-6l-5 6"/></svg></button>
        <input class="vp__vol" type="range" min="0" max="1" step="0.05" value="1" aria-label="{S['vol']}">
        <button class="vp__btn vp__speed" type="button" aria-label="{S['speed']}">1×</button>
        <button class="vp__btn vp__fs" type="button" aria-label="{S['fs']}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5"/></svg></button>
      </div>
    </div>
  </template>
</section>
'''
anchor='<section class="mod" id="photos">'
assert anchor in s; s=s.replace(anchor,sec+'\n'+anchor,1)
s=s.replace('href="#speakers"','href="#talks"')
FT=('<a href="#photos">Fotky</a>','<a href="#photos">Fotky</a><a href="#talks">Přednášky</a>') if CS else ('<a href="#photos">Photos</a>','<a href="#photos">Photos</a><a href="#talks">Talks</a>')
assert '<p class="facts">' in s and FT[0] in s
s=s.replace('<p class="facts"><a href="#programme">Program</a>'+FT[0],'<p class="facts"><a href="#programme">Program</a>'+FT[1],1)
s=s.replace('</style>',open('/workspace/build/swiss.css').read()+'</style>',1)
js=open('/workspace/build/talks.js').read()
cfg='<script>\n/* Talk videos. MEDIA_BASE: R2 bucket protorobot (r2.dev); switch to a custom domain here. Files: <base><id>.mp4 / .jpg / .webp */\nwindow.PR_MEDIA_BASE = "https://pub-afcf63b01ca7486c8bda7f2ff617f31e.r2.dev/0/";\nwindow.PR_I18N = {"play":"%s","pause":"%s"};\n'%(S['play'],S['pause'])+js+'</script>\n'
s=s.replace('</body>',cfg+'</body>',1)
open(path,'w',encoding='utf-8').write(s)
