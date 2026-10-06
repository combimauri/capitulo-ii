"""J1.05 — El parte de guerra (ParteScene), en la mesa del Departamento de Partes y Cartografía del Minipax.

Escritorio metálico verdoso del Ministerio visto desde arriba: la boca del tubo neumático por la que llega la
directiva, un cenicero con colillas de Victoria, un bote de lápices, la bandeja de partes enviados y el resplandor de
la telepantalla de la sala. El parte: papel `papel 3` con membrete (pirámide, «MINIPAX»), número de serie, filete rojo
y pie de impreso. La directiva es una tira de papel enrollado que sale del tubo (sprite aparte, la escena la anima).

Pantalla → arte: PAPEL (150, 170, 660×320) → (75, 85)-(405, 245). Directiva: contenedor en (40, 30), 380×120.
"""
import random

from PIL import Image
from pixel import Canvas, K
import papel as PP

PX0, PY0, PX1, PY1 = 75, 85, 405, 245


def _tubo(cv, x, y):
    """Boca del tubo neumático 14, empotrada en el tablero: brida de latón, tapa abatida y placa."""
    PP.sombra(cv, x, y, x + 54, y + 38, 2, 3)
    cv.rect(x, y, x + 54, y + 38, K("pared", 1)); cv.frame(x, y, x + 54, y + 38, K("pared", 0))
    cv.hline(x + 1, x + 53, y + 1, K("pared", 3))
    for (a, b) in ((x + 2, y + 2), (x + 50, y + 2), (x + 2, y + 34), (x + 50, y + 34)):
        cv.px(a, b, K("gris", 7)); cv.px(a + 1, b + 1, K("gris", 1))
    cx = x + 27
    cv.ellipse(cx - 17, y + 3, cx + 18, y + 31, K("ocre", 1))
    cv.ellipse(cx - 16, y + 4, cx + 17, y + 30, K("ocre", 2))
    cv.d.arc([cx - 16, y + 4, cx + 17, y + 30], 190, 320, fill=K("ocre", 3))
    cv.ellipse(cx - 12, y + 7, cx + 13, y + 27, K("gris", 0))
    cv.ellipse(cx - 9, y + 10, cx + 10, y + 25, K("gris", 1))
    cv.ellipse(cx - 6, y + 14, cx + 7, y + 23, K("gris", 0))
    # la tapa abatida hacia la derecha
    cv.rect(x + 46, y + 10, x + 53, y + 24, K("ocre", 2)); cv.vline(x + 52, y + 10, y + 24, K("ocre", 0))
    cv.vline(x + 46, y + 10, y + 24, K("ocre", 3))
    cv.rect(x + 16, y + 32, x + 38, y + 38, K("papel", 3)); cv.frame(x + 16, y + 32, x + 38, y + 38, K("gris", 3))
    cv.text(x + 23, y + 33, "14", K("gris", 2))


def _cenicero(cv, x, y):
    """Cenicero de chapa con tres colillas de Victoria y ceniza."""
    PP.sombra_elipse(cv, x, y, x + 30, y + 22, 2, 2)
    cv.ellipse(x, y, x + 30, y + 22, K("gris", 5), outline=K("gris", 2))
    cv.ellipse(x + 3, y + 3, x + 27, y + 19, K("gris", 3))
    cv.d.arc([x + 1, y + 1, x + 29, y + 21], 200, 300, fill=K("gris", 7))
    cv.ellipse(x + 6, y + 6, x + 24, y + 17, K("gris", 6))                     # ceniza
    for (a, b) in ((x + 9, y + 9), (x + 14, y + 12), (x + 18, y + 8)):
        cv.px(a, b, K("gris", 4)); cv.px(a + 1, b, K("gris", 8))
    # colillas
    cv.hline(x + 8, x + 15, y + 8, K("papel", 3)); cv.hline(x + 8, x + 15, y + 9, K("papel", 2)); cv.px(x + 15, y + 8, K("gris", 4))
    cv.d.line([x + 14, y + 15, x + 21, y + 11], fill=K("papel", 3)); cv.px(x + 21, y + 11, K("gris", 3))
    cv.hline(x + 20, x + 32, y + 4, K("papel", 4)); cv.hline(x + 20, x + 32, y + 5, K("papel", 2))   # la apoyada en el borde
    cv.hline(x + 30, x + 32, y + 4, K("ocre", 2)); cv.px(x + 33, y + 4, K("rojo", 4)); cv.px(x + 33, y + 5, K("gris", 6))


