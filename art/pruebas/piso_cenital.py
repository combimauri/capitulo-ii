"""Prueba de arte 2: el piso del protagonista en perspectiva cenital 3/4.

Estilo de referencia: Stardew Valley / Pokémon / Final Fantasy VI.
Cuadrícula de 16x16, personaje de 16x32, colores planos (2-3 tonos por material).

Uso: python3 art/pruebas/piso_cenital.py
Salida: art/pruebas/piso_cenital.png (1x) y piso_cenital@4x.png (vista previa)
"""
from pathlib import Path
from PIL import Image, ImageDraw

W, H = 320, 180
T = 16
OUT = Path(__file__).parent

PAL = {
    # grises del Partido
    "negro": "#0e0f12", "g1": "#1b1d22", "g2": "#2a2d33", "g3": "#3c4047",
    "g4": "#555a61", "g5": "#737980", "g6": "#969ca1", "g7": "#c2c6c4", "blanco": "#e6e4dc",
    # telepantalla
    "t0": "#0f2a22", "t1": "#1e4a3a", "t2": "#3f7a5c", "t3": "#8fc79a",
    # rojo propaganda
    "r0": "#4a0f12", "r1": "#8a1c1f", "r2": "#c8342c",
    # mono azul
    "a0": "#1d2a44", "a1": "#2f4468", "a2": "#4b6694",
    # madera
    "m0": "#2b2420", "m1": "#4a3426", "m2": "#6b4a33", "m3": "#8c6544", "m4": "#a98058",
    # pared
    "p0": "#3a423d", "p1": "#4d5650", "p2": "#66706a", "p3": "#7f8a83",
    # alfombra
    "f0": "#4a2626", "f1": "#6a3530", "f2": "#84473c",
    # piel y pelo
    "s0": "#a77b62", "s1": "#d6aa8a", "h0": "#2e2119", "h1": "#4a3426",
    # luz
    "luz": "#e8c96a",
}
C = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) for k, v in PAL.items()}

img = Image.new("RGB", (W, H), C["negro"])
d = ImageDraw.Draw(img)

def rect(x0, y0, x1, y1, col):
    d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=C[col])

def hline(x0, x1, y, col):
    d.line([x0, y, x1 - 1, y], fill=C[col])

def vline(x, y0, y1, col):
    d.line([x, y0, x, y1 - 1], fill=C[col])

def px(x, y, col):
    img.putpixel((x, y), C[col])

def grid(x, y, rows, palette):
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in palette:
                px(x + c, y + r, palette[ch])

# --- Geometría de la habitación ------------------------------------------
RX0, RX1 = 24, 296          # interior (17 tiles)
WALL_TOP, WALL_BOT = 12, 60  # pared del fondo (3 tiles de alto)
FLOOR_BOT = 168

# grosor superior del muro (visto desde arriba)
rect(RX0 - 8, WALL_TOP - 8, RX1 + 8, WALL_TOP, "g2")
hline(RX0 - 8, RX1 + 8, WALL_TOP - 8, "g3")

# pared del fondo: papel pintado a rayas
rect(RX0, WALL_TOP, RX1, WALL_BOT, "p1")
for x in range(RX0, RX1, 8):
    vline(x, WALL_TOP, WALL_BOT - 6, "p0")
    vline(x + 4, WALL_TOP, WALL_BOT - 6, "p2")
hline(RX0, RX1, WALL_TOP, "p0")
# zócalo
rect(RX0, WALL_BOT - 6, RX1, WALL_BOT, "m1")
hline(RX0, RX1, WALL_BOT - 6, "m2")
# mancha de humedad y papel despegado
for (x, y) in [(40, 16), (41, 17), (42, 16), (43, 18), (42, 19), (44, 17), (270, 40), (271, 41), (272, 40)]:
    px(x, y, "p0")
d.polygon([(258, 14), (266, 14), (264, 21), (259, 19)], fill=C["p3"])

# suelo de tablones (vistos desde arriba)
rect(RX0, WALL_BOT, RX1, FLOOR_BOT, "m2")
for i, y in enumerate(range(WALL_BOT, FLOOR_BOT, 8)):
    hline(RX0, RX1, y, "m1")
    hline(RX0, RX1, y + 1, "m3")
    off = (i * 37) % 48
    for x in range(RX0 + off, RX1, 48):
        vline(x, y, y + 8, "m1")
        px(x + 1, y + 4, "m1")  # clavo

