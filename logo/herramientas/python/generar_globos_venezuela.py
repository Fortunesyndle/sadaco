import json
import math
from pathlib import Path

import numpy as np
import shapely
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from shapely.geometry import Polygon, shape
from shapely.ops import unary_union


HERRAMIENTAS = Path(__file__).resolve().parents[1]
LOGO = HERRAMIENTAS.parent
ASSETS = Path(
    r"C:\Users\Luis\.cursor\projects"
    r"\c-Users-Luis-OneDrive-Desktop-SADACO\assets"
)
SOURCE = (
    ASSETS
    / "c__Users_Luis_AppData_Roaming_Cursor_User_workspaceStorage_99e8d97b8565766ea2aa305c93e17e70_images_sadaco-international-logo-65f7ffed-0adf-4878-9ec7-59df638c538c.png"
)
GEOJSON = HERRAMIENTAS / "datos" / "ne_110m_admin_0_countries.geojson"
OUTPUT_DIR = LOGO / "bocetos" / "globo-venezuela"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BLUE = (0, 74, 173, 255)
GREEN = (126, 217, 87, 255)
DEEP_GREEN = (19, 139, 101, 255)
RED = (207, 20, 43, 255)
FLAG_YELLOW = (255, 204, 0, 255)
FLAG_BLUE = (0, 36, 125, 255)
FLAG_RED = (207, 20, 43, 255)
WHITE = (255, 255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)

LON0 = -75.0
LAT0 = 10.0
SUPERSAMPLE = 2
GLOBE_SIZE = 640
GLOBE_RADIUS = 314


with GEOJSON.open(encoding="utf-8") as handle:
    data = json.load(handle)

geometries = [shape(feature["geometry"]) for feature in data["features"]]
land_geometry = unary_union(geometries)
base_venezuela_geometry = next(
    shape(feature["geometry"])
    for feature in data["features"]
    if feature["properties"].get("ADM0_A3") == "VEN"
)
guyana_geometry = next(
    shape(feature["geometry"])
    for feature in data["features"]
    if feature["properties"].get("ADM0_A3") == "GUY"
)

# Guayana Esequiba treatment requested by the client. The eastern edge follows
# the Essequibo River at the visual precision needed for this small globe.
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
guayana_esequiba_geometry = guyana_geometry.intersection(essequibo_west)
venezuela_geometry = unary_union(
    [base_venezuela_geometry, guayana_esequiba_geometry]
)


