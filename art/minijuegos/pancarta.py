"""J2.05 — La pancarta del Centro de la Comunidad: «¡MUERTE A EURASIA!».

El suelo de tablones del Centro, con la tela extendida sobre periódicos viejos y las letras trazadas a
lápiz (cada «píxel» de la letra es un cuadro de 4x4 del arte = 8x8 del juego, en las mismas posiciones
que usa la escena para puntuar). Alrededor: botes de pintura roja, un tarro con pinceles, un trapo
manchado, la otra pancarta enrollada y la lista de Hilda en una tablilla.

  pancarta-fondo   480x270
  pancarta-mancha  hoja de 3 fotogramas de 11x11 (pinceladas que se estampan al pintar)
  pancarta-brocha  20x20 (la brocha que sigue al puntero; la punta está abajo a la izquierda)
"""
import random

from _base import CLAVE, Canvas, K, a_rgba, guardar, hoja, sprite
import props as P

W, H = 480, 270
LEMA = "¡MUERTE A EURASIA!"
FUENTE = {  # la misma que PancartaScene.ts
    "M": "101111111101101", "U": "101101101101111", "E": "111100110100111", "R": "110101110101101",
    "T": "111010010010010", "A": "010101111101101", "S": "011100010001110", "I": "111010010010111",
    "¡": "010000010010010", "!": "010010010000010", " ": "000000000000000",
}
ORIGEN = (96, 100)                    # origen del juego (192, 200) a la mitad
PX = 4                                # PIXEL = 8 en el juego
TELA = (78, 86, 402, 136)


