#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026.

One 1024x1024 newspaper poster, rendered with Pillow from flat vector
shapes and programmatic text (no AI image generation, so every letter
stays sharp and legible). Run:  python3 generate_poster.py  ->  entry.png

Every main story happened, or was first reported, on 23 November 2026.
Stories from other days appear only in the DATE CHECK box, with their
real dates.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (251, 247, 238)
INK = (22, 22, 22)
GREY = (96, 92, 84)
RED = (178, 32, 44)
RED_BAND = (246, 226, 224)
CARD_BG = (255, 253, 247)

DJ = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(DJ, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(DJ, "DejaVuSans.ttf")
SANS_B = os.path.join(DJ, "DejaVuSans-Bold.ttf")

# Region colours (kickers, pins, map accents).
C_TEAL = (0, 128, 128)
C_BLUE = (30, 90, 168)
C_PURPLE = (122, 63, 160)
C_AMBER = (166, 106, 0)
C_GREEN = (46, 125, 50)
C_SLATE = (55, 71, 79)
C_CRIMSON = RED

PROBLEMS = []


def note(problem):
    PROBLEMS.append(problem)


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, font, max_w, max_lines, label):
    """Wrap text; record a problem if it needs more than max_lines."""
    lines = wrap(d, text, font, max_w)
    if len(lines) > max_lines:
        note("%s needs %d lines (max %d): %r" % (label, len(lines), max_lines, text))
    return lines[:max_lines]


def draw_lines(d, x, y, lines, font, fill, leading):
    for i, line in enumerate(lines):
        d.text((x, y + i * leading), line, font=font, fill=fill)
    return y + len(lines) * leading


