"""Compose a YouTube thumbnail from frames of the finished film.

A thumbnail is not a nice frame -- it is a poster that has to work at two very
different sizes. On a desktop home row it is about 360 px wide; in a mobile feed
or a suggested-video sidebar it is nearer 168 px. Everything here is driven by
that: text is sized as a fraction of frame height so it survives the shrink,
carries a heavy dark stroke so it survives being placed on any photo, and is
kept to two or three words because more is unreadable at feed size.

Three other constraints worth knowing:

  Pull frames from a CAPTION-FREE source. `final.mp4` has burned captions and
  graphics, so a frame from it puts stray sentence fragments in the thumbnail.
  Use base.mkv or the synced sources.

  Leave the bottom-right corner alone. The platform stamps the duration there,
  over whatever you put underneath.

  Push contrast and saturation harder than looks right on its own. A thumbnail
  competes against twenty others rather than being viewed in isolation, and a
  correctly graded frame reads as flat in that context.

Layouts
-------
split   food on one side, face on the other, divided by a bright rule. Says
        "food review" instantly because both halves of the promise are visible.
face    single full-bleed frame with a scrim panel for type. Stronger when the
        expression alone carries it.

Usage:
    python helpers/thumbnail.py --layout split \\
        --food edit/thumb/clean_1.0.png --face edit/thumb/clean_8.6.png \\
        --headline '$15.42' --kicker "ALBERTO'S · ESCONDIDO" \\
        --icon assets/tapatio_bottle.png --icons 4 \\
        -o edit/thumb/thumb_split.png

    python helpers/thumbnail.py --layout face --face edit/thumb/clean_8.6.png \\
        --headline '$15 BURRITO' --sub '4 TAPATIOS' -o edit/thumb/thumb_face.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 1280, 720          # YouTube's recommended thumbnail size
YELLOW = (255, 208, 40)
RED = (206, 32, 32)
INK = (12, 10, 9)

FONTS_BOLD = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONTS_BOLD:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def measure(d: ImageDraw.ImageDraw, text: str, f) -> tuple[int, int]:
    box = d.textbbox((0, 0), text, font=f)
    return box[2] - box[0], box[3] - box[1]


def fill_crop(img: Image.Image, tw: int, th: int, focus_x: float = 0.5,
              focus_y: float = 0.45, zoom: float = 1.0) -> Image.Image:
    """Scale to cover a tw x th box and crop, keeping a chosen point in view.

    focus_y defaults slightly above centre because faces sit high in a frame and
    a centre crop tends to slice the forehead.

    `zoom` crops in before fitting. It matters more than it sounds: a source
    frame that already matches 16:9 gets no crop at all, so whatever dead space
    the shot contained is faithfully reproduced in the thumbnail. Pushing in is
    what turns a wide shot into a poster.
    """
    if zoom > 1.0:
        cw, ch = int(img.width / zoom), int(img.height / zoom)
        cx = int((img.width - cw) * min(max(focus_x, 0), 1))
        cy = int((img.height - ch) * min(max(focus_y, 0), 1))
        img = img.crop((cx, cy, cx + cw, cy + ch))
    scale = max(tw / img.width, th / img.height)
    img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))),
                     Image.LANCZOS)
    x = int((img.width - tw) * min(max(focus_x, 0), 1))
    y = int((img.height - th) * min(max(focus_y, 0), 1))
    return img.crop((x, y, x + tw, y + th))


def punch(img: Image.Image, sat: float = 1.35, con: float = 1.18,
          bri: float = 1.05, sharp: float = 1.5) -> Image.Image:
    """Push the image past a correct grade, because a feed is a competition."""
    img = ImageEnhance.Color(img).enhance(sat)
    img = ImageEnhance.Contrast(img).enhance(con)
    img = ImageEnhance.Brightness(img).enhance(bri)
    return ImageEnhance.Sharpness(img).enhance(sharp)


def outlined(d: ImageDraw.ImageDraw, xy, text: str, f, fill, stroke_px: int,
             shadow: tuple[int, int] | None = None,
             shadow_fill=(0, 0, 0, 170)) -> None:
    """Text with a heavy stroke, and optionally an offset drop shadow.

    The stroke is what makes type survive landing on an arbitrary photo; without
    it, light text over a bright highlight simply disappears.
    """
    x, y = xy
    if shadow:
        d.text((x + shadow[0], y + shadow[1]), text, font=f, fill=shadow_fill,
               stroke_width=stroke_px, stroke_fill=shadow_fill)
    d.text((x, y), text, font=f, fill=fill, stroke_width=stroke_px,
           stroke_fill=INK)


def load_icons(path: Path, count: int, height: int) -> Image.Image | None:
    """A row of icons with a soft dark silhouette behind each."""
    if not path or not path.exists() or count <= 0:
        return None
    icon = Image.open(path).convert("RGBA")
    iw = max(1, int(icon.width * height / icon.height))
    icon = icon.resize((iw, height), Image.LANCZOS)
    gap = int(iw * 0.28)
    pad = max(4, height // 16)
    row = Image.new("RGBA", (iw * count + gap * (count - 1) + pad * 2,
                             height + pad * 2), (0, 0, 0, 0))
    sil = Image.new("RGBA", icon.size, (0, 0, 0, 255))
    sil.putalpha(icon.getchannel("A").point(lambda v: int(v * 0.8)))
    for i in range(count):
        x = pad + i * (iw + gap)
        shadow = Image.new("RGBA", row.size, (0, 0, 0, 0))
        shadow.alpha_composite(sil, (x, pad))
        row.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(pad * 0.8)))
        row.alpha_composite(icon, (x, pad))
    return row


# -------- Layouts ------------------------------------------------------------


def layout_split(args) -> Image.Image:
    """Food | face, divided by a bright rule. Both halves of the promise."""
    split_x = int(W * 0.46)
    canvas = Image.new("RGB", (W, H), INK)

    food = punch(fill_crop(Image.open(args.food).convert("RGB"), split_x, H,
                           args.food_x, args.food_y), sat=1.42, con=1.20)
    face = punch(fill_crop(Image.open(args.face).convert("RGB"), W - split_x, H,
                           args.face_x, args.face_y, args.zoom))
    canvas.paste(food, (0, 0))
    canvas.paste(face, (split_x, 0))

    d = ImageDraw.Draw(canvas, "RGBA")
    # Bright rule on the seam: reads as a designed split rather than a collage.
    d.rectangle([split_x - 7, 0, split_x + 6, H], fill=YELLOW)

    # Headline low on the food side, lifted off the picture by a scrim.
    f_head = font(int(H * args.head_scale))
    hw, hh = measure(d, args.headline, f_head)
    hx, hy = int(W * 0.035), int(H * 0.60)
    d.rectangle([0, hy - int(H * 0.05), split_x - 7, H], fill=(0, 0, 0, 130))
    outlined(d, (hx, hy), args.headline, f_head, YELLOW,
             stroke_px=max(6, int(H * 0.014)), shadow=(6, 8))

    if args.kicker:
        f_k = font(int(H * 0.052))
        kw, kh = measure(d, args.kicker.upper(), f_k)
        pad = int(H * 0.018)
        d.rectangle([hx - pad, hy - int(H * 0.05) - kh - pad * 2,
                     hx + kw + pad, hy - int(H * 0.05)], fill=RED)
        d.text((hx, hy - int(H * 0.05) - kh - pad), args.kicker.upper(),
               font=f_k, fill=(255, 255, 255))

    row = load_icons(args.icon, args.icons, int(H * (args.icon_scale or 0.20)))
    if row:
        canvas.paste(row, (W - row.width - int(W * 0.02), int(H * 0.03)), row)
    return canvas


def layout_face(args) -> Image.Image:
    """One full-bleed frame, type on a scrim panel."""
    canvas = punch(fill_crop(Image.open(args.face).convert("RGB"), W, H,
                             args.face_x, args.face_y, args.zoom))
    d = ImageDraw.Draw(canvas, "RGBA")

    panel_w = int(W * 0.46)
    # Gradient scrim rather than a hard box, so the frame still reads as a photo.
    grad = Image.new("L", (panel_w, 1))
    px = grad.load()
    for x in range(panel_w):
        px[x, 0] = int(215 * (1 - (x / panel_w) ** 1.7))
    scrim = Image.new("RGBA", (panel_w, H), INK + (255,))
    scrim.putalpha(grad.resize((panel_w, H), Image.BILINEAR))
    canvas.paste(scrim, (0, 0), scrim)

    words = args.headline.upper().split()
    f_head = font(int(H * args.head_scale))
    y = int(H * 0.20)
    for wd in words:
        outlined(d, (int(W * 0.035), y), wd, f_head, YELLOW,
                 stroke_px=max(6, int(H * 0.015)), shadow=(5, 7))
        y += int(H * args.head_scale * 1.06)

    if args.sub:
        f_s = font(int(H * args.sub_scale))
        outlined(d, (int(W * 0.035), y + int(H * 0.02)), args.sub.upper(), f_s,
                 (255, 255, 255), stroke_px=max(4, int(H * 0.010)))
        y += int(H * 0.10)

    row = load_icons(args.icon, args.icons, int(H * (args.icon_scale or 0.17)))
    if row:
        canvas.paste(row, (int(W * 0.035), min(y + int(H * 0.03), H - row.height)), row)
    return canvas


LAYOUTS = {"split": layout_split, "face": layout_face}


def main() -> None:
    ap = argparse.ArgumentParser(description="Compose a YouTube thumbnail.")
    ap.add_argument("--layout", choices=sorted(LAYOUTS), default="split")
    ap.add_argument("--face", type=Path, required=True,
                    help="Caption-free frame with the subject")
    ap.add_argument("--food", type=Path, help="split only: the food frame")
    ap.add_argument("--headline", required=True, help="2-3 words, no more")
    ap.add_argument("--sub", default="", help="face only: second line")
    ap.add_argument("--kicker", default="", help="split only: small red banner")
    ap.add_argument("--icon", type=Path, help="RGBA icon for a rating row")
    ap.add_argument("--icons", type=int, default=0)
    ap.add_argument("--zoom", type=float, default=1.0,
                    help="Crop in before fitting. A 16:9 source otherwise passes "
                         "through untouched, dead space included.")
    ap.add_argument("--sub-scale", type=float, default=0.072,
                    help="Second line height as a fraction of frame height")
    ap.add_argument("--icon-scale", type=float, default=0.0,
                    help="Icon row height as a fraction of frame height. Below "
                         "~0.14 icons collapse into coloured dots at feed size.")
    ap.add_argument("--head-scale", type=float, default=0.165,
                    help="Headline height as a fraction of frame height. Below "
                         "~0.12 it stops being readable at feed size.")
    ap.add_argument("--face-x", type=float, default=0.5)
    ap.add_argument("--face-y", type=float, default=0.42)
    ap.add_argument("--food-x", type=float, default=0.5)
    ap.add_argument("--food-y", type=float, default=0.5)
    ap.add_argument("-o", "--output", type=Path, required=True)
    args = ap.parse_args()

    if args.layout == "split" and not args.food:
        ap.error("--layout split needs --food")

    img = LAYOUTS[args.layout](args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    img.save(args.output, quality=95)

    # A feed-size proof next to the full size, because that is where thumbnails
    # actually fail and it is the one check people skip.
    proof = args.output.with_name(args.output.stem + "_feedsize.png")
    img.resize((168, 94), Image.LANCZOS).save(proof)
    kb = args.output.stat().st_size / 1024
    print(f"{args.output}  {W}x{H}  {kb:.0f} KB"
          + ("  (over YouTube's 2MB limit)" if kb > 2048 else ""))
    print(f"{proof}  168x94 proof -- if the text is not readable here, it fails")


if __name__ == "__main__":
    main()
