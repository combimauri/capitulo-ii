"""A3 — Sótano de La Campana: la bodega bajo el pub, donde se baja por una trampilla y una escalera de mano.

Ladrillo, barriles, una mesa con cuatro sillas que no casan entre sí y una sola vela. En la pared del fondo,
un hueco con ladrillos sueltos: lo que se esconde ahí no está en ningún registro. La paleta más cálida del juego.
"""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 100, 380
WT, WB, FB = 24, 92, 236
VX, VY = 240, 146                       # la vela


def ladrillo(cv, x0, y0, x1, y1, rnd):
    cv.rect(x0, y0, x1, y1, K("ocre", 0))                                                 # mortero
    for fila, y in enumerate(range(y0, y1, 5)):
        off = (fila % 2) * 5
        for x in range(x0 - off, x1, 10):
            b = rnd.choice([2, 2, 3, 3, 3, 4])
            cv.rect(max(x0, x + 1), y + 1, min(x1, x + 9), min(y1, y + 4), K("granate", b))
            if rnd.random() < 0.3:
                cv.hline(max(x0, x + 1), min(x1, x + 9), y + 1, K("granate", b + 1))


def escalera_mano(cv, x0, y0, x1, y1):
    # la trampilla abierta en el techo, con la luz del pub arriba
    cv.rect(x0 - 4, y0 - 12, x1 + 4, y0, K("gris", 1))
    cv.rect(x0 - 2, y0 - 11, x1 + 2, y0, K("ocre", 2)); cv.hline(x0 - 2, x1 + 2, y0 - 11, K("ocre", 3))
    for k in range(x0, x1 + 2, 6):
        cv.vline(k, y0 - 11, y0, K("ocre", 1))
    cv.add_emissive(x0 - 2, y0 - 11, x1 + 2, y0)
    cv.rect(x1 + 4, y0 - 14, x1 + 16, y0 - 2, K("madera", 3)); cv.frame(x1 + 4, y0 - 14, x1 + 16, y0 - 2, K("madera", 1))   # la tapa
    # sombra en la pared
    cv.rect(x0 + 4, y0, x0 + 7, y1 - 6, K("granate", 1)); cv.rect(x1 - 1, y0, x1 + 2, y1 - 6, K("granate", 1))
    # largueros
    for lx in (x0 + 1, x1 - 4):
        cv.rect(lx, y0 - 2, lx + 3, y1, K("madera", 3)); cv.vline(lx, y0 - 2, y1, K("madera", 5)); cv.vline(lx + 2, y0 - 2, y1, K("madera", 1))
    # peldaños
    for ry in range(y0 + 4, y1 - 2, 8):
        cv.rect(x0 + 4, ry, x1 - 4, ry + 2, K("madera", 4)); cv.hline(x0 + 4, x1 - 4, ry + 2, K("madera", 1))
    cv.rect(x0 + 1, y1 - 1, x1, y1 + 3, K("madera", 0))                                    # apoyo en el suelo


def barril(cv, x, y, w=20, h=26):
    """Barril de pie: tapa elíptica arriba y duelas con flejes."""
    cv.ellipse(x + 2, y + h - 4, x + w + 4, y + h + 3, K("madera", 0))                      # sombra
    cv.rect(x, y + 4, x + w, y + h, K("madera", 3))
    for k in range(x, x + w):
        t = (k - x) / w
        c = K("madera", 4) if 0.15 < t < 0.4 else K("madera", 2) if t > 0.75 else K("madera", 3)
        cv.vline(k, y + 4, y + h - 1, c)
    cv.ellipse(x, y + h - 6, x + w, y + h + 1, K("madera", 2))
    cv.rect(x, y + 4, x + w, y + h - 3, K("madera", 3))
    for k in range(x, x + w):
        t = (k - x) / w
        c = K("madera", 4) if 0.15 < t < 0.4 else K("madera", 2) if t > 0.75 else K("madera", 3)
        cv.vline(k, y + 4, y + h - 3, c)
    for k in range(x + 4, x + w - 2, 5):
        cv.vline(k, y + 6, y + h - 3, K("madera", 1))
    for fy in (y + 7, y + h - 7):                                                          # flejes
        cv.hline(x, x + w, fy, K("gris", 2)); cv.hline(x, x + w, fy + 1, K("gris", 4))
    cv.ellipse(x, y, x + w, y + 9, K("madera", 4), outline=K("madera", 1))                 # tapa
    cv.ellipse(x + 3, y + 2, x + w - 3, y + 7, K("madera", 5))
    cv.hline(x + 4, x + w - 4, y + 4, K("madera", 3))


