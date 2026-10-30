"""Generate print-ready PNGs (3600x4800, 300 DPI = 12x16in Printful front print area).

Run: python3 store/designs/generate.py
Output: store/designs/out/<slug>.png (transparent) and store/designs/out/_preview.png
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONTS = ROOT.parent / "fonts"
OUT = ROOT / "out"
W, H = 3600, 4800

GOLD = (254, 209, 0)
GREEN = (0, 155, 58)
WHITE = (245, 242, 235)
RED = (200, 30, 45)


def font(name, size):
    return ImageFont.truetype(str(FONTS / f"{name}.woff"), size)


def fit(draw, text, name, max_w, max_size):
    """Largest font size (<= max_size) at which text fits max_w."""
    size = max_size
    while size > 40:
        f = font(name, size)
        l, t, r, b = draw.textbbox((0, 0), text, font=f)
        if r - l <= max_w:
            return f
        size -= 20
    return font(name, size)


def stack(lines, top=300, gap=60, max_w=3300):
    """lines: list of (text, font_name, max_size, color). Draws centered, vertically stacked."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = top
    for text, name, max_size, color in lines:
        f = fit(d, text, name, max_w, max_size)
        l, t, r, b = d.textbbox((0, 0), text, font=f)
        d.text(((W - (r - l)) / 2 - l, y - t), text, font=f, fill=color)
        y += (b - t) + gap
    return img.crop(img.getbbox())  # trim; Printful centres on the print area


def bar(width=2400, h=70, colors=(GREEN, GOLD, GREEN)):
    img = Image.new("RGBA", (width, h * len(colors) + 30 * (len(colors) - 1)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, c in enumerate(colors):
        d.rectangle([0, i * (h + 30), width, i * (h + 30) + h], fill=c)
    return img


def vjoin(*parts, gap=120):
    w = max(p.width for p in parts)
    h = sum(p.height for p in parts) + gap * (len(parts) - 1)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    y = 0
    for p in parts:
        img.alpha_composite(p, ((w - p.width) // 2, y))
        y += p.height + gap
    return img


DESIGNS = {
    "likkle-but-tallawah": lambda: vjoin(
        stack([("WI LIKKLE", "anton", 900, WHITE), ("BUT WI", "anton", 500, GOLD),
               ("TALLAWAH", "anton", 900, GREEN)]), bar()),
    "christmas-breeze": lambda: vjoin(
        stack([("Christmas Breeze", "pacifico", 520, GOLD)]),
        stack([("A BLOW", "anton", 1100, WHITE)]),
        stack([("SORREL • BLACK CAKE • GRAND MARKET", "bebas-neue", 300, GREEN)])),
    "grand-market-2026": lambda: vjoin(
        stack([("GRAND", "archivo-black", 1000, WHITE), ("MARKET", "archivo-black", 1000, GOLD)]),
        bar(colors=(GREEN,)),
        stack([("DECEMBER 24 • 2026", "bebas-neue", 380, WHITE)])),
    "mi-deh-yah": lambda: vjoin(
        stack([("MI DEH YAH", "anton", 1000, GOLD)]),
        stack([("(and mi a gwaan good)", "permanent-marker", 300, WHITE)])),
    "yaad-heart": lambda: vjoin(
        stack([("YAAD", "anton", 1400, GREEN)]),
        stack([("IS WHERE THE HEART IS", "bebas-neue", 400, WHITE)]), bar(colors=(GOLD,))),
    "black-cake-supervisor": lambda: vjoin(
        stack([("BLACK CAKE", "anton", 900, WHITE), ("SUPERVISOR", "anton", 900, GOLD)]),
        stack([("certified by mama • soaked since september", "permanent-marker", 230, GREEN)])),
}

# Diaspora city series: one listing, many variants -> long-tail search traffic
for city in ["BROOKLYN", "THE BRONX", "TORONTO", "LONDON", "MIAMI", "BIRMINGHAM", "ATLANTA", "HARTFORD"]:
    slug = "roots-" + city.lower().replace("the ", "").replace(" ", "-")
    DESIGNS[slug] = (lambda c=city: vjoin(
        stack([("JAMAICAN ROOTS", "anton", 700, GOLD)]), bar(colors=(GREEN,)),
        stack([(f"{c} RAISED", "anton", 700, WHITE)])))


def family_reunion(surname, year="2026"):
    """Template for bulk/group orders (the fastest path to big order values)."""
    return vjoin(stack([("THE", "bebas-neue", 400, GOLD), (surname.upper(), "anton", 1000, WHITE),
                        ("FAMILY", "anton", 600, GOLD)]), bar(),
                 stack([(f"YAAD REUNION • {year}", "bebas-neue", 380, WHITE)]))


DESIGNS["family-template-sample"] = lambda: family_reunion("Campbell")


def main():
    OUT.mkdir(exist_ok=True)
    thumbs = []
    for slug, make in DESIGNS.items():
        art = make()
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        scale = min(3300 / art.width, 4500 / art.height, 1)
        art = art.resize((int(art.width * scale), int(art.height * scale)), Image.LANCZOS)
        canvas.alpha_composite(art, ((W - art.width) // 2, 150))
        canvas.save(OUT / f"{slug}.png", dpi=(300, 300))
        t = Image.new("RGBA", (W, H), (22, 22, 22, 255))
        t.alpha_composite(canvas)
        thumbs.append(t.resize((360, 480)))
        print("wrote", slug)
    cols = 6
    sheet = Image.new("RGB", (cols * 380, ((len(thumbs) + cols - 1) // cols) * 500), (60, 60, 60))
    for i, t in enumerate(thumbs):
        sheet.paste(t, ((i % cols) * 380 + 10, (i // cols) * 500 + 10))
    sheet.save(OUT / "_preview.png")


if __name__ == "__main__":
    main()
