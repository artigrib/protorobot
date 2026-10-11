# PROTO ROBOT #0 landing

Static site, no build step. Live at https://protorobot.cz (Czech) and https://protorobot.cz/en/ (English).

    index.html      Czech version (protorobot.cz/)
    en/index.html   English version (protorobot.cz/en/)
    img/            greyscale images (the orange duotone is CSS)
                    .webp files are what the pages load; the .jpg/.png next to them are the sources
                    og.jpg is the social preview (stays JPEG for crawlers)
    video/          H.264 clips for the timetable cards
    CNAME           custom domain for GitHub Pages (protorobot.cz)

The two pages are separate files with the same layout. Any change to content or styles has to be made in both.
Asset paths are absolute (/img/, /video/), so the site must live at the domain root, which it does with the custom domain.

## What is on the page

1. Hero carousel and intro (date, times, venue, languages)
2. Programme: timetable cards 18:00 / 19:00 / 21:00
3. Speakers: four cards in running order, each with photo, LinkedIn link, talk title and one-line note.
   Optional pills on the photo: "Live demo" (bottom left) and a robot tile (bottom right, img/bot-*.webp)
4. Registration: Luma link, Google Calendar link, "follow on Luma" for the next meetups
5. Venue: Pracovna, Vlkova 36, Prague 3, how to get in, map link, three photos of the place

Event details for search engines (date, venue, speakers) live in the JSON-LD block in the head of each page.

## Editing tips

- Speaker photos: square, greyscale, cropped so the head fills about the same share of the frame on every card.
- New images: add the source to img/, convert to .webp (quality ~78) and reference the .webp.
- After changing og.jpg, bump the `?v=` number in the og:image meta tags so Telegram and LinkedIn fetch the new one.
- Timetable videos load only when the visitor scrolls near them; hero slides after the first load one beat ahead.

## Deploy

GitHub Pages serves the main branch from the repository root. Pushing to main publishes within a minute or two.
DNS: `protorobot.cz` A records → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; `www` CNAME → `<github-user>.github.io`.
