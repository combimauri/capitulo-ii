"""A3 — Casa de Dot (Limehouse): cocina pequeña y abarrotada.

La estufa encendida, ropa tendida de pared a pared, la despensa con rendijas, el barreño de lavar y, en la repisa,
la colección de metralla de Sammy junto a una foto pequeña. Huele a té y a carbón.
"""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 120, 360
WT, WB, FB = 22, 92, 236


def papel_flores(cv, x0, y0, x1, y1, rnd):
    cv.rect(x0, y0, x1, y1, K("granate", 3))
    for x in range(x0, x1, 10):
        cv.vline(x, y0, y1, K("granate", 2))
    for y in range(y0 + 4, y1 - 3, 8):
        for x in range(x0 + 5 + (y // 8 % 2) * 5, x1 - 2, 10):
            cv.px(x, y, K("ocre", 2)); cv.px(x - 1, y + 1, K("granate", 5)); cv.px(x + 1, y + 1, K("granate", 5))
            cv.px(x, y + 2, K("granate", 5)); cv.px(x, y + 1, K("ocre", 3))
    # despegado: jirones que dejan ver el yeso
    for (px_, py_, pw, ph) in ((246, 62, 14, 10), (280, 30, 10, 8), (128, 26, 6, 12)):
        cv.rect(px_, py_, px_ + pw, py_ + ph, K("papel", 1))
        cv.d.line([(px_, py_), (px_ + pw, py_ + 2)], fill=K("granate", 1))
        cv.poly([(px_ + pw - 4, py_ + ph), (px_ + pw, py_ + ph), (px_ + pw + 2, py_ + ph + 4)], K("granate", 4))
    for _ in range(14):                                                                     # manchas de hollín cerca del techo
        cv.px(rnd.randint(x0, x1 - 1), rnd.randint(y0, y0 + 6), K("granate", 1))


def despensa(cv, x0, y0, x1, y1):
    cv.rect(x0 - 3, y0 - 3, x1 + 3, y1, K("madera", 1))
    cv.rect(x0, y0, x1, y1, K("madera", 3))
    cv.vline(x0, y0, y1, K("madera", 4)); cv.vline(x1 - 1, y0, y1, K("madera", 2))
    for y in range(y0 + 4, y1 - 4, 4):                                                       # lamas con rendijas
        cv.hline(x0 + 3, x1 - 3, y, K("gris", 0)); cv.hline(x0 + 3, x1 - 3, y + 1, K("madera", 4))
    cv.rect(x0 + 3, (y0 + y1) // 2 - 1, x1 - 3, (y0 + y1) // 2 + 2, K("madera", 3))         # travesaño
    cv.hline(x0 + 3, x1 - 3, (y0 + y1) // 2 - 1, K("madera", 5))
    cv.rect(x1 - 6, (y0 + y1) // 2 + 4, x1 - 3, (y0 + y1) // 2 + 7, K("ocre", 2)); cv.px(x1 - 5, (y0 + y1) // 2 + 5, K("ocre", 4))


def estufa(cv, x0, y0, x1, y1):
    """Cocina económica de hierro: plancha arriba, hogar encendido, tubo de humos por la pared."""
    cv.rect(x0 + 3, y1 - 2, x1 + 5, y1 + 3, K("madera", 0))                                  # sombra
    # tubo de humos
    cv.rect(x0 + 30, WT + 6, x0 + 37, y0 - 14, K("gris", 2))
    cv.vline(x0 + 30, WT + 6, y0 - 14, K("gris", 4)); cv.vline(x0 + 36, WT + 6, y0 - 14, K("gris", 1))
    for by in (WT + 14, 50):
        cv.rect(x0 + 29, by, x0 + 38, by + 2, K("gris", 3))
    cv.rect(x0 + 26, WT, x0 + 41, WT + 6, K("gris", 2)); cv.hline(x0 + 26, x0 + 41, WT + 5, K("gris", 1))   # codo a la pared
    cv.rect(x0 + 28, y0 - 14, x0 + 39, y0 - 8, K("gris", 3))
    # cuerpo
    top = y0 - 8
    cv.rect(x0, top, x1, top + 12, K("gris", 3)); cv.hline(x0, x1, top, K("gris", 5))       # plancha (cara de arriba)
    cv.ellipse(x0 + 4, top + 2, x0 + 18, top + 10, K("gris", 1), outline=K("gris", 4))      # fogones
    cv.ellipse(x0 + 22, top + 2, x0 + 36, top + 10, K("gris", 1), outline=K("gris", 4))
    cv.rect(x0, top + 12, x1, y1, K("gris", 2)); cv.frame(x0, top + 12, x1, y1, K("gris", 1))
    cv.hline(x0 + 1, x1 - 1, top + 12, K("gris", 4))
    cv.rect(x1 - 4, top + 14, x1 + 2, top + 16, K("ocre", 2))                                 # barra de latón
    # puerta del hogar, abierta: el fuego
    fx0, fy0, fx1, fy1 = x0 + 6, top + 16, x0 + 24, y1 - 4
    cv.rect(fx0 - 1, fy0 - 1, fx1 + 1, fy1 + 1, K("gris", 0))
    cv.rect(fx0, fy0, fx1, fy1, K("rojo", 2))
    rnd = random.Random(9)
    for x in range(fx0, fx1):
        h = rnd.randint(3, fy1 - fy0)
        for k in range(h):
            t = k / max(1, h)
            cv.px(x, fy1 - 1 - k, K("ocre", 4) if t < 0.3 else K("ocre", 3) if t < 0.6 else K("rojo", 5))
    cv.add_emissive(fx0, fy0, fx1, fy1)
    cv.rect(fx1 + 2, fy0, fx1 + 5, fy1, K("gris", 3)); cv.vline(fx1 + 4, fy0, fy1, K("gris", 1))   # la portezuela abierta
    cv.rect(x0 + 28, top + 18, x1 - 4, y1 - 6, K("gris", 1)); cv.px(x1 - 7, top + 22, K("ocre", 3))   # horno
    for lx in (x0 + 1, x1 - 4):
        cv.rect(lx, y1, lx + 3, y1 + 2, K("gris", 1))
    # tetera grande y cazo sobre la plancha
    cv.ellipse(x0 + 5, top - 6, x0 + 17, top + 6, K("gris", 6), outline=K("gris", 3))
    cv.rect(x0 + 9, top - 8, x0 + 13, top - 5, K("gris", 4)); cv.d.line([(x0 + 16, top - 2), (x0 + 20, top - 5)], fill=K("gris", 5))
    cv.rect(x0 + 23, top - 2, x0 + 35, top + 6, K("madera", 1)); cv.hline(x0 + 23, x0 + 35, top - 2, K("gris", 5))
    cv.hline(x0 + 35, x0 + 42, top + 1, K("madera", 2))


def ropa_tendida(cv, x0, x1, y, rnd):
    mid = (x0 + x1) // 2
    cv.d.line([(x0, y), (mid, y + 6), (x1, y)], fill=K("gris", 6))
    cv.rect(x0 - 2, y - 2, x0 + 1, y + 2, K("gris", 3)); cv.rect(x1 - 1, y - 2, x1 + 2, y + 2, K("gris", 3))   # escarpias
    prendas = [("granate", 4), ("papel", 3), ("ocre", 3), ("tela", 3), ("papel", 4), ("granate", 5), ("cielo", 5), ("tela", 4)]
    x = x0 + 8
    i = 0
    while x < x1 - 14:
        r, b = prendas[i % len(prendas)]
        t = (x - x0) / (x1 - x0)
        yy = int(y + 6 * (1 - abs(2 * t - 1))) + 1
        tipo = rnd.choice(["camisa", "trapo", "calcetin", "trapo"])
        if yy + 11 > 46:
            tipo = "calcetin" if tipo == "camisa" else tipo
        if tipo == "camisa":
            w = 14
            cv.rect(x, yy, x + w, yy + 10, K(r, b)); cv.rect(x - 2, yy, x + 1, yy + 5, K(r, b)); cv.rect(x + w - 1, yy, x + w + 2, yy + 5, K(r, b))
            cv.vline(x + w // 2, yy + 1, yy + 10, K(r, b - 1)); cv.hline(x, x + w, yy + 9, K(r, b - 1))
        elif tipo == "calcetin":
            w = 4
            cv.rect(x, yy, x + 3, yy + 8, K(r, b)); cv.rect(x, yy + 6, x + 6, yy + 9, K(r, b)); w = 6
        else:
            w = rnd.randint(8, 13)
            cv.rect(x, yy, x + w, min(46, yy + rnd.randint(7, 11)), K(r, b)); cv.vline(x + w - 1, yy, min(46, yy + 7), K(r, b - 1))
        cv.px(x + 1, yy - 1, K("madera", 4)); cv.px(x + w - 2, yy - 1, K("madera", 4))           # pinzas
        x += w + rnd.randint(4, 8)
        i += 1


def repisa(cv, x0, y0, x1, y1, rnd):
    cv.rect(x0 + 2, y1, x1 + 2, y1 + 2, K("granate", 1))                                      # sombra
    cv.rect(x0, y1 - 3, x1, y1, K("madera", 4)); cv.hline(x0, x1, y1 - 3, K("madera", 5)); cv.hline(x0, x1, y1 - 1, K("madera", 2))
    for bx in (x0 + 4, x1 - 6):
        cv.d.line([(bx, y1), (bx + 2, y1 + 4)], fill=K("madera", 1))
    # cajón con la metralla de Sammy
    cv.rect(x0 + 3, y0 - 1, x0 + 27, y1 - 3, K("madera", 3)); cv.frame(x0 + 3, y0 - 1, x0 + 27, y1 - 3, K("madera", 1))
    cv.hline(x0 + 4, x0 + 26, y0, K("madera", 4))
    for _ in range(16):
        sx, sy = rnd.randint(x0 + 5, x0 + 24), rnd.randint(y0 - 3, y0)
        c = rnd.choice([5, 6, 7, 4])
        cv.px(sx, sy, K("gris", c)); cv.px(sx + 1, sy, K("gris", c - 1))
        if rnd.random() < 0.4:
            cv.px(sx, sy - 1, K("gris", c + 1))
    cv.px(x0 + 12, y0 - 4, K("gris", 7)); cv.px(x0 + 13, y0 - 5, K("gris", 8)); cv.px(x0 + 14, y0 - 4, K("gris", 5))  # la pieza grande
    # bote del té, la foto enmarcada y una taza
    cv.rect(x0 + 32, y0 + 1, x0 + 39, y1 - 3, K("rojo", 2)); cv.hline(x0 + 32, x0 + 39, y0 + 1, K("ocre", 3))
    cv.rect(x0 + 43, y0 - 2, x0 + 53, y1 - 3, K("ocre", 2)); cv.rect(x0 + 44, y0 - 1, x0 + 52, y1 - 4, K("papel", 2))
    cv.rect(x0 + 46, y0, x0 + 50, y0 + 2, K("madera", 2)); cv.rect(x0 + 45, y0 + 2, x0 + 51, y1 - 4, K("madera", 3))   # un soldado
    cv.px(x0 + 47, y0 + 1, K("madera", 1)); cv.px(x0 + 48, y0 + 1, K("madera", 1))
    cv.rect(x0 + 56, y0 + 1, x1 - 2, y1 - 3, K("papel", 3)); cv.ellipse(x0 + 56, y0 - 1, x1 - 2, y0 + 3, K("papel", 4))   # taza


def silla(cv, x, y, base=3, respaldo="arriba"):
    cv.rect(x + 2, y + 12, x + 17, y + 16, K("madera", 0))
    cv.rect(x, y + 4, x + 14, y + 11, K("madera", base + 1)); cv.frame(x, y + 4, x + 14, y + 11, K("madera", base - 1))
    for xx in (x + 1, x + 11):
        cv.rect(xx, y + 11, xx + 2, y + 16, K("madera", base - 1))
    if respaldo == "arriba":
        cv.rect(x, y - 6, x + 14, y + 4, K("madera", base)); cv.hline(x, x + 14, y - 6, K("madera", base + 2))
        cv.vline(x + 4, y - 4, y + 4, K("madera", base - 1)); cv.vline(x + 9, y - 4, y + 4, K("madera", base - 1))
    else:                                                                                   # de lado, respaldo a la izquierda
        cv.rect(x, y - 6, x + 3, y + 11, K("madera", base)); cv.vline(x, y - 6, y + 11, K("madera", base + 2))


def barreño(cv, x0, y0, x1, y1):
    cv.ellipse(x0 + 2, y0 + 6, x1 + 4, y1 + 3, K("madera", 0))
    cv.ellipse(x0, y0 + 6, x1, y1, K("gris", 5))                                             # cuerpo de cinc
    cv.ellipse(x0, y0, x1, y1 - 8, K("gris", 7), outline=K("gris", 4))                        # borde
    cv.ellipse(x0 + 3, y0 + 2, x1 - 3, y1 - 10, K("cielo", 4))                                # agua jabonosa
    for (bx, by) in ((x0 + 8, y0 + 5), (x0 + 14, y0 + 8), (x0 + 20, y0 + 4)):
        cv.px(bx, by, K("papel", 4)); cv.px(bx + 1, by, K("cielo", 6))
    cv.rect(x0 + 2, y0 + 7, x0 + 13, y0 + 11, K("granate", 4))                                # una prenda en remojo
    for hx in (x0 - 1, x1):
        cv.rect(hx - 1, y0 + 6, hx + 2, y0 + 9, K("gris", 4))                                  # asas
    # tabla de lavar apoyada
    cv.rect(x1 - 8, y0 - 6, x1, y0 + 8, K("madera", 4)); cv.frame(x1 - 8, y0 - 6, x1, y0 + 8, K("madera", 2))
    for k in range(y0 - 3, y0 + 7, 2):
        cv.hline(x1 - 7, x1 - 1, k, K("gris", 6))


def dibujar(variante=None):
    rnd = random.Random(1944)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    papel_flores(cv, X0, WT, X1, WB, rnd)
    despensa(cv, 132, 40, 162, 92)
    # perchero junto a la despensa: la gorra de Sammy
    cv.px(170, 66, K("gris", 6)); cv.rect(166, 67, 176, 71, K("tela", 3)); cv.rect(165, 70, 178, 72, K("tela", 2))
    repisa(cv, 172, 48, 236, 56, rnd)
    # alacena con platos
    cv.rect(242, 60, 288, 64, K("madera", 4)); cv.hline(242, 288, 63, K("madera", 2))
    for k in range(246, 286, 9):
        cv.ellipse(k, 52, k + 8, 60, K("papel", 3), outline=K("papel", 1)); cv.px(k + 4, 56, K("cielo", 5))
    cv.rect(242, 76, 288, 80, K("madera", 4)); cv.hline(242, 288, 79, K("madera", 2))
    for k, c in zip(range(246, 286, 8), [("ocre", 2), ("granate", 3), ("papel", 2), ("gris", 5), ("ocre", 1)]):
        cv.rect(k, 68, k + 6, 76, K(*c)); cv.hline(k, k + 6, 68, K(c[0], c[1] + 1))
    P.zocalo(cv, X0, X1, WB, rampa="madera", base=2, alto=4)
    P.tablones(cv, X0, WB, X1, FB, rampa="madera", base=3, semilla=31)
    # alfombra de trapo trenzado bajo la mesa
    cv.ellipse(178, 140, 290, 196, K("granate", 2))
    cv.ellipse(182, 143, 286, 193, K("ocre", 1)); cv.ellipse(186, 146, 282, 190, K("granate", 3))
    cv.ellipse(190, 149, 278, 187, K("tela", 2)); cv.ellipse(194, 152, 274, 184, K("granate", 4))
    estufa(cv, 300, 92, 344, 120)
    # cubo de carbón junto a la estufa
    cv.rect(348, 106, 358, 120, K("gris", 2)); cv.ellipse(348, 102, 358, 109, K("gris", 0), outline=K("gris", 4))
    for k in range(350, 357, 2):
        cv.px(k, 104, K("gris", 3))
    ropa_tendida(cv, 130, 350, 30, rnd)
    # mesa con tetera y dos sillas
    silla(cv, 226, 130, base=3)
    silla(cv, 180, 154, base=2, respaldo="lado")
    mx0, my0, mx1, my1 = 196, 146, 270, 176
    cv.rect(mx0 + 4, my1 + 1, mx1 + 5, my1 + 7, K("madera", 1))
    cv.rect(mx0, my0, mx1, my1 - 6, K("madera", 5)); cv.frame(mx0, my0, mx1, my1 - 6, K("madera", 3))
    cv.hline(mx0 + 1, mx1 - 1, my0 + 1, K("madera", 6))
    cv.rect(mx0, my1 - 6, mx1, my1, K("madera", 4)); cv.hline(mx0, mx1, my1 - 1, K("madera", 2))
    for xx in (mx0 + 2, mx1 - 5):
        cv.rect(xx, my1, xx + 3, my1 + 5, K("madera", 3))
    cv.rect(mx0 + 6, my0 + 4, mx0 + 30, my0 + 18, K("papel", 3)); cv.frame(mx0 + 6, my0 + 4, mx0 + 30, my0 + 18, K("papel", 2))   # mantel
    # tetera de loza marrón, tazas y pan
    tx, ty = 232, 150
    cv.ellipse(tx, ty, tx + 14, ty + 11, K("granate", 4), outline=K("granate", 1))
    cv.px(tx + 4, ty + 3, K("granate", 5)); cv.px(tx + 5, ty + 2, K("papel", 3))
    cv.rect(tx + 5, ty - 2, tx + 9, ty + 1, K("granate", 3)); cv.px(tx + 7, ty - 3, K("granate", 2))
    cv.d.line([(tx + 14, ty + 5), (tx + 18, ty + 2)], fill=K("granate", 3))
    cv.d.line([(tx - 1, ty + 3), (tx - 2, ty + 7)], fill=K("granate", 2))
    for (cx, cy) in ((212, 154), (256, 158)):
        cv.ellipse(cx, cy, cx + 7, cy + 5, K("papel", 4), outline=K("papel", 1)); cv.ellipse(cx + 2, cy + 1, cx + 5, cy + 4, K("madera", 2))
    cv.ellipse(204, 158, 216, 164, K("ocre", 2)); cv.hline(206, 214, 159, K("ocre", 3))
    barreño(cv, 128, 200, 160, 226)
    # muros y puerta
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.vline(X0 - 1, WT, FB, K("gris", 4)); cv.vline(X1, WT, FB, K("gris", 4))
    cv.rect(X0 - 12, FB, 224, FB + 12, K("gris", 3)); cv.rect(256, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.hline(X0, 224, FB, K("gris", 4)); cv.hline(256, X1, FB, K("gris", 4))
    cv.rect(224, FB, 256, FB + 12, K("madera", 2)); cv.hline(224, 256, FB, K("madera", 4))
    # luz: la estufa calienta y alumbra; el resto, penumbra cálida
    ex, ey = 316, 110

    def fuego(x, y):
        if not (X0 <= x < X1 and WT <= y < FB):
            return 0
        d = ((x - ex) ** 2 + ((y - ey) * 1.3) ** 2) ** 0.5
        return 1 if d < 60 else (0 if d < 200 else -1)
    cv.add_light_fn(fuego)
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(ex, ey, 240, 0.3, squash=1.1, pasos=10, limite=(X0, WT, X1, FB))
    cv.add_glow_suave(ex, ey + 4, 30, 0.45, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