# ------------------------------------------------------------------ art --
def star(d, cx, cy, r_out, r_in, n, fill):
    import math
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def ill_ship(d, x, y, w, h):
    """Russian corvette hit by sea drones: hull, mast, blast, waves."""
    sea = y + h - 12
    d.line([(x, sea), (x + w, sea)], fill=C_BLUE, width=2)
    d.line([(x + 8, sea + 5), (x + w - 8, sea + 5)], fill=C_BLUE, width=1)
    d.polygon([(x + 6, sea), (x + w - 6, sea), (x + w - 16, sea - 16),
               (x + 16, sea - 16)], fill=(38, 38, 44))
    d.rectangle([x + w // 2 - 4, sea - 30, x + w // 2 + 12, sea - 16],
                fill=(110, 110, 116))
    d.line([(x + w // 2 + 4, sea - 30), (x + w // 2 + 4, sea - 42)],
           fill=(38, 38, 44), width=2)
    star(d, x + w - 22, y + h - 46, 16, 7, 8, (245, 158, 11))
    star(d, x + w - 22, y + h - 46, 9, 4, 8, (220, 38, 38))
    # two small drones
    d.ellipse([x + 10, y + h - 54, x + 18, y + h - 48], fill=INK)
    d.ellipse([x + 26, y + h - 60, x + 32, y + h - 55], fill=INK)


def ill_skyline(d, x, y, w, h):
    """City skyline, missile trail, burst."""
    base = y + h - 10
    heights = [52, 70, 44, 78, 58, 66]
    bw = w // 6
    for i, hh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 1, base - hh, bx + bw - 1, base], fill=(48, 48, 56))
        for wy in range(base - hh + 6, base - 6, 10):
            d.rectangle([bx + 4, wy, bx + 7, wy + 4], fill=(245, 200, 90))
    d.line([(x + w - 14, y + 6), (x + w - 34, y + 34)], fill=RED, width=2)
    star(d, x + w - 36, y + 36, 13, 6, 8, (245, 158, 11))
    star(d, x + w - 36, y + 36, 7, 3, 8, (220, 38, 38))


def ill_chip(d, x, y, w, h):
    """Green processor with pins and a rising arrow."""
    d.rounded_rectangle([x + 14, y + 22, x + w - 14, y + h - 14], radius=6,
                        fill=(27, 94, 32))
    d.rectangle([x + 26, y + 34, x + w - 26, y + h - 26], fill=(56, 142, 60))
    for i in range(4):
        px = x + 22 + i * 14
        d.line([(px, y + 22), (px, y + 14)], fill=(120, 120, 120), width=2)
        d.line([(px, y + h - 14), (px, y + h - 6)], fill=(120, 120, 120), width=2)
    d.text((x + w // 2 - 8, y + h // 2 - 8), "N", font=F(SANS_B, 20),
           fill=(255, 255, 255))
    d.line([(x + w - 12, y + 30), (x + w - 12, y + 10), (x + w - 2, y + 10)],
           fill=RED, width=3)
    d.polygon([(x + w - 2, y + 4), (x + w - 2, y + 14), (x + w + 4, y + 9)],
              fill=RED)


def ill_chart(d, x, y, w, h):
    """Falling market line and a gold coin."""
    d.line([(x + 8, y + 10), (x + 8, y + h - 14)], fill=GREY, width=2)
    d.line([(x + 8, y + h - 14), (x + w - 8, y + h - 14)], fill=GREY, width=2)
    pts = [(x + 10, y + 22), (x + 26, y + 30), (x + 42, y + 28),
           (x + 58, y + 48), (x + 74, y + 62)]
    d.line(pts, fill=RED, width=3)
    for px, py in pts[1:]:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    d.ellipse([x + w - 34, y + h - 40, x + w - 6, y + h - 12], fill=(212, 175, 55))
    d.ellipse([x + w - 31, y + h - 37, x + w - 9, y + h - 15],
              outline=(150, 120, 30), width=2)
    d.text((x + w - 24, y + h - 34), "B", font=F(SANS_B, 15), fill=(120, 90, 10))


def ill_fire(d, x, y, w, h):
    """Factory building with flame and smoke."""
    base = y + h - 8
    d.rectangle([x + 10, base - 44, x + w - 10, base], fill=(96, 80, 70))
    d.rectangle([x + 10, base - 52, x + w - 10, base - 44], fill=(70, 58, 50))
    for wx in range(x + 16, x + w - 16, 16):
        d.rectangle([wx, base - 34, wx + 8, base - 24], fill=(245, 200, 90))
    cx = x + w // 2
    d.polygon([(cx - 20, base - 48), (cx - 8, base - 78), (cx, base - 62),
               (cx + 10, base - 84), (cx + 22, base - 48)], fill=(234, 88, 12))
    d.polygon([(cx - 10, base - 48), (cx - 3, base - 66), (cx + 2, base - 56),
               (cx + 11, base - 48)], fill=(245, 200, 90))
    d.ellipse([x + 6, y + 4, x + 18, y + 16], fill=(180, 180, 180))
    d.ellipse([x + w - 22, y + 2, x + w - 10, y + 14], fill=(180, 180, 180))


def ill_planet(d, x, y, w, h):
    """Mercury with orbit ring and a small probe."""
    cx, cy, r = x + w // 2, y + h // 2 + 4, 30
    d.ellipse([cx - 46, cy - 16, cx + 46, cy + 16], outline=GREY, width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(176, 141, 110))
    for (ox, oy, rr) in [(-12, -8, 5), (10, 6, 7), (2, -14, 4), (14, -10, 3)]:
        d.ellipse([cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr],
                  fill=(140, 108, 82))
    d.rectangle([cx + 40, cy - 22, cx + 48, cy - 14], fill=INK)
    d.line([(cx + 44, cy - 18), (cx + 52, cy - 24)], fill=INK, width=2)


# ------------------------------------------------------------- world map --
# Land as ellipses in (lon, lat): centre, radius-x, radius-y. Coarse but
# recognisable at dot resolution.
LAND = [
    (-100, 47, 52, 20), (-96, 20, 13, 8), (-42, 74, 16, 9),
    (-60, -14, 17, 26), (17, 4, 30, 33), (47, -19, 3, 8),
    (75, 55, 92, 19), (78, 16, 11, 13), (102, 12, 11, 9),
    (45, 23, 9, 8), (134, -25, 19, 11), (-2, 54, 3, 4),
    (138, 37, 4, 7), (117, -3, 21, 5), (172, -41, 4, 6),
]

# (lon, lat, number or None, display offset dx, dy in px): the three
# numbered pins sit close together around the Mediterranean, so each is
# nudged a few pixels apart; the unnumbered dots mark Brussels, Khartoum
# and Athens. 1 Antalya, 2 Benghazi, 3 Kyiv.
PINS = [
    (30.7, 36.9, "1", 8, 14), (20.1, 32.1, "2", -16, 2),
    (30.5, 50.4, "3", 2, -14),
    (4.4, 50.8, None, 0, 0), (32.5, 15.6, None, 0, 0),
    (23.7, 38.0, None, 0, 0),
]


def draw_map(d, x0, y0, w, h):
    """Dotted world map with numbered pins."""
    lon0, lon1, lat0, lat1 = -180.0, 190.0, 78.0, -58.0

    def px(lon):
        return x0 + (lon - lon0) / (lon1 - lon0) * w

    def py(lat):
        return y0 + (lat0 - lat) / (lat0 - lat1) * h

    step_lon, step_lat = 5.8, 6.0
    lon = -177.0
    while lon <= 187.0:
        lat = 75.0
        while lat >= -55.0:
            for (clon, clat, rx, ry) in LAND:
                if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1.0:
                    gx, gy = px(lon), py(lat)
                    d.ellipse([gx - 2.2, gy - 2.2, gx + 2.2, gy + 2.2],
                              fill=(120, 130, 110))
                    break
            lat -= step_lat
        lon += step_lon
    for (lon, lat, num, dx, dy) in PINS:
        gx, gy = px(lon) + dx, py(lat) + dy
        if num is None:
            d.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=RED)
        else:
            d.ellipse([gx - 8, gy - 8, gx + 8, gy + 8], fill=RED,
                      outline=(255, 255, 255), width=2)
            f = F(SANS_B, 11)
            tw = d.textlength(num, font=f)
            d.text((gx - tw / 2, gy - 8), num, font=f, fill=(255, 255, 255))


def badge(d, x, y, num, r=9):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED,
              outline=(255, 255, 255), width=1)
    f = F(SANS_B, 11)
    tw = d.textlength(num, font=f)
    d.text((x - tw / 2, y - 8), num, font=f, fill=(255, 255, 255))


