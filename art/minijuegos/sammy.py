"""J5.04 — La contrarreloj de Sammy en el mercado de Watney Street, en el instante del silbido.

La calle del mercado (los mismos puestos, toldos y ladrillo que el escenario) un segundo antes del
cohete: la gente pegada al suelo, una cesta volcada con las patatas rodando, Dot alzando la cabeza
junto a su puesto de retales, las palomas que salen volando. La calzada de abajo queda libre: por
ahí corre el protagonista hacia Sammy, que está agachado en mitad de la calle, de espaldas.

  sammy-fondo  480x270
  sammy-nino   18x20  Sammy agachado de espaldas, recogiendo un trozo de metralla brillante
"""
import random

from _base import Canvas, K, a_rgba, guardar, sprite
import props as P
from limehouse import ladrillo
from mercado import puesto, toldo

W, H = 480, 270
FACHADA, CALLE = 96, 252


def _tumbado(cv, x, y, ropa, pelo):
    """Una persona echada boca abajo, con los brazos sobre la cabeza (vista cenital 3/4)."""
    cv.ellipse(x - 2, y + 4, x + 30, y + 11, K("gris", 1))                  # sombra
    cv.rect(x + 6, y + 1, x + 22, y + 8, K(ropa, 3)); cv.hline(x + 6, x + 22, y + 1, K(ropa, 4))
    cv.rect(x + 22, y + 2, x + 30, y + 7, K(ropa, 1))                       # piernas
    cv.rect(x + 29, y + 2, x + 31, y + 4, K("madera", 0)); cv.rect(x + 29, y + 5, x + 31, y + 7, K("madera", 0))
    cv.ellipse(x, y, x + 7, y + 7, K(*pelo))                                 # cabeza
    cv.rect(x - 4, y + 1, x + 2, y + 3, K(ropa, 2)); cv.rect(x - 4, y + 4, x + 2, y + 6, K(ropa, 2))  # brazos
    cv.px(x - 5, y + 2, K("piel", 2)); cv.px(x - 5, y + 5, K("piel", 2))


def _paloma(cv, x, y):
    cv.px(x, y, K("gris", 2)); cv.px(x - 1, y - 1, K("gris", 2)); cv.px(x + 1, y - 1, K("gris", 2))
    cv.px(x - 2, y - 1, K("gris", 3)); cv.px(x + 2, y - 1, K("gris", 3))


