"""FE.02 — Los años: viñetas fijas en la cripta de San Clemente, con un rótulo de año y la luz de las velas.

dibujar("1985") · "1987" · "1988" · "1990" · "1993"  (sin variante: 1985)

Las figuras son del tamaño del juego (20x40) y se pintan antes de hornear la luz, así que las velas las alumbran
igual que al resto de la cripta. El protagonista lleva el mono azul y un pelo a la altura de la mandíbula que no
fija su género (sirve para la versión H y para la M).
"""
from pixel import K
import _luz as L
import cripta as C
import elenco as E
import npcs as N
from protagonista import LADO_DER, FRENTE

# ---------------------------------------------------------------- piezas


def _ancho(filas, w):
    return [f.ljust(w, ".")[:w] for f in filas]


def _espejo(filas):
    return [f[::-1] for f in filas]


def _poner(filas, cambios):
    f = [list(r) for r in filas]
    for (r, c, ch) in cambios:
        if 0 <= r < len(f) and 0 <= c < len(f[r]):
            f[r][c] = ch
    return ["".join(r) for r in f]


def _cabeza_lado(media_melena=True):
    """Cabeza de perfil (mirando a la derecha) con el pelo a la altura de la mandíbula."""
    cab = list(LADO_DER[:18])
    if media_melena:
        cambios = []
        for r in (11, 12, 13, 14):
            cambios += [(r, 4, "o")] + [(r, c, "h") for c in (5, 6, 7)]
        cambios += [(15, 4, "o"), (15, 5, "h"), (15, 6, "h"), (15, 7, "h"), (16, 5, "o"), (16, 6, "h"), (16, 7, "h")]
        cab = _poner(cab, cambios)
    return cab


def _cabeza_frente(media_melena=True):
    cab = list(FRENTE[:18])
    if media_melena:
        cambios = []
        for r in range(7, 14):
            for (co, ch) in ((2, 3), (17, 16)):
                cambios += [(r, co, "o"), (r, ch, "h")]
        cambios += [(14, 3, "o"), (14, 16, "o"), (14, 4, "h"), (14, 15, "h")]
        cab = _poner(cab, cambios)
    return cab


def _cabeza_goldstein_lado():
    """Goldstein de perfil: pelo blanco revuelto y largo por detrás, gafas y perilla."""
    cab = _cabeza_lado(media_melena=True)
    cambios = [(0, 6, "o"), (0, 13, "o"), (1, 4, "o"), (2, 3, "o"), (3, 3, "h"), (1, 15, "o")]   # mechones sueltos
    cambios += [(r, 3, "o") for r in range(4, 16)] + [(r, 4, "h") for r in range(4, 16)]
    cambios += [(8, 12, "g"), (8, 13, "g"), (8, 14, "g"), (9, 12, "g"), (9, 13, "G"), (9, 14, "g"),
                (10, 12, "g"), (10, 13, "g"), (10, 14, "g"), (9, 9, "g"), (9, 10, "g"), (9, 11, "g")]
    cambios += [(14, c, "y") for c in range(11, 16)] + [(15, c, "y") for c in range(11, 15)] + [(16, 12, "y"), (16, 13, "y")]
    cambios += [(13, 13, "y"), (13, 15, "y")]                                       # bigote
    return _poner(cab, cambios)


# cuerpo sentado de perfil, mirando a la derecha, con los brazos hacia delante (22 de ancho)
SENTADO = [
    "......ndbbbLn.........",
    ".....ndbbbbbLn........",
    ".....ndbbbbbbLn.......",
    ".....ndbbbbbbbn.......",
    ".....ndbnnBbbbn.......",
    ".....ndbnbBnnnnnn.....",
    ".....ndbnbbBBBBBBnn...",
    ".....ndbbnnnnnnnnssn..",
    ".....ndbbbbbbbn..nn...",
    ".....nddddddddnnnn....",
    ".....ndbbbbbbbbbbbn...",
    ".....nnnnnnnnndbbbn...",
    ".............ndbbn....",
    ".............ndbbn....",
    ".............ndbbn....",
    ".............ndbbn....",
    ".............nwWwwn...",
    ".............nnnnnn...",
]
MANO_SENTADO = (25, 18)                     # fila y columna de la mano

