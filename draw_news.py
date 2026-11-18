#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

One clear newspaper composition, built to stay legible when shrunk to ~300px:
few stories, big headlines, short decks, no tiny body text.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 239)
INK = (18, 18, 18)
RED = (176, 30, 30)
GRAY = (233, 228, 218)
NAVY = (16, 40, 74)
BLUE = (28, 78, 158)
GOLD = (255, 193, 37)
ORANGE = (255, 122, 26)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star_points(cx, cy, r_out, r_in, n=5, rot=-90.0):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_flag_china(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon(star_points(x + w * 0.20, y + h * 0.30, h * 0.17, h * 0.07), fill=GOLD)
    for sx, sy in [(0.40, 0.14), (0.48, 0.30), (0.40, 0.46), (0.30, 0.52)]:
        d.polygon(star_points(x + w * sx, y + h * sy, h * 0.06, h * 0.025), fill=GOLD)


def draw_flag_russia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 43, 30))
    d.rectangle([x, y, x + w, y + h], outline=(120, 120, 120), width=1)


def draw_flag_usa(d, x, y, w, h):
    stripe = h / 7.0
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=(178, 34, 52))
    d.rectangle([x, y, x + w * 0.42, y + 4 * stripe], fill=(60, 59, 110))
    for row in range(3):
        for col in range(5):
            cx = x + w * 0.05 + col * w * 0.075
            cy = y + stripe * 0.6 + row * stripe * 1.05
            d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=(120, 120, 120), width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)

    # Masthead
    mast = font(SERIF, 82)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=mast)) / 2, 30), title, font=mast, fill=INK)

    # Date bar: the day, unmissable
    d.rectangle([28, 126, 996, 176], fill=INK)
    date_font = font(SANSB, 38)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=date_font)) / 2, 133), date, font=date_font, fill=(255, 255, 255))
    d.line([28, 184, 996, 184], fill=RED, width=4)

    # ---- Lead story ----
    kick = font(SANSB, 23)
    d.text((28, 198), "SUMMIT IN SHENZHEN  •  APEC", font=kick, fill=RED)
    head = font(SERIF, 54)
    y = 230
    for line in wrap(d, "THREE LEADERS MEET IN SHENZHEN", head, 600):
        d.text((28, y), line, font=head, fill=INK)
        y += 62
    deck = font(SANS, 26)
    y += 6
    for line in wrap(d, "Xi and Putin open talks; Trump joins for a rare three-way summit on trade and war.", deck, 600):
        d.text((28, y), line, font=deck, fill=INK)
        y += 34

    # Flags panel: the three leaders' countries
    d.rectangle([660, 198, 996, 468], fill=GRAY, outline=INK, width=2)
    cap = font(SANSB, 20)
    label = "XI  •  PUTIN  •  TRUMP"
    d.text((660 + (336 - d.textlength(label, font=cap)) / 2, 210), label, font=cap, fill=INK)
    flags = [(draw_flag_china, "CHINA"), (draw_flag_russia, "RUSSIA"), (draw_flag_usa, "USA")]
    fy = 242
    for draw_fn, name in flags:
        draw_fn(d, 700, fy, 150, 56)
        d.text((862, fy + 16), name, font=font(SANSB, 20), fill=INK)
        fy += 72

    # ---- Divider ----
    d.line([28, 488, 996, 488], fill=INK, width=3)

    # ---- Row 2: two stories ----
    # Gulf strikes
    d.text((28, 504), "MIDDLE EAST  •  GULF", font=kick, fill=RED)
    h2 = font(SERIF, 36)
    d.text((28, 532), "GULF STRIKES", font=h2, fill=INK)
    deck2 = font(SANS, 24)
    y = 582
    for line in wrap(d, "US jets hit Qeshm Island; Iran drones hit Bahrain and Kuwait.", deck2, 452):
        d.text((28, y), line, font=deck2, fill=INK)
        y += 31
    d.rectangle([28, 668, 480, 712], fill=NAVY)
    d.polygon(star_points(64, 690, 20, 8, n=8), fill=ORANGE)
    d.polygon(star_points(64, 690, 11, 5, n=8), fill=GOLD)
    gulf = font(SANSB, 19)
    d.text((96, 677), "QESHM  •  BAHRAIN  •  KUWAIT", font=gulf, fill=(255, 255, 255))

    # Kerch bridge
    d.text((528, 504), "UKRAINE  •  CRIMEA", font=kick, fill=RED)
    d.text((528, 532), "KERCH BRIDGE FALLS", font=h2, fill=INK)
    y = 582
    for line in wrap(d, "Second day of attacks collapses a span into the strait.", deck2, 452):
        d.text((528, y), line, font=deck2, fill=INK)
        y += 31
    # bridge pictogram: deck with a broken gap, falling piece, waves
    bx, by = 528, 656
    d.rectangle([bx, by, bx + 452, by + 56], fill=GRAY, outline=INK, width=1)
    d.rectangle([bx + 60, by + 6, bx + 72, by + 34], fill=INK)
    d.rectangle([bx + 368, by + 6, bx + 380, by + 34], fill=INK)
    d.line([bx + 10, by + 34, bx + 200, by + 34], fill=INK, width=5)
    d.line([bx + 252, by + 34, bx + 442, by + 34], fill=INK, width=5)
    d.polygon([(bx + 208, by + 38), (bx + 244, by + 38), (bx + 236, by + 48), (bx + 216, by + 48)], fill=INK)
    d.polygon(star_points(bx + 226, by + 30, 12, 5, n=8), fill=ORANGE)
    for wx in range(bx + 8, bx + 440, 34):
        d.arc([wx, by + 44, wx + 30, by + 56], 180, 360, fill=BLUE, width=2)
    d.line([512, 504, 512, 712], fill=(170, 165, 155), width=1)

    # ---- Divider ----
    d.line([28, 730, 996, 730], fill=INK, width=3)

    # ---- Row 3: three stories ----
    cols = [
        (28, "USA  •  SENATE", "PELTOLA WINS ALASKA", "Democrats take a 56–44 Senate majority."),
        (360, "HEALTH  •  CONGO", "EBOLA PASSES 11,000", "Cases double in three months; 5,400 dead."),
        (692, "SPACE  •  VOYAGER 1", "ONE LIGHT-DAY OUT", "Voyager 1 is the first object 16 billion miles out."),
    ]
    h3 = font(SERIF, 31)
    deck3 = font(SANS, 22)
    small_kick = font(SANSB, 20)
    for x, kicker, headline, text in cols:
        d.text((x, 746), kicker, font=small_kick, fill=RED)
        y = 774
        for line in wrap(d, headline, h3, 300):
            d.text((x, y), line, font=h3, fill=INK)
            y += 38
        y += 4
        for line in wrap(d, text, deck3, 300):
            d.text((x, y), line, font=deck3, fill=INK)
            y += 29
    d.line([344, 746, 344, 900], fill=(170, 165, 155), width=1)
    d.line([676, 746, 676, 900], fill=(170, 165, 155), width=1)

    # ---- Bottom ticker ----
    d.rectangle([28, 920, 996, 988], fill=INK)

    def fit_font(text, start, max_w):
        size = start
        while size > 12 and d.textlength(text, font=font(SANSB, size)) > max_w:
            size -= 1
        return font(SANSB, size)

    t1 = "ALSO: CYCLONE XAVIER HITS COOK ISLANDS  •  US LOSES MEASLES-FREE STATUS"
    t2 = "STOCKS FALL ON GULF TENSIONS  •  WORLD COURT TO RULE ON MYANMAR"
    f1, f2 = fit_font(t1, 21, 940), fit_font(t2, 21, 940)
    d.text(((W - d.textlength(t1, font=f1)) / 2, 928), t1, font=f1, fill=(255, 255, 255))
    d.text(((W - d.textlength(t2, font=f2)) / 2, 956), t2, font=f2, fill=(255, 255, 255))

    foot = font(SANS, 15)
    f = "THE WORLD TODAY  •  ONE DAY, IN ONE PAGE"
    d.text(((W - d.textlength(f, font=foot)) / 2, 994), f, font=foot, fill=(120, 115, 105))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
