#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page (1024x1024 PNG).

Deterministic: fixed strings, fixed layout, fixed fonts, no time, no random.
Run: python3 gen_image.py  -> writes entry.png next to this script (and ../entry.png).
Layout is flowed top-to-bottom with returned y positions; asserts guard overlaps.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 26, 43)
NAVY = (18, 33, 61)
RED = (178, 28, 28)
GOLD = (201, 162, 39)
GREY = (90, 90, 90)
RULE = (180, 172, 155)
SEA = (186, 214, 228)
LAND = (232, 220, 190)
BODY_GREY = (60, 60, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x, y, w, fill=RULE, width=2):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 36

# ---------- Masthead ----------
d.rectangle([0, 0, W, 112], fill=NAVY)
d.text((W // 2, 14), "THE WORLD TODAY", font=font(SERIF, 62),
       fill=(247, 243, 234), anchor="ma")
d.text((W // 2, 84), "WEDNESDAY, 18 NOVEMBER 2026  ·  THE DAY IN ONE PAGE",
       font=font(SANS_B, 17), fill=GOLD, anchor="ma")
d.rectangle([0, 112, W, 118], fill=RED)

# ---------- Lead story: Gulf (left) + schematic map (right) ----------
y = 136
d.text((M, y), "GULF CRISIS — LEAD STORY", font=font(SANS_B, 20), fill=RED)
y += 30
y = para(d, M, y, "U.S. STRIKES IRAN AS GULF WAR ESCALATES",
         font(SERIF, 42), 620, 50)
y += 8
y = para(d, M, y,
         "U.S. jets hit a Revolutionary Guard missile site on Qeshm Island and say "
         "they sank five Iranian tankers — as Iran fired drones at a U.S. radar base "
         "in Bahrain and at Kuwait, and missiles at a base in Jordan.",
         font(SANS, 20), 620, 28)
assert y <= 420, f"lead overran: {y}"
rule(d, M, 428, 620)

# Schematic Gulf map
mx, my, mw, mh = 692, 136, 296, 306
d.rectangle([mx, my, mx + mw, my + mh], outline=INK, width=2, fill=(255, 255, 255))
d.text((mx + mw // 2, my + 8), "THE GULF, 18 NOV", font=font(SANS_B, 16),
       fill=INK, anchor="ma")
d.polygon([(mx + 20, my + 190), (mx + 150, my + 150), (mx + 276, my + 120),
           (mx + 276, my + 280), (mx + 20, my + 280)], fill=SEA)
d.polygon([(mx + 20, my + 40), (mx + 276, my + 40), (mx + 276, my + 120),
           (mx + 150, my + 150), (mx + 20, my + 190)], fill=LAND)
d.text((mx + 30, my + 52), "IRAN", font=font(SANS_B, 15), fill=INK)
d.text((mx + mw - 10, my + 210), "GULF OF OMAN", font=font(SANS_B, 12),
       fill=(40, 80, 110), anchor="ra")
d.text((mx + 34, my + 250), "STRAIT OF HORMUZ", font=font(SANS_B, 11), fill=(40, 80, 110))
places = [("Qeshm I.", 150, 150), ("Bahrain", 96, 205), ("Kuwait", 60, 168),
          ("Jordan base", 44, 96)]
for name, px, py in places:
    d.ellipse([mx + px - 6, my + py - 6, mx + px + 6, my + py + 6], fill=RED)
    d.text((mx + px + 10, my + py - 9), name, font=font(SANS_B, 13), fill=INK)
d.text((mx + 12, my + mh - 22), "Schematic — strikes & drone attacks",
       font=font(SANS, 11), fill=GREY)

# ---------- Divider under lead ----------
rule(d, M, 460, W - 2 * M, fill=INK, width=3)

# ---------- Row 2: two stories ----------
y2 = 478
d.text((M, y2), "WAR IN UKRAINE", font=font(SANS_B, 20), fill=RED)
y2l = para(d, M, y2 + 28, "KERCH BRIDGE HIT FOR A SECOND NIGHT",
           font(SERIF, 25), 460, 31)
y2l = para(d, M, y2l + 8,
           "Ukraine struck the bridge to occupied Crimea again; part of its road span "
           "fell into the strait.",
           font(SANS, 18), 460, 25)
x3 = 524
d.text((x3, y2), "DIPLOMACY", font=font(SANS_B, 20), fill=RED)
y2r = para(d, x3, y2 + 28, "XI, PUTIN AND TRUMP MEET IN SHENZHEN",
           font(SERIF, 25), 464, 31)
y2r = para(d, x3, y2r + 8,
           "The three leaders meet Thursday at APEC in China; Trump is in Manila "
           "first for Quad talks.",
           font(SANS, 18), 464, 25)
assert max(y2l, y2r) <= 640, f"row2 overran: {y2l} {y2r}"
rule(d, M, 648, W - 2 * M, fill=INK, width=3)

# ---------- Row 3: four cards ----------
cards = [
    ("U.S. POLITICS", "PELTOLA WINS ALASKA",
     "Democrat Mary Peltola takes the Senate seat, giving her party 56 seats."),
    ("GAZA", "WINTER THREATENS GAZA",
     "The UN warns of more deaths from cold as 1.7 million remain displaced."),
    ("CLIMATE", "COP31 IN DECISIVE PHASE",
     "Negotiators in Antalya work through 144 disputed items; talks end Friday."),
    ("HEALTH", "EBOLA SURGE IN CONGO",
     "Cases in DR Congo more than doubled: 11,000+ cases, 5,400 dead."),
]
cw, gap = 226, 8
y3 = 666
for i, (kick, head, body) in enumerate(cards):
    x = M + i * (cw + gap)
    d.rectangle([x, y3, x + cw, y3 + 168], outline=RULE, width=1)
    d.rectangle([x, y3, x + cw, y3 + 6], fill=RED)
    d.text((x + 12, y3 + 16), kick, font=font(SANS_B, 15), fill=RED)
    hy = para(d, x + 12, y3 + 42, head, font(SERIF, 18), cw - 24, 23)
    by = para(d, x + 12, hy + 8, body, font(SANS, 14), cw - 24, 18, fill=BODY_GREY)
    assert by <= y3 + 164, f"card {i} overran: {by} vs {y3 + 164}"

# ---------- Also today strip ----------
y4 = 852
rule(d, M, y4, W - 2 * M, fill=INK, width=3)
d.text((M, y4 + 12), "ALSO TODAY", font=font(SANS_B, 19), fill=RED)
items = [
    "Category 5 Cyclone Xavier hits the Northern Cook Islands",
    "Russian military plane crashes in Kemerovo — 19 dead",
    "146,000 protest across France over living costs",
    "U.S. measles cases hit a 40-year high",
    "Robert Pattinson named the new James Bond",
    "5.3-magnitude quake shakes Romania",
]
yy = para(d, M, y4 + 44, "  ·  ".join(items), font(SANS, 17), W - 2 * M, 25)
assert yy <= 972, f"also-today overran: {yy}"

# ---------- Footer ----------
rule(d, M, 976, W - 2 * M)
d.text((M, 984), "Compiled from Reuters, AP, Al Jazeera, BBC and UN reports  ·  Wednesday 18 November 2026",
       font=font(SANS, 14), fill=GREY)
d.text((W - M, 984), "ONE PAGE · ONE DAY", font=font(SANS_B, 14), fill=GREY, anchor="ra")

out1 = os.path.join(HERE, "entry.png")
out2 = os.path.join(os.path.dirname(HERE), "entry.png")
img.save(out1, "PNG")
img.save(out2, "PNG")
print("wrote", out1, os.path.getsize(out1), "bytes")
print("wrote", out2, os.path.getsize(out2), "bytes")
