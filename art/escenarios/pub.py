"""J4.08 — Pub «La Campana»: humo, barra gastada, dardos y una campana de barco sobre la barra."""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 20, 88, 246


def jarra(cv, x, y):
    cv.rect(x, y, x + 4, y + 6, K("ocre", 3)); cv.hline(x, x + 4, y, K("papel", 4)); cv.vline(x + 5, y + 2, y + 4, K("ocre", 2))


def dibujar():
    rnd = random.Random(77)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    P.papel_pintado(cv, X0, WT, X1, WB, rampa="granate", base=2, motivo="rayas")              # papel pintado viejo
    cv.rect(X0, WT, X1, 40, K("granate", 1))
    # estantes con botellas detrás de la barra
    for sy in (44, 60):
        cv.rect(60, sy, 230, sy + 2, K("madera", 3))
        for bx in range(64, 228, 9):
            c = rnd.choice([K("tele", 2), K("granate", 3), K("ocre", 2), K("cielo", 3)])
            cv.rect(bx, sy - 9, bx + 4, sy, c); cv.px(bx + 1, sy - 8, K("papel", 3))
    # la campana de barco sobre la barra
    cv.hline(140, 156, 24, K("gris", 2)); cv.vline(148, 24, 30, K("gris", 2))
    cv.poly([(141, 40), (144, 30), (152, 30), (155, 40)], K("ocre", 3)); cv.hline(140, 156, 40, K("ocre", 1))
    cv.px(146, 33, K("ocre", 4)); cv.px(148, 42, K("ocre", 2))
    # diana de dardos
    cv.ellipse(300, 38, 326, 64, K("gris", 1)); cv.ellipse(304, 42, 322, 60, K("papel", 2)); cv.ellipse(309, 47, 317, 55, K("rojo", 3))
    cv.px(313, 51, K("gris", 0)); cv.d.line([(318, 44), (322, 41)], fill=K("ocre", 3))
    cv.rect(380, 36, 416, 60, K("papel", 2)); cv.text(384, 40, "LOTERIA", K("granate", 2))           # pizarra de la lotería
    for k in range(3):
        cv.hline(384, 412, 48 + k * 4, K("gris", 4))
    P.zocalo(cv, X0, X1, WB, rampa="madera", base=1)
    P.tablones(cv, X0, WB, X1, FB, rampa="madera", base=2, semilla=9)
    # la barra
    cv.rect(52, 96, 240, 118, K("madera", 3)); cv.hline(52, 240, 96, K("madera", 4))
    cv.rect(52, 118, 240, 128, K("madera", 1))
    for jx in (70, 120, 176, 214):
        jarra(cv, jx, 98)
    for tx in (80, 130, 180, 226):                                                        # taburetes
        cv.ellipse(tx - 6, 134, tx + 6, 140, K("madera", 2)); cv.vline(tx, 140, 150, K("madera", 1))
    # mesas
    for (mx, my) in [(290, 120), (370, 120), (300, 190)]:
        cv.ellipse(mx - 2, my + 18, mx + 42, my + 26, K("gris", 1))
        cv.ellipse(mx, my, mx + 40, my + 18, K("madera", 3), outline=K("madera", 1))
        jarra(cv, mx + 10, my + 4); jarra(cv, mx + 26, my + 6)
    # muros y puerta
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, 224, FB + 12, K("gris", 3)); cv.rect(256, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(224, FB, 256, FB + 12, K("madera", 2))
    # luz cálida de taberna y humo de tabaco
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(150, 90, 150, 0.28, squash=1.3, limite=(X0, WT, X1, FB))
    cv.add_glow_suave(340, 140, 110, 0.18, squash=1.3, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    for _ in range(900):
        x, y = rnd.randint(X0, X1), rnd.randint(WT, 120)
        if rnd.random() < 0.5:
            cv.px(x, y, K("gris", 6))
    return cv