# muros laterales e inferior (tapa vista desde arriba)
rect(RX0 - 8, WALL_TOP, RX0, FLOOR_BOT + 8, "g2")
rect(RX1, WALL_TOP, RX1 + 8, FLOOR_BOT + 8, "g2")
rect(RX0 - 8, FLOOR_BOT, RX1 + 8, FLOOR_BOT + 8, "g2")
vline(RX0 - 1, WALL_TOP, FLOOR_BOT, "g1")
vline(RX1, WALL_TOP, FLOOR_BOT, "g1")
hline(RX0, RX1, FLOOR_BOT, "g1")
# puerta (hueco en el muro inferior) y felpudo
rect(144, FLOOR_BOT, 176, FLOOR_BOT + 8, "m1")
hline(144, 176, FLOOR_BOT, "m0")
rect(148, FLOOR_BOT - 10, 172, FLOOR_BOT - 2, "g3")
hline(148, 172, FLOOR_BOT - 10, "g4")

# --- Ventana (pared del fondo) -----------------------------------------------
WX0, WY0, WX1, WY1 = 64, 18, 112, 50
rect(WX0 - 3, WY0 - 3, WX1 + 3, WY1 + 3, "m1")
# cielo en franjas
for i, col in enumerate(["g5", "g5", "g6", "g6", "g7"]):
    rect(WX0, WY0 + i * 7, WX1, WY0 + (i + 1) * 7, col)
# pirámide del Minipax
cx, base = 96, 44
for i, w2 in enumerate([14, 11, 8, 5, 2]):
    rect(cx - w2, base - (i + 1) * 4, cx + w2 + 1, base - i * 4, "blanco" if i % 2 == 0 else "g7")
# tejados
d.polygon([(WX0, 42), (72, 38), (78, 42), (84, 36), (88, 40), (WX1, 44), (WX1, WY1), (WX0, WY1)], fill=C["g3"])
for x in (70, 86, 104):
    rect(x, 35 + x % 4, x + 3, 44, "g2")
