"""Regenerate gallery thumbnails img/0/g-*.webp from brand/photos/0 originals.
Keeps the tone of the existing thumbnails (a lifted curve, fitted per photo as a smooth float curve)
but works in float and adds fine grain so the CSS orange multiply + dark gradient doesn't band."""
import sys,glob,os
from PIL import Image, ImageOps
import numpy as np
Q=int(sys.argv[1]) if len(sys.argv)>1 else 82
out=sys.argv[2] if len(sys.argv)>2 else 'img/0'
ref_dir=sys.argv[3] if len(sys.argv)>3 else 'img/0'  # tone reference (the previous thumbnails; keep a copy before overwriting)
rng=np.random.default_rng(0)
for src in sorted(glob.glob('brand/photos/0/DSC0*.jpg')):
    n=os.path.basename(src)[4:8]
    old=Image.open(f'{ref_dir}/g-{n}.webp')
    im=ImageOps.fit(Image.open(src).convert('RGB'),old.size,Image.LANCZOS)
    a=np.asarray(im).astype(np.float32)
    y=a[...,0]*.2126+a[...,1]*.7152+a[...,2]*.0722
    o=np.asarray(old.convert('L')).astype(np.float32)
    xs,ys=[],[]
    for v in range(0,256,4):
        m=(y>=v)&(y<v+4)
        if m.sum()>50: xs.append(v+2); ys.append(o[m].mean())
    c=np.polyfit(np.sqrt(np.array(xs)/255),ys,3)
    t=np.maximum.accumulate(np.polyval(c,np.sqrt(np.arange(256)/255)))
    y=np.interp(y,np.arange(256),t)
    y=y+rng.normal(0,1.6,y.shape)
    Image.fromarray(np.clip(np.round(y),0,255).astype(np.uint8),'L').save(f'{out}/g-{n}.webp','WEBP',quality=Q,method=6)
    print(n,end=' ',flush=True)
