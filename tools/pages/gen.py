import json, sys, os
ROOT = sys.argv[1]

T = {
 "cs": dict(
  title="Kde stavět v Praze: hackerspacy a dílny | PROTO ROBOT",
  desc="Mapa pražských hackerspaců, makerspaců a otevřených dílen, kde se dá pájet, tisknout a stavět roboty. Kdo tam smí, co tam je a trocha historie.",
  canon="https://protorobot.cz/dilny/", alt="/en/dilny/", altlang="en", altlabel="EN", altname="English",
  skip="Přeskočit na obsah", follow="Sledovat", home="Domů",
  kicker="Komunita PROTO ROBOT", h1a="Kde stavět", h1b="v Praze",
  lede="Hackerspacy, otevřené dílny a laby, kde se dá pájet, tisknout, řezat laserem nebo svařovat. Pro každého, kdo staví roboty a hardware.",
  checked="ověřeno 30. 10. 2026", active="aktivních míst",
  hmap="Mapa", mapnote="Schéma, ne měřítko. Cestu najdete přes odkaz Mapy u každého místa.",
  hlist="Místa", of="z", hlore="Pražská maker scéna v čase",
  web="web", maps="Mapy", src="zdroje",
  acc={"public":"Pro veřejnost","members":"Členové a na přihlášku","students":"Studenti"},
  missing="Chybí tu dílna, nebo něco nesedí? Napište nám přes Lumu nebo LinkedIn.",
  foot="© 2026 PROTO ROBOT. Máme toho hodně. A&nbsp;proto robot.",
  footlinks=[("/","#1"),("/0/","#0"),("/granty/","Granty")], hgrant="Granty",
  districts=["Holešovice","Dejvice","Strahov","Staré Město","Žižkov","Vinohrady","Smíchov","Nusle","Karlín"],
  timeline=[("2010","Vzniká brmlab, první český hackerspace. Začíná v Bubenské 1 v Holešovicích.",""),
   ("2014","Skupina Ztohoven otevírá Paralelní Polis: hackerspace, kavárna jen na bitcoin a Hackers Congress.",""),
   ("2018","Josef Průša otevírá PrusaLab, 350 m² pro veřejnost. Vzniká FutLab a brmlab se stěhuje k němu na chodbu.",""),
   ("2020","Covid zavírá dílny. PrusaLab se mění v prototypové centrum a akcelerátor.","end"),
   ("2021","Z FutLabu se stává umělecká slévárna bronzu.","end"),
   ("2024","Magistrát otevírá HW Lab Praha. NTK přidává svařování s FS ČVUT. Paralelní Polis končí.",""),
   ("2026","brmlab slaví 16. narozeniny. Veřejné dílny fungují v NTK, HW Labu i na Hybernské.","now")]
 ),
 "en": dict(
  title="Where to build in Prague: hackerspaces and workshops | PROTO ROBOT",
  desc="A map of Prague hackerspaces, makerspaces and open workshops where you can solder, 3D print and build robots. Who can use them, what they have, and a bit of history.",
  canon="https://protorobot.cz/en/dilny/", alt="/dilny/", altlang="cs", altlabel="CZ", altname="Česky",
  skip="Skip to content", follow="Follow", home="Home",
  kicker="PROTO ROBOT community", h1a="Where to build", h1b="in Prague",
  lede="Hackerspaces, open workshops and labs where you can solder, 3D print, laser cut or weld. For anyone building robots and hardware.",
  checked="checked 30 Oct 2026", active="active places",
  hmap="Map", mapnote="Schematic, not to scale. Use the Maps link on each place for directions.",
  hlist="Places", of="of", hlore="Prague's maker scene over time",
  web="website", maps="Maps", src="sources",
  acc={"public":"Open to the public","members":"Members or by application","students":"Students"},
  missing="Missing a workshop, or something is off? Message us on Luma or LinkedIn.",
  foot="© 2026 PROTO ROBOT. Máme toho hodně. A&nbsp;proto robot.",
  footlinks=[("/en/","#1"),("/en/0/","#0"),("/en/granty/","Grants")], hgrant="Grants",
  districts=["Holešovice","Dejvice","Strahov","Old Town","Žižkov","Vinohrady","Smíchov","Nusle","Karlín"],
  timeline=[("2010","brmlab opens, the first Czech hackerspace, at Bubenská 1 in Holešovice.",""),
   ("2014","The art group Ztohoven opens Paralelní Polis: a hackerspace, a bitcoin-only café and the Hackers Congress.",""),
   ("2018","Josef Průša opens PrusaLab, 350 m² for the public. FutLab opens and brmlab moves in across its corridor.",""),
   ("2020","Covid closes the workshops. PrusaLab becomes a prototyping centre and accelerator.","end"),
   ("2021","FutLab turns into an art bronze foundry.","end"),
   ("2024","The city opens HW Lab Praha. NTK adds welding with ČVUT. Paralelní Polis closes.",""),
   ("2026","brmlab turns 16. Public workshops run at NTK, HW Lab and Hybernská.","now")]
 )
}

