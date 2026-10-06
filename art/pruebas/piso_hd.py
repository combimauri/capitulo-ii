"""Prueba de arte 3: el piso del protagonista, cenital 3/4, a 480x270.

Uso: python3 art/pruebas/piso_hd.py
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from pixel import Canvas, K  # noqa: E402

random.seed(1984)
W, H = 480, 270
cv = Canvas(W, H)
R, HL, VL, PX = cv.rect, cv.hline, cv.vline, cv.px

# Geometría de la habitación
X0, X1 = 40, 440           # interior
CAP = 12                   # grosor de muro visto desde arriba
WT, WB = 20, 84            # pared del fondo (4 tiles)
FB = 246                   # fin del suelo

# ---------------------------------------------------------------- muros (tapas)
R(X0 - CAP, WT - CAP, X1 + CAP, WT, K("gris", 3))
HL(X0 - CAP, X1 + CAP, WT - CAP, K("gris", 4))
HL(X0 - CAP, X1 + CAP, WT - 1, K("gris", 2))

# ---------------------------------------------------------------- pared del fondo
R(X0, WT, X1, WB, K("pared", 3))
# papel pintado: rombos pequeños y rayas finas
for x in range(X0, X1, 6):
    VL(x, WT, 62, K("pared", 2))
for y in range(WT + 3, 60, 6):
    for x in range(X0 + 3 + (y // 6 % 2) * 3, X1, 6):
        PX(x, y, K("pared", 4)); PX(x - 1, y + 1, K("pared", 4)); PX(x + 1, y + 1, K("pared", 4)); PX(x, y + 2, K("pared", 4))
# moldura y zócalo de friso
R(X0, 60, X1, 63, K("madera", 3)); HL(X0, X1, 60, K("madera", 5)); HL(X0, X1, 62, K("madera", 2))
R(X0, 63, X1, 78, K("pared", 2))
for x in range(X0 + 10, X1, 20):
    cv.frame(x, 66, x + 14, 76, K("pared", 1))
    HL(x + 1, x + 13, 67, K("pared", 3))
R(X0, 78, X1, WB, K("madera", 2)); HL(X0, X1, 78, K("madera", 4)); HL(X0, X1, WB - 1, K("madera", 1))
# humedad y grietas
for _ in range(160):
    x = random.choice([random.randint(42, 70), random.randint(300, 330), random.randint(420, 438)])
    y = random.randint(WT, 40) if x < 80 else random.randint(WT, 34)
    PX(x, y, K("pared", 2))
crack = [(60, 21), (61, 22), (61, 23), (62, 24), (62, 25), (61, 26), (62, 27), (63, 28), (63, 29), (64, 30)]
for p in crack:
    PX(*p, K("pared", 0))
cv.poly([(424, 22), (436, 22), (434, 34), (426, 30)], K("papel", 2))
HL(424, 436, 22, K("pared", 1))
# tubería que baja hasta el radiador
HL(X0, 98, 24, K("gris", 6)); HL(X0, 98, 25, K("gris", 4))
VL(98, 24, 72, K("gris", 6)); VL(99, 24, 72, K("gris", 4))
for y in (36, 54):
    R(97, y, 101, y + 2, K("gris", 7))

# ---------------------------------------------------------------- ventana
WX0, WY0, WX1, WY1 = 108, 26, 176, 66
R(WX0 - 4, WY0 - 4, WX1 + 4, WY1 + 4, K("madera", 2))
cv.frame(WX0 - 4, WY0 - 4, WX1 + 4, WY1 + 4, K("madera", 1))
# cielo en bandas
for i, y in enumerate(range(WY0, WY1, 5)):
    R(WX0, y, WX1, y + 5, K("cielo", 3 + min(i // 2, 3)))
# nubes
for (cx, cy, w) in [(124, 31, 14), (154, 36, 18)]:
    HL(cx, cx + w, cy, K("cielo", 6)); HL(cx + 3, cx + w - 2, cy - 1, K("cielo", 6))
# pirámide escalonada del Minipax con ventanucos
pcx, pbase = 150, 58
for i, w2 in enumerate([22, 18, 14, 10, 6, 3]):
    top = pbase - (i + 1) * 5
    R(pcx - w2, top, pcx + w2 + 1, top + 5, K("papel", 4 if i % 2 == 0 else 3))
    HL(pcx - w2, pcx + w2 + 1, top + 4, K("papel", 1))
# ciudad: dos capas de tejados
cv.poly([(WX0, 52), (116, 48), (122, 52), (128, 46), (134, 50), (WX1, 54), (WX1, WY1), (WX0, WY1)], K("cielo", 1))
cv.poly([(WX0, 58), (114, 56), (120, 60), (138, 54), (146, 58), (160, 56), (170, 60), (WX1, 58), (WX1, WY1), (WX0, WY1)], K("cielo", 0))
for x, top in [(118, 44), (130, 42), (164, 48)]:
    R(x, top, x + 3, 54, K("cielo", 0))
    for k in range(4):  # humo
        PX(x + 1 + k % 2, top - 2 - k * 2, K("cielo", 5))
for (lx, ly) in [(112, 61), (126, 63), (158, 62), (168, 64)]:
    PX(lx, ly, K("ocre", 3))
# helicóptero de patrulla
HL(118, 127, 34, K("cielo", 0)); R(120, 35, 125, 38, K("cielo", 0)); HL(125, 130, 36, K("cielo", 0))
# reflejo y marco en cruz
for k in range(6):
    PX(WX0 + 3 + k, WY0 + 8 - k, K("cielo", 6))
VL((WX0 + WX1) // 2, WY0, WY1, K("madera", 2)); VL((WX0 + WX1) // 2 + 1, WY0, WY1, K("madera", 3))
HL(WX0, WX1, (WY0 + WY1) // 2, K("madera", 2)); HL(WX0, WX1, (WY0 + WY1) // 2 + 1, K("madera", 3))
# cortinas finas recogidas
for cx0 in (WX0 - 12, WX1 + 4):
    R(cx0, WY0 - 6, cx0 + 8, WY1 + 10, K("tela", 2))
    for k in range(1, 8, 3):
        VL(cx0 + k, WY0 - 6, WY1 + 10, K("tela", 1))
    VL(cx0 + 7, WY0 - 6, WY1 + 10, K("tela", 3))
R(WX0 - 14, WY0 - 8, WX1 + 14, WY0 - 6, K("gris", 5))  # barra
# alféizar con maceta seca
R(WX0 - 6, WY1 + 4, WX1 + 6, WY1 + 8, K("madera", 4)); HL(WX0 - 6, WX1 + 6, WY1 + 7, K("madera", 2))
R(160, WY1 - 2, 168, WY1 + 4, K("granate", 3)); HL(160, 168, WY1 - 2, K("granate", 4))
for (a, b) in [(163, WY1 - 6), (164, WY1 - 5), (165, WY1 - 7), (166, WY1 - 4), (162, WY1 - 4)]:
    PX(a, b, K("ocre", 1))
# radiador
R(116, 72, 168, 86, K("gris", 5))
for x in range(118, 168, 4):
    VL(x, 73, 85, K("gris", 3)); VL(x + 1, 73, 85, K("gris", 6))
HL(116, 168, 72, K("gris", 7))
R(116, 86, 168, 88, K("gris", 3))

# ---------------------------------------------------------------- cartel de Ivy
PX0, PY0, PW, PH = 192, 24, 40, 50
R(PX0 + 2, PY0 + 2, PX0 + PW + 2, PY0 + PH + 2, K("pared", 1))   # sombra
R(PX0, PY0, PX0 + PW, PY0 + PH, K("rojo", 4))
for k in range(0, 34, 5):                                            # rayos
    cv.d.line([PX0 + 20, PY0 + 18, PX0 + 1, PY0 + k], fill=K("rojo", 3))
    cv.d.line([PX0 + 20, PY0 + 18, PX0 + PW - 2, PY0 + k], fill=K("rojo", 3))
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
]
cv.grid(PX0 + 9, PY0 + 4, IVY, {"r": K("rojo", 1), "c": K("papel", 4)})
R(PX0, PY0 + 34, PX0 + PW, PY0 + PH, K("rojo", 1))
cv.text(PX0 + (PW - cv.text_width("RECUERDA")) // 2, PY0 + 37, "RECUERDA", K("papel", 4))
cv.text(PX0 + (PW - cv.text_width("STEPNEY")) // 2, PY0 + 43, "STEPNEY", K("rojo", 5))
cv.frame(PX0, PY0, PX0 + PW, PY0 + PH, K("rojo", 2))
for (cx, cy) in [(PX0 + 1, PY0 + 1), (PX0 + PW - 2, PY0 + 1)]:
    PX(cx, cy, K("gris", 8))  # chinchetas

# ---------------------------------------------------------------- estante con el reloj
R(242, 50, 276, 53, K("madera", 4)); HL(242, 276, 52, K("madera", 2))
for x in (246, 271):
    R(x, 53, x + 2, 58, K("madera", 2))
cv.ellipse(251, 41, 260, 50, K("papel", 3), outline=K("gris", 2))      # reloj de Ivy
PX(255, 45, K("gris", 1)); PX(255, 44, K("gris", 1)); PX(256, 46, K("gris", 1))
R(264, 44, 270, 50, K("gris", 5)); HL(264, 270, 44, K("gris", 7))    # lata
R(244, 46, 247, 50, K("papel", 3)); PX(245, 45, K("ocre", 3))         # cabo de vela

# ---------------------------------------------------------------- armario
AX0, AX1, ATOP, ABOT = 288, 326, 10, 96
R(AX0 + 3, ATOP + 2, AX1 + 3, ABOT + 3, K("madera", 0))              # sombra
R(AX0, ATOP, AX1, ATOP + 7, K("madera", 4)); HL(AX0, AX1, ATOP, K("madera", 6))
R(AX0, ATOP + 7, AX1, ABOT, K("madera", 3))
for (x0, x1) in [(AX0 + 3, (AX0 + AX1) // 2 - 1), ((AX0 + AX1) // 2 + 1, AX1 - 3)]:
    cv.frame(x0, ATOP + 11, x1, ABOT - 8, K("madera", 2))
    VL(x0 + 1, ATOP + 12, ABOT - 9, K("madera", 4))
    cv.frame(x0 + 3, ATOP + 15, x1 - 3, ATOP + 40, K("madera", 2))
VL((AX0 + AX1) // 2, ATOP + 9, ABOT - 6, K("madera", 1))
PX((AX0 + AX1) // 2 - 3, 54, K("ocre", 3)); PX((AX0 + AX1) // 2 + 2, 54, K("ocre", 3))
R(AX0, ABOT - 6, AX1, ABOT, K("madera", 2)); HL(AX0, AX1, ABOT - 6, K("madera", 4))
cv.frame(AX0, ATOP, AX1, ABOT, K("madera", 1))
# maleta encima
R(AX0 + 6, ATOP - 6, AX1 - 8, ATOP + 3, K("granate", 3)); HL(AX0 + 6, AX1 - 8, ATOP - 6, K("granate", 5))
R(AX0 + 14, ATOP - 8, AX0 + 20, ATOP - 6, K("granate", 1))

# ---------------------------------------------------------------- telepantalla
TX0, TY0, TX1, TY1 = 346, 24, 426, 70
R(TX0 - 6, TY0 - 6, TX1 + 6, TY1 + 10, K("gris", 2))
cv.frame(TX0 - 6, TY0 - 6, TX1 + 6, TY1 + 10, K("gris", 1))
HL(TX0 - 5, TX1 + 5, TY0 - 5, K("gris", 4))
for (sx, sy) in [(TX0 - 4, TY0 - 4), (TX1 + 3, TY0 - 4), (TX0 - 4, TY1 + 7), (TX1 + 3, TY1 + 7)]:
    PX(sx, sy, K("gris", 6))
R(TX0, TY0, TX1, TY1, K("tele", 1))
cx = (TX0 + TX1) // 2
# rostro del Gran Hermano
cv.poly([(cx - 34, TY1), (cx - 24, TY1 - 12), (cx + 24, TY1 - 12), (cx + 34, TY1)], K("tele", 2))
R(cx - 7, TY1 - 17, cx + 8, TY1 - 11, K("tele", 3))
cv.ellipse(cx - 15, TY0 + 4, cx + 16, TY1 - 10, K("tele", 3))
cv.ellipse(cx - 13, TY0 + 6, cx + 10, TY1 - 13, K("tele", 4))
cv.d.pieslice([cx - 16, TY0 + 1, cx + 16, TY0 + 25], 180, 360, fill=K("tele", 1))
R(cx - 11, TY0 + 17, cx - 3, TY0 + 19, K("tele", 1)); R(cx + 4, TY0 + 17, cx + 12, TY0 + 19, K("tele", 1))
R(cx - 10, TY0 + 20, cx - 4, TY0 + 22, K("tele", 6)); R(cx + 5, TY0 + 20, cx + 11, TY0 + 22, K("tele", 6))
PX(cx - 7, TY0 + 21, K("tele", 0)); PX(cx + 8, TY0 + 21, K("tele", 0))
cv.d.line([cx, TY0 + 22, cx - 2, TY0 + 29], fill=K("tele", 2)); HL(cx - 2, cx + 2, TY0 + 29, K("tele", 2))
cv.poly([(cx - 11, TY0 + 32), (cx + 12, TY0 + 32), (cx + 9, TY0 + 37), (cx, TY0 + 34), (cx - 8, TY0 + 37)], K("tele", 0))
HL(cx - 5, cx + 6, TY0 + 39, K("tele", 2))
# texto inferior y líneas de barrido
cv.text(cx - cv.text_width("TE VIGILA") // 2, TY1 - 7, "TE VIGILA", K("tele", 6))
for y in range(TY0, TY1, 2):
    for x in range(TX0, TX1):
        r, g, b = cv.img.getpixel((x, y))
        cv.img.putpixel((x, y), (int(r * 0.82), int(g * 0.82), int(b * 0.82)))
cv.add_emissive(TX0, TY0, TX1, TY1)
# rejilla del altavoz y piloto
for x in range(TX0, TX1 - 10, 3):
    VL(x, TY1 + 3, TY1 + 8, K("gris", 1))
PX(TX1 - 2, TY1 + 5, K("rojo", 5)); PX(TX1 - 2, TY1 + 4, K("rojo", 4))
# enchufe
R(436 - 8, 70, 436 - 3, 76, K("papel", 2)); PX(436 - 6, 72, K("gris", 2)); PX(436 - 6, 74, K("gris", 2))

# ---------------------------------------------------------------- suelo de tablones
R(X0, WB, X1, FB, K("madera", 3))
for i, y in enumerate(range(WB, FB, 8)):
    HL(X0, X1, y, K("madera", 1))
    HL(X0, X1, y + 1, K("madera", 4))
    x = X0 - random.randint(0, 60)
    while x < X1:
        w = random.randint(44, 90)
        if x > X0:
            VL(x, y, y + 8, K("madera", 1))
            PX(x + 2, y + 3, K("madera", 1)); PX(x + 2, y + 5, K("madera", 1))  # clavos
        # veta y nudos (solo si la tabla tiene sitio dentro de la habitación)
        lo, hi = max(X0 + 2, x + 4), min(X1 - 14, x + w - 8)
        if hi > lo:
            for _ in range(2):
                gx, gy = random.randint(lo, hi), y + random.randint(3, 6)
                HL(gx, gx + random.randint(4, 12), gy, K("madera", 2))
            if random.random() < 0.15:
                kx = random.randint(lo, hi)
                PX(kx, y + 4, K("madera", 1)); PX(kx + 1, y + 4, K("madera", 2)); PX(kx, y + 5, K("madera", 2))
        x += w
# ratonera en el zócalo
cv.ellipse(424, 78, 430, 86, K("gris", 0))

# ---------------------------------------------------------------- muros laterales e inferior
R(X0 - CAP, WT, X0, FB + CAP, K("gris", 3)); VL(X0 - 1, WT, FB, K("gris", 1)); VL(X0 - CAP, WT - CAP, FB + CAP, K("gris", 4))
R(X1, WT, X1 + CAP, FB + CAP, K("gris", 3)); VL(X1, WT, FB, K("gris", 1)); VL(X1 + CAP - 1, WT - CAP, FB + CAP, K("gris", 2))
R(X0 - CAP, FB, X1 + CAP, FB + CAP, K("gris", 3)); HL(X0, X1, FB, K("gris", 2)); HL(X0 - CAP, X1 + CAP, FB + CAP - 1, K("gris", 1))
# puerta y felpudo
DX0, DX1 = 224, 256
R(DX0, FB, DX1, FB + CAP, K("madera", 2)); HL(DX0, DX1, FB, K("madera", 1))
VL(DX0, FB, FB + CAP, K("gris", 1)); VL(DX1 - 1, FB, FB + CAP, K("gris", 1))
R(DX0 + 2, FB - 14, DX1 - 2, FB - 2, K("tela", 1))
for y in range(FB - 13, FB - 3, 2):
    HL(DX0 + 3, DX1 - 3, y, K("tela", 2))

# ---------------------------------------------------------------- cama de hierro
BX0, BX1, BY0, BY1 = 52, 100, 64, 166
R(BX0 + 3, BY0 + 20, BX1 + 4, BY1 + 6, K("madera", 1))             # sombra
# cabecero de barrotes (contra la pared)
R(BX0, BY0, BX1, BY0 + 3, K("gris", 5)); HL(BX0, BX1, BY0, K("gris", 7))
for x in range(BX0 + 2, BX1 - 1, 5):
    VL(x, BY0 + 3, BY0 + 20, K("gris", 4)); VL(x + 1, BY0 + 3, BY0 + 20, K("gris", 6))
R(BX0 - 2, BY0 - 4, BX0 + 2, BY0 + 22, K("gris", 4)); R(BX1 - 2, BY0 - 4, BX1 + 2, BY0 + 22, K("gris", 4))
PX(BX0 - 1, BY0 - 4, K("gris", 7)); PX(BX1 - 1, BY0 - 4, K("gris", 7))
# colchón, sábana, almohada
R(BX0 + 1, BY0 + 18, BX1 - 1, BY1, K("papel", 2))
R(BX0 + 5, BY0 + 21, BX1 - 5, BY0 + 35, K("papel", 4))
HL(BX0 + 5, BX1 - 5, BY0 + 34, K("papel", 2)); VL(BX0 + 24, BY0 + 23, BY0 + 33, K("papel", 3))
# manta de lana gris con franja
R(BX0 + 1, BY0 + 42, BX1 - 1, BY1, K("tela", 2))
R(BX0 + 1, BY0 + 40, BX1 - 1, BY0 + 44, K("papel", 3))                # embozo
R(BX0 + 1, BY0 + 54, BX1 - 1, BY0 + 57, K("granate", 3))               # franja
for y in range(BY0 + 62, BY1 - 4, 7):
    cv.d.line([BX0 + 6, y, BX0 + 18, y + 3], fill=K("tela", 1))
    cv.d.line([BX0 + 26, y + 2, BX1 - 8, y], fill=K("tela", 1))
VL(BX0 + 1, BY0 + 42, BY1, K("tela", 3))
# periódico sobre la cama
R(BX0 + 24, BY0 + 66, BX0 + 42, BY0 + 80, K("papel", 3))
for y in range(BY0 + 68, BY0 + 79, 2):
    HL(BX0 + 26, BX0 + 40, y, K("papel", 1))
R(BX0 + 26, BY0 + 68, BX0 + 32, BY0 + 72, K("gris", 4))
# frente del somier y patas
R(BX0, BY1, BX1, BY1 + 5, K("gris", 4)); HL(BX0, BX1, BY1, K("gris", 6))
R(BX0, BY1 + 5, BX0 + 3, BY1 + 9, K("gris", 3)); R(BX1 - 3, BY1 + 5, BX1, BY1 + 9, K("gris", 3))

# ---------------------------------------------------------------- alfombra
RX0, RY0, RX1, RY1 = 168, 140, 312, 210
R(RX0, RY0, RX1, RY1, K("granate", 3))
cv.frame(RX0, RY0, RX1, RY1, K("granate", 1))
cv.frame(RX0 + 3, RY0 + 3, RX1 - 3, RY1 - 3, K("granate", 5))
cv.frame(RX0 + 6, RY0 + 6, RX1 - 6, RY1 - 6, K("granate", 2))
for x in range(RX0 + 10, RX1 - 10, 8):           # greca
    PX(x, RY0 + 4, K("granate", 1)); PX(x + 4, RY1 - 5, K("granate", 1))
cx_, cy_ = (RX0 + RX1) // 2, (RY0 + RY1) // 2
cv.poly([(cx_, cy_ - 14), (cx_ + 26, cy_), (cx_, cy_ + 14), (cx_ - 26, cy_)], K("granate", 4))
cv.poly([(cx_, cy_ - 8), (cx_ + 14, cy_), (cx_, cy_ + 8), (cx_ - 14, cy_)], K("granate", 2))
for _ in range(90):                               # desgaste
    PX(random.randint(RX0 + 30, RX1 - 30), random.randint(RY0 + 20, RY1 - 18), K("granate", 2))
for x in range(RX0, RX1, 3):                      # flecos
    PX(x, RY0 - 1, K("papel", 1)); PX(x + 1, RY1, K("papel", 1))

# ---------------------------------------------------------------- mesa, silla y objetos
MX0, MX1, MY0, MY1 = 352, 416, 122, 150
R(MX0 + 3, MY1 + 4, MX1 + 4, MY1 + 22, K("madera", 1))            # sombra
R(MX0, MY0, MX1, MY1, K("madera", 4))
cv.frame(MX0, MY0, MX1, MY1, K("madera", 2))
HL(MX0 + 1, MX1 - 1, MY0 + 1, K("madera", 5))
for y in range(MY0 + 7, MY1 - 2, 7):
    HL(MX0 + 2, MX1 - 2, y, K("madera", 3))
R(MX0, MY1, MX1, MY1 + 5, K("madera", 3)); HL(MX0, MX1, MY1 + 4, K("madera", 1))
for x in (MX0 + 2, MX1 - 6):
    R(x, MY1 + 5, x + 4, MY1 + 20, K("madera", 2)); VL(x, MY1 + 5, MY1 + 20, K("madera", 3))
# hornillo con hervidor
R(MX0 + 5, MY0 + 4, MX0 + 23, MY0 + 18, K("gris", 3)); cv.frame(MX0 + 5, MY0 + 4, MX0 + 23, MY0 + 18, K("gris", 1))
cv.ellipse(MX0 + 8, MY0 + 6, MX0 + 20, MY0 + 16, K("gris", 2), outline=K("gris", 5))
cv.ellipse(MX0 + 9, MY0 + 2, MX0 + 19, MY0 + 12, K("gris", 6), outline=K("gris", 3))
HL(MX0 + 11, MX0 + 17, MY0 + 3, K("gris", 8)); R(MX0 + 18, MY0 + 5, MX0 + 22, MY0 + 7, K("gris", 5))
# taza, pan, botella de ginebra y cigarrillos
R(MX0 + 30, MY0 + 6, MX0 + 36, MY0 + 13, K("papel", 3)); HL(MX0 + 30, MX0 + 36, MY0 + 6, K("papel", 4))
PX(MX0 + 37, MY0 + 9, K("papel", 3)); R(MX0 + 31, MY0 + 7, MX0 + 35, MY0 + 8, K("madera", 1))
cv.ellipse(MX0 + 26, MY0 + 16, MX0 + 40, MY0 + 25, K("papel", 2), outline=K("papel", 1))
R(MX0 + 29, MY0 + 18, MX0 + 35, MY0 + 22, K("madera", 2))
R(MX0 + 46, MY0 + 2, MX0 + 52, MY0 + 18, K("tele", 3)); R(MX0 + 47, MY0 - 2, MX0 + 51, MY0 + 2, K("tele", 2))
R(MX0 + 46, MY0 + 8, MX0 + 52, MY0 + 13, K("papel", 4)); PX(MX0 + 48, MY0 + 10, K("rojo", 3))
VL(MX0 + 47, MY0 + 3, MY0 + 8, K("tele", 5))
R(MX0 + 54, MY0 + 18, MX0 + 61, MY0 + 23, K("rojo", 3)); HL(MX0 + 54, MX0 + 61, MY0 + 18, K("rojo", 5))
# silla (vista desde atrás, delante de la mesa)
SX0 = 370
R(SX0 + 2, 166, SX0 + 26, 182, K("madera", 1))
R(SX0, 154, SX0 + 22, 168, K("madera", 4)); cv.frame(SX0, 154, SX0 + 22, 168, K("madera", 2))
R(SX0, 150, SX0 + 22, 154, K("madera", 3))
for x in (SX0 + 1, SX0 + 18):
    R(x, 168, x + 3, 180, K("madera", 2))
R(SX0, 140, SX0 + 22, 143, K("madera", 3)); HL(SX0, SX0 + 22, 140, K("madera", 5))
for x in (SX0 + 1, SX0 + 19):
    R(x, 140, x + 2, 154, K("madera", 3))

# ---------------------------------------------------------------- perchero con el abrigo (junto a la puerta)
CX = 200
R(CX + 3, 236, CX + 14, 240, K("madera", 1))
R(CX + 4, 180, CX + 7, 238, K("madera", 2)); VL(CX + 4, 180, 238, K("madera", 4))
R(CX, 234, CX + 12, 238, K("madera", 3))
R(CX - 1, 180, CX + 12, 182, K("madera", 3))
def espejo(m):
    return [x + x[::-1] for x in m]
COAT = espejo([
    "......gg",
    "....gccc",
    "...gGcHc",
    "..gGGcGc",
    ".gGGGGcc",
    "gHGGGGGc",
    "gHGGGGGb",
    "gHGGGGGc",
    "gHgGGGGc",
    "gHgGGGGb",
    "gHgGGGGc",
    "gHgGppGc",
    "gHgGGGGc",
    "gggGGGGb",
    ".ggGGGGc",
    "..gGGGGc",
    "..gGGGGc",
    "..gGGGGc",
    "..gGGGGc",
    "..gGGGGc",
    "..gGGGGc",
    "..gGGGGc",
    "..gGGGGc",
    "..gGGGGc",
    "..gGGGGc",
    "..gHGGGc",
    "..gHGGGc",
    ".gHGGGGc",
    ".gggggg.",
])
R(CX + 4, 176, CX + 7, 180, K("madera", 2))                        # gancho
cv.grid(CX - 2, 180, COAT, {"g": K("tela", 0), "G": K("tela", 2), "H": K("tela", 3),
                            "c": K("tela", 1), "p": K("tela", 1), "b": K("gris", 6)})

# ---------------------------------------------------------------- protagonista (16x32)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "personajes"))
import protagonista  # noqa: E402
if "--sin-protagonista" not in sys.argv:
    protagonista.dibujar(cv, 230, 148, "abajo", sombra=K("granate", 1))

# ---------------------------------------------------------------- iluminación
def beam(x, y):
    # haz de la ventana: cae en diagonal sobre el suelo
    if y < WB:
        return 0
    t = y - WB
    x0 = WX0 - 6 + t * 0.62
    x1 = WX1 + 10 + t * 0.62
    if x0 <= x <= x1 and t < 130:
        return 2 if (x0 + 6 <= x <= x1 - 6 and t < 80) else 1
    return 0

cv.add_light_fn(beam)
cv.add_light_fn(lambda x, y: -1 if (WB <= y < FB and (x < X0 + 5 or x >= X1 - 5 or y >= FB - 5)) else 0)
cv.add_light_fn(lambda x, y: -1 if y < WT + 6 and WT <= y else 0)
cv.add_glow((TX0 + TX1) / 2, TY1 + 18, radii=[40, 70, 100], strengths=[0.26, 0.15, 0.07], squash=1.5)
for y in range(H):
    for x in range(W):
        if not (X0 <= x < X1 and WT <= y < FB):
            cv.glow[y][x] = 0.0

cv.bake_lighting()
salida = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--salida=")), None)
if salida:
    cv.img.save(salida)
    print("ok", salida)
    sys.exit(0)
prev = cv.save(Path(__file__).parent / "piso_hd.png", preview_scale=3)
print("ok", prev)