px(74, 46, "luz"); px(100, 47, "luz")
# helicóptero
hline(74, 81, 25, "g2"); rect(76, 26, 79, 28, "g2")
# marco en cruz y alféizar
vline((WX0 + WX1) // 2, WY0, WY1, "m1")
hline(WX0, WX1, (WY0 + WY1) // 2, "m1")
rect(WX0 - 5, WY1 + 3, WX1 + 5, WY1 + 6, "m3")
hline(WX0 - 5, WX1 + 5, WY1 + 5, "m1")

# --- Cartel de Ivy --------------------------------------------------------------
PX0, PY0 = 128, 18
rect(PX0, PY0, PX0 + 34, PY0 + 34, "r2")
d.rectangle([PX0, PY0, PX0 + 33, PY0 + 33], outline=C["r1"])
IVY = [
    "....rrrrrr......",
    "..rrrrrrrrrr....",
    ".rrrrrrcccccr...",
    ".rrrrcccccccc...",
    ".rrrcccccccrcc..",
    ".rrrcccccccccccc",
    "..rrcccccccccc..",
    "..rrrcccccccrc..",
    "...rrrcccccc....",
    "....rrrcccr.....",
    ".....rrcccr.....",
    "...rrrrcccrrr...",
    ".rrrrrrrrrrrrrr.",
    "rrrrrrrrrrrrrrrr",
]
grid(PX0 + 9, PY0 + 4, IVY, {"r": "r0", "c": "blanco"})
for i in range(0, 12, 4):
    hline(PX0 + 2, PX0 + 5, PY0 + 6 + i, "r1")
# rótulo 3x5
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
                    px(x + c, y + r, col)
        x += 4
rect(PX0 + 1, PY0 + 25, PX0 + 33, PY0 + 33, "r1")
text(PX0 + 2, PY0 + 27, "RECUERDA", "blanco")

# --- Estante con el reloj de Ivy ----------------------------------------------
rect(164, 40, 180, 43, "m3"); hline(164, 180, 42, "m1")
d.ellipse([169, 33, 175, 39], fill=C["g7"], outline=C["g1"])
px(172, 36, "negro"); px(173, 37, "negro")

# --- Telepantalla -------------------------------------------------------------
TX0, TY0, TX1, TY1 = 216, 16, 268, 50
rect(TX0 - 4, TY0 - 4, TX1 + 4, TY1 + 6, "g1")
rect(TX0, TY0, TX1, TY1, "t0")
cxs = (TX0 + TX1) // 2
BB = [
    "....tttttttttt....",
    "..tttttttttttttt..",
    ".ttTTTTTTTTTTTTtt.",
    ".tTTTTTTTTTTTTTTt.",
    ".TTttttTTTTttttTT.",
    ".TTTggTTTTTTggTTT.",
    ".TTTTTTTTTTTTTTTT.",
    ".TTTTTTTttTTTTTTT.",
    "..TTTTTTttTTTTTT..",
    "..TTTttttttttTTT..",
    "..TTtttttttttttT..",
    "...TTTTTTTTTTTT...",
    "....TTTTTTTTTT....",
    "......TTTTTT......",
    "..tttttTTTTttttt..",
    "tttttttttttttttttt",
]
grid(cxs - 9, TY0 + 2, BB, {"t": "t1", "T": "t2", "g": "t3"})
for y in range(TY0, TY1, 2):
    for x in range(TX0, TX1):
        r, g, b = img.getpixel((x, y))
        img.putpixel((x, y), (int(r * 0.8), int(g * 0.8), int(b * 0.8)))
rect(TX0 - 4, TY1 + 2, TX1 + 4, TY1 + 6, "g2")
px(TX1, TY1 + 4, "r2")

# --- Armario (alto, contra la pared) --------------------------------------------
AX0, AX1, ATOP, ABOT = 184, 208, 20, 72
rect(AX0, ATOP, AX1, ATOP + 5, "m3")            # tapa (vista desde arriba)
rect(AX0, ATOP + 5, AX1, ABOT, "m2")            # frente
vline((AX0 + AX1) // 2, ATOP + 7, ABOT - 2, "m1")
d.rectangle([AX0, ATOP, AX1 - 1, ABOT - 1], outline=C["m0"])
px(194, 46, "m4"); px(197, 46, "m4")
rect(AX0 + 2, ABOT - 3, AX1 - 2, ABOT, "m1")
# sombra en el suelo
rect(AX0, ABOT, AX1 + 2, ABOT + 3, "m1")

# --- Cama -----------------------------------------------------------------------
BX0, BX1, BY0, BY1 = 32, 64, 52, 108
rect(BX0, BY0, BX1, BY0 + 6, "g2")                 # cabecero (metal)
hline(BX0, BX1, BY0, "g4")
rect(BX0 + 2, BY0 + 6, BX1 - 2, BY1, "g6")        # sábana
rect(BX0 + 4, BY0 + 8, BX1 - 4, BY0 + 18, "blanco")  # almohada
hline(BX0 + 4, BX1 - 4, BY0 + 17, "g7")
rect(BX0 + 2, BY0 + 22, BX1 - 2, BY1, "g4")        # manta
hline(BX0 + 2, BX1 - 2, BY0 + 22, "g5")
for y in range(BY0 + 28, BY1 - 2, 8):
    hline(BX0 + 6, BX1 - 8, y, "g3")               # pliegues
rect(BX0, BY1, BX1, BY1 + 5, "g3")                 # frente del somier
hline(BX0, BX1, BY1 + 4, "g2")
rect(BX0, BY1 + 5, BX1 + 2, BY1 + 8, "m1")         # sombra

# --- Alfombra -------------------------------------------------------------------
rect(112, 104, 208, 144, "f1")
d.rectangle([112, 104, 207, 143], outline=C["f0"])
d.rectangle([116, 108, 203, 139], outline=C["f2"])
for (x, y) in [(130, 120), (131, 121), (170, 128), (171, 128), (150, 112)]:
    px(x, y, "f0")  # desgaste

# --- Mesa, silla, hornillo y taza --------------------------------------------------
MX0, MX1, MY0, MY1 = 232, 280, 84, 104
rect(MX0, MY0, MX1, MY1, "m3")                     # tablero
d.rectangle([MX0, MY0, MX1 - 1, MY1 - 1], outline=C["m1"])
hline(MX0 + 1, MX1 - 1, MY0 + 1, "m4")
rect(MX0, MY1, MX1, MY1 + 4, "m2")                 # canto
for x in (MX0 + 1, MX1 - 4):
    rect(x, MY1 + 4, x + 3, MY1 + 12, "m1")        # patas
rect(MX0, MY1 + 12, MX1 + 2, MY1 + 14, "m1")       # sombra
rect(238, 86, 252, 96, "g2"); d.ellipse([241, 88, 249, 94], outline=C["g4"])  # hornillo
rect(262, 88, 268, 94, "g7"); px(268, 90, "g7")   # taza
rect(248, 114, 264, 124, "m2"); rect(248, 110, 264, 114, "m3")  # silla
rect(248, 124, 251, 130, "m1"); rect(261, 124, 264, 130, "m1")

# --- Protagonista (16x32, de frente) ---------------------------------------------
SPRITE = [
    ".....oooooo.....",
    "....ohhhhhho....",
    "...ohhHHHhhho...",
    "..ohhHhhhhhhho..",
    "..ohhhhhhhhhho..",
    "..ohhsshhsshho..",
    "..ohssssssssho..",
    "..ossessssesso..",
    "..ossessssesso..",
    ".oSssssssssssSo.",
    "..osssssssssso..",
    "..osssSSSsssso..",
    "...oSSssssSSo...",
    "....ooSSSSoo....",
    "...onnbbbbnno...",
    "..onbbbbBbbbbno.",
    ".onbbbbbBbbbbbno",
    ".onbnbbbBbbbnbno",
    ".onbnbbbBbbbnbno",
    ".onbnbbbBbbbnbno",
    ".osnnbbbBbbbnnso",
    ".ossonnnnnnnosso",
    "...onbbbBbbbno..",
    "...onbbbobbbno..",
    "...onbbbobbbno..",
    "...onbbbobbbno..",
    "...onbbbobbbno..",
    "...onbbbobbbno..",
    "...onbbbobbbno..",
    "...owwwwowwwwo..",
    "...owwwwowwwwo..",
    "...ooooo.ooooo..",
]
SPR = {"o": "g1", "h": "h0", "H": "h1", "s": "s1", "S": "s0", "e": "negro",
       "n": "a0", "b": "a1", "B": "a2", "w": "g1"}
SX, SY = 152, 100
d.ellipse([SX + 1, SY + 28, SX + 15, SY + 34], fill=C["f0"])  # sombra sobre la alfombra
grid(SX, SY, SPRITE, SPR)

# --- Iluminación por rampas de material (sin tramado) ------------------------------
# Cada color pertenece a una rampa; la luz sube o baja un escalón dentro de su rampa,
# y el resplandor de la telepantalla usa variantes verdosas generadas a partir de cada color.
RAMPS = [
    ["negro", "g1", "g2", "g3", "g4", "g5", "g6", "g7", "blanco"],
    ["t0", "t1", "t2", "t3"], ["r0", "r1", "r2"], ["a0", "a1", "a2"],
    ["m0", "m1", "m2", "m3", "m4"], ["p0", "p1", "p2", "p3"], ["f0", "f1", "f2"],
    ["s0", "s1"], ["h0", "h1"], ["luz"],
]
STEP = {}
for ramp in RAMPS:
    for i, name in enumerate(ramp):
        STEP[C[name]] = (ramp, i)

def shift(rgb, n):
    if rgb not in STEP:
        return rgb
    ramp, i = STEP[rgb]
    return C[ramp[max(0, min(len(ramp) - 1, i + n))]]

def glow(rgb, k):
    g = C["t2"]
    return tuple(int(rgb[c] * (1 - k) + g[c] * k) for c in range(3))

src = img.copy()
sp = src.load()
op = img.load()
for y in range(H):
    for x in range(W):
        if TX0 <= x < TX1 and TY0 <= y < TY1:
            continue
        col = sp[x, y]
        n = 0
        if y >= WALL_BOT:                                     # haz de la ventana
            sx0 = WX0 - 4 + (y - WALL_BOT) * 0.55
            if sx0 <= x <= sx0 + (WX1 - WX0) + 8:
                n += 1
        if x < 40 or x > 284 or y > 156:                      # rincones
            n -= 1
        col = shift(col, n)
        dx, dy = x - (TX0 + TX1) / 2, (y - (TY1 + 10)) * 1.4  # telepantalla
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < 34:
            col = glow(col, 0.28)
        elif dist < 60:
            col = glow(col, 0.14)
        op[x, y] = col

img.save(OUT / "piso_cenital.png")
img.resize((W * 4, H * 4), Image.NEAREST).save(OUT / "piso_cenital@4x.png")
print("ok", OUT / "piso_cenital@4x.png")
