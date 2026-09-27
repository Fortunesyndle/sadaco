import json
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from shapely.geometry import Polygon, shape
from shapely.ops import unary_union


HERRAMIENTAS = Path(__file__).resolve().parents[1]
LOGO = HERRAMIENTAS.parent
ASSETS = Path(
    r"C:\Users\Luis\.cursor\projects"
    r"\c-Users-Luis-OneDrive-Desktop-SADACO\assets"
)
OUTPUT_DIR = LOGO / "bocetos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

THREE_LOGOS = (
    ASSETS
    / "c__Users_Luis_AppData_Roaming_Cursor_User_workspaceStorage_99e8d97b8565766ea2aa305c93e17e70_images_image-b2a99b09-ff96-4291-a2ed-556d0fa34f12.png"
)
PARENT_EMBLEM = (
    ASSETS
    / "c__Users_Luis_AppData_Roaming_Cursor_User_workspaceStorage_99e8d97b8565766ea2aa305c93e17e70_images_sadaco-international-logo-65f7ffed-0adf-4878-9ec7-59df638c538c.png"
)
GEOJSON = HERRAMIENTAS / "datos" / "ne_110m_admin_0_countries.geojson"
FONT_DIR = HERRAMIENTAS / "fonts-google"

NAVY = (11, 63, 122, 255)
GREEN = (19, 139, 101, 255)
WHITE = (255, 255, 255, 255)
INTL_BLUE = (0, 74, 173, 255)
INTL_GREEN = (126, 217, 87, 255)
TRANSPARENT = (0, 0, 0, 0)


def load_variable_font(
    filename: str, size: int, axes: list[int]
) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(FONT_DIR / filename, size)
    font.set_variation_by_axes(axes)
    return font


def tracked_text_width(
    text: str, font: ImageFont.FreeTypeFont, tracking: float
) -> float:
    return sum(font.getlength(character) for character in text) + tracking * (
        len(text) - 1
    )


def draw_tracked_centered(
    draw: ImageDraw.ImageDraw,
    center_x: float,
    y: float,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill,
    tracking: float,
) -> None:
    x = center_x - tracked_text_width(text, font, tracking) / 2
    for index, character in enumerate(text):
        draw.text((x, y), character, font=font, fill=fill)
        x += font.getlength(character)
        if index < len(text) - 1:
            x += tracking


NAME_FONT = load_variable_font("SpaceGrotesk.ttf", 136, [700])
REGION_FONT = load_variable_font("Manrope.ttf", 39, [650])


def draw_globe_grid(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    radius: int,
    line_width: int,
) -> None:
    cx, cy = center
    for ellipse_width in (int(radius * 0.70), int(radius * 1.30)):
        draw.ellipse(
            (
                cx - ellipse_width // 2,
                cy - radius,
                cx + ellipse_width // 2,
                cy + radius,
            ),
            outline=WHITE,
            width=line_width,
        )
    for latitude in (-0.56, -0.28, 0.0, 0.28, 0.56):
        y = cy + int(latitude * radius)
        half = int(math.sqrt(max(radius * radius - (y - cy) ** 2, 0)))
        draw.line((cx - half, y, cx + half, y), fill=WHITE, width=line_width)
    draw.ellipse(
        (cx - radius, cy - radius, cx + radius, cy + radius),
        outline=WHITE,
        width=line_width + 2,
    )


def draw_quiet_globe_grid(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    radius: int,
    line_width: int,
) -> None:
    """Minimal grid for the emblem: one meridian pair and the equator."""
    cx, cy = center
    half = int(radius * 0.55)
    draw.ellipse((cx - half, cy - radius, cx + half, cy + radius), outline=WHITE, width=line_width)
    draw.line((cx - radius, cy, cx + radius, cy), fill=WHITE, width=line_width)


