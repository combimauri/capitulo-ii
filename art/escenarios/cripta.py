"""J13.03 — La cripta de San Clemente, bajo una iglesia bombardeada hace treinta años.

Bóvedas de piedra ennegrecida, lápidas con los nombres borrados, velas por todas partes, estanterías de tablones
y ladrillos llenas de libros, la máquina de escribir, el camastro, el teléfono de campaña que nunca se ha usado
y, en el centro, la estructura de las campanas: vacía, con un solo gancho.

La paleta más cálida del juego: ámbar de vela, madera y el rojo apagado de los lomos. Ni Partido ni proles.

dibujar(variante=None, extras=None)
  variante "losa_nueva": una losa nueva, sin nombre, entre las lápidas (FE.02, 1988).
  extras(cv): se llama antes de hornear la luz, para pintar figuras que reciban la luz de las velas.
  detras(cv): igual, pero antes de dibujar la mesa (figuras sentadas detrás del tablero).
"""
import math
import random

from pixel import Canvas, K
import props as P
import _luz as L

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 20, 92, 246
ESCALERA = (48, 30, 80, 92)                     # la escalera de caracol; el jugador aparece en (64,112)
ESTANTE_IZQ = (100, 28, 200, 92)                # huella (100,92)-(200,104)
ESTANTE_DER = (300, 28, 430, 92)                # huella (300,92)-(430,104)
CAMPANAS = (214, 22, 286, 92)
MESA = (150, 140, 230, 170)
CAMASTRO = (340, 180, 420, 210)
TELEFONO = (52, 200, 68, 216)
LAPIDAS = [(64, 140, 92, 156), (106, 182, 136, 198), (176, 206, 206, 222), (292, 152, 322, 168),
           (246, 116, 274, 130), (378, 128, 408, 144), (300, 222, 330, 238), (84, 226, 112, 240)]
LOSA_NUEVA = (240, 186, 270, 202)
ALTO_MESA = 14                                  # el tablero se dibuja 14 px por encima de su huella

# velas: (x, y de la llama, tamaño). Se rellenan al dibujar el atrezo.
VELAS = []


# ---------------------------------------------------------------- piedra


def _sillares(cv, x0, y0, x1, y1, rnd):
    """Sillería de piedra ennegrecida por el humo de treinta años de velas."""
    cv.rect(x0, y0, x1, y1, K("madera", 0))
    for fila, y in enumerate(range(y0, y1, 9)):
        off = (fila % 2) * 9
        x = x0 - off
        while x < x1:
            w = rnd.choice([14, 16, 18, 20])
            b = rnd.choice([1, 2, 2, 2, 3])
            c = K("madera", b) if rnd.random() > 0.1 else K("papel", 0)
            cv.rect(max(x0, x + 1), y + 1, min(x1, x + w), min(y1, y + 9), c)
            cv.hline(max(x0, x + 1), min(x1, x + w), y + 1, K("madera", min(4, b + 1)) if c != K("papel", 0) else K("papel", 1))
            x += w
    for _ in range(40):                                                            # hollín y salitre
        sx, sy = rnd.randint(x0, x1 - 2), rnd.randint(y0, y1 - 10)
        for k in range(rnd.randint(4, 14)):
            cv.px(sx, sy + k, K("madera", 0))


def _bovedas(cv, rnd):
    """Tres crujías con arcos: la piedra del arco, en dovelas, y el fondo de cada bóveda más oscuro arriba."""
    pilastras = [(84, 96), (202, 212), (288, 298)]
    for (a, b) in pilastras:
        cv.rect(a, WT, b, WB, K("madera", 2))
        cv.vline(a, WT, WB, K("madera", 4)); cv.vline(b - 1, WT, WB, K("madera", 0))
        for y in range(WT + 6, WB, 9):
            cv.hline(a + 1, b - 1, y, K("madera", 1))
        cv.rect(a - 2, 42, b + 2, 46, K("madera", 3)); cv.hline(a - 2, b + 2, 42, K("madera", 4))   # imposta
    vanos = [(X0, 84), (96, 202), (212, 288), (298, X1)]
    for (a, b) in vanos:
        # el arco: una banda de dovelas desde la imposta hasta la clave, en WT
        cx, r = (a + b) / 2, (b - a) / 2
        for ang in range(0, 181, 2):
            t = math.radians(ang)
            for k in range(5):
                rr = r - k
                x = int(cx - math.cos(t) * rr)
                y = int(44 - math.sin(t) * min(24, rr * 0.5) - k * 0)
                if WT <= y < WB and a <= x < b:
                    cv.px(x, y, K("madera", 3) if k == 0 else (K("madera", 1) if k == 4 else K("madera", 2)))
        for ang in range(10, 171, 16):                                             # juntas de las dovelas
            t = math.radians(ang)
            x = int(cx - math.cos(t) * (r - 2)); y = int(44 - math.sin(t) * min(24, (r - 2) * 0.5))
            cv.px(x, y, K("madera", 0)); cv.px(x, y + 1, K("madera", 0))
        # el plemento por encima del arco, en sombra
        for x in range(a, b):
            t = (x - cx) / r
            ya = int(44 - math.sqrt(max(0.0, 1 - t * t)) * min(24, r * 0.5))
            cv.vline(x, WT, max(WT, ya - 1), K("madera", 0) if (x + ya) % 3 else K("madera", 1))


