"""A3 — Lavabos de la planta tres del Miniver: azulejo blanco, frío, un grifo que gotea.

Cuatro lavamanos bajo un espejo largo, tres retretes en el rincón y una telepantalla pequeña sobre la puerta,
girada hacia los lavamanos. Bajo el último lavamanos, un panel de registro que no está del todo encajado.

Variante "vaho": alguien ha dejado correr el agua caliente; el espejo y la pantalla se empañan.
"""
import math
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 80, 400
WT, WB, FB = 20, 92, 236
LAVAMANOS = (108, 148, 188, 228)


def azulejo_pared(cv, x0, y0, x1, y1):
    cv.rect(x0, y0, x1, y1, K("gris", 9))
    for y in range(y0, y1, 8):
        cv.hline(x0, x1, y, K("gris", 7))
    for x in range(x0, x1, 8):
        cv.vline(x, y0, y1, K("gris", 7))
    for y in range(y0 + 1, y1, 8):                                                          # brillo del esmalte
        for x in range(x0 + 1, x1, 8):
            cv.px(x, y, K("gris", 10))


def lavamanos(cv, x0, rnd, idx):
    x1 = x0 + 28
    # grifo y jabonera en la pared
    cv.rect(x0 + 12, 74, x0 + 16, 78, K("gris", 6)); cv.rect(x0 + 13, 78, x0 + 15, 84, K("gris", 7))
    cv.px(x0 + 13, 78, K("gris", 10)); cv.rect(x0 + 10, 72, x0 + 18, 74, K("gris", 5))
    # pila: cara de arriba (el seno) y frente redondeado
    cv.rect(x0 + 2, 100, x1 + 2, 104, K("gris", 6))                                         # sombra en el suelo
    cv.rect(x0, 84, x1, 98, K("papel", 4)); cv.frame(x0, 84, x1, 98, K("gris", 7))
    cv.ellipse(x0 + 4, 86, x1 - 4, 96, K("gris", 8), outline=K("gris", 7))
    cv.ellipse(x0 + 7, 89, x1 - 7, 95, K("gris", 7))
    cv.px(x0 + 14, 92, K("gris", 3))                                                         # desagüe
    cv.rect(x0, 98, x1, 102, K("gris", 9)); cv.hline(x0 + 1, x1 - 1, 102, K("gris", 6))      # canto frontal
    cv.hline(x0 + 1, x1 - 1, 98, K("papel", 4))
    if idx == 1:                                                                             # un grifo que gotea
        cv.px(x0 + 14, 86, K("cielo", 5)); cv.px(x0 + 14, 88, K("cielo", 4))
    # sifón bajo la pila
    cv.rect(x0 + 12, 102, x0 + 16, 104, K("gris", 5))


def espejo(cv, x0, y0, x1, y1, vaho):
    cv.rect(x0 + 2, y0 + 2, x1 + 2, y1 + 2, K("gris", 6))
    cv.rect(x0 - 2, y0 - 2, x1 + 2, y1 + 2, K("gris", 4)); cv.hline(x0 - 2, x1 + 2, y0 - 2, K("gris", 6))
    if not vaho:
        cv.rect(x0, y0, x1, y1, K("cielo", 4))
        cv.rect(x0, y1 - 10, x1, y1, K("cielo", 3))                                            # el reflejo del cuarto
        for k in range(x0 + 20, x1 - 10, 20):                                                # retretes reflejados
            cv.rect(k, y1 - 18, k + 12, y1 - 6, K("cielo", 2)); cv.vline(k + 6, y1 - 18, y1 - 6, K("cielo", 1))
        for k in range(x0 + 6, x1, 26):                                                      # brillos en diagonal
            cv.d.line([(k, y1 - 2), (k + 14, y0 + 2)], fill=K("cielo", 6))
            cv.d.line([(k + 4, y1 - 2), (k + 18, y0 + 2)], fill=K("cielo", 5))
        cv.px(x0 + 30, y0 + 6, K("cielo", 2)); cv.px(x1 - 40, y0 + 22, K("cielo", 2))         # manchas del azogue
    else:
        rnd = random.Random(5)
        cv.rect(x0, y0, x1, y1, K("gris", 9))
        for k in range(x0 + 20, x1 - 10, 20):                                                # el reflejo, apenas
            cv.rect(k, y1 - 18, k + 12, y1 - 6, K("gris", 8))
        for _ in range(70):                                                                  # vaho en nubes
            ex, ey = rnd.randint(x0 - 4, x1 - 4), rnd.randint(y0 - 3, y1 - 3)
            ew, eh = rnd.randint(6, 16), rnd.randint(3, 7)
            a, b, c, d = max(x0, ex), max(y0, ey), min(x1, ex + ew), min(y1, ey + eh)
            if c - a > 2 and d - b > 2:
                cv.ellipse(a, b, c, d, K("gris", 10))
        for k in range(x0 + 7, x1 - 4, 11):                                                  # gotas que resbalan
            L = rnd.randint(8, 24)
            sy = rnd.randint(y0 + 2, y0 + 12)
            cv.vline(k, sy, min(y1, sy + L), K("cielo", 5)); cv.px(k, min(y1 - 1, sy + L), K("cielo", 3))