def extract_previous_wordmark(crop_box: tuple[int, int, int, int]) -> Image.Image:
    source = Image.open(THREE_LOGOS).convert("RGB").crop(crop_box)
    array = np.array(source)
    darkness = 255 - np.min(array, axis=2)
    alpha = np.clip(darkness * 1.55, 0, 255).astype(np.uint8)
    colored = Image.new("RGBA", source.size, TRANSPARENT)
    pixels = colored.load()
    for py in range(source.height):
        for px in range(source.width):
            red, green, blue = array[py, px]
            if alpha[py, px] < 8:
                continue
            target = (
                GREEN
                if int(green) > int(blue) and int(green) > int(red) + 12
                else NAVY
            )
            pixels[px, py] = (*target[:3], int(alpha[py, px]))
    bbox = colored.getchannel("A").getbbox()
    return colored.crop(bbox) if bbox else colored


def build_oil_globe_logo() -> Image.Image:
    image = Image.new("RGBA", (1400, 1080), TRANSPARENT)
    draw = ImageDraw.Draw(image)
    cx, cy, radius = 700, 300, 220
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=NAVY)
    draw_globe_grid(draw, (cx, cy), radius, 6)

    # White drilling derrick: mast, working platform and cross-bracing.
    apex_y = cy - 152
    base_y = cy + 165
    left_base = cx - 86
    right_base = cx + 86
    draw.line((cx - 16, apex_y, left_base, base_y), fill=WHITE, width=10)
    draw.line((cx + 16, apex_y, right_base, base_y), fill=WHITE, width=10)
    draw.rectangle((cx - 35, apex_y - 22, cx + 35, apex_y - 8), fill=WHITE)
    draw.rectangle((cx - 52, apex_y + 18, cx + 52, apex_y + 34), fill=WHITE)
    draw.rectangle((left_base - 24, base_y, right_base + 24, base_y + 14), fill=WHITE)
    draw.line((cx, apex_y - 8, cx, base_y + 4), fill=WHITE, width=7)

    levels = [apex_y + 58, apex_y + 105, apex_y + 154, apex_y + 205, apex_y + 258]
    previous_left, previous_right, previous_y = cx - 24, cx + 24, apex_y + 34
    for level in levels:
        ratio = (level - apex_y) / (base_y - apex_y)
        current_left = int(cx - 16 - ratio * 70)
        current_right = int(cx + 16 + ratio * 70)
        draw.line((current_left, level, current_right, level), fill=WHITE, width=6)
        draw.line(
            (previous_left, previous_y, current_right, level),
            fill=WHITE,
            width=4,
        )
        draw.line(
            (previous_right, previous_y, current_left, level),
            fill=WHITE,
            width=4,
        )
        previous_left, previous_right, previous_y = current_left, current_right, level

    # Crown block and suspended drill line make the object read as petroleum equipment.
    draw.rounded_rectangle(
        (cx - 24, apex_y + 39, cx + 24, apex_y + 76),
        radius=7,
        outline=WHITE,
        width=6,
    )
    draw.line((cx, apex_y + 76, cx, base_y + 35), fill=WHITE, width=4)
    draw.polygon(
        ((cx - 10, base_y + 35), (cx + 10, base_y + 35), (cx, base_y + 58)),
        fill=WHITE,
    )

    previous_wordmark = extract_previous_wordmark((80, 188, 305, 274))
    target_width = 690
    target_height = round(previous_wordmark.height * target_width / previous_wordmark.width)
    previous_wordmark = previous_wordmark.resize(
        (target_width, target_height),
        Image.Resampling.LANCZOS,
    )
    image.alpha_composite(
        previous_wordmark,
        (
            int(700 - previous_wordmark.width / 2),
            610,
        ),
    )
    return image


def build_tepui_logo() -> Image.Image:
    image = Image.new("RGBA", (1400, 1080), TRANSPARENT)
    draw = ImageDraw.Draw(image)

    # Structural V.
    draw.polygon(
        (
            (430, 260),
            (970, 260),
            (900, 365),
            (796, 574),
            (604, 574),
            (500, 365),
        ),
        fill=NAVY,
    )
    # Negative V cut.
    draw.polygon(
        ((550, 294), (850, 294), (700, 492)),
        fill=WHITE,
    )
    # Flat tepui summit plane.
    draw.polygon(
        ((410, 242), (700, 138), (990, 242), (864, 286), (536, 286)),
        fill=GREEN,
    )

    draw_tracked_centered(draw, 700, 610, "SADACO", NAME_FONT, NAVY, 3)
    draw_tracked_centered(draw, 700, 785, "VENEZUELA", REGION_FONT, NAVY, 17)
    return image


