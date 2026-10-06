"""A3 — Sala de calderas del Minipax: sótano oscuro y caluroso.

Dos calderas de hierro remachado; por la rejilla de la grande se ven papeles ardiendo (lo que se «olvida» aquí abajo
se olvida para siempre). Tuberías por todas partes, carbón en un rincón y, al fondo, el montacargas viejo con su reja
de tijera, cubierto de polvo: nadie lo usa… o eso parece.
"""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 20, 92, 246

PERFIL = [1, 2, 3, 4, 5, 5, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 0]      # sombreado de cilindro (de izquierda a derecha)


def muro_bloques(cv, x0, y0, x1, y1, rnd):
    """Bloques de hormigón con manchas de humedad y hollín."""
    cv.rect(x0, y0, x1, y1, K("gris", 2))
    for fila, y in enumerate(range(y0, y1, 8)):
        cv.hline(x0, x1, y, K("gris", 1))
        off = (fila % 2) * 12
        for x in range(x0 - off, x1, 24):
            if x > x0:
                cv.vline(x, y, min(y + 8, y1), K("gris", 1))
            if rnd.random() < 0.25:
                cv.hline(max(x0, x + 2), min(x1, x + rnd.randint(6, 18)), y + 1, K("gris", 3))
    for _ in range(14):                                               # hollín que baja en chorretones
        sx, sy = rnd.randint(x0, x1 - 4), rnd.randint(y0, y1 - 20)
        for k in range(rnd.randint(6, 20)):
            cv.px(sx + rnd.choice([0, 0, 1]), sy + k, K("gris", 1))


def tubo_h(cv, x0, x1, y, g=5, base=4, rampa="gris", bridas=40):
    cv.rect(x0, y, x1, y + g, K(rampa, base))
    cv.hline(x0, x1, y, K(rampa, base + 2)); cv.hline(x0, x1, y + 1, K(rampa, base + 1))
    cv.hline(x0, x1, y + g - 1, K(rampa, base - 2))
    cv.hline(x0, x1, y + g, K("gris", 1))                                  # sombra en la pared
    if bridas:
        for bx in range(x0 + 8, x1 - 4, bridas):
            cv.rect(bx, y - 1, bx + 3, y + g + 1, K(rampa, base + 1)); cv.vline(bx + 2, y - 1, y + g + 1, K(rampa, base - 1))


def tubo_v(cv, x, y0, y1, g=5, base=4, rampa="gris", bridas=30):
    cv.rect(x, y0, x + g, y1, K(rampa, base))
    cv.vline(x, y0, y1, K(rampa, base + 2)); cv.vline(x + 1, y0, y1, K(rampa, base + 1))
    cv.vline(x + g - 1, y0, y1, K(rampa, base - 2))
    cv.vline(x + g, y0, y1, K("gris", 1))
    if bridas:
        for by in range(y0 + 6, y1 - 4, bridas):
            cv.rect(x - 1, by, x + g + 1, by + 3, K(rampa, base + 1)); cv.hline(x - 1, x + g + 1, by + 2, K(rampa, base - 1))


def volante(cv, cx, cy, r=4):
    """Válvula de volante, de hierro pintado de rojo (el único rojo de la sala)."""
    cv.ellipse(cx - r, cy - r, cx + r + 1, cy + r + 1, None, outline=K("rojo", 2))
    cv.hline(cx - r + 1, cx + r, cy, K("rojo", 3)); cv.vline(cx, cy - r + 1, cy + r, K("rojo", 3))
    cv.px(cx, cy, K("gris", 5)); cv.px(cx - r + 1, cy - 2, K("rojo", 4))


