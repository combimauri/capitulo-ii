"""FC.05 / FD.06 — El Café del Castaño.

Café pequeño y casi vacío. Por la ventana, una calle gris; dentro, algo más cálido: papel pintado
desvaído, friso de madera, tres mesas de madera (en la del centro, un tablero de ajedrez a medio
jugar), una barra a la derecha con botellas de Ginebra de la Victoria y, en la pared, el cartel de
Ivy (el mismo de la casa, en pequeño) mirando a la telepantalla de enfrente.
"""
import random

from pixel import Canvas, K
import props as P
import _luz as L

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 20, 92, 246
ENTRADA = (224, 256)
VENTANA = (60, 30, 130, 80)
CARTEL = (150, 26, 190, 76)
TELE = (300, 30, 360, 70)
MESAS = [(100, 140, 150, 170), (220, 170, 270, 200), (330, 130, 380, 160)]     # huellas (colisiones)
AJEDREZ = 1                                                                      # índice de la mesa con tablero
BARRA = (400, 100, 436, 200)

IVY = [
    "......rrrrrr..........",
    "....rrrrrrrrrr........",
    "...rrrrrrrrrrrr.......",
    "..rrrrrrrrrrrrrr......",
    "..rrrrrrrcccccrr......",
    ".rrrrrrcccccccccr.....",
    ".rrrrrcccccccccccc....",
    ".rrrrcccccccccrrcc....",
    ".rrrrccccccccccrcc....",
    "..rrrcccccccccccccc...",
    "..rrrccccccccccccccc..",
    "...rrcccccccccccccc...",
    "...rrrcccccccccccc....",
    "....rrcccccccccrrc....",
    "....rrrcccccccccc.....",
    ".....rrrccccccccc.....",
    "......rrrcccccc.......",
    ".......rrrccccr.......",
    "........rrccccr.......",
    "......rrrrccccrrr.....",
    "....rrrrrrrrrrrrrrr...",
    "..rrrrrrrrrrrrrrrrrr..",
]