# de pie, de perfil, con el brazo extendido (ofreciendo algo)
_DE_PIE = [r.ljust(22, ".") for r in LADO_DER[18:]]
DE_PIE_BRAZO = _poner(_DE_PIE, [(9, 9, "b"), (9, 10, "b"), (9, 11, "b"), (10, 9, "b"), (10, 10, "b"), (10, 11, "b")]
                      + [(5, c, "n") for c in range(12, 18)] + [(6, c, "B") for c in range(12, 18)]
                      + [(7, c, "n") for c in range(12, 18)] + [(6, 18, "s"), (6, 19, "s"), (7, 18, "S"), (7, 19, "S"),
                                                                 (5, 18, "n"), (5, 19, "n"), (6, 20, "n"), (7, 20, "n")])
MANO_DE_PIE = (24, 19)


def _pal_prota(edad=0):
    pelo = [("pelo", 0, 1, 3), ("gris", 3, 5, 7), ("gris", 5, 7, 9)][edad]
    return {"o": K(pelo[0], pelo[1]), "h": K(pelo[0], pelo[2]), "H": K(pelo[0], pelo[3]),
            "O": K("piel", 1), "S": K("piel", 2), "s": K("piel", 3), "l": K("piel", 4), "e": K("gris", 1), "m": K("piel", 1),
            "n": K("azul", 0), "d": K("azul", 1), "b": K("azul", 2), "B": K("azul", 3), "L": K("azul", 4),
            "w": K("gris", 2), "W": K("gris", 4), "g": K("gris", 3), "G": K("cielo", 6)}


PAL_GOLDSTEIN = {"o": K("papel", 1), "h": K("papel", 3), "H": K("papel", 4),
                 "O": K("piel", 2), "S": K("piel", 3), "s": K("piel", 4), "l": K("piel", 4), "e": K("gris", 1), "m": K("piel", 2),
                 "n": K("granate", 0), "d": K("granate", 1), "b": K("granate", 3), "B": K("granate", 4), "L": K("granate", 4),
                 "w": K("madera", 1), "W": K("madera", 3), "g": K("gris", 4), "G": K("cielo", 6), "y": K("papel", 4)}


def sentado(cv, x, y, cabeza, pal, mirando="derecha"):
    filas = _ancho(cabeza, 22) + SENTADO
    if mirando == "izquierda":
        filas = _espejo(filas)
    cv.grid(x, y, filas, pal)


def de_pie(cv, x, y, cabeza, pal, mirando="derecha", brazo=False, sombra=True):
    cuerpo = DE_PIE_BRAZO if brazo else _DE_PIE
    filas = _ancho(cabeza, 22) + cuerpo
    if mirando == "izquierda":
        filas = _espejo(filas)
    if sombra:
        cv.ellipse(x + 3, y + 36, x + 19, y + 43, K("madera", 0))
    cv.grid(x, y, filas, pal)


def taza(cv, x, y, humo=False):
    cv.rect(x, y, x + 4, y + 4, K("papel", 3)); cv.hline(x, x + 4, y, K("papel", 4))
    cv.px(x + 1, y + 1, K("madera", 2)); cv.px(x + 2, y + 1, K("madera", 2))
    cv.px(x + 4, y + 1, K("papel", 2)); cv.px(x + 4, y + 2, K("papel", 2))


def taburete(cv, sx, sy):
    cv.ellipse(sx + 2, sy + 12, sx + 18, sy + 17, K("madera", 0))
    for lx in (sx + 2, sx + 12):
        cv.rect(lx, sy + 4, lx + 2, sy + 14, K("madera", 1))
    cv.ellipse(sx, sy, sx + 16, sy + 7, K("madera", 4), outline=K("madera", 2))


CIFRAS = {"1": "010110010010111", "9": "111101111001111", "8": "111101111101111", "5": "111100111001111",
          "7": "111001010010010", "3": "111001111001111", "0": "111101101101111"}


