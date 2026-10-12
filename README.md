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

One system: everything sits on the left axis, the intro h1 is the only large heading, every section
heading uses the same smaller h2, and decoration without a job is left out.

1. Hero: carousel, straight PROTO ROBOT title on the left axis, flipping badge under it (Meetup #0 / date)
2. Intro: date, times, venue, languages, then the first Register button
3. Ticker: links to registration
4. Speakers: four cards in running order (photo, LinkedIn, talk title, one-line note; optional "Live demo"
   and robot tile). On phones each card is photo left, text right
5. Program: three lines, 18:00 / 19:00 / 21:00
6. Venue: address, how to get in, map link, the way in as three photos (street, café, hall)
7. Register: last section before the footer (Luma, Google Calendar, follow on Luma)

Register appears three times: the header pill, under the intro, and as the last section.

Event details for search engines (date, venue, speakers) live in the JSON-LD block in the head of each page.

## Editing tips

- Speaker photos: square, greyscale, cropped so the head fills about the same share of the frame on every card.
- New images: add the source to img/, convert to .webp (quality ~78) and reference the .webp.
- After changing og.jpg, bump the `?v=` number in the og:image meta tags so Telegram and LinkedIn fetch the new one.
- Hero slides after the first load one beat ahead. video/ is no longer used on the page.

## Deploy

GitHub Pages serves the main branch from the repository root. Pushing to main publishes within a minute or two.
DNS: `protorobot.cz` A records → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; `www` CNAME → `<github-user>.github.io`.
