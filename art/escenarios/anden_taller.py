"""J13.02, tramo 2 — Andén de una estación tapiada: el taller de telepantallas y la pared de los nombres.

Azulejo crema renegrido, el nombre de la estación tapado con ladrillo (solo asoma el anillo rojo), una docena de
telepantallas desmontadas con sus etiquetas, la mesa de Barlow con el mono del Servicio Técnico encima, velas
consumidas y, al fondo a la derecha, un panel pintado de negro lleno de nombres a tiza. Uno dice «Ivy».
Luz tenue y uniforme: el juego oscurece la escena y la alumbra con la linterna.
"""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
TECHO, MURO, BORDE, FOSO = 14, 92, 200, 246
PANTALLAS = (60, 92, 200, 110)            # huella de la pila de telepantallas
MESA = (300, 110, 380, 140)               # huella de la mesa de trabajo
NOMBRES = (390, 30, 466, 90)              # la pared de los nombres
ENTRADA = (0, 110, 20, 190)
VELAS = [(36, 126), (228, 104), (250, 160), (292, 182), (402, 118), (430, 172), (150, 176), (96, 150)]


# ---------------------------------------------------------------- pared


def _azulejo(cv, rnd):
    """Azulejo biselado crema, renegrido por el humo; una cenefa ocre y un zócalo oscuro."""
    cv.rect(0, TECHO, W, MURO, K("papel", 0))
    for y in range(TECHO, MURO, 5):
        off = (y // 5 % 2) * 5
        for x in range(-off, W, 10):
            b = 1 if rnd.random() < 0.82 else rnd.choice([0, 2])
            cv.rect(max(0, x + 1), y + 1, min(W, x + 10), y + 5, K("papel", b))
            cv.hline(max(0, x + 1), min(W, x + 10), y + 1, K("papel", min(4, b + 1)))
    # cenefa y zócalo
    cv.rect(0, 26, W, 30, K("ocre", 1)); cv.hline(0, W, 26, K("ocre", 2)); cv.hline(0, W, 29, K("ocre", 0))
    cv.rect(0, 80, W, MURO, K("granate", 1))
    for x in range(0, W, 10):
        cv.vline(x, 80, MURO, K("granate", 0))
    cv.hline(0, W, 80, K("granate", 3))
    # hollín de las velas y de los años: manchas verticales desde el techo
    for _ in range(60):
        sx = rnd.randint(0, W - 3)
        largo = rnd.randint(6, 30)
        for k in range(largo):
            if rnd.random() < 0.7:
                cv.px(sx + rnd.choice([0, 0, 1]), TECHO + k, K("papel", 0) if k > largo // 2 else K("gris", 3))
    # azulejos caídos
    for _ in range(14):
        x, y = rnd.randint(10, W - 20), rnd.randint(32, 76)
        if NOMBRES[0] - 4 < x < NOMBRES[2] + 4:
            continue
        cv.rect(x, y, x + 9, y + 4, K("gris", 2)); cv.hline(x, x + 9, y, K("gris", 1))


def _techo(cv):
    cv.rect(0, 0, W, TECHO, K("gris", 1))
    for x in range(0, W, 24):                                                      # nervios de la bóveda
        cv.vline(x, 0, TECHO, K("gris", 0))
    cv.hline(0, W, TECHO - 2, K("gris", 2)); cv.hline(0, W, TECHO - 1, K("gris", 0))
    # cables viejos colgando
    cv.d.line([(0, 9), (60, 12), (120, 9), (180, 12), (240, 9), (300, 12), (360, 9), (420, 12), (480, 9)], fill=K("gris", 0))


def _rotulo_tapado(cv, rnd):
    """El rótulo de la estación: anillo rojo con barra. La barra (el nombre) está tapiada con ladrillo."""
    cx, cy, r = 256, 52, 18
    cv.ellipse(cx - r + 2, cy - r + 2, cx + r + 2, cy + r + 2, K("papel", 0))      # sombra
    cv.ellipse(cx - r, cy - r, cx + r, cy + r, K("rojo", 2))
    cv.ellipse(cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5, K("papel", 1))
    cv.d.arc([cx - r, cy - r, cx + r - 1, cy + r - 1], 200, 300, fill=K("rojo", 3))
    # ladrillos sobre la barra, mal enrasados, con el mortero rebosando
    bx0, bx1, by0, by1 = cx - r - 8, cx + r + 8, cy - 7, cy + 7
    cv.rect(bx0 - 1, by0 - 1, bx1 + 1, by1 + 1, K("gris", 4))
    for fila, y in enumerate(range(by0, by1, 4)):
        for x in range(bx0 - (fila % 2) * 4, bx1, 8):
            b = rnd.choice([2, 2, 3])
            cv.rect(max(bx0, x + 1), y + 1, min(bx1, x + 8), min(by1, y + 4), K("granate", b))
            cv.hline(max(bx0, x + 1), min(bx1, x + 8), y + 1, K("granate", b + 1))
    for _ in range(10):
        cv.px(rnd.randint(bx0, bx1 - 1), rnd.choice([by0 - 2, by1 + 1]), K("gris", 5))
    cv.px(bx0 + 2, by1 + 2, K("gris", 4)); cv.px(bx1 - 6, by1 + 2, K("gris", 4)); cv.px(bx1 - 6, by1 + 3, K("gris", 4))
    # asoma la última letra
    cv.rect(bx1 + 1, by0 + 2, bx1 + 4, by1 - 2, K("azul", 2)); cv.px(bx1 + 2, by0 + 5, K("papel", 3))


def _reloj(cv):
    """Reloj de andén parado (nadie sabe a qué hora)."""
    cx, cy = 334, 46
    cv.vline(cx, TECHO, cy - 9, K("gris", 1))
    cv.ellipse(cx - 9, cy - 9 + 2, cx + 11, cy + 11 + 2, K("papel", 0))
    cv.ellipse(cx - 10, cy - 10, cx + 10, cy + 10, K("gris", 1))
    cv.ellipse(cx - 8, cy - 8, cx + 8, cy + 8, K("papel", 2))
    for (dx, dy) in ((0, -6), (6, 0), (0, 6), (-6, 0)):
        cv.px(cx + dx, cy + dy, K("gris", 1))
    cv.d.line([(cx, cy), (cx - 3, cy - 4)], fill=K("gris", 0)); cv.d.line([(cx, cy), (cx + 5, cy + 1)], fill=K("gris", 0))
    cv.d.line([(cx - 6, cy - 3), (cx + 4, cy + 6)], fill=K("papel", 0))           # cristal rajado


# ---------------------------------------------------------------- telepantallas


def _telepantalla_suelta(cv, x, y, w, h, rnd, de_espaldas=False, etiqueta=True, rota=False):
    """Telepantalla desmontada vista en 3/4: tapa superior, frente y pantalla muerta (o la trasera abierta)."""
    cv.rect(x + 2, y + h, x + w + 3, y + h + 3, K("gris", 0))                      # sombra
    cv.rect(x, y - 4, x + w, y, K("gris", 4)); cv.hline(x, x + w, y - 4, K("gris", 5))   # tapa superior
    cv.rect(x, y, x + w, y + h, K("gris", 2)); cv.frame(x, y, x + w, y + h, K("gris", 1))
    cv.vline(x + w - 1, y - 4, y + h, K("gris", 1))
    if de_espaldas:
        cv.rect(x + 3, y + 3, x + w - 3, y + h - 3, K("gris", 0))
        for k in range(3):                                                         # válvulas
            vx = x + 5 + k * ((w - 10) // 3)
            cv.rect(vx, y + 6, vx + 3, y + 12, K("cielo", 2)); cv.px(vx + 1, y + 7, K("cielo", 4))
            cv.rect(vx, y + 12, vx + 3, y + 14, K("gris", 3))
        cv.rect(x + 4, y + h - 8, x + w - 4, y + h - 4, K("ocre", 0))
        for k in range(x + 5, x + w - 5, 3):
            cv.px(k, y + h - 6, K("ocre", 2))
    else:
        sx0, sy0, sx1, sy1 = x + 3, y + 3, x + w - 3, y + h - 5
        cv.rect(sx0, sy0, sx1, sy1, K("tele", 0))
        cv.hline(sx0, sx1 - 2, sy0 + 1, K("tele", 1)); cv.px(sx0 + 1, sy0 + 2, K("tele", 2))   # reflejo
        if rota:
            cv.d.line([(sx0 + 3, sy0), (sx0 + 8, sy1 - 1)], fill=K("gris", 4))
            cv.d.line([(sx0 + 8, sy0 + 5), (sx1 - 2, sy0 + 2)], fill=K("gris", 4))
        cv.hline(x + 2, x + w - 2, y + h - 3, K("gris", 1))
        cv.px(x + w - 4, y + h - 3, K("rojo", 1))                                  # el piloto, apagado
    # cables al aire
    for k in range(rnd.randint(1, 2)):
        cx = x + rnd.randint(3, w - 4)
        pts = [(cx, y + h), (cx + rnd.randint(-4, 4), y + h + 3), (cx + rnd.randint(-6, 6), y + h + rnd.randint(5, 9))]
        cv.d.line(pts, fill=K("gris", 0))
        cv.px(*pts[-1], K("ocre", 3))                                                  # el cobre pelado
    if etiqueta:
        ex, ey = x + rnd.randint(2, w - 12), y - 3
        cv.d.line([(ex + 4, ey), (ex + 5, ey + 4)], fill=K("papel", 1))             # cordel
        cv.rect(ex, ey + 4, ex + 10, ey + 10, K("papel", 3)); cv.frame(ex, ey + 4, ex + 10, ey + 10, K("papel", 1))
        cv.hline(ex + 2, ex + 8, ey + 6, K("gris", 3)); cv.hline(ex + 2, ex + 6, ey + 8, K("gris", 3))


def _pila_telepantallas(cv, rnd):
    x0, y0, x1, y1 = PANTALLAS
    # de atrás (arriba) hacia delante: tres hileras contra la pared, la de abajo más adelantada
    fila_alta = [(66, 40, 30, 20, False), (100, 38, 32, 22, True), (136, 42, 28, 18, False), (168, 40, 28, 20, False)]
    fila_media = [(62, 62, 32, 22, False), (98, 64, 30, 20, False), (132, 62, 34, 22, True), (170, 64, 28, 20, False)]
    fila_baja = [(60, 84, 34, 22, False), (96, 86, 34, 20, True), (134, 84, 32, 22, False), (168, 86, 30, 20, False)]
    for i, (x, y, w, h, espalda) in enumerate(fila_alta + fila_media + fila_baja):
        x += rnd.randint(-2, 2); y += rnd.randint(-1, 1)
        _telepantalla_suelta(cv, x, y, w, h, rnd, de_espaldas=espalda, etiqueta=(i % 3 != 1), rota=(i in (2, 9)))
    # una pantalla de pie, de lado, apoyada en la pila
    cv.poly([(190, 106), (200, 104), (200, 80), (192, 82)], K("gris", 3))
    cv.d.line([(190, 106), (192, 82)], fill=K("gris", 5))
    # un rollo de cable en el suelo delante
    cv.ellipse(150, 104, 166, 112, K("gris", 0), outline=K("gris", 2))
    cv.ellipse(153, 106, 163, 110, None, outline=K("gris", 1))


# ---------------------------------------------------------------- mesa


def _mesa(cv, rnd):
    x0, y0, x1, y1 = MESA
    top0, top1 = y0 - 12, y1 - 12                                                  # tablero elevado sobre su huella
    cv.rect(x0 + 4, y1 - 2, x1 + 5, y1 + 3, K("gris", 0))                          # sombra
    for lx in (x0 + 2, x1 - 6, x0 + 2, x1 - 6):                                    # patas (caballetes)
        cv.rect(lx, top1, lx + 4, y1, K("madera", 1)); cv.vline(lx, top1, y1, K("madera", 2))
    cv.d.line([(x0 + 4, top1 + 2), (x0 + 12, y1 - 1)], fill=K("madera", 1)); cv.d.line([(x1 - 4, top1 + 2), (x1 - 12, y1 - 1)], fill=K("madera", 1))
    cv.rect(x0, top0, x1, top1, K("madera", 3))                                    # tablero: una puerta vieja sobre caballetes
    cv.frame(x0, top0, x1, top1, K("madera", 1)); cv.hline(x0 + 1, x1 - 1, top0 + 1, K("madera", 4))
    for k in (top0 + 9, top0 + 18):
        cv.hline(x0 + 1, x1 - 1, k, K("madera", 2))
    cv.px(x1 - 6, top0 + 14, K("ocre", 2))                                         # el pomo de la puerta que fue
    cv.rect(x0, top1, x1, top1 + 5, K("madera", 2)); cv.hline(x0, x1, top1 + 4, K("madera", 0))
    # el mono del Servicio Técnico, extendido, con su distintivo
    mx, my = x0 + 6, top0 + 3
    cv.rect(mx + 4, my, mx + 22, my + 12, K("azul", 2))                            # cuerpo
    cv.rect(mx, my + 1, mx + 4, my + 9, K("azul", 1)); cv.rect(mx + 22, my + 1, mx + 30, my + 5, K("azul", 1))   # mangas
    cv.rect(mx + 4, my + 12, mx + 12, my + 22, K("azul", 2)); cv.rect(mx + 14, my + 12, mx + 22, my + 21, K("azul", 1))   # perneras
    cv.vline(mx + 13, my, my + 12, K("azul", 4)); cv.hline(mx + 4, mx + 22, my + 12, K("azul", 0))
    cv.rect(mx + 15, my + 3, mx + 20, my + 7, K("papel", 3)); cv.px(mx + 16, my + 4, K("rojo", 3)); cv.hline(mx + 17, mx + 19, my + 5, K("gris", 2))
    cv.rect(mx + 6, my + 3, mx + 10, my + 7, K("azul", 1))                         # bolsillo (con la tarjeta de Barlow)
    cv.hline(mx + 6, mx + 10, my + 3, K("papel", 2))
    # herramientas
    cv.rect(x0 + 40, top0 + 4, x0 + 54, top0 + 6, K("madera", 4)); cv.rect(x0 + 52, top0 + 2, x0 + 56, top0 + 8, K("gris", 4))   # martillo
    cv.rect(x0 + 40, top0 + 10, x0 + 46, top0 + 12, K("rojo", 2)); cv.hline(x0 + 46, x0 + 56, top0 + 11, K("gris", 6))           # destornillador
    cv.d.line([(x0 + 60, top0 + 4), (x0 + 66, top0 + 12)], fill=K("gris", 5)); cv.d.line([(x0 + 66, top0 + 4), (x0 + 60, top0 + 12)], fill=K("gris", 5))   # alicates
    cv.rect(x0 + 58, top0 + 14, x0 + 72, top0 + 22, K("gris", 2)); cv.frame(x0 + 58, top0 + 14, x0 + 72, top0 + 22, K("gris", 1))   # chasis abierto
    for k in range(x0 + 60, x0 + 70, 3):
        cv.rect(k, top0 + 15, k + 2, top0 + 19, K("cielo", 2))
    cv.ellipse(x0 + 42, top0 + 15, x0 + 52, top0 + 23, None, outline=K("ocre", 2))    # bobina de hilo de cobre
    cv.ellipse(x0 + 44, top0 + 17, x0 + 50, top0 + 21, None, outline=K("ocre", 1))
    # una vela consumida en la esquina de la mesa
    cv.ellipse(x1 - 10, top0 + 3, x1 - 2, top0 + 8, K("papel", 3)); cv.rect(x1 - 8, top0 + 1, x1 - 4, top0 + 5, K("papel", 2))
    cv.px(x1 - 6, top0, K("gris", 0))
    # un taburete delante
    sx, sy = x0 + 30, y1 + 4
    cv.ellipse(sx + 2, sy + 10, sx + 18, sy + 14, K("gris", 0))
    cv.ellipse(sx, sy, sx + 16, sy + 6, K("madera", 4), outline=K("madera", 1))
    for lx in (sx + 2, sx + 12):
        cv.rect(lx, sy + 5, lx + 2, sy + 12, K("madera", 1))


# ---------------------------------------------------------------- la pared de los nombres


IVY = ["#..........", "#..........", "#.#.#.#.#..", "#.#.#.#.#..", "#..#...##..", "........#..", ".......#..."]


def _garabato(cv, x, y, largo, col, rnd, inclinado=0):
    """Un nombre escrito a tiza, ilegible a esta distancia: trazo cursivo arriba y abajo."""
    pts = []
    k = 0
    while k < largo:
        pts.append((x + k, y + rnd.choice([0, -2, -3, 1]) - (k * inclinado) // 10))
        k += rnd.choice([1, 2, 2, 3])
    cv.d.line(pts, fill=col)
    if rnd.random() < 0.35:                                                        # mayúscula al principio
        cv.vline(x, y - 4, y + 1, col)


def _pared_nombres(cv, rnd):
    x0, y0, x1, y1 = NOMBRES
    # un viejo panel de anuncios, pintado de negro: la pizarra de los que pasaron por aquí
    cv.rect(x0 - 3, y0 - 3, x1 + 5, y1 + 5, K("papel", 0))
    cv.rect(x0 - 3, y0 - 3, x1 + 3, y1 + 3, K("madera", 1)); cv.hline(x0 - 3, x1 + 3, y0 - 3, K("madera", 3))
    cv.rect(x0, y0, x1, y1, K("gris", 1))
    for _ in range(80):                                                            # borrones de tiza
        cv.px(rnd.randint(x0, x1 - 1), rnd.randint(y0, y1 - 1), K("gris", 2))
    tizas = [K("papel", 1), K("papel", 2), K("gris", 5), K("gris", 6), K("papel", 2), K("papel", 3)]
    filas = list(range(y0 + 6, y1 - 1, 5))
    for fy in filas:
        x = x0 + rnd.randint(2, 5)
        while x < x1 - 6:
            largo = rnd.randint(5, 13)
            if x + largo > x1 - 2:
                break
            if y0 + 19 <= fy <= y0 + 45 and x0 + 25 <= x + largo and x <= x0 + 61:   # el hueco de Ivy (y de Felix)
                x += 2
                continue
            col = rnd.choice(tizas)
            _garabato(cv, x, fy + rnd.randint(-1, 1), largo, col, rnd, inclinado=rnd.choice([0, 0, 1, -1]))
            if rnd.random() < 0.22:                                                # tachado
                cv.hline(x - 1, x + largo + 1, fy - 1, col)
            x += largo + rnd.randint(2, 4)
    # Ivy, legible, con letra redonda
    ix, iy = x0 + 30, y0 + 23
    cv.grid(ix, iy, IVY, {"#": K("papel", 4)})
    cv.hline(ix - 1, ix + 10, iy + 8, K("papel", 3))                               # alguien la subrayó
    # y debajo, con otra letra, Felix A.
    cv.text(ix - 2, iy + 12, "FELIX A.", K("gris", 6))
    # la tiza, en el reborde
    cv.rect(x0 + 50, y1 + 1, x0 + 56, y1 + 3, K("papel", 4))


# ---------------------------------------------------------------- andén y foso


def _anden(cv, rnd):
    cv.rect(0, MURO, W, BORDE, K("gris", 3))
    for y in range(MURO, BORDE, 12):                                               # losas
        cv.hline(0, W, y, K("gris", 2))
        for x in range((y // 12 % 2) * 16, W, 32):
            cv.vline(x, y, min(BORDE, y + 12), K("gris", 2))
    P.manchas(cv, 0, MURO, W, BORDE, K("gris", 2), n=600, semilla=33)
    P.manchas(cv, 0, MURO, W, BORDE, K("gris", 4), n=200, semilla=34)
    cv.rect(0, MURO, W, MURO + 4, K("gris", 2))                                    # sombra al pie de la pared
    # la línea blanca de antes y el bordillo de piedra
    for x in range(0, W, 10):
        cv.hline(x, x + 7, 186, K("papel", 1))
    cv.rect(0, 190, W, BORDE, K("gris", 5)); cv.hline(0, W, 190, K("gris", 6))
    for x in range(0, W, 24):
        cv.vline(x, 190, BORDE, K("gris", 4))
    cv.rect(0, BORDE, W, BORDE + 4, K("gris", 2)); cv.hline(0, W, BORDE + 3, K("gris", 1))   # canto del andén


def _foso(cv, rnd):
    cv.rect(0, BORDE + 4, W, FOSO, K("gris", 1))
    for _ in range(900):
        cv.px(rnd.randint(0, W - 1), rnd.randint(BORDE + 4, FOSO - 1), K("gris", rnd.choice([0, 2])))
    cv.rect(0, BORDE + 4, W, BORDE + 8, K("gris", 0))                              # bajo el voladizo del andén
    for x in range(6, W, 14):                                                      # traviesas
        cv.rect(x, 214, x + 7, 240, K("madera", 1)); cv.vline(x + 6, 214, 240, K("madera", 0))
    for ry in (220, 234):
        cv.rect(0, ry - 1, W, ry + 2, K("gris", 3)); cv.hline(0, W, ry - 1, K("gris", 4)); cv.hline(0, W, ry + 2, K("gris", 0))
        for x in range(0, W, 9):
            if rnd.random() < 0.5:
                cv.hline(x, x + rnd.randint(2, 6), ry, K("madera", 2))
    cv.ellipse(140, 222, 200, 238, K("pared", 0), outline=K("pared", 1))           # agua estancada
    cv.hline(152, 170, 226, K("pared", 2))
    cv.rect(0, FOSO, W, H, K("gris", 0))
    cv.hline(0, W, FOSO, K("gris", 2))


def _vela_consumida(cv, x, y, rnd):
    cv.ellipse(x - 5, y - 1, x + 6, y + 4, K("papel", 2))                         # charco de cera
    cv.ellipse(x - 3, y, x + 3, y + 3, K("papel", 3))
    h = rnd.randint(1, 4)
    cv.rect(x - 1, y - h, x + 2, y + 1, K("papel", 3)); cv.vline(x + 1, y - h, y + 1, K("papel", 2))
    cv.px(x, y - h - 1, K("gris", 0))                                              # pabilo quemado
    if rnd.random() < 0.5:
        cv.px(x + 4, y + 1, K("papel", 3)); cv.px(x - 4, y + 2, K("papel", 1))


def dibujar(variante=None):
    rnd = random.Random(1322)
    cv = Canvas(W, H)
    _techo(cv)
    _azulejo(cv, rnd)
    _rotulo_tapado(cv, rnd)
    _reloj(cv)
    _pared_nombres(cv, rnd)
    _anden(cv, rnd)
    _foso(cv, rnd)
    _pila_telepantallas(cv, rnd)
    _mesa(cv, rnd)
    for (vx, vy) in VELAS:
        _vela_consumida(cv, vx, vy, rnd)
    # cajas de piezas y un saco junto a la mesa
    for (bx, by) in ((384, 100), (392, 112)):
        cv.rect(bx + 2, by + 12, bx + 22, by + 15, K("gris", 0))
        cv.rect(bx, by, bx + 20, by + 4, K("madera", 4)); cv.rect(bx, by + 4, bx + 20, by + 13, K("madera", 3))
        cv.frame(bx, by, bx + 20, by + 13, K("madera", 1))
        cv.px(bx + 5, by + 2, K("cielo", 3)); cv.px(bx + 9, by + 1, K("cielo", 2)); cv.px(bx + 13, by + 2, K("ocre", 2))
    # muro derecho (tapa) y techo; la entrada a la izquierda queda abierta
    cv.rect(468, 0, W, BORDE + 4, K("gris", 3)); cv.vline(468, TECHO, BORDE + 4, K("gris", 4))
    # luz tenue y uniforme; un poco más oscuro hacia la boca del túnel (izquierda) y en el foso
    cv.add_light(0, 0, W, TECHO, -1)
    cv.add_light(0, MURO, 14, BORDE, -1)
    cv.add_light(0, BORDE + 4, W, H, -1)
    cv.bake_lighting()
    return cv
