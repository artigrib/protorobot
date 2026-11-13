"""Portrait series v4: one crop rule, per-face tone normalisation, grain + posterise, duotone on orange.
Run from repo root: python3 tools/pages/cutouts_1.py
Writes
  brand/speakers-1/<key>.png   600x600 orange duotone cards for the covers (banner_1.py), + _sheet.jpg
  img/1/sp-<key>.webp          600x600 grayscale-on-white site portraits (the page adds its own orange multiply), + _sheet_site.jpg
Site window: a square 1.5x the face-box height, eye line at 44% of the side, face centred, no lead room. The window is
placed in the full-resolution cut and is never allowed to leave the source frame (the face is scaled up a few % or the
window nudged sideways instead), so no source edge and no fade is ever visible: the body exits through the frame.
"""
import pathlib, cv2, numpy as np
from PIL import Image, ImageOps, ImageFilter
from rembg import remove, new_session

A = '/mnt/user-data/attachments/a1a697a9-e7d7-5d30-b5c7-82cdf3b35dfb/'
SRC = {
 'filipensky': A + '3292d9d4-image.png',
 'borek': '/tmp/claude-0/-home-claude/a1a697a9-e7d7-5d30-b5c7-82cdf3b35dfb/scratchpad/borek.jpg',
 'vidovicova': str(pathlib.Path(__file__).resolve().parents[2] / 'brand/original/vidovicova_fss.jpg'),
 'cerny': A + '1ae5b3d6-image.png',
 'mikesova': A + '5141ef10-image.jpg',
 'orlova': A + '0b8213bf-image.png',
}
FACE = {'vidovicova': (380, 200, 300, 350)}   # manual face box (x, y, w, h) in source px where the detector misfires
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / 'brand/speakers-1'; OUT.mkdir(exist_ok=True)
SITE = ROOT / 'img/1'
W = H = 600
CARD_FACE, CARD_EYE = 0.44, 0.40      # covers: face-box height / eye line as a fraction of the 600 card
SITE_FACE, SITE_EYE = 1 / 1.5, 0.45   # site: window side = 1.5 face heights, eyes at 45% (Filipensky source native ratio)
EYE_IN_BOX = 0.42                     # eye line inside the haar box
ORANGE = np.array([232, 54, 10], np.float32)
SEED = 7

sess = new_session('u2net_human_seg')
casc = cv2.CascadeClassifier('/tmp/haar.xml')

def levels3(L, lo, mid, hi, tlo=0.08, tmid=0.52, thi=0.90):
    """three-point fit: black, white, gamma so that lo->tlo, hi->thi, mid->tmid"""
    x = np.clip((L - lo) / max(hi - lo, 1e-3), 0, 1)
    m = np.clip((mid - lo) / max(hi - lo, 1e-3), 0.05, 0.95)
    g = np.log((tmid - tlo) / (thi - tlo)) / np.log(m)
    return tlo + (thi - tlo) * x ** g

def finish(Lc, lv):
    """9) unsharp, 10) grain, 11) posterise - on the placed 600x600 luminance"""
    Lc = np.asarray(Image.fromarray((Lc * 255).astype(np.uint8)).filter(ImageFilter.UnsharpMask(1.5, 60, 2)), np.float32) / 255
    rng = np.random.default_rng(SEED); Lc = np.clip(Lc + rng.normal(0, 0.045, Lc.shape), 0, 1)
    return np.round(Lc * lv) / lv

def place(Lim, scale, cx, ey, eye_y):
    """scale the LA image and paste it so that (cx, ey) in source px lands at (W/2, eye_y)"""
    im = Lim.resize((max(1, int(Lim.width * scale)), max(1, int(Lim.height * scale))), Image.LANCZOS)
    canvas = Image.new('LA', (W, H), (0, 0))
    canvas.paste(im, (int(round(W / 2 - cx * scale)), int(round(eye_y - ey * scale))), im)
    return (np.asarray(canvas.split()[0], np.float32) / 255, np.asarray(canvas.split()[1], np.float32) / 255)

