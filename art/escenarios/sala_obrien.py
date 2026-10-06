"""FC.03 / FD.04 — Ministerio del Amor: la sala de O'Brien.

Sala blanca, luz plana, sin sombras. En el centro, una camilla de metal con correas; de su cabecera
sale un cable que corre por el suelo hasta la pared, bajo un dial enorme graduado del 1 al 100
(semicírculo con aguja, en reposo). A la derecha, una mesa de acero con lo que O'Brien va a usar:
una grabadora de bobinas, un paño doblado, el reloj de Ivy, un lápiz, un vaso de agua.
Solo blancos y grises: la amenaza está en la escala del dial, no en el color.
"""
import math

from pixel import Canvas, K

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 20, 92, 246
ENTRADA = (224, 256)
CAMILLA = (180, 120, 300, 170)                       # huellas en el suelo (colisiones)
DIAL = (320, 26, 400, 90)
MESA = (330, 150, 420, 180)

BLANCO, BLANCO2, JUNTA, FILO = K("gris", 10), K("papel", 4), K("gris", 9), K("gris", 8)


def _tapa(cv, x0, y0, x1, y1):
    cv.rect(x0, y0, x1, y1, K("gris", 9)); cv.hline(x0, x1, y0, BLANCO)


def _dial(cv, x0, y0, x1, y1, valor=4):
    """Dial graduado del 1 al 100: panel blanco, arco con marcas y una aguja."""
    cv.rect(x0 + 2, y0 + 2, x1 + 2, y1 + 2, K("gris", 8))                               # resalte de 2 px (no sombra)
    cv.rect(x0, y0, x1, y1, K("gris", 7)); cv.frame(x0, y0, x1, y1, K("gris", 5))
    cv.rect(x0 + 3, y0 + 3, x1 - 3, y1 - 3, BLANCO2); cv.frame(x0 + 3, y0 + 3, x1 - 3, y1 - 3, K("gris", 6))
    for (sx, sy) in [(x0 + 1, y0 + 1), (x1 - 2, y0 + 1), (x0 + 1, y1 - 2), (x1 - 2, y1 - 2)]:
        cv.px(sx, sy, K("gris", 9))                                                     # tornillos
    cx, cy = (x0 + x1) // 2, y1 - 14
    r = 30
    # banda de la escala, píxel a píxel: cuanto más alto el valor, más oscura (sin rojo: es el Minimor)
    for y in range(cy - r, cy + 1):
        for x in range(cx - r, cx + r + 1):
            d = math.hypot(x - cx, y - cy)
            if r - 5 <= d <= r:
                v = 100 * (math.pi - math.atan2(cy - y, x - cx)) / math.pi
                tono = 8 if v < 40 else 7 if v < 60 else 5 if v < 80 else 3 if v < 92 else 1
                cv.px(x, y, K("gris", tono))
    # marcas cada 10 (largas) y cada 5 (cortas)
    for v in range(0, 101, 5):
        a = math.pi - math.pi * v / 100
        largo = 9 if v % 10 == 0 else 7
        cv.d.line([(round(cx + (r - largo) * math.cos(a)), round(cy - (r - largo) * math.sin(a))),
                   (round(cx + (r - 6) * math.cos(a)), round(cy - (r - 6) * math.sin(a)))], fill=K("gris", 3))
    # cifras: el 1 y el 100 bajo los extremos del arco, el 50 arriba
    cv.text(cx - r + 1, cy + 3, "1", K("gris", 3))
    cv.text(cx + r - cv.text_width("100") + 1, cy + 3, "100", K("gris", 3))
    cv.text(cx - cv.text_width("50") // 2, cy - r + 9, "50", K("gris", 3))
    # aguja (en reposo, casi en el 1) y eje
    a = math.pi - math.pi * max(1, valor) / 100
    cv.d.line([(cx, cy), (round(cx + (r - 3) * math.cos(a)), round(cy - (r - 3) * math.sin(a)))], fill=K("gris", 1), width=2)
    cv.ellipse(cx - 3, cy - 3, cx + 4, cy + 4, K("gris", 1)); cv.px(cx, cy, K("gris", 6))


def _correa(cv, x, y_top, y_bot, ancho=4):
    cv.rect(x, y_top, x + ancho, y_bot, K("gris", 4)); cv.vline(x, y_top, y_bot, K("gris", 3))
    cv.vline(x + ancho - 1, y_top, y_bot, K("gris", 5))
    cv.rect(x - 1, y_top + 9, x + ancho + 1, y_top + 14, K("gris", 7)); cv.rect(x + 1, y_top + 10, x + ancho - 1, y_top + 13, K("gris", 4))


def _camilla(cv, x0, y0, x1, y1):
    alto = 14                                                                           # altura aparente del tablero
    t0, t1 = y0 - alto + 4, y1 - alto
    # patas y travesaño (dentro de la huella)
    for lx in (x0 + 4, x1 - 8):
        cv.rect(lx, t1 + 4, lx + 4, y1, K("gris", 6)); cv.vline(lx, t1 + 4, y1, K("gris", 8))
        cv.rect(lx - 1, y1 - 2, lx + 5, y1, K("gris", 4))                               # ruedas bloqueadas
    cv.hline(x0 + 8, x1 - 8, y1 - 6, K("gris", 6))
    # canto del tablero
    cv.rect(x0, t1, x1, t1 + 5, K("gris", 6)); cv.hline(x0, x1, t1 + 4, K("gris", 4))
    # tablero de acero y colchoneta fina
    cv.rect(x0, t0, x1, t1, K("gris", 8)); cv.frame(x0, t0, x1, t1, K("gris", 5))
    cv.rect(x0 + 3, t0 + 3, x1 - 3, t1 - 2, K("gris", 9)); cv.hline(x0 + 3, x1 - 3, t0 + 3, BLANCO)
    cv.rect(x1 - 24, t0 + 6, x1 - 5, t1 - 5, BLANCO2); cv.frame(x1 - 24, t0 + 6, x1 - 5, t1 - 5, K("gris", 8))   # cabecera
    # electrodos en la cabecera, unidos al cable que llega de la pared
    for (ex, ey) in ((x1 - 14, t0 + 9), (x1 - 14, t1 - 11)):
        cv.rect(ex, ey, ex + 5, ey + 4, K("gris", 4)); cv.px(ex + 2, ey + 1, K("gris", 8))
        cv.hline(ex + 5, x1, ey + 2, K("gris", 3))
    # correas: tobillos, rodillas, muñecas, pecho, frente
    for fx in (x0 + 12, x0 + 34, x0 + 58, x0 + 80, x1 - 20):
        _correa(cv, fx, t0 - 1, t1 + 5)


def _mesa(cv, x0, y0, x1, y1):
    alto = 12
    t0, t1 = y0 - alto + 2, y1 - alto
    for lx in (x0 + 2, x1 - 5):
        cv.rect(lx, t1 + 4, lx + 3, y1, K("gris", 6))
    cv.rect(x0, t1, x1, t1 + 4, K("gris", 6)); cv.hline(x0, x1, t1 + 3, K("gris", 4))
    cv.rect(x0, t0, x1, t1, K("gris", 8)); cv.frame(x0, t0, x1, t1, K("gris", 5)); cv.hline(x0 + 1, x1 - 1, t0 + 1, K("gris", 9))
    # grabadora de bobinas
    gx, gy = x0 + 5, t0 + 3
    cv.rect(gx, gy, gx + 34, gy + 18, K("gris", 3)); cv.frame(gx, gy, gx + 34, gy + 18, K("gris", 1))
    cv.hline(gx + 1, gx + 33, gy + 1, K("gris", 5))
    for bx in (gx + 3, gx + 19):
        cv.ellipse(bx, gy + 2, bx + 12, gy + 12, K("gris", 6), outline=K("gris", 1))
        cv.ellipse(bx + 3, gy + 5, bx + 9, gy + 10, K("gris", 2)); cv.px(bx + 6, gy + 7, K("gris", 8))
    cv.hline(gx + 9, gx + 25, gy + 11, K("gris", 7))                                    # la cinta entre bobinas
    for k in range(4):
        cv.rect(gx + 4 + k * 7, gy + 14, gx + 9 + k * 7, gy + 16, K("gris", 8 if k else 9))   # teclas
    # paño doblado
    px_ = x0 + 44
    cv.rect(px_, t0 + 4, px_ + 16, t0 + 13, BLANCO2); cv.frame(px_, t0 + 4, px_ + 16, t0 + 13, K("papel", 2))
    cv.hline(px_ + 1, px_ + 15, t0 + 8, K("papel", 3)); cv.px(px_ + 15, t0 + 12, K("papel", 2))
    # el reloj de Ivy, boca arriba, con la correa abierta
    rx = x0 + 64
    cv.rect(rx - 4, t0 + 7, rx + 13, t0 + 9, K("madera", 2))
    cv.ellipse(rx, t0 + 4, rx + 9, t0 + 13, K("papel", 3), outline=K("gris", 3))
    cv.px(rx + 4, t0 + 8, K("gris", 1)); cv.px(rx + 4, t0 + 7, K("gris", 1)); cv.px(rx + 3, t0 + 8, K("gris", 1))
    # lápiz y vaso de agua
    cv.d.line([(x0 + 48, t0 + 17), (x0 + 60, t0 + 15)], fill=K("ocre", 2)); cv.px(x0 + 61, t0 + 15, K("gris", 2))
    vx = x0 + 79
    cv.rect(vx, t0 + 4, vx + 6, t0 + 14, K("gris", 9)); cv.frame(vx, t0 + 4, vx + 6, t0 + 14, K("gris", 6))
    cv.hline(vx + 1, vx + 5, t0 + 7, K("cielo", 6)); cv.vline(vx + 1, t0 + 8, t0 + 13, BLANCO)


def dibujar(variante=None):
    cv = Canvas(W, H, bg=("gris", 8))
    _tapa(cv, X0 - 12, WT - 12, X1 + 12, WT)
    for fx in (120, 240, 360):                                                           # fluorescentes, sin halo
        cv.rect(fx - 30, WT - 9, fx + 30, WT - 3, K("gris", 8)); cv.rect(fx - 28, WT - 8, fx + 28, WT - 4, BLANCO)
    # pared de azulejo
    cv.rect(X0, WT, X1, WB, BLANCO)
    for y in range(WT, WB, 8):
        cv.hline(X0, X1, y, JUNTA)
    for x in range(X0, X1, 8):
        cv.vline(x, WT, WB, JUNTA)
    _dial(cv, *DIAL)
    # caja de conexiones bajo el dial, con el cable que baja al suelo
    cv.rect(352, 92 - 10, 368, 92 - 2, K("gris", 7)); cv.frame(352, 92 - 10, 368, 92 - 2, K("gris", 5))
    cv.vline(360, 90, 99, K("gris", 3))
    # reloj de pared (sin agujas, como en la recepción) y un interruptor
    cv.ellipse(222, 32, 240, 50, BLANCO2, outline=K("gris", 6))
    for (hx, hy) in [(231, 34), (238, 41), (231, 47), (224, 41)]:
        cv.px(hx, hy, K("gris", 6))
    # un espejo de observación: detrás, alguien mira (y no se ve a nadie)
    cv.rect(70, 34, 160, 70, K("gris", 6)); cv.frame(70, 34, 160, 70, K("gris", 5))
    cv.rect(73, 37, 157, 67, K("gris", 3))
    for k in range(3):
        cv.d.line([(80 + k * 6, 66), (100 + k * 6, 38)], fill=K("gris", 4))
    cv.d.line([(124, 66), (138, 46)], fill=K("gris", 4))
    cv.hline(73, 157, 37, K("gris", 2))
    cv.rect(X0, WB - 3, X1, WB, K("gris", 9))                                            # zócalo
    # suelo blanco
    cv.rect(X0, WB, X1, FB, BLANCO)
    for y in range(WB, FB, 24):
        cv.hline(X0, X1, y, JUNTA)
    for x in range(X0, X1, 24):
        cv.vline(x, WB, FB, JUNTA)
    cv.rect(234, 196, 246, 204, K("gris", 8))                                            # desagüe
    for k in range(235, 246, 2):
        cv.vline(k, 197, 203, K("gris", 6))
    # el cable: de la pared, bajo el dial, hasta la cabecera de la camilla (plano, por el suelo)
    cv.vline(360, 99, 112, K("gris", 3)); cv.vline(361, 99, 111, K("gris", 3))
    cv.px(359, 112, K("gris", 3)); cv.hline(304, 359, 113, K("gris", 3)); cv.hline(304, 359, 114, K("gris", 3))
    cv.px(303, 114, K("gris", 3)); cv.vline(302, 115, 120, K("gris", 3)); cv.vline(301, 115, 120, K("gris", 3))
    _camilla(cv, *CAMILLA)
    _mesa(cv, *MESA)
    # muros laterales e inferior, con la entrada
    a, b = ENTRADA
    _tapa(cv, X0 - 12, WT, X0, FB + 12); _tapa(cv, X1, WT, X1 + 12, FB + 12)
    _tapa(cv, X0 - 12, FB, a, FB + 12); _tapa(cv, b, FB, X1 + 12, FB + 12)
    cv.rect(a, FB, b, H, BLANCO)
    for y in range(FB, H, 24):
        cv.hline(a, b, y, JUNTA)
    cv.vline(a, FB, H, K("gris", 8)); cv.vline(b - 1, FB, H, K("gris", 8))
    cv.bake_lighting()                                                                   # luz plana
    return cv
