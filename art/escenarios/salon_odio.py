"""J2.03 — Gran Salón del Ministerio de la Verdad: hileras de asientos frente a una telepantalla gigantesca."""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 24, 456
WT, WB, FB = 12, 92, 252
FILAS = [118, 146, 174, 202, 230]       # y de cada hilera de asientos
PASILLO = (226, 254)
ASIENTO_PROTA = (196, 174)               # hueco libre en la tercera fila


def _publico(cv, x, y, rnd):
    """Una persona sentada vista de espaldas: cabeza y hombros."""
    ramp = rnd.choice(["azul", "azul", "azul", "gris"])
    cv.rect(x - 6, y - 8, x + 6, y, K(ramp, 2 if ramp == "azul" else 1))
    cv.hline(x - 6, x + 6, y - 8, K(ramp, 3 if ramp == "azul" else 2))
    pelo = rnd.choice([("pelo", 1), ("madera", 2), ("ocre", 1), ("gris", 5)])
    cv.ellipse(x - 4, y - 16, x + 4, y - 7, K(*pelo))


def dibujar():
    rnd = random.Random(2)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    cv.rect(X0, WT, X1, WB, K("papel", 3))
    for x in range(X0, X1, 36):
        cv.vline(x, WT, WB, K("papel", 2))
    # telepantalla gigantesca
    tx0, ty0, tx1, ty1 = 132, 18, 348, 84
    cv.rect(tx0 - 6, ty0 - 6, tx1 + 6, ty1 + 8, K("gris", 1))
    cv.rect(tx0, ty0, tx1, ty1, K("tele", 1))
    for y in range(ty0, ty1, 2):
        cv.hline(tx0, tx1, y, K("tele", 0))
    t1, t2 = "DOS MINUTOS DE ODIO", "11:00"
    cv.text(240 - cv.text_width(t1) // 2, 40, t1, K("tele", 5))
    cv.text(240 - cv.text_width(t2) // 2, 50, t2, K("tele", 5))
    cv.add_emissive(tx0, ty0, tx1, ty1)
    # estandartes del Partido
    for sx in (40, 96, 372, 428):
        cv.rect(sx, WT + 2, sx + 16, WB - 8, K("rojo", 3)); cv.vline(sx + 8, WT + 6, WB - 12, K("papel", 3))
        cv.poly([(sx, WB - 8), (sx + 8, WB - 2), (sx + 16, WB - 8)], K("rojo", 3))
    P.zocalo(cv, X0, X1, WB, alto=4, rampa="gris", base=3)
    # suelo de parqué oscuro con alfombra en el pasillo
    P.tablones(cv, X0, WB, X1, FB, rampa="madera", base=2, semilla=9)
    cv.rect(PASILLO[0], WB, PASILLO[1], FB, K("rojo", 2)); cv.vline(PASILLO[0], WB, FB, K("rojo", 1)); cv.vline(PASILLO[1] - 1, WB, FB, K("rojo", 1))
    # hileras de asientos con el público de espaldas
    for fila, y in enumerate(FILAS):
        for (xa, xb) in ((X0 + 10, PASILLO[0] - 6), (PASILLO[1] + 6, X1 - 10)):
            cv.rect(xa, y, xb, y + 6, K("madera", 4)); cv.hline(xa, xb, y, K("madera", 5))
            cv.rect(xa, y + 6, xb, y + 9, K("madera", 1))
            for x in range(xa + 8, xb - 4, 16):
                if (x, y) == ASIENTO_PROTA or abs(x - ASIENTO_PROTA[0]) < 8 and y == ASIENTO_PROTA[1]:
                    continue
                if rnd.random() < 0.82:
                    _publico(cv, x, y + 2, rnd)
    # muros
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.add_glow_suave(240, 90, 220, 0.2, squash=1.6, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