def telepantalla_puerta(cv, x0, y0, x1, y1, vaho):
    """Telepantalla pequeña sobre el marco, girada hacia los lavamanos (se le ve el costado derecho)."""
    cv.rect(x0 + 2, y0 + 2, x1 + 2, y1 + 2, K("gris", 6))
    cv.rect(x0, y0, x1 - 4, y1, K("gris", 2)); cv.frame(x0, y0, x1 - 4, y1, K("gris", 1))
    cv.poly([(x1 - 4, y0), (x1 - 1, y0 + 2), (x1 - 1, y1 - 2), (x1 - 4, y1 - 1)], K("gris", 1))
    sx0, sy0, sx1, sy1 = x0 + 2, y0 + 2, x1 - 6, y1 - 3
    if vaho:
        cv.rect(sx0, sy0, sx1, sy1, K("gris", 8))
        cv.rect(sx0 + 3, sy0 + 2, sx1 - 3, sy1 - 2, K("tele", 5))
        cv.rect(sx0, sy0 + 1, sx1, sy1 - 1, K("gris", 9))
        cv.ellipse(sx0 + 1, sy0, sx0 + 9, sy1, K("gris", 10)); cv.ellipse(sx0 + 8, sy0 + 2, sx1, sy1, K("gris", 10))
        cv.px(sx0 + 7, sy0 + 4, K("tele", 5)); cv.px(sx0 + 11, sy0 + 4, K("tele", 5))
    else:
        cv.rect(sx0, sy0, sx1, sy1, K("tele", 2))
        cx = (sx0 + sx1) // 2 - 2
        cv.ellipse(cx - 4, sy0 + 1, cx + 5, sy1, K("tele", 4))                                # una cara, mirando a la izquierda
        cv.hline(cx - 3, cx, sy0 + 3, K("tele", 6))
        cv.hline(cx - 2, cx + 2, sy1 - 2, K("tele", 1))
    cv.px(x1 - 6, y1 - 1, K("rojo", 4))
    cv.vline((x0 + x1) // 2, y1, y1 + 2, K("gris", 3))                                         # soporte
    cv.add_emissive(sx0, sy0, sx1, sy1)


def retretes(cv, x0, y0, x1, y1, rnd):
    alto = 30
    n = 3
    wcub = (x1 - x0) // n
    # interior de cada cubículo, visto desde arriba
    for i in range(n):
        cx0 = x0 + i * wcub
        cv.rect(cx0 + 3, y0, cx0 + wcub, y1, K("gris", 6))
        for yy in range(y0, y1, 8):
            cv.hline(cx0 + 3, cx0 + wcub, yy, K("gris", 5))
        # cisterna contra el muro de abajo y taza
        tx = cx0 + wcub // 2 - 6
        cv.rect(tx - 1, y1 - 12, tx + 14, y1 - 2, K("papel", 4)); cv.frame(tx - 1, y1 - 12, tx + 14, y1 - 2, K("gris", 7))
        cv.hline(tx, tx + 13, y1 - 11, K("gris", 10)); cv.rect(tx + 10, y1 - 10, tx + 12, y1 - 8, K("gris", 6))
        cv.ellipse(tx, y1 - 32, tx + 13, y1 - 12, K("papel", 4), outline=K("gris", 7))
        cv.ellipse(tx + 3, y1 - 28, tx + 10, y1 - 16, K("cielo", 4), outline=K("gris", 8))
        cv.rect(cx0 + wcub - 6, y0 + 20, cx0 + wcub - 2, y0 + 26, K("papel", 3))                 # rollo de papel
        cv.hline(cx0 + wcub - 6, cx0 + wcub - 2, y0 + 20, K("papel", 4))
    # tabiques entre cubículos (cantos vistos desde arriba)
    for i in range(n + 1):
        px_ = min(x0 + i * wcub, x1 - 3)
        cv.rect(px_, y0 - alto, px_ + 3, y1, K("gris", 5)); cv.vline(px_, y0 - alto, y1, K("gris", 7))
        cv.vline(px_ + 2, y0 - alto, y1, K("gris", 3))
    # frente con las puertecitas (se ve su cara interior)
    cv.rect(x0, y0 - alto, x1, y0, K("gris", 5))
    cv.rect(x0, y0 - alto - 2, x1, y0 - alto + 1, K("gris", 7))                                # canto superior
    for i in range(n):
        dx0 = x0 + i * wcub + 4
        dx1 = dx0 + wcub - 5
        if i == 2:                                                                             # la tercera, entornada
            cv.rect(dx0, y0 - alto + 2, dx1, y0, K("gris", 2))
            cv.poly([(dx0, y0 - alto + 2), (dx0 + 10, y0 - alto + 8), (dx0 + 10, y0 + 8), (dx0, y0 - 2)], K("tela", 3))
            cv.vline(dx0 + 10, y0 - alto + 8, y0 + 8, K("tela", 1))
            continue
        cv.rect(dx0, y0 - alto + 2, dx1, y0 - 3, K("tela", 3)); cv.frame(dx0, y0 - alto + 2, dx1, y0 - 3, K("tela", 1))
        cv.hline(dx0 + 1, dx1 - 1, y0 - alto + 3, K("tela", 4))
        cv.rect(dx0 + 3, y0 - alto + 6, dx1 - 3, y0 - 7, K("tela", 2))
        cv.rect(dx0, y0 - 3, dx1, y0, K("gris", 6))                                            # hueco bajo la puerta
        cv.rect(dx1 - 5, y0 - alto + 14, dx1 - 2, y0 - alto + 17, K("gris", 7))                 # pestillo
        cv.px(dx1 - 4, y0 - alto + 13, K("rojo", 3) if i == 0 else K("gris", 8))              # ocupado / libre
        cv.vline(dx0 + 2, y0 - alto + 8, y0 - alto + 14, K("gris", 6))                         # colgador


def dibujar(variante=None):
    vaho = variante == "vaho"
    rnd = random.Random(303)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    azulejo_pared(cv, X0, WT, X1, WB)
    cv.rect(X0, 76, X1, 80, K("gris", 4)); cv.hline(X0, X1, 76, K("gris", 5))                 # cenefa de azulejo oscuro
    cv.rect(X0, WT, X1, WT + 3, K("gris", 6))
    # fluorescente
    cv.rect(220, 10, 300, 15, K("gris", 2)); cv.rect(222, 11, 298, 14, K("papel", 4)); cv.add_emissive(222, 11, 298, 14)
    espejo(cv, 104, 34, 260, 70, vaho)
    for x0 in LAVAMANOS:
        cv.rect(x0 + 10, 72, x0 + 18, 74, K("gris", 5))
    # puerta, telepantalla y percha
    P.puerta(cv, 330, 40, w=32, h=52, rampa="gris", base=5)
    cv.rect(318, 42, 326, 50, K("gris", 6)); cv.frame(318, 42, 326, 50, K("gris", 4))           # percha
    cv.d.line([(322, 44), (322, 48), (324, 50)], fill=K("gris", 2)); cv.px(320, 47, K("gris", 2))
    telepantalla_puerta(cv, 334, 24, 358, 38, vaho)
    # dispensador de toallas y cartel
    cv.rect(276, 44, 296, 66, K("gris", 6)); cv.frame(276, 44, 296, 66, K("gris", 4)); cv.rect(280, 64, 292, 68, K("papel", 3))
    cv.rect(372, 34, 396, 56, K("papel", 3)); cv.frame(372, 34, 396, 56, K("gris", 5))
    cv.text(374, 36, "AGUA", K("azul", 2)); cv.text(374, 42, "UNA", K("gris", 3)); cv.text(374, 48, "VEZ", K("gris", 3))
    P.zocalo(cv, X0, X1, WB, rampa="gris", base=6, alto=3)
    # suelo de baldosín
    P.baldosas(cv, X0, WB, X1, FB, K("gris", 8), K("gris", 7), t=8, linea=K("gris", 6))
    cv.ellipse(232, 150, 248, 158, K("gris", 5)); cv.ellipse(234, 151, 246, 157, K("gris", 3))   # sumidero
    for k in range(236, 246, 3):
        cv.vline(k, 152, 156, K("gris", 6))
    cv.ellipse(150, 106, 192, 116, K("cielo", 5)); cv.ellipse(162, 108, 178, 113, K("cielo", 6))   # charco bajo el grifo
    for x0 in LAVAMANOS:
        lavamanos(cv, x0, rnd, LAVAMANOS.index(x0))
    # panel de registro mal encajado bajo el cuarto lavamanos
    cv.rect(232, 104, 252, 110, K("gris", 4))
    cv.rect(233, 101, 253, 109, K("gris", 7)); cv.frame(233, 101, 253, 109, K("gris", 5))
    cv.hline(233, 253, 109, K("gris", 2)); cv.vline(253, 102, 110, K("gris", 2))
    cv.px(235, 103, K("gris", 4)); cv.px(250, 103, K("gris", 4)); cv.px(235, 107, K("gris", 4))  # falta un tornillo
    cv.px(245, 112, K("gris", 4)); cv.px(246, 112, K("gris", 5))                               # el tornillo, en el suelo
    # papelera
    P.papelera(cv, 278, 98)
    retretes(cv, 300, 168, 396, 236, rnd)
    # muros (abajo, cerrado)
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.vline(X0 - 1, WT, FB, K("gris", 4)); cv.vline(X1, WT, FB, K("gris", 4))
    cv.rect(X0 - 12, FB, X1 + 12, FB + 12, K("gris", 3)); cv.hline(X0, X1, FB, K("gris", 4))
    # luz fría y plana del fluorescente
    cv.glow_rgb = K("cielo", 6)
    cv.add_glow_suave(260, 60, 220, 0.18, squash=1.2, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    cv.light = [[0] * W for _ in range(H)]
    cv.glow = [[0.0] * W for _ in range(H)]
    if vaho:
        cv.glow_rgb = K("gris", 10)
        for x0 in LAVAMANOS:
            cv.add_glow_suave(x0 + 14, 74, 34, 0.5, squash=0.8, pasos=6, limite=(X0, WT, X1, FB))
        cv.add_glow_suave(182, 54, 110, 0.35, squash=1.6, pasos=6, limite=(X0, WT, X1, FB))
        cv.add_glow_suave(346, 31, 22, 0.4, limite=(X0, WT, X1, FB))
    else:
        cv.glow_rgb = K("tele", 4)
        cv.add_glow_suave(344, 31, 30, 0.2, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    if vaho:                                                                                 # vapor que sube de las pilas
        for x0 in LAVAMANOS:
            for _ in range(110):
                t = rnd.random() ** 1.3                                                      # más denso abajo
                y = int(86 - t * 50)
                ancho = 6 + t * 16
                x = int(x0 + 14 + rnd.uniform(-ancho, ancho) + 4 * math.sin(y * 0.2 + x0))
                if rnd.random() > t * 0.85:
                    cv.hline(x, x + rnd.choice([2, 3]), y, K("gris", 10) if rnd.random() < 0.7 else K("papel", 4))
    return cv
