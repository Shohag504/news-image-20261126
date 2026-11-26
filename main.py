#!/usr/bin/env python3
"""Render the front page of THE WORLD TODAY for Thursday 26 November 2026.

Deterministic: no clock, no randomness, no network. Writes entry.png
(1024x1024, under 1 MiB) to $MAKEFUN_OUTPUT_DIR or /output. If Pillow is
missing, falls back to copying the shipped entry.png next to this script.
"""
import os
import shutil

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT_PATH = os.path.join(OUT_DIR, "entry.png")
HERE = os.path.dirname(os.path.abspath(__file__))
SHIPPED = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (158, 27, 27)
GOLD = (176, 141, 60)
GREY = (90, 86, 78)
PANEL = (255, 255, 255)
SKY = (214, 228, 238)


def main():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        shutil.copyfile(SHIPPED, OUT_PATH)
        return

    def font(name, size):
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/" + name, size)

    serif = lambda s: font("DejaVuSerif-Bold.ttf", s)
    serif_r = lambda s: font("DejaVuSerif.ttf", s)
    sans = lambda s: font("DejaVuSans.ttf", s)
    sans_b = lambda s: font("DejaVuSans-Bold.ttf", s)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    def wrap(text, fnt, width):
        words, lines, cur = text.split(), [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if d.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def para(text, fnt, x, y, width, leading, fill=INK):
        for line in wrap(text, fnt, width):
            d.text((x, y), line, font=fnt, fill=fill)
            y += leading
        return y

    def rule(x0, y, x1, width=2, fill=INK):
        d.line([(x0, y), (x1, y)], fill=fill, width=width)

    def kicker(text, x, y):
        d.text((x, y), text, font=sans_b(20), fill=RED)

    # ---- masthead ----
    d.text((48, 26), "THE WORLD TODAY", font=serif(66), fill=INK)
    d.text((48, 108), "THURSDAY 26 NOVEMBER 2026", font=sans_b(26), fill=RED)
    d.text((48, 140), "World news in one image  |  $100 prize  |  50 winners",
           font=sans(20), fill=GREY)
    rule(48, 176, 976, 3)
    rule(48, 182, 976, 1, GOLD)

    # ---- lead story: US tariffs (left column, ends by y=700) ----
    lx, ly, lw = 48, 200, 600
    kicker("TRADE WAR  •  WASHINGTON", lx, ly)
    y = para("US hits 14 nations with new tariffs",
             serif(40), lx, ly + 30, lw, 46)
    y = para("India faces a 25% duty on its goods; China, the EU and "
             "Japan are also in the firing line as Washington opens a "
             "second act in its tariff war.",
             serif_r(22), lx, y + 6, lw, 29)
    y = para("The White House says the levies punish \u201cexcess capacity\u201d "
             "and unfair trade. Partners from Delhi to Brussels called "
             "the move a blow to trade.",
             sans(19), lx, y + 8, lw, 26)

    # cargo-ship illustration panel, 140 tall
    py = y + 14
    d.rectangle([lx, py, lx + lw, py + 140], fill=SKY, outline=INK, width=2)
    d.rectangle([lx, py + 106, lx + lw, py + 140], fill=(58, 110, 158))
    d.polygon([(lx + 60, py + 84), (lx + 540, py + 84),
               (lx + 510, py + 108), (lx + 90, py + 108)],
              fill=(38, 48, 60))
    for i, col in enumerate([(158, 27, 27), (176, 141, 60), (38, 90, 60),
                             (158, 27, 27)]):
        x0 = lx + 110 + i * 82
        d.rectangle([x0, py + 38, x0 + 74, py + 82], fill=col,
                    outline=INK, width=2)
    d.rectangle([lx + 452, py + 22, lx + 540, py + 82], fill=(240, 240, 240),
                outline=INK, width=2)
    d.text((lx + 24, py + 6), "25%  •  TARIFFS", font=sans_b(22), fill=RED)
    d.text((lx + 430, py + 112), "GLOBAL TRADE", font=sans_b(17),
           fill=(255, 255, 255))

    # ---- right column: three short blocks, each capped ----
    rx, rw = 688, 288
    ry = 200
    kicker("DISASTER  •  CAIRO", rx, ry)
    ry = para("Tanker fire kills 31 near Cairo",
              serif(26), rx, ry + 28, rw, 31)
    ry = para("At least 31 died and about 21 were hurt in the tanker "
              "fire on the highway around Cairo.",
              sans(18), rx, ry + 4, rw, 24)
    rule(rx, ry + 10, rx + rw, 1, GREY)
    ry += 22
    kicker("GULF ON EDGE", rx, ry)
    ry = para("Houthis hit Saudi refinery",
              serif(26), rx, ry + 28, rw, 31)
    ry = para("Attacks on Saudi ports and Ras Tanura pushed Brent "
              "crude to $94.71 a barrel.",
              sans(18), rx, ry + 4, rw, 24)
    rule(rx, ry + 10, rx + rw, 1, GREY)
    ry += 22
    kicker("NORTH KOREA", rx, ry)
    para("Kim widens tactical nuclear rollout",
         serif(26), rx, ry + 28, rw, 31)

    # ---- space band ----
    rule(48, 712, 976, 2)
    d.rectangle([48, 726, 976, 812], fill=PANEL, outline=INK, width=2)
    d.text((72, 738), "SPACE", font=sans_b(19), fill=RED)
    d.text((72, 760),
           "First Pakistani in orbit aboard China\u2019s Tiangong station",
           font=serif(27), fill=INK)
    d.text((72, 792), "Muhammad Zeeshan Ali, on Shenzhou-24, is the first "
           "foreign national to join the Chinese station.",
           font=sans(17), fill=GREY)

    # ---- also today strip ----
    ay = 828
    d.text((48, ay), "ALSO TODAY", font=sans_b(21), fill=RED)
    rule(48, ay + 30, 976, 1, GREY)
    items = [
        ("UKRAINE", "Kyiv says it struck a Russian airbase and damaged five jets."),
        ("THANKSGIVING", "New York\u2019s Macy\u2019s parade put off to Saturday as a storm nears."),
        ("MISS UNIVERSE", "Puerto Rico\u2019s Jennifer Barreto takes the 2026 crown."),
        ("FOOTBALL", "Liverpool beat Club Brugge 3\u20130 in the Champions League."),
        ("MARKETS", "Nasdaq slides as the AI stock sell-off deepens."),
        ("ISRAEL", "Judges urge prosecutors to drop a Netanyahu bribery case."),
    ]
    yy = ay + 42
    for tag, text in items:
        d.text((48, yy), tag, font=sans_b(18), fill=RED)
        d.text((214, yy), text, font=sans(18), fill=INK)
        yy += 23

    # ---- footer ----
    rule(48, 1006, 976, 1, GREY)
    d.text((48, 1010), "26 NOVEMBER 2026  •  THE WORLD TODAY",
           font=sans_b(13), fill=GREY)

    os.makedirs(OUT_DIR, exist_ok=True)
    img.save(OUT_PATH, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
