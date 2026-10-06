"""A3 — Archivo Restringido (planta 11 del Minipax): sin ventanas, techo bajo, una sola bombilla con pantalla verde.

Al fondo, estanterías viejas con cajas por años. En medio, dos filas de estanterías llenas de carpetas azules idénticas,
numeradas por semanas. Polvo en todo menos en un camino de pisadas que va de la puerta a una sola carpeta.
Ni una telepantalla: aquí nadie mira, porque nadie debería entrar.
"""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 28, 92, 246
LX, LY = 240, 30                       # la bombilla


def modulo_anos(cv, x0, x1, y0, y1, ano, rnd):
    """Estantería vieja de madera con cajas y legajos de un año."""
    cv.rect(x0 + 2, y0 + 2, x1 + 2, y1, K("pared", 0))
    cv.rect(x0, y0, x1, y1, K("madera", 1)); cv.frame(x0, y0, x1, y1, K("madera", 0))
    cv.vline(x0 + 1, y0, y1, K("madera", 3)); cv.vline(x1 - 2, y0, y1, K("madera", 2))
    for by in range(y0 + 22, y1, 17):
        cv.rect(x0 + 2, by, x1 - 2, by + 3, K("madera", 3)); cv.hline(x0 + 2, x1 - 2, by, K("madera", 4))
        bx = x0 + 3
        while bx < x1 - 12:
            r = rnd.random()
            if r < 0.45:                                                                   # caja de cartón
                bw = rnd.randint(12, 18)
                cv.rect(bx, by - 12, bx + bw, by, K("ocre", 1)); cv.hline(bx, bx + bw, by - 12, K("ocre", 2))
                cv.vline(bx + bw - 1, by - 12, by, K("ocre", 0))
                cv.rect(bx + 3, by - 8, bx + bw - 4, by - 5, K("papel", 2))
            elif r < 0.85:                                                                 # legajos atados
                bw = rnd.randint(8, 14)
                for k in range(bx, bx + bw, 2):
                    cv.vline(k, by - rnd.randint(9, 11), by, K("papel", rnd.choice([0, 1, 1, 2])))
                cv.hline(bx, bx + bw, by - 5, K("madera", 2))
            else:                                                                          # hueco
                bw = rnd.randint(6, 10)
            bx += bw + 1
    # cartela del año
    cv.rect(x0 + 5, y0 + 3, x0 + 27, y0 + 12, K("papel", 3))
    cv.frame(x0 + 5, y0 + 3, x0 + 27, y0 + 12, K("madera", 0))
    cv.text(x0 + 16 - cv.text_width(ano) // 2, y0 + 5, ano, K("gris", 1))
    cv.rect(x1 - 30, y0 + 4, x1 - 6, y0 + 11, K("madera", 0))                              # cajón de fichas
    cv.px(x1 - 18, y0 + 7, K("ocre", 3))
    for _ in range((x1 - x0) // 2):                                                      # polvo en las baldas
        cv.px(rnd.randint(x0 + 2, x1 - 3), rnd.randint(y0 + 14, y1 - 2), K("gris", 5))


def estanteria_carpetas(cv, x0, y0, x1, y1, semana, rnd):
    """Estantería exenta vista en 3/4: la huella (x0,y0)-(x1,y1); el mueble sube por encima de ella."""
    alto = 30
    ft = y1 - alto                                                                         # arriba de la cara frontal
    cv.rect(x0 + 3, y1, x1 + 5, y1 + 4, K("gris", 1))                                       # sombra en el suelo
    cv.rect(x1, ft + 4, x1 + 5, y1 + 4, K("gris", 1))
    cv.rect(x0, ft - 8, x1, ft, K("gris", 5)); cv.hline(x0, x1, ft - 8, K("gris", 6))        # cara de arriba
    cv.hline(x0, x1, ft - 1, K("gris", 4))
    for _ in range((x1 - x0) // 2):
        cv.px(rnd.randint(x0 + 1, x1 - 2), rnd.randint(ft - 7, ft - 2), K("papel", 0))         # polvo
    cv.rect(x0, ft, x1, y1, K("gris", 1))                                                   # cara frontal
    cv.vline(x0, ft, y1, K("gris", 4)); cv.vline(x0 + 1, ft, y1, K("gris", 3)); cv.vline(x1 - 1, ft, y1, K("gris", 2))
    n = semana
    for by in (ft + 10, ft + 20, y1 - 1):
        cv.hline(x0 + 2, x1 - 1, by, K("gris", 4)); cv.hline(x0 + 2, x1 - 1, by - 1, K("gris", 3))
        bx = x0 + 3
        while bx < x1 - 4:
            fw = 3
            col = K("azul", 3)
            cv.rect(bx, by - 8, bx + fw, by - 1, col)
            cv.vline(bx, by - 8, by - 1, K("azul", 4)); cv.vline(bx + fw - 1, by - 8, by - 1, K("azul", 2))
            cv.px(bx + 1, by - 6, K("papel", 4)); cv.px(bx + 1, by - 5, K("papel", 3))        # etiqueta numerada
            if rnd.random() < 0.04:                                                         # una carpeta sobresale
                cv.rect(bx, by - 10, bx + fw, by - 8, K("azul", 4))
            bx += fw + 1
            n += 1
    # cartela en el costado: semanas
    t = f"S{semana:02d}"
    cv.rect(x0 + 3, ft - 7, x0 + 7 + cv.text_width(t), ft - 1, K("papel", 3))
    cv.text(x0 + 5, ft - 6, t, K("gris", 1))


def mesa_lectura(cv, x0, y0, x1, y1, rnd):
    cv.rect(x0 + 3, y1 + 4, x1 + 4, y1 + 9, K("gris", 1))                                   # sombra
    cv.rect(x0, y0, x1, y1, K("madera", 4)); cv.frame(x0, y0, x1, y1, K("madera", 2))
    cv.hline(x0 + 1, x1 - 1, y0 + 1, K("madera", 5))
    cv.rect(x0, y1, x1, y1 + 5, K("madera", 3)); cv.hline(x0, x1, y1 + 4, K("madera", 1))
    for xx in (x0 + 1, x1 - 4):
        cv.rect(xx, y1 + 5, xx + 3, y1 + 10, K("madera", 2))
    # una carpeta azul abierta
    cv.rect(x0 + 30, y0 + 5, x0 + 58, y0 + 20, K("azul", 2)); cv.frame(x0 + 30, y0 + 5, x0 + 58, y0 + 20, K("azul", 1))
    cv.rect(x0 + 32, y0 + 6, x0 + 43, y0 + 19, K("papel", 4)); cv.rect(x0 + 45, y0 + 6, x0 + 56, y0 + 19, K("papel", 3))
    for k in range(5):
        cv.hline(x0 + 34, x0 + 42, y0 + 8 + k * 2, K("gris", 6)); cv.hline(x0 + 47, x0 + 55, y0 + 8 + k * 2, K("gris", 6))
    cv.rect(x0 + 47, y0 + 15, x0 + 53, y0 + 18, K("rojo", 2))                                # sello en rojo
    # tampón y sello
    cv.rect(x0 + 6, y0 + 6, x0 + 20, y0 + 14, K("gris", 2)); cv.rect(x0 + 8, y0 + 7, x0 + 18, y0 + 12, K("rojo", 1))
    cv.rect(x0 + 10, y0 + 15, x0 + 16, y0 + 19, K("madera", 2)); cv.rect(x0 + 12, y0 + 12, x0 + 14, y0 + 16, K("madera", 3))
    # lupa
    cv.ellipse(x0 + 64, y0 + 6, x0 + 75, y0 + 17, K("cielo", 5), outline=K("ocre", 2))
    cv.px(x0 + 67, y0 + 9, K("cielo", 6)); cv.px(x0 + 68, y0 + 8, K("cielo", 6))
    cv.d.line([(x0 + 74, y0 + 16), (x0 + 81, y0 + 21)], fill=K("madera", 1))
    cv.d.line([(x0 + 75, y0 + 16), (x0 + 82, y0 + 21)], fill=K("madera", 2))


def silla_de_espaldas(cv, x0, y0, x1, y1):
    cv.rect(x0 + 2, y1 - 2, x1 + 3, y1 + 2, K("gris", 1))
    cv.rect(x0, y0 - 2, x1, y0 + 6, K("madera", 4)); cv.frame(x0, y0 - 2, x1, y0 + 6, K("madera", 2))   # asiento
    for xx in (x0 + 1, x1 - 3):
        cv.rect(xx, y0 + 6, xx + 2, y1, K("madera", 1))
    cv.rect(x0, y0 + 2, x1, y0 + 9, K("madera", 3)); cv.hline(x0, x1, y0 + 2, K("madera", 5))          # respaldo
    cv.vline(x0 + 5, y0 + 3, y0 + 9, K("madera", 1)); cv.vline(x1 - 6, y0 + 3, y0 + 9, K("madera", 1))


def bombilla(cv):
    cv.vline(LX, WT - 14, LY - 4, K("gris", 2))
    cv.poly([(LX - 10, LY + 4), (LX - 3, LY - 4), (LX + 3, LY - 4), (LX + 10, LY + 4)], K("tele", 3))   # pantalla de chapa verde
    cv.d.line([(LX - 3, LY - 3), (LX - 8, LY + 3)], fill=K("tele", 5))
    cv.d.line([(LX + 3, LY - 3), (LX + 9, LY + 3)], fill=K("tele", 2))
    cv.rect(LX - 2, LY - 6, LX + 3, LY - 3, K("gris", 3))
    cv.hline(LX - 10, LX + 11, LY + 4, K("tele", 1))
    cv.ellipse(LX - 3, LY + 3, LX + 4, LY + 8, K("papel", 4))                                # la bombilla
    cv.px(LX - 1, LY + 4, K("ocre", 4))
    cv.add_emissive(LX - 3, LY + 4, LX + 4, LY + 8)


def dibujar(variante=None):
    rnd = random.Random(1984)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    P.papel_pintado(cv, X0, WT, X1, WB, rampa="pared", base=1, motivo="rayas")
    for _ in range(10):                                                                     # humedad
        x, y = rnd.randint(X0, X1 - 10), rnd.randint(WT, WB - 30)
        for k in range(rnd.randint(8, 24)):
            cv.px(x + rnd.randint(0, 3), y + k, K("pared", 0))
    for (x0, x1, ano) in ((60, 160, "1975"), (190, 290, "1979"), (330, 430, "1983")):
        modulo_anos(cv, x0, x1, 32, WB, ano, rnd)
    P.zocalo(cv, X0, X1, WB, rampa="madera", base=1, alto=4)
    # suelo de baldosa, cubierto de polvo
    P.baldosas(cv, X0, WB, X1, FB, K("gris", 4), K("gris", 3), t=16, linea=K("gris", 2))
    P.manchas(cv, X0, WB, X1, FB, K("gris", 5), n=700, semilla=3)
    P.manchas(cv, X0, WB, X1, FB, K("papel", 0), n=160, semilla=4)
    # pisadas en el polvo: de la puerta a la segunda fila, a la derecha
    pasos = [(236, 236), (246, 226), (236, 216), (248, 206), (240, 196), (252, 188), (246, 178), (258, 172), (264, 176)]
    for i, (fx, fy) in enumerate(pasos):
        cv.rect(fx, fy, fx + 4, fy + 6, K("gris", 2)); cv.rect(fx + 1, fy + 1, fx + 3, fy + 3, K("gris", 1))
        cv.rect(fx + 1, fy + 4, fx + 3, fy + 6, K("gris", 1))
    # las dos filas de estanterías de carpetas azules
    semana = 1
    for y0, y1 in ((112, 126), (156, 170)):
        for x0, x1 in ((70, 210), (270, 410)):
            estanteria_carpetas(cv, x0, y0, x1, y1, semana, rnd)
            semana += 13
    # mesa de lectura y silla
    mesa_lectura(cv, 320, 196, 410, 222, rnd)
    silla_de_espaldas(cv, 360, 224, 376, 236)
    bombilla(cv)
    # muros y puerta de acero
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.vline(X0 - 1, WT, FB, K("gris", 4)); cv.vline(X1, WT, FB, K("gris", 4))
    cv.rect(X0 - 12, FB, 224, FB + 12, K("gris", 3)); cv.rect(256, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.hline(X0, 224, FB, K("gris", 4)); cv.hline(256, X1, FB, K("gris", 4))
    cv.rect(224, FB, 256, FB + 12, K("gris", 5)); cv.hline(224, 256, FB, K("gris", 7))
    for rx in range(227, 255, 6):
        cv.px(rx, FB + 3, K("gris", 7)); cv.px(rx, FB + 9, K("gris", 7))
    # luz: penumbra; un cono verdoso bajo la bombilla
    cv.add_light(X0 - 12, WT - 12, X1 + 12, FB + 12, -1)

    def cono(x, y):
        if not (X0 <= x < X1 and WT <= y < FB):
            return 0
        d = (((x - LX) / 1.25) ** 2 + ((y - 140) * 1.0) ** 2) ** 0.5
        return 2 if d < 46 else (1 if d < 100 else 0)
    cv.add_light_fn(cono)
    cv.glow_rgb = K("pared", 6)
    cv.add_glow_suave(LX, 120, 170, 0.26, squash=0.9, pasos=8, limite=(X0, WT, X1, FB))
    cv.add_glow_suave(LX, LY + 6, 30, 0.35, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
