from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ASSET_DIR = Path(
    r"C:\Users\Luis\.cursor\projects"
    r"\c-Users-Luis-OneDrive-Desktop-SADACO\assets"
)
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "bocetos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DOUBLE_SOURCE = (
    ASSET_DIR
    / "c__Users_Luis_AppData_Roaming_Cursor_User_workspaceStorage_99e8d97b8565766ea2aa305c93e17e70_images_image-bff83e2d-d15f-4d86-bb0c-6e0070c5a5d7.png"
)

SOURCES = [
    (
        ASSET_DIR
        / "c__Users_Luis_AppData_Roaming_Cursor_User_workspaceStorage_99e8d97b8565766ea2aa305c93e17e70_images_image-7ebca125-4ec8-4844-a5b3-bf22054d9918.png",
        None,
        False,
    ),
    (
        ASSET_DIR
        / "c__Users_Luis_AppData_Roaming_Cursor_User_workspaceStorage_99e8d97b8565766ea2aa305c93e17e70_images_image-71cf0a20-9275-466f-8f92-5d9e945925c2.png",
        None,
        False,
    ),
    (
        ASSET_DIR
        / "c__Users_Luis_AppData_Roaming_Cursor_User_workspaceStorage_99e8d97b8565766ea2aa305c93e17e70_images_image-b5df89ab-118d-4fc8-94f5-16e010a9cfe9.png",
        None,
        False,
    ),
    (
        ASSET_DIR
        / "c__Users_Luis_AppData_Roaming_Cursor_User_workspaceStorage_99e8d97b8565766ea2aa305c93e17e70_images_image-246c578d-5709-4470-8f93-f775721be860.png",
        None,
        False,
    ),
    (DOUBLE_SOURCE, (60, 30, 400, 275), True),
    (DOUBLE_SOURCE, (470, 25, 820, 278), False),
    (
        ASSET_DIR
        / "c__Users_Luis_AppData_Roaming_Cursor_User_workspaceStorage_99e8d97b8565766ea2aa305c93e17e70_images_image-652eb163-0c57-460a-9f1a-9b7f16621f31.png",
        (20, 30, 400, 225),
        False,
    ),
]

WIDTH = 2800
HEIGHT = 1500
MARGIN = 80
HEADER = 180
GAP = 32
CARD_W = (WIDTH - 2 * MARGIN - 3 * GAP) // 4
CARD_H = 590

NAVY = "#0B3F7A"
GREEN = "#138B65"
INK = "#172536"
LINE = "#DCE2E8"
BACKGROUND = "#F1F4F6"
WHITE = "#FFFFFF"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(Path(r"C:\Windows\Fonts") / name, size)


title_font = font("segoeuib.ttf", 58)
subtitle_font = font("segoeui.ttf", 24)
number_font = font("segoeuib.ttf", 22)

canvas = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
draw = ImageDraw.Draw(canvas)

draw.text((MARGIN, 52), "SADACO · MODELOS SELECCIONADOS", font=title_font, fill=INK)
draw.text(
    (MARGIN, 128),
    "Siete propuestas independientes para la siguiente ronda de evaluación.",
    font=subtitle_font,
    fill="#687587",
)
draw.rectangle((MARGIN, 176, WIDTH - MARGIN, 182), fill=NAVY)
draw.rectangle((MARGIN, 182, MARGIN + 330, 188), fill=GREEN)

def normalize_globe_colors(image: Image.Image) -> Image.Image:
    """Make the globe and SADACO navy, leaving VENEZUELA as the green accent."""
    normalized = image.copy().convert("RGB")
    pixels = normalized.load()
    target_navy = (11, 63, 122)
    target_green = (19, 139, 101)

    for py in range(normalized.height):
        for px in range(normalized.width):
            red, green, blue = pixels[px, py]
            spread = max(red, green, blue) - min(red, green, blue)
            if spread < 22 or max(red, green, blue) > 248:
                continue

            target = target_green if py >= 218 else target_navy
            opacity = (255 - min(red, green, blue)) / 255
            opacity = max(0.0, min(1.0, opacity))
            pixels[px, py] = tuple(
                round(opacity * channel + (1 - opacity) * 255) for channel in target
            )

    return normalized


for index, (source, crop, normalize_colors) in enumerate(SOURCES):
    row, column = divmod(index, 4)
    row_count = 4 if row == 0 else 3
    row_width = row_count * CARD_W + (row_count - 1) * GAP
    row_start = (WIDTH - row_width) // 2
    x = row_start + column * (CARD_W + GAP)
    y = HEADER + row * (CARD_H + GAP)

    draw.rounded_rectangle(
        (x, y, x + CARD_W, y + CARD_H),
        radius=20,
        fill=WHITE,
        outline=LINE,
        width=2,
    )
    draw.text((x + 24, y + 20), f"{index + 1:02d}", font=number_font, fill=NAVY)

    image = Image.open(source).convert("RGB")
    if crop:
        image = image.crop(crop)
    if normalize_colors:
        image = normalize_globe_colors(image)
    fitted = ImageOps.contain(image, (CARD_W - 52, CARD_H - 86), Image.Resampling.LANCZOS)
    image_x = x + (CARD_W - fitted.width) // 2
    image_y = y + 58 + (CARD_H - 70 - fitted.height) // 2
    canvas.paste(fitted, (image_x, image_y))

output = OUTPUT_DIR / "20-modelos-limpios-globo-azul-v2.png"
canvas.save(output, optimize=True)
print(output)
