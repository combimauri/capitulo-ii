"""Atrezo reutilizable para los escenarios (perspectiva cenital 3/4, biblia visual §4)."""
import random

from pixel import K

# ---------------------------------------------------------------- suelos y paredes


def tablones(cv, x0, y0, x1, y1, rampa="madera", base=3, semilla=1):
    rnd = random.Random(semilla)
    cv.rect(x0, y0, x1, y1, K(rampa, base))
    for y in range(y0, y1, 8):
        cv.hline(x0, x1, y, K(rampa, base - 2)); cv.hline(x0, x1, y + 1, K(rampa, base + 1))
        x = x0 - rnd.randint(0, 60)
        while x < x1:
            w = rnd.randint(44, 90)
            if x > x0:
                cv.vline(x, y, min(y + 8, y1), K(rampa, base - 2))
            lo, hi = max(x0 + 2, x + 4), min(x1 - 14, x + w - 8)
            if hi > lo:
                gx = rnd.randint(lo, hi)
                cv.hline(gx, gx + rnd.randint(4, 12), y + rnd.randint(3, 6), K(rampa, base - 1))
            x += w


def baldosas(cv, x0, y0, x1, y1, a, b, t=16, linea=None):
    """Suelo de baldosas en damero (a y b son colores)."""
    for y in range(y0, y1, t):
        for x in range(x0, x1, t):
            cv.rect(x, y, min(x + t, x1), min(y + t, y1), a if ((x - x0) // t + (y - y0) // t) % 2 == 0 else b)
    if linea:
        for y in range(y0, y1, t):
            cv.hline(x0, x1, y, linea)
        for x in range(x0, x1, t):
            cv.vline(x, y0, y1, linea)


def adoquines(cv, x0, y0, x1, y1, semilla=3, rampa="gris", base=3):
    rnd = random.Random(semilla)
    cv.rect(x0, y0, x1, y1, K(rampa, base - 1))
    for fila, y in enumerate(range(y0, y1, 6)):
        off = (fila % 2) * 5
        for x in range(x0 - off, x1, 10):
            cv.rect(max(x0, x + 1), y + 1, min(x1, x + 9), min(y1, y + 5), K(rampa, base + rnd.choice([0, 0, 1, -1])))


def papel_pintado(cv, x0, y0, x1, y1, rampa="pared", base=3, motivo="rombo"):
    cv.rect(x0, y0, x1, y1, K(rampa, base))
    if motivo == "rombo":
        for x in range(x0, x1, 6):
            cv.vline(x, y0, y1, K(rampa, base - 1))
        for y in range(y0 + 3, y1 - 2, 6):
            for x in range(x0 + 3 + (y // 6 % 2) * 3, x1 - 1, 6):
                cv.px(x, y, K(rampa, base + 1)); cv.px(x, y + 2, K(rampa, base + 1))
                cv.px(x - 1, y + 1, K(rampa, base + 1)); cv.px(x + 1, y + 1, K(rampa, base + 1))
    elif motivo == "rayas":
        for x in range(x0, x1, 8):
            cv.vline(x, y0, y1, K(rampa, base - 1)); cv.vline(x + 4, y0, y1, K(rampa, base + 1))


def zocalo(cv, x0, x1, y, alto=6, rampa="madera", base=2):
    cv.rect(x0, y - alto, x1, y, K(rampa, base))
    cv.hline(x0, x1, y - alto, K(rampa, base + 2)); cv.hline(x0, x1, y - 1, K(rampa, base - 1))


def tapa_muro(cv, x0, y0, x1, y1):
    cv.rect(x0, y0, x1, y1, K("gris", 3))
    cv.hline(x0, x1, y0, K("gris", 4))


def manchas(cv, x0, y0, x1, y1, color, n=120, semilla=7):
    rnd = random.Random(semilla)
    for _ in range(n):
        cv.px(rnd.randint(x0, x1 - 1), rnd.randint(y0, y1 - 1), color)


# ---------------------------------------------------------------- propaganda


_GH = [
    "........hhhh", "......hhhhhh", ".....hhhhhhh", "....hhhhhhhh", "....hhhhssss", "....hhssssss",
    "....hsssssss", "....hsbbbbbs", "....ssssssss", "....sssseess", "...Sssssssss", "...Sssssssnn",
    "....ssssssnn", "....sssmmmmm", "....ssmmmmmm", "....ssssssss", ".....sssssss", "......ssssss",
    ".......SSSSS", "........SSSS", "......cccccc", "....cccccccc", "..cccccccccc", ".ccccccccccc",
]
GRAN_HERMANO = []
for _f in _GH:
    _fila = list(_f + _f[::-1])
    for _c in range(16, 20):                     # sombra en el lado derecho de la cara
        if _fila[_c] == "s":
            _fila[_c] = "S"
    GRAN_HERMANO.append("".join(_fila))


def cara_gran_hermano(cv, x, y, pal=None):
    pal = pal or {"h": K("pelo", 0), "b": K("pelo", 0), "m": K("pelo", 0), "e": K("gris", 0),
                  "s": K("piel", 3), "S": K("piel", 2), "n": K("piel", 1), "c": K("gris", 1)}
    cv.grid(x, y, GRAN_HERMANO, pal)


def cartel_gran_hermano(cv, x, y, w=40, h=52, texto=True):
    cv.rect(x + 2, y + 2, x + w + 2, y + h + 2, K("gris", 1))
    cv.rect(x, y, x + w, y + h, K("papel", 3))
    banda = 10 if texto else 0
    cara_gran_hermano(cv, x + (w - 24) // 2, y + max(2, (h - banda - 24) // 2))
    if texto:
        cv.rect(x, y + h - banda, x + w, y + h, K("rojo", 3))
        t = "TE VIGILA" if w >= 40 else "VIGILA"
        cv.text(x + (w - cv.text_width(t)) // 2, y + h - 8, t, K("papel", 4))
    cv.frame(x, y, x + w, y + h, K("papel", 1))


def cartel_consignas(cv, x, y, w=60, h=40):
    cv.rect(x + 2, y + 2, x + w + 2, y + h + 2, K("gris", 1))
    cv.rect(x, y, x + w, y + h, K("rojo", 3))
    cv.frame(x + 2, y + 2, x + w - 2, y + h - 2, K("papel", 3))
    for i, t in enumerate(["LA GUERRA", "ES LA PAZ"] if h < 30 else ["LA GUERRA ES LA PAZ", "LA LIBERTAD ES", "LA ESCLAVITUD",
                                                                     "LA IGNORANCIA", "ES LA FUERZA"]):
        cv.text(x + (w - cv.text_width(t)) // 2, y + 5 + i * 7, t, K("papel", 4))


def telepantalla(cv, x, y, w, h, cara=True, texto=None):
    """Telepantalla de pared. Devuelve el rectángulo emisivo."""
    cv.rect(x - 4, y - 4, x + w + 4, y + h + 7, K("gris", 2))
    cv.frame(x - 4, y - 4, x + w + 4, y + h + 7, K("gris", 1))
    cv.rect(x, y, x + w, y + h, K("tele", 1))
    if cara:
        cx = x + w // 2
        s = min(w, h)
        cv.ellipse(cx - s // 4, y + 3, cx + s // 4, y + h - 3, K("tele", 3))
        cv.d.pieslice([cx - s // 4 - 1, y + 1, cx + s // 4 + 1, y + h // 2], 180, 360, fill=K("tele", 1))
        ey = y + h // 2 - 1
        cv.hline(cx - s // 6, cx - 1, ey, K("tele", 5)); cv.hline(cx + 2, cx + s // 6 + 1, ey, K("tele", 5))
        cv.hline(cx - s // 7, cx + s // 7, ey + max(3, h // 5), K("tele", 0))
    if texto:
        cv.text(x + (w - cv.text_width(texto)) // 2, y + h - 7, texto, K("tele", 6))
    cv.hline(x - 4, x + w + 4, y + h + 4, K("gris", 1))
    cv.px(x + w - 1, y + h + 5, K("rojo", 4))
    cv.add_emissive(x, y, x + w, y + h)
    return (x, y, x + w, y + h)


def lineas_barrido(cv, x0, y0, x1, y1):
    for y in range(y0, y1, 2):
        for x in range(x0, x1):
            r, g, b = cv.img.getpixel((x, y))
            cv.img.putpixel((x, y), (int(r * 0.82), int(g * 0.82), int(b * 0.82)))


# ---------------------------------------------------------------- mobiliario


def sombra(cv, x0, y0, x1, y1, rampa_suelo="madera", base=1):
    cv.rect(x0, y0, x1, y1, K(rampa_suelo, base))


def mesa_oficina(cv, x, y, w=44, d=22, maquina=True, papeles=True, telepantallita=False, semilla=0):
    rnd = random.Random(semilla)
    cv.rect(x + 3, y + d + 4, x + w + 3, y + d + 12, K("gris", 2))          # sombra
    cv.rect(x, y, x + w, y + d, K("madera", 4))                             # tablero
    cv.frame(x, y, x + w, y + d, K("madera", 2))
    cv.hline(x + 1, x + w - 1, y + 1, K("madera", 5))
    cv.rect(x, y + d, x + w, y + d + 5, K("madera", 3)); cv.hline(x, x + w, y + d + 4, K("madera", 1))
    for xx in (x + 1, x + w - 4):
        cv.rect(xx, y + d + 5, xx + 3, y + d + 11, K("madera", 2))
    if maquina:
        mx = x + 6
        cv.rect(mx, y + 4, mx + 18, y + 14, K("gris", 2)); cv.frame(mx, y + 4, mx + 18, y + 14, K("gris", 0))
        cv.rect(mx + 2, y + 1, mx + 16, y + 5, K("gris", 4))
        cv.rect(mx + 4, y - 3, mx + 14, y + 2, K("papel", 4))                # hoja
        for k in range(3):
            cv.hline(mx + 3, mx + 15, y + 8 + k * 2, K("gris", 5))
    if papeles:
        px0 = x + w - 16 + rnd.randint(-2, 2)
        cv.rect(px0, y + 5, px0 + 11, y + 15, K("papel", 3)); cv.rect(px0 + 2, y + 3, px0 + 13, y + 13, K("papel", 4))
        cv.hline(px0 + 4, px0 + 11, y + 6, K("gris", 6)); cv.hline(px0 + 4, px0 + 10, y + 8, K("gris", 6))
    if telepantallita:
        tx = x + w - 14
        cv.rect(tx, y - 10, tx + 12, y + 1, K("gris", 2)); cv.rect(tx + 1, y - 9, tx + 11, y - 1, K("tele", 3))
        cv.add_emissive(tx + 1, y - 9, tx + 11, y - 1)


def silla(cv, x, y, rampa="madera", base=3, respaldo="arriba"):
    cv.rect(x + 2, y + 12, x + 16, y + 16, K("gris", 2))
    cv.rect(x, y + 4, x + 14, y + 12, K(rampa, base + 1)); cv.frame(x, y + 4, x + 14, y + 12, K(rampa, base - 1))
    for xx in (x + 1, x + 11):
        cv.rect(xx, y + 12, xx + 2, y + 16, K(rampa, base - 1))
    if respaldo == "arriba":
        cv.rect(x, y - 4, x + 14, y + 4, K(rampa, base)); cv.hline(x, x + 14, y - 4, K(rampa, base + 2))


def papelera(cv, x, y):
    cv.rect(x + 1, y + 9, x + 10, y + 11, K("gris", 2))
    cv.rect(x, y, x + 9, y + 10, K("gris", 4)); cv.frame(x, y, x + 9, y + 10, K("gris", 2))
    cv.ellipse(x, y - 2, x + 9, y + 3, K("gris", 1), outline=K("gris", 5))
    cv.px(x + 3, y - 1, K("papel", 3)); cv.px(x + 5, y, K("papel", 3))


def puerta(cv, x, y, w=30, h=46, rampa="madera", base=2, numero=None, cristal=False):
    cv.rect(x - 3, y - 3, x + w + 3, y + h, K(rampa, base - 1))
    cv.rect(x, y, x + w, y + h, K(rampa, base + 1))
    cv.frame(x + 3, y + 4, x + w - 3, y + h // 2 - 2, K(rampa, base))
    cv.frame(x + 3, y + h // 2 + 2, x + w - 3, y + h - 3, K(rampa, base))
    if cristal:
        cv.rect(x + 4, y + 5, x + w - 4, y + h // 2 - 3, K("cielo", 5))
        for k in range(4, w - 6, 3):
            cv.px(x + k, y + 8 + k % 5, K("cielo", 6))
    cv.px(x + w - 6, y + h // 2 + 1, K("ocre", 3)); cv.px(x + w - 6, y + h // 2 + 2, K("ocre", 2))
    if numero:
        cv.rect(x + w // 2 - 6, y + 7, x + w // 2 + 7, y + 14, K("papel", 3))
        cv.text(x + w // 2 - cv.text_width(numero) // 2 + 1, y + 8, numero, K("gris", 1))


def barandilla(cv, x0, x1, y, alto=10, vertical=False):
    if vertical:
        cv.rect(x0, y, x0 + 3, x1, K("madera", 2)); cv.vline(x0, y, x1, K("madera", 4))
        for yy in range(y + 4, x1, 6):
            cv.rect(x0 - 1, yy, x0 + 4, yy + 2, K("madera", 1))
        return
    cv.rect(x0, y - alto, x1, y - alto + 3, K("madera", 3)); cv.hline(x0, x1, y - alto, K("madera", 5))
    for xx in range(x0 + 2, x1, 6):
        cv.vline(xx, y - alto + 3, y, K("gris", 3))


def farola(cv, x, y, encendida=False):
    """y = base. Devuelve la posición de la luz."""
    cv.ellipse(x - 5, y - 2, x + 7, y + 3, K("gris", 1))
    cv.rect(x - 1, y - 54, x + 2, y, K("gris", 2)); cv.vline(x - 1, y - 54, y, K("gris", 4))
    cv.rect(x - 4, y - 60, x + 5, y - 52, K("gris", 1))
    cv.rect(x - 2, y - 58, x + 3, y - 54, K("ocre", 4) if encendida else K("gris", 4))
    if encendida:
        cv.add_emissive(x - 2, y - 58, x + 3, y - 54)
    return (x, y - 56)


def escombros(cv, x0, y0, x1, y1, n=30, semilla=11, rampa="granate"):
    rnd = random.Random(semilla)
    for _ in range(n):
        w, h = rnd.randint(4, 14), rnd.randint(3, 9)
        x, y = rnd.randint(x0, x1 - w), rnd.randint(y0, y1 - h)
        b = rnd.choice([2, 3, 3, 4])
        cv.rect(x + 1, y + 1, x + w + 1, y + h + 1, K(rampa, 0))
        cv.rect(x, y, x + w, y + h, K(rampa, b)); cv.hline(x, x + w, y, K(rampa, min(5, b + 1)))
    for _ in range(n * 3):
        cv.px(rnd.randint(x0, x1), rnd.randint(y0, y1), K("gris", rnd.choice([4, 5])))
