"""J2.06 — Sueño: una calle sin bombardear, en sepia. Ivy niña salta a la comba al fondo (960x270)."""
import random

from pixel import Canvas, K
import props as P

W, H = 960, 270
FACHADA = 110


def dibujar():
    rnd = random.Random(1979)
    cv = Canvas(W, H, bg=("papel", 1))
    for i, y in enumerate(range(0, 50, 10)):
        cv.rect(0, y, W, y + 10, K("papel", 4 - i // 2))
    # casas obreras intactas, como la calle Stepney antes del cohete
    for i, x in enumerate(range(0, W, 64)):
        top = 22 + (i % 3) * 4
        cv.rect(x, top, x + 64, FACHADA, K("madera", 3))
        for y in range(top + 4, FACHADA, 4):
            cv.hline(x, x + 64, y, K("madera", 2))
        cv.rect(x - 1, top - 4, x + 65, top, K("madera", 1))
        for wx in (x + 10, x + 38):
            cv.rect(wx, top + 12, wx + 14, top + 30, K("papel", 3)); cv.frame(wx - 1, top + 11, wx + 15, top + 31, K("madera", 1))
            cv.vline(wx + 7, top + 12, top + 30, K("madera", 1))
            if rnd.random() < 0.5:
                cv.rect(wx + 1, top + 13, wx + 6, top + 29, K("granate", 4))     # cortinas
        cv.rect(x + 24, FACHADA - 26, x + 38, FACHADA, K("madera", 1))
        if rnd.random() < 0.4:
            cv.rect(x + 22, FACHADA - 4, x + 40, FACHADA, K("ocre", 2))          # escalón fregado
    # acera y adoquines en sepia
    cv.rect(0, FACHADA, W, FACHADA + 8, K("papel", 2)); cv.hline(0, W, FACHADA + 8, K("madera", 2))
    P.adoquines(cv, 0, FACHADA + 9, W, H, semilla=6, rampa="madera", base=3)
    for fx in (120, 400, 680):
        P.farola(cv, fx, 160)
    # ropa tendida entre casas
    for (x0, x1) in ((250, 330), (560, 640)):
        cv.d.line([(x0, 60), (x1, 64)], fill=K("madera", 1))
        for k in range(x0 + 6, x1 - 6, 14):
            cv.rect(k, 62, k + 8, 74, K("papel", 4 if k % 3 else 2))
    # bruma en los bordes: el sueño se desvanece
    for y in range(H):
        for x in list(range(0, 40)) + list(range(W - 40, W)):
            d = min(x, W - 1 - x)
            if rnd.random() > d / 40:
                cv.px(x, y, K("papel", 3))
    cv.bake_lighting()
    return cv