# ---------------------------------------------------------------- velas


def vela(cv, x, y, alto=6, grosor=2, apagada=False):
    """Vela de pie: (x, y) es la base. Devuelve la posición de la llama y la registra en VELAS."""
    cv.ellipse(x - 3, y - 1, x + grosor + 3, y + 2, K("papel", 2))                  # cera derramada
    cv.rect(x, y - alto, x + grosor, y + 1, K("papel", 4))
    cv.vline(x + grosor - 1, y - alto + 1, y + 1, K("papel", 2))
    cv.px(x - 1, y - alto + 2, K("papel", 3))                                      # goterón
    if apagada:
        cv.px(x, y - alto - 1, K("gris", 0))
        return None
    fx = x + grosor // 2
    cv.px(fx, y - alto - 1, K("gris", 0))
    cv.rect(fx - 1 + (grosor == 1), y - alto - 4, fx + 1, y - alto - 1, K("ocre", 4))
    cv.px(fx, y - alto - 5, K("ocre", 3)); cv.px(fx - (grosor > 1), y - alto - 3, K("papel", 4))
    cv.add_emissive(fx - 1, y - alto - 5, fx + 1, y - alto - 1)
    VELAS.append((fx, y - alto - 3, alto))
    return (fx, y - alto - 3)


def grupo_velas(cv, x, y, rnd, n=3):
    for k in range(n):
        vela(cv, x + k * 4 + rnd.randint(-1, 1), y + rnd.randint(-2, 2) + (k % 2) * 2, alto=rnd.randint(3, 9),
             grosor=rnd.choice([1, 2, 2]))


# ---------------------------------------------------------------- atrezo


def _escalera_caracol(cv):
    x0, y0, x1, y1 = ESCALERA
    cx = (x0 + x1) // 2
    # el pozo en el techo por donde baja
    cv.ellipse(x0 - 2, WT - 12, x1 + 2, WT + 2, K("gris", 0))
    cv.d.arc([x0 - 2, WT - 12, x1 + 1, WT + 1], 0, 180, fill=K("madera", 2))
    cv.rect(x0 - 4, WT - 2, x1 + 4, y1 + 4, K("madera", 0))                        # hueco oscuro en la esquina
    cv.rect(x0 - 4, WT - 2, x0 - 2, y1 + 4, K("madera", 1))
    # peldaños en hélice: los de detrás del mástil primero
    pasos = []
    for i in range(12):
        ang = i * 0.78
        y = WT + 4 + i * 6
        pasos.append((math.sin(ang), ang, y))
    radio = 15
    for fondo in (True, False):
        for (s, ang, y) in pasos:
            if (s < 0) != fondo:
                continue
            ex = cx + math.cos(ang) * radio
            col_cara, col_canto = (K("gris", 2), K("gris", 1)) if fondo else (K("gris", 4), K("gris", 2))
            cv.poly([(cx, y - 1), (int(ex), y - 2 + int(s * 2)), (int(ex), y + 1 + int(s * 2)), (cx, y + 2)], col_cara)
            cv.d.line([(cx, y + 2), (int(ex), y + 1 + int(s * 2))], fill=col_canto)
            cv.px(int(ex), y - 2 + int(s * 2), K("gris", 6) if not fondo else K("gris", 3))
            # balaustre del pasamanos
            cv.vline(int(ex), y - 11 + int(s * 2), y - 1 + int(s * 2), K("gris", 3) if not fondo else K("gris", 1))
        if fondo:
            cv.rect(cx - 1, WT - 6, cx + 2, y1 + 2, K("gris", 3))                   # el mástil
            cv.vline(cx - 1, WT - 6, y1 + 2, K("gris", 5)); cv.vline(cx + 1, WT - 6, y1 + 2, K("gris", 1))
    # pasamanos: una hélice por encima de los peldaños
    pts = [(int(cx + math.cos(ang) * radio), y - 11 + int(s * 2)) for (s, ang, y) in pasos]
    for (a, b) in zip(pts, pts[1:]):
        cv.d.line([a, b], fill=K("gris", 4))
    # arranque en el suelo
    cv.ellipse(x0 + 2, y1, x1 - 2, y1 + 8, K("gris", 1))
    cv.ellipse(x0 + 6, y1 + 1, x1 - 6, y1 + 6, K("gris", 3))


