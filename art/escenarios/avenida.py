"""J1.03 — Avenida de la Victoria hasta la puerta del Minipax (960x270, la cámara sigue al jugador)."""
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


def dibujar():
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
    # sombra suave a pie de fachada
    cv.add_light(0, FACHADA, W, FACHADA + 8, -1)
    cv.bake_lighting()
    return cv
