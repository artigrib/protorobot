"""Cut backgrounds, normalise face scale and eye line, render uniform 3:4 duotone cards."""
import sys, pathlib, cv2, numpy as np
from PIL import Image, ImageOps
from rembg import remove, new_session

A = '/mnt/user-data/attachments/a1a697a9-e7d7-5d30-b5c7-82cdf3b35dfb/'
SRC = {
 'filipensky': A + '3292d9d4-image.png',
 'borek': '/tmp/claude-0/-home-claude/a1a697a9-e7d7-5d30-b5c7-82cdf3b35dfb/scratchpad/borek.jpg',
 'vidovicova': '/mnt/user-data/uploads/Downloads/protorobot-spk/vidovicova.jpg',
 'cerny': A + '1ae5b3d6-image.png',
 'mikesova': A + '5141ef10-image.jpg',
 'orlova': A + '0b8213bf-image.png',
}
OUT = pathlib.Path('/home/claude/spk/cut'); OUT.mkdir(exist_ok=True)
W, H = 600, 560           # card
FACE_H = 0.58 * H         # target face box height
EYE_Y = 0.47 * H          # eye line
ORANGE = (232, 54, 10)
BG = tuple(int(sys.argv[1][i:i+2], 16) for i in (1, 3, 5)) if len(sys.argv) > 1 else ORANGE

sess = new_session('u2net_human_seg')
casc = cv2.CascadeClassifier('/tmp/haar.xml')

for k, path in SRC.items():
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    g = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    faces = casc.detectMultiScale(g, 1.05, 3, minSize=(int(im.width*0.08),)*2)
    if len(faces) == 0:
        print('no face', k); fx, fy, fw, fh = im.width*0.3, im.height*0.15, im.width*0.4, im.width*0.4
    else:
        fx, fy, fw, fh = max(faces, key=lambda f: f[2])
    up = max(1.0, 1200 / min(im.size))                  # small sources: upscale before matting, cleaner edge
    if up > 1:
        im = im.resize((int(im.width*up), int(im.height*up)), Image.LANCZOS); fx, fy, fw, fh = fx*up, fy*up, fw*up, fh*up
    cut = remove(im, session=sess)                      # RGBA
    from PIL import ImageFilter
    A = cut.split()[3].filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(2))  # eat the dark halo
    cut.putalpha(A)
    a0 = np.array(cut.split()[3]) > 40
    touch_l, touch_r = a0[:, :3].any(), a0[:, -3:].any()
    ey0 = fy + fh*0.42; cx0 = fx + fw/2
    s = FACE_H / fh
    s = max(s, (H - EYE_Y) / (im.height - ey0))            # no fade: subject must reach the card bottom
    cut = cut.resize((int(cut.width*s), int(cut.height*s)), Image.LANCZOS)
    cx = (fx + fw/2) * s; ey = (fy + fh*0.42) * s        # eyes ~42% down the face box
    # duotone: luminance -> black..orange, keep alpha
    rgb = cut.convert('RGB'); a = cut.split()[3]
    lum = ImageOps.autocontrast(rgb.convert('L'), cutoff=1)
    duo = ImageOps.colorize(lum, black=(0, 0, 0), white=ORANGE).convert('RGBA'); duo.putalpha(a)
    # fade the lower part into the background so every card ends the same way
    y0 = int(EYE_Y - ey0*s)
    grad = np.ones((cut.height, cut.width), np.float32)
    ys = (np.arange(cut.height) + y0) / H
    grad *= 1  # no fade
    aa = np.clip((np.array(a).astype(np.float32) - 120) / 110, 0, 1) * 255
    a2 = Image.fromarray((aa * grad).astype(np.uint8)); duo.putalpha(a2)
    card = Image.new('RGBA', (W, H), BG + (255,))
    card.alpha_composite(duo, (int(W/2 - cx), int(EYE_Y - ey)))
    card.convert('RGB').save(OUT / f'{k}.png')
    print(k, im.size, 'face', fw, 'scale %.2f' % s)
sheet = Image.new('RGB', (W*6 + 50, H), 'white')
for i, k in enumerate(SRC):
    sheet.paste(Image.open(OUT / f'{k}.png'), (i*(W+10), 0))
sheet.save(OUT / '_sheet.jpg', quality=85)