def _libros(cv, x0, x1, base, rnd, hueco_vela=None):
    """Una balda llena: lomos verticales, algún libro tumbado, alguno inclinado."""
    x = x0 + 1
    while x < x1 - 2:
        if hueco_vela and hueco_vela[0] <= x < hueco_vela[1]:
            x = hueco_vela[1]
            continue
        t = rnd.random()
        if t < 0.08:                                                               # pila de libros tumbados
            w = rnd.randint(8, 12)
            if x + w > x1 - 1:
                break
            for k in range(rnd.randint(2, 3)):
                c = rnd.choice([("granate", 3), ("madera", 4), ("rojo", 1), ("ocre", 1)])
                cv.rect(x, base - 3 - k * 3, x + w - k, base - k * 3, K(*c)); cv.hline(x, x + w - k, base - 3 - k * 3, K(c[0], c[1] + 1))
            x += w + 1
            continue
        w = rnd.choice([2, 3, 3, 4])
        h = rnd.randint(8, 13)
        if x + w > x1 - 1:
            break
        c = rnd.choice([("granate", 2), ("granate", 3), ("granate", 4), ("rojo", 1), ("rojo", 2), ("madera", 3),
                        ("madera", 4), ("madera", 5), ("ocre", 1), ("ocre", 2), ("papel", 1), ("granate", 1)])
        cv.rect(x, base - h, x + w, base, K(*c))
        cv.vline(x, base - h, base, K(c[0], c[1] + 1))
        if w >= 3 and rnd.random() < 0.5:                                          # nervios del lomo
            cv.hline(x, x + w, base - h + 2, K("ocre", 2)); cv.hline(x, x + w, base - 3, K("ocre", 2))
        cv.vline(x + w - 1, base - h, base, K(c[0], max(0, c[1] - 1)))
        x += w
        if rnd.random() < 0.06:                                                    # uno inclinado
            cv.d.line([(x + 1, base - 1), (x + 5, base - 11)], fill=K("granate", 3))
            cv.d.line([(x + 2, base - 1), (x + 6, base - 11)], fill=K("granate", 2))
            x += 7


