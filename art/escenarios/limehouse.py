"""J4.06–J4.07 — Limehouse al atardecer (960x270, la cámara sigue al jugador).

Calle prole de casas de ladrillo ennegrecido, ropa tendida, charcos y farolas de gas.
Ni una telepantalla: solo un altavoz lejano. Al fondo, la casa partida por la mitad.
"""
import random

from pixel import Canvas, K, LOOKUP
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


def casa(cv, x, w, top, rnd, puerta_verde=False, luz=0.2, manana=False):
    ladrillo(cv, x, top, x + w, FACHADA, rnd, base=rnd.choice([1, 2]))
    cv.rect(x, top - 4, x + w, top, K("gris", 2)); cv.hline(x, x + w, top - 4, K("gris", 4))      # cornisa
    for wx in range(x + 8, x + w - 14, 22):
        lit = rnd.random() < luz
        if manana:                                   # de día: cristal que refleja el cielo (mismo consumo de rnd)
            ventana_manana(cv, wx, top + 10, x * 31 + wx)
            continue
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


def dibujar(variante=None):
    """variante None: el atardecer de J4.06–J4.07. "manana": FD.03, la mañana del Final D."""
    if variante == "manana":
        return dibujar_manana()
    if variante is not None:
        raise ValueError(f"variante desconocida: {variante!r}")
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


# ================================================================ FD.03 — Limehouse por la mañana
# El protagonista sale de casa de Dot. No huye. El barrio se ha levantado: el mercado reconstruido a medias,
# la casa alcanzada con andamio y ladrillo nuevo, más ropa tendida que nunca. Es la imagen más luminosa del
# juego después del patio final: sol bajo que entra por la izquierda, farolas apagadas, charcos casi secos.
# Mismas casas (mismo consumo del generador), misma puerta verde, mismas huellas de colisión.

PUESTO_A = (420, 112, 500, 138)          # huella de colisión del puesto A (x0, y0, x1, y1)
ZONA_B = (716, 108, 926, 142)            # zona de colisión de la obra y el puesto B (antes, los escombros)
PUESTO_B = (800, 116, 868, 141)          # el puesto B dentro de esa zona
PUERTA_DOT = (265, 72, 283, 104)         # la puerta verde (el «11»)
FAROLAS = (150, 470, 640)
CIELO_MANANA = {K("cielo", 5), K("cielo", 6), K("papel", 4)}
CHARCOS = [(120, 170, 22), (420, 200, 30), (610, 150, 18), (300, 214, 14)]

VIVOS = [K("rojo", 4), K("rojo", 5), K("granate", 5), K("ocre", 4), K("ocre", 3), K("ocre", 4), K("papel", 4),
         K("pared", 5), K("pared", 6), K("cielo", 6), K("madera", 6), K("rojo", 4), K("ocre", 3), K("papel", 4)]


