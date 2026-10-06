"""J1.02 — Rellano y escalera de las Mansiones Victoria.

Variante "odio": Semana del Odio. Ristras de banderines, el soldado euroasiático gigante en lugar
del Gran Hermano y el cartel de los mártires (con Ivy) repetido junto a la puerta de los Parsons.
"""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 20, 84, 246


def _ristra(cv, pts, rnd, caida=8, paso=7):
    """Cuerda de banderines triangulares entre anclajes (x, y), con comba."""
    cols = [K("rojo", 4), K("papel", 4), K("rojo", 2), K("papel", 3), K("rojo", 3)]
    i = 0
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        prev = None
        for x in range(xa, xb + 1):
            t = (x - xa) / max(1, xb - xa)
            y = int(round(ya + (yb - ya) * t + caida * 4 * t * (1 - t)))
            if prev is not None:
                cv.d.line([prev, (x, y)], fill=K("gris", 1))
            prev = (x, y)
            if (x - xa) % paso == 3 and 2 < x - xa < xb - xa - 3:
                c = cols[i % len(cols)]; i += 1
                for r in range(6):                                              # triángulo que cuelga
                    cv.hline(x - 2 + r // 2, x + 3 - r // 2, y + 1 + r, c)
                cv.px(x + 1, y + 6, K("rojo", 1) if c != K("rojo", 1) else c)


def _cartel_soldado(cv, x, y, w=52, h=58):
    """Semana del Odio: un soldado euroasiático gigantesco, metralleta a la cadera, botas enormes hacia ti."""
    cv.rect(x + 2, y + 2, x + w + 2, y + h + 2, K("pared", 0))                  # sombra
    cv.rect(x, y, x + w, y + h, K("rojo", 1))
    cx = x + w // 2
    for k in range(1, w - 1, 5):                                                # rayos desde la cabeza
        cv.d.line([cx, y + 10, x + k, y + h - 9], fill=K("rojo", 2))
    for k in range(y + 4, y + h - 12, 6):
        cv.d.line([cx, y + 10, x + 1, k], fill=K("rojo", 2)); cv.d.line([cx, y + 10, x + w - 2, k], fill=K("rojo", 2))
    cv.rect(x, y, x + w, y + 2, K("rojo", 1))
    # piernas abiertas, cada vez más anchas hacia el espectador (escorzo)
    cv.poly([(cx - 9, y + 27), (cx - 1, y + 27), (cx - 8, y + 40), (cx - 21, y + 40)], K("tela", 1))
    cv.poly([(cx + 1, y + 27), (cx + 9, y + 27), (cx + 20, y + 39), (cx + 8, y + 39)], K("tela", 0))
    cv.d.line([(cx - 9, y + 28), (cx - 20, y + 39)], fill=K("tela", 2))
    # capote
    cv.poly([(cx - 9, y + 13), (cx + 9, y + 13), (cx + 11, y + 29), (cx - 11, y + 29)], K("tela", 1))
    cv.poly([(cx + 3, y + 13), (cx + 9, y + 13), (cx + 11, y + 29), (cx + 4, y + 29)], K("tela", 0))
    cv.hline(cx - 10, cx + 11, y + 22, K("pelo", 0))                                   # cinturón
    cv.px(cx - 1, y + 22, K("ocre", 2))
    # cabeza: casco y cara inexpresiva, ojos rasgados
    cv.ellipse(cx - 5, y + 3, cx + 6, y + 14, K("piel", 2))
    cv.vline(cx + 4, y + 8, y + 13, K("piel", 1))
    cv.ellipse(cx - 6, y + 1, cx + 7, y + 9, K("gris", 3)); cv.hline(cx - 7, cx + 8, y + 7, K("gris", 2))
    cv.hline(cx - 6, cx + 7, y + 8, K("gris", 1)); cv.hline(cx - 3, cx + 2, y + 2, K("gris", 5))
    cv.hline(cx - 4, cx - 1, y + 10, K("pelo", 0)); cv.hline(cx + 2, cx + 5, y + 10, K("pelo", 0))
    cv.hline(cx - 1, cx + 2, y + 12, K("piel", 0))
    # metralleta a la cadera apuntándote: cañón en escorzo (boca negra)
    cv.rect(cx - 13, y + 19, cx - 7, y + 25, K("madera", 2)); cv.hline(cx - 13, cx - 7, y + 19, K("madera", 4))
    cv.rect(cx - 8, y + 20, cx + 2, y + 24, K("gris", 2))
    cv.ellipse(cx - 1, y + 17, cx + 9, y + 27, K("gris", 2), outline=K("gris", 0))
    cv.ellipse(cx + 2, y + 20, cx + 6, y + 24, K("gris", 0)); cv.px(cx + 1, y + 18, K("gris", 5))
    cv.rect(cx - 12, y + 24, cx - 8, y + 27, K("piel", 2))                       # mano
    # botas gigantes, puntera hacia ti: la izquierda casi se sale del cartel
    def bota(bx0, bx1, by0, by1):
        cv.rect(bx0 + 3, by0, bx1 - 3, by0 + 4, K("gris", 1))                    # caña
        cv.ellipse(bx0, by0 + 2, bx1, by1 + 2, K("gris", 1), outline=K("gris", 0))
        cv.d.arc([bx0 + 2, by0 + 3, bx1 - 2, by1], 200, 340, fill=K("gris", 4))   # brillo de la puntera
        cv.rect(bx0, by1 - 1, bx1, by1 + 1, K("gris", 0))                        # suela
    bota(cx - 25, cx - 4, y + 38, y + 48)
    bota(cx + 6, cx + 22, y + 37, y + 45)
    # banda con el nombre del enemigo
    cv.rect(x, y + h - 9, x + w, y + h, K("papel", 4))
    t = "EURASIA"
    cv.text(x + (w - cv.text_width(t)) // 2, y + h - 7, t, K("rojo", 3))
    cv.frame(x, y, x + w, y + h, K("rojo", 1))
    for (px_, py_) in [(x + 1, y + 1), (x + w - 2, y + 1)]:
        cv.px(px_, py_, K("gris", 8))


def _cartel_martires(cv, x, y, w=48, h=46):
    """El cartel de los mártires de Stepney: caras en fila e Ivy, más clara, delante en el centro."""
    cv.rect(x + 2, y + 2, x + w + 2, y + h + 2, K("pared", 0))
    cv.rect(x, y, x + w, y + h, K("rojo", 4)); cv.frame(x, y, x + w, y + h, K("rojo", 2))
    for i in range(5):                                                          # fila de atrás
        fx = x + 3 + i * 9
        cv.ellipse(fx, y + 4, fx + 8, y + 14, K("papel", 2)); cv.ellipse(fx, y + 3, fx + 8, y + 8, K("rojo", 1))
    for i, fx in enumerate((x + 4, x + 14, x + 30, x + 40)):                   # fila de delante
        cv.ellipse(fx, y + 14, fx + 9, y + 25, K("papel", 3)); cv.ellipse(fx, y + 13, fx + 9, y + 19, K("rojo", 1))
    ix = x + w // 2 - 6                                                        # Ivy
    cv.ellipse(ix, y + 12, ix + 12, y + 28, K("papel", 4)); cv.ellipse(ix - 1, y + 10, ix + 13, y + 19, K("rojo", 1))
    cv.rect(ix - 1, y + 16, ix + 2, y + 26, K("rojo", 1)); cv.hline(ix + 4, ix + 8, y + 24, K("rojo", 3))
    cv.rect(x, y + 30, x + w, y + h, K("rojo", 1))
    cv.text(x + (w - cv.text_width("MARTIRES")) // 2, y + 32, "MARTIRES", K("papel", 4))
    cv.text(x + (w - cv.text_width("STEPNEY")) // 2, y + 39, "STEPNEY", K("rojo", 5))
    for (px_, py_) in [(x + 1, y + 1), (x + w - 2, y + 1)]:
        cv.px(px_, py_, K("gris", 8))


def dibujar(variante=None):
    odio = variante == "odio"
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
    if odio:
        _cartel_soldado(cv, 262, 22, w=52, h=58)
        _cartel_martires(cv, 328, 32, w=48, h=44)
        rb = random.Random(1984)
        _ristra(cv, [(X0, 22), (112, 23), (186, 23), (262, 22)], rb, caida=6)
        _ristra(cv, [(314, 22), (382, 22), (X1, 22)], rb, caida=4)
    else:
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
    if odio:
        _ristra(cv, [(318, 158), (378, 160), (X1, 158)], random.Random(5), caida=5)         # banderines en la barandilla
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
