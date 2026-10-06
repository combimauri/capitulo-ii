"""Prueba de arte: el piso del protagonista (320x180), generado por código.

Uso: python3 art/pruebas/piso.py
Salida: art/pruebas/piso.png (1x) y art/pruebas/piso@4x.png (vista previa)
"""
import random
from pathlib import Path
from PIL import Image, ImageDraw

W, H = 320, 180
OUT = Path(__file__).parent
random.seed(1984)

# --- Paleta del juego (prueba) -------------------------------------------
PAL = [
    "#0e0f12", "#1b1d22", "#2a2d33", "#3c4047", "#555a61", "#737980",  # 0-5 grises Partido
    "#969ca1", "#c2c6c4", "#e6e4dc",                                    # 6-8 claros / ministerios
    "#0f2a22", "#1e4a3a", "#3f7a5c", "#8fc79a",                         # 9-12 telepantalla
    "#4a0f12", "#8a1c1f", "#c8342c",                                    # 13-15 rojo propaganda
    "#1d2a44", "#2f4468", "#4b6694",                                    # 16-18 mono azul
    "#3b2a1e", "#5e4430", "#8a6a45", "#c19a62",                         # 19-22 ocres prole
    "#6e4a3a", "#a77b62", "#d6aa8a",                                    # 23-25 piel
    "#e8c96a",                                                          # 26 luz cálida
]
RGB = [tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) for h in PAL]
C = lambda i: RGB[i]

img = Image.new("RGB", (W, H), C(3))
d = ImageDraw.Draw(img)

