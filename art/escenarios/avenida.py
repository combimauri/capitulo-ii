"""J1.03 — Avenida de la Victoria hasta la puerta del Minipax (960x270, la cámara sigue al jugador).

Variante "furgoneta": una furgoneta negra aparcada junto al bordillo, delante del portal de las
Mansiones Victoria, y cajas con las pertenencias de alguien apiladas en la acera.
"""
import random

from pixel import Canvas, K
import props as P

W, H = 960, 270
FACHADA, ACERA, CALZADA = 112, 200, 270


def _edificio(cv, x, w, top, rnd):
    cv.rect(x, top, x + w, FACHADA, K("gris", 4))
    cv.rect(x, top, x + w, top + 4, K("gris", 3))
    for wy in range(top + 10, FACHADA - 26, 18):
        for wx in range(x + 8, x + w - 12, 18):
            luz = rnd.random() < 0.08
            cv.rect(wx, wy, wx + 10, wy + 12, K("ocre", 2) if luz else K("gris", 1))
            cv.hline(wx, wx + 10, wy + 12, K("gris", 6))
    for _ in range(40):
        cv.px(rnd.randint(x, x + w - 1), rnd.randint(top, FACHADA - 1), K("gris", 3))


# huella en el suelo de la furgoneta (variante "furgoneta"): x0, y0, x1, y1
FURGONETA = (26, 212, 128, 236)
CAJAS = (62, 114, 106, 136)


def _furgoneta(cv, x0, y0, x1, y1):
    """Furgoneta negra vista de lado en 3/4: techo, costado, ruedas. (x0..x1, y0..y1) es la huella."""
    fondo = y1 - y0                                       # la anchura del vehículo vista desde arriba
    alto = 30
    ys = y1 - alto                                        # arista superior del costado
    yt = ys - fondo                                       # borde trasero del techo
    cv.rect(x0 + 4, y1 - 2, x1 + 5, y1 + 4, K("gris", 0))                     # sombra en la calzada
    # techo
    cv.rect(x0 + 1, yt, x1 - 18, ys, K("gris", 3)); cv.hline(x0 + 1, x1 - 18, yt, K("gris", 5))
    cv.vline(x0, yt + 1, ys, K("gris", 1))
    for k in range(x0 + 10, x1 - 22, 14):                                     # nervios del techo
        cv.vline(k, yt + 2, ys - 1, K("gris", 2))
    # cabina más baja delante (derecha)
    cv.poly([(x1 - 18, yt + 6), (x1 - 6, yt + 8), (x1, ys + 6), (x1 - 18, ys)], K("gris", 2))
    cv.poly([(x1 - 16, yt + 8), (x1 - 7, yt + 10), (x1 - 3, ys + 2), (x1 - 16, ys - 1)], K("cielo", 1))   # parabrisas
    cv.d.line([(x1 - 15, yt + 10), (x1 - 9, ys - 3)], fill=K("cielo", 3))
    # costado
    cv.rect(x0, ys, x1, y1 - 5, K("gris", 1)); cv.hline(x0, x1, ys, K("gris", 4))
    cv.rect(x1 - 4, ys + 6, x1, y1 - 7, K("gris", 2))                         # morro
    cv.rect(x1 - 2, ys + 10, x1 + 1, ys + 13, K("papel", 2))                  # faro apagado
    cv.rect(x0 + 2, ys + 3, x0 + 14, ys + 9, K("gris", 0))                    # ventanuco trasero enrejado
    for k in range(x0 + 4, x0 + 14, 3):
        cv.vline(k, ys + 3, ys + 9, K("gris", 3))
    cv.vline(x0 + 22, ys + 1, y1 - 6, K("gris", 0))                           # puerta corredera
    cv.vline(x1 - 22, ys + 1, y1 - 6, K("gris", 0))
    cv.rect(x1 - 19, ys + 3, x1 - 6, ys + 11, K("cielo", 1)); cv.hline(x1 - 19, x1 - 6, ys + 3, K("cielo", 3))   # ventanilla
    cv.hline(x1 - 20, x1 - 16, ys + 15, K("gris", 4))                         # manilla
    cv.hline(x0 + 26, x1 - 24, y1 - 9, K("gris", 2))                          # moldura
    cv.rect(x0, y1 - 6, x1, y1 - 4, K("gris", 0))                             # bajos
    # ruedas
    for wx in (x0 + 14, x1 - 20):
        cv.ellipse(wx - 9, y1 - 13, wx + 9, y1 + 1, K("gris", 0))                # paso de rueda
        cv.ellipse(wx - 7, y1 - 10, wx + 7, y1 + 3, K("gris", 1), outline=K("gris", 0))
        cv.ellipse(wx - 3, y1 - 6, wx + 3, y1, K("gris", 4)); cv.px(wx - 1, y1 - 5, K("gris", 6))
    # ni matrícula ni rótulo: solo un número pequeño sobre la puerta
    cv.text(x0 + 40, ys + 4, "17", K("gris", 3))


