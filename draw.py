#!/usr/bin/env python3
"""news-23 b106 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026 (31 stories)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")

def F(path, size):
    return ImageFont.truetype(path, size)

BLACK = (17, 17, 17)
RED = (176, 30, 36)
GOLD = (201, 162, 39)
NAVY = (27, 42, 74)
GREEN = (30, 91, 60)
CREAM = (247, 243, 232)
MAPG = (200, 221, 187)
DARK = (34, 34, 34)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
LGREY = (230, 230, 225)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def tw(text, font, maxw):
    """Wrap text to maxw pixels; return list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(x, y, lines, font, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

def chip(x, y, text, kind):
    """Draw REPORTED (navy) or CLAIM (red) chip; returns right edge."""
    f = F(SANS_B, 11)
    w = int(d.textlength(text, font=f)) + 12
    col = NAVY if kind == "REPORTED" else RED
    d.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=col)
    d.text((x + 6, y + 2), text, font=f, fill=WHITE)
    return x + w

# ---------------- masthead ----------------
d.rectangle([0, 0, W, 58], fill=BLACK)
f_mast = F(SERIF_B, 40)
d.text((14, 7), "THE WORLD TODAY", font=f_mast, fill=WHITE)
f_date = F(SANS_B, 15)
dt = "MONDAY 23 NOVEMBER 2026"
d.text((W - 14 - d.textlength(dt, font=f_date), 20), dt, font=f_date, fill=GOLD)

# ---------------- kicker ----------------
d.rectangle([0, 58, W, 84], fill=RED)
f_kick = F(SANS_B, 14)
kick = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
d.text(((W - d.textlength(kick, font=f_kick)) / 2, 65), kick, font=f_kick, fill=WHITE)

