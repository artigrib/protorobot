# PROTO ROBOT #0 landing

Static site, no build step. Live at https://protorobot.cz (Czech) and https://protorobot.cz/en/ (English).

    index.html      Czech version (protorobot.cz/)
    en/index.html   English version (protorobot.cz/en/)
    img/            greyscale images (the orange duotone is CSS)
                    .webp files are what the pages load; the .jpg/.png next to them are the sources
                    og.jpg is the social preview with the logo band (stays JPEG for crawlers)
    video/          H.264 clips (not used on the page since the program became a timetable)
    CNAME           custom domain for GitHub Pages (protorobot.cz)

The two pages are separate files with the same layout. Any change to content or styles has to be made in both.
Asset paths are absolute (/img/, /video/), so the site must live at the domain root, which it does with the custom domain.

## What is on the page

One system: the two posters (hero and the closing Register block) are centred, everything people read
sits on the left axis. The hero title is the page title (the intro h1 is visually hidden), every section heading
uses the same h2, and decoration without a job is left out.

Two shapes: a pill is something you press (orange pill = register), everything else is a rectangle
(photos, robot tiles, Live demo and step labels, the black hero badge). One lead size for the intro,
venue and registration text, at most ~60 characters a line. Nothing fades in on scroll.

1. Hero: carousel, PROTO ROBOT title centred and still; the black badge under it turns to the next fact with each photo (what / when / where)
2. Intro: who it is for, and one row: date and time → Program, place → Venue, orange Register on Luma.
   Details live once, in their own sections; the talk languages sit on the 19:00 line.
   Under it the line-up (.lineup), everything black and greyscale:
   "Řečníci z / Speakers from": Pollen Robotics, Hugging Face, Integra Robotics (mark + name; add Robotservice
   the same way once Tomáš sends a logo); "Podporují / Supported by": Pracovna, Maker Faire, ČAUI (logos sized by eye:
   --h 54/40/36px on desktop, 70% on phones). Pracovna's site logo recoloured, Maker Faire's site SVG recoloured,
   ČAUI from the PDFs the association sent (partner-caai.svg Czech, partner-caai-en.svg English).
   Only the speakers' companies and these three partners; no other organisations' logos (no investors, no registrants).
   Not "backed by": nobody here funds the event.
3. (The ticker was removed: its Register moved into the intro row.)
4. Speakers (a company logo sits right before its own name in the company line: an <img height="18" alt=""> inside
   that company's <span class="spk__co">, shown in greyscale to match the line-up; Fabien has Pollen + Hugging Face, Vítek has the
   Integra square mark (cut from the logo on integrarobotics.cz), Konečný gets his once he sends it; Bruna has none): four cards ordered by prominence, not by running order (Danieau, Vítek, Bruna, Konečný; the same goes for the line-up: Hugging Face first) (photo, LinkedIn, talk title, one-line note; optional "Live demo"
   and robot tile). On phones each card is photo left, text right
5. Program: three lines, 18:00 / 19:00 / 21:00
6. Venue: address, how to get in, map link, the way in as three photos (street, café, hall)
7. Register: centred closing block before the footer (one Luma button, follow on Luma). No separate
   calendar button: Luma offers it after registering, and a second button invites "added to calendar" instead of registering
(The separate Partners section at the bottom was folded into the line-up under the intro.)

Register appears three times: the header pill, the intro row and the closing block. The footer is plain text links.
On phones the section menu starts folded into one pill so the hero stays clear; tap it to open.

Every Register link opens Luma's checkout window on the page (embed.lu.ma/checkout-button.js, data-luma-* attributes).
If the script fails, the link opens the Luma event page as before. Each link tags registrations with
data-luma-utm-source (web-header-cs, web-ticker-en, ...) and page views with the same utm_source in the URL,
so Luma → Insights / Guests shows which button converts (web-header, web-intro, web-final; web-ticker and web-footer are retired).

Event details for search engines (date, venue, speakers) live in the JSON-LD block in the head of each page.

## Editing tips

- Speaker photos: square, greyscale, cropped so the head fills about the same share of the frame on every card.
- New images: add the source to img/, convert to .webp (quality ~78) and reference the .webp.
- After changing og.jpg, bump the `?v=` number in the og:image meta tags so Telegram and LinkedIn fetch the new one.
- Hero slides after the first load one beat ahead. video/ is no longer used on the page.

## Deploy

GitHub Pages serves the main branch from the repository root. Pushing to main publishes within a minute or two.
DNS: `protorobot.cz` A records → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; `www` CNAME → `<github-user>.github.io`.