def silla(cv, x0, y0, x1, y1, tipo, rampa, base):
    w = x1 - x0
    cv.rect(x0 + 2, y1 - 2, x1 + 3, y1 + 2, K("madera", 0))
    if tipo == "izq":                                                                      # de perfil, mirando a la mesa (derecha)
        cv.rect(x0, y0 + 6, x1, y0 + 11, K(rampa, base + 1)); cv.hline(x0, x1, y0 + 6, K(rampa, base + 2))
        cv.rect(x0, y0 - 4, x0 + 3, y0 + 11, K(rampa, base)); cv.vline(x0, y0 - 4, y0 + 11, K(rampa, base + 2))
        for xx in (x0, x1 - 2):
            cv.rect(xx, y0 + 11, xx + 2, y1, K(rampa, base - 1))
    elif tipo == "der":
        cv.rect(x0, y0 + 6, x1, y0 + 11, K(rampa, base + 1)); cv.hline(x0, x1, y0 + 6, K(rampa, base + 2))
        cv.rect(x1 - 3, y0 - 4, x1, y0 + 11, K(rampa, base)); cv.vline(x1 - 3, y0 - 4, y0 + 11, K(rampa, base + 2))
        for xx in (x0, x1 - 2):
            cv.rect(xx, y0 + 11, xx + 2, y1, K(rampa, base - 1))
    elif tipo == "arriba":                                                                 # detrás de la mesa: se ve el respaldo
        cv.rect(x0, y0 - 6, x1, y0 + 2, K(rampa, base)); cv.hline(x0, x1, y0 - 6, K(rampa, base + 2))
        cv.vline(x0 + w // 2, y0 - 4, y0 + 2, K(rampa, base - 1))
        cv.rect(x0, y0 + 2, x1, y1, K(rampa, base + 1)); cv.frame(x0, y0 + 2, x1, y1, K(rampa, base - 1))
    else:                                                                                  # delante: de espaldas a la cámara
        cv.rect(x0, y0, x1, y0 + 6, K(rampa, base + 1)); cv.frame(x0, y0, x1, y0 + 6, K(rampa, base - 1))
        for xx in (x0 + 1, x1 - 3):
            cv.rect(xx, y0 + 6, xx + 2, y1, K(rampa, base - 1))
        cv.rect(x0, y0 + 3, x1, y0 + 10, K(rampa, base)); cv.hline(x0, x1, y0 + 3, K(rampa, base + 2))
        cv.rect(x0 + 3, y0 + 5, x1 - 3, y0 + 8, K(rampa, base - 1))


def dibujar(variante=None):
    rnd = random.Random(1213)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    ladrillo(cv, X0, WT, X1, WB, rnd)
    cv.rect(X0, WT, X1, WT + 4, K("madera", 1))                                             # vigas del techo
    for vx in range(X0 + 20, X1, 52):
        cv.rect(vx, WT, vx + 8, WT + 7, K("madera", 2)); cv.hline(vx, vx + 8, WT + 6, K("madera", 0))
    # botellero en la pared
    cv.rect(178, 40, 262, 80, K("madera", 1)); cv.frame(178, 40, 262, 80, K("madera", 0))
    for by in range(43, 78, 7):
        for bx in range(181, 259, 7):
            cv.ellipse(bx, by, bx + 6, by + 6, K("madera", 0))
            if rnd.random() < 0.6:
                cv.ellipse(bx + 1, by + 1, bx + 5, by + 5, K("granate", rnd.choice([1, 2, 3])))
                cv.px(bx + 2, by + 2, K("ocre", 3))
    # el hueco con ladrillos sueltos
    hx0, hy0, hx1, hy1 = 300, 52, 324, 72
    cv.rect(hx0 - 1, hy0 - 1, hx1 + 1, hy1 + 1, K("ocre", 0))
    cv.rect(hx0, hy0, hx1, hy1, K("granate", 0))
    cv.rect(hx0 + 2, hy0 + 2, hx1 - 2, hy0 + 5, K("gris", 0))
    cv.rect(hx0 + 3, hy1 - 8, hx0 + 13, hy1 - 2, K("papel", 1)); cv.hline(hx0 + 3, hx0 + 13, hy1 - 8, K("papel", 2))   # algo envuelto
    cv.rect(hx0 + 15, hy1 - 6, hx1 - 3, hy1 - 1, K("granate", 3)); cv.hline(hx0 + 15, hx1 - 3, hy1 - 6, K("granate", 4))  # un ladrillo dentro
    cv.rect(hx1 - 2, hy0 + 8, hx1 + 4, hy0 + 12, K("granate", 4)); cv.hline(hx1 - 2, hx1 + 4, hy0 + 8, K("granate", 5))  # uno salido
    # repisa a la derecha con trastos
    cv.rect(340, 56, 376, 59, K("madera", 3)); cv.hline(340, 376, 59, K("madera", 0))
    cv.rect(344, 46, 350, 56, K("ocre", 1)); cv.rect(354, 50, 362, 56, K("gris", 3)); cv.rect(366, 48, 370, 56, K("granate", 2))
    # tubo de la cerveza que baja del pub
    cv.rect(360, WT, 363, 92, K("ocre", 2)); cv.vline(360, WT, 92, K("ocre", 3))
    cv.rect(354, 64, 368, 70, K("ocre", 1)); cv.px(366, 66, K("ocre", 4))
    # telaraña en la esquina
    cv.d.line([(X1 - 1, WT + 4), (X1 - 18, WT + 4)], fill=K("papel", 1)); cv.d.line([(X1 - 1, WT + 4), (X1 - 14, WT + 18)], fill=K("papel", 1))
    cv.d.line([(X1 - 1, WT + 4), (X1 - 4, WT + 22)], fill=K("papel", 1)); cv.d.line([(X1 - 10, WT + 4), (X1 - 3, WT + 14)], fill=K("papel", 0))
    P.zocalo(cv, X0, X1, WB, rampa="granate", base=1, alto=3)
    # suelo: losas de piedra irregulares
    cv.rect(X0, WB, X1, FB, K("madera", 1))
    for fila, y in enumerate(range(WB, FB, 12)):
        x = X0 - (fila % 3) * 7
        while x < X1:
            w = rnd.randint(14, 26)
            r, b = rnd.choice([("madera", 2), ("madera", 2), ("madera", 1), ("madera", 3)])
            cv.rect(max(X0, x + 1), y + 1, min(X1, x + w), min(FB, y + 11), K(r, b))
            cv.hline(max(X0, x + 1), min(X1, x + w), y + 1, K(r, b + 1))
            x += w
    P.manchas(cv, X0, WB, X1, FB, K("madera", 1), n=260, semilla=8)
    # ladrillos sueltos en el suelo, bajo el hueco
    for (bx, by) in ((304, 96), (314, 100)):
        cv.rect(bx, by, bx + 8, by + 4, K("granate", 3)); cv.hline(bx, bx + 8, by, K("granate", 4)); cv.hline(bx, bx + 8, by + 4, K("madera", 0))
    escalera_mano(cv, 118, WT, 146, 100)
    # barriles apilados a la izquierda
    barril(cv, 106, 122); barril(cv, 128, 124)
    barril(cv, 106, 152); barril(cv, 128, 154)
    barril(cv, 116, 104, w=20, h=22)                                                        # uno encima
    cv.rect(130, 140, 134, 143, K("gris", 4)); cv.px(132, 143, K("ocre", 3))                # espita
    # cajas y sacos al fondo a la derecha
    for (cx, cy) in ((340, 100), (352, 112)):
        cv.rect(cx, cy, cx + 22, cy + 16, K("madera", 3)); cv.hline(cx, cx + 22, cy, K("madera", 4))
        cv.frame(cx, cy, cx + 22, cy + 16, K("madera", 1)); cv.d.line([(cx, cy), (cx + 22, cy + 16)], fill=K("madera", 1))
    # la mesa y sus cuatro sillas desparejadas
    silla(cv, 232, 124, 248, 136, "arriba", "granate", 3)
    silla(cv, 180, 150, 194, 166, "izq", "madera", 5)
    silla(cv, 286, 150, 300, 166, "der", "ocre", 1)
    mx0, my0, mx1, my1 = 196, 140, 284, 170
    cv.rect(mx0 + 4, my1 + 2, mx1 + 6, my1 + 8, K("madera", 0))                             # sombra
    cv.rect(mx0, my0, mx1, my1 - 6, K("madera", 4)); cv.frame(mx0, my0, mx1, my1 - 6, K("madera", 2))
    cv.hline(mx0 + 1, mx1 - 1, my0 + 1, K("madera", 5))
    for k in (my0 + 8, my0 + 16):
        cv.hline(mx0 + 1, mx1 - 1, k, K("madera", 3))
    cv.rect(mx0, my1 - 6, mx1, my1, K("madera", 3)); cv.hline(mx0, mx1, my1 - 1, K("madera", 1))
    for xx in (mx0 + 2, mx1 - 5):
        cv.rect(xx, my1, xx + 3, my1 + 6, K("madera", 2))
    # sobre la mesa: dos jarras, un papel doblado, cera derramada
    for (jx, jy) in ((212, 148), (262, 150)):
        cv.rect(jx, jy, jx + 5, jy + 7, K("ocre", 2)); cv.hline(jx, jx + 5, jy, K("papel", 3)); cv.vline(jx + 5, jy + 2, jy + 5, K("ocre", 1))
    cv.poly([(248, 154), (260, 152), (262, 160), (250, 162)], K("papel", 3)); cv.d.line([(254, 153), (256, 161)], fill=K("papel", 1))
    cv.ellipse(VX - 5, VY + 2, VX + 6, VY + 6, K("papel", 3))
    cv.rect(VX - 2, VY - 4, VX + 3, VY + 4, K("papel", 4)); cv.vline(VX + 2, VY - 4, VY + 4, K("papel", 2))   # la vela
    cv.px(VX, VY - 5, K("gris", 0))
    cv.rect(VX - 1, VY - 9, VX + 2, VY - 5, K("ocre", 4)); cv.px(VX, VY - 10, K("ocre", 3)); cv.px(VX, VY - 7, K("papel", 4))
    cv.add_emissive(VX - 1, VY - 10, VX + 2, VY - 5)
    silla(cv, 232, 172, 248, 186, "abajo", "madera", 1)
    # muros (abajo, cerrado)
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.vline(X0 - 1, WT, FB, K("gris", 4)); cv.vline(X1, WT, FB, K("gris", 4))
    cv.rect(X0 - 12, FB, X1 + 12, FB + 12, K("gris", 3)); cv.hline(X0, X1, FB, K("gris", 4))
    # luz: solo la vela
    cv.add_light(X0 - 12, WT - 12, X1 + 12, FB + 12, -1)

    def vela(x, y):
        if not (X0 <= x < X1 and WT <= y < FB):
            return 0
        d = ((x - VX) ** 2 + ((y - VY) * 1.25) ** 2) ** 0.5
        return 3 if d < 30 else (2 if d < 64 else (1 if d < 104 else (0 if d < 150 else -1)))
    cv.add_light_fn(vela)
    cv.glow_rgb = K("rojo", 5)
    cv.add_glow_suave(VX, VY - 6, 210, 0.2, squash=1.1, pasos=8, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    cv.light = [[0] * W for _ in range(H)]
    cv.glow = [[0.0] * W for _ in range(H)]
    cv.glow_rgb = K("ocre", 4)
    cv.add_glow_suave(VX, VY - 6, 110, 0.26, squash=1.1, pasos=8, limite=(X0, WT, X1, FB))
    cv.add_glow_suave(VX, VY - 7, 16, 0.5, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    # un hilo de luz que cae por la trampilla
    cv.light = [[0] * W for _ in range(H)]
    cv.glow = [[0.0] * W for _ in range(H)]
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(132, WT, 46, 0.22, squash=0.8, limite=(X0, WT - 12, X1, FB))
    cv.bake_lighting()
    return cv
