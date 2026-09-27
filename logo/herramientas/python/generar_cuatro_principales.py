import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
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
TRANSPARENT = (0, 0, 0, 0)


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

# Client-requested Venezuelan cartographic convention including Guayana Esequiba.
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
# Slight closing connects and thickens the eastern extension at logo scale
# while retaining the recognizable political-map silhouette.
venezuela = unary_union([base_venezuela, guayana_esequiba]).buffer(0.10).buffer(-0.10)


def recolor_layer(image: Image.Image, color: tuple[int, int, int, int]) -> Image.Image:
    solid = Image.new("RGBA", image.size, color)
    solid.putalpha(image.getchannel("A"))
    return solid


def draw_geometry(
    draw: ImageDraw.ImageDraw,
    geometry,
    box: tuple[float, float, float, float],
    fill: tuple[int, int, int, int],
) -> None:
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
        if len(points) >= 3:
            draw.polygon(points, fill=fill)


def build_corrected_emblem() -> Image.Image:
    scale = 2
    size = 500 * scale
    center = (250 * scale, 253 * scale)
    radius = 160 * scale

    parent = Image.open(PARENT_EMBLEM).convert("RGBA").resize(
        (size, size), Image.Resampling.LANCZOS
    )

    # Keep only the parent's laurel; replace the original globe completely.
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
    parent.putalpha(alpha)
    laurels = recolor_layer(parent, NAVY)

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
        fill=WHITE,
        outline=NAVY,
        width=10,
    )
    draw_geometry(
        draw,
        venezuela,
        (
            center[0] - 250,
            center[1] - 196,
            center[0] + 250,
            center[1] + 196,
        ),
        GREEN,
    )
    return emblem.resize((500, 500), Image.Resampling.LANCZOS)


def tracked_text(
    draw: ImageDraw.ImageDraw,
    position: tuple[float, float],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    tracking: float,
) -> None:
    x, y = position
    for index, character in enumerate(text):
        draw.text((x, y), character, font=font, fill=fill)
        x += font.getlength(character)
        if index < len(text) - 1:
            x += tracking


def build_corrected_lockup() -> Image.Image:
    lockup = Image.new("RGBA", (1350, 500), TRANSPARENT)
    emblem = build_corrected_emblem().resize((420, 420), Image.Resampling.LANCZOS)
    lockup.alpha_composite(emblem, (10, 40))

    name_font = ImageFont.truetype(FONT_DIR / "Manrope.ttf", 132)
    name_font.set_variation_by_axes([800])
    region_font = ImageFont.truetype(FONT_DIR / "Manrope.ttf", 42)
    region_font.set_variation_by_axes([650])
    draw = ImageDraw.Draw(lockup)
    draw.text((440, 128), "SADACO", font=name_font, fill=NAVY)
    tracked_text(draw, (450, 278), "VENEZUELA", region_font, NAVY, 14)
    return lockup


corrected_emblem = build_corrected_emblem()
corrected_lockup = build_corrected_lockup()
corrected_emblem.save(OUTPUT_DIR / "23-emblema-venezuela-corregido-v3.png", optimize=True)
corrected_lockup.save(OUTPUT_DIR / "23-logo-venezuela-corregido-v3.png", optimize=True)


source = Image.open(THREE_LOGOS).convert("RGB")
logos = [
    source.crop((80, 42, 302, 276)),
    source.crop((390, 38, 615, 276)),
    source.crop((675, 82, 950, 220)),
    corrected_lockup,
]
labels = [
    "01  GLOBO TÉCNICO",
    "02  TEPUI V",
    "03  LOGOTIPO",
    "04  EMBLEMA VENEZUELA",
]

BOARD_WIDTH = 2200
BOARD_HEIGHT = 1500
MARGIN = 90
HEADER = 190
GAP = 44
CARD_W = (BOARD_WIDTH - 2 * MARGIN - GAP) // 2
CARD_H = 600
BACKGROUND = (241, 244, 246)
PAPER = (255, 255, 255)
LINE = (220, 226, 232)
INK = (23, 37, 54)
MUTED = (104, 117, 135)


def windows_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(Path(r"C:\Windows\Fonts") / name, size)


title_font = windows_font("segoeuib.ttf", 58)
subtitle_font = windows_font("segoeui.ttf", 25)
label_font = windows_font("segoeuib.ttf", 22)

board = Image.new("RGB", (BOARD_WIDTH, BOARD_HEIGHT), BACKGROUND)
board_draw = ImageDraw.Draw(board)
board_draw.text(
    (MARGIN, 52),
    "SADACO · CUATRO DIRECCIONES PRINCIPALES",
    font=title_font,
    fill=INK,
)
board_draw.text(
    (MARGIN, 128),
    "Propuestas retocadas y normalizadas para evaluación.",
    font=subtitle_font,
    fill=MUTED,
)
board_draw.rectangle((MARGIN, 176, BOARD_WIDTH - MARGIN, 182), fill=NAVY[:3])
board_draw.rectangle((MARGIN, 182, MARGIN + 330, 188), fill=GREEN[:3])

for index, (logo, label) in enumerate(zip(logos, labels)):
    row, column = divmod(index, 2)
    x = MARGIN + column * (CARD_W + GAP)
    y = HEADER + row * (CARD_H + GAP)
    board_draw.rounded_rectangle(
        (x, y, x + CARD_W, y + CARD_H),
        radius=20,
        fill=PAPER,
        outline=LINE,
        width=2,
    )
    board_draw.text((x + 28, y + 22), label, font=label_font, fill=NAVY[:3])

    converted = logo.convert("RGBA")
    fitted = ImageOps.contain(converted, (CARD_W - 90, CARD_H - 115), Image.Resampling.LANCZOS)
    board.paste(
        fitted,
        (
            x + (CARD_W - fitted.width) // 2,
            y + 76 + (CARD_H - 90 - fitted.height) // 2,
        ),
        fitted if fitted.mode == "RGBA" else None,
    )

output = OUTPUT_DIR / "24-cuatro-logos-principales-v4.png"
board.save(output, optimize=True)
print(output)
