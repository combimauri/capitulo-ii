"""J8.04 — El panel de llaves de la garita de la planta 11.

Un tablero de madera con doce ganchos de latón y el rótulo pintado de la garita; a la izquierda, la
telepantalla de la garita; a la derecha, el cuadrante de turnos y la gorra del guardia colgada; abajo,
el mostrador con el libro de firmas abierto. Las llaves y sus etiquetas son piezas aparte (las etiquetas
ya vienen inclinadas -6°, igual que su texto en el juego).

  llaves-fondo     480x270
  llaves-llave     hoja de 4 fotogramas de 16x28 (cuatro dentados distintos)
  llaves-etiqueta  50x20 (etiqueta de cartulina con ojal)
"""
import math
import random

from _base import Canvas, K, a_rgba, guardar, hoja, sprite, texto_escalado, ancho_escalado

W, H = 480, 270
TABLERO = (65, 40, 415, 240)
COLUMNAS = [120, 200, 280, 360]          # x del juego / 2  (240 + i·160)
FILAS = [85, 140, 195]                    # y del juego / 2  (170 + j·110)


def gancho_y(fy):
    """Punta del gancho, en el arte; la anilla de la llave cuelga justo debajo."""
    return fy - 12


def fondo():
    rnd = random.Random(8)
    cv = Canvas(W, H, bg=("pared", 2))
    # pared de la garita: papel a rayas, techo oscuro
    for x in range(0, W, 8):
        cv.vline(x, 0, H, K("pared", 1)); cv.vline(x + 4, 0, H, K("pared", 3))
    cv.rect(0, 0, W, 6, K("gris", 2)); cv.hline(0, W, 6, K("gris", 1))
    # telepantalla de la garita
    tx0, ty0, tx1, ty1 = 14, 70, 52, 98
    cv.rect(tx0 - 3, ty0 - 3, tx1 + 3, ty1 + 6, K("gris", 2)); cv.frame(tx0 - 3, ty0 - 3, tx1 + 3, ty1 + 6, K("gris", 1))
    cv.rect(tx0, ty0, tx1, ty1, K("tele", 2))
    cv.ellipse(tx0 + 11, ty0 + 3, tx1 - 11, ty1 - 3, K("tele", 3))
    cv.ellipse(tx0 + 15, ty0 + 10, tx1 - 15, ty0 + 18, K("tele", 6)); cv.ellipse(tx0 + 17, ty0 + 12, tx1 - 17, ty0 + 16, K("tele", 1))
    for y in range(ty0, ty1, 2):
        cv.hline(tx0, tx1, y, K("tele", 2) if y % 4 else K("tele", 3))
    cv.ellipse(tx0 + 11, ty0 + 3, tx1 - 11, ty1 - 3, None, outline=K("tele", 4))
    cv.ellipse(tx0 + 15, ty0 + 10, tx1 - 15, ty0 + 18, K("tele", 6)); cv.ellipse(tx0 + 17, ty0 + 12, tx1 - 17, ty0 + 16, K("tele", 1))
    cv.px(tx1, ty1 + 3, K("rojo", 4))
    cv.add_emissive(tx0, ty0, tx1, ty1)
    # cuadrante de turnos y gorra del guardia en su percha
    cv.rect(427, 64, 465, 112, K("gris", 1))
    cv.rect(425, 62, 463, 110, K("papel", 3)); cv.frame(425, 62, 463, 110, K("papel", 1))
    cv.text(429, 65, "TURNOS", K("gris", 2))
    for k in range(6):
        y = 73 + k * 6
        cv.hline(428, 460, y, K("papel", 1))
        cv.hline(429, 429 + rnd.randint(10, 18), y + 2, K("gris", 4))
        if k < 4:
            cv.px(456, y + 2, K("rojo", 3)); cv.px(457, y + 3, K("rojo", 3))
    cv.rect(442, 59, 446, 63, K("gris", 5))
    cv.rect(440, 132, 448, 136, K("ocre", 1)); cv.px(444, 137, K("ocre", 2))       # percha
    cv.ellipse(428, 136, 462, 150, K("gris", 1)); cv.rect(434, 128, 456, 142, K("gris", 2))
    cv.hline(434, 456, 128, K("gris", 3)); cv.rect(436, 138, 454, 141, K("gris", 0))
    cv.rect(443, 131, 447, 134, K("rojo", 3))                                       # insignia

    # el tablero
    x0, y0, x1, y1 = TABLERO
    cv.rect(x0 + 3, y0 + 3, x1 + 3, y1 + 3, K("pared", 0))                          # sombra 2-3 px
    cv.rect(x0, y0, x1, y1, K("madera", 1))
    cv.hline(x0, x1, y0, K("madera", 3)); cv.vline(x0, y0, y1, K("madera", 2))
    ix0, iy0, ix1, iy1 = x0 + 6, y0 + 6, x1 - 6, y1 - 6
    cv.rect(ix0, iy0, ix1, iy1, K("madera", 3))
    xx = ix0
    while xx < ix1:                                                                 # tablas verticales
        w = rnd.choice([28, 34, 40])
        cv.vline(xx, iy0, iy1, K("madera", 2))
        for _ in range(4):
            gy = rnd.randint(iy0 + 22, iy1 - 14)
            gx = xx + rnd.randint(4, max(4, w - 4))
            if gx < ix1 - 1:
                cv.vline(gx, gy, min(iy1, gy + rnd.randint(6, 16)), K("madera", 2))
        xx += w
    cv.hline(ix0, ix1, iy0, K("madera", 0)); cv.vline(ix0, iy0, iy1, K("madera", 0))
    cv.hline(ix0, ix1, iy1 - 1, K("madera", 4))
    # rótulo pintado
    cv.rect(ix0, iy0, ix1, iy0 + 18, K("madera", 1)); cv.hline(ix0, ix1, iy0 + 18, K("madera", 0))
    titulo = "GARITA   PLANTA 11"
    tw = ancho_escalado(titulo)
    texto_escalado(cv, 240 - tw // 2, iy0 + 4, titulo, K("papel", 3))
    pto = 240 - tw // 2 + ancho_escalado("GARITA ") + 1
    cv.rect(pto, iy0 + 8, pto + 2, iy0 + 10, K("papel", 3))                         # el punto medio
    # ganchos y cordeles
    for fy in FILAS:
        gy = gancho_y(fy)
        cv.hline(ix0 + 4, ix1 - 4, gy - 6, K("madera", 2))                         # listón
        cv.hline(ix0 + 4, ix1 - 4, gy - 5, K("madera", 4))
        for cx in COLUMNAS:
            cv.rect(cx - 3, gy - 4, cx + 4, gy + 1, K("ocre", 0))
            cv.rect(cx - 2, gy - 3, cx + 3, gy, K("ocre", 2)); cv.px(cx - 1, gy - 3, K("ocre", 4))
            cv.vline(cx, gy - 2, gy + 2, K("ocre", 3)); cv.px(cx + 1, gy + 1, K("ocre", 1))
            # cordel de la anilla a la etiqueta
            cv.d.line([(cx + 3, gy + 9), (cx + 3, gy + 21)], fill=K("papel", 1))
            # silueta pintada de la llave (se ve si falta)
            cv.rect(cx - 1, gy + 12, cx + 2, gy + 26, K("madera", 2))
    # mostrador con el libro de firmas
    cv.rect(0, 240, W, 246, K("madera", 4)); cv.hline(0, W, 240, K("madera", 6)); cv.hline(0, W, 245, K("madera", 2))
    cv.rect(0, 246, W, H, K("madera", 1)); cv.hline(0, W, 246, K("madera", 0))
    for x in range(0, W, 30):
        cv.vline(x, 247, H, K("madera", 0))
    bx = 30
    cv.rect(bx + 2, 232, bx + 52, 244, K("madera", 0))
    cv.rect(bx, 230, bx + 25, 242, K("papel", 3)); cv.rect(bx + 25, 230, bx + 50, 242, K("papel", 4))
    cv.vline(bx + 25, 230, 242, K("papel", 1)); cv.frame(bx - 1, 229, bx + 51, 243, K("granate", 2))
    for k in range(4):
        cv.hline(bx + 3, bx + 22, 233 + k * 2, K("gris", 6))
        cv.hline(bx + 28, bx + 28 + (18 if k < 3 else 9), 233 + k * 2, K("gris", 6))
    cv.d.line([(bx + 40, 240), (bx + 58, 236)], fill=K("gris", 1)); cv.px(bx + 40, 240, K("ocre", 3))
    cv.rect(420, 234, 432, 242, K("papel", 2)); cv.rect(421, 231, 431, 234, K("papel", 3))   # taza
    cv.rect(432, 236, 435, 240, K("papel", 2)); cv.hline(422, 430, 232, K("madera", 1))

    # luz: fluorescente fría arriba, la telepantalla tiñe de verde el lado izquierdo
    cv.add_light_fn(lambda x, y: -1 if y > 250 else 0)
    cv.glow_rgb = K("tele", 4)
    cv.add_glow_suave(33, 84, 130, 0.22, squash=1.2)
    cv.bake_lighting()
    return cv.img


def _llave(variante):
    cv = sprite(16, 28)
    acero = variante == 3
    R = (lambda i: K("gris", i + 4)) if acero else (lambda i: K("ocre", i))
    # anilla
    cv.ellipse(3, 0, 14, 11, R(0))
    cv.ellipse(4, 1, 13, 10, R(2))
    cv.px(5, 3, R(4)); cv.px(6, 2, R(4)); cv.px(6, 3, R(3))
    cv.ellipse(6, 3, 11, 8, (255, 0, 255), outline=R(0))
    cv.px(11, 8, R(1)); cv.px(12, 7, R(1))
    # cuello y caña
    cv.rect(6, 10, 11, 13, R(0)); cv.rect(7, 11, 10, 12, R(3))
    cv.rect(7, 13, 10, 27, R(0)); cv.vline(8, 13, 26, R(3)); cv.px(9, 26, R(1))
    # dentado: cuatro llaves distintas
    dientes = [[(15, 3), (18, 2), (21, 4)], [(14, 2), (17, 4), (20, 2), (23, 3)],
               [(16, 4), (20, 3)], [(15, 2), (18, 3), (21, 2), (24, 4)]][variante]
    for (yy, prof) in dientes:
        cv.rect(7 - prof, yy, 7, yy + 2, R(0)); cv.hline(8 - prof, 7, yy, R(2))
    return a_rgba(cv)


def llave():
    return hoja([_llave(v) for v in range(4)])


def etiqueta():
    """Etiqueta de 46x13 inclinada -6°, en un lienzo de 50x20 (el juego la centra en x+46, y+10)."""
    cv = sprite(50, 20)
    a = math.radians(-6)
    cx, cy = 24.5, 9.5

    def rot(dx, dy):
        return (cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a))

    esq = [rot(-23, -6.5), rot(23, -6.5), rot(23, 6.5), rot(-23, 6.5)]
    cv.poly([(x + 1, y + 2) for x, y in esq], K("madera", 0))                       # sombra sobre el tablero
    cv.poly(esq, K("papel", 4))
    cv.d.polygon(esq, outline=K("papel", 1))
    cv.d.line([rot(-23, 5.5), rot(23, 5.5)], fill=K("papel", 3))
    ox, oy = rot(-20, 0)
    cv.ellipse(round(ox) - 2, round(oy) - 2, round(ox) + 3, round(oy) + 3, K("papel", 2))
    cv.px(round(ox), round(oy), K("madera", 1))
    return a_rgba(cv)


def exportar(destino):
    return [guardar(fondo(), destino, "llaves-fondo"), guardar(llave(), destino, "llaves-llave"),
            guardar(etiqueta(), destino, "llaves-etiqueta")]