def _cajas(cv, x0, y0, x1, y1):
    """Cajas de cartón y un baúl con las pertenencias de alguien, apiladas contra la fachada."""
    cv.rect(x0 + 3, y1 - 3, x1 + 3, y1 + 2, K("gris", 4))                     # sombra
    # baúl de madera (abajo)
    cv.rect(x0, y1 - 14, x0 + 26, y1, K("madera", 3)); cv.rect(x0, y1 - 18, x0 + 26, y1 - 14, K("madera", 5))
    cv.frame(x0, y1 - 18, x0 + 26, y1, K("madera", 1)); cv.hline(x0, x0 + 26, y1 - 14, K("madera", 1))
    cv.rect(x0 + 11, y1 - 12, x0 + 15, y1 - 9, K("ocre", 3))
    # cajas de cartón (papel oscuro)
    for (bx, by, bw, bh) in [(x0 + 24, y1 - 16, 20, 16), (x0 + 3, y1 - 32, 18, 14), (x0 + 26, y1 - 30, 16, 14)]:
        cv.rect(bx, by + 4, bx + bw, by + bh, K("papel", 1)); cv.rect(bx, by, bx + bw, by + 4, K("papel", 2))
        cv.frame(bx, by, bx + bw, by + bh, K("papel", 0)); cv.vline(bx + bw // 2, by, by + 4, K("papel", 0))
    # lo que asoma: libros, una lámpara, un marco de foto boca abajo
    cv.rect(x0 + 6, y1 - 35, x0 + 10, y1 - 31, K("granate", 3)); cv.rect(x0 + 11, y1 - 34, x0 + 15, y1 - 31, K("azul", 2))
    cv.rect(x0 + 29, y1 - 33, x0 + 39, y1 - 30, K("papel", 4)); cv.hline(x0 + 30, x0 + 38, y1 - 32, K("gris", 6))   # papeles
    cv.rect(x0 + 28, y1 - 20, x0 + 38, y1 - 16, K("madera", 2))
    # un papel caído en la acera
    cv.rect(x1 + 2, y1 - 6, x1 + 10, y1, K("papel", 4)); cv.hline(x1 + 4, x1 + 9, y1 - 4, K("gris", 6))


def dibujar(variante=None):
    rnd = random.Random(1984)
    cv = Canvas(W, H)
    # cielo gris de la mañana
    for i, y in enumerate(range(0, 60, 10)):
        cv.rect(0, y, W, y + 10, K("cielo", 4 + i // 3))
    # pirámide del Minipax al fondo, a la derecha, creciendo sobre los tejados
    pcx = 860
    for i, w2 in enumerate([90, 74, 58, 42, 28, 14]):
        top = 104 - (i + 1) * 16
        cv.rect(pcx - w2, top, pcx + w2, top + 16, K("papel", 4 if i % 2 == 0 else 3))
        cv.hline(pcx - w2, pcx + w2, top + 15, K("papel", 1))
    # edificios del centro
    x = 0
    while x < 760:
        w = rnd.randint(70, 120)
        _edificio(cv, x, w, rnd.randint(20, 46), rnd)
        x += w
    # muro blanco del Minipax con alambre de espino y la puerta
    cv.rect(760, 70, W, FACHADA, K("papel", 3)); cv.hline(760, W, 70, K("papel", 4))
    for xx in range(762, W, 6):
        cv.px(xx, 67, K("gris", 2)); cv.px(xx + 3, 68, K("gris", 2)); cv.px(xx + 1, 66, K("gris", 3))
    cv.rect(856, 74, 904, FACHADA, K("gris", 2)); cv.rect(860, 78, 900, FACHADA, K("gris", 1))
    cv.text(880 - cv.text_width("MINIPAX") // 2, 84, "MINIPAX", K("papel", 4))
    # carteles: Gran Hermano y consignas
    for cx in (60, 230, 420, 600):
        P.cartel_gran_hermano(cv, cx, 52, w=40, h=46)
    P.cartel_consignas(cv, 296, 50, w=84, h=42)
    # portal de las Mansiones Victoria
    P.puerta(cv, 24, 66, w=30, h=46, numero="MV")
    # acera de losas
    P.baldosas(cv, 0, FACHADA, W, ACERA, K("gris", 5), K("gris", 6), t=16, linea=K("gris", 4))
    P.manchas(cv, 0, FACHADA, W, ACERA, K("gris", 4), n=500, semilla=4)
    cv.rect(0, ACERA, W, ACERA + 4, K("gris", 3)); cv.hline(0, W, ACERA, K("gris", 7))   # bordillo
    # calzada
    cv.rect(0, ACERA + 4, W, CALZADA, K("gris", 2))
    for xx in range(0, W, 48):
        cv.rect(xx, 238, xx + 24, 241, K("papel", 2))
    # puesto prole (lotería y cordones)
    cv.rect(500, 124, 560, 150, K("madera", 3)); cv.rect(498, 118, 562, 126, K("granate", 4))
    for xx in range(500, 562, 8):
        cv.rect(xx, 118, xx + 4, 126, K("papel", 3))
    for i in range(6):
        cv.vline(506 + i * 8, 130, 146, K("papel", 2 + i % 2))
    # farolas
    for fx in (150, 380, 640):
        P.farola(cv, fx, 186)
    # helicóptero de la Patrulla sobre los edificios
    hx, hy = 470, 20
    cv.rect(hx, hy, hx + 22, hy + 8, K("gris", 1)); cv.rect(hx + 22, hy + 3, hx + 38, hy + 5, K("gris", 1))
    cv.hline(hx - 8, hx + 30, hy - 2, K("gris", 0)); cv.rect(hx + 4, hy + 2, hx + 10, hy + 6, K("cielo", 5))
    if variante == "furgoneta":
        _cajas(cv, *CAJAS)
        _furgoneta(cv, *FURGONETA)
    # sombra suave a pie de fachada
    cv.add_light(0, FACHADA, W, FACHADA + 8, -1)
    cv.bake_lighting()
    return cv