def celdas():
    out = set()
    for i, ch in enumerate(LEMA):
        for k, b in enumerate(FUENTE.get(ch, FUENTE[" "])):
            if b == "1":
                out.add((ORIGEN[0] + i * 4 * PX + (k % 3) * PX, ORIGEN[1] + (k // 3) * PX))
    return out


def _periodico(cv, x0, y0, x1, y1, semilla):
    rnd = random.Random(semilla)
    cv.rect(x0 + 1, y0 + 1, x1 + 1, y1 + 1, K("madera", 1))
    cv.rect(x0, y0, x1, y1, K("papel", 2)); cv.frame(x0, y0, x1, y1, K("papel", 1))
    cv.rect(x0 + 3, y0 + 3, x1 - 3, y0 + 7, K("papel", 1))                       # cabecera
    for y in range(y0 + 10, y1 - 2, 3):
        for cx in (x0 + 3, (x0 + x1) // 2 + 2):
            w = rnd.randint(8, (x1 - x0) // 2 - 6)
            cv.hline(cx, cx + w, y, K("papel", 0))


def _bote(cv, x, y, abierto=True, etiqueta=True):
    """Bote de pintura de 18x20, con la boca en (x, y)."""
    cv.ellipse(x + 2, y + 19, x + 22, y + 26, K("madera", 1))                   # sombra
    cv.rect(x, y + 3, x + 18, y + 22, K("gris", 6)); cv.vline(x, y + 3, y + 22, K("gris", 4))
    cv.vline(x + 17, y + 3, y + 22, K("gris", 4)); cv.vline(x + 3, y + 4, y + 21, K("gris", 8))
    cv.ellipse(x, y + 18, x + 18, y + 24, K("gris", 4))
    if etiqueta:
        cv.rect(x, y + 9, x + 18, y + 17, K("papel", 3)); cv.rect(x, y + 11, x + 18, y + 14, K("rojo", 3))
    cv.ellipse(x, y, x + 18, y + 7, K("gris", 3))
    if abierto:
        cv.ellipse(x + 1, y + 1, x + 17, y + 6, K("rojo", 3))
        cv.hline(x + 4, x + 9, y + 2, K("rojo", 5))
        for dx, largo in ((2, 8), (12, 5), (15, 10)):                         # chorretones
            cv.vline(x + dx, y + 4, y + 4 + largo, K("rojo", 3)); cv.px(x + dx, y + 4 + largo, K("rojo", 2))
    else:
        cv.ellipse(x + 1, y + 1, x + 17, y + 6, K("gris", 7)); cv.ellipse(x + 4, y + 2, x + 14, y + 5, K("gris", 6))


def fondo():
    rnd = random.Random(14)
    cv = Canvas(W, H)
    P.tablones(cv, 0, 0, W, H, rampa="madera", base=3, semilla=12)
    # periódicos bajo la tela
    for i, (x0, y0) in enumerate(((60, 76), (150, 120), (300, 74), (356, 118), (218, 70))):
        _periodico(cv, x0, y0, x0 + 56, y0 + 34, i)
    # la tela, con dobladillo y arrugas
    x0, y0, x1, y1 = TELA
    cv.rect(x0 + 2, y0 + 3, x1 + 2, y1 + 3, K("madera", 1))
    cv.rect(x0, y0, x1, y1, K("papel", 3))
    cv.frame(x0 + 2, y0 + 2, x1 - 2, y1 - 2, K("papel", 2)); cv.frame(x0, y0, x1, y1, K("papel", 1))
    for _ in range(14):
        ax, ay = rnd.randint(x0 + 6, x1 - 20), rnd.randint(y0 + 4, y1 - 8)
        if ORIGEN[1] - 2 <= ay <= ORIGEN[1] + 22:
            continue
        cv.d.line([(ax, ay), (ax + rnd.randint(6, 16), ay + rnd.choice([-2, 2, 3]))], fill=K("papel", 2))
    # las letras, trazadas a lápiz: relleno pálido y contorno solo por fuera
    cel = celdas()
    for (cx, cy) in cel:
        cv.rect(cx, cy, cx + PX, cy + PX, K("papel", 2))
    for (cx, cy) in cel:
        if (cx, cy - PX) not in cel:
            cv.hline(cx, cx + PX, cy, K("gris", 6))
        if (cx, cy + PX) not in cel:
            cv.hline(cx, cx + PX, cy + PX - 1, K("gris", 6))
        if (cx - PX, cy) not in cel:
            cv.vline(cx, cy, cy + PX, K("gris", 6))
        if (cx + PX, cy) not in cel:
            cv.vline(cx + PX - 1, cy, cy + PX, K("gris", 6))
    # renglones de guía a lápiz
    cv.hline(ORIGEN[0] - 6, x1 - 12, ORIGEN[1] - 3, K("papel", 1))
    cv.hline(ORIGEN[0] - 6, x1 - 12, ORIGEN[1] + 22, K("papel", 1))
    # gotas de un intento anterior, fuera de las letras
    for (gx, gy) in ((90, 126), (92, 128), (380, 92), (300, 130), (301, 131)):
        cv.px(gx, gy, K("rojo", 3))
    # botes, tarro de pinceles, trapo
    _bote(cv, 24, 150, abierto=True)
    _bote(cv, 46, 166, abierto=False)
    cv.ellipse(30, 196, 52, 204, K("rojo", 2))                                  # charquito
    cv.ellipse(33, 197, 47, 202, K("rojo", 3))
    _bote(cv, 430, 160, abierto=True, etiqueta=False)
    tx = 414                                                                    # tarro con pinceles
    cv.ellipse(tx, 196, tx + 14, 202, K("madera", 1))
    cv.rect(tx, 180, tx + 12, 198, K("cielo", 4)); cv.frame(tx, 180, tx + 12, 198, K("cielo", 2))
    cv.rect(tx + 1, 188, tx + 11, 197, K("granate", 4)); cv.vline(tx + 2, 181, 197, K("cielo", 6))
    for k, (dx, h) in enumerate(((3, 18), (6, 22), (9, 16))):
        cv.d.line([(tx + dx, 184), (tx + dx + k - 1, 184 - h)], fill=K("madera", 5))
        cv.px(tx + dx + k - 1, 184 - h, K("rojo", 3)); cv.px(tx + dx + k - 1, 185 - h, K("gris", 6))
    cv.poly([(436, 206), (462, 202), (468, 214), (446, 220), (434, 214)], K("papel", 2))   # trapo
    cv.d.polygon([(436, 206), (462, 202), (468, 214), (446, 220), (434, 214)], outline=K("papel", 1))
    for (mx, my) in ((444, 208), (452, 212), (445, 214), (458, 207)):
        cv.rect(mx, my, mx + 3, my + 2, K("rojo", 3))
    # la otra pancarta, enrollada, y la tablilla de Hilda
    cv.rect(22, 30, 150, 41, K("papel", 3)); cv.hline(22, 150, 30, K("papel", 4)); cv.hline(22, 150, 40, K("papel", 1))
    cv.ellipse(146, 30, 154, 42, K("papel", 2)); cv.ellipse(148, 33, 152, 39, K("papel", 1))
    cv.hline(24, 146, 42, K("madera", 1))
    for k in range(5):
        cv.rect(40 + k * 22, 31, 46 + k * 22, 40, K("rojo", 3))                    # letras que asoman
    hx, hy = 400, 22
    cv.rect(hx + 2, hy + 2, hx + 44, hy + 48, K("madera", 1))
    cv.rect(hx, hy, hx + 42, hy + 46, K("madera", 5)); cv.frame(hx, hy, hx + 42, hy + 46, K("madera", 2))
    cv.rect(hx + 4, hy + 6, hx + 38, hy + 44, K("papel", 4))
    cv.rect(hx + 14, hy - 2, hx + 28, hy + 5, K("gris", 6)); cv.hline(hx + 14, hx + 28, hy - 2, K("gris", 8))
    cv.text(hx + 6, hy + 9, "SEMANA", K("gris", 2)); cv.text(hx + 6, hy + 15, "DEL ODIO", K("gris", 2))
    for k in range(4):
        y = hy + 23 + k * 5
        cv.hline(hx + 10, hx + 10 + rnd.randint(14, 24), y, K("gris", 5))
        cv.rect(hx + 6, y - 1, hx + 8, y + 1, K("gris", 4))
        if k < 2:
            cv.px(hx + 6, y - 1, K("rojo", 3)); cv.px(hx + 7, y, K("rojo", 3))
    cv.d.line([(hx - 10, hy + 40), (hx + 2, hy + 30)], fill=K("ocre", 2))       # lápiz
    cv.px(hx + 3, hy + 29, K("gris", 2))
    # rastro de gotas del bote a la tela
    for k in range(9):
        cv.px(52 + k * 3 + rnd.randint(0, 1), 150 - k * 2 + rnd.randint(-1, 1), K("rojo", 3))
    # luz cálida de las bombillas del Centro
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(240, 60, 300, 0.14, squash=1.4)
    cv.bake_lighting()
    return cv.img


def _mancha(semilla):
    rnd = random.Random(semilla)
    cv = sprite(11, 11)
    cv.ellipse(0, 0, 11, 11, K("rojo", 3))
    for _ in range(4):                                                          # borde irregular
        cv.px(rnd.choice([0, 10]), rnd.randint(3, 7), K("rojo", 3))
        cv.px(rnd.randint(3, 7), rnd.choice([0, 10]), K("rojo", 3))
    cv.d.arc([1, 1, 10, 10], 20, 110, fill=K("rojo", 2))
    for _ in range(2):                                                          # cerdas
        y = rnd.randint(3, 7)
        cv.hline(rnd.randint(2, 4), rnd.randint(6, 9), y, K("rojo", 2))
    cv.px(3 + rnd.randint(0, 1), 3, K("rojo", 4)); cv.px(4, 2 + rnd.randint(0, 1), K("rojo", 4))
    return a_rgba(cv)


def mancha():
    return hoja([_mancha(s) for s in (1, 2, 3)])


def brocha():
    cv = sprite(20, 20)
    # mango en diagonal hacia arriba a la derecha
    for k in range(9):
        x, y = 9 + k, 10 - k
        cv.rect(x, y - 1, x + 2, y + 1, K("madera", 5)); cv.px(x + 1, y + 1, K("madera", 3))
    cv.px(18, 2, K("madera", 2)); cv.px(17, 1, K("madera", 6))
    # virola
    for k in range(3):
        cv.rect(6 + k, 11 - k, 9 + k, 14 - k, K("gris", 7))
    cv.px(7, 11, K("gris", 9)); cv.px(9, 13, K("gris", 4))
    # cerdas, empapadas de rojo
    cv.poly([(1, 18), (6, 11), (10, 15), (3, 19)], K("granate", 2))
    cv.poly([(0, 19), (3, 15), (6, 18), (2, 19)], K("rojo", 3))
    cv.px(2, 17, K("rojo", 5)); cv.px(0, 19, K("rojo", 2))
    return a_rgba(cv)


def exportar(destino):
    return [guardar(fondo(), destino, "pancarta-fondo"), guardar(mancha(), destino, "pancarta-mancha"),
            guardar(brocha(), destino, "pancarta-brocha")]