def _estanteria(cv, rect, rnd, baldas=(40, 58, 76, 94)):
    x0, y0, x1, y1 = rect
    cv.rect(x0 + 3, y0 + 3, x1 + 3, 104, K("madera", 0))                            # sombra en la pared
    # pilares de ladrillo en los extremos (y en medio si es larga)
    pilares = [x0, x1 - 8] + ([(x0 + x1) // 2 - 4] if x1 - x0 > 110 else [])
    tops = [y0] + list(baldas[:-1])
    for i, by in enumerate(baldas):
        top = tops[i] + 4
        # ladrillos de este tramo
        for px_ in pilares:
            for yy in range(top, by, 4):
                cv.rect(px_, yy, px_ + 8, yy + 4, K("granate", 2 + (yy // 4 + px_) % 2))
                cv.hline(px_, px_ + 8, yy + 3, K("granate", 0)); cv.vline(px_ + 4 * ((yy // 4) % 2), yy, yy + 3, K("granate", 0))
        # libros entre pilares
        tramos = sorted(pilares)
        for (a, b) in zip(tramos, tramos[1:]):
            hueco = None
            if rnd.random() < 0.45:
                hx = rnd.randint(a + 12, b - 20)
                hueco = (hx, hx + 8)
            _libros(cv, a + 8, b, by, rnd, hueco_vela=hueco)
            if hueco:
                vela(cv, hueco[0] + 3, by - 1, alto=rnd.randint(3, 6), grosor=2)
        # el tablón
        cv.rect(x0 - 2, by, x1 + 2, by + 4, K("madera", 4))
        cv.hline(x0 - 2, x1 + 2, by, K("madera", 5)); cv.hline(x0 - 2, x1 + 2, by + 3, K("madera", 1))
    # tablón superior con libros tumbados y papeles
    cv.rect(x0 - 2, y0, x1 + 2, y0 + 4, K("madera", 4)); cv.hline(x0 - 2, x1 + 2, y0, K("madera", 5)); cv.hline(x0 - 2, x1 + 2, y0 + 3, K("madera", 1))
    # base de ladrillo sobre el suelo (huella hasta y=104)
    cv.rect(x0, baldas[-1] + 4, x1, 104, K("granate", 1)); cv.hline(x0, x1, 103, K("granate", 0))
    for px_ in range(x0 + 4, x1 - 4, 10):
        cv.rect(px_, baldas[-1] + 5, px_ + 8, 103, K("madera", 1))                  # cajas de papeles bajo la última balda
        cv.hline(px_, px_ + 8, baldas[-1] + 5, K("papel", 1))


def _campanas(cv):
    x0, y0, x1, y1 = CAMPANAS
    cv.rect(x0 + 4, y1 + 4, x1 + 6, y1 + 10, K("madera", 0))                        # sombra en el suelo
    # durmientes en el suelo
    cv.rect(x0 - 2, y1, x1 + 2, y1 + 6, K("madera", 2)); cv.hline(x0 - 2, x1 + 2, y1, K("madera", 4)); cv.hline(x0 - 2, x1 + 2, y1 + 5, K("madera", 0))
    # postes
    for px_ in (x0 + 2, x1 - 10):
        cv.rect(px_, y0 + 6, px_ + 8, y1, K("madera", 3))
        cv.vline(px_, y0 + 6, y1, K("madera", 5)); cv.vline(px_ + 7, y0 + 6, y1, K("madera", 1))
        for yy in range(y0 + 14, y1 - 4, 11):
            cv.hline(px_ + 2, px_ + 5, yy, K("madera", 2))                         # vetas
    # tornapuntas en diagonal
    for (a, b, c, d) in ((x0 + 10, y0 + 30, x0 + 26, y0 + 10), (x1 - 10, y0 + 30, x1 - 26, y0 + 10),
                         (x0 - 2, y1, x0 + 4, y1 - 22), (x1 + 2, y1, x1 - 4, y1 - 22)):
        cv.d.line([(a, b), (c, d)], fill=K("madera", 3), width=3)
        cv.d.line([(a, b + 2), (c, d + 2)], fill=K("madera", 1))
    # travesaño alto (el cabezal) y uno bajo
    cv.rect(x0 - 2, y0, x1 + 2, y0 + 8, K("madera", 3))
    cv.hline(x0 - 2, x1 + 2, y0, K("madera", 5)); cv.hline(x0 - 2, x1 + 2, y0 + 7, K("madera", 1))
    cv.rect(x0 + 2, y1 - 22, x1 - 2, y1 - 17, K("madera", 2)); cv.hline(x0 + 2, x1 - 2, y1 - 22, K("madera", 4))
    for (bx, by) in ((x0 + 4, y0 + 3), (x1 - 6, y0 + 3), (x0 + 5, y1 - 20), (x1 - 7, y1 - 20)):
        cv.px(bx, by, K("gris", 4))                                                # pernos
    # las marcas claras donde colgaban las otras campanas
    for mx in (x0 + 18, x1 - 22):
        cv.rect(mx, y0 + 8, mx + 4, y0 + 10, K("madera", 5))
    # el gancho, el único que queda
    gx = (x0 + x1) // 2
    cv.rect(gx - 2, y0 + 8, gx + 3, y0 + 11, K("gris", 3))
    for k in range(5):                                                             # cadena
        cv.px(gx, y0 + 12 + k * 2, K("gris", 4)); cv.px(gx, y0 + 13 + k * 2, K("gris", 2))
    cv.d.arc([gx - 4, y0 + 20, gx + 4, y0 + 30], 0, 200, fill=K("gris", 4))
    cv.px(gx - 4, y0 + 24, K("gris", 5)); cv.px(gx - 3, y0 + 23, K("gris", 4))
    # velas al pie de la estructura
    VELAS_BASE = [(x0 + 14, y1 + 2), (x0 + 22, y1 + 4), (x1 - 20, y1 + 3)]
    for (vx, vy) in VELAS_BASE:
        vela(cv, vx, vy, alto=7, grosor=2)


def _mesa(cv, rnd):
    x0, y0, x1, y1 = MESA
    t0, t1 = y0 - ALTO_MESA, y1 - ALTO_MESA
    cv.rect(x0 + 4, y1 - 2, x1 + 6, y1 + 4, K("madera", 0))                        # sombra
    for lx in (x0 + 2, x1 - 6):
        cv.rect(lx, t1, lx + 4, y1, K("madera", 2)); cv.vline(lx, t1, y1, K("madera", 3)); cv.vline(lx + 3, t1, y1, K("madera", 0))
    cv.rect(x0, t0, x1, t1, K("madera", 4)); cv.frame(x0, t0, x1, t1, K("madera", 2))
    cv.hline(x0 + 1, x1 - 1, t0 + 1, K("madera", 5))
    for k in (t0 + 10, t0 + 20):
        cv.hline(x0 + 1, x1 - 1, k, K("madera", 3))
    cv.rect(x0, t1, x1, t1 + 6, K("madera", 3)); cv.hline(x0, x1, t1 + 5, K("madera", 1))
    cv.px(x0 + 30, t1 + 2, K("ocre", 2))                                           # tirador del cajón
    cv.frame(x0 + 22, t1 + 1, x0 + 40, t1 + 5, K("madera", 2))
    # la máquina de escribir, antigua, negra con letras doradas
    mx, my = x0 + 28, t0 + 6
    cv.rect(mx - 1, my + 12, mx + 25, my + 15, K("madera", 2))                      # sombra en el tablero
    cv.rect(mx, my + 2, mx + 24, my + 13, K("gris", 1)); cv.frame(mx, my + 2, mx + 24, my + 13, K("gris", 0))
    cv.rect(mx + 1, my, mx + 23, my + 3, K("gris", 2)); cv.hline(mx + 1, mx + 23, my, K("gris", 4))   # rodillo
    cv.rect(mx - 2, my, mx, my + 2, K("gris", 3)); cv.rect(mx + 24, my, mx + 26, my + 2, K("gris", 3))
    cv.rect(mx + 5, my - 7, mx + 19, my + 1, K("papel", 4))                         # la hoja en el rodillo
    for k in range(3):
        cv.hline(mx + 7, mx + 16 - k * 2, my - 5 + k * 2, K("gris", 4))
    for r in range(3):                                                             # teclas
        for c in range(6 - (r == 2)):
            cv.px(mx + 4 + c * 3 + r, my + 6 + r * 2, K("papel", 3))
    cv.hline(mx + 4, mx + 20, my + 11, K("gris", 3))                               # barra espaciadora
    cv.hline(mx + 8, mx + 16, my + 4, K("ocre", 3))                                # el nombre del fabricante, en dorado
    # montones de papel (a la izquierda, escrito; a la derecha, en blanco)
    for k in range(4):
        cv.rect(x0 + 4 - k % 2, t0 + 10 - k * 2, x0 + 22 - k % 2, t0 + 22 - k * 2, K("papel", 3 if k % 2 else 2))
        cv.hline(x0 + 4 - k % 2, x0 + 22 - k % 2, t0 + 22 - k * 2, K("papel", 1))
    for k in range(3):
        cv.hline(x0 + 7, x0 + 19, t0 + 6 + k * 2, K("gris", 5))
    for k in range(3):
        cv.rect(x1 - 24 + k, t0 + 18 - k * 2, x1 - 8 + k, t0 + 26 - k * 2, K("papel", 4 - (k % 2)))
    # la tetera y dos tazas desportilladas
    tx, ty = x1 - 22, t0 + 2
    cv.ellipse(tx, ty + 1, tx + 12, ty + 11, K("granate", 3), outline=K("granate", 1))
    cv.ellipse(tx + 2, ty + 2, tx + 7, ty + 6, K("granate", 4))
    cv.rect(tx + 4, ty - 1, tx + 8, ty + 2, K("granate", 2)); cv.px(tx + 5, ty - 2, K("granate", 4))
    cv.d.line([(tx + 11, ty + 6), (tx + 15, ty + 2)], fill=K("granate", 3))
    cv.d.arc([tx - 4, ty + 3, tx + 2, ty + 9], 90, 270, fill=K("granate", 2))
    for (cx, cy) in ((x0 + 18, t0 + 24), (x1 - 36, t0 + 22)):
        cv.rect(cx, cy, cx + 5, cy + 5, K("papel", 3)); cv.hline(cx, cx + 5, cy, K("papel", 4))
        cv.rect(cx + 1, cy + 1, cx + 4, cy + 2, K("madera", 2))                     # té frío
        cv.px(cx + 5, cy + 2, K("papel", 2)); cv.px(cx + 6, cy + 2, K("papel", 2)); cv.px(cx + 6, cy + 3, K("papel", 2))   # asa
        cv.px(cx + 1, cy, K("madera", 1))                                           # la mella
    # velas en la mesa
    vela(cv, x0 + 2, t0 + 8, alto=5, grosor=2)
    vela(cv, x1 - 6, t0 + 30, alto=8, grosor=2)
    # taburetes a cada lado
    for sx in (x0 - 20, x1 + 4):
        sy = y0 + 2
        cv.ellipse(sx + 2, sy + 14, sx + 18, sy + 19, K("madera", 0))
        for lx in (sx + 2, sx + 12):
            cv.rect(lx, sy + 4, lx + 2, sy + 16, K("madera", 1))
        cv.ellipse(sx, sy, sx + 16, sy + 7, K("madera", 4), outline=K("madera", 2))
        cv.hline(sx + 3, sx + 12, sy + 2, K("madera", 5))


def _camastro(cv, rnd):
    x0, y0, x1, y1 = CAMASTRO
    t0, t1 = y0 - 6, y1 - 6
    cv.rect(x0 + 3, y1 - 2, x1 + 5, y1 + 3, K("madera", 0))
    cv.rect(x0, t1, x1, t1 + 6, K("madera", 2)); cv.hline(x0, x1, t1 + 5, K("madera", 0))   # larguero
    for lx in (x0 + 1, x1 - 4):
        cv.rect(lx, t1 + 6, lx + 3, y1, K("madera", 1))
    cv.rect(x0, t0, x1, t1, K("madera", 3)); cv.frame(x0, t0, x1, t1, K("madera", 1))
    cv.rect(x0 + 2, t0 + 1, x1 - 2, t1 - 1, K("papel", 1))                         # colchón de lana
    cv.rect(x0 + 3, t0 + 3, x0 + 18, t1 - 4, K("papel", 3)); cv.hline(x0 + 3, x0 + 18, t0 + 3, K("papel", 4))   # almohada
    cv.hline(x0 + 3, x0 + 18, t1 - 5, K("papel", 1))
    # la manta: granate con cenefa ocre, arrugada y a medio caer
    cv.poly([(x0 + 20, t0 + 1), (x1 - 2, t0 + 1), (x1 + 2, t1 + 6), (x0 + 22, t1 + 2)], K("granate", 3))
    cv.d.line([(x0 + 20, t0 + 1), (x0 + 22, t1 + 2)], fill=K("granate", 4))
    for k in range(x0 + 26, x1 - 4, 9):                                            # pliegues
        cv.d.line([(k, t0 + 3), (k + 3, t1 - 2)], fill=K("granate", 2))
    cv.d.line([(x0 + 22, t1 + 2), (x1 + 2, t1 + 6)], fill=K("ocre", 2))
    cv.d.line([(x0 + 22, t1 + 1), (x1 + 2, t1 + 5)], fill=K("granate", 1))
    # un libro abierto y las gafas de leer sobre la manta
    cv.rect(x1 - 30, t0 + 5, x1 - 18, t0 + 11, K("papel", 3)); cv.vline(x1 - 24, t0 + 5, t0 + 11, K("papel", 1))
    # caja-mesilla con una vela
    bx, by = x1 + 4, y0 - 6
    if bx + 14 <= X1:
        cv.rect(bx, by, bx + 14, by + 16, K("madera", 2)); cv.rect(bx, by, bx + 14, by + 4, K("madera", 4))
        cv.frame(bx, by, bx + 14, by + 16, K("madera", 0))
        vela(cv, bx + 6, by + 3, alto=5, grosor=2)


def _telefono(cv, rnd):
    x0, y0, x1, y1 = TELEFONO
    cv.rect(x0 + 2, y1 - 1, x1 + 3, y1 + 2, K("madera", 0))                        # sombra
    cv.rect(x0, y0 + 4, x1, y1, K("pared", 2)); cv.frame(x0, y0 + 4, x1, y1, K("pared", 0))
    cv.rect(x0, y0, x1, y0 + 4, K("pared", 3)); cv.hline(x0, x1, y0, K("pared", 4))   # tapa
    cv.rect(x0 + 2, y0 - 2, x1 - 2, y0 + 1, K("gris", 1))                          # auricular en su horquilla
    cv.rect(x0 + 1, y0 - 3, x0 + 4, y0, K("gris", 2)); cv.rect(x1 - 4, y0 - 3, x1 - 1, y0, K("gris", 2))
    cv.rect(x0 + 3, y0 + 7, x1 - 3, y0 + 10, K("pared", 1)); cv.px(x0 + 5, y0 + 8, K("papel", 2))   # placa
    cv.rect(x1, y0 + 8, x1 + 3, y0 + 10, K("gris", 3)); cv.vline(x1 + 2, y0 + 10, y0 + 13, K("gris", 3))   # manivela
    for _ in range(14):                                                            # polvo
        cv.px(rnd.randint(x0, x1 - 1), rnd.randint(y0, y1 - 1), K("pared", 4))
    # el cable: por el suelo hasta el muro, y luego arriba por la esquina hasta perderse en el techo
    cv.d.line([(x0, y0 + 12), (X0 + 2, y0 + 10), (X0 + 1, WB + 6)], fill=K("gris", 1))
    cv.vline(X0 + 1, WT, WB + 6, K("gris", 1))
    for gy in range(WT + 8, WB + 6, 16):
        cv.px(X0 + 2, gy, K("gris", 4))                                            # grapas


def _lapida(cv, x0, y0, x1, y1, rnd, nueva=False):
    if nueva:
        cv.rect(x0 - 1, y0 - 1, x1 + 1, y1 + 1, K("madera", 0))
        cv.rect(x0, y0, x1, y1, K("papel", 2)); cv.hline(x0, x1, y0, K("papel", 3))
        cv.hline(x0, x1, y1 - 1, K("papel", 1)); cv.vline(x1 - 1, y0, y1, K("papel", 1))
        for _ in range(8):                                                         # mortero fresco en las juntas
            cv.px(rnd.randint(x0 - 1, x1), rnd.choice([y0 - 1, y1]), K("papel", 3))
        return
    cv.rect(x0, y0, x1, y1, K("papel", 0)); cv.frame(x0, y0, x1, y1, K("madera", 0))
    cv.hline(x0 + 1, x1 - 1, y0 + 1, K("papel", 1)); cv.vline(x1 - 1, y0 + 1, y1, K("madera", 3))
    # cruz e inscripción borradas por las pisadas
    cx = (x0 + x1) // 2
    cv.vline(cx, y0 + 2, y0 + 7, K("madera", 2)); cv.hline(cx - 2, cx + 3, y0 + 3, K("madera", 2))
    for k in range(y0 + 9, y1 - 2, 2):
        for xx in range(x0 + 4, x1 - 4):
            if rnd.random() < 0.35:
                cv.px(xx, k, K("madera", 2))
    for _ in range(10):
        cv.px(rnd.randint(x0 + 1, x1 - 2), rnd.randint(y0 + 1, y1 - 2), K("papel", 1))
    if rnd.random() < 0.5:                                                         # una grieta
        gx, gy = rnd.randint(x0 + 3, x1 - 6), y0 + 1
        for _ in range(y1 - y0 - 2):
            cv.px(gx, gy, K("madera", 0)); gx += rnd.choice([-1, 0, 1]); gy += 1


def _suelo(cv, rnd, losa_nueva=False):
    cv.rect(X0, WB, X1, FB, K("madera", 0))
    for fila, y in enumerate(range(WB, FB, 14)):
        x = X0 - (fila % 3) * 9
        while x < X1:
            w = rnd.randint(18, 30)
            b = rnd.choice([1, 2, 2, 2, 3])
            cv.rect(max(X0, x + 1), y + 1, min(X1, x + w), min(FB, y + 14), K("madera", b))
            cv.hline(max(X0, x + 1), min(X1, x + w), y + 1, K("madera", b + 1))
            x += w
    P.manchas(cv, X0, WB, X1, FB, K("madera", 1), n=500, semilla=1303)
    for (x0, y0, x1, y1) in LAPIDAS:
        _lapida(cv, x0, y0, x1, y1, rnd)
    if losa_nueva:
        _lapida(cv, *LOSA_NUEVA, rnd, nueva=True)
    cv.rect(X0, WB, X1, WB + 3, K("madera", 0))                                    # sombra al pie del muro


def _alfombra(cv):
    """Una alfombra raída bajo la mesa: lo único blando de la cripta."""
    x0, y0, x1, y1 = MESA[0] - 26, MESA[1] - 6, MESA[2] + 26, MESA[3] + 14
    cv.rect(x0, y0, x1, y1, K("granate", 2)); cv.frame(x0, y0, x1, y1, K("granate", 1))
    cv.frame(x0 + 3, y0 + 3, x1 - 3, y1 - 3, K("ocre", 1))
    for x in range(x0 + 8, x1 - 8, 8):
        cv.px(x, y0 + 6, K("ocre", 1)); cv.px(x + 4, y1 - 7, K("ocre", 1))
    cv.poly([(x1 - 14, y1), (x1, y1 - 8), (x1, y1)], K("gris", 2))                 # esquina comida
    for x in range(x0, x1, 3):
        cv.px(x, y1, K("granate", 1))                                               # flecos


def _muros(cv):
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 2)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 2))
    cv.vline(X0 - 1, WT, FB, K("gris", 3)); cv.vline(X1, WT, FB, K("gris", 3))
    cv.rect(X0 - 12, FB, X1 + 12, FB + 12, K("gris", 2)); cv.hline(X0, X1, FB, K("gris", 3))


def _luz(cv):
    """Solo velas. −1 en todo, y cada vela suma pasos alrededor; resplandor ámbar encima."""
    cv.add_light(0, 0, W, H, -1)
    cv.add_light_fn(lambda x, y: -1 if (WB <= y < FB and X0 <= x < X1 and (x < X0 + 8 or x >= X1 - 8 or y >= FB - 8)) else 0)
    velas = list(VELAS)
    sala = (X0, WT, X1, FB)

    def pasos(x, y):
        if not (X0 <= x < X1 and WT - 12 <= y < FB):
            return 0
        best = 0
        for (vx, vy, alto) in velas:
            dx, dy = x - vx, (y - vy - 4) * 1.3
            d2 = dx * dx + dy * dy
            if d2 < 100:
                return 2
            if d2 < 900:
                best = 1
        return best
    cv.add_light_fn(pasos)
    cv.glow_rgb = K("ocre", 4)
    for (vx, vy, alto) in velas:
        cv.add_glow_suave(vx, vy + 4, 48, 0.2, squash=1.2, pasos=4,
                          limite=(max(X0, vx - 57), max(WT, vy - 50), min(X1, vx + 58), min(FB, vy + 56)))
    # resplandor general de la mesa (la sala vive alrededor de ella)
    cv.add_glow_suave((MESA[0] + MESA[2]) // 2, MESA[1] - 20, 230, 0.26, squash=1.1, pasos=8, limite=sala)
    cv.bake_lighting()
    for (vx, vy, alto) in velas:
        L.glow_post(cv, vx, vy, 7, 0.45, K("ocre", 4), limite=(vx - 8, vy - 8, vx + 9, vy + 9))
    # y un velo rojizo muy leve en los rincones, para que la sombra sea cálida y no gris
    L.glow_post(cv, (X0 + X1) // 2, (WT + FB) // 2, 320, 0.12, K("rojo", 1), squash=1.6, pasos=4, limite=sala,
                respetar_emisivos=True)


def dibujar(variante=None, extras=None, detras=None):
    VELAS.clear()
    rnd = random.Random(1303)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    _sillares(cv, X0, WT, X1, WB, rnd)
    _bovedas(cv, rnd)
    _suelo(cv, rnd, losa_nueva=(variante == "losa_nueva"))
    _alfombra(cv)
    _escalera_caracol(cv)
    _telefono(cv, rnd)
    _estanteria(cv, ESTANTE_IZQ, rnd)
    _estanteria(cv, ESTANTE_DER, rnd)
    _campanas(cv)
    # montones de libros y papeles por el suelo, con velas encima
    for (bx, by) in ((206, 104), (290, 112), (414, 116)):
        for k in range(4):
            c = rnd.choice([("granate", 3), ("madera", 4), ("rojo", 1), ("granate", 2), ("ocre", 1)])
            cv.rect(bx + k % 2, by - k * 3, bx + 14 - k % 2, by - k * 3 + 3, K(*c)); cv.hline(bx + k % 2, bx + 14 - k % 2, by - k * 3, K(c[0], c[1] + 1))
        vela(cv, bx + 6, by - 12, alto=4, grosor=2)
    if detras:
        detras(cv)
    # velas en el suelo: grupos sobre las lápidas y en los rincones
    for (gx, gy, n) in ((70, 136, 3), (112, 178, 2), (300, 150, 3), (384, 126, 2), (96, 222, 3), (420, 234, 2),
                        (250, 238, 2), (44, 122, 2)):
        grupo_velas(cv, gx, gy, rnd, n=n)
    _mesa(cv, rnd)
    _camastro(cv, rnd)
    # un orinal y una palangana junto al camastro; una estufilla apagada
    cv.ellipse(326, 214, 338, 220, K("papel", 1), outline=K("papel", 0)); cv.ellipse(328, 215, 336, 218, K("madera", 2))
    if extras:
        extras(cv)
    _muros(cv)
    _luz(cv)
    return cv
