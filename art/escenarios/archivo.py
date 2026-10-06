"""J6.03 — Sala de archivo del departamento: estanterías de cajas grises, mesa de consulta con lámpara verde
y una telepantalla pequeña en el techo, en un ángulo, que gira."""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 20, 92, 236


def estanteria(cv, x, y, w, h, rnd, etiquetas=True):
    cv.rect(x, y, x + w, y + h, K("gris", 3)); cv.frame(x, y, x + w, y + h, K("gris", 2))
    for fy in range(y + 4, y + h - 4, 18):
        cv.hline(x + 1, x + w - 1, fy + 14, K("gris", 5))
        bx = x + 3
        while bx < x + w - 14:
            bw = rnd.randint(10, 14)
            cv.rect(bx, fy, bx + bw, fy + 13, K("gris", rnd.choice([5, 6, 6, 7])))
            cv.hline(bx, bx + bw, fy, K("gris", 8))
            if etiquetas:
                cv.rect(bx + 3, fy + 5, bx + bw - 3, fy + 8, K("papel", 3))
            bx += bw + 2


def dibujar():
    rnd = random.Random(84)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    P.papel_pintado(cv, X0, WT, X1, WB, rampa="gris", base=4, motivo="rayas")
    estanteria(cv, 70, 26, 140, 66, rnd)
    estanteria(cv, 230, 26, 180, 66, rnd)
    # telepantalla de techo, en el ángulo, con su soporte
    cv.vline(58, WT, 36, K("gris", 2)); cv.rect(48, 36, 70, 50, K("gris", 1)); cv.rect(50, 38, 68, 48, K("tele", 2))
    cv.rect(56, 41, 62, 45, K("tele", 4)); cv.add_emissive(50, 38, 68, 48)
    P.zocalo(cv, X0, X1, WB, rampa="gris", base=3)
    P.baldosas(cv, X0, WB, X1, FB, K("gris", 5), K("gris", 4), t=12, linea=K("gris", 3))
    # estanterías laterales
    for ex in (X0 + 2, X1 - 26):
        estanteria(cv, ex, 100, 24, 110, rnd, etiquetas=False)
    # la mesa de consulta con la lámpara verde
    cv.rect(192, 150, 290, 172, K("madera", 3)); cv.hline(192, 290, 150, K("madera", 4)); cv.rect(192, 172, 290, 178, K("madera", 1))
    cv.rect(270, 140, 274, 152, K("gris", 2)); cv.poly([(262, 140), (282, 140), (278, 134), (266, 134)], K("tele", 3))
    cv.add_emissive(264, 138, 280, 141)
    P.silla(cv, 232, 176, rampa="madera", base=2)
    # muros y puerta
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, 224, FB + 12, K("gris", 3)); cv.rect(256, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(224, FB, 256, FB + 12, K("madera", 2))
    cv.add_light(X0, WB, X1, FB, -1)
    cv.glow_rgb = K("tele", 4)
    cv.add_glow_suave(272, 156, 60, 0.3, squash=1.3, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