P = [
 dict(n=1,name="brmlab",lat=50.0835,lon=14.4803,acc="members",q="Pod Kapličkou 3155/20, Praha",web="https://brmlab.cz",mail="brmlab@brmlab.cz",
  src=[("mailing list 2026","https://brmlab.cz/mailman3/hyperkitty/list/brmlab@brmlab.cz/latest?count=100"),("Lupa 2018","https://www.lupa.cz/clanky/jako-cukrarna-pro-geeky-a-kutily-v-praze-otevira-komunitni-dilna-futlab/")],
  cs=dict(kind="hackerspace",area="Praha 3, Pod Kapličkou 3155/20",who="Členové, hosté jsou vítáni na přednáškách a akcích. Podle starších zdrojů 500 Kč měsíčně, studenti 250 Kč; aktuální ceny ověřte.",gear=["3D tisk","výroba DPS","elektronika","biolab"],lore="První český hackerspace, otevřený v říjnu 2010 v Bubenské 1. Odtud robot BRMBOT pro soutěž RoboTour, větev RepRapu, kterou komunita přijala jako doporučenou, a dílna s Mitchem Altmanem. V roce 2018 se přestěhoval na Žižkov, v říjnu 2026 slaví 16. narozeniny."),
  en=dict(kind="hackerspace",area="Praha 3, Pod Kapličkou 3155/20",who="Members; guests are welcome at talks and events. Older sources say CZK 500 a month, CZK 250 for students; check current fees.",gear=["3D printing","PCB making","electronics","biolab"],lore="The first Czech hackerspace, opened in October 2010 at Bubenská 1. Home of BRMBOT, built for the RoboTour contest, a RepRap branch the community adopted as recommended, and a workshop with Mitch Altman. Moved to Žižkov in 2018 and turns 16 in October 2026.")),
 dict(n=2,name="Polytechnická dílna NTK",lat=50.1039,lon=14.3905,acc="public",q="Národní technická knihovna, Technická 6, Praha",web="https://www.techlib.cz/cs/84997-polytechnicka-dilna",mail="dilna@techlib.cz",
  src=[("techlib.cz","https://www.techlib.cz/cs/84997-polytechnicka-dilna"),("fablabs.io","https://fablabs.io/labs/ntk3dworkshop")],
  cs=dict(kind="veřejná dílna v knihovně",area="Praha 6, Technická 6, přízemí NTK",who="Registrace v NTK a česká adresa, od 18 let. Online školení a certifikát pro každý stroj, rezervace předem. Zdarma, platí se materiál.",gear=["3D tisk Prusa XL, MK4","laser Epilog","elektronika","dílna dřevo a kov","3D sken","svařování"],lore="Svařování MIG/MAG, TIG a MMA jednou měsíčně v halách FS ČVUT, od roku 2024. Pořádá i opravárenské dny otevřené všem."),
  en=dict(kind="public library workshop",area="Praha 6, Technická 6, NTK ground floor",who="NTK registration and a Czech address, 18+. Online safety course and a certificate per machine, book ahead. Free, you pay for materials.",gear=["Prusa XL, MK4","Epilog laser","electronics","wood and metal shop","3D scanner","welding"],lore="MIG/MAG, TIG and MMA welding once a month in the ČVUT mechanical engineering halls, since 2024. Also runs repair days open to anyone.")),
 dict(n=3,name="HW Lab Praha",lat=50.0629,lon=14.4285,acc="public",q="Kongresové centrum Praha, 5. května 65",web="https://hwlab.praha.eu",mail="hwlab@hwlabpraha.cz",
  src=[("hwlab.praha.eu","https://hwlab.praha.eu/otevrena-dilna")],
  cs=dict(kind="městský makerspace",area="Praha 4, Kongresové centrum, vchod 11",who="Zdarma v otevírací době, platí se materiál. Předem online registrace a QR kód. Do 18 let s podpisem rodiče.",gear=["3D tisk Prusa, Formlabs, Bambu","laser xTool 55 W","pájení a horký vzduch","osciloskop","nářadí","CNC výšivka"],lore="Otevřen v červnu 2024 z iniciativy Magistrátu a místní tech komunity, provozuje DDM Praha 6. Otevřená dílna út až čt 16:30–20:00, ve čtvrtek opravy elektroniky."),
  en=dict(kind="city makerspace",area="Praha 4, Prague Congress Centre, entrance 11",who="Free during opening hours, you pay for materials. Register online first and get a QR code. Under 18 with a parent's signature.",gear=["Prusa, Formlabs, Bambu","xTool 55 W laser","soldering and hot air","oscilloscope","power tools","CNC embroidery"],lore="Opened in June 2024 by Prague City Hall with the local tech community, run by DDM Praha 6. Open workshop Tue to Thu 16:30–20:00, electronics repair on Thursdays.")),
 dict(n=4,name="HYB4 Cirkulární dílna",lat=50.0874,lon=14.4317,acc="public",q="Kampus Hybernská, Hybernská 4, Praha",web="https://kampushybernska.cz/en/cirkularita/cirkularni-dilna-hyb4",mail="dilna@kampushybernska.cz",
  src=[("kampushybernska.cz","https://kampushybernska.cz/en/cirkularita/cirkularni-dilna-hyb4")],
  cs=dict(kind="komunitní dílna",area="Praha 1, Kampus Hybernská",who="Rezervace po hodinách, 150 Kč za osobu a hodinu, po zaškolení. Placené workshopy 650 až 1 800 Kč.",gear=["pájení","vrtačky","pily","frézka","bruska","kompresor"],lore="Dílna cirkulárního programu Univerzity Karlovy v Kampusu Hybernská. Na kovové a dřevěné díly; 3D tisk ani laser tu nejsou."),
  en=dict(kind="community workshop",area="Praha 1, Kampus Hybernská",who="Book by the hour, CZK 150 per person per hour, after training. Paid workshops CZK 650 to 1,800.",gear=["soldering","drills","saws","milling machine","grinder","compressor"],lore="The workshop of Charles University's circularity programme at Kampus Hybernská. Good for metal and wood parts; no 3D printer or laser.")),
 dict(n=5,name="PrusaLab",lat=50.1063,lon=14.4405,acc="members",q="PrusaLab, Partyzánská 188/7a, Praha",web="https://prusalab.cz",mail="info@prusalab.cz",
  src=[("prusalab.cz","https://prusalab.cz/"),("Prusa blog 2022","https://blog.prusa3d.com/redefining-prusalab-from-makerspace-to-a-hi-tech-prototyping-center_67340")],
  cs=dict(kind="prototypové centrum",area="Praha 7, Partyzánská 188/7a",who="Není to veřejná dílna. Kontaktujte lab s projektem; přijetí podle kapacity, funguje spíš jako akcelerátor. Nabízí i 3D tisk na zakázku.",gear=["3D tisk","CNC frézování","laser","výroba DPS","vakuové lití"],lore="Josef Průša ho otevřel 6. 6. 2018 jako 350 m² komunitní dílnu, za dva roky měla kolem sta stálých členů. Za covidu se zavřela veřejnosti a v roce 2020 spustila akcelerátor pro hardwarové startupy. Pořádá Prague Hardware Meetup."),
  en=dict(kind="prototyping centre",area="Praha 7, Partyzánská 188/7a",who="Not a public workshop. Contact the lab with a project; acceptance depends on capacity and works more like an accelerator. Also offers 3D printing on demand.",gear=["3D printing","CNC milling","laser","PCB making","vacuum casting"],lore="Josef Průša opened it on 6 June 2018 as a 350 m² community workshop with about a hundred regular members in two years. It closed to the public during Covid and launched a hardware startup accelerator in 2020. Hosts the Prague Hardware Meetup.")),
 dict(n=6,name="TAKT Praha",lat=50.0868,lon=14.4635,acc="members",q="Jeseniova 212, Praha",web="https://wiki.taktpraha.cz",mail="info@taktpraha.cz",
  src=[("wiki.taktpraha.cz","https://wiki.taktpraha.cz/")],
  cs=dict(kind="hackerspace",area="Žižkov, Jeseniova 212",who="Členové s přístupem 24/7. Poslední doložená akce je z března 2024, aktivitu před návštěvou ověřte.",gear=["3D tisk","elektronika"],lore="Spolek Takt z.s., kolem roku 2020 popisovaný jako nový hackerspace. Na wiki uvádí čtvrteční lekce elektroniky."),
  en=dict(kind="hackerspace",area="Žižkov, Jeseniova 212",who="Members with 24/7 access. The last documented event is from March 2024; check it is active before you go.",gear=["3D printing","electronics"],lore="Run by Takt z.s., described around 2020 as a new hackerspace. Its wiki lists Thursday electronics lessons.")),
 dict(n=7,name="MacGyver, bastlíři Silicon Hill",lat=50.0810,lon=14.3920,acc="students",q="Koleje Strahov blok 9, Praha",web="https://www.siliconhill.cz",mail="",
  src=[("Silicon Hill 2024","https://zapisy.sh.cvut.cz/prilohy/20250227-Vyrocni-zprava-SH-2024.pdf")],
  cs=dict(kind="studentský klub ČVUT",area="Praha 6, koleje Strahov, blok 9",who="Jen členové klubu Silicon Hill, tedy hlavně studenti ČVUT na Strahově. V semestru 4 večery v týdnu bez rezervace.",gear=["pájecí stanice","ultrazvuková čistička","pila na DPS","ruční nářadí"],lore="Elektronická místnost má přezdívku Mučírna, mechanická Mechadílna. Klub vede výroční zprávy už od roku 2009."),
  en=dict(kind="ČVUT student club",area="Praha 6, Strahov dorms, block 9",who="Silicon Hill club members only, mostly ČVUT students living at Strahov. Four evenings a week in term, no booking.",gear=["soldering stations","ultrasonic cleaner","PCB saw","hand tools"],lore="The electronics room is nicknamed Mučírna (torture room), the mechanical one Mechadílna. The club has kept annual reports since 2009.")),
 dict(n=8,name="HWLab FIT ČVUT",lat=50.1052,lon=14.3935,acc="students",q="Thákurova 7, Praha",web="https://fit.cvut.cz/en/science-and-research/facilities/laboratories/12218-hardware-workshop-and-laboratory-hwlab",mail="",
  src=[("fit.cvut.cz","https://fit.cvut.cz/en/science-and-research/facilities/laboratories/12218-hardware-workshop-and-laboratory-hwlab")],
  cs=dict(kind="univerzitní laboratoř",area="Praha 6, Thákurova 7, budova A, 10. patro",who="Zaměstnanci a studenti FIT a výzkumné laby. Veřejnosti nepřístupná.",gear=["osciloskopy","logické analyzátory","FPGA","mikropájení","leptání DPS"],lore="Hardwarová dílna Fakulty informačních technologií pro studentské projekty a výzkum."),
  en=dict(kind="university lab",area="Praha 6, Thákurova 7, building A, 10th floor",who="FIT staff and students and research labs. Not open to the public.",gear=["oscilloscopes","logic analysers","FPGA","micro soldering","PCB etching"],lore="The hardware workshop of the Faculty of Information Technology, for student projects and research.")),
 dict(n=9,name="Maker Institute",lat=None,lon=None,acc="public",q="",web="https://makerinstitute.cz",mail="info@makerinstitute.cz",
  src=[("makerinstitute.cz","https://makerinstitute.cz/")],
  cs=dict(kind="vzdělávací makerspace",area="Dejvice, adresa labu neuvedena",who="Placené workshopy, např. 500 až 700 Kč za 2 hodiny. Semestrální inkubátor Make-iton pro studenty.",gear=["workshopy"],lore="Dřív provozoval fablaby na dejvickém kampusu. S FEL ČVUT vede od roku 2023 předmět Jak vyrobit (téměř) cokoli."),
  en=dict(kind="education makerspace",area="Dejvice, lab address not published",who="Paid workshops, e.g. CZK 500 to 700 for 2 hours. Make-iton, a one-semester incubator for students.",gear=["workshops"],lore="Used to run fablabs on the Dejvice campus. Since 2023 it co-teaches the FEL ČVUT course How to Make (Almost) Anything.")),
]

