#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026 (v2).

One 1024x1024 newspaper poster, rendered with Pillow from flat vector
shapes and programmatic text (no AI image generation, so every letter
stays sharp and legible). Run:  python3 generate_poster.py  ->  entry.png

v2 rebuilds v1 (commit 9155506) because v1's lead stories were dated
wrong: COP31 ended Sun 22 Nov, BepiColombo reached Mercury Sat 21 Nov,
Bitcoin's $55,100 low was Sat 21 Nov. v2 verifies EVERY story against a
primary source (see test-report-v2.md); stories from other days appear
only in the DATE CHECK box, with their real dates.

Layout v2 (structure changed from v1, which is why this file was
rewritten rather than patched): 3 illustrated leads, a world map with
numbered pins + a UTC timeline, a 6-card grid, an expanded 9-item
DATE CHECK, and 26 one-line briefs (35 stories, 7 regions).
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


def ill_rise(d, x, y, w, h):
    """Rising market line with arrowhead (Nvidia +31.5%)."""
    d.line([(x + 8, y + 8), (x + 8, y + h - 12)], fill=GREY, width=2)
    d.line([(x + 8, y + h - 12), (x + w - 6, y + h - 12)], fill=GREY, width=2)
    pts = [(x + 12, y + h - 22), (x + 26, y + h - 30),
           (x + 40, y + h - 44), (x + 54, y + h - 58)]
    d.line(pts, fill=C_GREEN, width=3)
    for px, py in pts:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=C_GREEN)
    ex, ey = pts[-1]
    d.polygon([(ex + 2, ey - 10), (ex + 10, ey - 2), (ex - 2, ey - 2)],
              fill=C_GREEN)
    d.text((x + w - 34, y + h - 24), "+31%", font=F(SANS_B, 13),
           fill=C_GREEN)


def ill_plane(d, x, y, w, h):
    """Grounded airliner: plane on the runway under a red no-sign."""
    cx, cy = x + w // 2, y + h // 2
    d.line([(x + 4, y + h - 10), (x + w - 4, y + h - 10)], fill=GREY, width=2)
    # fuselage
    d.rounded_rectangle([x + 8, cy - 8, x + w - 14, cy + 6], radius=6,
                        fill=(200, 205, 210))
    d.polygon([(x + w - 14, cy - 8), (x + w - 2, cy - 1), (x + w - 14, cy + 6)],
              fill=(200, 205, 210))
    # tail fin + wing
    d.polygon([(x + 12, cy - 8), (x + 18, cy - 24), (x + 26, cy - 8)],
              fill=(30, 90, 168))
    d.polygon([(x + w // 2 - 4, cy + 6), (x + w // 2 + 16, cy + 16),
               (x + w // 2 + 4, cy + 6)], fill=(120, 125, 130))
    for wx in range(x + 16, x + w - 22, 9):
        d.rectangle([wx, cy - 5, wx + 4, cy - 1], fill=(30, 90, 168))
    d.ellipse([x + 20, cy + 6, x + 25, cy + 11], fill=INK)
    d.ellipse([x + w - 26, cy + 6, x + w - 21, cy + 11], fill=INK)
    # red no-sign over the plane
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=RED, width=4)
    d.line([(cx - 21, cy + 21), (cx + 21, cy - 21)], fill=RED, width=4)


def ill_nato(d, x, y, w, h):
    """NATO compass rose on a dark-blue disc, three red impact dots."""
    cx, cy = x + w // 2, y + h // 2 - 6
    d.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], fill=(18, 48, 94))
    d.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], outline=(255, 255, 255),
              width=2)
    star(d, cx, cy, 24, 6, 4, (255, 255, 255))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(18, 48, 94))
    for i, dx in enumerate((-16, 0, 16)):
        d.ellipse([cx + dx - 3, y + h - 12, cx + dx + 3, y + h - 6],
                  fill=RED)


def ill_btc(d, x, y, w, h):
    """Bitcoin rebound: V-shaped line (low, then recovery) + gold coin."""
    d.line([(x + 8, y + 10), (x + 8, y + h - 14)], fill=GREY, width=2)
    d.line([(x + 8, y + h - 14), (x + w - 8, y + h - 14)], fill=GREY, width=2)
    pts = [(x + 10, y + 24), (x + 26, y + 46), (x + 42, y + 58),
           (x + 58, y + 40), (x + 74, y + 22)]
    d.line(pts, fill=C_GREEN, width=3)
    for px, py in pts[1:]:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=C_GREEN)
    d.ellipse([x + w - 34, y + h - 40, x + w - 6, y + h - 12], fill=(212, 175, 55))
    d.ellipse([x + w - 31, y + h - 37, x + w - 9, y + h - 15],
              outline=(150, 120, 30), width=2)
    d.text((x + w - 24, y + h - 34), "B", font=F(SANS_B, 15), fill=(120, 90, 10))