# -------------------------------------------------------------- content ---
STRIP = [
    ("15+", "KILLED IN KYIV STRIKES"),
    ("24+", "DEAD IN FACTORY FIRE"),
    ("30%", "NVIDIA SHARES SURGE"),
    ("$55,100", "BITCOIN'S LOW"),
    ("8 YRS", "TO MERCURY ORBIT"),
    ("258", "DEMOCRAT HOUSE SEATS"),
]

LEAD = {
    "kicker": "CLIMATE \u2022 ANTALYA",
    "color": C_TEAL,
    "badge": "1",
    "headline": "COP31 ENDS WITHOUT A DEAL",
    "deck": ("The longest climate summit on record closes with no agreement, "
             "after the EU rejects a text with no fossil-fuel phase-out \u2014 "
             "the first COP without a deal since 2009."),
}

GRID = [
    {"kicker": "UKRAINE \u2022 LIBYA", "color": C_BLUE, "badge": "2",
     "art": ill_ship,
     "headline": "SEA DRONES SINK RUSSIAN WARSHIP OFF LIBYA",
     "body": ("Ukraine says its sea drones sank the corvette Merkury off "
              "Benghazi. The cargo ship Angara was hit too.")},
    {"kicker": "UKRAINE \u2022 KYIV", "color": C_BLUE, "badge": "3",
     "art": ill_skyline,
     "headline": "STRIKES ON KYIV REGION KILL AT LEAST 15",
     "body": ("At least 15 are killed around Kyiv; a missile kills two in "
              "Kryvyi Rih and a drone brings down a block of flats.")},
    {"kicker": "UNITED STATES \u2022 TECH", "color": C_PURPLE, "badge": None,
     "art": ill_chip,
     "headline": "HUANG BACK AS NVIDIA CHIEF; SHARES SOAR 30%",
     "body": ("Nvidia's board restores Jensen Huang as chief executive; "
              "Trump says he urged the board. Shares jump about 30%.")},
    {"kicker": "MARKETS", "color": C_AMBER, "badge": None,
     "art": ill_chart,
     "headline": "BITCOIN SINKS TO $55,100 IN AI SELL-OFF",
     "body": ("AI sell-off deepens in Asia. Bitcoin falls to its lowest "
              "since September 2024, then recovers to about $61,000.")},
    {"kicker": "INDONESIA", "color": C_GREEN, "badge": None,
     "art": ill_fire,
     "headline": "FACTORY FIRE KILLS AT LEAST 24 IN INDONESIA",
     "body": ("A fire at a candy factory kills at least 24 people, with "
              "about 30 missing.")},
    {"kicker": "SPACE", "color": C_SLATE, "badge": None,
     "art": ill_planet,
     "headline": "BEPICOLOMBO REACHES MERCURY AFTER 8 YEARS",
     "body": ("The European-Japanese probe enters orbit around Mercury "
              "after an eight-year journey.")},
]

