from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ASSETS = Path(
    r"C:\Users\Luis\.cursor\projects"
    r"\c-Users-Luis-OneDrive-Desktop-SADACO\assets"
)
OUTPUT = Path(__file__).resolve().parents[2] / "bocetos"

CONCEPTS = [
    (
        "01  EMBLEMA",
        "Mayor parentesco con SADACO International",
        ASSETS / "sadaco-venezuela-01-emblema.png",
    ),
    (
        "02  TEPUI",
        "Venezuela + solidez industrial",
        ASSETS / "sadaco-venezuela-02-tepui.png",
    ),
    (
        "03  MONOGRAMA SV",
        "S azul + V verde, sin marco exterior",
        ASSETS / "sadaco-venezuela-03-monograma-v2.png",
    ),
    (
        "04  LOGOTIPO",
        "Sobrio, internacional y flexible",
        ASSETS / "sadaco-venezuela-04-logotipo.png",
    ),
]

NAVY = "#073B78"
GREEN = "#008B67"
INK = "#152334"
MUTED = "#657080"
LINE = "#D9DEE4"
BACKGROUND = "#EEF1F4"
WHITE = "#FFFFFF"

WIDTH = 2400
HEIGHT = 1900
MARGIN = 110
GAP = 54
HEADER = 215
CARD_W = (WIDTH - 2 * MARGIN - GAP) // 2
CARD_H = 720
LABEL_H = 96


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(Path(r"C:\Windows\Fonts") / name, size)


title_font = font("segoeuib.ttf", 64)
subtitle_font = font("segoeui.ttf", 26)
label_font = font("segoeuib.ttf", 27)
description_font = font("segoeui.ttf", 22)
footer_font = font("segoeui.ttf", 20)

canvas = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
draw = ImageDraw.Draw(canvas)

draw.text((MARGIN, 68), "SADACO VENEZUELA", font=title_font, fill=INK)
draw.text(
    (MARGIN, 145),
    "Cuatro direcciones de identidad visual · propuestas conceptuales",
    font=subtitle_font,
    fill=MUTED,
)
draw.rectangle((MARGIN, 192, WIDTH - MARGIN, 198), fill=NAVY)
draw.rectangle((MARGIN, 198, MARGIN + 320, 204), fill=GREEN)

for index, (label, description, path) in enumerate(CONCEPTS):
    row, col = divmod(index, 2)
    x = MARGIN + col * (CARD_W + GAP)
    y = HEADER + row * (CARD_H + GAP)

    draw.rectangle((x, y, x + CARD_W, y + CARD_H), fill=WHITE, outline=LINE, width=2)
    draw.text((x + 34, y + 24), label, font=label_font, fill=NAVY)
    draw.text((x + 34, y + 61), description, font=description_font, fill=MUTED)
    draw.line((x + 34, y + LABEL_H, x + CARD_W - 34, y + LABEL_H), fill=LINE, width=2)

    image = Image.open(path).convert("RGB")
    area_w = CARD_W - 36
    area_h = CARD_H - LABEL_H - 26
    image.thumbnail((area_w, area_h), Image.Resampling.LANCZOS)
    image_x = x + (CARD_W - image.width) // 2
    image_y = y + LABEL_H + 13 + (area_h - image.height) // 2
    canvas.paste(image, (image_x, image_y))

footer_y = HEADER + 2 * (CARD_H + GAP) + 10
draw.text(
    (MARGIN, footer_y),
    "Orden sugerido para la reunión: 02 Tepui → 03 Monograma SV → 04 Logotipo → 01 Emblema.",
    font=footer_font,
    fill=INK,
)
draw.text(
    (MARGIN, footer_y + 34),
    "Son direcciones para seleccionar y refinar; no son artes finales ni sustituyen una prueba de registro marcario.",
    font=footer_font,
    fill=MUTED,
)

output = OUTPUT / "SADACO-Venezuela-Propuestas-v2.png"
canvas.save(output, optimize=True)
print(output)