for k, path in SRC.items():
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    up = max(1.0, 1200 / min(im.size))
    if up > 1: im = im.resize((int(im.width * up), int(im.height * up)), Image.LANCZOS)
    g = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    if k in FACE:
        fx, fy, fw, fh = [v * up for v in FACE[k]]
    else:
        faces = casc.detectMultiScale(g, 1.05, 3, minSize=(int(im.width * 0.08),) * 2)
        fx, fy, fw, fh = max(faces, key=lambda f: f[2])
    sw, sh = im.size
    # 3) cutout
    cut = remove(im, session=sess)
    cut = ImageOps.expand(cut, 12, (0, 0, 0, 0)); fx, fy = fx + 12, fy + 12
    alpha = cut.split()[3].filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(1.5))
    an = np.asarray(alpha, np.float32) / 255
    # card only - frame-edge feather: where the subject is cut by the source frame, melt the last 10% into the field
    am = an.copy(); hh, ww = am.shape; f = int(min(hh, ww) * 0.10) + 12
    if am[12:16, :].max() > 0.5: am[:f, :] *= np.linspace(0, 1, f)[:, None]
    if am[-16:-12, :].max() > 0.5: am[-f:, :] *= np.linspace(1, 0, f)[:, None]
    if am[:, 12:16].max() > 0.5: am[:, :f] *= np.linspace(0, 1, f)[None, :]
    if am[:, -16:-12].max() > 0.5: am[:, -f:] *= np.linspace(1, 0, f)[None, :]
    # luminance 0..1
    L = np.asarray(cut.convert('L'), np.float32) / 255
    # 6) per-image levels to face targets (box: eyes to mouth, central 60% width)
    bx0, bx1 = int(fx + fw * 0.2), int(fx + fw * 0.8); by0, by1 = int(fy + fh * 0.3), int(fy + fh * 0.85)
    face = L[by0:by1, bx0:bx1]
    lo, mid, hi = np.percentile(face, 5), np.median(face), np.percentile(face, 95)
    L = levels3(L, lo, mid, hi)
    # 7) clothing lift below chin: adaptive, so a dark jacket and a white shirt land in the same band (mean ~0.45)
    #    under the site's orange multiply; measured within one face height below the chin, subject pixels only
    chin = int(fy + fh * 1.02)
    body = (an[chin:int(chin + fh), :] > 0.5)
    body_mean = float(L[chin:int(chin + fh), :][body].mean()) if body.any() else 0.45
    lift = float(np.clip(0.45 - body_mean, 0.06, 0.26))
    ramp = np.zeros_like(L); ramp[chin:, :] = lift
    ramp = cv2.GaussianBlur(ramp, (0, 0), 25)
    L = np.clip(L + ramp, 0, 1)
    # 8) global black / white
    L = np.clip((L - 0.06) / (0.94 - 0.06), 0, 1)
    L8 = Image.fromarray((L * 255).astype(np.uint8))
    cx, ey = fx + fw / 2, fy + fh * EYE_IN_BOX
    lv = 15 if k == 'filipensky' else 9   # scanned source bands at 10 levels

    # --- card (covers): melted edges, face 0.44H, eyes at 0.40H, duotone on orange
    Lim = L8.copy(); Lim.putalpha(Image.fromarray((am * 255).astype(np.uint8)))
    Lc, Ac = place(Lim, CARD_FACE * H / fh, cx, ey, CARD_EYE * H)
    Lc = finish(Lc, lv)
    rgb = Lc[..., None] * ORANGE[None, None, :]
    outp = rgb * Ac[..., None] + ORANGE * (1 - Ac[..., None])
    Image.fromarray(outp.astype(np.uint8)).save(OUT / f'{k}.png')

    # --- site: window 1.5 face heights, eyes at 44%, never outside the source frame (12px pad excluded)
    s = SITE_FACE * H / fh
    top_room, bot_room = (ey - 12) * s, (sh + 12 - ey) * s          # source px above / below the eye line, scaled
    need_top, need_bot = SITE_EYE * H, (1 - SITE_EYE) * H
    s *= max(1.0, need_top / top_room, need_bot / bot_room)          # grow the face a little rather than show the frame
    left_room, right_room = (cx - 12) * s, (sw + 12 - cx) * s
    nudge = max(0.0, W / 2 - left_room) - max(0.0, W / 2 - right_room)   # shift the window sideways if a side is short
    Lim = L8.copy(); Lim.putalpha(Image.fromarray((an * 255).astype(np.uint8)))
    Ls, As = place(Lim, s, cx - nudge / s, ey, SITE_EYE * H)
    Ls = finish(Ls, lv)
    site = Image.fromarray(((Ls * As + 1.0 * (1 - As)) * 255).astype(np.uint8)).convert('RGB')
    site.save(SITE / f'sp-{k}.webp', 'WEBP', quality=84)
    print(f'{k:11s} face {int(fh)}  lo/mid/hi {lo:.2f} {mid:.2f} {hi:.2f}  site scale x{s * fh / H / SITE_FACE:.3f} nudge {nudge:+.0f}px  body {body_mean:.2f} lift {lift:.2f}')

sheet = Image.new('RGB', (W * 6 + 50, H), 'white')
for i, k in enumerate(SRC): sheet.paste(Image.open(OUT / f'{k}.png'), (i * (W + 10), 0))
sheet.save(OUT / '_sheet.jpg', quality=85)
sheet = Image.new('RGB', (W * 6 + 50, H), 'white')
for i, k in enumerate(SRC): sheet.paste(Image.open(SITE / f'sp-{k}.webp'), (i * (W + 10), 0))
sheet.save(OUT / '_sheet_site.jpg', quality=85)
