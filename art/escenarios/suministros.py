"""J7.03 — Cuarto de suministros: estrecho, sin ventanas, una bombilla desnuda.
Donde hubo una telepantalla, un hueco cuadrado tapado con una tabla: el único ángulo muerto de la planta."""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 120, 360
WT, WB, FB = 24, 92, 230


def balda(cv, x, y, w, rnd, cosas):
    cv.rect(x, y, x + w, y + 3, K("madera", 3)); cv.hline(x, x + w, y + 3, K("madera", 1))
    k = x + 3
    while k < x + w - 10:
        c = rnd.choice(cosas)
        if c == "papel":
            cv.rect(k, y - 9, k + 12, y, K("papel", 3)); cv.hline(k, k + 12, y - 5, K("papel", 1)); k += 14
        elif c == "cinta":
            cv.ellipse(k, y - 7, k + 7, y, K("gris", 1), outline=K("gris", 4)); cv.px(k + 3, y - 4, K("rojo", 3)); k += 9
        elif c == "tinta":
            cv.rect(k, y - 8, k + 5, y, K("azul", 1)); cv.rect(k + 1, y - 10, k + 4, y - 8, K("gris", 2)); k += 7
        elif c == "chinchetas":
            cv.rect(k, y - 8, k + 7, y, K("cielo", 6)); cv.px(k + 2, y - 4, K("gris", 0)); cv.px(k + 4, y - 3, K("gris", 0)); k += 9
        else:
            cv.rect(k, y - 6, k + 14, y, K("ocre", 2)); cv.hline(k, k + 14, y - 6, K("ocre", 3)); k += 16


def dibujar():
    rnd = random.Random(7)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    P.papel_pintado(cv, X0, WT, X1, WB, rampa="pared", base=1, motivo="rayas")
    # el hueco de la telepantalla, tapado con una tabla
    cv.rect(220, 34, 262, 62, K("gris", 1)); cv.rect(222, 36, 260, 60, K("madera", 2))
    for k in (40, 48, 56):
        cv.hline(222, 260, k, K("madera", 1))
    cv.px(224, 38, K("gris", 6)); cv.px(258, 38, K("gris", 6)); cv.px(224, 58, K("gris", 6)); cv.px(258, 58, K("gris", 6))
    # estanterías a ambos lados (la tercera balda: cintas)
    for (ex, ew) in ((126, 82), (276, 80)):
        cv.rect(ex, 26, ex + ew, WB, K("madera", 1))
        for i, by in enumerate((40, 58, 76, 90)):
            balda(cv, ex + 2, by, ew - 4, rnd, ["cinta"] if i == 2 else ["papel", "tinta", "chinchetas", "lapices"])
    P.zocalo(cv, X0, X1, WB, rampa="madera", base=1)
    P.baldosas(cv, X0, WB, X1, FB, K("gris", 4), K("gris", 3), t=12, linea=K("gris", 2))
    # cajas apiladas
    for (bx, by) in ((134, 190), (150, 196), (318, 186)):
        cv.rect(bx, by, bx + 24, by + 18, K("ocre", 2)); cv.hline(bx, bx + 24, by, K("ocre", 3)); cv.vline(bx + 12, by, by + 18, K("ocre", 1))
    # bombilla desnuda
    cv.vline(240, WT - 12, 18, K("gris", 2)); cv.ellipse(236, 18, 244, 26, K("ocre", 4)); cv.add_emissive(236, 18, 244, 26)
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, 224, FB + 12, K("gris", 3)); cv.rect(256, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(224, FB, 256, FB + 12, K("madera", 2))
    cv.add_light(X0, WB, X1, FB, -1)
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(240, 60, 150, 0.3, squash=1.2, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