def fondo():
    rnd = random.Random(1905)
    cv = Canvas(W, H)
    # cielo de madrugada, con humo lejano
    for i, y in enumerate(range(0, 40, 8)):
        cv.rect(0, y, W, y + 8, K("cielo", 4 + i // 2))
    # humo de un incendio lejano: bocanadas que se abren y se tuercen con el viento
    for (cx, cy, r) in ((356, 30, 4), (358, 24, 5), (362, 17, 6), (368, 10, 7), (377, 4, 8), (388, -1, 9)):
        cv.ellipse(cx - r - 2, cy - r + 2, cx + r - 1, cy + r - 1, K("cielo", 3))
        cv.ellipse(cx - r + 1, cy - r, cx + r + 2, cy + r - 2, K("cielo", 3))
        cv.ellipse(cx - r + 2, cy - r + 1, cx + r - 2, cy, K("cielo", 4))
    # fachadas
    x = -20
    while x < W:
        w = rnd.randint(70, 100)
        top = rnd.randint(14, 28)
        ladrillo(cv, x, top, x + w, FACHADA, rnd, base=rnd.choice([1, 2]))
        cv.rect(x, top - 3, x + w, top, K("gris", 2)); cv.hline(x, x + w, top - 3, K("gris", 4))
        for wx in range(x + 10, x + w - 14, 24):
            cv.rect(wx, top + 12, wx + 12, top + 28, K("gris", 1)); cv.vline(wx + 6, top + 12, top + 28, K("madera", 1))
            cv.hline(wx - 1, wx + 13, top + 29, K("gris", 5))
            if rnd.random() < 0.3:                                             # una ventana rota
                cv.poly([(wx + 1, top + 13), (wx + 6, top + 13), (wx + 2, top + 19)], K("cielo", 2))
        x += w
    # ropa tendida entre dos ventanas
    cv.d.line([(60, 44), (190, 52)], fill=K("gris", 4))
    for k, (cx, col) in enumerate(((78, K("papel", 3)), (104, K("granate", 4)), (128, K("tela", 4)), (160, K("papel", 2)))):
        cy = 45 + (cx - 60) * 8 // 130
        cv.rect(cx, cy, cx + 12, cy + 12 + (k % 2) * 4, col); cv.hline(cx, cx + 12, cy, K("gris", 3))
    # adoquines
    P.adoquines(cv, 0, FACHADA, W, CALLE, semilla=12)
    cv.rect(0, FACHADA, W, FACHADA + 3, K("gris", 2))
    # puestos del fondo
    puesto(cv, 20, 128, 64, [K("tele", 3), K("papel", 3)], "patatas", rnd)
    puesto(cv, 150, 128, 76, [K("granate", 4), K("ocre", 3)], "retales", rnd)        # el de Dot
    puesto(cv, 300, 128, 60, [K("cielo", 4), K("papel", 3)], "cordones", rnd)
    puesto(cv, 410, 128, 64, [K("rojo", 3), K("papel", 3)], "cacharros", rnd)
    # gente pegada al suelo
    _tumbado(cv, 36, 172, "tela", ("pelo", 1))
    _tumbado(cv, 114, 186, "granate", ("pelo", 0))
    _tumbado(cv, 252, 170, "madera", ("papel", 1))
    _tumbado(cv, 350, 182, "tela", ("ocre", 2))
    # Dot, de rodillas junto a su puesto, alzando la cabeza (pañuelo rojo con lunares)
    dx, dy = 206, 156
    cv.ellipse(dx - 4, dy + 22, dx + 18, dy + 28, K("gris", 1))
    cv.rect(dx, dy + 10, dx + 14, dy + 24, K("granate", 4)); cv.hline(dx, dx + 14, dy + 10, K("granate", 5))
    cv.rect(dx + 2, dy + 14, dx + 12, dy + 23, K("papel", 3))                    # delantal
    cv.rect(dx + 2, dy, dx + 12, dy + 10, K("piel", 3)); cv.rect(dx + 2, dy + 7, dx + 12, dy + 10, K("piel", 2))
    cv.rect(dx + 1, dy - 2, dx + 13, dy + 4, K("rojo", 3))
    for (lx, ly) in ((dx + 3, dy), (dx + 8, dy - 1), (dx + 11, dy + 2)):
        cv.px(lx, ly, K("papel", 4))
    cv.px(dx + 5, dy + 5, K("pelo", 0)); cv.px(dx + 9, dy + 5, K("pelo", 0))
    cv.rect(dx + 14, dy + 8, dx + 20, dy + 11, K("granate", 4)); cv.rect(dx + 19, dy + 7, dx + 22, dy + 10, K("piel", 3))   # brazo tendido
    # cesta volcada y patatas rodando por la calzada
    cv.ellipse(150, 196, 172, 210, K("madera", 2)); cv.ellipse(152, 198, 166, 206, K("madera", 0))
    for (px_, py_) in ((176, 204), (184, 210), (196, 207), (210, 214), (232, 211)):
        cv.ellipse(px_, py_, px_ + 5, py_ + 4, K("ocre", 1)); cv.px(px_ + 1, py_ + 1, K("ocre", 2))
    # la lata de Sammy, en el bordillo, con su colección de metralla
    cv.rect(452, 200, 460, 210, K("gris", 5)); cv.hline(452, 460, 200, K("gris", 7))
    for k in range(5):
        cv.px(440 + k * 3, 214, K("gris", 7)); cv.px(441 + k * 3, 214, K("gris", 5))
    # palomas que levantan el vuelo
    for (px_, py_) in ((120, 30), (128, 24), (136, 33), (300, 18), (309, 12), (392, 40)):
        _paloma(cv, px_, py_)
    # bordillo y acera
    cv.rect(0, CALLE, W, CALLE + 4, K("gris", 3)); cv.hline(0, W, CALLE, K("gris", 6))
    ladrillo(cv, 0, CALLE + 4, W, H, rnd, base=1)
    cv.add_light(0, 0, W, FACHADA, -1)
    cv.bake_lighting()
    return cv.img


NINO = [
    "......cccccc......",
    ".....cCCCCcccc....",
    ".....cCCcccccccc..",
    ".....cbbbbbbbbbbbb",
    "......hhhhhhhhs...",
    "......hhhhhhhss...",
    ".......shhhhs.....",
    "....dOOOOOooood...",
    "...dOOOOOoooooodd.",
    "...dOOOOooooooddss",
    "...dOOOoooooodd.ss",
    "...dooooooooddd.s.",
    "....ppppppppPP..s.",
    "...ppppppppppPP.sM",
    "..lppppppppppPPP.m",
    "..lllpppppppPPll..",
    "..lll.......lll...",
    "..kkk......kkkk...",
    ".kkkk......kkkkk..",
    "..................",
]


def nino():
    cv = sprite(18, 20)
    cv.ellipse(1, 16, 18, 20, K("gris", 1))                                     # sombra en el suelo
    pal = {"c": K("tela", 2), "C": K("tela", 3), "b": K("tela", 1), "h": K("pelo", 1), "s": K("piel", 2),
           "O": K("ocre", 3), "o": K("ocre", 2), "d": K("ocre", 1), "p": K("madera", 2), "P": K("madera", 1),
           "l": K("piel", 2), "k": K("madera", 0), "m": K("gris", 7), "M": K("gris", 10)}
    cv.grid(0, 0, NINO, pal)
    return a_rgba(cv)


def exportar(destino):
    return [guardar(fondo(), destino, "sammy-fondo"), guardar(nino(), destino, "sammy-nino")]