def _lapicero(cv, x, y):
    """Bote de lápices visto desde arriba: el círculo del bote y las puntas de los lápices."""
    PP.sombra_elipse(cv, x, y, x + 22, y + 22, 2, 3)
    cv.ellipse(x, y, x + 22, y + 22, K("gris", 3), outline=K("gris", 1))
    cv.ellipse(x + 2, y + 2, x + 20, y + 20, K("gris", 1))
    for (a, b, c) in ((x + 6, y + 6, "ocre"), (x + 12, y + 5, "rojo"), (x + 14, y + 12, "ocre"), (x + 7, y + 13, "azul")):
        cv.rect(a, b, a + 3, b + 3, K(c, 2)); cv.px(a + 1, b + 1, K("madera", 5)); cv.px(a + 1, b + 1, K("gris", 1))
    # un lápiz tumbado y una goma
    cv.d.line([x - 6, y + 40, x + 34, y + 30], fill=K("ocre", 2))
    cv.d.line([x - 6, y + 41, x + 34, y + 31], fill=K("ocre", 1))
    cv.d.line([x + 34, y + 30, x + 38, y + 29], fill=K("madera", 5)); cv.px(x + 39, y + 29, K("gris", 1))
    cv.rect(x - 8, y + 40, x - 4, y + 43, K("rojo", 3))
    PP.sombra(cv, x + 4, y + 52, x + 18, y + 59, 1, 2, 1)
    cv.rect(x + 4, y + 52, x + 18, y + 59, K("granate", 4)); cv.hline(x + 4, x + 18, y + 52, K("granate", 5))
    cv.frame(x + 4, y + 52, x + 18, y + 59, K("granate", 2))


def _papel_carbon(cv, x, y):
    """Hojas de papel carbón (azul oscuro) bajo un taco de copias."""
    PP.sombra(cv, x, y, x + 48, y + 60, 2, 2)
    cv.rect(x, y, x + 48, y + 60, K("azul", 0)); cv.frame(x, y, x + 48, y + 60, K("azul", 1))
    for k in range(6):
        cv.hline(x + 4, x + 40, y + 6 + k * 8, K("azul", 1))
    PP.hoja(cv, x + 6, y + 10, x + 50, y + 72, base=3, semilla=31, muescas=1)
    for k in range(7):
        a = x + 10; b = x + 10 + (34 if k % 3 else 22)
        for xx in range(a, b):
            if (xx + k) % 4:
                cv.px(xx, y + 18 + k * 6, K("azul", 2))


def _bandeja(cv, x, y):
    """Bandeja de rejilla con partes ya enviados (copias en papel cebolla)."""
    PP.sombra(cv, x, y, x + 60, y + 80, 3, 3)
    cv.rect(x, y, x + 60, y + 80, K("gris", 2)); cv.frame(x, y, x + 60, y + 80, K("gris", 1))
    for k in range(3):
        PP.hoja(cv, x + 4 + k, y + 6 - k * 2, x + 56 + k, y + 76 - k * 2, base=4 - (k == 0), semilla=60 + k, muescas=1,
                sombra_mesa=False)
    tx, ty = x + 7, y + 4
    PP.piramide(cv, tx + 2, ty + 4, 5, K("gris", 4))
    cv.hline(tx + 1, tx + 50, ty + 12, K("rojo", 4))
    for k in range(8):
        for xx in range(tx + 2, tx + 2 + (44 if k % 4 != 3 else 26)):
            if (xx * 3 + k) % 5:
                cv.px(xx, ty + 17 + k * 6, K("gris", 6))
    for xx in range(x, x + 61, 6):                                              # la rejilla de alambre del borde
        cv.vline(xx, y + 74, y + 80, K("gris", 5))
    cv.hline(x, x + 60, y + 74, K("gris", 6)); cv.hline(x, x + 60, y + 79, K("gris", 4))
    cv.rect(x + 14, y + 66, x + 46, y + 73, K("papel", 2)); cv.frame(x + 14, y + 66, x + 46, y + 73, K("gris", 3))
    cv.text(x + 16, y + 67, "SALIDA", K("gris", 2))