def _cifras(cv, x, y, s, col, escala=3):
    for ch in s:
        for i, b in enumerate(CIFRAS[ch]):
            if b == "1":
                cv.rect(x + (i % 3) * escala, y + (i // 3) * escala, x + (i % 3 + 1) * escala, y + (i // 3 + 1) * escala, col)
        x += 4 * escala


def rotulo(cv, anio):
    """El año, en blanco roto, abajo a la derecha (sobre el muro de la cripta)."""
    ancho = len(anio) * 12 - 3
    x, y = C.W - 16 - ancho, C.H - 21
    _cifras(cv, x + 1, y + 1, anio, K("gris", 0))
    _cifras(cv, x, y, anio, K("papel", 4))


# ---------------------------------------------------------------- viñetas


def _1985(cv):
    x0, y0, x1, y1 = C.MESA
    t0 = y0 - C.ALTO_MESA
    # el protagonista, en el taburete de la izquierda, escribiendo a mano sobre el montón de papel
    sentado(cv, x0 - 27, y0 - 26, _cabeza_lado(), _pal_prota(0), "derecha")
    cv.d.line([(x0 - 7, y0 - 2), (x0 - 4, y0 - 6)], fill=K("gris", 1))             # lápiz
    # Goldstein, enfrente, con la manta sobre los hombros
    sentado(cv, x1 + 5, y0 - 26, _cabeza_goldstein_lado(), PAL_GOLDSTEIN, "izquierda")
    for (r, a, b) in ((18, 12, 19), (19, 11, 20), (20, 10, 21), (21, 10, 21), (22, 11, 20)):   # la manta
        cv.hline(x1 + 5 + a - 4, x1 + 5 + b - 4, y0 - 26 + r, K("tela", 3) if r % 2 else K("tela", 2))
    cv.hline(x1 + 5 + 6, x1 + 5 + 17, y0 - 26 + 23, K("tela", 1))
    # Brooke, en la escalera, con un cesto y un fajo de copias atado con cordel
    filas, pal = N.NPCS["brooke"]
    pal = {**pal, "n": K("tela", 0), "d": K("tela", 1), "b": K("tela", 2), "B": K("tela", 3), "L": K("tela", 4)}
    bx, by = 55, 34
    cv.grid(bx, by, filas, pal)
    cv.rect(bx + 15, by + 26, bx + 27, by + 33, K("madera", 3)); cv.frame(bx + 15, by + 26, bx + 27, by + 33, K("madera", 1))
    for k in range(bx + 16, bx + 27, 2):
        cv.vline(k, by + 27, by + 33, K("madera", 2))                              # mimbre
    cv.d.arc([bx + 16, by + 20, bx + 26, by + 31], 180, 360, fill=K("madera", 2))  # asa
    cv.rect(bx + 17, by + 24, bx + 21, by + 27, K("papel", 3)); cv.px(bx + 23, by + 25, K("ocre", 2))   # pan y una manzana
    cv.rect(bx - 6, by + 22, bx + 4, by + 30, K("papel", 3)); cv.hline(bx - 6, bx + 4, by + 22, K("papel", 4))
    cv.vline(bx - 1, by + 22, by + 30, K("madera", 2)); cv.hline(bx - 6, bx + 4, by + 26, K("madera", 2))   # cordel


def _1987(cv):
    x0, y0, x1, y1 = C.CAMASTRO
    t0 = y0 - 6
    # Goldstein, acostado, la cabeza en la almohada y la manta hasta el pecho
    filas, _ = next((f, p) for n, f, p in E.ELENCO if n == "GOLDSTEIN")
    cabeza = filas[:18]
    pal = {**PAL_GOLDSTEIN, "o": K("papel", 1), "h": K("papel", 3), "H": K("papel", 4)}
    cv.grid(x0 + 1, t0 - 10, cabeza, pal)
    cv.rect(x0 + 4, t0 + 8, x0 + 18, t0 + 14, K("granate", 3))                     # el embozo
    cv.hline(x0 + 4, x0 + 18, t0 + 8, K("granate", 4))
    cv.rect(x0 + 15, t0 + 6, x0 + 19, t0 + 9, K("piel", 3))                        # la mano en la boca: tose
    for (dx, dy) in ((20, -2), (22, -4), (21, -6)):
        cv.px(x0 + dx, t0 + dy, K("papel", 3))
    # el protagonista, en un taburete junto al camastro, le acerca la taza
    taburete(cv, x0 - 26, y0 + 6)
    sentado(cv, x0 - 31, y0 - 22, _cabeza_lado(), _pal_prota(0), "derecha")
    mx, my = x0 - 31 + MANO_SENTADO[1], y0 - 22 + MANO_SENTADO[0]
    taza(cv, mx, my - 4)


def _1988(cv):
    x0, y0, x1, y1 = C.LOSA_NUEVA
    # las gafas remendadas con hilo, sobre la losa sin nombre
    gx, gy = (x0 + x1) // 2 - 6, (y0 + y1) // 2 - 2
    for ox in (0, 7):
        cv.ellipse(gx + ox, gy, gx + ox + 5, gy + 5, K("cielo", 5), outline=K("gris", 3))
        cv.px(gx + ox + 1, gy + 1, K("cielo", 6))
    cv.hline(gx + 5, gx + 7, gy + 2, K("gris", 3))                                 # puente
    cv.px(gx + 5, gy + 1, K("papel", 4)); cv.px(gx + 6, gy + 1, K("papel", 4)); cv.px(gx + 6, gy + 3, K("papel", 4))   # el hilo
    cv.d.line([(gx, gy + 2), (gx - 3, gy + 5)], fill=K("gris", 3)); cv.d.line([(gx + 12, gy + 2), (gx + 15, gy + 5)], fill=K("gris", 3))
    C.vela(cv, x1 - 4, y1 - 2, alto=6, grosor=2)
    # el protagonista, de pie al lado, mirando la losa
    cab = _cabeza_lado()
    cab = ["." * 20] + cab[:-1]                                                    # la cabeza un poco gacha
    de_pie(cv, x0 - 24, y1 - 38, cab, _pal_prota(0), "derecha")


def _1990(cv):
    pass                                                                           # todo pasa detrás de la mesa


def _1990_detras(cv):
    x0, y0, x1, y1 = C.MESA
    t0 = y0 - C.ALTO_MESA
    cab = _cabeza_frente()
    cuerpo = [r for r in FRENTE[18:30]]
    filas = cab + cuerpo
    filas = _poner(filas, [(r, c, "s") for r in (28, 29) for c in (7, 8, 11, 12)])  # las manos, juntas sobre las teclas
    cx = x0 + 28 + 12 - 10
    cv.grid(cx, t0 - 26, filas, _pal_prota(1))


def _1993(cv):
    # la muchacha, al pie de la escalera: pañuelo y mirada dura
    filas = E.construir("panuelo", "abrigo", [(8, c, "o") for c in (5, 6, 7, 12, 13, 14)] + [(9, c, "o") for c in (8, 11)]
                        + [(14, c, "m") for c in range(8, 12)])
    pal = {**E.PIEL(0), "o": K("pelo", 0), "e": K("gris", 0), "m": K("piel", 1),
           "k": K("tela", 0), "K": K("tela", 3), "j": K("tela", 2),
           "n": K("madera", 0), "d": K("madera", 1), "b": K("madera", 2), "B": K("madera", 3), "L": K("madera", 2),
           "g": K("piel", 3), "p": K("tela", 1), **E.BOTAS}
    gx, gy = 70, 68
    cv.ellipse(gx + 3, gy + 36, gx + 18, gy + 43, K("madera", 0))
    cv.grid(gx, gy, filas, pal)
    # el protagonista, viejo, le ofrece una taza (el té ya está frío)
    px_, py_ = 100, 70
    de_pie(cv, px_, py_, _cabeza_lado(), _pal_prota(2), "izquierda", brazo=True)
    taza(cv, px_ + 22 - MANO_DE_PIE[1] - 4, py_ + MANO_DE_PIE[0] - 4)


VINETAS = {"1985": (_1985, None, None), "1987": (_1987, None, None), "1988": (_1988, None, "losa_nueva"),
           "1990": (_1990, _1990_detras, None), "1993": (_1993, None, None)}


def dibujar(variante=None):
    anio = variante or "1985"
    extras, detras, var = VINETAS[anio]
    cv = C.dibujar(var, extras=extras, detras=detras)
    rotulo(cv, anio)
    return cv
