"""J4.06–J4.07 — Limehouse al atardecer (960x270, la cámara sigue al jugador).

Calle prole de casas de ladrillo ennegrecido, ropa tendida, charcos y farolas de gas.
Ni una telepantalla: solo un altavoz lejano. Al fondo, la casa partida por la mitad.
"""
import random

from pixel import Canvas, K
import props as P

W, H = 960, 270
FACHADA, CALLE = 104, 236


def ladrillo(cv, x0, y0, x1, y1, rnd, base=2, rampa="granate"):
    cv.rect(x0, y0, x1, y1, K(rampa, base - 1))
    for fila, y in enumerate(range(y0, y1, 4)):
        off = (fila % 2) * 4
        for x in range(x0 - off, x1, 8):
            c = K(rampa, base + rnd.choice([0, 0, 0, -1, 1])) if rnd.random() > 0.12 else K("gris", 2)
            cv.rect(max(x0, x + 1), y + 1, min(x1, x + 7), min(y1, y + 3), c)


def casa(cv, x, w, top, rnd, puerta_verde=False, luz=0.2):
    ladrillo(cv, x, top, x + w, FACHADA, rnd, base=rnd.choice([1, 2]))
    cv.rect(x, top - 4, x + w, top, K("gris", 2)); cv.hline(x, x + w, top - 4, K("gris", 4))      # cornisa
    for wx in range(x + 8, x + w - 14, 22):
        lit = rnd.random() < luz
        cv.rect(wx, top + 10, wx + 12, top + 26, K("ocre", 3) if lit else K("gris", 1))
        cv.vline(wx + 6, top + 10, top + 26, K("madera", 1)); cv.hline(wx - 1, wx + 13, top + 27, K("gris", 5))
        if lit:
            cv.add_emissive(wx, top + 10, wx + 12, top + 26)
    px_ = x + w // 2 - 10
    if puerta_verde:
        cv.rect(px_, FACHADA - 32, px_ + 18, FACHADA, K("tele", 3)); cv.frame(px_, FACHADA - 32, px_ + 18, FACHADA, K("tele", 1))
        cv.px(px_ + 14, FACHADA - 16, K("ocre", 4))
    else:
        P.puerta(cv, px_, FACHADA - 32, w=18, h=32, rampa="madera", base=1)
    cv.rect(px_ - 2, FACHADA, px_ + 20, FACHADA + 3, K("gris", 4))                                 # escalón


