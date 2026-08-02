"""Render motion-graphic overlays as alpha video, with no browser or network.

Produces VP9 WebM with a real alpha channel, which `render.py` composites
straight onto the cut. Everything is drawn with PIL and piped to ffmpeg, so
this works offline and has no Node, Chrome or CDN dependency. For anything
more ambitious than the card types here -- 3D, physics, data-viz, a designed
brand system -- use the `motion-graphics` skill and HyperFrames instead.

Card types
----------
lower_third   name plus a smaller line under it, slides in from the left
stamp         big rotated word that punches in and settles. The reaction beat.
price         a price chip that pops
title         full-frame opener
chapter       a section break band

Motion rules that make these read as intentional rather than default:

  Nothing moves linearly. Entrances ease out, exits ease in, and the stamp
  overshoots and settles because a hard stop reads as a freeze.

  Everything holds still in the middle. An element that keeps drifting while
  you read it fights the reading. Move, stop, hold, leave.

  Entrances are fast (0.35 s) and exits are faster (0.25 s). Slow titles are
  the single most common reason a cut feels sluggish.

Usage:
    python helpers/graphics.py lower_third --text "AL PASTOR" --sub "$3.50 each" \\
        -o edit/animations/slot_1/render.webm
    python helpers/graphics.py stamp --text "10/10" --duration 1.6 -o out.webm
    python helpers/graphics.py title --text "MR TACO SHOP" --sub "BREAKFAST BURRITO" -o out.webm
    python helpers/graphics.py --spec cards.json --out-dir edit/animations
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FPS = 24

FONT_CANDIDATES_BOLD = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]
FONT_CANDIDATES_REGULAR = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
]

# Campy diner palette: hot yellow on near-black with a chilli-red accent.
THEMES = {
    "campy": {"bg": (18, 16, 14, 235), "fg": (255, 214, 51, 255),
              "accent": (214, 40, 40, 255), "sub": (240, 235, 225, 255)},
    "clean": {"bg": (12, 12, 14, 210), "fg": (255, 255, 255, 255),
              "accent": (90, 170, 230, 255), "sub": (200, 205, 210, 255)},
    "salsa": {"bg": (28, 10, 10, 235), "fg": (255, 244, 224, 255),
              "accent": (240, 130, 30, 255), "sub": (250, 200, 140, 255)},
}


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    for path in (FONT_CANDIDATES_BOLD if bold else FONT_CANDIDATES_REGULAR):
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


# -------- Easing -------------------------------------------------------------


def ease_out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3


def ease_in_cubic(t: float) -> float:
    return t ** 3


def ease_out_back(t: float, overshoot: float = 1.7) -> float:
    """Overshoots past the target and settles. Use for anything that punches."""
    c3 = overshoot + 1
    return 1 + c3 * (t - 1) ** 3 + overshoot * (t - 1) ** 2


def envelope(t: float, duration: float, tin: float = 0.35, tout: float = 0.25) -> tuple[float, float]:
    """Return (enter, exit) progress in 0..1 for time t.

    enter ramps 0->1 over the entrance, exit ramps 0->1 over the departure.
    The hold in the middle has enter=1, exit=0.
    """
    enter = 1.0 if t >= tin else max(0.0, t / tin)
    remaining = duration - t
    leave = 0.0 if remaining >= tout else min(1.0, 1 - remaining / tout)
    return enter, leave


def text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


# -------- Card renderers -----------------------------------------------------
#
# Each returns an RGBA frame for time t. Coordinates are absolute pixels in the
# full output frame, so a card can be positioned anywhere without the caller
# doing any maths.


def draw_lower_third(t: float, cfg: dict) -> Image.Image:
    W, H, dur = cfg["width"], cfg["height"], cfg["duration"]
    th = THEMES[cfg["theme"]]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    enter, leave = envelope(t, dur)
    slide = ease_out_cubic(enter) * (1 - ease_in_cubic(leave))
    if slide <= 0.001:
        return img

    f_main = load_font(int(H * 0.052), bold=True)
    f_sub = load_font(int(H * 0.030), bold=False)
    text, sub = cfg["text"].upper(), cfg.get("sub", "")

    tw, th_ = text_size(d, text, f_main)
    sw, sh = text_size(d, sub, f_sub) if sub else (0, 0)

    padx, pady = int(H * 0.028), int(H * 0.022)
    bar_w = int(H * 0.011)
    box_w = max(tw, sw) + padx * 2 + bar_w
    box_h = th_ + (sh + int(H * 0.018) if sub else 0) + pady * 2

    # Sit on the caption safe line: clear of the lower third of the frame where
    # burned captions and platform UI live.
    x0 = int(W * 0.06) - int((1 - slide) * (box_w + W * 0.06))
    y0 = int(H * 0.66)

    d.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], radius=int(H * 0.012),
                        fill=th["bg"])
    d.rounded_rectangle([x0, y0, x0 + bar_w, y0 + box_h],
                        radius=int(H * 0.004), fill=th["accent"])

    tx = x0 + bar_w + padx
    d.text((tx, y0 + pady), text, font=f_main, fill=th["fg"])
    if sub:
        d.text((tx, y0 + pady + th_ + int(H * 0.018)), sub, font=f_sub, fill=th["sub"])
    return img


def draw_stamp(t: float, cfg: dict) -> Image.Image:
    """A rotated word that punches in and settles. The reaction beat."""
    W, H, dur = cfg["width"], cfg["height"], cfg["duration"]
    th = THEMES[cfg["theme"]]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    enter, leave = envelope(t, dur, tin=0.30, tout=0.20)
    if enter <= 0.001:
        return img
    scale = ease_out_back(enter) * (1 - ease_in_cubic(leave) * 0.35)
    alpha = int(255 * min(1.0, enter * 2.5) * (1 - ease_in_cubic(leave)))
    if scale <= 0.01 or alpha <= 2:
        return img

    text = cfg["text"].upper()
    f = load_font(int(H * 0.16), bold=True)

    # Draw big on its own layer, then rotate and scale, so the rotation does
    # not chew the glyph edges.
    layer = Image.new("RGBA", (int(W * 1.2), int(H * 0.5)), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    tw, th_ = text_size(ld, text, f)
    cx, cy = (layer.width - tw) // 2, (layer.height - th_) // 2
    stroke = max(3, int(H * 0.008))
    ld.text((cx, cy), text, font=f, fill=th["fg"],
            stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    # Chunky offset shadow in the accent colour: reads as a print sticker.
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((cx + stroke * 2, cy + stroke * 2), text, font=f,
                                fill=th["accent"], stroke_width=stroke,
                                stroke_fill=(0, 0, 0, 255))
    layer = Image.alpha_composite(shadow, layer)

    layer = layer.rotate(cfg.get("rotate", -8), expand=True,
                         resample=Image.BICUBIC)
    nw, nh = max(1, int(layer.width * scale)), max(1, int(layer.height * scale))
    layer = layer.resize((nw, nh), Image.LANCZOS)
    if alpha < 255:
        a = layer.getchannel("A").point(lambda v: v * alpha // 255)
        layer.putalpha(a)

    px = int(W * cfg.get("cx", 0.5)) - nw // 2
    py = int(H * cfg.get("cy", 0.34)) - nh // 2
    img.alpha_composite(layer, (px, py))
    return img


def draw_price(t: float, cfg: dict) -> Image.Image:
    W, H, dur = cfg["width"], cfg["height"], cfg["duration"]
    th = THEMES[cfg["theme"]]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    enter, leave = envelope(t, dur, tin=0.28, tout=0.20)
    if enter <= 0.001:
        return img
    scale = ease_out_back(enter, 2.0) * (1 - ease_in_cubic(leave))
    if scale <= 0.01:
        return img

    text = cfg["text"]
    f = load_font(int(H * 0.075 * scale) or 1, bold=True)
    tw, th_ = text_size(d, text, f)
    pad = int(H * 0.022 * scale)
    x = int(W * cfg.get("cx", 0.80)) - (tw + pad * 2) // 2
    y = int(H * cfg.get("cy", 0.22))
    d.rounded_rectangle([x, y, x + tw + pad * 2, y + th_ + pad * 2],
                        radius=int(H * 0.014), fill=th["accent"])
    d.text((x + pad, y + pad), text, font=f, fill=(255, 255, 255, 255))
    return img


def draw_title(t: float, cfg: dict) -> Image.Image:
    W, H, dur = cfg["width"], cfg["height"], cfg["duration"]
    th = THEMES[cfg["theme"]]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    enter, leave = envelope(t, dur, tin=0.45, tout=0.35)
    fade = ease_out_cubic(enter) * (1 - ease_in_cubic(leave))
    if fade <= 0.002:
        return img

    d.rectangle([0, 0, W, H], fill=(*th["bg"][:3], int(th["bg"][3] * fade)))

    text, sub = cfg["text"].upper(), cfg.get("sub", "")
    f_main = load_font(int(H * 0.11), bold=True)
    f_sub = load_font(int(H * 0.038), bold=True)
    tw, th_ = text_size(d, text, f_main)

    # Rise into place: 40 px of travel is enough to feel like motion without
    # drawing attention to the movement itself.
    rise = int((1 - ease_out_cubic(enter)) * H * 0.04)
    y = int(H * 0.40) + rise
    d.text(((W - tw) // 2, y), text, font=f_main,
           fill=(*th["fg"][:3], int(255 * fade)),
           stroke_width=max(2, int(H * 0.005)),
           stroke_fill=(0, 0, 0, int(255 * fade)))
    if sub:
        sw, sh = text_size(d, sub, f_sub)
        d.rectangle([(W - sw) // 2 - int(H * 0.02), y + th_ + int(H * 0.035),
                     (W + sw) // 2 + int(H * 0.02), y + th_ + int(H * 0.035) + sh + int(H * 0.024)],
                    fill=(*th["accent"][:3], int(255 * fade)))
        d.text(((W - sw) // 2, y + th_ + int(H * 0.047)), sub, font=f_sub,
               fill=(255, 255, 255, int(255 * fade)))
    return img


def draw_chapter(t: float, cfg: dict) -> Image.Image:
    W, H, dur = cfg["width"], cfg["height"], cfg["duration"]
    th = THEMES[cfg["theme"]]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    enter, leave = envelope(t, dur, tin=0.35, tout=0.25)
    p = ease_out_cubic(enter) * (1 - ease_in_cubic(leave))
    if p <= 0.002:
        return img

    band_h = int(H * 0.16)
    y = (H - band_h) // 2
    # Wipe open from the centre.
    half = int(W * 0.5 * p)
    d.rectangle([W // 2 - half, y, W // 2 + half, y + band_h], fill=th["bg"])
    d.rectangle([W // 2 - half, y + band_h - int(H * 0.008),
                 W // 2 + half, y + band_h], fill=th["accent"])

    if p > 0.55:
        text = cfg["text"].upper()
        f = load_font(int(H * 0.062), bold=True)
        tw, th_ = text_size(d, text, f)
        a = int(255 * (p - 0.55) / 0.45)
        d.text(((W - tw) // 2, y + (band_h - th_) // 2), text, font=f,
               fill=(*th["fg"][:3], a))
    return img


def draw_score(t: float, cfg: dict) -> Image.Image:
    """A row of icon images that pop in one after another, plus a label.

    The show's rating reveal: each bottle punches in with an overshoot and a
    small alternating tilt, staggered left to right, and the label lands after
    the last one. `icon` is a path to an RGBA image; `count` is how many.
    """
    W, H, dur = cfg["width"], cfg["height"], cfg["duration"]
    th = THEMES[cfg["theme"]]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    icon = cfg.get("_icon_img")
    if icon is None:
        icon = Image.open(cfg["icon"]).convert("RGBA")
        cfg["_icon_img"] = icon

    count = int(cfg.get("count", 4))
    stagger = float(cfg.get("stagger", 0.16))
    pop = 0.34
    _, leave = envelope(t, dur, tin=0.01, tout=0.28)
    fade_out = 1 - ease_in_cubic(leave)
    if fade_out <= 0.002:
        return img

    ih = int(H * cfg.get("icon_h", 0.44))
    iw = int(icon.width * ih / icon.height)
    spacing = int(iw * 1.35)
    x0 = W // 2 - spacing * (count - 1) // 2
    cy = int(H * cfg.get("cy", 0.42))

    for i in range(count):
        t_i = (t - i * stagger) / pop
        if t_i <= 0:
            continue
        scale = ease_out_back(min(1.0, t_i)) * fade_out
        if scale <= 0.01:
            continue
        nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
        b = icon.resize((nw, nh), Image.LANCZOS)
        # Alternating tilt reads as hand-placed, not templated.
        b = b.rotate(-6 if i % 2 == 0 else 6, expand=True, resample=Image.BICUBIC)
        if fade_out < 1.0:
            a = b.getchannel("A").point(lambda v: int(v * fade_out))
            b.putalpha(a)
        img.alpha_composite(b, (x0 + i * spacing - b.width // 2,
                                cy - b.height // 2))

    text = cfg.get("text", "").upper()
    t_label = (t - count * stagger - 0.1) / 0.3
    if text and t_label > 0:
        d = ImageDraw.Draw(img)
        f = load_font(int(H * 0.085), bold=True)
        tw, th_ = text_size(d, text, f)
        a = int(255 * min(1.0, t_label) * fade_out)
        rise = int((1 - ease_out_cubic(min(1.0, t_label))) * H * 0.03)
        d.text(((W - tw) // 2, int(H * 0.70) + rise), text, font=f,
               fill=(*th["fg"][:3], a),
               stroke_width=max(3, int(H * 0.007)),
               stroke_fill=(0, 0, 0, a))
    return img


def draw_news(t: float, cfg: dict) -> Image.Image:
    """A parody news-alert 'TV' that slides into a corner.

    Deliberately the SHOW'S graphic, not an imitation of a real network --
    fabricating a real broadcaster's screen is a lawyer's errand, and the
    show-branded version is funnier anyway. Red alert banner, headline,
    a slow ticker, and a blinking LIVE dot.
    """
    W, H, dur = cfg["width"], cfg["height"], cfg["duration"]
    th = THEMES[cfg["theme"]]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    enter, leave = envelope(t, dur, tin=0.40, tout=0.30)
    slide = ease_out_cubic(enter) * (1 - ease_in_cubic(leave))
    if slide <= 0.002:
        return img

    tw_box = int(W * cfg.get("scale", 0.34))
    th_box = int(tw_box * 9 / 16)
    margin = int(W * 0.025)
    x0 = W - margin - int(slide * (tw_box + margin)) + (tw_box + margin) - tw_box
    x0 = W - int(slide * (tw_box + margin))
    y0 = margin

    tv = Image.new("RGBA", (tw_box, th_box), (12, 12, 16, 245))
    d = ImageDraw.Draw(tv)
    bar_h = int(th_box * 0.22)
    d.rectangle([0, 0, tw_box, bar_h], fill=(190, 20, 20, 255))
    f_bar = load_font(int(bar_h * 0.52), bold=True)
    d.text((int(tw_box * 0.03), int(bar_h * 0.20)), cfg.get("kicker", "NEWS ALERT").upper(),
           font=f_bar, fill=(255, 255, 255, 255))
    # Blinking LIVE dot -- 1 Hz, like every cable box ever
    if int(t * 2) % 2 == 0:
        r = int(bar_h * 0.16)
        cx = tw_box - int(tw_box * 0.17)
        d.ellipse([cx - r, bar_h // 2 - r, cx + r, bar_h // 2 + r], fill=(255, 255, 255, 255))
        d.text((cx + r + 6, int(bar_h * 0.26)), "LIVE",
               font=load_font(int(bar_h * 0.38), bold=True), fill=(255, 255, 255, 255))

    # Headline, wrapped
    f_head = load_font(int(th_box * 0.115), bold=True)
    words = cfg["text"].upper().split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if text_size(d, trial, f_head)[0] > tw_box * 0.92 and cur:
            lines.append(cur); cur = wd
        else:
            cur = trial
    if cur:
        lines.append(cur)
    y = bar_h + int(th_box * 0.10)
    for ln in lines[:3]:
        d.text((int(tw_box * 0.04), y), ln, font=f_head, fill=(255, 255, 255, 255))
        y += int(th_box * 0.16)

    # Ticker: crawls right-to-left along the bottom
    tick_h = int(th_box * 0.16)
    d.rectangle([0, th_box - tick_h, tw_box, th_box], fill=th["fg"])
    f_tick = load_font(int(tick_h * 0.62), bold=True)
    tick = ("  ***  " + cfg.get("ticker", "DEVELOPING STORY").upper()) * 6
    tick_w = text_size(d, tick, f_tick)[0]
    xoff = -int((t * tw_box * 0.35) % (tick_w / 6))
    d.text((xoff, th_box - tick_h + int(tick_h * 0.14)), tick, font=f_tick,
           fill=(20, 16, 12, 255))

    d.rectangle([0, 0, tw_box - 1, th_box - 1], outline=(0, 0, 0, 255),
                width=max(2, int(th_box * 0.012)))
    img.alpha_composite(tv, (x0, y0))
    return img


RENDERERS = {
    "news": draw_news,
    "score": draw_score,
    "lower_third": draw_lower_third,
    "stamp": draw_stamp,
    "price": draw_price,
    "title": draw_title,
    "chapter": draw_chapter,
}


# -------- Encoding -----------------------------------------------------------


def render_card(cfg: dict, out_path: Path, verbose: bool = True) -> Path:
    """Render one card to an alpha WebM."""
    kind = cfg["kind"]
    if kind not in RENDERERS:
        raise SystemExit(f"unknown card kind {kind!r}; "
                         f"choose from {', '.join(sorted(RENDERERS))}")
    fn = RENDERERS[kind]
    W, H = cfg["width"], cfg["height"]
    n_frames = max(1, int(round(cfg["duration"] * FPS)))
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y", "-v", "error", "-nostdin",
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-",
        # VP9 with yuva420p is the reliable way to carry alpha through to the
        # overlay filter. An MP4 cannot do it.
        "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p",
        "-b:v", "0", "-crf", "26", "-row-mt", "1",
        str(out_path),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    try:
        for i in range(n_frames):
            frame = fn(i / FPS, cfg)
            proc.stdin.write(frame.tobytes())
    finally:
        proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit(f"ffmpeg failed encoding {out_path}")

    if verbose:
        kb = out_path.stat().st_size / 1024
        print(f"  {kind:<12} {cfg['duration']:.2f}s  {W}x{H}  -> {out_path} ({kb:.0f} KB)")
    return out_path


def normalize(cfg: dict, defaults: dict) -> dict:
    out = dict(defaults)
    out.update(cfg)
    out.setdefault("theme", "campy")
    out.setdefault("duration", 2.5)
    out.setdefault("width", 1920)
    out.setdefault("height", 1080)
    if out["theme"] not in THEMES:
        raise SystemExit(f"unknown theme {out['theme']!r}; "
                         f"choose from {', '.join(sorted(THEMES))}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Render motion-graphic overlays as alpha WebM.")
    ap.add_argument("kind", nargs="?", choices=sorted(RENDERERS),
                    help="Card type to render")
    ap.add_argument("--text", help="Main text")
    ap.add_argument("--sub", default="", help="Secondary line")
    ap.add_argument("--theme", default="campy", choices=sorted(THEMES))
    ap.add_argument("--duration", type=float, default=2.5)
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--rotate", type=float, default=-8.0, help="stamp only")
    ap.add_argument("--icon", help="score only: path to an RGBA icon image")
    ap.add_argument("--kicker", default="NEWS ALERT", help="news only: banner text")
    ap.add_argument("--ticker", default="DEVELOPING STORY", help="news only: crawl text")
    ap.add_argument("--count", type=int, default=4, help="score only: number of icons")
    ap.add_argument("--cx", type=float, help="Centre X as a fraction of width")
    ap.add_argument("--cy", type=float, help="Centre Y as a fraction of height")
    ap.add_argument("-o", "--output", type=Path, help="Output .webm path")
    ap.add_argument("--spec", type=Path,
                    help="JSON file: a list of card configs to render in one go")
    ap.add_argument("--out-dir", type=Path, default=Path("."),
                    help="Output directory when using --spec")
    args = ap.parse_args()

    if args.spec:
        spec = json.loads(args.spec.read_text())
        cards = spec if isinstance(spec, list) else spec.get("cards", [])
        defaults = {} if isinstance(spec, list) else spec.get("defaults", {})
        print(f"rendering {len(cards)} card(s)")
        results = []
        for i, card in enumerate(cards):
            cfg = normalize(card, defaults)
            name = card.get("name") or f"{cfg['kind']}_{i:02d}"
            path = render_card(cfg, args.out_dir / f"{name}.webm")
            results.append({"file": str(path), "duration": cfg["duration"],
                            "name": name})
        # Paste-ready EDL fragment; start_in_output still has to be filled in,
        # which is deliberate -- placement is an editorial decision.
        print("\noverlays fragment for the EDL:")
        print(json.dumps([{"file": r["file"], "start_in_output": 0.0,
                           "duration": r["duration"]} for r in results], indent=2))
        return

    if not args.kind or (not args.text and args.kind != "score"):
        ap.error("give a card kind and --text, or use --spec <file.json>")
    if args.kind == "score" and not args.icon:
        ap.error("score needs --icon <image.png>")

    cfg = {"kind": args.kind, "text": args.text, "sub": args.sub,
           "theme": args.theme, "duration": args.duration,
           "width": args.width, "height": args.height, "rotate": args.rotate,
           "icon": args.icon, "count": args.count,
           "kicker": args.kicker, "ticker": args.ticker}
    if args.cx is not None:
        cfg["cx"] = args.cx
    if args.cy is not None:
        cfg["cy"] = args.cy
    out = args.output or Path(f"{args.kind}.webm")
    render_card(normalize(cfg, {}), out)


if __name__ == "__main__":
    main()