BRIEFS_A = [
    ("BELGIUM", C_BLUE, "Austerity strike grounds almost all flights in Brussels."),
    ("IRAN", C_CRIMSON, "US sanctions hit a shadow-banking network of 2 dozen firms."),
    ("SUDAN", C_CRIMSON, "A drone strikes a home and a UN building in Khartoum."),
    ("HEALTH", C_TEAL, "NHS begins AI breast-cancer screening trial in 700,000 women."),
    ("GREECE", C_BLUE, "Acropolis Museum reopens; Mitsotakis wants Marbles back."),
    ("SCIENCE", C_PURPLE, "Anthropic says AI helped prove the Riemann hypothesis."),
    ("EUROPE", C_BLUE, "EU proposes sanctions on 60 banks, crypto and 70 shadow ships."),
    ("FINLAND", C_BLUE, "Summons Russia's envoy over airspace breach and Sparta II."),
    ("IRAN", C_CRIMSON, "Singer Parastoo Ahmadi and four band members flogged in Qom."),
    ("COLOMBIA", C_GREEN, "Drone hits police HQ in C\u00facuta; 60 homes damaged."),
    ("UNITED STATES", C_SLATE, "Amtrak train derails in Louisiana after hitting a truck."),
]

BRIEFS_B = [
    ("EUROPE", C_BLUE, "Eurozone inflation stands at 4.0%."),
    ("POLAND", C_BLUE, "NATO holds an emergency meeting over Poland."),
    ("UNITED STATES", C_SLATE, "Democrats win 258 House seats, most since 1992."),
    ("IRAN", C_CRIMSON, "Trump: Iran launches its heaviest missile week in over a year."),
    ("NEPAL", C_GREEN, "India gives \u20ac1.4bn in aid after the floods."),
    ("NIGERIA", C_GREEN, "Presidential villa hit by a water and power outage."),
    ("IRAN", C_CRIMSON, "Tehran threatens to counter a Hormuz blockade."),
    ("HUNGARY", C_BLUE, "The prime minister visits Transcarpathia."),
    ("UNITED STATES", C_SLATE, "NYT: US intel tracked Alice Huang's China contacts."),
    ("UNITED KINGDOM", C_BLUE, "Rising prices are voters' top concern."),
    ("RUSSIA", C_BLUE, "Cargo ship Sparta II hit by drones in the Gulf of Finland."),
]

DATE_CHECK = [
    ("Chapo Isidro arrested in Mexico", "21 NOV"),
    ("Wall Street sell-off", "20 NOV"),
    ("Shenzhen declaration", "19 NOV"),
    ("ICJ Rohingya ruling", "19 NOV"),
]


