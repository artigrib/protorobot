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
  footlinks=[("/","Domů"),("/1/","#1"),("/0/","#0"),("/granty/","Granty")], hgrant="Granty",
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
  footlinks=[("/en/","Home"),("/en/1/","#1"),("/en/0/","#0"),("/en/granty/","Grants")], hgrant="Grants",
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

P_PRAHA = [
 dict(n=1,name="brmlab",lat=50.0835,lon=14.4803,acc="members",q="Pod Kapličkou 3155/20, Praha",web="https://brmlab.cz",mail="brmlab@brmlab.cz",
  src=[("mailing list 2026","https://brmlab.cz/mailman3/hyperkitty/list/brmlab@brmlab.cz/latest?count=100"),("Lupa 2018","https://www.lupa.cz/clanky/jako-cukrarna-pro-geeky-a-kutily-v-praze-otevira-komunitni-dilna-futlab/")],
  cs=dict(kind="hackerspace",area="Praha 3, Pod Kapličkou 3155/20",who="Členství 1 000 Kč měsíčně, studenti 250 Kč. Hosté jsou vítáni na přednáškách a akcích.",gear=["3D tisk","výroba DPS","elektronika","biolab"],lore="První český hackerspace, otevřený v říjnu 2010 v Bubenské 1. Odtud robot BRMBOT pro soutěž RoboTour, větev RepRapu, kterou komunita přijala jako doporučenou, a dílna s Mitchem Altmanem. V roce 2018 se přestěhoval na Žižkov, v říjnu 2026 slaví 16. narozeniny."),
  en=dict(kind="hackerspace",area="Praha 3, Pod Kapličkou 3155/20",who="Membership CZK 1,000 a month, students CZK 250. Guests are welcome at talks and events.",gear=["3D printing","PCB making","electronics","biolab"],lore="The first Czech hackerspace, opened in October 2010 at Bubenská 1. Home of BRMBOT, built for the RoboTour contest, a RepRap branch the community adopted as recommended, and a workshop with Mitch Altman. Moved to Žižkov in 2018 and turns 16 in October 2026.")),
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

P_BRNO = [
 dict(n=1,name="FabLab Brno",lat=49.2298,lon=16.5718,acc="members",q="Purkyňova 649/127, Brno",web="https://www.fablabbrno.cz",mail="",
  src=[("fablabs.io","https://fablabs.io/labs/fablabbrno"),("Lupa 2017","https://www.lupa.cz/clanky/3d-tiskarny-i-laserova-rezacka-v-brne-otevrela-komunitni-digitalni-dilna-fablab/"),("Objev Brno 4/2026","https://www.objevbrno.cz/cs/article/kutilem-v-brne-objevte-mista-kde-vam-pujci-3-d-tiskarnu-truhlarske-stroje-i-sitotisk")],
  cs=dict(kind="otevřená digitální dílna (JIC)",area="Královo Pole, Technologický park, Purkyňova 649/127",who="Pro každého po založení účtu ve FabShopu a vstupním školení na každý stroj. Členství od 149 Kč měsíčně (2017), aktuální ceník na webu. Materiál se platí zvlášť.",gear=["3D tisk","laser","CNC frézka","řezací plotr","elektronika a IoT","mechanická dílna"],lore="Otevřel v dubnu 2017 v Jihomoravském inovačním centru, 182 m², stroje za 3 mil. Kč z kraje a od Honeywellu. První a největší veřejný FabLab na Moravě; z něj vyjela i pojízdná dílna FabLab Experience."),
  en=dict(kind="open digital workshop (JIC)",area="Královo Pole, Technology Park, Purkyňova 649/127",who="Open to anyone after creating a FabShop account and an intro training per machine. Membership from CZK 149 a month (2017), current prices on the website. Materials paid separately.",gear=["3D printing","laser","CNC mill","vinyl cutter","electronics and IoT","mechanical workshop"],lore="Opened in April 2017 at the South Moravian Innovation Centre, 182 m², CZK 3M of machines funded by the region and Honeywell. The first and largest public FabLab in Moravia; the FabLab Experience mobile lab grew out of it.")),
 dict(n=2,name="base48",lat=49.2227,lon=16.5938,acc="members",q="Palackého třída 742/82, Brno",web="https://base48.cz",mail="",
  src=[("base48.cz","https://base48.cz/index_eng.html")],
  cs=dict(kind="hackerspace",area="Královo Pole, dvůr Palackého třída 742/82, vchod i z Mojmírova nám. 17",who="Členství 1 000 Kč měsíčně, studenti 600 Kč. Veřejnost může přijít prakticky bez omezení, nejlépe s členem; otevřeno ukazuje heatmapa na webu.",gear=["farma 3D tiskáren","elektrolab s osciloskopy","CNC","svařování","dřevodílna","cyklodílna","autodílna se zvedákem"],lore="Druhý nejstarší český hackerspace, spolek zapsaný 6. 8. 2010. Začínal na adrese s číslem 48, odtud jméno. Dnes dvůr v Králově Poli s garáží a dílnou."),
  en=dict(kind="hackerspace",area="Královo Pole, courtyard at Palackého třída 742/82, also from Mojmírovo nám. 17",who="Membership CZK 1,000 a month, students CZK 600. The public can drop in with virtually no restrictions, ideally with a member; the website heatmap shows when it is open.",gear=["3D printer farm","electro lab with oscilloscopes","CNC","welding","wood shop","bike shop","car workshop with a lift"],lore="The second oldest Czech hackerspace, registered on 6 Aug 2010. It started at an address with the number 48, hence the name. Today a courtyard in Královo Pole with a garage and a workshop.")),
 dict(n=3,name="Makerspace KJM, IN-centrum",lat=49.1951,lon=16.6085,acc="public",q="náměstí Svobody 15, Brno",web="https://www.kjm.cz/pobocky/in-centrum",mail="incentrum@kjm.cz",
  src=[("kjm.cz","https://www.kjm.cz/pobocky/in-centrum"),("Brno Love 11/2026","https://www.brnolove.cz/makerspace-kjm-brno-poprve/")],
  cs=dict(kind="veřejný makerspace v knihovně",area="střed, náměstí Svobody 15, 2. patro Kleinova paláce",who="Zdarma pro všechny, platí se jen tisk: 30 Kč plus 7 Kč za 10 g. 3D tisk pondělí, úterý a čtvrtek 15 až 18, rezervace online, telefonem nebo e-mailem.",gear=["Prusa MK3S+ a MK4S","VR Meta Quest 2","roboti Ozobot","kurzy digitálních dovedností"],lore="Pobočka Knihovny Jiřího Mahena pro digitální dovednosti. Bez pevné otevírací doby, žije kurzy a rezervacemi. Nejnižší práh vstupu v Brně: stačí přijít."),
  en=dict(kind="public library makerspace",area="centre, náměstí Svobody 15, 2nd floor of Klein Palace",who="Free for everyone, you pay only for printing: CZK 30 plus CZK 7 per 10 g. 3D printing Monday, Tuesday and Thursday 15:00 to 18:00, book online, by phone or e-mail.",gear=["Prusa MK3S+ and MK4S","VR Meta Quest 2","Ozobot robots","digital skills courses"],lore="The Jiří Mahen Library's branch for digital skills. No fixed opening hours, it runs on courses and bookings. The lowest entry barrier in Brno: just come.")),
 dict(n=4,name="strojLAB, FSI VUT",lat=49.2262,lon=16.5755,acc="students",q="Technická 2896/2, Brno",web="https://www.fme.vutbr.cz",mail="david.skaroupka@vut.cz",
  src=[("Interreg DiSTT 2/2026","https://www.interreg-central.eu/?p=41904"),("Prototyp Brno","https://www.prototypbrno.cz/portfolio/strojlab/")],
  cs=dict(kind="univerzitní FabLab",area="Královo Pole, hlavní budova FSI, Technická 2896/2",who="Studenti a zaměstnanci VUT po vstupním školení. Veřejnosti není určen, kontakt přes vedoucího David Škaroupka.",gear=["3D tisk","pájení","prototypování","aditivní technologie"],lore="První univerzitní FabLab v Česku, studentům slouží skoro deset let. V únoru 2026 otevřel nový prostor v hlavní budově FSI při akci strojLAB DAY, s projektem DiSTT k digitálním dovednostem."),
  en=dict(kind="university FabLab",area="Královo Pole, FME main building, Technická 2896/2",who="VUT students and staff after an entry training. Not meant for the public; contact via the lead David Škaroupka.",gear=["3D printing","soldering","prototyping","additive technologies"],lore="The first university FabLab in Czechia, serving students for almost ten years. In February 2026 it opened a new space in the FME main building at strojLAB DAY, together with the DiSTT digital skills project.")),
 dict(n=5,name="Hobbylab",lat=None,lon=None,acc="members",q="Hobbylab, Rousínov",web="https://hobbylab.cz",mail="veronika@hobbylab.cz",
  src=[("hobbylab.cz","https://hobbylab.cz/"),("Objev Brno 4/2026","https://www.objevbrno.cz/cs/article/kutilem-v-brne-objevte-mista-kde-vam-pujci-3-d-tiskarnu-truhlarske-stroje-i-sitotisk")],
  cs=dict(kind="řemeslná dílna",area="Rousínov, 25 km od Brna, adresa na webu",who="Pro každého s vlastním projektem, po zaškolení a s členstvím. Čtvrtek až neděle 10 až 18. Spotřební materiál koupíte na místě, hlavní materiál si vezete.",gear=["truhlárna","zámečnická dílna","kovárna","formátovací pila","pásová pila","srovnávačka"],lore="Spolek z roku 2016, od 2019 v Rousínově. Přes 300 m² strojů na dřevo a kov s lektory po ruce. Pro roboty spíš rámy a konstrukce než elektronika."),
  en=dict(kind="craft workshop",area="Rousínov, 25 km from Brno, address on the website",who="For anyone with their own project, after training and with membership. Thursday to Sunday 10:00 to 18:00. Consumables sold on site, bring your main material.",gear=["wood shop","metal shop","forge","panel saw","bandsaw","jointer-planer"],lore="A non-profit from 2016, in Rousínov since 2019. Over 300 m² of wood and metal machines with instructors at hand. For robots think frames and structures rather than electronics.")),
]

PRAHA_GEO = dict(box=dict(lon0=14.372,lon1=14.498,lat0=50.054,lat1=50.122),
  rivers=[dict(name="VLTAVA",lat=50.0745,lon=14.4065,rot=-80,pts=[[50.054,14.4165],[50.060,14.4160],[50.0665,14.4165],[50.0725,14.4135],[50.0790,14.4120],[50.0865,14.4115],[50.0910,14.4140],[50.0935,14.4200],[50.0948,14.4290],[50.0968,14.4375],[50.1010,14.4480],[50.1045,14.4605],[50.1090,14.4610],[50.1110,14.4520],[50.1135,14.4380],[50.1140,14.4240],[50.1125,14.4080],[50.1150,14.3960],[50.1220,14.3920]])],
  dpos=[[50.1055,14.4300],[50.0985,14.3870],[50.0775,14.3880],[50.0905,14.4240],[50.0800,14.4600],[50.0725,14.4470],[50.0670,14.3990],[50.0590,14.4420],[50.0960,14.4600]])
BRNO_GEO = dict(box=dict(lon0=16.540,lon1=16.650,lat0=49.170,lat1=49.245),
  rivers=[dict(name="SVRATKA",lat=49.1880,lon=16.5870,rot=-55,pts=[[49.245,16.548],[49.236,16.552],[49.228,16.552],[49.219,16.558],[49.211,16.566],[49.204,16.572],[49.197,16.578],[49.191,16.585],[49.184,16.594],[49.178,16.604],[49.172,16.615],[49.170,16.625]]),
          dict(name="SVITAVA",lat=49.2160,lon=16.6285,rot=-85,pts=[[49.245,16.622],[49.236,16.626],[49.227,16.629],[49.218,16.629],[49.209,16.631],[49.200,16.632],[49.191,16.634],[49.182,16.636],[49.172,16.636]])],
  dpos=[[49.2320,16.5870],[49.2130,16.5690],[49.2040,16.5990],[49.2040,16.6180],[49.1870,16.6060],[49.2230,16.6130],[49.1950,16.5760],[49.2350,16.5640]])
CITIES = {
 "praha": dict(P=P_PRAHA, geo=PRAHA_GEO, dir="dilny", other="brno",
   cs=dict(districts=["Holešovice","Dejvice","Strahov","Staré Město","Žižkov","Vinohrady","Smíchov","Nusle","Karlín"], othercity="Brno", othercity_lede="Hledáte dílnu v Brně?"),
   en=dict(districts=["Holešovice","Dejvice","Strahov","Old Town","Žižkov","Vinohrady","Smíchov","Nusle","Karlín"], othercity="Brno", othercity_lede="Looking for a workshop in Brno?")),
 "brno": dict(P=P_BRNO, geo=BRNO_GEO, dir="dilny/brno", other="praha",
   cs=dict(title="Kde stavět v Brně: FabLab, hackerspace a dílny | PROTO ROBOT", desc="Mapa brněnských dílen, kde se dá tisknout, pájet, řezat laserem a stavět roboty: FabLab Brno, base48, makerspace v knihovně, strojLAB na VUT. Kdo tam smí a co tam je.",
     h1b="v Brně", hlore="Brněnská maker scéna v čase", checked="ověřeno 13. 11. 2026",
     districts=["Královo Pole","Žabovřesky","střed","Zábrdovice","Štýřice","Černá Pole","Pisárky","Medlánky"], othercity="Praha", othercity_lede="Hledáte dílnu v Praze?",
     timeline=[("2010","Vzniká base48, druhý český hackerspace. Spolek zapsán 6. srpna, jméno podle čísla domu, kde začínal.",""),
       ("2016","Vzniká Hobbylab, řemeslná dílna na dřevo a kov. Na FSI VUT se otevírá studentům strojLAB.",""),
       ("2017","JIC otevírá FabLab Brno v Technologickém parku: 182 m², stroje za 3 miliony od kraje a Honeywellu.",""),
       ("2019","Z FabLabu vyjíždí FabLab Experience, pojízdná dílna o 44 m² s laserem, tiskárnami a robotickou rukou. Hobbylab se stěhuje do Rousínova.",""),
       ("2026","strojLAB otevírá nový prostor v hlavní budově FSI. Knihovna Jiřího Mahena provozuje makerspace v IN-centru na náměstí Svobody.","now")]),
   en=dict(title="Where to build in Brno: FabLab, hackerspace and workshops | PROTO ROBOT", desc="A map of Brno workshops where you can 3D print, solder, laser cut and build robots: FabLab Brno, base48, the library makerspace, strojLAB at VUT. Who can use them and what they have.",
     h1b="in Brno", hlore="Brno's maker scene over time", checked="checked 13 Nov 2026",
     districts=["Královo Pole","Žabovřesky","centre","Zábrdovice","Štýřice","Černá Pole","Pisárky","Medlánky"], othercity="Prague", othercity_lede="Looking for a workshop in Prague?",
     timeline=[("2010","base48 opens, the second Czech hackerspace. Registered on 6 August, named after the house number where it started.",""),
       ("2016","Hobbylab opens, a craft workshop for wood and metal. strojLAB opens to students at FME VUT.",""),
       ("2017","JIC opens FabLab Brno in the Technology Park: 182 m², CZK 3M of machines funded by the region and Honeywell.",""),
       ("2019","FabLab Experience rolls out of the FabLab, a 44 m² mobile workshop with a laser, printers and a robot arm. Hobbylab moves to Rousínov.",""),
       ("2026","strojLAB opens a new space in the FME main building. The Jiří Mahen Library runs a makerspace at IN-centrum on náměstí Svobody.","now")]),
 ),
}

TPL = open(os.path.join(os.path.dirname(__file__), "tpl.html"), encoding="utf-8").read()
for city, C in CITIES.items():
  for lang, base in T.items():
    t = dict(base); t.update(C[lang])
    cs_url = "https://protorobot.cz/" + C["dir"] + "/"; en_url = "https://protorobot.cz/en/" + C["dir"] + "/"
    t["canon"] = cs_url if lang == "cs" else en_url
    t["alt"] = ("/en/" + C["dir"] + "/") if lang == "cs" else ("/" + C["dir"] + "/")
    odir = CITIES[C["other"]]["dir"]
    t["othercity_href"] = ("/" if lang == "cs" else "/en/") + odir + "/"
    data = [dict(n=p["n"], name=p["name"], lat=p["lat"], lon=p["lon"], acc=p["acc"], q=p["q"], web=p["web"], mail=p["mail"], src=p["src"], **p[lang]) for p in C["P"]]
    html = TPL
    rep = {k: v for k, v in t.items() if isinstance(v, str)}
    rep["lang"] = lang; rep["cs_url"] = cs_url; rep["en_url"] = en_url
    rep["datajson"] = json.dumps(dict(places=data, acc=t["acc"], districts=t["districts"], web=t["web"], maps=t["maps"], src=t["src"], of=t["of"], **C["geo"]), ensure_ascii=False)
    rep["timeline"] = "".join(f'<div class="ev {c}"><b>{y}</b><span>{s}</span></div>' for y, s, c in t["timeline"])
    rep["footlinks"] = "".join(f'<a href="{h}">{l}</a>' for h, l in t["footlinks"])
    rep["homehref"] = "/" if lang == "cs" else "/en/"
    for k, v in rep.items():
        html = html.replace("{{" + k + "}}", v)
    assert "{{" not in html, html[html.index("{{"):html.index("{{")+40]
    out = os.path.join(ROOT, C["dir"] if lang == "cs" else "en/" + C["dir"], "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out)
