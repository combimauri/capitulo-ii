"""Imágenes de la telepantalla de los Dos Minutos de Odio (80x60), el mapa de corcho del frente y el mapa de
los frentes del este (360x200)."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from pixel import Canvas, K  # noqa: E402
import props as P  # noqa: E402

W, H = 80, 60


def _fondo(cv, tono=1):
    cv.rect(0, 0, W, H, K("tele", tono))
    for y in range(0, H, 2):
        cv.hline(0, W, y, K("tele", max(0, tono - 1)))


def goldstein():
    cv = Canvas(W, H)
    _fondo(cv)
    # columnas de soldados al fondo
    for x in range(2, W, 7):
        cv.rect(x, 44, x + 4, 58, K("tele", 2)); cv.rect(x, 40, x + 4, 44, K("tele", 3))
    cx = 40
    cv.ellipse(cx - 15, 6, cx + 15, 46, K("tele", 4))                     # cara alargada
    cv.ellipse(cx - 17, 2, cx + 17, 20, K("tele", 6))                     # pelo blanco revuelto
    cv.ellipse(cx - 13, 10, cx + 13, 44, K("tele", 4))
    for (ex) in (cx - 9, cx + 3):                                          # gafas
        cv.frame(ex, 20, ex + 7, 26, K("tele", 1)); cv.px(ex + 3, 23, K("tele", 0))
    cv.hline(cx - 2, cx + 3, 22, K("tele", 1))
    cv.d.line([cx, 26, cx - 2, 33], fill=K("tele", 2))                    # nariz
    cv.poly([(cx - 6, 38), (cx + 6, 38), (cx + 3, 52), (cx, 55), (cx - 3, 52)], K("tele", 6))   # perilla blanca
    cv.hline(cx - 4, cx + 4, 37, K("tele", 1))                            # boca balando

    return cv.img


def oveja():
    cv = Canvas(W, H)
    _fondo(cv)
    cx = 40
    for (x, y, r) in [(cx - 16, 10, 9), (cx + 16, 10, 9), (cx - 18, 26, 8), (cx + 18, 26, 8), (cx, 6, 10)]:
        cv.ellipse(x - r, y - r, x + r, y + r, K("tele", 6))                # lana
    cv.ellipse(cx - 12, 10, cx + 12, 48, K("tele", 3))                    # cara
    cv.ellipse(cx - 22, 18, cx - 10, 24, K("tele", 3)); cv.ellipse(cx + 10, 18, cx + 22, 24, K("tele", 3))   # orejas
    for ex in (cx - 7, cx + 4):                                            # gafas (sigue siendo él)
        cv.frame(ex, 22, ex + 6, 27, K("tele", 1))
    cv.ellipse(cx - 5, 38, cx + 5, 46, K("tele", 2)); cv.hline(cx - 3, cx + 3, 44, K("tele", 0))
    cv.text(28, 52, "BEEE", K("tele", 6))
    return cv.img


def soldado():
    cv = Canvas(W, H)
    _fondo(cv, 0)
    cx = 40
    cv.ellipse(cx - 20, 4, cx + 20, 30, K("tele", 2))                      # casco
    cv.rect(cx - 22, 22, cx + 22, 26, K("tele", 1))
    cv.ellipse(cx - 14, 20, cx + 14, 52, K("tele", 3))                     # cara
    cv.rect(cx - 10, 30, cx - 3, 33, K("tele", 0)); cv.rect(cx + 3, 30, cx + 10, 33, K("tele", 0))   # ojos
    cv.px(cx - 6, 31, K("rojo", 4)); cv.px(cx + 6, 31, K("rojo", 4))
    cv.hline(cx - 6, cx + 6, 44, K("tele", 0)); cv.hline(cx - 5, cx + 5, 45, K("tele", 0))
    cv.rect(cx - 30, 50, cx + 30, H, K("tele", 2))                         # hombros
    cv.d.line([cx + 18, H, cx + 34, 20], fill=K("tele", 1), width=3)       # fusil
    cv.text(6, 2, "EURASIA", K("rojo", 4))
    return cv.img


def diccionario():
    cv = Canvas(W, H)
    _fondo(cv, 0)
    cx, cy = 40, 30
    rnd = random.Random(3)
    for _ in range(14):                                                    # pantalla rajada
        a = rnd.uniform(0, 6.28)
        import math
        cv.d.line([cx, cy, cx + int(math.cos(a) * 40), cy + int(math.sin(a) * 30)], fill=K("tele", 5))
    cv.poly([(cx - 14, cy - 6), (cx + 10, cy - 12), (cx + 16, cy + 6), (cx - 8, cy + 12)], K("rojo", 3))   # libro
    cv.poly([(cx - 12, cy - 4), (cx + 9, cy - 9), (cx + 13, cy + 4), (cx - 7, cy + 9)], K("papel", 4))
    cv.d.line([(cx - 2, cy - 7), (cx + 2, cy + 10)], fill=K("rojo", 1))
    cv.text(16, 50, "NEOLENGUA", K("tele", 6))
    return cv.img


def gran_hermano():
    cv = Canvas(W, H, bg=("tele", 1))
    pal = {"h": K("tele", 1), "b": K("tele", 0), "m": K("tele", 0), "e": K("tele", 0),
           "s": K("tele", 4), "S": K("tele", 3), "n": K("tele", 2), "c": K("tele", 2)}
    big = Canvas(24, 24, bg=("tele", 1))
    P.cara_gran_hermano(big, 0, 0, pal)
    cv.img.paste(big.img.resize((48, 48), 0), (16, 4))
    cv.text(40 - cv.text_width("GRAN HERMANO") // 2, 53, "GRAN HERMANO", K("tele", 6))
    return cv.img


def amory():
    """Felix Amory confesando: sin gafas, rapado, la cara hinchada, huecos donde había dientes."""
    cv = Canvas(W, H)
    _fondo(cv, 0)
    cx = 40
    cv.rect(0, 50, W, H, K("tele", 1))                                                   # mesa de la confesión
    cv.rect(cx - 25, 44, cx + 25, H, K("tele", 2))                                       # mono que le queda enorme
    cv.poly([(cx - 25, 44), (cx - 6, 40), (cx, 48), (cx + 6, 40), (cx + 25, 44)], K("tele", 3))
    cv.d.line([(cx - 6, 40), (cx, 48), (cx + 6, 40)], fill=K("tele", 1))                 # cuello abierto
    cv.rect(cx - 4, 36, cx + 4, 44, K("tele", 3)); cv.vline(cx - 4, 37, 44, K("tele", 2))   # cuello flaquísimo
    cv.hline(cx - 9, cx - 3, 46, K("tele", 4)); cv.hline(cx + 3, cx + 9, 46, K("tele", 4))  # clavículas
    cv.ellipse(cx - 13, 4, cx + 13, 40, K("tele", 4))                                    # cabeza rapada
    cv.ellipse(cx - 11, 4, cx + 11, 16, K("tele", 3))                                    # cráneo con el pelo al cero
    for (x, y) in ((cx - 7, 7), (cx - 3, 6), (cx + 2, 6), (cx + 6, 8), (cx - 9, 11), (cx + 9, 11), (cx, 9)):
        cv.px(x, y, K("tele", 2))
    cv.rect(cx - 15, 18, cx - 12, 26, K("tele", 3)); cv.rect(cx + 13, 18, cx + 16, 26, K("tele", 3))   # orejas de soplillo
    cv.ellipse(cx - 14, 20, cx + 14, 39, K("tele", 4))                                   # cara hinchada, más ancha abajo
    cv.d.arc([cx - 13, 22, cx - 3, 32], 200, 300, fill=K("tele", 5))                     # brillo de la hinchazón
    cv.d.arc([cx + 3, 22, cx + 13, 32], 240, 340, fill=K("tele", 5))
    for ex, sw in ((cx - 9, K("tele", 3)), (cx + 3, K("tele", 3))):                     # ojos hinchados, sin gafas
        cv.rect(ex, 18, ex + 7, 23, sw)
        cv.hline(ex + 1, ex + 6, 20, K("tele", 0)); cv.px(ex + 3, 21, K("tele", 0))
        cv.hline(ex + 1, ex + 6, 22, K("tele", 2))
    cv.px(cx - 6, 25, K("tele", 2)); cv.px(cx + 7, 24, K("tele", 2))                     # marcas donde apoyaban las gafas
    cv.d.line([(cx, 22), (cx - 1, 28)], fill=K("tele", 3)); cv.hline(cx - 2, cx + 2, 29, K("tele", 3))   # nariz
    cv.rect(cx - 5, 31, cx + 6, 35, K("tele", 0)); cv.hline(cx - 4, cx + 5, 35, K("tele", 0))   # boca entreabierta
    cv.hline(cx - 4, cx + 6, 31, K("tele", 6))                                          # dientes, con huecos
    for x in (cx - 2, cx + 1, cx + 2, cx + 5):
        cv.px(x, 31, K("tele", 0))
    cv.hline(cx - 3, cx + 4, 34, K("tele", 5)); cv.px(cx, 34, K("tele", 0)); cv.px(cx + 3, 34, K("tele", 0))
    cv.hline(cx - 5, cx + 6, 36, K("tele", 3))
    cv.d.line([(cx - 8, 13), (cx - 3, 15)], fill=K("tele", 3)); cv.d.line([(cx + 8, 13), (cx + 3, 15)], fill=K("tele", 3))
    cv.rect(16, 46, 22, 52, K("tele", 1)); cv.vline(19, 52, 58, K("tele", 1))
    cv.rect(2, 53, 35, 59, K("tele", 0)); cv.text(4, 54, "F. AMORY", K("tele", 6))
    return cv.img


def estasia():
    """El nuevo enemigo: un soldado de Estasia bajo una bandera amarilla."""
    cv = Canvas(W, H)
    _fondo(cv, 0)
    cv.vline(10, 2, H, K("tele", 2))                                                     # asta
    cv.poly([(11, 3), (36, 5), (34, 13), (38, 21), (11, 19)], K("ocre", 3))              # bandera amarilla, al viento
    cv.poly([(11, 13), (35, 14), (38, 21), (11, 19)], K("ocre", 2))
    cx = 46
    cv.ellipse(cx - 18, 6, cx + 18, 30, K("tele", 2))                                    # gorro acolchado con orejeras
    cv.rect(cx - 18, 18, cx + 18, 24, K("tele", 3))
    for k in range(cx - 16, cx + 17, 4):
        cv.vline(k, 9, 18, K("tele", 1))
    cv.px(cx, 13, K("ocre", 4)); cv.px(cx - 1, 14, K("ocre", 4)); cv.px(cx + 1, 14, K("ocre", 4))   # estrella
    cv.ellipse(cx - 13, 18, cx + 13, 50, K("tele", 3))                                   # cara
    cv.rect(cx - 19, 22, cx - 12, 40, K("tele", 2)); cv.rect(cx + 12, 22, cx + 19, 40, K("tele", 2))   # orejeras
    cv.rect(cx - 9, 28, cx - 3, 31, K("tele", 0)); cv.rect(cx + 3, 28, cx + 9, 31, K("tele", 0))   # ojos
    cv.px(cx - 6, 29, K("ocre", 4)); cv.px(cx + 6, 29, K("ocre", 4))
    cv.d.line([(cx - 10, 26), (cx - 3, 27)], fill=K("tele", 1)); cv.d.line([(cx + 10, 26), (cx + 3, 27)], fill=K("tele", 1))
    cv.hline(cx - 5, cx + 5, 42, K("tele", 0)); cv.hline(cx - 4, cx + 4, 43, K("tele", 0))
    cv.rect(cx - 28, 50, cx + 28, H, K("tele", 2))                                       # hombros
    cv.d.line([cx + 22, H, cx + 30, 18], fill=K("tele", 1), width=3)                     # fusil
    cv.text(42, 1, "ESTASIA", K("ocre", 3))
    return cv.img


def mapa_frente():
    """Corcho, mapa del sector de Malabar y cientos de agujeros de alfiler a ambos lados del río."""
    rnd = random.Random(1984)
    cv = Canvas(360, 200)
    cv.rect(0, 0, 360, 200, K("ocre", 2))
    for _ in range(4000):
        cv.px(rnd.randint(0, 359), rnd.randint(0, 199), K("ocre", rnd.choice([1, 1, 3])))
    cv.rect(10, 8, 350, 192, K("papel", 3)); cv.frame(10, 8, 350, 192, K("papel", 1))
    for x in range(10, 350, 30):
        cv.vline(x, 8, 192, K("papel", 2))
    for y in range(8, 192, 30):
        cv.hline(10, 350, y, K("papel", 2))
    cv.poly([(10, 8), (110, 8), (90, 40), (40, 52), (10, 60)], K("cielo", 5))           # mar
    # el río Malabar
    rio = [(20, 190), (60, 150), (110, 128), (160, 132), (210, 116), (260, 108), (310, 92), (345, 70)]
    cv.d.line(rio, fill=K("cielo", 3), width=4)
    cv.d.line(rio, fill=K("cielo", 5), width=1)
    # agujeros de alfiler: concentrados en una franja estrecha a ambos lados del río
    for _ in range(900):
        i = rnd.randint(0, len(rio) - 2)
        (x0, y0), (x1, y1) = rio[i], rio[i + 1]
        t = rnd.random()
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        cv.px(int(x + rnd.gauss(0, 7)), int(y + rnd.gauss(0, 9)), K("gris", rnd.choice([2, 3])))
    # banderas negras enemigas al otro lado del río
    for (x, y) in [(90, 112), (150, 112), (205, 98), (260, 90), (305, 74)]:
        cv.vline(x, y - 10, y, K("gris", 1)); cv.rect(x + 1, y - 10, x + 7, y - 6, K("gris", 0))
    cv.text(250, 175, "SECTOR MALABAR", K("gris", 1))
    cv.text(60, 20, "OCEANO INDICO", K("cielo", 2))
    return cv.img


# casillas donde se clavan las banderitas amarillas (centro de cada casilla, en píxeles de la imagen)
BANDERITAS_ESTASIA = {"MONGOLIA": [(78, 74), (128, 92)], "MANCHURIA": [(214, 52), (238, 88)],
                      "INDONESIA": [(150, 162), (262, 170)]}


def mapa_estasia():
    """El mapa nuevo: los frentes del este, con casillas vacías para las banderitas de Estasia."""
    rnd = random.Random(1985)
    cv = Canvas(360, 200)
    cv.rect(0, 0, 360, 200, K("ocre", 2))
    for _ in range(4000):
        cv.px(rnd.randint(0, 359), rnd.randint(0, 199), K("ocre", rnd.choice([1, 1, 3])))
    cv.rect(10, 8, 350, 192, K("cielo", 5)); cv.frame(10, 8, 350, 192, K("papel", 1))   # el mar
    costa = [(10, 8), (262, 8), (270, 30), (256, 48), (268, 66), (258, 96), (238, 116), (204, 126), (170, 122),
             (146, 132), (120, 126), (90, 134), (60, 128), (10, 136)]
    cv.poly(costa, K("papel", 3))                                                        # el continente
    cv.d.line(costa[1:], fill=K("cielo", 3))
    cv.poly([(282, 22), (296, 14), (300, 34), (288, 58), (280, 50)], K("papel", 3))     # una isla al este
    for isla in ([(96, 152), (130, 146), (172, 156), (180, 166), (140, 170), (100, 164)],          # Indonesia
                 [(196, 168), (240, 160), (290, 166), (300, 176), (250, 180), (204, 178)],
                 [(186, 142), (204, 140), (210, 150), (194, 154)], [(306, 150), (326, 146), (330, 158), (312, 160)]):
        cv.poly(isla, K("papel", 3)); cv.d.line(isla + [isla[0]], fill=K("cielo", 3))
    for y in range(8, 192):                                                             # cuadrícula, sobre tierra y mar
        for x in range(10, 350):
            if (x - 10) % 30 == 0 or (y - 8) % 30 == 0:
                cv.px(x, y, K("cielo", 4) if cv.img.getpixel((x, y)) == K("cielo", 5) else K("papel", 2))
    # fronteras de puntos entre Mongolia y Manchuria, y con el resto del continente
    for (a, b) in (((168, 8), (176, 60)), ((176, 60), (162, 122)), ((10, 112), (176, 104))):
        n = int(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5) // 3
        for k in range(n):
            if k % 2 == 0:
                cv.px(a[0] + (b[0] - a[0]) * k // n, a[1] + (b[1] - a[1]) * k // n, K("gris", 3))
    # líneas de frente nuevas, a lápiz rojo, todavía sin agujeros
    cv.d.line([(56, 60), (90, 54), (122, 66), (150, 60)], fill=K("rojo", 3))
    cv.d.line([(196, 34), (222, 40), (246, 70), (236, 102)], fill=K("rojo", 3))
    cv.d.line([(118, 156), (160, 154), (218, 168), (280, 166)], fill=K("rojo", 3))
    for region, puntos in BANDERITAS_ESTASIA.items():                                     # casillas vacías
        for (x, y) in puntos:
            cv.frame(x - 5, y - 5, x + 6, y + 6, K("gris", 3)); cv.frame(x - 4, y - 4, x + 5, y + 5, K("papel", 4))
            cv.px(x, y, K("gris", 2))
    cv.text(60, 30, "MONGOLIA", K("gris", 1))
    cv.text(196, 20, "MANCHURIA", K("gris", 1))
    cv.text(184, 184, "INDONESIA", K("gris", 1))
    cv.text(290, 110, "PACIFICO", K("cielo", 2))
    cv.text(20, 172, "MAR DE LA CHINA", K("cielo", 2))
    cv.text(20, 12, "FRENTES DEL ESTE", K("rojo", 2))
    return cv.img


# ---------------------------------------------------------------- fichas policiales de los presos (24x28 cada una)

FICHAS = [  # nombre, rasgos
    ("CHEN W.", dict(ancho=11, alto=14, piel=8, pelo="liso", tono_pelo=1, cejas=1, nariz=2, boca="fina", ojeras=True, num="412")),
    ("KOVAL D.", dict(ancho=13, alto=15, piel=7, pelo="calvo", tono_pelo=6, cejas=2, nariz=3, boca="bigote", arrugas=True, num="413")),
    ("PIKE L.", dict(ancho=14, alto=14, piel=7, pelo="rapado", tono_pelo=2, cejas=2, nariz=2, boca="recta", barba=True,
                     cuello=7, hombros=12, ancla=True, num="414")),
    ("HOGAN T.", dict(ancho=11, alto=14, piel=8, pelo="rizado", tono_pelo=5, cejas=1, nariz=2, boca="torcida", moraton=True, num="415")),
    ("R1", dict(ancho=11, alto=16, piel=7, pelo="entradas", tono_pelo=3, cejas=1, nariz=3, boca="recta", gafas=True, num="581")),
    ("R2", dict(ancho=11, alto=14, piel=8, pelo="recogido", tono_pelo=2, cejas=1, nariz=1, boca="fina", num="582")),
    ("R3", dict(ancho=12, alto=15, piel=7, pelo="ralo", tono_pelo=8, cejas=1, nariz=3, boca="hundida", arrugas=True,
                ojeras=True, num="583")),
    ("R4", dict(ancho=10, alto=13, piel=8, pelo="flequillo", tono_pelo=2, cejas=1, nariz=1, boca="fina", cuello=3,
                hombros=8, ojos_grandes=True, orejas=True, num="584")),
    ("R5", dict(ancho=12, alto=14, piel=7, pelo="rapado", tono_pelo=4, cejas=2, nariz=2, boca="recta", cicatriz=True, num="585")),
]


def ficha(r):
    g = lambda i: K("gris", i)
    cv = Canvas(24, 28, bg=("gris", 9))
    for y in range(3, 22, 4):                                                            # tallímetro
        cv.hline(0, 24, y, g(8)); cv.hline(0, 2, y + 2, g(8))
    cx, w, h = 12, r["ancho"], r["alto"]
    ty = 3 if h >= 15 else 4
    x0, x1 = cx - w // 2, cx - w // 2 + w
    hombros = r.get("hombros", 10)
    cv.poly([(cx - hombros, 28), (cx - hombros + 2, 22), (cx + hombros - 2, 22), (cx + hombros, 28)], g(3))   # ropa de preso
    cuello = r.get("cuello", 5)
    cv.rect(cx - cuello // 2, ty + h - 2, cx - cuello // 2 + cuello, 23, g(r["piel"] - 1))
    if r.get("ancla"):                                                                   # ancla de Limehouse en el cuello
        cv.grid(cx - 1, 17, ["..x..", ".xxx.", "..x..", "x.x.x", ".xxx."], {"x": g(2)})
    if r.get("orejas"):
        cv.rect(x0 - 2, ty + 5, x0, ty + 9, g(r["piel"] - 1)); cv.rect(x1, ty + 5, x1 + 2, ty + 9, g(r["piel"] - 1))
    else:
        cv.rect(x0 - 1, ty + 6, x0, ty + 9, g(r["piel"] - 1)); cv.rect(x1, ty + 6, x1 + 1, ty + 9, g(r["piel"] - 1))
    cv.ellipse(x0, ty, x1, ty + h, g(r["piel"]))
    cv.vline(x1 - 2, ty + 4, ty + h - 3, g(r["piel"] - 1))                                # sombra lateral (flash de frente)
    tp, pelo = g(r["tono_pelo"]), r["pelo"]
    if pelo == "liso":
        cv.ellipse(x0, ty - 1, x1, ty + 6, tp); cv.rect(x0, ty + 2, x0 + 1, ty + 6, tp); cv.rect(x1 - 1, ty + 2, x1, ty + 6, tp)
        cv.hline(x0 + 2, x1 - 2, ty + 4, tp)
    elif pelo == "calvo":
        cv.rect(x0, ty + 3, x0 + 2, ty + 8, tp); cv.rect(x1 - 2, ty + 3, x1, ty + 8, tp)
        cv.px(cx - 2, ty + 1, g(r["piel"] + 1)); cv.px(cx - 1, ty + 1, g(r["piel"] + 1))   # brillo de la calva
    elif pelo == "rapado":
        cv.ellipse(x0, ty - 1, x1, ty + 5, g(r["piel"] - 2))                             # pelo al cero
        cv.hline(x0 + 2, x1 - 2, ty + 4, g(r["piel"] - 1))
    elif pelo == "rizado":
        for (dx, dy) in ((0, 0), (3, -1), (6, -1), (9, 0), (-1, 3), (10, 3), (2, 2), (5, 1), (8, 2)):
            cv.ellipse(x0 + dx - 1, ty + dy - 1, x0 + dx + 3, ty + dy + 3, tp)
    elif pelo == "entradas":
        cv.ellipse(x0, ty - 1, x1, ty + 4, tp); cv.ellipse(cx - 4, ty, cx + 4, ty + 6, g(r["piel"]))
        cv.rect(x0, ty + 2, x0 + 1, ty + 7, tp); cv.rect(x1 - 1, ty + 2, x1, ty + 7, tp)
    elif pelo == "recogido":
        cv.ellipse(x0, ty - 1, x1, ty + 6, tp); cv.ellipse(cx - 1, ty + 2, cx + 6, ty + 6, g(r["piel"]))   # raya al lado
        cv.rect(x0, ty + 2, x0 + 1, ty + 9, tp); cv.rect(x1 - 1, ty + 2, x1, ty + 9, tp)
    elif pelo == "ralo":
        for k in range(x0 + 1, x1 - 1, 2):
            cv.px(k, ty, tp); cv.px(k + 1, ty + 1, tp)
        cv.rect(x0, ty + 3, x0 + 1, ty + 8, tp); cv.rect(x1 - 1, ty + 3, x1, ty + 8, tp)
    elif pelo == "flequillo":
        cv.ellipse(x0 - 1, ty - 1, x1 + 1, ty + 6, tp)
        cv.poly([(x0, ty + 3), (x1, ty + 3), (x1 - 2, ty + 6), (cx, ty + 5), (x0 + 2, ty + 7)], tp)
    ey = ty + h * 9 // 20 + 1
    ex1, ex2 = cx - 3, cx + 2
    if r.get("ojos_grandes"):
        for ex in (ex1, ex2):
            cv.rect(ex - 1, ey - 1, ex + 2, ey + 1, g(9)); cv.rect(ex, ey - 1, ex + 1, ey + 1, g(1))
    else:
        cv.hline(ex1 - 1, ex1 + 1, ey, g(1)); cv.hline(ex2, ex2 + 2, ey, g(1))
    for ex in (ex1 - 1, ex2):                                                            # cejas
        cv.rect(ex, ey - 2 - (1 if r["cejas"] > 1 else 0), ex + 2, ey - 1, g(r["tono_pelo"] if r["tono_pelo"] < 6 else 4))
    if r.get("ojeras"):
        cv.hline(ex1 - 1, ex1 + 1, ey + 1, g(r["piel"] - 2)); cv.hline(ex2, ex2 + 2, ey + 1, g(r["piel"] - 2))
    if r.get("gafas"):
        cv.frame(ex1 - 2, ey - 1, ex1 + 3, ey + 2, g(3)); cv.frame(ex2 - 1, ey - 1, ex2 + 4, ey + 2, g(3))
        cv.hline(ex1 + 3, ex2 - 1, ey, g(3))
    if r.get("moraton"):
        cv.rect(ex2 - 1, ey - 1, ex2 + 3, ey + 2, g(4)); cv.hline(ex2, ex2 + 2, ey, g(1))
    nl = r["nariz"]
    cv.vline(cx, ey + 1, ey + 1 + nl, g(r["piel"] - 1)); cv.hline(cx - 1, cx + 1, ey + 1 + nl, g(r["piel"] - 2))
    my = min(ty + h - 3, ey + nl + 4)
    boca = r["boca"]
    if boca == "bigote":                                                                # bigote caído
        cv.hline(cx - 3, cx + 4, my - 1, g(3)); cv.px(cx - 3, my, g(3)); cv.px(cx + 3, my, g(3))
    elif boca == "torcida":
        cv.hline(cx - 2, cx + 1, my, g(2)); cv.px(cx + 1, my - 1, g(2))
    elif boca == "hundida":
        cv.hline(cx - 2, cx + 3, my, g(2)); cv.px(cx - 3, my - 1, g(r["piel"] - 2)); cv.px(cx + 3, my - 1, g(r["piel"] - 2))
    elif boca == "fina":
        cv.hline(cx - 1, cx + 2, my, g(r["piel"] - 3))
    else:
        cv.hline(cx - 2, cx + 3, my, g(2))
    if r.get("barba"):                                                                   # barba de varios días
        for k in range(x0 + 2, x1 - 1):
            for yy in (my + 1, my + 2, my - 1):
                if (k + yy) % 2 and abs(k - cx) > (0 if yy != my - 1 else 2):
                    cv.px(k, yy, g(r["piel"] - 1))
    if r.get("arrugas"):
        cv.hline(cx - 2, cx + 2, ty + 3, g(r["piel"] - 1))
        cv.px(x0 + 2, my - 1, g(r["piel"] - 1)); cv.px(x1 - 3, my - 1, g(r["piel"] - 1))
    if r.get("cicatriz"):
        cv.d.line([(x0 + 2, ey + 1), (x0 + 4, ey + 5)], fill=g(r["piel"] + 2))
    cv.rect(5, 22, 19, 28, g(1)); cv.text(7, 23, r["num"], g(9))                         # pizarrita con el número
    return cv.img


def fichas_presos():
    """Hoja de 9 fotogramas de 24x28: CHEN W., KOVAL D., PIKE L., HOGAN T. y la lista de reserva (R1-R5)."""
    from PIL import Image
    hoja = Image.new("RGB", (24 * len(FICHAS), 28))
    for i, (_, rasgos) in enumerate(FICHAS):
        hoja.paste(ficha(rasgos), (i * 24, 0))
    return hoja


def exportar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    for nombre, f in (("goldstein", goldstein), ("oveja", oveja), ("soldado", soldado),
                      ("diccionario", diccionario), ("gran_hermano", gran_hermano),
                      ("amory", amory), ("estasia", estasia)):
        f().save(destino / f"cf-{nombre}.png")
    mapa_frente().save(destino / "mapa-frente.png")
    mapa_estasia().save(destino / "mapa-estasia.png")
    fichas_presos().save(destino / "fichas-presos.png")


if __name__ == "__main__":
    from PIL import Image
    S = Path(sys.argv[1])
    hoja = Image.new("RGB", (W * 5 + 20, H))
    for i, f in enumerate((goldstein, oveja, soldado, diccionario, gran_hermano)):
        hoja.paste(f(), (i * (W + 5), 0))
    hoja.resize((hoja.width * 3, H * 3), 0).save(S / "odio.png")
    mapa_frente().resize((720, 400), 0).save(S / "mapa.png")