TPL = open(os.path.join(os.path.dirname(__file__), "tpl.html"), encoding="utf-8").read()
for lang, t in T.items():
    data = [dict(n=p["n"], name=p["name"], lat=p["lat"], lon=p["lon"], acc=p["acc"], q=p["q"], web=p["web"], mail=p["mail"], src=p["src"], **p[lang]) for p in P]
    html = TPL
    rep = {k: v for k, v in t.items() if isinstance(v, str)}
    rep["lang"] = lang
    rep["datajson"] = json.dumps(dict(places=data, acc=t["acc"], districts=t["districts"], web=t["web"], maps=t["maps"], src=t["src"], of=t["of"]), ensure_ascii=False)
    rep["timeline"] = "".join(f'<div class="ev {c}"><b>{y}</b><span>{s}</span></div>' for y, s, c in t["timeline"])
    rep["footlinks"] = "".join(f'<a href="{h}">{l}</a>' for h, l in t["footlinks"])
    rep["homehref"] = "/" if lang == "cs" else "/en/"
    for k, v in rep.items():
        html = html.replace("{{" + k + "}}", v)
    assert "{{" not in html, html[html.index("{{"):html.index("{{")+40]
    out = os.path.join(ROOT, "dilny" if lang == "cs" else "en/dilny", "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out)