# --------------------------------------------------------------- drawing --
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 30                      # side margin
    CW = W - 2 * MX              # content width = 964

    # Masthead.
    f_mast = F(SERIF_B, 46)
    mast = "THE WORLD IN ONE DAY"
    mw = d.textlength(mast, font=f_mast)
    check = mw <= CW
    if not check:
        note("masthead too wide: %.1f > %d" % (mw, CW))
    d.text(((W - mw) / 2, 14), mast, font=f_mast, fill=INK)
    d.line([(MX, 76), (W - MX, 76)], fill=INK, width=2)
    d.line([(MX, 80), (W - MX, 80)], fill=INK, width=1)

    # Date, big and red.
    f_date = F(SERIF_B, 34)
    date = "MONDAY, 23 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 88), date, font=f_date, fill=RED)

    # Sub-line.
    f_sub = F(SANS_B, 12)
    sub = "ONE DAY \u2022 SIX REGIONS \u2022 THE WORLD'S NEWS IN ONE IMAGE"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 132), sub, font=f_sub, fill=INK)

    # Big-number strip.
    sy, sh = 152, 50
    d.rectangle([MX, sy, W - MX, sy + sh], fill=RED_BAND)
    d.line([(MX, sy), (W - MX, sy)], fill=RED, width=2)
    d.line([(MX, sy + sh), (W - MX, sy + sh)], fill=RED, width=2)
    cell = CW / len(STRIP)
    f_num = F(SANS_B, 27)
    f_lab = F(SANS_B, 10)
    for i, (num, lab) in enumerate(STRIP):
        cx = MX + cell * i + cell / 2
        nw = d.textlength(num, font=f_num)
        if nw > cell - 8:
            note("strip number too wide: %r (%.1f)" % (num, nw))
        d.text((cx - nw / 2, sy + 4), num, font=f_num, fill=RED)
        lab_lines = wrap(d, lab, f_lab, cell - 10)
        if len(lab_lines) > 1:
            note("strip label wraps: %r" % lab)
        ly = sy + 34
        for line in lab_lines:
            lw = d.textlength(line, font=f_lab)
            d.text((cx - lw / 2, ly), line, font=f_lab, fill=INK)
            ly += 12
        if i:
            x = MX + cell * i
            d.line([(x, sy + 8), (x, sy + sh - 8)], fill=(200, 160, 158), width=1)

    # Lead story: text left, dotted world map right.
    ly = 212
    d.rectangle([MX, ly, W - MX, ly + 140], fill=CARD_BG, outline=(200, 194, 178))
    f_kick = F(SANS_B, 12)
    kx = MX + 14
    d.text((kx, ly + 10), LEAD["kicker"], font=f_kick, fill=LEAD["color"])
    kw = d.textlength(LEAD["kicker"], font=f_kick)
    badge(d, kx + kw + 18, ly + 17, LEAD["badge"])
    f_head = F(SANS_B, 28)
    head_lines = fit_lines(d, LEAD["headline"], f_head, 600, 1, "lead headline")
    draw_lines(d, kx, ly + 32, head_lines, f_head, INK, 33)
    f_deck = F(SANS, 13)
    deck_lines = fit_lines(d, LEAD["deck"], f_deck, 600, 3, "lead deck")
    draw_lines(d, kx, ly + 70, deck_lines, f_deck, INK, 17)
    f_maplab = F(SANS_B, 10)
    maplab = "WHERE IT HAPPENED"
    mlw = d.textlength(maplab, font=f_maplab)
    d.text((W - MX - 14 - mlw, ly + 10), maplab, font=f_maplab, fill=GREY)
    draw_map(d, 668, ly + 30, 312, 104)

    # Grid: 2 columns x 3 rows of main stories.
    gy = 364
    card_w, card_h, gap = 464, 118, 8
    f_h = F(SANS_B, 17)
    f_b = F(SANS, 12)
    for i, story in enumerate(GRID):
        cx = MX + (i % 2) * (card_w + gap)
        cy = gy + (i // 2) * (card_h + gap)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=CARD_BG,
                    outline=(200, 194, 178))
        tx = cx + 12
        d.text((tx, cy + 8), story["kicker"], font=f_kick, fill=story["color"])
        if story["badge"]:
            kw = d.textlength(story["kicker"], font=f_kick)
            badge(d, tx + kw + 16, cy + 15, story["badge"], r=8)
        art_w, art_h = 84, 100
        ax, ay = cx + card_w - art_w - 8, cy + 9
        story["art"](d, ax, ay, art_w, art_h)
        text_w = card_w - art_w - 12 - 14
        h_lines = fit_lines(d, story["headline"], f_h, text_w, 2,
                            "headline %d" % (i + 1))
        draw_lines(d, tx, cy + 28, h_lines, f_h, INK, 20)
        b_lines = fit_lines(d, story["body"], f_b, text_w, 2, "body %d" % (i + 1))
        draw_lines(d, tx, cy + 70, b_lines, f_b, INK, 15)

    # DATE CHECK box: non-23-Nov stories, honestly dated.
    dy = gy + 3 * card_h + 2 * gap + 10
    dh = 52
    d.rectangle([MX, dy, W - MX, dy + dh], fill=RED_BAND, outline=RED, width=2)
    f_dc = F(SANS_B, 12)
    f_dci = F(SANS, 12)
    title = "DATE CHECK \u2014 WHAT WE LEFT OUT:"
    d.text((MX + 12, dy + 6), title, font=f_dc, fill=RED)
    tw = d.textlength(title, font=f_dc)
    line1 = ("  \u2715 " + DATE_CHECK[0][0] + " \u2014 " + DATE_CHECK[0][1] +
             "   \u00b7   \u2715 " + DATE_CHECK[1][0] + " \u2014 " + DATE_CHECK[1][1])
    line2 = ("  \u2715 " + DATE_CHECK[2][0] + " \u2014 " + DATE_CHECK[2][1] +
             "   \u00b7   \u2715 " + DATE_CHECK[3][0] + " \u2014 " + DATE_CHECK[3][1])
    for ln, yy in ((line1, dy + 6), (line2, dy + 28)):
        if d.textlength(ln, font=f_dci) > CW - tw - 30:
            note("DATE CHECK line too wide: %r" % ln)
        d.text((MX + 12 + tw, yy), ln, font=f_dci, fill=INK)

    # Briefs, two columns, one line each.
    by = dy + dh + 12
    f_sec = F(SANS_B, 11)
    d.text((MX, by), "IN BRIEF", font=f_sec, fill=RED)
    d.line([(MX + 74, by + 6), (W - MX, by + 6)], fill=(200, 194, 178), width=1)
    f_br = F(SANS, 12)
    f_bk = F(SANS_B, 12)
    lead = 14
    for col, briefs in enumerate((BRIEFS_A, BRIEFS_B)):
        bx = MX + col * (card_w + gap)
        for j, (kick, color, text) in enumerate(briefs):
            yy = by + 20 + j * lead
            d.text((bx, yy), kick, font=f_bk, fill=color)
            kw = d.textlength(kick, font=f_bk)
            rest = " \u2014 " + text
            if d.textlength(kick + rest, font=f_br) > card_w:
                note("brief too wide: %r" % (kick + rest))
            d.text((bx + kw, yy), rest, font=f_br, fill=INK)

    # Footer.
    f_foot = F(SANS, 10)
    foot = ("Events happened or were first reported on 23 November 2026, "
            "unless dated otherwise. Drawn from wire reports.")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 988), foot, font=f_foot, fill=GREY)

    img.save(OUT, format="PNG")
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))
    if PROBLEMS:
        print("PROBLEMS (%d):" % len(PROBLEMS))
        for p in PROBLEMS:
            print("  - " + p)
        return 1
    print("layout: no overflow problems")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