def vectorize_wordmark() -> Image.Image:
    image = Image.new("RGBA", (1900, 650), TRANSPARENT)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_DIR / "Michroma-Regular.ttf", 184)
    region_font = load_variable_font("Manrope.ttf", 53, [600])

    navy_text = "SADAC"
    navy_width = font.getlength(navy_text)
    o_width = font.getlength("O")
    spacing = 4
    total_width = navy_width + spacing + o_width
    start_x = (image.width - total_width) / 2
    baseline_y = 85

    draw.text((start_x, baseline_y), navy_text, font=font, fill=NAVY)
    o_x = start_x + navy_width + spacing
    draw.text((o_x, baseline_y), "O", font=font, fill=GREEN)

    # Proprietary O detail: a deliberately thin central axis.
    o_bbox = draw.textbbox((o_x, baseline_y), "O", font=font)
    center_x = (o_bbox[0] + o_bbox[2]) / 2
    draw.line(
        (center_x, o_bbox[1] + 10, center_x, o_bbox[3] - 10),
        fill=GREEN,
        width=5,
    )

    draw_tracked_centered(
        draw,
        image.width / 2,
        345,
        "VENEZUELA",
        region_font,
        GREEN,
        24,
    )

    bbox = image.getchannel("A").getbbox()
    if bbox:
        left, top, right, bottom = bbox
        image = image.crop(
            (max(0, left - 20), max(0, top - 20), min(image.width, right + 20), min(image.height, bottom + 20))
        )
    return image


with GEOJSON.open(encoding="utf-8") as handle:
    countries = json.load(handle)

base_venezuela = next(
    shape(feature["geometry"])
    for feature in countries["features"]
    if feature["properties"].get("ADM0_A3") == "VEN"
)
guyana = next(
    shape(feature["geometry"])
    for feature in countries["features"]
    if feature["properties"].get("ADM0_A3") == "GUY"
)
essequibo_west = Polygon(
    [
        (-58.45, 7.10),
        (-58.55, 6.75),
        (-58.62, 6.35),
        (-58.72, 5.95),
        (-58.78, 5.55),
        (-58.66, 5.15),
        (-58.58, 4.75),
        (-58.48, 4.30),
        (-58.30, 3.85),
        (-58.18, 3.35),
        (-58.30, 2.85),
        (-58.55, 2.35),
        (-58.84, 1.82),
        (-59.10, 1.35),
        (-64.00, 1.00),
        (-64.00, 9.00),
        (-58.45, 9.00),
    ]
)
guayana_esequiba = guyana.intersection(essequibo_west.buffer(0.28))
venezuela = unary_union([base_venezuela, guayana_esequiba]).buffer(0.10).buffer(-0.10)


def draw_geometry_mask(size: int, geometry, box) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    min_lon, min_lat, max_lon, max_lat = geometry.bounds
    left, top, right, bottom = box
    scale = min(
        (right - left) / (max_lon - min_lon),
        (bottom - top) / (max_lat - min_lat),
    )
    width = (max_lon - min_lon) * scale
    height = (max_lat - min_lat) * scale
    offset_x = left + (right - left - width) / 2
    offset_y = top + (bottom - top - height) / 2
    polygons = list(geometry.geoms) if geometry.geom_type == "MultiPolygon" else [geometry]
    for polygon in polygons:
        points = [
            (
                offset_x + (lon - min_lon) * scale,
                offset_y + (max_lat - lat) * scale,
            )
            for lon, lat in polygon.exterior.coords
        ]
        draw.polygon(points, fill=255)
    return mask


def recolor_laurels(parent: Image.Image, center, radius) -> Image.Image:
    alpha = parent.getchannel("A")
    alpha_draw = ImageDraw.Draw(alpha)
    alpha_draw.ellipse(
        (
            center[0] - radius - 8,
            center[1] - radius - 8,
            center[0] + radius + 8,
            center[1] + radius + 8,
        ),
        fill=0,
    )
    layer = Image.new("RGBA", parent.size, INTL_BLUE)
    layer.putalpha(alpha)
    return layer