def cilindro(cv, x0, y0, x1, y1, base=1):
    w = x1 - x0
    for x in range(x0, x1):
        i = PERFIL[min(len(PERFIL) - 1, (x - x0) * len(PERFIL) // w)]
        cv.vline(x, y0, y1, K("gris", base + i))


def caldera(cv, x0, top, x1, y1, rnd, cupula=14):
    """Caldera vertical: cúpula, cuerpo cilíndrico con bandas remachadas y zócalo de ladrillo."""
    w = x1 - x0
    cv.rect(x1, top + cupula + 6, x1 + 6, y1 + 2, K("gris", 0))                       # sombra a la derecha
    # cúpula
    cv.ellipse(x0, top, x1, top + 2 * cupula, K("gris", 3))
    for x in range(x0, x1):
        i = PERFIL[min(len(PERFIL) - 1, (x - x0) * len(PERFIL) // w)]
        for y in range(top, top + cupula + 2):
            if cv.img.getpixel((x, y)) == K("gris", 3):
                cv.px(x, y, K("gris", 1 + i + (1 if y < top + 5 else 0)))
    cv.ellipse(x0, top, x1, top + 2 * cupula, None, outline=K("gris", 1))
    cilindro(cv, x0, top + cupula, x1, y1 - 8, base=1)
    cv.vline(x0, top + cupula, y1 - 8, K("gris", 1)); cv.vline(x1 - 1, top + cupula, y1 - 8, K("gris", 0))
    # bandas remachadas
    for by in range(top + cupula + 10, y1 - 14, 22):
        cv.hline(x0, x1, by, K("gris", 1)); cv.hline(x0, x1, by + 1, K("gris", 5))
        for rx in range(x0 + 4, x1 - 2, 6):
            cv.px(rx, by + 3, K("gris", 6)); cv.px(rx, by + 4, K("gris", 1))
    # zócalo de ladrillo
    cv.rect(x0 - 4, y1 - 8, x1 + 4, y1, K("granate", 2))
    cv.hline(x0 - 4, x1 + 4, y1 - 8, K("granate", 4))
    for k, yy in enumerate(range(y1 - 7, y1, 3)):
        cv.hline(x0 - 4, x1 + 4, yy + 2, K("granate", 1))
        for xx in range(x0 - 4 + (k % 2) * 4, x1 + 4, 8):
            cv.vline(xx, yy, yy + 2, K("granate", 1))
    # manchas de óxido
    for by in range(top + cupula + 10, y1 - 14, 22):                               # óxido bajo los remaches
        for _ in range(w // 10):
            x = rnd.randint(x0 + 3, x1 - 4)
            for k in range(rnd.randint(1, 5)):
                cv.px(x, by + 5 + k, K("granate", rnd.choice([1, 2])))


def manometro(cv, cx, cy):
    cv.ellipse(cx - 6, cy - 6, cx + 7, cy + 7, K("ocre", 1))
    cv.ellipse(cx - 5, cy - 5, cx + 6, cy + 6, K("papel", 3), outline=K("ocre", 2))
    for a, b in ((-3, -3), (0, -4), (3, -3), (4, 0)):
        cv.px(cx + a, cy + b, K("gris", 3))
    cv.d.line([(cx, cy), (cx + 3, cy - 3)], fill=K("rojo", 3))                       # la aguja, en la zona roja
    cv.px(cx, cy, K("gris", 1))


def rejilla_fuego(cv, x0, y0, x1, y1, rnd):
    """La boca del hogar: barrotes de hierro y, detrás, papeles ardiendo."""
    cv.rect(x0 - 4, y0 - 5, x1 + 4, y1 + 3, K("gris", 1))                             # marco de fundición
    cv.hline(x0 - 4, x1 + 4, y0 - 5, K("gris", 4)); cv.rect(x0 - 4, y1 + 1, x1 + 4, y1 + 3, K("gris", 0))
    for bx in (x0 - 2, x1 + 1):
        cv.px(bx, y0 - 3, K("gris", 6)); cv.px(bx, y1 - 1, K("gris", 6))
    cv.rect(x0, y0, x1, y1, K("rojo", 1))
    # llamas: columnas que se afinan hacia arriba
    for x in range(x0, x1):
        h = rnd.randint(6, y1 - y0 - 3)
        for k in range(h):
            t = k / h
            c = K("ocre", 4) if k < 2 else K("ocre", 3) if t < 0.3 else K("rojo", 5) if t < 0.6 else K("rojo", 3)
            cv.px(x, y1 - 1 - k, c)
    # papeles retorciéndose en el fuego
    for (pts, quemado) in (([(x0 + 2, y1 - 10), (x0 + 10, y1 - 13), (x0 + 12, y1 - 7), (x0 + 4, y1 - 5)], False),
                           ([(x0 + 13, y1 - 15), (x0 + 21, y1 - 13), (x0 + 19, y1 - 8), (x0 + 12, y1 - 10)], True),
                           ([(x0 + 21, y1 - 11), (x0 + 29, y1 - 12), (x0 + 30, y1 - 6), (x0 + 22, y1 - 5)], False)):
        cv.poly(pts, K("papel", 2) if quemado else K("papel", 4))
        cv.d.line([pts[0], pts[1]], fill=K("gris", 0))
        cv.d.line([pts[1], pts[2]], fill=K("ocre", 4))
        cv.d.line([pts[2], pts[3]], fill=K("gris", 1) if quemado else K("papel", 2))
        mx, my = sum(p[0] for p in pts) // 4, sum(p[1] for p in pts) // 4
        cv.hline(mx - 3, mx + 2, my, K("gris", 4)); cv.hline(mx - 2, mx + 3, my + 2, K("gris", 4))
    for _ in range(10):
        cv.px(rnd.randint(x0, x1 - 1), rnd.randint(y0, y1 - 10), K("ocre", 4))       # pavesas
    # barrotes
    for bx in range(x0 + 3, x1 - 1, 7):
        cv.vline(bx, y0, y1, K("gris", 0)); cv.vline(bx + 1, y0, y1, K("gris", 2))
    cv.hline(x0, x1, y0, K("gris", 0)); cv.hline(x0, x1, y0 + 1, K("gris", 2))
    cv.add_emissive(x0, y0, x1, y1)


def montacargas(cv, x0, y0, x1, y1, rnd):
    cv.rect(x0 - 3, y0 - 2, x1 + 3, y1, K("gris", 3))                                 # marco
    cv.vline(x0 - 3, y0 - 2, y1, K("gris", 5)); cv.hline(x0 - 3, x1 + 3, y0 - 2, K("gris", 5))
    cv.vline(x1 + 2, y0 - 2, y1, K("gris", 1))
    cv.rect(x0, y0, x1, y1, K("gris", 0))                                               # el pozo
    for yy in range(y0 + 6, y1, 9):                                                     # fondo de la cabina
        cv.hline(x0 + 2, x1 - 2, yy, K("gris", 1))
    for cx in (x0 + 30, x0 + 50):                                                      # cables
        cv.vline(cx, y0, y1 - 22, K("gris", 3)); cv.vline(cx + 1, y0, y1 - 22, K("gris", 1))
    cv.rect(x0 + 2, y1 - 24, x1 - 2, y1 - 20, K("gris", 2)); cv.hline(x0 + 2, x1 - 2, y1 - 24, K("gris", 4))  # techo de la cabina
    cv.rect(x0 + 4, y1 - 20, x1 - 4, y1, K("gris", 1))                                # cabina en sombra
    cv.rect(x0 + 6, y1 - 10, x0 + 18, y1 - 2, K("ocre", 1)); cv.hline(x0 + 6, x0 + 18, y1 - 10, K("ocre", 2))  # una caja olvidada
    # carril de la reja
    cv.rect(x0, y0, x1, y0 + 3, K("gris", 4)); cv.hline(x0, x1, y0 + 3, K("gris", 1))
    cv.rect(x0, y1 - 3, x1, y1, K("gris", 4))
    # reja de tijera: montantes verticales y aspas en rombo
    paso = 8
    for bx in range(x0 + 2, x1, paso):
        cv.vline(bx, y0 + 3, y1 - 3, K("gris", 6)); cv.vline(bx + 1, y0 + 3, y1 - 3, K("gris", 3))
    seg = 10
    for bx in range(x0 + 2, x1 - paso + 1, paso):
        for sy in range(y0 + 4, y1 - 4, seg):
            cv.d.line([(bx + 1, sy), (bx + paso, min(y1 - 4, sy + seg))], fill=K("gris", 5))
            cv.d.line([(bx + paso, sy), (bx + 1, min(y1 - 4, sy + seg))], fill=K("gris", 4))
            cv.px(bx + paso // 2 + 1, sy + seg // 2, K("gris", 7))
    cv.rect(x1 - 6, y0 + 28, x1 - 2, y0 + 38, K("ocre", 2)); cv.px(x1 - 4, y0 + 30, K("ocre", 4))   # tirador de latón
    # polvo y telarañas
    for _ in range(90):
        x, y = rnd.randint(x0, x1 - 1), rnd.randint(y0, y1 - 1)
        cv.px(x, y, K("gris", rnd.choice([4, 5])))
    cv.hline(x0, x1, y0 + 3, K("gris", 6))
    cv.d.line([(x0, y0 + 14), (x0 + 12, y0 + 4)], fill=K("gris", 6))
    cv.d.line([(x0, y0 + 9), (x0 + 6, y0 + 4)], fill=K("gris", 5))
    cv.d.line([(x0 + 4, y0 + 4), (x0 + 3, y0 + 12)], fill=K("gris", 5))


def chapa(cv, x0, y0, x1, y1):
    cv.rect(x0, y0, x1, y1, K("gris", 4)); cv.frame(x0, y0, x1, y1, K("gris", 2))
    cv.hline(x0, x1, y0, K("gris", 5))
    for y in range(y0 + 2, y1 - 1, 3):
        for x in range(x0 + 2 + (y % 2) * 3, x1 - 2, 6):
            cv.hline(x, x + 2, y, K("gris", 6))
    for x in (x0 + 1, x1 - 2):
        cv.px(x, y0 + 1, K("gris", 7)); cv.px(x, y1 - 2, K("gris", 7))


def palanca(cv, x0, y0, x1, y1):
    cv.rect(x0 + 1, y0 + 1, x1 + 1, y1 + 1, K("gris", 0))
    cv.rect(x0, y0, x1, y1, K("ocre", 1)); cv.frame(x0, y0, x1, y1, K("ocre", 0))
    cv.hline(x0, x1, y0, K("ocre", 2))
    cv.rect(x0 + 4, y0 + 4, x0 + 6, y1 - 3, K("gris", 0))                              # ranura
    cv.d.line([(x0 + 5, y1 - 8), (x0 + 8, y0 + 3)], fill=K("ocre", 3))                # brazo (abajo: parado)
    cv.d.line([(x0 + 6, y1 - 8), (x0 + 9, y0 + 3)], fill=K("ocre", 2))
    cv.rect(x0 + 7, y0 + 1, x0 + 11, y0 + 5, K("ocre", 3)); cv.px(x0 + 8, y0 + 2, K("ocre", 4))
    cv.text(x0 + 1, y1 - 6, "S", K("ocre", 3)); cv.text(x0 + 6, y1 - 6, "B", K("ocre", 3))


def saco(cv, x, y, w, h, rnd):
    cv.ellipse(x + 2, y + h - 4, x + w + 3, y + h + 2, K("gris", 1))                  # sombra
    cv.ellipse(x, y + 4, x + w, y + h, K("papel", 1), outline=K("papel", 0))
    cv.ellipse(x + 2, y + 6, x + w // 2 + 1, y + h - 3, K("papel", 2))
    cv.rect(x + w // 2 - 3, y, x + w // 2 + 3, y + 6, K("papel", 1)); cv.frame(x + w // 2 - 3, y, x + w // 2 + 3, y + 6, K("papel", 0))
    cv.hline(x + w // 2 - 3, x + w // 2 + 3, y + 5, K("madera", 3))                   # cordel
    cv.px(x + w // 2 - 2, y + 1, K("papel", 2))
    for _ in range(w):                                                                # trama de arpillera
        cv.px(rnd.randint(x + 2, x + w - 3), rnd.randint(y + 7, y + h - 3), K("papel", 0))


def carbon(cv, x0, y0, x1, y1, rnd):
    cv.ellipse(x0 + 22, y0 + 8, x1 + 4, y1 + 3, K("gris", 1))                        # sombra
    cv.ellipse(x0 + 18, y0 + 6, x1, y1, K("gris", 0))
    cv.ellipse(x0 + 24, y0 + 4, x1 - 4, y1 - 8, K("gris", 1))
    cv.ellipse(x0 + 30, y0 + 6, x1 - 10, y1 - 16, K("gris", 2))
    for _ in range(120):                                                               # terrones
        x, y = rnd.randint(x0 + 18, x1 - 3), rnd.randint(y0 + 4, y1 - 2)
        if cv.img.getpixel((x, y)) in (K("gris", 0), K("gris", 1), K("gris", 2)):
            cv.rect(x, y, x + 3, y + 2, K("gris", 1)); cv.px(x, y, K("gris", 3)); cv.px(x + 2, y + 1, K("gris", 0))
    for _ in range(12):
        cv.px(rnd.randint(x0 + 30, x1 - 8), rnd.randint(y0 + 8, y1 - 10), K("gris", 5))     # brillos
    for _ in range(14):                                                                # carbón desparramado
        x, y = rnd.randint(x0 + 10, x1 + 8), rnd.randint(y1 - 4, y1 + 6)
        cv.rect(x, y, x + 2, y + 2, K("gris", 1)); cv.px(x, y, K("gris", 3))
    # pala clavada
    cv.d.line([(x1 - 6, y0 - 6), (x1 - 14, y0 + 12)], fill=K("madera", 3))
    cv.d.line([(x1 - 5, y0 - 6), (x1 - 13, y0 + 12)], fill=K("madera", 1))
    cv.rect(x1 - 8, y0 - 8, x1 - 3, y0 - 5, K("madera", 2))
    cv.poly([(x1 - 19, y0 + 11), (x1 - 10, y0 + 11), (x1 - 11, y0 + 19), (x1 - 18, y0 + 19)], K("gris", 4))
    cv.hline(x1 - 19, x1 - 10, y0 + 11, K("gris", 6))
    # sacos
    saco(cv, x0, y0, 18, 24, rnd)
    saco(cv, x0 + 10, y0 + 10, 18, 24, rnd)


def dibujar(variante=None):
    rnd = random.Random(1931)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    muro_bloques(cv, X0, WT, X1, WB, rnd)
    # banda de tuberías del techo
    cv.rect(X0, WT, X1, WT + 12, K("gris", 1))
    tubo_h(cv, X0, X1, WT + 1, g=5, base=4, bridas=48)
    tubo_h(cv, X0, X1, WT + 7, g=4, base=3, bridas=0)
    tubo_h(cv, 230, X1, 58, g=4, base=3, bridas=36)
    tubo_h(cv, 230, 330, 70, g=6, base=4, bridas=30)
    for vx in (244, 286):
        tubo_v(cv, vx, WT + 12, WB, g=5, base=4)
    tubo_v(cv, 306, WT + 12, 70, g=4, base=3)
    volante(cv, 297, 72); volante(cv, 262, 60)
    # cartel de aviso
    cv.rect(254, 36, 280, 50, K("papel", 2)); cv.frame(254, 36, 280, 50, K("papel", 0))
    cv.text(256, 38, "NO", K("rojo", 2)); cv.text(256, 44, "ABRIR", K("gris", 1))
    # el montacargas viejo y su palanca
    montacargas(cv, 340, 28, 420, WB, rnd)
    palanca(cv, 322, 56, 332, 80)
    tubo_v(cv, 426, WT + 12, WB, g=6, base=4)                                          # bajante de la esquina
    # suelo de losas de hormigón
    cv.rect(X0, WB, X1, FB, K("gris", 3))
    for fila, y in enumerate(range(WB, FB, 22)):
        cv.hline(X0, X1, y, K("gris", 2))
        for x in range(X0 + (fila % 2) * 18, X1, 36):
            cv.vline(x, y, min(FB, y + 22), K("gris", 2))
    for _ in range(9):                                                                # grietas
        x, y = rnd.randint(X0 + 10, X1 - 30), rnd.randint(WB + 20, FB - 10)
        for k in range(rnd.randint(6, 16)):
            x += rnd.choice([1, 1, 2]); y += rnd.choice([-1, 0, 1])
            cv.px(x, y, K("gris", 2))
    P.manchas(cv, X0, WB, X1, FB, K("gris", 2), n=500, semilla=4)
    P.manchas(cv, X0, WB, X1, FB, K("gris", 4), n=200, semilla=5)
    cv.ellipse(300, 196, 336, 206, K("gris", 2)); cv.ellipse(306, 198, 326, 204, K("gris", 1))   # mancha de aceite
    # sumidero
    cv.rect(268, 170, 284, 180, K("gris", 1)); cv.frame(268, 170, 284, 180, K("gris", 4))
    for k in range(270, 283, 3):
        cv.vline(k, 171, 179, K("gris", 0))
    chapa(cv, 340, WB, 420, 100)
    # tubería tendida a lo largo del muro derecho
    cv.rect(429, WB, 438, FB, K("gris", 1))
    tubo_v(cv, 428, WB, FB, g=8, base=4, bridas=34)
    for by in range(WB + 18, FB, 34):
        cv.rect(426, by, 440, by + 2, K("gris", 2))
    # tubería por el suelo que sale de la caldera B hacia la pared
    tubo_v(cv, 236, WB, 120, g=5, base=3, bridas=0)
    tubo_h(cv, 236, 280, 116, g=5, base=3, bridas=0)
    volante(cv, 262, 118)
    # calderas
    caldera(cv, 160, 44, 228, 150, rnd, cupula=10)
    cv.rect(182, 116, 206, 136, K("gris", 1)); cv.frame(182, 116, 206, 136, K("gris", 4))       # portezuela de B, cerrada
    cv.hline(184, 204, 133, K("rojo", 4)); cv.add_emissive(184, 133, 204, 134)
    cv.rect(202, 124, 206, 128, K("gris", 6))
    caldera(cv, 54, 34, 146, 170, rnd, cupula=14)
    tubo_h(cv, 146, 162, 82, g=6, base=4, bridas=0)                                  # A y B, unidas
    tubo_v(cv, 96, WT + 12, 38, g=7, base=4, bridas=0)                                # chimenea de A
    tubo_v(cv, 190, WT + 12, 46, g=5, base=4, bridas=0)
    manometro(cv, 126, 76); manometro(cv, 210, 86)
    cv.rect(66, 70, 92, 78, K("ocre", 1)); cv.text(68, 72, "CAL 1", K("ocre", 3))       # placa
    rejilla_fuego(cv, 84, 140, 116, 160, rnd)
    for _ in range(10):                                                               # ceniza y brasas caídas
        x, y = rnd.randint(84, 118), rnd.randint(171, 182)
        cv.px(x, y, K("gris", 5) if rnd.random() < 0.6 else K("rojo", 4))
    carbon(cv, 56, 200, 110, 236, rnd)
    # un rastro de papeles a medio quemar, del montacargas a la boca del fuego
    for (sx, sy) in ((372, 108), (344, 122), (318, 134), (286, 148), (248, 158), (214, 166), (176, 170), (136, 176)):
        sx += rnd.randint(-4, 4); sy += rnd.randint(-3, 3)
        cv.rect(sx, sy, sx + 5, sy + 3, K("papel", rnd.choice([2, 3]))); cv.px(sx + 4, sy, K("gris", 1))
        cv.px(sx, sy + 2, K("gris", 2)); cv.hline(sx + 1, sx + 4, sy + 1, K("gris", 5))
    # bombilla enjaulada sobre el montacargas
    cv.vline(380, WT + 12, 26, K("gris", 1))
    cv.rect(377, 26, 384, 32, K("gris", 1)); cv.rect(378, 27, 383, 31, K("ocre", 3)); cv.px(379, 28, K("ocre", 4))
    cv.vline(380, 26, 32, K("gris", 1)); cv.hline(377, 384, 29, K("gris", 1))
    # muros y puerta de servicio
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.vline(X0 - 1, WT, FB, K("gris", 4)); cv.vline(X1, WT, FB, K("gris", 4))
    cv.rect(X0 - 12, FB, 224, FB + 12, K("gris", 3)); cv.rect(256, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.hline(X0, 224, FB, K("gris", 4)); cv.hline(256, X1, FB, K("gris", 4))
    cv.rect(224, FB, 256, FB + 12, K("gris", 2)); cv.hline(224, 256, FB + 2, K("gris", 4))
    # luz: penumbra general; el fuego de la rejilla manda
    cv.add_light(X0, WT, X1, FB, -1)
    fx, fy = 100, 164

    def calor(x, y):
        d = ((x - fx) ** 2 + ((y - fy) * 1.3) ** 2) ** 0.5
        if not (X0 <= x < X1 and WT <= y < FB) or (y < 160 and x < 150):                                          # el cuerpo de la caldera no se ilumina a sí mismo
            return 0
        return 2 if d < 34 else (1 if d < 80 else (0 if d < 150 else -1))
    cv.add_light_fn(calor)
    cv.glow_rgb = K("rojo", 5)
    cv.add_glow_suave(fx, fy, 230, 0.42, squash=1.15, pasos=9, limite=(X0, WT, X1, FB))
    cv.add_glow_suave(fx, 150, 40, 0.5, limite=(70, 128, 130, 175))
    cv.add_emissive(378, 27, 383, 31)
    cv.bake_lighting()
    # segunda pasada: la bombilla enjaulada, tenue y amarillenta
    cv.light = [[0] * W for _ in range(H)]
    cv.glow = [[0.0] * W for _ in range(H)]
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(380, 40, 110, 0.22, squash=0.9, pasos=6, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
