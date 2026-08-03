"""Isolate the Alberto's roofline sign into an alpha PNG.

Source is a crop of a 4K frame: the red script "Alberto's" plus the little
waiter mascot, mounted above the building's red corrugated roof against clean
blue sky.

Keying the sky is easy — sky is blue-dominant and bright, while the sign's red,
the mascot's navy and its white shirt all fail at least one of those tests.
Dropping the roof is the hard part, because the roof is the same red as the
sign and rust streaks running down from the letters connect the two into a
single blob, so a connected-component filter cannot separate them.

What does separate them is that the roof is a straight edge. Scanning each
column upward from the bottom while the pixel stays opaque finds the roof's
top edge and nothing else (the sign floats above it), and those points fit a
line to within a couple of pixels. Cut on that line.
"""
import sys
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from scipy import ndimage

RAW = "edit/thumb/logo_raw.png"    # ffmpeg -ss 4.0 -i footage/IMG_1843.MOV -vframes 1,
                                  # cropped (1500,60)-(3400,620) of the 3840x2160 frame
OUT = sys.argv[1] if len(sys.argv) > 1 else "assets/albertos_logo.png"

im = Image.open(RAW).convert("RGB").crop((320, 120, 1380, 500))
a = np.asarray(im).astype(np.int16)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

sky = ((B - R) > 26) & (B > 105)
# border_value=1: the default 0 erodes the frame edge away, and the bottom row
# is exactly where the roof edge has to be measured.
opaque = ndimage.binary_closing(~sky, np.ones((3, 3)), border_value=1)
h, w = opaque.shape

# Roof top edge: from the bottom of each column, climb while still opaque.
xs, ys = [], []
for x in range(w):
    col = opaque[:, x]
    if not col[h - 1]:
        continue
    y = h - 1
    while y > 0 and col[y - 1]:
        y -= 1
    xs.append(x)
    ys.append(y)
m, b = np.polyfit(np.array(xs, float), np.array(ys, float), 1)
resid = np.abs(np.array(ys) - (m * np.array(xs) + b))
print(f"roofline y = {m:+.4f}x {b:+.1f}   "
      f"fit over {len(xs)} cols, max resid {resid.max():.1f} px")

grid_x = np.arange(w)[None, :]
grid_y = np.arange(h)[:, None]
above_roof = grid_y < (m * grid_x + b) - 2      # 2 px of margin
keep = opaque & above_roof

# Anything left that is tiny is key noise along the cut, not sign.
lab, n = ndimage.label(keep)
sizes = ndimage.sum(keep, lab, range(1, n + 1))
for i, s in enumerate(sizes, start=1):
    if s < 400:
        keep[lab == i] = False
print(f"kept {int(keep.sum())} px in "
      f"{int((sizes >= 400).sum())} components (of {n})")

# The sign is sun-washed in the frame and reads dull against a saturated
# thumbnail background.
rgb = ImageEnhance.Color(im).enhance(1.55)
rgb = ImageEnhance.Contrast(rgb).enhance(1.20)

alpha = Image.fromarray((keep * 255).astype(np.uint8), "L")
alpha = alpha.filter(ImageFilter.GaussianBlur(0.8))   # no aliasing when scaled
out = rgb.convert("RGBA")
out.putalpha(alpha)
out = out.crop(out.getchannel("A").getbbox())
out.save(OUT)
print("wrote", OUT, out.size)