# ---------------- number strip (2 rows x 5) ----------------
nums = [
    ("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"), ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL STABILISATION FUND"), ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"), ("12,000", "CLEARED IN MANCHESTER"),
    ("264 kg", "EXPLOSIVES SEIZED"), ("$107.3B", "ANTHROPIC IPO"),
]
f_val = F(SANS_B, 15)
f_lab = F(SANS, 9)
colw = W // 5
for i, (v, lab) in enumerate(nums):
    cx = (i % 5) * colw + 12
    cy = 88 + (i // 5) * 28
    vcol = RED if i in (0, 5) else (NAVY if i in (1, 9) else GREEN if i in (2, 7) else (GOLD if i in (3, 8) else DARK))
    d.text((cx, cy), v, font=f_val, fill=vcol)
    d.text((cx, cy + 15), lab, font=f_lab, fill=GREY)

# ---------------- region bar ----------------
regs = [("ASIA-PACIFIC 7", NAVY), ("AMERICAS 8", RED), ("MIDDLE EAST 6", GOLD),
        ("EUROPE 5", (46, 90, 140)), ("AFRICA 3", GREEN), ("WORLD 2", (70, 70, 70))]
f_reg = F(SANS_B, 12)
rx = 0
for name, col in regs:
    w = int(d.textlength(name, font=f_reg)) + 24
    d.rectangle([rx, 146, rx + w, 166], fill=col)
    d.text((rx + 12, 150), name, font=f_reg, fill=WHITE)
    rx += w
d.rectangle([rx, 146, W, 166], fill=(70, 70, 70))

# ---------------- UTC strip ----------------
f_utc = F(SANS, 11)
utc = "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles"
d.text((10, 170), utc, font=f_utc, fill=DARK)
d.text((W - 10 - d.textlength("~ APPROX", font=f_utc), 170), "~ APPROX", font=f_utc, fill=GREY)

# ---------------- heroes ----------------
HERO_Y = 186
SCENE_H = 132
COLW = 336
GAP = 8
heroes = [
    dict(kind="kospi", head="AI ROUT HITS ASIA",
         body="Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
         src="KOREA EXCHANGE"),
    dict(kind="guterres", head="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         body="UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
         src="UNITED NATIONS"),
    dict(kind="power", head="US LEAD OVER CHINA AT RECORD LOW",
         body="Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
         src="LOWY INSTITUTE"),
]
f_head = F(SERIF_B, 20)
f_body = F(SANS, 12)
f_src = F(SANS, 10)

for i, h in enumerate(heroes):
    x0 = i * (COLW + GAP) + GAP // 2
    x1 = x0 + COLW
    # scene
    if h["kind"] == "kospi":
        d.rectangle([x0, HERO_Y, x1, HERO_Y + SCENE_H], fill=NAVY)
        # buildings
        import random
        random.seed(7)
        for bx in range(x0 + 8, x1 - 8, 22):
            bh = random.randint(30, 78)
            d.rectangle([bx, HERO_Y + SCENE_H - 22 - bh, bx + 16, HERO_Y + SCENE_H - 22], fill=(38, 56, 96))
            for wy in range(HERO_Y + SCENE_H - 18 - bh, HERO_Y + SCENE_H - 24, 10):
                for wx in (bx + 3, bx + 9):
                    if random.random() < 0.6:
                        d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
        # chart line
        pts = [(x0 + 12 + k * 40, HERO_Y + 52 - k * 3 + (k % 2) * 6) for k in range(8)]
        pts[-1] = (x1 - 14, HERO_Y + 84)
        d.line(pts, fill=(255, 140, 40), width=3)
        for px, py in pts:
            d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=WHITE, outline=(255, 140, 40))
        f_big = F(SANS_B, 30)
        d.text((x0 + 10, HERO_Y + 4), "-3.3%", font=f_big, fill=WHITE)
        d.rectangle([x0, HERO_Y + SCENE_H - 22, x1, HERO_Y + SCENE_H], fill=BLACK)
        f_sc = F(SANS_B, 11)
        d.text((x0 + 8, HERO_Y + SCENE_H - 19), "KOSPI 4,708.54  \u00b7  -161 PTS", font=f_sc, fill=WHITE)
    elif h["kind"] == "guterres":
        d.rectangle([x0, HERO_Y, x1, HERO_Y + SCENE_H], fill=GREEN)
        f_g1 = F(SANS_B, 34)
        d.text((x0 + 10, HERO_Y + 6), "150", font=f_g1, fill=GOLD)
        f_g2 = F(SANS_B, 19)
        gl = tw("DELEGATES BACK A RISK FRAMEWORK", f_g2, 190)
        draw_lines(x0 + 10, HERO_Y + 44, gl, f_g2, GOLD, 22)
        # globe
        cx, cy, r = x1 - 52, HERO_Y + 62, 40
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 225, 200), outline=WHITE, width=2)
        d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(120, 170, 140))
        d.line([cx - r, cy, cx + r, cy], fill=(120, 170, 140))
        d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(120, 170, 140))
        d.rectangle([x0, HERO_Y + SCENE_H - 22, x1, HERO_Y + SCENE_H], fill=BLACK)
        f_sc = F(SANS_B, 11)
        d.text((x0 + 8, HERO_Y + SCENE_H - 19), "UN  \u00b7  BRIDGETOWN", font=f_sc, fill=WHITE)
    else:
        d.rectangle([x0, HERO_Y, x1, HERO_Y + SCENE_H], fill=CREAM)
        d.rectangle([x0, HERO_Y, x1, HERO_Y + 20], fill=BLACK)
        f_sc = F(SANS_B, 11)
        d.text((x0 + 8, HERO_Y + 3), "NARROWEST SINCE 2018", font=f_sc, fill=WHITE)
        d.text((x1 - 8 - d.textlength("GAP 5.3", font=f_sc), HERO_Y + 3), "GAP 5.3", font=f_sc, fill=RED)
        bars = [("78.9", "US", NAVY, 92), ("73.6", "CHINA", RED, 86), ("40.5", "INDIA", GOLD, 48)]
        bx = x0 + 24
        f_bv = F(SANS_B, 17)
        f_bl = F(SANS_B, 12)
        for val, lab, col, bh in bars:
            base = HERO_Y + SCENE_H - 6
            d.rectangle([bx, base - bh, bx + 62, base], fill=col)
            d.text((bx + 31 - d.textlength(val, font=f_bv) / 2, base - bh - 22), val, font=f_bv, fill=DARK)
            d.text((bx + 31 - d.textlength(lab, font=f_bl) / 2, base - 18), lab, font=f_bl, fill=WHITE if col != GOLD else DARK)
            bx += 104
        d.rectangle([x0, HERO_Y + SCENE_H - 22, x1, HERO_Y + SCENE_H], fill=BLACK)
        d.text((x0 + 8, HERO_Y + SCENE_H - 19), "ASIA POWER INDEX 2026", font=f_sc, fill=WHITE)
    # headline below scene
    hy = HERO_Y + SCENE_H + 8
    hl = tw(h["head"], f_head, COLW - 4)
    hy = draw_lines(x0 + 2, hy, hl, f_head, DARK, 23)
    by = hy + 4
    bl = tw(h["body"], f_body, COLW - 4)
    by = draw_lines(x0 + 2, by, bl, f_body, DARK, 15)
    # source + chip row (fixed, below body with gap; chip bottom clears the 428 strip)
    sy = HERO_Y + SCENE_H + 8 + 46 + 30 + 6  # 408
    d.text((x0 + 2, sy + 2), h["src"], font=f_src, fill=GREY)
    chip(x1 - 82, sy, "REPORTED", "REPORTED")

# ---------------- 10 stories strip ----------------
d.rectangle([0, 428, W, 452], fill=BLACK)
f_sec = F(SERIF_B, 16)
d.text((10, 432), "MORE OF THE DAY  \u2014  10 STORIES", font=f_sec, fill=WHITE)

