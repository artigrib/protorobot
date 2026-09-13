# PROTO ROBOT #0 landing

Static site, no build step.

    index.html      Czech version (protorobot.cz/)
    en/index.html   English version (protorobot.cz/en/)
    img/         greyscale JPEGs (orange duotone is CSS), og.jpg for social previews
    video/       H.264 clips for the agenda cards
    CNAME        custom domain for GitHub Pages (protorobot.cz)
    .nojekyll    tells Pages to serve files as-is

Both pages link to each other with hreflang; the language switch is the small pill next to Register and a link in the footer.
Asset paths are absolute (/img/, /video/), so the site must live at the domain root, which is the case with the custom domain.

## Deploy to GitHub Pages with protorobot.cz

1. Push the contents of this folder to the repository root (or to a `docs/` folder) on the branch you publish from.
2. Repository → Settings → Pages: pick the branch/folder. The CNAME file sets the custom domain automatically.
3. DNS at the registrar:
   - `protorobot.cz`  A records → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - `www`  CNAME → `<github-user>.github.io`
4. Back in Settings → Pages, wait for the DNS check to pass, then tick "Enforce HTTPS".

Both `protorobot.cz` and `www.protorobot.cz` will resolve; GitHub redirects www to the apex.

## After the first deploy

- Open the page, send one test request through the form and check it lands in the Google Form responses.
- Share the URL in Telegram or LinkedIn to confirm the og.jpg preview shows up.