def cartel_ivy(cv, x, y, w=40, h=50, sombra=K("pared", 1)):
    """El cartel de los Mártires de Stepney (misma composición que en el piso, 40x50)."""
    cv.rect(x + 2, y + 2, x + w + 2, y + h + 2, sombra)
    cv.rect(x, y, x + w, y + h, K("rojo", 4))
    for k in range(0, 34, 5):                                                    # rayos
        cv.d.line([x + 20, y + 18, x + 1, y + k], fill=K("rojo", 3))
        cv.d.line([x + 20, y + 18, x + w - 2, y + k], fill=K("rojo", 3))
    cv.grid(x + 9, y + 4, IVY, {"r": K("rojo", 1), "c": K("papel", 4)})
    cv.rect(x, y + 34, x + w, y + h, K("rojo", 1))
    cv.text(x + (w - cv.text_width("RECUERDA")) // 2, y + 37, "RECUERDA", K("papel", 4))
    cv.text(x + (w - cv.text_width("STEPNEY")) // 2, y + 43, "STEPNEY", K("rojo", 5))
    cv.frame(x, y, x + w, y + h, K("rojo", 2))
    for (cx, cy) in [(x + 1, y + 1), (x + w - 2, y + 1)]:
        cv.px(cx, cy, K("gris", 8))                                              # chinchetas


def _ventana(cv, x0, y0, x1, y1, rnd):
    cv.rect(x0 - 3, y0 - 3, x1 + 3, y1 + 3, K("madera", 1))
    # la calle gris, al otro lado del cristal
    cv.rect(x0, y0, x1, y1, K("cielo", 4))
    cv.rect(x0, y0, x1, y0 + 8, K("cielo", 5))
    x = x0 - 4
    while x < x1:                                                                # fachadas de enfrente
        w = rnd.randint(14, 24)
        top = y0 + rnd.randint(8, 16)
        cv.rect(max(x0, x), top, min(x1, x + w), y1, K("cielo", 2 + rnd.choice([0, 1])))
        for wy in range(top + 4, y1 - 14, 8):
            for wx in range(x + 3, x + w - 3, 6):
                if x0 <= wx and wx + 3 <= x1:
                    cv.rect(wx, wy, wx + 3, wy + 4, K("cielo", 1))
        x += w
    cv.rect(x0, y1 - 12, x1, y1, K("gris", 4)); cv.hline(x0, x1, y1 - 12, K("gris", 6))   # acera
    cv.rect(x0 + 44, y0 + 18, x0 + 46, y1 - 10, K("gris", 2))                            # farola apagada
    cv.rect(x0 + 41, y0 + 15, x0 + 49, y0 + 19, K("gris", 2))
    for k in range(9):                                                                    # llovizna
        rx, ry = rnd.randint(x0 + 2, x1 - 2), rnd.randint(y0 + 2, y1 - 16)
        cv.vline(rx, ry, ry + 3, K("cielo", 5))
    # parteluz, travesaño y cristal sucio
    cv.rect((x0 + x1) // 2 - 1, y0, (x0 + x1) // 2 + 1, y1, K("madera", 2))
    cv.rect(x0, y0 + 22, x1, y0 + 24, K("madera", 2))
    for k in range(3):
        cv.d.line([(x0 + 4 + k * 5, y0 + 18), (x0 + 14 + k * 5, y0 + 4)], fill=K("cielo", 5))
    cv.rect(x0 - 6, y1 + 3, x1 + 6, y1 + 7, K("madera", 4)); cv.hline(x0 - 6, x1 + 6, y1 + 6, K("madera", 2))   # alféizar
    cv.add_emissive(x0, y0, x1, y1)


def _silla(cv, x, y, lado):
    """Silla de madera vista desde arriba: asiento y respaldo en el lado exterior (lado -1 izq, +1 der)."""
    cv.rect(x + 1, y + 10, x + 11, y + 13, K("madera", 1))                                # sombra
    cv.rect(x, y, x + 10, y + 10, K("madera", 4)); cv.frame(x, y, x + 10, y + 10, K("madera", 2))
    cv.hline(x + 1, x + 9, y + 1, K("madera", 5))
    bx = x if lado < 0 else x + 7
    cv.rect(bx, y - 8, bx + 3, y + 10, K("madera", 3)); cv.vline(bx, y - 8, y + 10, K("madera", 2))
    cv.hline(bx, bx + 3, y - 8, K("madera", 5))
    for lx in (x + 1, x + 8):
        cv.rect(lx, y + 10, lx + 2, y + 13, K("madera", 2))


def _mesa(cv, x0, y0, x1, y1, ajedrez=False, vasos=1):
    cy = (y0 + y1) // 2
    _silla(cv, x0, cy - 5, -1)
    _silla(cv, x1 - 10, cy - 5, +1)
    tx0, tx1 = x0 + 11, x1 - 11
    top0, top1 = y0 + 2, y1 - 10
    cv.rect(tx0 + 3, y1 - 6, tx1 + 3, y1 + 1, K("madera", 1))                             # sombra
    cv.rect(tx0, top1, tx1, top1 + 4, K("madera", 2)); cv.hline(tx0, tx1, top1 + 3, K("madera", 1))
    for lx in (tx0 + 1, tx1 - 3):
        cv.rect(lx, top1 + 4, lx + 2, y1, K("madera", 1))
    cv.rect(tx0, top0, tx1, top1, K("madera", 4)); cv.frame(tx0, top0, tx1, top1, K("madera", 2))
    cv.hline(tx0 + 1, tx1 - 1, top0 + 1, K("madera", 5))
    cv.hline(tx0 + 3, tx0 + 10, top0 + 7, K("madera", 3))                                 # veta
    if ajedrez:
        bx, by = tx0 + 5, top0 + 2
        cv.rect(bx - 1, by - 1, bx + 17, by + 13, K("madera", 1))
        for r in range(6):                                                                # tablero 8x6 (en escorzo)
            for c in range(8):
                cv.rect(bx + c * 2, by + r * 2, bx + c * 2 + 2, by + r * 2 + 2,
                        K("papel", 3) if (r + c) % 2 == 0 else K("madera", 2))
        piezas = [(1, 0, "n"), (3, 0, "n"), (4, 1, "n"), (6, 0, "n"), (2, 2, "n"), (5, 3, "b"), (1, 4, "b"),
                  (3, 5, "b"), (6, 5, "b"), (4, 4, "b")]
        for (c, r, col) in piezas:
            px_, py_ = bx + c * 2, by + r * 2
            k = K("gris", 1) if col == "n" else K("papel", 4)
            cv.vline(px_ + 1, py_ - 2, py_ + 1, k); cv.px(px_ + 1, py_ - 3, k)
        cv.vline(tx1 - 4, top0 + 5, top0 + 9, K("papel", 4)); cv.px(tx1 - 4, top0 + 4, K("papel", 4))   # pieza comida, al borde
        cv.vline(tx1 - 6, top0 + 6, top0 + 9, K("gris", 1))
    for k in range(vasos):
        vx = tx1 - 7 - k * 9 if not ajedrez else tx0 - 1
        vy = top0 + 6 if not ajedrez else top0 + 9
        cv.rect(vx, vy, vx + 4, vy + 6, K("cielo", 5)); cv.hline(vx, vx + 4, vy, K("cielo", 6))
        cv.hline(vx + 1, vx + 3, vy + 4, K("cielo", 4))


def _botella(cv, x, y, alto=12):
    """Ginebra de la Victoria: cristal claro, etiqueta blanca."""
    cv.rect(x, y - alto, x + 4, y, K("cielo", 5)); cv.vline(x, y - alto, y, K("cielo", 4))
    cv.rect(x + 1, y - alto - 3, x + 3, y - alto, K("cielo", 4)); cv.px(x + 1, y - alto - 4, K("gris", 2))
    cv.rect(x, y - alto + 4, x + 4, y - alto + 8, K("papel", 3)); cv.px(x + 2, y - alto + 5, K("rojo", 3))
    cv.vline(x + 3, y - alto + 1, y - alto + 4, K("cielo", 6))


def _barra(cv, x0, y0, x1, y1, rnd):
    alto = 14
    t0, t1 = y0 - alto, y1 - alto
    cv.rect(x0 - 3, y0, x0, y1, K("madera", 1))                                          # sombra a la izquierda
    cv.rect(x0, t1, x1, y1, K("madera", 2)); cv.hline(x0, x1, y1 - 1, K("madera", 0))   # frente (el extremo de la barra)
    for k in range(x0 + 4, x1, 8):
        cv.vline(k, t1 + 2, y1 - 2, K("madera", 1))
    cv.rect(x0, t0, x1, t1, K("madera", 3)); cv.frame(x0, t0, x1, t1, K("madera", 1))  # tablero de la barra
    cv.vline(x0 + 1, t0 + 1, t1 - 1, K("madera", 5)); cv.hline(x0 + 1, x1 - 1, t0 + 1, K("madera", 4))
    cv.rect(x0 + 4, t0 + 2, x1 - 2, t1 - 2, K("madera", 4))
    # vasos, botellas, un paño y la pila de platillos
    for by in (t0 + 22, t0 + 30, t0 + 56):
        _botella(cv, x0 + 20 + rnd.randint(-2, 2), by, alto=11)
    for (vx, vy) in [(x0 + 7, t0 + 40), (x0 + 12, t0 + 44), (x0 + 7, t0 + 70), (x0 + 22, t0 + 82)]:
        cv.rect(vx, vy, vx + 4, vy + 5, K("cielo", 5)); cv.hline(vx, vx + 4, vy, K("cielo", 6))
    cv.rect(x0 + 8, t0 + 88, x0 + 22, t0 + 94, K("papel", 2)); cv.hline(x0 + 8, x0 + 22, t0 + 91, K("papel", 1))   # paño
    for k in range(4):
        cv.ellipse(x0 + 18, t0 + 6 - k, x0 + 30, t0 + 11 - k, K("papel", 4 - k % 2), outline=K("papel", 1))


def dibujar(variante=None):
    rnd = random.Random(1984)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    # papel pintado viejo, desvaído; friso de madera abajo
    P.papel_pintado(cv, X0, WT, X1, WB, rampa="papel", base=1, motivo="rayas")
    cv.rect(X0, WT, X1, WT + 4, K("madera", 2)); cv.hline(X0, X1, WT + 4, K("madera", 1))  # moldura del techo
    cv.rect(X0, 76, X1, WB, K("madera", 2)); cv.hline(X0, X1, 76, K("madera", 4))
    for x in range(X0 + 10, X1, 20):
        cv.frame(x, 79, x + 16, WB - 4, K("madera", 1))
    # una mancha de humedad que baja del techo
    for k, (mx, mw) in enumerate([(286, 10), (284, 14), (285, 11), (287, 7), (288, 4)]):
        cv.hline(mx, mx + mw, WT + 5 + k, K("papel", 0))
    _ventana(cv, *VENTANA, rnd)
    cartel_ivy(cv, CARTEL[0], CARTEL[1], sombra=K("papel", 0))
    P.telepantalla(cv, TELE[0], TELE[1], TELE[2] - TELE[0], TELE[3] - TELE[1], cara=False)
    tx, ty = TELE[0], TELE[1]
    cv.text(tx + 4, ty + 4, "NOTICIAS", K("tele", 6))
    for k, w in enumerate((40, 32, 44, 26)):
        cv.hline(tx + 4, tx + 4 + w, ty + 14 + k * 5, K("tele", 4))
    cv.rect(tx + 4, ty + 34, tx + 56, ty + 37, K("tele", 3))
    # pizarra con el precio de la ginebra y estante de botellas sobre la barra
    cv.rect(232, 44, 270, 66, K("gris", 1)); cv.frame(232, 44, 270, 66, K("madera", 2))
    cv.text(236, 48, "GINEBRA", K("papel", 3)); cv.text(236, 56, "VICTORIA", K("papel", 2))
    cv.rect(272, 46, 274, 64, K("madera", 2))
    for sy in (48, 66):
        cv.rect(392, sy, 438, sy + 2, K("madera", 4)); cv.hline(392, 438, sy + 2, K("madera", 1))
        for bx in range(396, 434, 7):
            _botella(cv, bx, sy, alto=9 + rnd.randint(0, 2))
    P.zocalo(cv, X0, X1, WB, rampa="madera", base=1)
    # suelo de tablones gastados
    P.tablones(cv, X0, WB, X1, FB, rampa="madera", base=2, semilla=31)
    for (mx, my) in [(170, 214), (300, 120), (90, 196)]:                                   # cercos de vasos
        cv.ellipse(mx, my, mx + 6, my + 4, None, outline=K("madera", 1))
    for i, m in enumerate(MESAS):
        _mesa(cv, *m, ajedrez=(i == AJEDREZ), vasos=0 if i == 2 else 1)
    _barra(cv, *BARRA, rnd)
    # muros y puerta a la calle
    a, b = ENTRADA
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, a, FB + 12, K("gris", 3)); cv.rect(b, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.hline(X0 - 12, a, FB, K("gris", 4)); cv.hline(b, X1 + 12, FB, K("gris", 4))
    cv.rect(a, FB, b, FB + 12, K("madera", 2)); cv.hline(a, b, FB, K("madera", 3))
    # luz: penumbra en los bordes, una lámpara cálida sobre el ajedrez y la luz gris de la ventana
    cv.add_light_fn(lambda x, y: -1 if (WB <= y < FB and (x < X0 + 5 or x >= X1 - 5 or y >= FB - 5)) else 0)
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(245, 175, 110, 0.24, squash=1.3, pasos=10, limite=(X0, WT, X1, FB))
    cv.add_glow_suave(410, 110, 70, 0.16, squash=1.2, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    L.glow_post(cv, 95, 110, 70, 0.14, K("cielo", 5), squash=1.1, limite=(X0, WB, X1, FB))
    L.glow_post(cv, 330, 80, 60, 0.12, K("tele", 4), squash=1.4, limite=(X0, WT, X1, FB))
    return cv
