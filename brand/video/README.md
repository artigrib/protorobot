# Video overlays, PROTO ROBOT #0

Same system as the website: Archivo (titles Black Italic, 125% width, caps), one orange #FF5A00, black rectangles,
duotone photos (greyscale + orange multiply). Folders by format: 9x16 (1080x1920, Reels/Shorts), 1x1 (1080x1080,
LinkedIn feed), 16x9 (1920x1080, YouTube).

| file | what | background |
|---|---|---|
| intro_<speaker>.png, intro_reachy-demo.png | opening card, 1.5–2 s | full frame |
| lower_<speaker>.png | name + company, bottom left, first 3–4 s of the talk | transparent |
| subtitle_sample.png | how subtitles should look | transparent |
| end_cs.png / end_en.png | closing card, 2–3 s | full frame |

Editing rules
- Footage in natural colour, only correct white balance and calm the green walls. Orange only on intro and end cards.
- Hard cuts. No zooms, Ken Burns or wipe transitions.
- Subtitles: Archivo SemiBold, white on a black box (not outline), centred, max 2 lines, sentence case.
  Size and position as in subtitle_sample.png. In CapCut: Text > font Archivo, background box #000 100%, no stroke.
- Lower third: in at 0.5 s, out after 3–4 s, plain cut or 6-frame fade.
- 9x16 safe zones: nothing important in the top 200 px or the bottom 250 px (app UI). The overlays already respect them.

Regenerate: `python3 brand/video/build.py <repo> <workdir> -` with the Archivo wdth woff2 files in <workdir>/f,
logos in <workdir>/logos and stage photos (img/0/l-NNNN.webp) in <workdir>/photos. Edit TALKS / DEMOS at the top.