def build_matrix_inspired_emblem() -> Image.Image:
    scale = 2
    size = 1000
    center = (500, 506)
    radius = 320
    parent = Image.open(PARENT_EMBLEM).convert("RGBA").resize(
        (size, size), Image.Resampling.LANCZOS
    )
    laurels = recolor_laurels(parent, center, radius)
    emblem = Image.new("RGBA", (size, size), TRANSPARENT)
    emblem.alpha_composite(laurels)
    draw = ImageDraw.Draw(emblem)

    draw.ellipse(
        (
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        ),
        fill=INTL_BLUE,
        outline=WHITE,
        width=9,
    )
    draw_quiet_globe_grid(draw, center, radius - 10, 4)

    country_mask = draw_geometry_mask(
        size,
        venezuela,
        (
            center[0] - 252,
            center[1] - 198,
            center[0] + 252,
            center[1] + 198,
        ),
    )
    country_outline = country_mask.filter(ImageFilter.MaxFilter(21))
    emblem.paste(WHITE, (0, 0, size, size), country_outline)
    emblem.paste(INTL_GREEN, (0, 0, size, size), country_mask)

    outer = ImageDraw.Draw(emblem)
    outer.ellipse(
        (
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        ),
        outline=INTL_BLUE,
        width=8,
    )
    return emblem.resize((500, 500), Image.Resampling.LANCZOS)


def build_emblem_lockup() -> Image.Image:
    image = Image.new("RGBA", (1450, 520), TRANSPARENT)
    emblem = build_matrix_inspired_emblem().resize((430, 430), Image.Resampling.LANCZOS)
    image.alpha_composite(emblem, (10, 45))
    draw = ImageDraw.Draw(image)
    name_font = load_variable_font("Manrope.ttf", 132, [800])
    draw.text((450, 190), "SADACO", font=name_font, fill=INTL_BLUE)
    return image


previous_source = Image.open(THREE_LOGOS).convert("RGBA")
previous_tepui = previous_source.crop((390, 38, 615, 276))
previous_wordmark = previous_source.crop((675, 82, 950, 220))

logos = [
    build_oil_globe_logo(),
    previous_tepui,
    previous_wordmark,
    build_emblem_lockup(),
]
filenames = [
    "30-01-globo-petrolero-tipografia-original.png",
    "30-02-tepui-original.png",
    "30-03-logotipo-original.png",
    "30-04-emblema-globo-simplificado.png",
]

for logo, filename in zip(logos, filenames):
    logo.save(LOGO / "entregables" / "png-sin-fondo" / "direcciones" / filename, optimize=True)


MARGIN = 90
GAP = 44
BOARD_WIDTH = 2400
CARD_W = (BOARD_WIDTH - 2 * MARGIN - GAP) // 2
CARD_H = 670
BOARD_HEIGHT = 2 * MARGIN + 2 * CARD_H + GAP
BACKGROUND = (241, 244, 246)
PAPER = (255, 255, 255)
LINE = (220, 226, 232)

board = Image.new("RGB", (BOARD_WIDTH, BOARD_HEIGHT), BACKGROUND)
board_draw = ImageDraw.Draw(board)

for index, logo in enumerate(logos):
    row, column = divmod(index, 2)
    x = MARGIN + column * (CARD_W + GAP)
    y = MARGIN + row * (CARD_H + GAP)
    board_draw.rounded_rectangle(
        (x, y, x + CARD_W, y + CARD_H),
        radius=20,
        fill=PAPER,
        outline=LINE,
        width=2,
    )
    fitted = ImageOps.contain(
        logo.convert("RGBA"),
        (CARD_W - 100, CARD_H - 110),
        Image.Resampling.LANCZOS,
    )
    board.paste(
        fitted,
        (
            x + (CARD_W - fitted.width) // 2,
            y + (CARD_H - fitted.height) // 2,
        ),
        fitted,
    )

PRESENTATION_DIR = LOGO / "entregables" / "presentacion"
PRESENTATION_DIR.mkdir(exist_ok=True)
output = PRESENTATION_DIR / "03-cuatro-direcciones.png"
board.save(output, optimize=True)
print(output)