def inverse_orthographic(size: int, radius: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    yy, xx = np.mgrid[0:size, 0:size]
    x = (xx + 0.5 - size / 2) / radius
    y = (size / 2 - (yy + 0.5)) / radius
    rho = np.sqrt(x * x + y * y)
    inside = rho <= 1.0
    safe_rho = np.where(rho == 0, 1.0, rho)
    c = np.arcsin(np.clip(rho, 0, 1))

    lat0 = math.radians(LAT0)
    lon0 = math.radians(LON0)
    latitude = np.arcsin(
        np.cos(c) * math.sin(lat0)
        + (y * np.sin(c) * math.cos(lat0) / safe_rho)
    )
    longitude = lon0 + np.arctan2(
        x * np.sin(c),
        safe_rho * math.cos(lat0) * np.cos(c)
        - y * math.sin(lat0) * np.sin(c),
    )
    latitude = np.degrees(latitude)
    longitude = ((np.degrees(longitude) + 180) % 360) - 180
    return longitude, latitude, inside


longitude, latitude, inside_globe = inverse_orthographic(GLOBE_SIZE, GLOBE_RADIUS)
land_mask_array = shapely.contains_xy(land_geometry, longitude, latitude) & inside_globe
venezuela_mask_array = (
    shapely.contains_xy(venezuela_geometry, longitude, latitude) & inside_globe
)


def mask_image(mask: np.ndarray) -> Image.Image:
    return Image.fromarray((mask.astype(np.uint8) * 255), mode="L")


land_mask = mask_image(land_mask_array)
venezuela_mask = mask_image(venezuela_mask_array)
venezuela_dilated = venezuela_mask.filter(ImageFilter.MaxFilter(17))
venezuela_outline = Image.fromarray(
    np.maximum(
        np.array(venezuela_dilated, dtype=np.int16)
        - np.array(venezuela_mask, dtype=np.int16),
        0,
    ).astype(np.uint8),
    mode="L",
)


def project(longitude_deg: float, latitude_deg: float) -> tuple[float, float, bool]:
    lon = math.radians(longitude_deg)
    lat = math.radians(latitude_deg)
    lon0 = math.radians(LON0)
    lat0 = math.radians(LAT0)
    delta = lon - lon0
    visibility = (
        math.sin(lat0) * math.sin(lat)
        + math.cos(lat0) * math.cos(lat) * math.cos(delta)
    )
    x = math.cos(lat) * math.sin(delta)
    y = (
        math.cos(lat0) * math.sin(lat)
        - math.sin(lat0) * math.cos(lat) * math.cos(delta)
    )
    return (
        GLOBE_SIZE / 2 + GLOBE_RADIUS * x,
        GLOBE_SIZE / 2 - GLOBE_RADIUS * y,
        visibility >= 0,
    )


def draw_graticules(image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)

    def draw_curve(points: list[tuple[float, float, bool]]) -> None:
        segment: list[tuple[float, float]] = []
        for px, py, visible in points:
            if visible:
                segment.append((px, py))
            elif len(segment) > 1:
                draw.line(segment, fill=WHITE, width=3, joint="curve")
                segment = []
            else:
                segment = []
        if len(segment) > 1:
            draw.line(segment, fill=WHITE, width=3, joint="curve")

    for lon in range(-180, 181, 20):
        draw_curve([project(lon, lat) for lat in np.linspace(-89, 89, 260)])
    for lat in range(-75, 76, 15):
        draw_curve([project(lon, lat) for lon in np.linspace(-180, 180, 520)])


def base_globe() -> Image.Image:
    globe = Image.new("RGBA", (GLOBE_SIZE, GLOBE_SIZE), TRANSPARENT)
    circle = Image.new("L", (GLOBE_SIZE, GLOBE_SIZE), 0)
    circle_draw = ImageDraw.Draw(circle)
    inset = GLOBE_SIZE / 2 - GLOBE_RADIUS
    circle_draw.ellipse(
        (inset, inset, GLOBE_SIZE - inset, GLOBE_SIZE - inset),
        fill=255,
    )
    globe.paste(BLUE, (0, 0, GLOBE_SIZE, GLOBE_SIZE), circle)
    globe.paste(GREEN, (0, 0, GLOBE_SIZE, GLOBE_SIZE), land_mask)
    draw_graticules(globe)
    outer = ImageDraw.Draw(globe)
    outer.ellipse(
        (inset, inset, GLOBE_SIZE - inset, GLOBE_SIZE - inset),
        outline=WHITE,
        width=6,
    )
    return globe


def apply_country_treatment(globe: Image.Image, variant: int) -> None:
    draw = ImageDraw.Draw(globe)
    center_x, center_y, _ = project(-66.5, 7.0)

    if variant == 1:
        globe.paste(WHITE, (0, 0, GLOBE_SIZE, GLOBE_SIZE), venezuela_mask)
    elif variant == 2:
        globe.paste(WHITE, (0, 0, GLOBE_SIZE, GLOBE_SIZE), venezuela_outline)
        globe.paste(BLUE, (0, 0, GLOBE_SIZE, GLOBE_SIZE), venezuela_mask)
    elif variant == 3:
        globe.paste(WHITE, (0, 0, GLOBE_SIZE, GLOBE_SIZE), venezuela_outline)
        globe.paste(DEEP_GREEN, (0, 0, GLOBE_SIZE, GLOBE_SIZE), venezuela_mask)
    elif variant == 4:
        radius = 33
        draw.ellipse(
            (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
            outline=WHITE,
            width=8,
        )
        draw.ellipse(
            (center_x - 10, center_y - 10, center_x + 10, center_y + 10),
            fill=DEEP_GREEN,
            outline=WHITE,
            width=3,
        )
    elif variant == 5:
        radius = 34
        draw.ellipse(
            (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
            fill=WHITE,
            outline=BLUE,
            width=5,
        )
        draw.line(
            (
                center_x - 17,
                center_y - 10,
                center_x,
                center_y + 16,
                center_x + 18,
                center_y - 10,
            ),
            fill=DEEP_GREEN,
            width=9,
            joint="curve",
        )
    elif variant == 6:
        radius = 30
        draw.ellipse(
            (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
            outline=WHITE,
            width=5,
        )
        draw.line((center_x - 48, center_y, center_x + 48, center_y), fill=WHITE, width=4)
        draw.line((center_x, center_y - 48, center_x, center_y + 48), fill=WHITE, width=4)
        draw.ellipse(
            (center_x - 8, center_y - 8, center_x + 8, center_y + 8),
            fill=DEEP_GREEN,
        )
    elif variant == 7:
        globe.paste(WHITE, (0, 0, GLOBE_SIZE, GLOBE_SIZE), venezuela_outline)
        globe.paste(RED, (0, 0, GLOBE_SIZE, GLOBE_SIZE), venezuela_mask)
    elif variant == 8:
        globe.paste(WHITE, (0, 0, GLOBE_SIZE, GLOBE_SIZE), venezuela_outline)
        flag = Image.new("RGBA", (GLOBE_SIZE, GLOBE_SIZE), TRANSPARENT)
        flag_draw = ImageDraw.Draw(flag)
        left, top, right, bottom = venezuela_mask.getbbox()
        third = (bottom - top) / 3
        flag_draw.rectangle((left, top, right, top + third), fill=FLAG_YELLOW)
        flag_draw.rectangle((left, top + third, right, top + 2 * third), fill=FLAG_BLUE)
        flag_draw.rectangle((left, top + 2 * third, right, bottom), fill=FLAG_RED)
        globe.paste(flag, (0, 0), venezuela_mask)
    elif variant == 9:
        pin_y = center_y - 48
        radius = 31
        draw.polygon(
            (
                (center_x - 22, pin_y + 18),
                (center_x + 22, pin_y + 18),
                (center_x, center_y + 7),
            ),
            fill=RED,
        )
        draw.ellipse(
            (center_x - radius, pin_y - radius, center_x + radius, pin_y + radius),
            fill=RED,
            outline=WHITE,
            width=5,
        )
        draw.ellipse(
            (center_x - 9, pin_y - 9, center_x + 9, pin_y + 9),
            fill=WHITE,
        )
    elif variant == 10:
        pin_y = center_y - 48
        radius = 31
        draw.polygon(
            (
                (center_x - 22, pin_y + 18),
                (center_x + 22, pin_y + 18),
                (center_x, center_y + 7),
            ),
            fill=BLUE,
        )
        draw.ellipse(
            (center_x - radius, pin_y - radius, center_x + radius, pin_y + radius),
            fill=BLUE,
            outline=WHITE,
            width=5,
        )
        draw.ellipse(
            (center_x - 12, pin_y - 12, center_x + 12, pin_y + 12),
            fill=DEEP_GREEN,
            outline=WHITE,
            width=4,
        )


def build_emblem(variant: int) -> Image.Image:
    source = Image.open(SOURCE).convert("RGBA")
    large = source.resize(
        (source.width * SUPERSAMPLE, source.height * SUPERSAMPLE),
        Image.Resampling.LANCZOS,
    )
    globe = base_globe()
    apply_country_treatment(globe, variant)

    # Exact globe location measured from the supplied parent emblem.
    large.alpha_composite(globe, (180, 188))
    return large.resize(source.size, Image.Resampling.LANCZOS)


VARIANTS = [
    (1, "PAÍS EN BLANCO"),
    (2, "AZUL + CONTORNO"),
    (3, "VERDE PROFUNDO + CONTORNO"),
    (4, "LOCALIZADOR CIRCULAR"),
    (5, "MARCADOR V"),
    (6, "MIRA GEOGRÁFICA"),
]

emblems: list[Image.Image] = []
for number, _ in VARIANTS:
    emblem = build_emblem(number)
    emblem.save(OUTPUT_DIR / f"{number:02d}-venezuela.png", optimize=True)
    emblems.append(emblem)


BOARD_WIDTH = 2400
BOARD_HEIGHT = 1760
MARGIN = 90
HEADER = 190
GAP = 42
CARD_W = (BOARD_WIDTH - 2 * MARGIN - 2 * GAP) // 3
CARD_H = 690
PAPER = (255, 255, 255)
BACKGROUND = (241, 244, 246)
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
    "SADACO · VENEZUELA EN EL EMBLEMA INTERNATIONAL",
    font=title_font,
    fill=INK,
)
board_draw.text(
    (MARGIN, 128),
    "América centrada. Se conserva el globo, la grilla, el laurel y la paleta de la marca matriz.",
    font=subtitle_font,
    fill=MUTED,
)
board_draw.rectangle((MARGIN, 176, BOARD_WIDTH - MARGIN, 182), fill=BLUE[:3])
board_draw.rectangle((MARGIN, 182, MARGIN + 330, 188), fill=GREEN[:3])

for index, ((number, label), emblem) in enumerate(zip(VARIANTS, emblems)):
    row, column = divmod(index, 3)
    x = MARGIN + column * (CARD_W + GAP)
    y = HEADER + row * (CARD_H + GAP)
    board_draw.rounded_rectangle(
        (x, y, x + CARD_W, y + CARD_H),
        radius=20,
        fill=PAPER,
        outline=LINE,
        width=2,
    )
    board_draw.text(
        (x + 28, y + 22),
        f"{number:02d}  {label}",
        font=label_font,
        fill=BLUE[:3],
    )
    resized = emblem.resize((510, 510), Image.Resampling.LANCZOS)
    board.paste(
        resized,
        (x + (CARD_W - resized.width) // 2, y + 100),
        resized,
    )

board_output = LOGO / "bocetos" / "21-venezuela-emblema-international-v3.png"
board.save(board_output, optimize=True)


SPECIAL_VARIANTS = [
    (7, "ROJO + CONTORNO"),
    (8, "TRICOLOR VENEZOLANO"),
    (9, "PIN ROJO"),
    (10, "PIN CORPORATIVO"),
]

special_emblems: list[Image.Image] = []
for number, _ in SPECIAL_VARIANTS:
    emblem = build_emblem(number)
    emblem.save(OUTPUT_DIR / f"{number:02d}-venezuela.png", optimize=True)
    special_emblems.append(emblem)

SPECIAL_WIDTH = 2000
SPECIAL_HEIGHT = 1540
SPECIAL_MARGIN = 90
SPECIAL_HEADER = 190
SPECIAL_GAP = 42
SPECIAL_CARD_W = (SPECIAL_WIDTH - 2 * SPECIAL_MARGIN - SPECIAL_GAP) // 2
SPECIAL_CARD_H = 620

special_board = Image.new("RGB", (SPECIAL_WIDTH, SPECIAL_HEIGHT), BACKGROUND)
special_draw = ImageDraw.Draw(special_board)
special_draw.text(
    (SPECIAL_MARGIN, 52),
    "SADACO · CUATRO FORMAS DE MARCAR VENEZUELA",
    font=title_font,
    fill=INK,
)
special_draw.text(
    (SPECIAL_MARGIN, 128),
    "Variaciones de color y localización sobre el emblema de SADACO International.",
    font=subtitle_font,
    fill=MUTED,
)
special_draw.rectangle(
    (SPECIAL_MARGIN, 176, SPECIAL_WIDTH - SPECIAL_MARGIN, 182),
    fill=BLUE[:3],
)
special_draw.rectangle(
    (SPECIAL_MARGIN, 182, SPECIAL_MARGIN + 330, 188),
    fill=GREEN[:3],
)

for index, ((number, label), emblem) in enumerate(
    zip(SPECIAL_VARIANTS, special_emblems)
):
    row, column = divmod(index, 2)
    x = SPECIAL_MARGIN + column * (SPECIAL_CARD_W + SPECIAL_GAP)
    y = SPECIAL_HEADER + row * (SPECIAL_CARD_H + SPECIAL_GAP)
    special_draw.rounded_rectangle(
        (x, y, x + SPECIAL_CARD_W, y + SPECIAL_CARD_H),
        radius=20,
        fill=PAPER,
        outline=LINE,
        width=2,
    )
    special_draw.text(
        (x + 28, y + 22),
        f"{index + 1:02d}  {label}",
        font=label_font,
        fill=BLUE[:3],
    )
    resized = emblem.resize((500, 500), Image.Resampling.LANCZOS)
    special_board.paste(
        resized,
        (x + (SPECIAL_CARD_W - resized.width) // 2, y + 86),
        resized,
    )

special_output = LOGO / "bocetos" / "22-venezuela-rojo-bandera-pines-v3.png"
special_board.save(special_output, optimize=True)
print(special_output)