def dibujar():
    cv = Canvas(480, 270, ("pared", 3))
    PP.chapa(cv, 0, 0, 480, 270, base=3, semilla=8, rampa="pared")
    for x in (0, 160, 320):                                                     # juntas de las planchas del tablero
        cv.vline(x + 159, 0, 270, K("pared", 1))
        cv.vline(x + 160, 0, 270, K("pared", 4))
    cv.hline(0, 480, 266, K("pared", 1)); cv.rect(0, 267, 480, 270, K("pared", 0))   # canto

    _tubo(cv, 226, -6)
    _cenicero(cv, 432, 10)
    _lapicero(cv, 20, 92)
    _papel_carbon(cv, 10, 168)
    _bandeja(cv, 412, 150)
    # cerco de una taza de sucedáneo de café de otra mañana
    import math
    aro = set()
    for a in range(0, 360, 2):
        if not 130 < a < 165:
            aro.add((int(round(330 + math.cos(math.radians(a)) * 10)), int(round(40 + math.sin(math.radians(a)) * 7.5))))
    for (x, y) in aro:
        PP.desplazar(cv, x, y, x + 1, y + 1, -1)

    # --- el parte
    PP.sombra(cv, PX0, PY0, PX1, PY1, 3, 3)
    PP.hoja(cv, PX0, PY0, PX1, PY1, base=3, semilla=21, mordidas=0.04, muescas=2, fibra=0.03, sombra_mesa=False)
    PP.manchas_papel(cv, PX0 + 2, PY0 + 2, PX1 - 2, PY1 - 2, 4, semilla=6, radio=(1, 3))
    # membrete
    PP.piramide(cv, PX0 + 8, PY0 + 7, 9, K("gris", 2))
    PP.texto_c(cv, PX0 + 17, PY0 + 19, "MINIPAX", K("gris", 2))
    cv.text(PX1 - 44, PY0 + 6, "SERIE A", K("papel", 0))
    cv.frame(PX1 - 46, PY0 + 12, PX1 - 8, PY0 + 22, K("papel", 1))
    cv.text(PX1 - 44, PY0 + 15, "N.", K("papel", 0))
    cv.hline(PX0 + 15, PX1 - 15, PY0 + 29, K("rojo", 3))
    cv.hline(PX0 + 15, PX1 - 15, PY0 + 31, K("rojo", 2))
    # pie de impreso y el margen de las grapas
    cv.text(PX0 + 17, PY1 - 7, "DPTO. DE PARTES Y CARTOGRAFIA DEL FRENTE - IMPRESO P-3", K("papel", 1))
    cv.hline(PX0 + 6, PX0 + 13, PY0 + 4, K("gris", 6)); cv.px(PX0 + 6, PY0 + 5, K("gris", 5)); cv.px(PX0 + 12, PY0 + 5, K("gris", 5))

    # la telepantalla de la sala, fuera de cuadro a la derecha
    cv.glow_rgb = K("tele", 4)
    cv.add_glow_suave(520, 130, 230, 0.15, squash=0.8)
    cv.bake_lighting()
    return cv


def directiva():
    """La tira de la directiva, enrollada por haber viajado en la cápsula. 190×60 + 3 px de sombra translúcida."""
    w, h = 190, 60
    cv = Canvas(w + 3, h + 3, ("gris", 0))
    rnd = random.Random(14)
    m = set()
    # bordes izquierdo y derecho rasgados (arrancada del rollo), arriba y abajo rectos pero curvados
    for y in range(h):
        a = rnd.choice([0, 0, 1, 1, 2]); b = w - rnd.choice([0, 0, 1, 2])
        for x in range(a, b):
            m.add((x, y))
    PP.pintar_hoja(cv, m, base=4, semilla=15, fibra=0.025, borde=-2)
    p = cv.img.load()
    for (x, y) in m:                                                            # la curvatura del rollo
        if y in (1, 2) or y in (h - 3, h - 2):
            p[x, y] = K("papel", 3)
        if y == h - 4 and x % 3:
            p[x, y] = K("papel", 3)
    img = cv.img.convert("RGBA")
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sp = sh.load()
    for (x, y) in m:
        sp[x + 3, y + 3] = (11, 12, 15, 110)
    out.alpha_composite(sh)
    ip = img.load()
    op = out.load()
    for (x, y) in m:
        op[x, y] = ip[x, y]
    return out


def exportar(destino):
    dibujar().img.save(destino / "parte-fondo.png")
    directiva().save(destino / "parte-directiva.png")
    return ["parte-fondo.png", "parte-directiva.png"]
