"""J5.02–J5.05 — Mercado de Watney Street (960x270, la cámara sigue al jugador).

Puestos de madera con toldos remendados, mucha gente y, al fondo, el escaparate del Estudio Crane.
Variante "ruinas": después del cohete. Toldos ardiendo, polvo, la lata de Sammy volcada.
La paleta se desatura casi por completo, salvo el rojo.
"""
import random

from PIL import Image
from pixel import Canvas, K
import props as P
from limehouse import ladrillo

W, H = 960, 270
FACHADA, CALLE = 100, 236
CRATER = (520, 182)


def toldo(cv, x, y, w, colores, rnd, roto=False):
    for i, k in enumerate(range(x, x + w, 8)):
        cv.rect(k, y, min(x + w, k + 8), y + 10, colores[i % len(colores)])
    for k in range(x, x + w, 8):                                     # festón
        cv.px(k + 4, y + 11, colores[0])
    cv.hline(x, x + w, y + 10, K("gris", 1))
    for _ in range(3):                                               # remiendos
        rx = rnd.randint(x + 2, x + w - 8)
        cv.rect(rx, y + 2, rx + 5, y + 6, K("papel", 2))
    if roto:
        cv.poly([(x + w // 2, y + 10), (x + w // 2 + 10, y + 10), (x + w // 2 + 4, y + 22)], K("gris", 1))


def puesto(cv, x, y, w, colores, genero, rnd):
    toldo(cv, x - 4, y - 30, w + 8, colores, rnd)
    cv.vline(x - 2, y - 20, y + 16, K("madera", 1)); cv.vline(x + w + 2, y - 20, y + 16, K("madera", 1))
    cv.rect(x, y, x + w, y + 14, K("madera", 3)); cv.hline(x, x + w, y, K("madera", 4)); cv.rect(x, y + 14, x + w, y + 18, K("madera", 1))
    for k in range(x + 3, x + w - 4, 7):
        if genero == "patatas":
            cv.ellipse(k, y + 2, k + 5, y + 7, K("ocre", 1)); cv.ellipse(k + 2, y + 5, k + 7, y + 10, K("ocre", 2))
        elif genero == "retales":
            cv.rect(k, y + 2, k + 6, y + 11, rnd.choice([K("granate", 4), K("cielo", 5), K("ocre", 3), K("tele", 4), K("papel", 3)]))
        elif genero == "cacharros":
            cv.ellipse(k, y + 3, k + 6, y + 10, K("gris", 5), outline=K("gris", 2))
        elif genero == "cordones":
            cv.vline(k + 2, y + 1, y + 12, K("papel", 1)); cv.vline(k + 4, y + 1, y + 12, K("madera", 0))


def estudio(cv, x):
    """El escaparate del Estudio Crane: fotos enmarcadas y un rótulo pintado a mano."""
    cv.rect(x, 30, x + 96, FACHADA, K("madera", 1)); cv.frame(x, 30, x + 96, FACHADA, K("madera", 0))
    cv.rect(x + 4, 34, x + 92, 46, K("papel", 3)); cv.text(x + 48 - cv.text_width("ESTUDIO CRANE") // 2, 38, "ESTUDIO CRANE", K("madera", 0))
    cv.rect(x + 6, 52, x + 50, 92, K("cielo", 2))
    for (fx, fy) in [(x + 9, 55), (x + 27, 55), (x + 12, 74), (x + 31, 72)]:
        cv.rect(fx, fy, fx + 14, fy + 14, K("madera", 3)); cv.rect(fx + 2, fy + 2, fx + 12, fy + 12, K("papel", 2))
        cv.px(fx + 7, fy + 6, K("gris", 3)); cv.hline(fx + 5, fx + 9, fy + 9, K("gris", 3))
    P.puerta(cv, x + 60, FACHADA - 36, w=22, h=36, rampa="madera", base=2, cristal=True)


def fuego(cv, x, y, rnd):
    for _ in range(110):
        alto = rnd.randint(0, 26)
        fx, fy = x + rnd.randint(-12 + alto // 3, 12 - alto // 3), y - alto
        cv.px(fx, fy, rnd.choice([K("rojo", 4), K("rojo", 3), K("ocre", 4)]))
    cv.add_emissive(x - 12, y - 26, x + 12, y)


def desaturar(img):
    """Todo a gris salvo los rojos (J5.05)."""
    img = img.convert("RGB")
    px = img.load()
    for yy in range(img.height):
        for xx in range(img.width):
            r, g, b = px[xx, yy]
            rojo = r > 110 and r > g * 1.6 and r > b * 1.6
            if not rojo:
                v = int(0.3 * r + 0.59 * g + 0.11 * b)
                px[xx, yy] = (v, v, int(v * 1.03))
    return img


def dibujar(variante=None):
    ruinas = variante == "ruinas"
    rnd = random.Random(1905)
    cv = Canvas(W, H)
    for i, y in enumerate(range(0, 40, 8)):
        cv.rect(0, y, W, y + 8, K("cielo", 4 + i // 2))           # madrugada
    x = 0
    while x < 800:
        w = rnd.randint(70, 100)
        ladrillo(cv, x, rnd.randint(18, 30), x + w, FACHADA, rnd, base=2)
        for wx in range(x + 10, x + w - 14, 24):
            cv.rect(wx, 44, wx + 12, 60, K("gris", 1)); cv.hline(wx - 1, wx + 13, 61, K("gris", 5))
        x += w
    estudio(cv, 820)
    ladrillo(cv, 916, 26, W, FACHADA, rnd, base=1)
    P.adoquines(cv, 0, FACHADA, W, CALLE, semilla=12)
    # puestos
    puestos = [(40, 132, 70, "cacharros", [K("rojo", 3), K("papel", 3)]),
               (180, 132, 76, "patatas", [K("tele", 3), K("papel", 3)]),
               (330, 132, 80, "retales", [K("granate", 4), K("ocre", 3)]),            # el de Dot
               (650, 132, 60, "cordones", [K("cielo", 4), K("papel", 3)]),
               (120, 214, 70, "patatas", [K("ocre", 2), K("papel", 3)]),
               (720, 214, 70, "cacharros", [K("granate", 3), K("papel", 3)])]
    if not ruinas:
        for (px_, py, w, g, cols) in puestos:
            puesto(cv, px_, py, w, cols, g, rnd)
        # el bordillo donde se sienta Sammy, con su colección en filas
        for k in range(8):
            cv.px(498 + k * 3, 160, K("gris", 6)); cv.px(498 + k * 3, 163, K("gris", 5))
    else:
        for (px_, py, w, g, cols) in puestos:                                       # puestos derrumbados
            cv.poly([(px_, py + 18), (px_ + w, py + 6), (px_ + w + 4, py + 14), (px_ + 6, py + 22)], K("madera", 3))
            cv.d.line([(px_, py + 18), (px_ + w, py + 6)], fill=K("madera", 4))
            cv.d.line([(px_ + 10, py - 14), (px_ + 24, py + 16)], fill=K("madera", 2))           # un poste caído
            toldo(cv, px_ - 4, py + 2, w // 2, cols, rnd, roto=True)
            fuego(cv, px_ + w // 2, py + 8, rnd)
        P.escombros(cv, 380, 150, 680, 222, n=60, semilla=9, rampa="gris")
        cv.ellipse(CRATER[0] - 34, CRATER[1] - 12, CRATER[0] + 34, CRATER[1] + 12, K("gris", 1))
        cv.ellipse(CRATER[0] - 24, CRATER[1] - 7, CRATER[0] + 24, CRATER[1] + 7, K("gris", 0))
        for _ in range(30):                                                          # la metralla de la lata, esparcida
            mx, my = CRATER[0] + rnd.randint(-70, 60), CRATER[1] + rnd.randint(-20, 30)
            cv.px(mx, my, K("gris", 7)); cv.px(mx + 1, my, K("gris", 5))
        cv.rect(470, 198, 478, 206, K("gris", 5)); cv.hline(470, 478, 198, K("gris", 7))  # la lata volcada
        for _ in range(2500):                                                        # polvo
            cv.px(rnd.randint(0, W - 1), rnd.randint(0, CALLE), K("papel", 1))
    cv.rect(0, CALLE, W, CALLE + 4, K("gris", 3)); cv.hline(0, W, CALLE, K("gris", 6))
    ladrillo(cv, 0, CALLE + 4, W, H, rnd, base=1)
    cv.add_light(0, 0, W, FACHADA, -1)
    cv.bake_lighting()
    if ruinas:
        cv.img = desaturar(cv.img)
    return cv