cards = [
    ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
catcols = {"AMERICAS": RED, "FBI": NAVY, "WHITE HOUSE": (46, 90, 140), "MARKETS": GREEN,
           "SPORT": RED, "LEGAL": NAVY, "TECH": (46, 90, 140), "EUROPE": (90, 60, 120), "SPACE": (90, 60, 120)}
f_cat = F(SANS_B, 10)
f_ch = F(SANS_B, 12)
f_cb = F(SANS, 11)
CARDW = 200
CARDH = 82
for i, (cat, head, body, src, kind) in enumerate(cards):
    cx = (i % 5) * CARDW + 4
    cy = 456 + (i // 5) * (CARDH + 4)
    d.rectangle([cx, cy, cx + CARDW - 8, cy + 16], fill=catcols[cat])
    d.text((cx + 4, cy + 2), cat, font=f_cat, fill=WHITE)
    d.text((cx + CARDW - 22, cy + 2), str(i + 1), font=f_cat, fill=WHITE)
    hl = tw(head, f_ch, CARDW - 16)
    hy = draw_lines(cx + 4, cy + 19, hl[:2], f_ch, DARK, 14)
    d.text((cx + 4, hy + 2), body, font=f_cb, fill=DARK)
    sy = cy + CARDH - 18
    d.text((cx + 4, sy + 2), src, font=f_src, fill=GREY)
    chip(cx + CARDW - 86, sy, kind, kind)

# ---------------- map + also header ----------------
d.rectangle([0, 628, 336, 652], fill=BLACK)
d.text((10, 632), "WHERE IT HAPPENED", font=f_sec, fill=WHITE)
d.rectangle([344, 628, W, 652], fill=BLACK)
d.text((354, 632), "ALSO ON MONDAY", font=f_sec, fill=WHITE)

# map blobs
d.rectangle([0, 652, 336, 872], fill=CREAM)
# rough continents (light green blobs)
d.polygon([(20, 700), (90, 672), (150, 690), (160, 740), (120, 790), (60, 800), (18, 760)], fill=MAPG)
d.polygon([(180, 690), (250, 668), (310, 690), (300, 750), (240, 770), (185, 740)], fill=MAPG)
d.polygon([(120, 810), (170, 800), (185, 840), (150, 862), (118, 845)], fill=MAPG)
d.polygon([(250, 800), (300, 790), (318, 830), (285, 860), (248, 845)], fill=MAPG)
pins = [(70, 712), (58, 798), (272, 735), (95, 782), (120, 762), (232, 700), (150, 760),
        (105, 738), (135, 800), (112, 790), (215, 688), (195, 700), (255, 685)]
f_pin = F(SANS_B, 10)
for n, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    d.text((px - 3, py - 7), str(n), font=f_pin, fill=WHITE)
f_leg = F(SANS, 10)
leg = ["Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing",
       "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF",
       "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow"]
ly = 872 - 34
for ln in leg:
    d.text((8, ly), ln, font=f_leg, fill=GREY)
    ly += 12

# ALSO list (2 columns x 9)
also = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared",
    "Zelenskyy: 165 missiles in a week",
    "COP31: the day after Antalya pact rejected",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: strike hits plant, 2 hurt",
    "Benghazi: UN demands probe  [CLAIM]",
    "Sudan: defences down drones  [CLAIM]",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits in exam row",
    "SK Telecom -7.3% as hype cools",
    "China eases margin rules",
    "Seoul readies 10T-won fund",
]
f_al = F(SANS, 12)
f_alb = F(SANS_B, 12)
for i, item in enumerate(also):
    col = i // 9
    row = i % 9
    ax = 354 + col * 340
    ay = 660 + row * 24
    num = f"{i + 14}."
    d.text((ax, ay), num, font=f_alb, fill=RED)
    d.text((ax + 28, ay), item, font=f_al, fill=DARK)

# ---------------- DATE CHECK ----------------
d.rectangle([8, 880, W - 8, 946], outline=RED, width=2)
f_dc = F(SANS_B, 13)
d.text((14, 884), "DATE CHECK", font=f_dc, fill=RED)
d.text((W - 14 - d.textlength("READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", font=F(SANS_B, 10)), 886),
       "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", font=F(SANS_B, 10), fill=RED)
f_dcb = F(SANS, 11)
d.text((14, 904), "LEFT OUT \u2014 NOT 23 NOV:  Dems 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo (22 Nov)  \u00b7  EU\u2013Indonesia (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar (19 Nov)",
       font=f_dcb, fill=DARK)
d.text((14, 922), "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
       font=f_dcb, fill=DARK)

# ---------------- footer ----------------
f_ft = F(SANS, 10)
d.text((10, 952), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).", font=f_ft, fill=GREY)
d.text((10, 966), "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.", font=f_ft, fill=GREY)
d.text((10, 980), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.", font=f_ft, fill=GREY)
f_gf = F(SANS_B, 12)
gf = "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((W - d.textlength(gf, font=f_gf)) / 2, 998), gf, font=f_gf, fill=GOLD)

out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png")
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
img.save(out)
print("saved", out, os.path.getsize(out), "bytes")