def ill_bank(d, x, y, w, h):
    """Bank building under a red slash (SWIFT cut-off)."""
    base = y + h - 10
    d.polygon([(x + 8, base - 52), (x + w // 2, base - 66),
               (x + w - 8, base - 52)], fill=(70, 70, 78))
    for cx in (x + 18, x + w // 2, x + w - 18):
        d.rectangle([cx - 4, base - 50, cx + 4, base - 12], fill=(70, 70, 78))
    d.rectangle([x + 8, base - 12, x + w - 8, base - 6], fill=(70, 70, 78))
    d.rectangle([x + 4, base - 6, x + w - 4, base], fill=(70, 70, 78))
    d.line([(x + 6, y + 6), (x + w - 6, y + h - 16)], fill=RED, width=4)


def ill_dollar(d, x, y, w, h):
    """Dollar sign in a circle, crossed out (sanctions)."""
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=C_SLATE, width=3)
    d.text((cx - 9, cy - 14), "$", font=F(SANS_B, 26), fill=C_SLATE)
    d.line([(cx - 19, cy + 19), (cx + 19, cy - 19)], fill=RED, width=4)


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

# (lon, lat, number or None, dx, dy): numbered pins 1-3 leads, 4-9 grid;
# unnumbered dots mark brief locations. European pins are nudged apart.
PINS = [
    (-122.0, 37.4, "1", 0, -12),    # Nvidia, Santa Clara
    (4.4, 50.8, "2", -16, 10),      # Brussels
    (21.0, 52.2, "3", 8, -4),       # Warsaw
    (20.1, 32.1, "4", -14, -8),     # Benghazi
    (-74.0, 40.7, "5", -18, -10),   # New York (Bitcoin)
    (7.7, 48.6, "6", 20, 14),       # Strasbourg
    (-77.0, 38.9, "7", 16, 12),     # Washington
    (30.5, 50.4, "8", 14, 10),      # Kyiv
    (106.8, -6.2, "9", 0, 0),       # Jakarta
    (-0.1, 51.5, None, -8, -8),     # London
    (23.7, 38.0, None, 14, 10),    # Athens
    (32.5, 15.6, None, 8, 8),      # Khartoum
    (77.2, 28.6, None, 0, 0),      # New Delhi
    (-72.5, 7.9, None, 0, 0),      # Cucuta
    (44.5, 40.2, None, 12, -10),   # Yerevan
    (116.4, 39.9, None, 0, 0),     # Beijing
    (149.1, -35.3, None, 0, 0),    # Canberra
]


def draw_map(d, x0, y0, w, h, dot_r=2.2):
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
                    d.ellipse([gx - dot_r, gy - dot_r, gx + dot_r, gy + dot_r],
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
    ("+31.5%", "NVIDIA SHARES SURGE"),
    ("404", "BELGIUM FLIGHTS AXED"),
    ("24", "DEAD IN FACTORY FIRE"),
    ("258", "DEMOCRAT HOUSE SEATS"),
    ("60", "BANKS OFF SWIFT"),
    ("$61,271", "BITCOIN'S CLOSE"),
]

LEADS = [
    {"kicker": "UNITED STATES \u2022 TECH", "color": C_PURPLE, "badge": "1",
     "art": ill_rise,
     "headline": "HUANG IS BACK; NVIDIA SOARS 31%",
     "deck": ("Board reinstates Jensen Huang 11 days after he quit. "
              "Shares +31.5% to $165.05, adding ~$950bn.")},
    {"kicker": "BELGIUM \u2022 STRIKE", "color": C_BLUE, "badge": "2",
     "art": ill_plane,
     "headline": "BELGIUM GROUNDED: 404 FLIGHTS AXED",
     "deck": ("Controllers join a national strike; airspace shuts "
              "07:00\u201321:00. Brussels axes 404 of 429 flights.")},
    {"kicker": "NATO \u2022 POLAND", "color": C_BLUE, "badge": "3",
     "art": ill_nato,
     "headline": "NATO MEETS AFTER MISSILES HIT POLAND",
     "deck": ("Three Russian Kh-101 missiles fell in Poland on Friday. "
              "NATO meets; AWACS head to Poland.")},
]

TIMELINE = [
    ("06:00", "Belgium airspace shuts; 404 flights axed"),
    ("07:44", "Bitcoin back above $61,000"),
    ("14:00", "Nvidia reinstates Huang; shares soar"),
    ("15:58", "Finland summons Russia's envoy"),
    ("17:31", "EU unveils 22nd sanctions package"),
    ("21:00", "Wall St closes: NVDA +31.5%, S&P +4.7%"),
]

GRID = [
    {"kicker": "UKRAINE \u2022 LIBYA", "color": C_BLUE, "badge": "4",
     "art": ill_ship,
     "headline": "UKRAINE SAYS IT SANK RUSSIAN CORVETTE OFF LIBYA",
     "body": ("Kyiv claims its sea drones sank the corvette Merkury off "
              "Benghazi. Moscow has not confirmed the claim.")},
    {"kicker": "MARKETS \u2022 CRYPTO", "color": C_AMBER, "badge": "5",
     "art": ill_btc,
     "headline": "BITCOIN REBOUNDS ABOVE $61,000 AFTER $55,100 LOW",
     "body": ("Bitcoin fell to a two-year low of $55,100 on Saturday, "
              "then climbed back above $61,000 as stocks rebounded.")},
    {"kicker": "EUROPE \u2022 SANCTIONS", "color": C_BLUE, "badge": "6",
     "art": ill_bank,
     "headline": "EU PROPOSES CUTTING 60 RUSSIAN BANKS OFF SWIFT",
     "body": ("Von der Leyen unveils the 22nd package: 60 banks off "
              "SWIFT, 70+ shadow-fleet ships, crypto crackdown. Needs "
              "all 27 states.")},
    {"kicker": "UNITED STATES \u2022 IRAN", "color": C_CRIMSON, "badge": "7",
     "art": ill_dollar,
     "headline": "US HITS IRAN'S SHADOW BANKING NETWORK",
     "body": ("Treasury sanctions 30+ exchange houses, front firms and "
              "people in Iran, the UAE, T\u00fcrkiye and Hong Kong.")},
    {"kicker": "UKRAINE \u2022 KYIV", "color": C_BLUE, "badge": "8",
     "art": ill_skyline,
     "headline": "DYMER TOLL RISES TO 11 AFTER SUNDAY STRIKE",
     "body": ("Rescuers pull an 11th body from a block hit by a Russian "
              "drone early Sunday. Kyiv region marks a day of mourning.")},
    {"kicker": "INDONESIA", "color": C_GREEN, "badge": "9",
     "art": ill_fire,
     "headline": "FACTORY FIRE KILLS 24 IN INDONESIA",
     "body": ("Indonesia confirms 24 dead in a factory fire that began "
              "on Saturday; rescuers search for dozens still missing.")},
]

BRIEFS_A = [
    ("US", C_SLATE, "Democrats hold 258 House seats, most since 1992."),
    ("HEALTH", C_TEAL, "NHS starts AI breast-screening trial, 700,000 women."),
    ("GREECE", C_BLUE, "Acropolis Museum reopens after 19 years."),
    ("FINLAND", C_BLUE, "Summons Russia's envoy over airspace breach."),
    ("IRAN", C_CRIMSON, "Singer Ahmadi flogged 74 lashes in Qom."),
    ("COLOMBIA", C_GREEN, "Drone hits C\u00facuta police base; 60 homes damaged."),
    ("SUDAN", C_CRIMSON, "UN and US condemn Sunday's Khartoum strikes."),
    ("NEPAL", C_GREEN, "India pledges $1.62bn for flood-hit Nepal."),
    ("IRAN", C_CRIMSON, "Tehran vows \u2018all means\u2019 against US blockade."),
    ("HUNGARY", C_BLUE, "PM Magyar vows to visit Zakarpattia."),
    ("ESTONIA", C_BLUE, "Russia warns of \u2018open war\u2019 over border closure."),
    ("UK", C_BLUE, "UK to host 2035 Women's World Cup."),
    ("UK", C_BLUE, "Capita shares crash 70%; CEO quits."),
]

BRIEFS_B = [
    ("SPACE", C_SLATE, "Rutte: NATO will defend space as well as land."),
    ("UK", C_BLUE, "Recognises Rohingya genocide; sanctions 5 officers."),
    ("SPORT", C_GREEN, "Weekend sport: Alcaraz, Verstappen, Liverpool win."),
    ("ISRAEL", C_CRIMSON, "Eisenkot calls settler arson \u2018Jewish terrorism\u2019."),
    ("THAILAND", C_AMBER, "Court halves lawmaker's jail term."),
    ("INDONESIA", C_GREEN, "President to name VP candidates."),
    ("ARMENIA", C_BLUE, "Trump route TRIPP launches in Syunik."),
    ("ASIA", C_AMBER, "China, S. Korea, Taiwan steady markets after rout."),
    ("TECH", C_PURPLE, "OpenAI proposes shared AI safety limits."),
    ("CHINA", C_CRIMSON, "Shenzhou-24 crew named; first Pakistani astronaut."),
    ("INDIA", C_GREEN, "Direct rail link to Nepal opens."),
    ("RUSSIA", C_BLUE, "Leaked records put war dead at 490,000+."),
    ("AUSTRALIA", C_GREEN, "Treasurer warns of tougher year ahead."),
]

DATE_CHECK = [
    ("COP31 ends without a deal", "22 NOV"),
    ("BepiColombo reaches Mercury", "21 NOV"),
    ("Bitcoin's $55,100 low", "21 NOV"),
    ("Dymer strike", "22 NOV"),
    ("Kryvyi Rih missile", "20 NOV"),
    ("Chapo Isidro arrested", "20 NOV"),
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
    if mw > CW:
        note("masthead too wide: %.1f > %d" % (mw, CW))
    d.text(((W - mw) / 2, 10), mast, font=f_mast, fill=INK)
    d.line([(MX, 72), (W - MX, 72)], fill=INK, width=2)
    d.line([(MX, 76), (W - MX, 76)], fill=INK, width=1)

    # Date, big and red.
    f_date = F(SERIF_B, 32)
    date = "MONDAY, 23 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 82), date, font=f_date, fill=RED)

    # Sub-line.
    f_sub = F(SANS_B, 11)
    sub = "ONE DAY \u2022 35 STORIES \u2022 SEVEN REGIONS"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 124), sub, font=f_sub, fill=INK)

    # Big-number strip.
    sy, sh = 142, 44
    d.rectangle([MX, sy, W - MX, sy + sh], fill=RED_BAND)
    d.line([(MX, sy), (W - MX, sy)], fill=RED, width=2)
    d.line([(MX, sy + sh), (W - MX, sy + sh)], fill=RED, width=2)
    cell = CW / len(STRIP)
    f_num = F(SANS_B, 26)
    f_lab = F(SANS_B, 10)
    for i, (num, lab) in enumerate(STRIP):
        cx = MX + cell * i + cell / 2
        nw = d.textlength(num, font=f_num)
        if nw > cell - 8:
            note("strip number too wide: %r (%.1f)" % (num, nw))
        d.text((cx - nw / 2, sy + 3), num, font=f_num, fill=RED)
        lab_lines = wrap(d, lab, f_lab, cell - 10)
        if len(lab_lines) > 1:
            note("strip label wraps: %r" % lab)
        lw = d.textlength(lab, font=f_lab)
        d.text((cx - lw / 2, sy + 31), lab, font=f_lab, fill=INK)
        if i:
            x = MX + cell * i
            d.line([(x, sy + 7), (x, sy + sh - 7)], fill=(200, 160, 158), width=1)

    # Three leads, side by side, each with its own graphic.
    ly, lh = 194, 132
    lead_w, lead_gap = 316, 8
    f_kick = F(SANS_B, 11)
    f_lhead = F(SANS_B, 16)
    f_ldeck = F(SANS, 11)
    for i, lead in enumerate(LEADS):
        lx = MX + i * (lead_w + lead_gap)
        d.rectangle([lx, ly, lx + lead_w, ly + lh], fill=CARD_BG,
                    outline=(200, 194, 178))
        d.text((lx + 10, ly + 8), lead["kicker"], font=f_kick,
               fill=lead["color"])
        kw = d.textlength(lead["kicker"], font=f_kick)
        badge(d, lx + 10 + kw + 14, ly + 15, lead["badge"], r=8)
        lead["art"](d, lx + lead_w - 72 - 8, ly + 26, 72, 72)
        h_lines = fit_lines(d, lead["headline"], f_lhead, 216, 3,
                            "lead %d headline" % (i + 1))
        draw_lines(d, lx + 10, ly + 26, h_lines, f_lhead, INK, 19)
        deck_lines = fit_lines(d, lead["deck"], f_ldeck, 296, 2,
                               "lead %d deck" % (i + 1))
        draw_lines(d, lx + 10, ly + 102, deck_lines, f_ldeck, INK, 14)

    # Map + UTC timeline row.
    my, mh = 334, 110
    # Map (left).
    d.rectangle([MX, my, MX + 500, my + mh], fill=CARD_BG,
                outline=(200, 194, 178))
    f_maplab = F(SANS_B, 10)
    d.text((MX + 10, my + 8), "WHERE IT HAPPENED", font=f_maplab, fill=GREY)
    d.text((MX + 500 - 10 - d.textlength("1\u20139 = LEADS & GRID",
           font=f_maplab), my + 8), "1\u20139 = LEADS & GRID",
           font=f_maplab, fill=GREY)
    draw_map(d, MX + 8, my + 22, 484, 84, dot_r=1.8)
    # Timeline (right).
    tx0 = MX + 508
    tw = W - MX - tx0
    d.rectangle([tx0, my, tx0 + tw, my + mh], fill=CARD_BG,
                outline=(200, 194, 178))
    d.text((tx0 + 10, my + 8), "THE DAY IN UTC", font=f_maplab, fill=GREY)
    f_tl = F(SANS, 11)
    f_tlb = F(SANS_B, 11)
    for j, (tm, txt) in enumerate(TIMELINE):
        yy = my + 26 + j * 14
        d.text((tx0 + 10, yy), tm, font=f_tlb, fill=RED)
        if d.textlength(tm + "  " + txt, font=f_tl) > tw - 20:
            note("timeline too wide: %r" % txt)
        d.text((tx0 + 52, yy), txt, font=f_tl, fill=INK)

    # Grid: 2 columns x 3 rows of main stories.
    gy = 452
    card_w, card_h, gap = 478, 84, 6
    f_h = F(SANS_B, 16)
    f_b = F(SANS, 11)
    for i, story in enumerate(GRID):
        cx = MX + (i % 2) * (card_w + gap)
        cy = gy + (i // 2) * (card_h + gap)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=CARD_BG,
                    outline=(200, 194, 178))
        tx = cx + 12
        d.text((tx, cy + 6), story["kicker"], font=f_kick, fill=story["color"])
        if story["badge"]:
            kw = d.textlength(story["kicker"], font=f_kick)
            badge(d, tx + kw + 16, cy + 13, story["badge"], r=8)
        art_w, art_h = 80, 66
        ax, ay = cx + card_w - art_w - 8, cy + 9
        story["art"](d, ax, ay, art_w, art_h)
        text_w = card_w - art_w - 12 - 14
        h_lines = fit_lines(d, story["headline"], f_h, text_w, 2,
                            "headline %d" % (i + 1))
        draw_lines(d, tx, cy + 22, h_lines, f_h, INK, 18)
        b_lines = fit_lines(d, story["body"], f_b, text_w, 2, "body %d" % (i + 1))
        draw_lines(d, tx, cy + 58, b_lines, f_b, INK, 12)

    # DATE CHECK box: 9 non-23-Nov stories, honestly dated.
    dy, dh = 724, 64
    d.rectangle([MX, dy, W - MX, dy + dh], fill=RED_BAND, outline=RED, width=2)
    f_dc = F(SANS_B, 12)
    f_dci = F(SANS, 11)
    d.text((MX + 12, dy + 5), "DATE CHECK \u2014 WHAT WE LEFT OUT:",
           font=f_dc, fill=RED)
    for r in range(3):
        items = DATE_CHECK[r * 3:(r + 1) * 3]
        line = "   \u2715 " + "   \u00b7   \u2715 ".join(
            "%s \u2014 %s" % (t, dt) for (t, dt) in items)
        if d.textlength(line, font=f_dci) > CW - 24:
            note("DATE CHECK line too wide: %r" % line)
        d.text((MX + 12, dy + 22 + r * 14), line, font=f_dci, fill=INK)

    # Briefs, two columns, one line each.
    by = 796
    f_sec = F(SANS_B, 11)
    d.text((MX, by), "IN BRIEF", font=f_sec, fill=RED)
    d.line([(MX + 74, by + 6), (W - MX, by + 6)], fill=(200, 194, 178), width=1)
    f_br = F(SANS, 12)
    f_bk = F(SANS_B, 12)
    lead = 13
    for col, briefs in enumerate((BRIEFS_A, BRIEFS_B)):
        bx = MX + col * (card_w + gap)
        for j, (kick, color, text) in enumerate(briefs):
            yy = by + 18 + j * lead
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
    d.text(((W - fw) / 2, 992), foot, font=f_foot, fill=GREY)

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
