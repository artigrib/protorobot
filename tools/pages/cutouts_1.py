"""Portrait series v3 (jury recipe): one crop rule, per-face tone normalisation, grain + posterise, duotone on orange.
Output: /home/claude/spk/cut3/<key>.png 600x600 and _sheet.jpg
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
GAZE = {'borek': -1}
FACE = {'vidovicova': (380, 200, 300, 350)}   # manual face box (x, y, w, h) in source px where the detector misfires   # -1 looks left, +1 looks right -> shift face 8% toward gaze side
OUT = pathlib.Path(__file__).resolve().parents[2] / 'brand/speakers-1'; OUT.mkdir(exist_ok=True)
W = H = 600
FACE_H, EYE_Y = 0.44 * H, 0.40 * H
ORANGE = np.array([232, 54, 10], np.float32)

sess = new_session('u2net_human_seg')
casc = cv2.CascadeClassifier('/tmp/haar.xml')

def levels3(L, lo, mid, hi, tlo=0.08, tmid=0.52, thi=0.90):
    """three-point fit: black, white, gamma so that lo->tlo, hi->thi, mid->tmid"""
    x = np.clip((L - lo) / max(hi - lo, 1e-3), 0, 1)
    m = np.clip((mid - lo) / max(hi - lo, 1e-3), 0.05, 0.95)
    g = np.log(tmid_n(tlo, tmid, thi)) / np.log(m)
    return tlo + (thi - tlo) * x ** g

def tmid_n(tlo, tmid, thi):
    return (tmid - tlo) / (thi - tlo)

for k, path in SRC.items():
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    up = max(1.0, 1200 / min(im.size))
    if up > 1: im = im.resize((int(im.width*up), int(im.height*up)), Image.LANCZOS)
    g = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    if k in FACE:
        fx, fy, fw, fh = [v*up for v in FACE[k]]
    else:
        faces = casc.detectMultiScale(g, 1.05, 3, minSize=(int(im.width*0.08),)*2)
        fx, fy, fw, fh = max(faces, key=lambda f: f[2])
    # 3) cutout
    cut = remove(im, session=sess)
    cut = ImageOps.expand(cut, 12, (0, 0, 0, 0)); fx, fy = fx + 12, fy + 12
    alpha = cut.split()[3].filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(1.5))
    # frame-edge feather: where the subject is cut by the source frame, melt the last 3% into the field instead of a hard line
    an = np.asarray(alpha, np.float32) / 255; hh, ww = an.shape; f = int(min(hh, ww) * 0.10) + 12
    if an[12:16, :].max() > 0.5: an[:f, :] *= np.linspace(0, 1, f)[:, None]
    if an[-16:-12, :].max() > 0.5: an[-f:, :] *= np.linspace(1, 0, f)[:, None]
    if an[:, 12:16].max() > 0.5: an[:, :f] *= np.linspace(0, 1, f)[None, :]
    if an[:, -16:-12].max() > 0.5: an[:, -f:] *= np.linspace(1, 0, f)[None, :]
    alpha = Image.fromarray((an * 255).astype(np.uint8))
    # luminance 0..1
    L = np.asarray(cut.convert('L'), np.float32) / 255
    # 6) per-image levels to face targets (box: eyes to mouth, central 60% width)
    bx0, bx1 = int(fx + fw*0.2), int(fx + fw*0.8); by0, by1 = int(fy + fh*0.3), int(fy + fh*0.85)
    face = L[by0:by1, bx0:bx1]
    lo, mid, hi = np.percentile(face, 5), np.median(face), np.percentile(face, 95)
    L = levels3(L, lo, mid, hi)
    # 7) clothing lift below chin
    chin = int(fy + fh * 1.02)
    ramp = np.zeros_like(L); ramp[chin:, :] = 0.12
    ramp = cv2.GaussianBlur(ramp, (0, 0), 25)
    L = np.clip(L + ramp, 0, 1)
    # 8) global black / white
    L = np.clip((L - 0.06) / (0.94 - 0.06), 0, 1)
    Lim = Image.fromarray((L * 255).astype(np.uint8)); Lim.putalpha(alpha)
    # 4-5) scale + place
    s = FACE_H / fh
    Lim = Lim.resize((int(Lim.width*s), int(Lim.height*s)), Image.LANCZOS)
    cx = (fx + fw/2) * s + GAZE.get(k, 0) * 0.04 * W   # lead room: face offset against the gaze, space in front of the look
    ey = (fy + fh*0.42) * s
    canvas = Image.new('LA', (W, H), (0, 0))
    canvas.paste(Lim, (int(W/2 - cx), int(EYE_Y - ey)), Lim)
    Lc = np.asarray(canvas.split()[0], np.float32) / 255; Ac = np.asarray(canvas.split()[1], np.float32) / 255
    # 9) unsharp, 10) grain, 11) posterise
    Lc = np.asarray(Image.fromarray((Lc*255).astype(np.uint8)).filter(ImageFilter.UnsharpMask(1.5, 60, 2)), np.float32) / 255
    rng = np.random.default_rng(7); Lc = np.clip(Lc + rng.normal(0, 0.045, Lc.shape), 0, 1)
    lv = 15 if k == 'filipensky' else 9   # scanned source bands at 10 levels
    Lc = np.round(Lc * lv) / lv
    # 12-13) duotone over orange
    rgb = Lc[..., None] * ORANGE[None, None, :]
    outp = rgb * Ac[..., None] + ORANGE * (1 - Ac[..., None])
    Image.fromarray(outp.astype(np.uint8)).save(OUT / f'{k}.png')
    # site version: same cut and tone, grayscale on white; the page applies its own orange multiply
    site = (Lc * Ac + 1.0 * (1 - Ac)) * 255
    Image.fromarray(site.astype(np.uint8)).convert('RGB').save(OUT.parents[1] / 'img/1' / f'sp-{k}.webp', 'WEBP', quality=84)
    print(k, 'face', int(fh), 'lo/mid/hi %.2f %.2f %.2f' % (lo, mid, hi))

sheet = Image.new('RGB', (W*6 + 50, H), 'white')
for i, k in enumerate(SRC): sheet.paste(Image.open(OUT / f'{k}.png'), (i*(W+10), 0))
sheet.save(OUT / '_sheet.jpg', quality=85)
