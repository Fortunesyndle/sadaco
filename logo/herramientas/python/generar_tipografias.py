from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERRAMIENTAS = Path(__file__).resolve().parents[1]
LOGO = HERRAMIENTAS.parent
FONT_DIR = HERRAMIENTAS / "fonts-google"
OUTPUT_DIR = LOGO / "bocetos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NAVY = "#0B3F7A"
GREEN = "#138B65"
INK = "#172536"
MUTED = "#687587"
LINE = "#DCE2E8"
PAPER = "#FFFFFF"
BACKGROUND = "#F1F4F6"

WIDTH = 2400
HEIGHT = 1500
MARGIN = 100
HEADER = 210
GAP = 42
CARD_W = (WIDTH - 2 * MARGIN - 2 * GAP) // 3
CARD_H = 540


def load_font(filename: str, size: int, axes: list[int] | None = None) -> ImageFont.FreeTypeFont:
    loaded = ImageFont.truetype(FONT_DIR / filename, size)
    if axes:
        loaded.set_variation_by_axes(axes)
    return loaded


def system_font(filename: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(Path(r"C:\Windows\Fonts") / filename, size)


title_font = system_font("segoeuib.ttf", 58)
subtitle_font = system_font("segoeui.ttf", 25)
label_font = system_font("segoeuib.ttf", 22)
note_font = system_font("segoeui.ttf", 19)

faces = [
    ("01", "SPACE GROTESK", "Geométrica, técnica y contemporánea", "SpaceGrotesk.ttf", [700], -2, False),
    ("02", "MANROPE", "Corporativa, limpia y muy legible", "Manrope.ttf", [760], 1, True),
    ("03", "ARCHIVO EXPANDED", "Robusta y preparada para señalización", "Archivo.ttf", [760, 118], 0, False),
    ("04", "BARLOW SEMI CONDENSED", "Industrial, eficiente y compacta", "BarlowSemiCondensed-SemiBold.ttf", None, 6, True),
    ("05", "SORA", "Tecnológica sin perder formalidad", "Sora.ttf", [720], -1, True),
    ("06", "RAJDHANI", "Técnica, estrecha y distintiva", "Rajdhani-SemiBold.ttf", None, 8, False),
]


def tracked_width(text: str, face: ImageFont.FreeTypeFont, tracking: float) -> float:
    return sum(face.getlength(char) for char in text) + tracking * (len(text) - 1)


def fit_face(filename: str, axes: list[int] | None, max_width: int) -> ImageFont.FreeTypeFont:
    size = 150
    while size > 72:
        face = load_font(filename, size, axes)
        if face.getlength("SADACO") <= max_width:
            return face
        size -= 3
    return load_font(filename, size, axes)


def draw_wordmark(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    face: ImageFont.FreeTypeFont,
    tracking: float,
    accent_o: bool,
) -> None:
    text = "SADACO"
    x1, y1, x2, y2 = box
    total = tracked_width(text, face, tracking)
    x = x1 + (x2 - x1 - total) / 2
    bbox = face.getbbox(text)
    text_height = bbox[3] - bbox[1]
    y = y1 + (y2 - y1 - text_height) / 2 - bbox[1]
    for index, char in enumerate(text):
        fill = GREEN if accent_o and char == "O" else NAVY
        draw.text((x, y), char, font=face, fill=fill)
        x += face.getlength(char)
        if index < len(text) - 1:
            x += tracking


canvas = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
draw = ImageDraw.Draw(canvas)

draw.text((MARGIN, 55), "SADACO · EXPLORACIÓN TIPOGRÁFICA", font=title_font, fill=INK)
draw.text(
    (MARGIN, 132),
    "Solo el nombre. Seis familias reales de Google Fonts para comparar personalidad, proporción y lectura.",
    font=subtitle_font,
    fill=MUTED,
)
draw.rectangle((MARGIN, 187, WIDTH - MARGIN, 193), fill=NAVY)
draw.rectangle((MARGIN, 193, MARGIN + 330, 199), fill=GREEN)

for index, (number, name, note, filename, axes, tracking, accent_o) in enumerate(faces):
    row, column = divmod(index, 3)
    x = MARGIN + column * (CARD_W + GAP)
    y = HEADER + row * (CARD_H + GAP)
    draw.rounded_rectangle(
        (x, y, x + CARD_W, y + CARD_H),
        radius=22,
        fill=PAPER,
        outline=LINE,
        width=2,
    )
    draw.text((x + 30, y + 24), f"{number}  {name}", font=label_font, fill=NAVY)
    draw.text((x + 30, y + 58), note, font=note_font, fill=MUTED)
    draw.line((x + 30, y + 98, x + CARD_W - 30, y + 98), fill=LINE, width=2)

    face = fit_face(filename, axes, CARD_W - 82)
    draw_wordmark(
        draw,
        (x + 30, y + 118, x + CARD_W - 30, y + 385),
        face,
        tracking,
        accent_o,
    )

    small = load_font(filename, 47, axes)
    draw_wordmark(
        draw,
        (x + 30, y + 410, x + CARD_W - 30, y + 492),
        small,
        tracking / 2,
        False,
    )
    draw.text((x + 30, y + 500), "Prueba de reducción", font=note_font, fill=MUTED)

output = OUTPUT_DIR / "13-tipografias-google-fonts-sadaco.png"
canvas.save(output, optimize=True)
print(output)
