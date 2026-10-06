"""J1.02 — Rellano y escalera de las Mansiones Victoria."""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 20, 84, 246


def dibujar():
    rnd = random.Random(84)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    # pared del fondo: pintura verde desconchada sobre yeso
    cv.rect(X0, WT, X1, WB, K("pared", 2))
    cv.rect(X0, 58, X1, WB, K("pared", 1)); cv.hline(X0, X1, 58, K("pared", 4))
    for _ in range(26):
        x, y = rnd.randint(X0, X1 - 14), rnd.randint(WT + 2, 54)
        w, h = rnd.randint(4, 14), rnd.randint(3, 8)
        cv.rect(x, y, x + w, y + h, K("papel", 1)); cv.hline(x, x + w, y + h, K("pared", 1))
    P.zocalo(cv, X0, X1, WB)
    cv.hline(X0, X1, WT + 4, K("gris", 5)); cv.hline(X0, X1, WT + 5, K("gris", 3))            # tubería
    # ascensor averiado
    cv.rect(60, 26, 108, WB - 2, K("gris", 3)); cv.frame(60, 26, 108, WB - 2, K("gris", 1))
    cv.rect(64, 30, 83, WB - 4, K("gris", 4)); cv.rect(85, 30, 104, WB - 4, K("gris", 4))
    cv.vline(84, 30, WB - 4, K("gris", 1))
    cv.rect(66, 46, 102, 56, K("papel", 3)); cv.frame(66, 46, 102, 56, K("rojo", 3))
    cv.text(84 - cv.text_width("AVERIADO") // 2, 49, "AVERIADO", K("rojo", 3))
    # puerta del piso del protagonista y puerta de los Parsons
    P.puerta(cv, 186, 34, numero="5B")
    P.puerta(cv, 386, 34, numero="5C")
    # cartel del Gran Hermano
    P.cartel_gran_hermano(cv, 262, 22, w=52, h=58)
    # bombilla desnuda
    cv.vline(160, WT, 32, K("gris", 1)); cv.ellipse(157, 31, 164, 38, K("ocre", 4)); cv.add_emissive(157, 31, 164, 38)

    # suelo de linóleo gastado
    P.baldosas(cv, X0, WB, X1, FB, K("tela", 2), K("tela", 3), t=16, linea=K("tela", 1))
    P.manchas(cv, X0, WB, X1, FB, K("tela", 1), n=260, semilla=3)

    # escalera que sube (izquierda): peldaños cada vez más claros hacia arriba
    for i, y in enumerate(range(96, 190, 10)):
        cv.rect(X0, y, 120, y + 10, K("madera", 5 - i // 3)); cv.hline(X0, 120, y, K("madera", 6 - i // 3))
        cv.hline(X0, 120, y + 9, K("madera", 1))
    P.barandilla(cv, 96, 190, 122, vertical=True)
    # hueco de la escalera que baja (abajo a la derecha)
    cv.rect(320, 168, X1, FB, K("gris", 1))
    for i, y in enumerate(range(170, FB, 10)):
        cv.rect(326, y, X1, y + 9, K("madera", max(0, 3 - i // 2))); cv.hline(326, X1, y, K("madera", max(1, 4 - i // 2)))
    P.barandilla(cv, 168, 222, 318, vertical=True)
    P.barandilla(cv, 318, X1, 168)
    # tapas de muro laterales e inferior
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.vline(X0 - 1, WT, FB, K("gris", 1))
    cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3)); cv.vline(X1, WT, FB, K("gris", 1))
    cv.rect(X0 - 12, FB, 320, FB + 12, K("gris", 3)); cv.hline(X0, 320, FB, K("gris", 1))

    # luz: bombilla cálida y rincones oscuros
    cv.add_light_fn(lambda x, y: -1 if (x < X0 + 6 or x > X1 - 6 or y > FB - 6) else 0)
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(160, 90, 150, 0.18, squash=1.1, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
