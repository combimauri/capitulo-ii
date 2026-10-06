"""Las dos fotos de Ivy (160x110, mismo formato FW x FH que foto_sotano / foto_iniciacion de vinetas.py).

foto_ivy(genero): la foto que el protagonista guarda en el cajón (J4.01). Un parque, dos niños: Ivy, de unos
    diez años, con el uniforme de los Espías (camisa clara y pañuelo al cuello), y el protagonista, algo mayor,
    a su lado, tirándole de una trenza. Blanco y negro viejo, desvaído y con grano; arrugada (dos pliegues con la
    emulsión cuarteada), quemada por la esquina de abajo a la derecha (papel ennegrecido, abarquillado y ceniza)
    y con una mancha de agua (un cerco de humedad con la emulsión corrida) que borra casi por completo la cara
    de Ivy. La quemadura no llega a ninguna cara.
foto_ivy_restaurada(genero): la misma foto positivada de nuevo por Crane (J6.04), restaurada «del agua y el
    fuego»: la misma composición, entera, más nítida y más cálida (luces de papel, negros profundos). Ivy sonríe
    abiertamente y le falta un diente; el pañuelo de los Espías lleva un toque de color a mano, muy tenue.
genero "h" / "m": el protagonista de niño o de niña (pelo y ropa). Ivy es igual en las dos.

Al mostrarse como viñeta, el juego la escala x6 y recorta 10 px arriba y abajo: lo importante va en y 10-100.
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from pixel import LOOKUP, Canvas, K  # noqa: E402

FW, FH = 160, 110
BX0, BY0, BX1, BY1 = 6, 6, FW - 6, FH - 10          # la imagen dentro del margen blanco

# rampas de positivado: el tono 0-10 de la escena -> color de la paleta
RESTAURADA = [K("gris", i) for i in range(6)] + [K("papel", i) for i in range(5)]          # negros fríos, luces de papel
VIEJA = [K("gris", i) for i in (2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8)] + [K("papel", 2)]      # desvaída: sin negros ni blancos
# el pañuelo coloreado a mano (muy tenue): tono -> color
PANUELO = {1: K("granate", 1), 2: K("granate", 2), 3: K("granate", 3), 4: K("granate", 4), 5: K("granate", 4),
           6: K("granate", 5), 7: K("granate", 5)}

IVY_CX, IVY_TOP = 60, 26        # centro y coronilla de Ivy
PRO_CX, PRO_TOP = 106, 12       # el protagonista, algo mayor: más alto

# caras en tonos 0-9 (a = 10), «.» = transparente. Se escriben por mitades (la derecha es el reflejo) y luego se
# retocan píxel a píxel; el sol viene de arriba a la izquierda, así que el lado derecho baja un tono.
IVY_MITAD = [
    "......111", "....11224", "...112233", "..1122222", "..1222277", ".11227777", ".12277777", ".12777777",
    ".12743377", ".12777777", ".67761167", ".67776677", ".67888777", ".27756666", ".27773aaa", ".27776299",
    ".27777634", ".22777766", ".22277777", "..2227777", "...222666",
]
IVY_RETOQUES = {(11, 9): "6", (12, 8): "7", (12, 9): "5",                                    # nariz
                (14, 8): "1", (15, 8): "2"}                                                   # el diente que falta
PRO_MITAD = [
    ".....1111", "...112222", "..1122233", "..1223322", ".11222222", ".12222222", ".12222222", ".12777777",
    ".17777777", ".17743377", ".17777777", ".67701877", ".67766777", ".67888777", ".17777777", ".17777777",
    ".17777777", ".17777777", "..1777777", "...177777", "....66666",
]
PRO_RETOQUES = {(11, 11): "0", (11, 12): "1", (11, 13): "8", (12, 11): "6", (12, 12): "6", (12, 13): "7",  # miran a Ivy
                (13, 9): "5", (14, 8): "6", (14, 9): "5",                                         # nariz
                (9, 11): "7", (9, 12): "7", (9, 13): "7", (8, 11): "3", (8, 12): "3", (8, 13): "4",   # una ceja levantada
                (15, 12): "5", (16, 6): "5", (16, 7): "2", (16, 8): "2", (16, 9): "2", (16, 10): "2", (16, 11): "2",
                (17, 7): "6", (17, 8): "9", (17, 9): "a", (17, 10): "9", (17, 11): "3", (18, 8): "6", (18, 9): "6",
                (18, 10): "6"}                                                                    # sonrisa de medio lado


def _g(i):
    return K("gris", max(0, min(10, i)))


def _cara(cv, x, y, mitad, retoques, sombra=12):
    filas = [list(m + m[::-1]) for m in mitad]
    for (r, c), ch in retoques.items():
        filas[r][c] = ch
    for r, fila in enumerate(filas):
        for c, ch in enumerate(fila):
            if ch == ".":
                continue
            v = 10 if ch == "a" else int(ch)
            if c >= sombra and 6 <= v <= 8:
                v -= 1
            cv.px(x + c, y + r, _g(v))


# ---------------------------------------------------------------- la escena, en tonos de gris (0-10)


def _copa(cv, rnd, x0, x1, y0, y1, base, n):
    """Masa de follaje: muchas bolitas con la luz arriba a la izquierda."""
    for _ in range(n):
        x, y, r = rnd.randint(x0, x1), rnd.randint(y0, y1), rnd.randint(3, 6)
        cv.ellipse(x - r, y - r, x + r, y + r, _g(base - 1))
        cv.ellipse(x - r, y - r, x + r - 1, y + r - 1, _g(base))
        cv.ellipse(x - r + 1, y - r + 1, x, y, _g(base + 1))


def _parque(cv, rnd):
    """Fondo: cielo claro, arboleda, un banco, una farola, el césped y un camino de grava. Sol arriba a la izquierda."""
    cv.rect(0, 0, FW, FH, _g(9))
    for x in range(FW):                                                                       # nubes tenues
        for y in range(4, 22):
            if math.sin(x / 9.0 + y / 4.0) + math.sin(x / 23.0) > 1.35:
                cv.px(x, y, _g(10))
    _copa(cv, rnd, 0, FW, 34, 46, 7, 70)                                                      # arboleda lejana
    _copa(cv, rnd, 40, FW, 40, 50, 5, 40)                                                     # más cerca
    cv.rect(0, 50, FW, FH, _g(6))                                                             # césped
    for _ in range(500):
        x, y = rnd.randrange(FW), rnd.randrange(50, FH)
        cv.vline(x, y, y + 2, _g(rnd.choice((5, 5, 7))))
    cv.poly([(0, 74), (0, 92), (70, 64), (130, 54), (150, 52), (122, 52), (60, 60)], _g(8))    # camino
    for _ in range(140):
        x, y = rnd.randrange(0, 150), rnd.randrange(52, 92)
        if cv.img.getpixel((x, y)) == _g(8):
            cv.px(x, y, _g(rnd.choice((7, 9))))
    # banco detrás, a la derecha (casi tapado)
    for k, y in enumerate((46, 49, 55, 58)):
        cv.rect(126, y, 158, y + 2, _g(3 if k < 2 else 2)); cv.hline(126, 158, y, _g(4 if k < 2 else 3))
    for x in (129, 154):
        cv.rect(x, 46, x + 2, 66, _g(1))
    cv.vline(146, 20, 50, _g(3)); cv.vline(147, 20, 50, _g(2))                                  # farola
    cv.rect(143, 15, 150, 21, _g(2)); cv.rect(144, 16, 149, 19, _g(8))
    # un árbol grande a la izquierda: tronco y copa oscura
    cv.rect(12, 14, 19, 58, _g(2)); cv.vline(12, 14, 58, _g(4)); cv.vline(18, 14, 58, _g(1))
    cv.d.line([(15, 28), (4, 14)], fill=_g(2), width=2); cv.d.line([(17, 24), (30, 10)], fill=_g(2), width=2)
    cv.ellipse(8, 55, 28, 60, _g(4))
    _copa(cv, rnd, -4, 40, 0, 18, 4, 26)


def _sombra_suelo(cv, x0, x1, y0, y1):
    for x in range(x0, x1):
        for y in range(y0, min(FH, y1)):
            c = cv.img.getpixel((x, y))
            if c in LOOKUP and LOOKUP[c][0] == "gris":
                cv.px(x, y, _g(LOOKUP[c][1] - 2))


def _trenza(cv, x, y0, y1, tiron=0):
    """Trenza de mechones alternos; `tiron` la desplaza hacia la derecha por abajo (alguien tira de ella)."""
    for k, y in enumerate(range(y0, y1, 3)):
        t = (y - y0) / max(1, y1 - y0)
        xx = x + int(round(tiron * t * t))
        cv.rect(xx - 1, y, xx + 2, y + 3, _g(2 if k % 2 else 3)); cv.px(xx + (k % 2), y + 2, _g(1))
        if k % 2 == 0:
            cv.px(xx - 1, y, _g(4))
    xx = x + tiron
    cv.rect(xx - 2, y1, xx + 3, y1 + 2, _g(9)); cv.px(xx - 2, y1 + 2, _g(9)); cv.px(xx + 2, y1 + 2, _g(8))   # lazo
    cv.rect(xx - 1, y1 + 2, xx + 2, y1 + 5, _g(2)); cv.px(xx, y1 + 5, _g(2))                    # la punta


def _ivy(cv, mascara):
    cx, top = IVY_CX, IVY_TOP
    # piernas, pantalón corto con cinturón y camisa del uniforme
    for (lx, t) in ((cx - 7, 8), (cx + 2, 7)):
        cv.rect(lx, 86, lx + 5, FH, _g(t)); cv.vline(lx, 86, FH, _g(t - 2)); cv.vline(lx + 4, 86, FH, _g(t - 1))
        cv.hline(lx + 1, lx + 4, 96, _g(t - 1))
    cv.rect(cx - 10, 74, cx + 11, 88, _g(3)); cv.vline(cx, 79, 88, _g(2)); cv.vline(cx + 10, 74, 88, _g(2))
    cv.rect(cx - 10, 74, cx + 11, 76, _g(2)); cv.rect(cx - 1, 74, cx + 2, 76, _g(7))
    cv.poly([(cx - 12, 75), (cx - 13, 52), (cx - 7, 48), (cx + 7, 48), (cx + 13, 52), (cx + 12, 75)], _g(9))
    cv.poly([(cx + 4, 49), (cx + 13, 52), (cx + 12, 75), (cx + 6, 75)], _g(8))                  # lado en sombra
    cv.vline(cx, 54, 74, _g(7)); cv.vline(cx + 1, 54, 74, _g(8))                                # tapeta y botones
    for y in (58, 64, 70):
        cv.px(cx + 1, y, _g(5))
    for px_ in (cx - 9, cx + 3):                                                                 # bolsillos con solapa
        cv.frame(px_, 57, px_ + 6, 64, _g(7)); cv.rect(px_, 57, px_ + 6, 59, _g(8)); cv.hline(px_, px_ + 6, 59, _g(6))
    cv.d.line([(cx - 9, 68), (cx - 5, 73)], fill=_g(8)); cv.d.line([(cx + 8, 67), (cx + 5, 73)], fill=_g(7))   # arrugas
    cv.rect(cx - 13, 49, cx - 8, 52, _g(8)); cv.rect(cx + 8, 49, cx + 13, 52, _g(7))             # hombreras
    # brazos: manga corta y el brazo desnudo; las manos junto al pantalón
    cv.poly([(cx - 12, 51), (cx - 17, 62), (cx - 12, 64), (cx - 10, 56)], _g(9))
    cv.poly([(cx - 17, 62), (cx - 17, 80), (cx - 13, 80), (cx - 12, 64)], _g(8))
    cv.vline(cx - 17, 62, 80, _g(6)); cv.rect(cx - 17, 80, cx - 12, 85, _g(8)); cv.px(cx - 13, 84, _g(6))
    cv.poly([(cx + 12, 51), (cx + 16, 62), (cx + 12, 64), (cx + 11, 56)], _g(8))
    cv.poly([(cx + 16, 62), (cx + 16, 80), (cx + 12, 80), (cx + 12, 64)], _g(7))
    cv.vline(cx + 15, 62, 80, _g(5)); cv.rect(cx + 12, 80, cx + 17, 85, _g(7))
    # el pañuelo de los Espías: vuelta al cuello, nudo y dos puntas sobre el pecho
    for d in (cv, mascara):
        g = _g if d is cv else (lambda i: _g(10))
        d.poly([(cx - 6, 46), (cx + 7, 46), (cx + 6, 50), (cx - 5, 50)], g(4))
        d.hline(cx - 5, cx + 6, 49, g(3))
        d.rect(cx - 1, 49, cx + 3, 53, g(3)); d.px(cx, 50, g(5))
        d.poly([(cx - 1, 52), (cx + 1, 52), (cx - 2, 61), (cx - 4, 60)], g(4))
        d.poly([(cx + 1, 52), (cx + 3, 52), (cx + 5, 60), (cx + 3, 61)], g(3))
        d.px(cx - 3, 60, g(2)); d.px(cx + 4, 60, g(2))
    # cabeza (las trenzas, por detrás de los hombros y por delante del pecho)
    cv.rect(cx - 2, top + 20, cx + 3, 47, _g(6)); cv.hline(cx - 2, cx + 3, top + 20, _g(5))
    _cara(cv, cx - 9, top, IVY_MITAD, IVY_RETOQUES, sombra=13)
    _trenza(cv, cx - 9, top + 18, top + 31)
    _trenza(cv, cx + 9, top + 18, top + 29, tiron=3)


def _protagonista(cv, genero):
    cx, top = PRO_CX, PRO_TOP
    m = genero == "m"
    tela, sombra = (_g(8), _g(7)) if m else (_g(4), _g(3))
    # cuerpo: jersey de pico con el cuello de la camisa (niño) o blusa con pichi (niña)
    cv.poly([(cx - 15, FH), (cx - 16, 36), (cx - 9, 31), (cx + 9, 31), (cx + 16, 36), (cx + 16, FH)], tela)
    cv.poly([(cx + 6, 32), (cx + 16, 36), (cx + 16, FH), (cx + 8, FH)], sombra)
    if m:                                                                                       # la blusa clara, recortada contra el césped
        cv.d.line([(cx - 15, FH), (cx - 16, 36)], fill=_g(6)); cv.d.line([(cx + 16, 36), (cx + 16, FH)], fill=_g(5))
    if m:
        cv.poly([(cx - 10, FH), (cx - 9, 46), (cx + 9, 46), (cx + 11, FH)], _g(3))              # pichi
        cv.rect(cx - 9, 36, cx - 6, 47, _g(3)); cv.rect(cx + 6, 36, cx + 9, 47, _g(3))           # tirantes
        cv.vline(cx + 8, 46, FH, _g(2)); cv.hline(cx - 9, cx + 9, 46, _g(4))
        cv.rect(cx - 4, 50, cx + 4, 56, _g(2)); cv.hline(cx - 4, cx + 4, 50, _g(4))               # bolsillo del pichi
        cv.poly([(cx - 5, 31), (cx, 35), (cx - 7, 36)], _g(10)); cv.poly([(cx + 5, 31), (cx, 35), (cx + 7, 36)], _g(9))
    else:
        cv.poly([(cx - 5, 31), (cx + 5, 31), (cx, 42)], _g(8))                                  # el pico
        cv.d.line([(cx - 5, 31), (cx, 42), (cx + 5, 31)], fill=_g(2))
        cv.poly([(cx - 5, 31), (cx, 35), (cx - 7, 35)], _g(10)); cv.poly([(cx + 5, 31), (cx, 35), (cx + 7, 35)], _g(8))
        for y in range(78, 84, 2):
            cv.hline(cx - 15, cx + 16, y, _g(3))                                                # elástico del jersey
        cv.rect(cx - 15, 84, cx + 16, FH, _g(2)); cv.vline(cx, 88, FH, _g(1))                    # pantalón
        cv.d.line([(cx - 10, 50), (cx - 6, 60)], fill=_g(3)); cv.d.line([(cx + 6, 62), (cx + 9, 70)], fill=_g(2))
    cv.rect(cx - 3, top + 20, cx + 3, 32, _g(6)); cv.hline(cx - 3, cx + 3, top + 20, _g(5))      # cuello
    # brazo derecho, colgando
    cv.poly([(cx + 15, 35), (cx + 20, 58), (cx + 16, 60), (cx + 13, 40)], sombra)
    cv.poly([(cx + 20, 58), (cx + 20, 76), (cx + 16, 76), (cx + 16, 60)], sombra)
    cv.vline(cx + 19, 40, 76, _g(5 if m else 2))
    cv.rect(cx + 16, 76, cx + 21, 82, _g(7)); cv.vline(cx + 20, 76, 82, _g(6))
    # brazo izquierdo: cruza hasta la trenza de Ivy y tira de ella
    cv.poly([(cx - 15, 34), (cx - 12, 43), (cx - 22, 50), (cx - 25, 44)], tela)
    cv.poly([(cx - 25, 44), (cx - 22, 50), (cx - 31, 56), (cx - 33, 51)], tela)
    cv.d.line([(cx - 13, 43), (cx - 22, 50), (cx - 31, 56)], fill=_g(5 if m else 2))          # el canto de abajo
    cv.d.line([(cx - 16, 35), (cx - 25, 44), (cx - 33, 51)], fill=_g(9 if m else 5))          # el de arriba, al sol
    # cabeza
    _cara(cv, cx - 9, top, PRO_MITAD, PRO_RETOQUES, sombra=13)
    if m:                                                                                       # melena con flequillo y horquilla
        for (x0, x1, t) in ((cx - 10, cx - 7, 2), (cx + 7, cx + 10, 1)):
            cv.rect(x0, top + 5, x1, top + 21, _g(t))
        cv.px(cx - 10, top + 21, _g(1)); cv.px(cx + 9, top + 21, _g(1))
        cv.rect(cx - 7, top + 4, cx + 8, top + 8, _g(2))
        for k in range(cx - 6, cx + 7, 3):
            cv.px(k, top + 8, _g(2)); cv.px(k + 1, top + 8, _g(3))
        cv.d.line([(cx - 7, top + 2), (cx - 2, top)], fill=_g(4))
        cv.hline(cx + 7, cx + 10, top + 7, _g(8)); cv.px(cx + 10, top + 7, _g(6))               # horquilla


def _mano_en_trenza(cv):
    """El puño del protagonista cerrado sobre la trenza derecha de Ivy."""
    hx, hy = IVY_CX + 10, IVY_TOP + 23
    cv.rect(hx + 3, hy - 1, hx + 9, hy + 4, _g(2))                                              # puño de la manga
    cv.rect(hx - 2, hy - 2, hx + 4, hy + 3, _g(7))
    cv.hline(hx - 1, hx + 4, hy - 2, _g(8)); cv.px(hx - 2, hy - 2, _g(6))
    cv.vline(hx - 2, hy - 1, hy + 3, _g(5)); cv.hline(hx - 1, hx + 4, hy + 3, _g(5))
    cv.hline(hx - 1, hx + 3, hy + 1, _g(6))                                                     # los dedos cerrados
    cv.px(hx + 4, hy - 1, _g(6))


def _escena(genero):
    """Devuelve (lienzo en tonos de gris, máscara del pañuelo)."""
    rnd = random.Random(1965)
    cv = Canvas(FW, FH, bg=("gris", 9))
    mascara = Canvas(FW, FH, bg=("gris", 0))
    _parque(cv, rnd)
    _sombra_suelo(cv, 64, 84, 98, FH); _sombra_suelo(cv, 116, 134, 98, FH)
    _protagonista(cv, genero)
    _ivy(cv, mascara)
    _mano_en_trenza(cv)
    return cv, mascara


def _tonos(cv):
    return [[LOOKUP.get(cv.img.getpixel((x, y)), ("gris", 0))[1] for x in range(FW)] for y in range(FH)]


def _suavizar(t):
    """Desenfoque leve (la foto vieja, peor positivada)."""
    out = [fila[:] for fila in t]
    for y in range(1, FH - 1):
        for x in range(1, FW - 1):
            s = 4 * t[y][x] + t[y - 1][x] + t[y + 1][x] + t[y][x - 1] + t[y][x + 1]
            out[y][x] = int(round(s / 8))
    return out


def _grano(t, rnd, n):
    for _ in range(n):
        x, y = rnd.randrange(FW), rnd.randrange(FH)
        t[y][x] = max(0, min(10, t[y][x] + rnd.choice((-1, 1))))


# ---------------------------------------------------------------- daños de la foto vieja


def _mancha_agua(t, cerco, rnd):
    """Un cerco de humedad sobre la cara de Ivy: dentro, la emulsión corrida y lavada hasta casi el blanco."""
    cx, cy = IVY_CX + 1, IVY_TOP + 10
    radio = [15 + 2.5 * math.sin(a / 64 * 2 * math.pi * 3 + 1) + 1.2 * math.sin(a / 64 * 2 * math.pi * 5) for a in range(64)]

    def r_en(x, y):
        a = math.atan2((y - cy) * 1.15, x - cx)
        i = int((a + math.pi) / (2 * math.pi) * 64) % 64
        return math.hypot(x - cx, (y - cy) * 1.15), radio[i]

    for y in range(FH):
        for x in range(FW):
            d, r = r_en(x, y)
            if d < r - 1:
                lavado = 9 if d < r * 0.7 else 8
                v = t[y][x] * 0.25 + lavado * 0.75 + math.sin(x / 2.3 + y / 3.1) * 0.6 + rnd.uniform(-0.5, 0.5)
                t[y][x] = max(5, min(9, int(round(v))))
            elif d < r + 0.8:
                cerco[(x, y)] = K("papel", 0)                                                  # la marca de marea
            elif d < r + 1.8 and (x * 3 + y) % 4 == 0:
                cerco[(x, y)] = K("papel", 1)
    # la emulsión que se corrió hacia abajo: un reguero lavado
    for y in range(cy + 12, cy + 26):
        for x in range(cx - 3 + (y - cy) // 6, cx + 2 + (y - cy) // 6):
            if 0 <= x < FW and 0 <= y < FH and (x, y) not in cerco:
                t[y][x] = max(t[y][x], 6)


def _pliegues(t, extra):
    """Dos pliegues: el lado que levanta coge luz, el otro hace sombra, y la emulsión se cuartea en la arista."""
    for (x0, y0, x1, y1) in ((0, 74, FW, 44), (136, 0, 128, FH)):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for k in range(n + 1):
            x = round(x0 + (x1 - x0) * k / n + (1.5 * math.sin(k / 9.0) if x1 - x0 < 20 else 0))
            y = round(y0 + (y1 - y0) * k / n + (1.5 * math.sin(k / 11.0) if x1 - x0 >= 20 else 0))
            if not (0 <= x < FW and 0 <= y < FH):
                continue
            t[y][x] = min(10, t[y][x] + 3)
            if abs(x1 - x0) >= 20 and y + 1 < FH:
                t[y + 1][x] = max(0, t[y + 1][x] - 1)
            elif x + 1 < FW:
                t[y][x + 1] = max(0, t[y][x + 1] - 1)
            if k % 5 == 0:
                extra[(x, y)] = K("papel", 3)


def _quemar(cv, rnd):
    """La esquina de abajo a la derecha, quemada: falta el papel, el borde se ennegrece y se abarquilla."""
    px = cv.img.load()
    fondo = lambda x, y: K("madera", 1) if (y + int(3 * math.sin(x / 13.0))) % 7 else K("madera", 0)   # el fondo del cajón
    ruido = [rnd.uniform(-2.5, 2.5) for _ in range(FW + FH)]

    def linea(x, y):
        """>0 dentro de la foto; <0 quemado. Distancia (aprox.) al borde de la quemadura."""
        k = (FW - x) * 0.85 + (FH - y)
        i = int(x + (FH - y))
        return (k - 56 + 6 * math.sin(x / 8.0 + 1) + 4 * math.sin(y / 5.0) + 2 * math.sin((x + y) / 2.3)
                + ruido[i % len(ruido)])

    for y in range(FH):
        for x in range(FW):
            d = linea(x, y)
            if d < 0:
                # sombra que hace el borde abarquillado sobre el fondo
                px[x, y] = K("madera", 0) if d > -3 else fondo(x, y)
            elif d < 2:
                px[x, y] = K("gris", 0)                                                         # papel carbonizado
            elif d < 3.5:
                px[x, y] = K("gris", 1) if (x + y) % 3 else K("madera", 0)
            elif d < 6:
                px[x, y] = K("madera", 1 if d < 4.8 else 2)                                     # chamuscado
            elif d < 9 and rnd.random() < 0.7:
                px[x, y] = K("madera", 3) if d < 7.5 else K("ocre", 1)
            elif d < 11 and rnd.random() < 0.35:
                px[x, y] = K("ocre", 1)
    # el borde levantado: un trozo del dorso del papel, sin imprimir, asoma junto al carbón
    for x in range(96, 140):
        for y in range(FH):
            d = linea(x, y)
            if -3 < d < -0.5 and 108 < x + (FH - y) * 0.2 < 138:
                px[x, y] = K("papel", 2) if d > -2 else K("papel", 1)
    # ceniza
    for _ in range(120):
        x, y = rnd.randrange(80, FW), rnd.randrange(40, FH)
        d = linea(x, y)
        if -1.5 < d < 3:
            px[x, y] = K("gris", rnd.choice((5, 6, 7)))


# ---------------------------------------------------------------- positivado


def _positivar(t, rampa, mascara=None, tinte=False, extra=None):
    cv = Canvas(FW, FH, bg=("papel", 4))
    px = cv.img.load()
    for y in range(FH):
        for x in range(FW):
            v = max(0, min(len(rampa) - 1, t[y][x]))
            col = rampa[v]
            if tinte and mascara is not None and mascara.img.getpixel((x, y)) != K("gris", 0):
                col = PANUELO.get(v, col)
            px[x, y] = col
    for (x, y), col in (extra or {}).items():
        px[x, y] = col
    return cv


def _marco(cv, color, filo):
    for (x0, y0, x1, y1) in ((0, 0, FW, BY0), (0, BY1, FW, FH), (0, 0, BX0, FH), (BX1, 0, FW, FH)):
        cv.rect(x0, y0, x1, y1, color)
    cv.frame(0, 0, FW, FH, filo)
    cv.frame(BX0 - 1, BY0 - 1, BX1 + 1, BY1 + 1, filo)


def foto_ivy_restaurada(genero="h"):
    escena, mascara = _escena(genero)
    t = _tonos(escena)
    _grano(t, random.Random(6), 260)
    cv = _positivar(t, RESTAURADA, mascara, tinte=True)
    _marco(cv, K("papel", 4), K("papel", 2))
    return cv


def foto_ivy(genero="h"):
    rnd = random.Random(1979)
    escena, _ = _escena(genero)
    t = _suavizar(_tonos(escena))
    _grano(t, rnd, 2200)
    marcas = {}
    _mancha_agua(t, marcas, rnd)
    _pliegues(t, marcas)
    # foto vieja: el margen, amarillento y sobado, entra también en el positivado
    for y in range(FH):
        for x in range(FW):
            if not (BX0 <= x < BX1 and BY0 <= y < BY1):
                t[y][x] = 11
    cv = _positivar(t, VIEJA, extra=marcas)
    cv.frame(0, 0, FW, FH, K("papel", 1)); cv.frame(BX0 - 1, BY0 - 1, BX1 + 1, BY1 + 1, K("papel", 1))
    for _ in range(30):                                                                         # motas y suciedad
        cv.px(rnd.randrange(FW), rnd.randrange(FH), K("papel", rnd.choice((0, 1, 3))))
    cv.d.line([(0, 14), (6, 20)], fill=K("papel", 0))                                         # esquina gastada
    _quemar(cv, rnd)
    return cv


def exportar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    hechos = []
    for g in ("h", "m"):
        foto_ivy(g).img.save(destino / f"foto_ivy_{g}.png"); hechos.append(f"foto_ivy_{g}")
        foto_ivy_restaurada(g).img.save(destino / f"foto_ivy_restaurada_{g}.png"); hechos.append(f"foto_ivy_restaurada_{g}")
    return hechos


if __name__ == "__main__":
    salida = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    for g in ("h", "m"):
        foto_ivy(g).save(salida / f"foto_ivy_{g}.png", preview_scale=6)
        foto_ivy_restaurada(g).save(salida / f"foto_ivy_restaurada_{g}.png", preview_scale=6)