def ventana_manana(cv, wx, wy, semilla):
    """Ventana de día: cristal que refleja el cielo, a veces visillos, a veces abierta, a veces con geranios."""
    r = random.Random(semilla)
    cv.rect(wx - 1, wy - 1, wx + 13, wy + 17, K("madera", 3))                       # marco pintado
    cv.rect(wx, wy, wx + 12, wy + 16, K("cielo", 4))
    cv.rect(wx, wy + 9, wx + 12, wy + 16, K("cielo", 3))
    for k in range(4):                                                               # reflejo del sol
        cv.px(wx + 1 + k, wy + 4 - k, K("cielo", 6)); cv.px(wx + 7 + k, wy + 6 - k, K("cielo", 5))
    tipo = r.choice(["visillo", "visillo", "abierta", "nada", "cortina"])
    if tipo == "visillo":
        cv.rect(wx, wy, wx + 12, wy + 3, K("papel", 3))
        for k in range(wx, wx + 12, 2):
            cv.px(k, wy + 3, K("papel", 2))
    elif tipo == "abierta":                                                          # hoja de abajo subida
        cv.rect(wx, wy + 9, wx + 12, wy + 16, K("granate", 1)); cv.hline(wx, wx + 12, wy + 8, K("madera", 4))
    elif tipo == "cortina":
        c = r.choice([K("granate", 4), K("ocre", 3), K("tela", 3)])
        cv.rect(wx, wy, wx + 3, wy + 16, c); cv.rect(wx + 9, wy, wx + 12, wy + 16, c)
    cv.vline(wx + 6, wy, wy + 16, K("madera", 3))
    cv.hline(wx - 1, wx + 13, wy + 17, K("papel", 2))                                # alféizar
    if r.random() < 0.45:                                                            # jardinera con geranios
        cv.rect(wx - 1, wy + 18, wx + 13, wy + 21, K("madera", 3)); cv.hline(wx - 1, wx + 13, wy + 18, K("madera", 5))
        flor = r.choice([K("rojo", 4), K("granate", 5), K("ocre", 4), K("papel", 4)])
        for k in range(wx, wx + 12, 2):
            cv.px(k, wy + 17 - (k // 2) % 2, K("pared", 5 if k % 4 else 4))
            if r.random() < 0.5:
                cv.px(k, wy + 15 - (k // 2) % 2, flor)


def _prendas(x0, x1, y, rnd, colgada=5):
    """Lista de prendas a lo largo de un tendedero: (forma, x, y, w, h, color)."""
    out = []
    x = x0 + 5
    while x < x1 - 10:
        forma = rnd.choice(["sabana", "camisa", "camisa", "pantalon", "panuelo", "calcetines"])
        w = {"sabana": rnd.randint(11, 16), "camisa": 9, "pantalon": 8, "panuelo": 6, "calcetines": 5}[forma]
        h = {"sabana": rnd.randint(11, 15), "camisa": 10, "pantalon": 13, "panuelo": 6, "calcetines": 5}[forma]
        if x + w > x1 - 4:
            break
        t = (x + w / 2 - x0) / (x1 - x0)
        yy = int(y + colgada * (1 - abs(2 * t - 1))) + 1
        out.append((forma, x, yy, w, h, rnd.choice(VIVOS)))
        x += w + rnd.randint(2, 6)
    return out


def _dibujar_prenda(cv, forma, x, y, w, h, col):
    ramp, i = LOOKUP[col]
    osc = K(ramp, i - 1)
    if forma == "camisa":
        cv.rect(x + 2, y, x + w - 2, y + h, col); cv.rect(x, y, x + w, y + 4, col)       # cuerpo y mangas
        cv.vline(x + w - 3, y + 4, y + h, osc); cv.hline(x + 2, x + w - 2, y + h - 1, osc)
        cv.px(x + w // 2, y, osc); cv.px(x + w // 2, y + 1, osc)                        # cuello
    elif forma == "pantalon":
        cv.rect(x, y, x + w, y + 4, col); cv.rect(x, y + 4, x + 3, y + h, col); cv.rect(x + w - 3, y + 4, x + w, y + h, col)
        cv.vline(x + w - 1, y + 4, y + h, osc)
    elif forma == "calcetines":
        for k in (0, 3):
            cv.rect(x + k, y, x + k + 2, y + h, col); cv.px(x + k + 2, y + h - 1, col)
    else:
        cv.rect(x, y, x + w, y + h, col)
        cv.vline(x + w - 1, y + 1, y + h, osc); cv.hline(x, x + w, y + h - 1, osc)
        if forma == "sabana" and w > 12:
            cv.vline(x + w // 2, y + 2, y + h - 1, osc)                                 # pliegue
    cv.px(x + 1, y - 1, K("madera", 5)); cv.px(x + w - 2, y - 1, K("madera", 5))         # pinzas


def _tendedero(cv, x0, x1, y, prendas, colgada=5):
    cv.d.line([(x0, y), ((x0 + x1) // 2, y + colgada), (x1, y)], fill=K("papel", 1))
    for p in prendas:
        _dibujar_prenda(cv, *p)


def _cielo_manana(cv, rnd):
    franjas = [(0, 9, ("cielo", 5)), (9, 26, ("cielo", 6)), (26, 48, ("papel", 4))]
    for y0, y1, c in franjas:
        cv.rect(0, y0, W, y1, K(*c))
    for (nx, ny, nw) in [(40, 12, 60), (470, 14, 70), (840, 16, 80)]:                 # alguna nube fina
        cv.rect(nx, ny, nx + nw, ny + 2, K("papel", 4)); cv.rect(nx + 10, ny - 1, nx + nw - 18, ny, K("papel", 4))
    for (bx, by) in [(330, 12), (338, 9), (352, 14), (760, 6)]:                       # pájaros
        cv.px(bx, by, K("cielo", 2)); cv.px(bx + 1, by + 1, K("cielo", 2)); cv.px(bx + 2, by, K("cielo", 2))


def _chimenea(cv, x, top, voluta=False):
    cv.rect(x, top - 14, x + 10, top - 4, K("granate", 2)); cv.hline(x, x + 10, top - 14, K("granate", 4))
    cv.rect(x - 1, top - 16, x + 11, top - 14, K("gris", 4))
    for k in (x + 2, x + 6):
        cv.rect(k, top - 20, k + 3, top - 16, K("madera", 4)); cv.hline(k, k + 3, top - 20, K("madera", 5))
    if voluta:                                                                       # una voluta muy tenue
        pts = [(1, 0), (2, -1), (2, -2), (3, -3), (4, -4), (4, -5), (3, -6), (3, -7), (4, -8), (5, -9), (6, -10),
               (7, -10), (8, -11)]
        for i, (dx, dy) in enumerate(pts):
            if i % 4 != 3:
                cv.px(x + 2 + dx, top - 21 + dy, K("papel", 4) if i < 6 else K("cielo", 6))


def _casa_reconstruida(cv, x, rnd):
    """La casa alcanzada, a medias: planta baja levantada con ladrillo nuevo, andamio y una lona arriba."""
    ladrillo(cv, x, 22, x + 70, FACHADA, rnd, base=1)                                 # lo que quedó en pie
    cv.rect(x, 18, x + 70, 22, K("gris", 2)); cv.hline(x, x + 70, 18, K("gris", 4))
    ventana_manana(cv, x + 12, 34, 5); ventana_manana(cv, x + 40, 34, 6)
    P.puerta(cv, x + 26, FACHADA - 32, w=18, h=32, rampa="madera", base=1)
    cv.rect(x + 24, FACHADA, x + 46, FACHADA + 3, K("gris", 4))
    # ladrillo nuevo, más claro, con el último tramo escalonado (aún se está subiendo)
    ladrillo(cv, x + 70, 50, x + 176, FACHADA, rnd, base=5)
    for (a, b, y) in [(x + 70, x + 110, 42), (x + 70, x + 92, 34), (x + 130, x + 176, 46)]:
        ladrillo(cv, a, y, b, 50, rnd, base=5)
    # la lona tapa el primer piso, todavía abierto
    cv.poly([(x + 92, 22), (x + 176, 22), (x + 176, 46), (x + 130, 46), (x + 110, 42), (x + 92, 34)], K("papel", 2))
    for k in range(x + 98, x + 176, 12):                                             # pliegues
        cv.vline(k, 23, 40 if k < x + 112 else 45, K("papel", 1))
    cv.rect(x + 140, 26, x + 154, 35, K("ocre", 2)); cv.frame(x + 140, 26, x + 154, 35, K("ocre", 1))   # remiendo
    cv.hline(x + 92, x + 176, 22, K("papel", 3))
    for k in (x + 96, x + 128, x + 160):                                             # cuerdas de la lona
        cv.px(k, 23, K("ocre", 2)); cv.px(k, 24, K("ocre", 2))
    # vigas nuevas del tejado asomando por encima
    for k in range(x + 90, x + 178, 14):
        cv.d.line([(k, 22), (k + 8, 12)], fill=K("madera", 5))
    cv.hline(x + 96, x + 186, 12, K("madera", 4))
    # huecos de la planta baja nueva, con dintel de madera fresca
    cv.rect(x + 84, 72, x + 102, FACHADA, K("granate", 0)); cv.rect(x + 82, 69, x + 104, 72, K("madera", 5))
    cv.rect(x + 120, 62, x + 140, 84, K("granate", 0)); cv.rect(x + 118, 59, x + 142, 62, K("madera", 5))
    cv.hline(x + 118, x + 142, 84, K("papel", 2))
    cv.rect(x + 150, 62, x + 168, 84, K("granate", 0)); cv.rect(x + 148, 59, x + 170, 62, K("madera", 5))
    cv.d.line([(x + 150, 62), (x + 167, 83)], fill=K("madera", 4)); cv.d.line([(x + 167, 62), (x + 150, 83)], fill=K("madera", 4))
    # media pared vieja que queda
    ladrillo(cv, x + 176, 40, x + 200, FACHADA, rnd, base=1)
    cv.poly([(x + 176, 40), (x + 186, 32), (x + 200, 40)], K("gris", 2))


def _andamio(cv, x0, x1):
    """Andamio de madera delante del ladrillo nuevo (todo por encima de la fachada, y < 108)."""
    postes = list(range(x0, x1 + 1, 30))
    for (y, alto) in [(48, 3), (76, 3)]:                                             # tablones
        cv.rect(x0 - 2, y, x1 + 3, y + alto, K("madera", 5)); cv.hline(x0 - 2, x1 + 3, y + alto, K("madera", 2))
        for k in range(x0 + 8, x1, 17):
            cv.vline(k, y, y + alto, K("madera", 4))
    for a, b in zip(postes, postes[1:]):                                             # tornapuntas
        cv.d.line([(a + 1, 76), (b - 1, 51)], fill=K("madera", 3))
    for p in postes:
        cv.rect(p, 16, p + 2, FACHADA + 2, K("madera", 4)); cv.vline(p + 2, 16, FACHADA + 2, K("madera", 2))
        for y in (48, 76):
            cv.px(p - 1, y + 1, K("ocre", 2)); cv.px(p + 2, y + 1, K("ocre", 2))      # atados de cuerda
        cv.rect(p - 2, FACHADA + 1, p + 4, FACHADA + 3, K("madera", 2))              # durmiente
    # escalera de mano
    for k in (x0 + 36, x0 + 42):
        cv.vline(k, 50, FACHADA + 2, K("madera", 5))
    for y in range(54, FACHADA, 5):
        cv.hline(x0 + 36, x0 + 43, y, K("madera", 4))
    # en el tablón: un cubo, una pila de ladrillos y una carretilla de mortero
    cv.rect(x0 + 14, 42, x0 + 20, 48, K("gris", 5)); cv.hline(x0 + 14, x0 + 20, 42, K("gris", 7)); cv.px(x0 + 17, 40, K("gris", 3))
    cv.rect(x0 + 62, 40, x0 + 76, 48, K("granate", 5))                               # ladrillos apilados
    for yy in (42, 45):
        cv.hline(x0 + 62, x0 + 76, yy, K("granate", 3))
    for xx in range(x0 + 66, x0 + 76, 5):
        cv.vline(xx, 40, 48, K("granate", 3))
    cv.rect(x0 + 52, 72, x0 + 64, 76, K("papel", 2)); cv.hline(x0 + 52, x0 + 64, 72, K("papel", 3))   # saco de cal
    # polea con su cuerda
    cv.hline(x1 - 12, x1 + 4, 14, K("madera", 3)); cv.ellipse(x1 - 4, 14, x1 + 1, 19, K("gris", 3))
    cv.vline(x1 - 2, 19, 70, K("ocre", 2)); cv.rect(x1 - 5, 70, x1 + 1, 75, K("gris", 4))


def _cajon(cv, x, y, w, genero, rnd, d=7):
    """Caja de fruta vista en 3/4: el género se amontona por encima del borde; frente de tablillas (5 px)."""
    cv.rect(x, y, x + w, y + d, K("madera", 2))
    cols = {"manzanas": [K("rojo", 4), K("rojo", 3), K("granate", 5)], "coles": [K("pared", 5), K("pared", 4)],
            "zanahorias": [K("ocre", 3), K("ocre", 4)], "patatas": [K("madera", 5), K("madera", 4), K("ocre", 2)],
            "nabos": [K("papel", 4), K("papel", 3)], "peras": [K("ocre", 3), K("ocre", 4), K("pared", 6)]}[genero]
    bw = 4 if genero == "coles" else 3
    for fila in range(4):                                                            # de atrás hacia delante
        yy = y + fila * 2 - 1
        for xx in range(x + 1 + (fila % 2), x + w - bw, bw):
            t = (xx + bw / 2 - x) / w
            alto = int(2.5 * (1 - abs(2 * t - 1)))                                   # montón: más alto en el centro
            c = rnd.choice(cols)
            ramp, tono = LOOKUP[c]
            top = yy - alto
            if genero == "zanahorias":
                cv.hline(xx, xx + 3, top + 1, c); cv.px(xx + 3, top + 1, K("pared", 5)); cv.px(xx, top + 2, K(ramp, tono - 1))
                continue
            cv.rect(xx, top, xx + bw, top + 3, c)
            cv.px(xx, top, K(ramp, tono - 1)); cv.px(xx + bw - 1, top + 2, K(ramp, tono - 1))
            cv.px(xx + 1, top, K(ramp, tono + 1))                                    # brillo
            if genero == "nabos":
                cv.px(xx + 1, top, K("granate", 5))
            if genero == "coles":
                cv.px(xx + 1, top + 1, K("pared", 6)); cv.px(xx + 2, top + 1, K("pared", 6))
    cv.rect(x, y + d, x + w, y + d + 5, K("madera", 4))
    cv.hline(x, x + w, y + d, K("madera", 5)); cv.hline(x, x + w, y + d + 2, K("madera", 2))
    cv.vline(x, y, y + d + 5, K("madera", 2)); cv.vline(x + w - 1, y, y + d + 5, K("madera", 2))


def _toldo_remendado(cv, x0, x1, y, alto, colores, rnd):
    """Toldo de tela a rayas, inclinado hacia delante, con remiendos cosidos y el festón deshilachado."""
    for i, k in enumerate(range(x0, x1, 7)):
        cv.rect(k, y, min(x1, k + 7), y + alto, colores[i % 2])
        rampa, tono = LOOKUP[colores[i % 2]]
        cv.vline(min(x1, k + 7) - 1, y + 2, y + alto, K(rampa, tono - 1))           # pliegue de cada raya
    cv.hline(x0, x1, y, K("madera", 2))                                              # barra de arriba
    for k in range(x0, x1, 7):                                                       # festón
        c = colores[((k - x0) // 7) % 2]
        cv.rect(k + 1, y + alto, k + 6, y + alto + 2, c); cv.px(k + 3, y + alto + 2, c)
    for _ in range(3):                                                               # remiendos
        rx, ry = rnd.randint(x0 + 3, x1 - 12), rnd.randint(y + 2, y + alto - 7)
        pc = rnd.choice([K("ocre", 3), K("rojo", 4), K("pared", 5), K("papel", 3), K("granate", 5)])
        cv.rect(rx, ry, rx + 7, ry + 5, pc); cv.frame(rx, ry, rx + 7, ry + 5, K(LOOKUP[pc][0], LOOKUP[pc][1] - 1))
    cv.hline(x0, x1, y + alto - 1, K("gris", 3))


def _puesto(cv, x0, y0, x1, y1, colores, generos, rnd, cartel=None):
    """Puesto de mercado cuya base ocupa exactamente (x0, y0)-(x1, y1); el toldo sube por encima."""
    tapa = y1 - y0 - 14                                                              # profundidad de la mesa vista desde arriba
    # postes de atrás (asoman por encima de la mesa)
    for p in (x0 + 2, x1 - 4):
        cv.rect(p, y0 - 28, p + 2, y0 + 2, K("madera", 2))
    # mesa: tapa de tablones y frente
    cv.rect(x0, y0, x1, y0 + tapa, K("madera", 5))
    for k in range(y0 + 3, y0 + tapa, 4):
        cv.hline(x0, x1, k, K("madera", 4))
    cv.rect(x0, y0 + tapa, x1, y1 - 3, K("madera", 3)); cv.hline(x0, x1, y0 + tapa, K("madera", 6))
    for k in range(x0 + 6, x1, 9):
        cv.vline(k, y0 + tapa + 1, y1 - 3, K("madera", 2))
    cv.frame(x0, y0, x1, y1 - 3, K("madera", 1))
    for p in (x0 + 1, x1 - 4):                                                       # patas
        cv.rect(p, y1 - 3, p + 3, y1, K("madera", 2))
    # cajones de fruta y verdura sobre la mesa
    n = len(generos)
    cw = (x1 - x0 - 4) // n
    for i, g in enumerate(generos):
        _cajon(cv, x0 + 2 + i * cw + 1, y0 - 2, cw - 2, g, rnd, d=max(5, tapa - 5))
    # postes de delante y toldo
    alto_toldo = 13
    ty = y0 - 26
    for p in (x0, x1 - 2):                                                           # dentro de la huella
        cv.rect(p, ty, p + 2, y1, K("madera", 3)); cv.vline(p, ty, y1, K("madera", 5))
    _toldo_remendado(cv, x0 - 5, x1 + 5, ty, alto_toldo, colores, rnd)
    if cartel:                                                                       # pizarrita colgada del poste
        cx = x1 - 14
        cv.vline(cx + 5, ty + alto_toldo + 2, ty + alto_toldo + 5, K("ocre", 2))
        cv.rect(cx, ty + alto_toldo + 5, cx + 11, ty + alto_toldo + 12, K("gris", 1)); cv.frame(cx, ty + alto_toldo + 5, cx + 11, ty + alto_toldo + 12, K("madera", 3))
        cv.text(cx + 2, ty + alto_toldo + 6, cartel, K("papel", 4))


def _pila_ladrillos(cv, x, y_base, w, capas):
    """Pila de ladrillo nuevo sobre un palé, vista en 3/4. y_base = línea del suelo."""
    cv.rect(x, y_base - 3, x + w, y_base, K("madera", 3)); cv.hline(x, x + w, y_base - 3, K("madera", 5))
    for k in range(x + 2, x + w, 6):
        cv.px(k, y_base - 1, K("madera", 1))
    y = y_base - 3
    for c in range(capas):
        cv.rect(x + 1, y - 3, x + w - 1, y, K("granate", 4))                         # frente de la capa
        for k in range(x + 1 + (c % 2) * 3, x + w - 1, 6):
            cv.vline(k, y - 3, y, K("granate", 2))
        y -= 3
    cv.rect(x + 1, y - 6, x + w - 1, y, K("granate", 5))                             # cara de arriba
    for k in range(x + 1, x + w - 1, 6):
        cv.vline(k, y - 6, y, K("ocre", 2))
    cv.hline(x + 1, x + w - 1, y - 3, K("ocre", 2))


def _obra_y_puesto_b(cv, rnd):
    x0, y0, x1, y1 = ZONA_B
    # arena para el mortero
    cv.ellipse(x0 + 44, y1 - 18, x0 + 80, y1 - 1, K("ocre", 2))
    cv.ellipse(x0 + 48, y1 - 22, x0 + 74, y1 - 6, K("ocre", 3))
    cv.ellipse(x0 + 54, y1 - 23, x0 + 66, y1 - 14, K("ocre", 4))
    cv.vline(x0 + 72, y1 - 30, y1 - 8, K("madera", 4)); cv.rect(x0 + 69, y1 - 10, x0 + 76, y1 - 6, K("gris", 5))   # pala clavada
    # ladrillo nuevo apilado
    _pila_ladrillos(cv, x0 + 4, y1 - 2, 30, 4)
    _pila_ladrillos(cv, x0 + 10, y1 - 22, 22, 2)
    # puesto B
    a, b, c, d = PUESTO_B
    _puesto(cv, a, b, c, d, [K("ocre", 3), K("papel", 4)], ["coles", "patatas", "peras"], rnd)
    # tablones apilados y una carretilla con cal
    for i in range(3):
        yy = y1 - 4 - i * 3
        cv.rect(x1 - 26, yy - 3, x1 - 2, yy, K("madera", 5 - i % 2)); cv.vline(x1 - 3, yy - 3, yy, K("madera", 2))
        cv.hline(x1 - 26, x1 - 2, yy - 3, K("madera", 6))
    cv.rect(x1 - 24, y1 - 4, x1 - 4, y1 - 1, K("madera", 1))
    cv.poly([(x1 - 58, y1 - 17), (x1 - 34, y1 - 17), (x1 - 38, y1 - 8), (x1 - 53, y1 - 8)], K("gris", 4))
    cv.hline(x1 - 58, x1 - 33, y1 - 17, K("gris", 6)); cv.rect(x1 - 56, y1 - 16, x1 - 36, y1 - 14, K("papel", 3))
    cv.d.line([(x1 - 36, y1 - 15), (x1 - 27, y1 - 11)], fill=K("madera", 3))
    cv.vline(x1 - 40, y1 - 8, y1 - 2, K("madera", 2))
    cv.ellipse(x1 - 60, y1 - 10, x1 - 52, y1 - 2, K("gris", 2)); cv.px(x1 - 57, y1 - 7, K("gris", 5))
    # algún ladrillo viejo apartado, ya limpio, contra la pared
    for (bx, by) in [(x0 + 90, y0 + 2), (x0 + 96, y0 + 4), (x0 + 84, y0 + 5)]:
        cv.rect(bx, by, bx + 6, by + 3, K("granate", 3)); cv.hline(bx, bx + 6, by, K("granate", 4))


def _rayuela(cv, x, y):
    """Rayuela pintada con tiza en los adoquines (plana: no estorba al paso)."""
    tiza = K("papel", 3)
    celdas = [(0, 0, 1), (0, 1, 2), (0, 2, 3), (-1, 3, 4), (1, 3, 5), (0, 4, 6), (-1, 5, 7), (1, 5, 8)]
    for (cx, cy, n) in celdas:
        px_, py = x + cx * 11, y - cy * 8
        cv.frame(px_, py, px_ + 12, py + 9, tiza)
        cv.text(px_ + 5, py + 2, str(n), tiza)
    cv.d.arc([x - 2, y - 56, x + 14, y - 40], 180, 360, fill=tiza)
    cv.hline(x - 2, x + 15, y - 48, tiza)


def _sol(cv, fuerza):
    """Calidez del sol bajo que entra por la izquierda: un velo ocre suave, más fuerte hacia el oeste."""
    cv.glow_rgb = K("ocre", 4)
    for y in range(H):
        fila = cv.glow[y]
        for x in range(W):
            d = ((x + 40) ** 2 + ((y - 10) * 2) ** 2) ** 0.5
            k = fuerza * (0.10 + 0.12 * (1 - x / W) + 0.22 * max(0.0, 1 - d / 320))
            fila[x] = k * (0.45 if y < 26 and cv.img.getpixel((x, y)) in CIELO_MANANA else 1)   # el cielo, más azul


def dibujar_manana():
    rnd = random.Random(1904)                 # mismo generador y mismo orden que el atardecer: mismas casas
    rnd2 = random.Random(1984)                # todo lo nuevo sale de aquí
    cv = Canvas(W, H)
    _cielo_manana(cv, rnd2)
    # casas adosadas (mismo consumo de rnd que en dibujar())
    x, n = 0, 0
    casas = []
    while x < 690:
        w = rnd.randint(64, 88)
        if 270 <= x < 370:
            w = 92
        top = rnd.randint(26, 40)
        casa(cv, x, w, top, rnd, puerta_verde=(n == 3), manana=True)
        casas.append((x, w, top))
        x += w
        n += 1
    # chimeneas, una con una voluta muy tenue de desayuno
    for (cx, w, top) in casas:
        if cx not in (316,):
            _chimenea(cv, cx + w - 18, top, voluta=(cx == 157))
    # la puerta verde de Dot, con su 11
    px_, py0, px1, py1 = PUERTA_DOT
    cv.frame(px_ + 3, py0 + 15, px1 - 3, py1 - 3, K("tele", 2))                       # cuarterón
    cv.rect(px_ + 4, py0 + 5, px_ + 14, py0 + 12, K("papel", 3)); cv.frame(px_ + 4, py0 + 5, px_ + 14, py0 + 12, K("ocre", 2))
    cv.text(px_ + 6, py0 + 6, "11", K("gris", 1))
    cv.px(px_ + 14, py0 + 16, K("ocre", 4)); cv.px(px_ + 14, py0 + 17, K("ocre", 3))  # pomo
    cv.rect(px_ - 2, FACHADA, px1 + 2, FACHADA + 3, K("papel", 2))                   # escalón fregado
    for bx in (px1 + 3, px1 + 6):                                                    # botellas de leche
        cv.rect(bx, FACHADA - 5, bx + 2, FACHADA + 1, K("papel", 4)); cv.px(bx, FACHADA - 6, K("papel", 3)); cv.px(bx + 1, FACHADA - 6, K("ocre", 4))
    # pub «La Campana», cerrado a esta hora
    pb = 288
    cv.rect(pb, 60, pb + 74, FACHADA, K("madera", 1)); cv.frame(pb, 60, pb + 74, FACHADA, K("madera", 0))
    cv.rect(pb + 4, 64, pb + 70, 74, K("granate", 2)); cv.text(pb + 37 - cv.text_width("LA CAMPANA") // 2, 66, "LA CAMPANA", K("ocre", 4))
    for wx in (pb + 6, pb + 52):
        cv.rect(wx, 78, wx + 16, 96, K("cielo", 4)); cv.rect(wx, 88, wx + 16, 96, K("cielo", 3))
        for k in range(5):
            cv.px(wx + 2 + k, 84 - k, K("cielo", 6))
        cv.vline(wx + 8, 78, 96, K("madera", 0)); cv.hline(wx, wx + 16, 87, K("madera", 0))
    P.puerta(cv, pb + 28, FACHADA - 30, w=18, h=30, rampa="madera", base=2)
    cv.ellipse(pb + 33, 52, pb + 41, 60, K("ocre", 3), outline=K("ocre", 1)); cv.hline(pb + 30, pb + 44, 52, K("gris", 2))
    cv.px(pb + 35, 54, K("ocre", 4)); cv.px(pb + 35, 55, K("ocre", 4))
    # un gato rubio tomando el sol en el alféizar
    gx, gy = 171, 55
    cv.rect(gx, gy - 4, gx + 6, gy, K("ocre", 2)); cv.rect(gx + 4, gy - 7, gx + 8, gy - 3, K("ocre", 2))
    cv.px(gx + 4, gy - 8, K("ocre", 2)); cv.px(gx + 7, gy - 8, K("ocre", 2)); cv.hline(gx - 3, gx, gy - 1, K("ocre", 2))
    cv.px(gx + 2, gy - 4, K("ocre", 3)); cv.px(gx + 5, gy - 6, K("ocre", 3))
    # la casa alcanzada, reconstruida a medias, y la pared del fondo
    _casa_reconstruida(cv, 690, rnd2)
    ladrillo(cv, 890, 30, W, FACHADA, rnd2, base=1)
    cv.rect(890, 26, W, 30, K("gris", 2)); cv.hline(890, W, 26, K("gris", 4))
    ventana_manana(cv, 904, 40, 7); ventana_manana(cv, 930, 40, 8)
    # altavoz en su poste (callado)
    cv.rect(560, 10, 562, FACHADA, K("gris", 2))
    cv.poly([(562, 14), (574, 8), (574, 24), (562, 18)], K("gris", 4))
    # calle: adoquines secándose, charcos casi secos, una rayuela de tiza
    P.adoquines(cv, 0, FACHADA, W, CALLE, semilla=8)
    for (cx, cy, rw) in CHARCOS:                                                    # lo que queda de los charcos
        cv.ellipse(cx - rw // 3, cy - 1, cx + rw // 3, cy + 2, K("cielo", 3))
        cv.hline(cx - rw // 3 + 2, cx + 1, cy, K("cielo", 5))
    _rayuela(cv, 236, 214)
    # bordillo y muro bajo de enfrente
    cv.rect(0, CALLE, W, CALLE + 4, K("gris", 3)); cv.hline(0, W, CALLE, K("gris", 6))
    ladrillo(cv, 0, CALLE + 4, W, H, rnd2, base=1)

    # ---- tendederos (las prendas se calculan antes para proyectar su sombra en la pared)
    lineas = [(20, 150, 30), (170, 262, 26), (380, 520, 32), (590, 680, 28),
              (88, 226, 52), (404, 548, 54), (562, 676, 48), (896, 958, 46), (6, 80, 58)]
    tendederos = [(a, b, y, _prendas(a, b, y, rnd2)) for (a, b, y) in lineas]

    # ---- luz de la mañana sobre el fondo: sol bajo por la izquierda
    cv.add_light(0, 18, W, FACHADA, 1)                                               # fachadas
    cv.add_light(0, FACHADA, W, H, 2)                                                # la calle, a pleno sol
    for (cx, w, top) in casas:                                                       # los pisos altos ya tienen sol
        cv.add_light(cx, top - 4, cx + w, top + 30, 1)
    for (cx, cy, rw) in CHARCOS:                                                     # humedad que se seca
        cv.add_light_fn(lambda x, y, cx=cx, cy=cy, rw=rw: -1 if ((x - cx) / rw) ** 2 + ((y - cy) / 6) ** 2 < 1
                        and (x * 7 + y * 3) % 5 else 0)
    cv.add_light(690, 18, 760, 52, 1); cv.add_light(866, 36, 960, 60, 1)
    for (a, b, y, prendas) in tendederos:                                            # sombra de la ropa en la pared
        for (_, px_, py, pw, ph, _) in prendas:
            cv.add_light(px_ + 2, py + 2, px_ + pw + 2, py + ph + 2, -1)
    for fx in FAROLAS:                                                               # sombras largas hacia la derecha
        for k in range(0, 58):
            yy = 168 + k // 14
            cv.add_light(fx + 2 + k, yy - 1, fx + 3 + k, yy + 1, -1)
        cv.add_light(fx + 58, 169, fx + 66, 175, -1)
    for (a, b, c, d) in (PUESTO_A, PUESTO_B):                                        # sombra de los puestos
        for k in range(0, 34):
            cv.add_light(c + k, b + 2 + k // 4, c + k + 1, d + 1, -1)
    x0b, y0b, x1b, y1b = ZONA_B
    cv.add_light(x0b + 34, y1b - 8, x0b + 46, y1b, -1)
    cv.add_light(560, 104, 622, 108, -1)                                              # el poste del altavoz
    _sol(cv, 1.0)
    cv.bake_lighting()

    # ---- primer plano (segunda pasada de luz, más suave)
    cv.light = [[0] * W for _ in range(H)]
    cv.glow = [[0.0] * W for _ in range(H)]
    cv.emissive = []
    _andamio(cv, 758, 868)
    for (a, b, y, prendas) in tendederos:
        _tendedero(cv, a, b, y, prendas)
    a, b, c, d = PUESTO_A
    _puesto(cv, a, b, c, d, [K("granate", 4), K("papel", 4)], ["manzanas", "zanahorias", "coles", "nabos"], rnd2, cartel="2D")
    _obra_y_puesto_b(cv, rnd2)
    for fx in FAROLAS:                                                               # apagadas
        P.farola(cv, fx, 168, encendida=False)
    _sol(cv, 0.5)
    cv.bake_lighting()
    return cv