def ropa_tendida(cv, x0, x1, y, rnd):
    cv.d.line([(x0, y), ((x0 + x1) // 2, y + 5), (x1, y)], fill=K("gris", 2))
    colores = [K("granate", 4), K("ocre", 3), K("cielo", 5), K("papel", 3), K("tele", 4), K("rojo", 3), K("papel", 4)]
    x = x0 + 6
    while x < x1 - 10:
        w = rnd.randint(6, 12)
        t = (x - x0) / (x1 - x0)
        yy = int(y + 5 * (1 - abs(2 * t - 1))) + 1
        cv.rect(x, yy, x + w, yy + rnd.randint(7, 13), rnd.choice(colores))
        x += w + rnd.randint(3, 8)


def casa_alcanzada(cv, x, rnd):
    """Una casa partida por la mitad: se ve el interior, como una casa de muñecas."""
    ladrillo(cv, x, 22, x + 70, FACHADA, rnd, base=1)
    # el corte: borde irregular y el interior a la vista
    cv.poly([(x + 70, 22), (x + 92, 30), (x + 88, 50), (x + 100, 64), (x + 94, FACHADA), (x + 70, FACHADA)], K("granate", 1))
    cv.rect(x + 100, 30, x + 176, 62, K("granate", 5))                                       # papel pintado de flores
    for fx in range(x + 104, x + 174, 8):
        for fy in range(34, 60, 8):
            cv.px(fx, fy, K("ocre", 4)); cv.px(fx + 1, fy + 1, K("rojo", 4)); cv.px(fx - 1, fy + 1, K("rojo", 4))
    cv.rect(x + 100, 62, x + 176, 66, K("madera", 2))                                        # suelo del primer piso, roto
    cv.poly([(x + 150, 62), (x + 176, 62), (x + 176, 74), (x + 160, 70)], K("gris", 0))
    cv.rect(x + 100, 66, x + 176, FACHADA, K("granate", 1))                                  # planta baja, en penumbra
    # la cama colgando
    cv.poly([(x + 118, 58), (x + 146, 62), (x + 156, 86), (x + 128, 82)], K("papel", 4))
    cv.d.line([(x + 122, 64), (x + 150, 68)], fill=K("cielo", 5)); cv.d.line([(x + 126, 72), (x + 153, 76)], fill=K("cielo", 5))
    cv.poly([(x + 118, 58), (x + 146, 62), (x + 148, 66), (x + 120, 62)], K("madera", 2))
    cv.vline(x + 128, 82, 92, K("madera", 1)); cv.vline(x + 155, 86, 96, K("madera", 1))
    cv.vline(x + 140, 30, 40, K("gris", 2)); cv.rect(x + 136, 40, x + 144, 44, K("ocre", 3))       # una lámpara que aún cuelga
    cv.rect(x + 104, 70, x + 120, 90, K("granate", 3))                                       # una butaca
    ladrillo(cv, x + 176, 40, x + 200, FACHADA, rnd, base=1)                                  # media pared que queda
    cv.poly([(x + 176, 40), (x + 186, 32), (x + 200, 40)], K("gris", 2))


def humo(cv, x, rnd):
    """Humo que sube del escombro y se deshace hacia el este: manchas tramadas, sin contorno."""
    for i in range(22):
        cy = 96 - i * 4.5
        r = 5 + i * 1.5
        cx = x + i * 3 + rnd.randint(-2, 2)
        tono = K("gris", 6) if i < 8 else K("gris", 5)
        for _ in range(int(r * r * 0.9)):
            dx, dy = rnd.uniform(-r, r), rnd.uniform(-r * 0.6, r * 0.6)
            if (dx / r) ** 2 + (dy / (r * 0.6)) ** 2 <= 1 and 0 <= cy + dy < H:
                cv.px(int(cx + dx), int(cy + dy), tono)


def dibujar():
    rnd = random.Random(1904)
    cv = Canvas(W, H)
    # cielo del atardecer, sucio y cálido por el horizonte
    for i, y in enumerate(range(0, 48, 8)):
        cv.rect(0, y, W, y + 8, K("ocre", 1) if i >= 4 else K("cielo", 3 - i // 2))
    # casas adosadas
    x = 0
    puerta_verde = 3
    n = 0
    while x < 690:
        w = rnd.randint(64, 88)
        if 270 <= x < 370:                       # el pub ocupa su propio hueco
            w = 92
        casa(cv, x, w, rnd.randint(26, 40), rnd, puerta_verde=(n == puerta_verde))
        x += w
        n += 1
    # pub «La Campana»
    px_ = 288
    cv.rect(px_, 60, px_ + 74, FACHADA, K("madera", 1)); cv.frame(px_, 60, px_ + 74, FACHADA, K("madera", 0))
    cv.rect(px_ + 4, 64, px_ + 70, 74, K("granate", 2)); cv.text(px_ + 37 - cv.text_width("LA CAMPANA") // 2, 66, "LA CAMPANA", K("ocre", 4))
    for wx in (px_ + 6, px_ + 52):
        cv.rect(wx, 78, wx + 16, 96, K("ocre", 3)); cv.add_emissive(wx, 78, wx + 16, 96)
        cv.vline(wx + 8, 78, 96, K("madera", 0)); cv.hline(wx, wx + 16, 87, K("madera", 0))
    P.puerta(cv, px_ + 28, FACHADA - 30, w=18, h=30, rampa="madera", base=2)
    # campana colgada sobre la puerta
    cv.ellipse(px_ + 33, 52, px_ + 41, 60, K("ocre", 3), outline=K("ocre", 1)); cv.hline(px_ + 30, px_ + 44, 52, K("gris", 2))
    # casa alcanzada y columna de humo
    casa_alcanzada(cv, 690, rnd)
    ladrillo(cv, 890, 30, W, FACHADA, rnd, base=1)
    humo(cv, 830, rnd)
    # altavoz lejano en un poste
    cv.rect(560, 10, 562, FACHADA, K("gris", 2))
    cv.poly([(562, 14), (574, 8), (574, 24), (562, 18)], K("gris", 4))
    # ropa tendida de lado a lado
    for (a, b, y) in [(20, 150, 30), (170, 270, 26), (380, 520, 32), (590, 680, 28)]:
        ropa_tendida(cv, a, b, y, rnd)
    # calle de adoquines con charcos
    P.adoquines(cv, 0, FACHADA, W, CALLE, semilla=8)
    for (cx, cy, rw) in [(120, 170, 22), (420, 200, 30), (610, 150, 18), (300, 214, 14)]:
        cv.ellipse(cx - rw, cy - 5, cx + rw, cy + 5, K("cielo", 2)); cv.hline(cx - rw + 6, cx + rw - 10, cy - 2, K("ocre", 2))
    P.escombros(cv, 700, 108, 930, 186, n=70, semilla=21)
    P.escombros(cv, 760, 150, 900, 210, n=30, semilla=5, rampa="gris")
    # un gato
    cv.rect(200, 120, 208, 124, K("gris", 1)); cv.rect(206, 117, 210, 121, K("gris", 1)); cv.px(206, 116, K("gris", 1)); cv.px(209, 116, K("gris", 1))
    cv.d.line([(200, 121), (196, 116)], fill=K("gris", 1))
    # bordillo y muro bajo de enfrente
    cv.rect(0, CALLE, W, CALLE + 4, K("gris", 3)); cv.hline(0, W, CALLE, K("gris", 6))
    ladrillo(cv, 0, CALLE + 4, W, H, rnd, base=1)
    # farolas de gas encendiéndose
    luces = [P.farola(cv, fx, 168, encendida=True) for fx in (150, 470, 640)]
    cv.add_light(0, 0, W, H, -1)
    for (lx, ly) in luces:
        cv.glow_rgb = K("ocre", 3)
        cv.add_glow_suave(lx, ly + 40, 70, 0.3, squash=1.2)
    cv.bake_lighting()
    return cv