# --- Pared con papel pintado ----------------------------------------------
WALL_BOTTOM = 134
d.rectangle([0, 0, W, WALL_BOTTOM], fill=C(4))
for x in range(0, W, 8):
    d.line([x, 0, x, WALL_BOTTOM], fill=C(3))
    for y in range(4, WALL_BOTTOM, 10):
        d.point((x + 4, y + (x // 8) % 2 * 5), fill=C(5))
# manchas de humedad
for _ in range(14):
    cx, cy, r = random.randint(0, W), random.randint(0, 60), random.randint(4, 14)
    for _ in range(r * 6):
        px, py = cx + random.randint(-r, r), cy + random.randint(0, r * 2)
        if 0 <= px < W and 0 <= py < WALL_BOTTOM:
            img.putpixel((px, py), C(3))
# papel despegado
for (x0, y0) in [(62, 18), (226, 104), (12, 96)]:
    d.polygon([(x0, y0), (x0 + 9, y0 + 1), (x0 + 7, y0 + 10), (x0 + 1, y0 + 7)], fill=C(6))
    d.line([(x0, y0), (x0 + 9, y0 + 1)], fill=C(2))
# moldura superior y zócalo
d.rectangle([0, 0, W, 5], fill=C(2))
d.rectangle([0, WALL_BOTTOM - 4, W, WALL_BOTTOM], fill=C(2))
d.line([0, WALL_BOTTOM - 5, W, WALL_BOTTOM - 5], fill=C(5))

# --- Suelo de tablones ------------------------------------------------------
d.rectangle([0, WALL_BOTTOM + 1, W, H], fill=C(20))
y = WALL_BOTTOM + 1
h = 5
while y < H:
    d.line([0, y, W, y], fill=C(19))
    off = random.randint(0, 40)
    for x in range(off, W, 47):
        d.line([x, y, x, y + h], fill=C(19))
    y += h
    h += 2

# --- Ventana con vista a la ciudad ------------------------------------------
WX0, WY0, WX1, WY1 = 84, 22, 146, 96
# cielo con degradado (se dithera al cuantizar)
for yy in range(WY0, WY1):
    t = (yy - WY0) / (WY1 - WY0)
    col = tuple(int(C(5)[k] * (1 - t) + C(6)[k] * t) for k in range(3))
    d.line([WX0, yy, WX1, yy], fill=col)
# pirámide escalonada del Minipax
px, pbase = 124, 86
for i, (w2, hh) in enumerate([(20, 6), (16, 6), (12, 6), (8, 6), (4, 5)]):
    top = pbase - (i + 1) * hh
    d.rectangle([px - w2, top, px + w2, top + hh], fill=C(8) if i % 2 == 0 else C(7))
    d.line([px - w2, top, px + w2, top], fill=C(6))
# tejados y chimeneas
roof = [(WX0, 80), (92, 74), (100, 80), (106, 70), (112, 76), (WX1, 84), (WX1, WY1), (WX0, WY1)]
d.polygon(roof, fill=C(2))
for cx in (95, 109, 138):
    d.rectangle([cx, 66 + (cx % 5), cx + 3, 80], fill=C(1))
# luces de ventanas lejanas (pocas)
for (lx, ly) in [(93, 86), (118, 90), (137, 89)]:
    d.point((lx, ly), fill=C(26))
# helicóptero de patrulla
d.line([(100, 40), (108, 40)], fill=C(1))
d.rectangle([102, 41, 105, 43], fill=C(1))
# marco y cruz
d.rectangle([WX0 - 3, WY0 - 3, WX1 + 3, WY1 + 3], outline=C(1), width=3)
d.line([(WX0 + WX1) // 2, WY0, (WX0 + WX1) // 2, WY1], fill=C(1), width=2)
d.line([WX0, (WY0 + WY1) // 2, WX1, (WY0 + WY1) // 2], fill=C(1), width=2)
d.rectangle([WX0 - 6, WY1 + 3, WX1 + 6, WY1 + 6], fill=C(2))  # alféizar

# --- Cama -------------------------------------------------------------------
d.rectangle([6, 104, 70, 140], fill=C(2))             # bastidor
d.rectangle([8, 98, 68, 112], fill=C(5))              # colchón/manta
d.line([8, 98, 68, 98], fill=C(6))
for x in range(12, 66, 7):
    d.line([x, 100, x + 3, 111], fill=C(4))           # arrugas
d.rectangle([8, 92, 22, 100], fill=C(7))              # almohada
d.rectangle([4, 84, 7, 142], fill=C(1))               # cabecero
d.rectangle([68, 98, 71, 142], fill=C(1))

# --- Mesa con hornillo y taza ------------------------------------------------
d.rectangle([92, 112, 140, 116], fill=C(19))
d.rectangle([94, 116, 97, 140], fill=C(19))
d.rectangle([135, 116, 138, 140], fill=C(19))
d.rectangle([100, 104, 116, 111], fill=C(2))          # hornillo
d.rectangle([104, 102, 112, 104], fill=C(1))
d.rectangle([124, 106, 129, 111], fill=C(7))          # taza
d.point((130, 108), fill=C(7))

# --- Cartel de Ivy ----------------------------------------------------------
PX0, PY0, PX1, PY1 = 156, 30, 192, 82
d.rectangle([PX0, PY0, PX1, PY1], fill=C(15))
d.rectangle([PX0, PY0, PX1, PY1], outline=C(14))
# perfil heroico (dibujado a mano, impresión a dos tintas)
IVY = [
    "......rrrrrr..........",
    "....rrrrrrrrrr........",
    "...rrrrrrrrrrrr.......",
    "..rrrrrrrrrrrrrr......",
    "..rrrrrrrcccccrr......",
    ".rrrrrrcccccccccr.....",
    ".rrrrrcccccccccccc....",
    ".rrrrcccccccccrrcc....",
    ".rrrrccccccccccrcc....",
    "..rrrcccccccccccccc...",
    "..rrrccccccccccccccc..",
    "...rrcccccccccccccc...",
    "...rrrcccccccccccc....",
    "....rrcccccccccrrc....",
    "....rrrcccccccccc.....",
    ".....rrrccccccccc.....",
    "......rrrcccccc.......",
    ".......rrrccccr.......",
    "........rrccccr.......",
    "......rrrrccccrrr.....",
    "....rrrrrrrrrrrrrrr...",
    "..rrrrrrrrrrrrrrrrrr..",
    "..rrrrrrrrrrrrrrrrrrr.",
]
for r, row in enumerate(IVY):
    for c, ch in enumerate(row):
        if ch != ".":
            img.putpixel((PX0 + 7 + c, PY0 + 5 + r), C(8) if ch == "c" else C(13))
# rayos de propaganda detrás
for k in range(0, 36, 6):
    d.line([(PX0 + 1, PY0 + 1 + k), (PX0 + 6, PY0 + 4 + k)], fill=C(14))

# Fuente 3x5 mínima para el rótulo
FONT = {
    "R": ["110", "101", "110", "101", "101"], "E": ["111", "100", "110", "100", "111"],
    "C": ["011", "100", "100", "100", "011"], "U": ["101", "101", "101", "101", "111"],
    "D": ["110", "101", "101", "101", "110"], "A": ["010", "101", "111", "101", "101"],
}
def text(x, y, s, col):
    for ch in s:
        for r, row in enumerate(FONT[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    img.putpixel((x + c, y + r), col)
        x += 4
text(PX0 + 3, PY1 - 8, "RECUERDA", C(8))

# --- Armario (el ángulo muerto queda entre el cartel y el armario) -----------
d.rectangle([200, 44, 232, 140], fill=C(19))
d.rectangle([200, 44, 232, 140], outline=C(0))
d.line([216, 48, 216, 136], fill=C(0))
d.point((213, 92), fill=C(22))
d.point((219, 92), fill=C(22))
d.rectangle([198, 40, 234, 44], fill=C(20))

# --- Estantería con el reloj de Ivy ------------------------------------------
d.rectangle([150, 96, 186, 98], fill=C(19))
d.rectangle([152, 99, 153, 103], fill=C(19))
d.rectangle([183, 99, 184, 103], fill=C(19))
d.ellipse([170, 90, 175, 95], fill=C(7), outline=C(1))   # reloj
d.point((172, 92), fill=C(0))
d.point((173, 93), fill=C(0))

# --- Telepantalla -----------------------------------------------------------
TX0, TY0, TX1, TY1 = 246, 30, 312, 82
d.rectangle([TX0 - 4, TY0 - 4, TX1 + 4, TY1 + 4], fill=C(1))
d.rectangle([TX0, TY0, TX1, TY1], fill=C(9))
# el rostro del Gran Hermano
cx = (TX0 + TX1) // 2
d.polygon([(cx - 26, TY1), (cx - 18, TY1 - 12), (cx + 18, TY1 - 12), (cx + 26, TY1)], fill=C(10))  # hombros
d.rectangle([cx - 6, TY1 - 16, cx + 6, TY1 - 10], fill=C(11))                    # cuello
d.ellipse([cx - 13, TY0 + 5, cx + 13, TY1 - 12], fill=C(11))                     # cara
d.pieslice([cx - 14, TY0 + 2, cx + 14, TY0 + 22], 180, 360, fill=C(9))           # pelo
d.rectangle([cx - 9, TY0 + 15, cx - 3, TY0 + 16], fill=C(9))                     # cejas
d.rectangle([cx + 3, TY0 + 15, cx + 9, TY0 + 16], fill=C(9))
d.rectangle([cx - 8, TY0 + 18, cx - 4, TY0 + 19], fill=C(12))                    # ojos que miran
d.rectangle([cx + 4, TY0 + 18, cx + 8, TY0 + 19], fill=C(12))
d.point((cx - 6, TY0 + 18), fill=C(9)); d.point((cx + 6, TY0 + 18), fill=C(9))
d.line([(cx, TY0 + 19), (cx - 2, TY0 + 25), (cx + 1, TY0 + 26)], fill=C(10))     # nariz
d.polygon([(cx - 9, TY0 + 28), (cx + 9, TY0 + 28), (cx + 7, TY0 + 32), (cx, TY0 + 30), (cx - 7, TY0 + 32)], fill=C(9))  # bigote
for yy in range(TY0, TY1, 2):                                    # líneas de barrido
    d.line([TX0, yy, TX1, yy], fill=C(10))
d.rectangle([TX0 - 4, TY1 + 4, TX1 + 4, TY1 + 7], fill=C(2))     # rejilla
d.point((TX1, TY1 + 5), fill=C(15))                              # piloto rojo

# --- Protagonista (sprite dibujado a mano, 16x40) ----------------------------
SPRITE = [
    "......kkkk......",
    ".....khhhhkk....",
    "....khhhhhhhk...",
    "...khhhhhhhhk...",
    "...khhhSSShhk...",
    "...khhSSSSSSk...",
    "...khdSSkSSSk...",
    "...kkdSSSSSSSk..",
    "....kdSSSSSSk...",
    "....kddSSkkSk...",
    ".....kdSSSSk....",
    "......kddddk....",
    "......kdddk.....",
    "....kknnbbnkk...",
    "...knbbbbbbbbk..",
    "..knbbbbbBbbbbk.",
    "..knbbbbbBbbbbk.",
    "..knbnbbbBbbbbk.",
    "..knbnbbbBbbnbk.",
    "..knbnbbbBbbnbk.",
    "..knbnbbbBbbnbk.",
    "..knbnbbbBbbnbk.",
    "..kdnbbbbBbbndk.",
    "..kdkbbbbBbbkdk.",
    "..kSkbbbbBbbkSk.",
    "...kknnnnnnnkk..",
    "....knbbbbbnk...",
    "....knbbkbbnk...",
    "....knbbkbbnk...",
    "....knbbkbbnk...",
    "....knbbkbbnk...",
    "....knbbkbbnk...",
    "....knbbkbbnk...",
    "....knbbkbbnk...",
    "....knbbkbbnk...",
    "....knbbkbbnk...",
    "....knbbkbbnk...",
    "....kwwwkwwwk...",
    "....kwwwkwwwwk..",
    "....kkkkkkkkkk..",
]
SPR_COL = {"k": 0, "h": 19, "S": 25, "s": 24, "d": 24, "n": 16, "b": 17, "B": 18, "w": 1}
SX, SY = 166, 104
# sombra en el suelo
d.ellipse([SX - 1, SY + 37, SX + 16, SY + 42], fill=C(19))
sprite_mask = []
for r, row in enumerate(SPRITE):
    for c, ch in enumerate(row[:16]):
        if ch in SPR_COL:
            img.putpixel((SX + c, SY + r), C(SPR_COL[ch]))
            sprite_mask.append((SX + c, SY + r))

# --- Iluminación ------------------------------------------------------------
def lerp(a, b, t):
    return a + (b - a) * t

light = Image.new("RGB", (W, H))
lp = light.load()
for yy in range(H):
    for xx in range(W):
        amb = 0.62
        # haz de la ventana sobre el suelo (paralelogramo)
        if yy > WALL_BOTTOM:
            sx0 = WX0 + (yy - WALL_BOTTOM) * 0.9 - 6
            if sx0 < xx < sx0 + (WX1 - WX0) + 10:
                amb += 0.28
        # resplandor de la ventana en la pared
        dx, dy = xx - (WX0 + WX1) / 2, yy - (WY0 + WY1) / 2
        amb += max(0, 0.25 - (dx * dx + dy * dy) ** 0.5 / 260)
        # viñeta
        vx, vy = (xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)
        amb -= 0.18 * (vx * vx + vy * vy)
        # resplandor verde de la telepantalla
        gx, gy = xx - (TX0 + TX1) / 2, yy - (TY0 + TY1) / 2
        g = max(0, 0.55 - (gx * gx * 0.6 + gy * gy) ** 0.5 / 110)
        lp[xx, yy] = (int(amb * 255), int(g * 255), 0)

base = img.load()
out = Image.new("RGB", (W, H))
op = out.load()
GLOW = C(11)
for yy in range(H):
    for xx in range(W):
        r, g, b = base[xx, yy]
        amb, glow, _ = lp[xx, yy]
        a, gl = amb / 255, glow / 255
        if TX0 <= xx <= TX1 and TY0 <= yy <= TY1:  # la pantalla emite, no recibe
            a, gl = 1.05, 0.0
        op[xx, yy] = (
            int(min(255, r * a + GLOW[0] * gl * 0.5)),
            int(min(255, g * a + GLOW[1] * gl * 0.5)),
            int(min(255, b * a + GLOW[2] * gl * 0.5)),
        )

# --- Cuantización a la paleta con dithering ordenado (Bayer 4x4) ------------
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
def nearest(rgb):
    return min(RGB, key=lambda p: (p[0] - rgb[0]) ** 2 * 3 + (p[1] - rgb[1]) ** 2 * 4 + (p[2] - rgb[2]) ** 2 * 2)

final = Image.new("RGB", (W, H))
fp = final.load()
cache = {}
for yy in range(H):
    for xx in range(W):
        t = (BAYER[yy % 4][xx % 4] / 16 - 0.5) * 12
        r, g, b = op[xx, yy]
        key = (int(r + t) // 2, int(g + t) // 2, int(b + t) // 2)
        if key not in cache:
            cache[key] = nearest((key[0] * 2, key[1] * 2, key[2] * 2))
        fp[xx, yy] = cache[key]

final.save(OUT / "piso.png")
final.resize((W * 4, H * 4), Image.NEAREST).save(OUT / "piso@4x.png")
print("ok", OUT / "piso@4x.png")
