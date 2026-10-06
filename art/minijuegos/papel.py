"""Minijuegos «de papel»: el soporte físico de los documentos (biblia visual §8).

Cada minijuego tiene su módulo papel_<minijuego>.py con dibujar…() y exportar(destino). Este módulo reúne las
piezas comunes (hojas con fibra y bordes irregulares, sombras sobre la mesa, membretes y sellos del Partido,
renglones, velas) y exporta todo junto:

    python3 art/minijuegos/papel.py            → public/assets/minijuegos/{ficha,parte,diario,…}-*.png

El texto de los documentos lo escribe cada escena con sus fuentes; aquí solo se hornean rótulos fijos
(membretes, cabeceras impresas) con la fuente 3x5.
"""
import random
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ART = AQUI.parent
for _p in (ART / "lib", ART / "escenarios", AQUI):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from PIL import Image  # noqa: E402
from pixel import Canvas, K, LOOKUP  # noqa: E402

W, H = 480, 270
DESTINO = ART.parent / "public" / "assets" / "minijuegos"


# ---------------------------------------------------------------- utilidades de píxel


def desplazar(cv, x0, y0, x1, y1, pasos, prob=1.0, rnd=None, solo=None):
    """Sube o baja `pasos` tonos dentro de su rampa los píxeles del rectángulo (sombras y luces inmediatas)."""
    p = cv.img.load()
    for y in range(max(0, y0), min(cv.h, y1)):
        for x in range(max(0, x0), min(cv.w, x1)):
            if prob < 1 and (rnd or random).random() > prob:
                continue
            col = p[x, y]
            if col in LOOKUP:
                rampa, i = LOOKUP[col]
                if solo and rampa not in solo:
                    continue
                p[x, y] = K(rampa, i + pasos)


def sombra(cv, x0, y0, x1, y1, dx=3, dy=3, fuerte=2):
    """Sombra de un objeto plano sobre la mesa: un tono abajo en el borde y `fuerte` tonos dentro."""
    desplazar(cv, x0 + dx, y0 + dy, x1 + dx, y1 + dy, -1)
    if fuerte > 1:
        desplazar(cv, x0 + dx + 1, y0 + dy + 1, x1 + dx - 1, y1 + dy - 1, -(fuerte - 1))


def sombra_elipse(cv, x0, y0, x1, y1, dx=2, dy=3, pasos=-2):
    """Sombra de un objeto redondo (taza, cenicero, platillo): una elipse desplazada, `pasos` tonos más oscura."""
    cx, cy = (x0 + x1 - 1) / 2 + dx, (y0 + y1 - 1) / 2 + dy
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                desplazar(cv, x, y, x + 1, y + 1, pasos)


def rgba(img, fondo=None):
    """Convierte un color de fondo en transparente (por defecto gris 0)."""
    img = img.convert("RGBA")
    f = (fondo or K("gris", 0)) + (255,)
    img.putdata([(0, 0, 0, 0) if px == f else px for px in img.getdata()])
    return img


def recorte(cv, x0, y0, x1, y1):
    return cv.img.crop((x0, y0, x1, y1))


BAYER4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def luz_radial(cv, cx, cy, tramos, squash=1.0):
    """Pasos de luz en anillos alrededor de (cx, cy) con transición tramada (Bayer 4×4), sin bordes duros.

    tramos: [(r0, r1, pasos)]: a partir de r0 se empieza a aplicar `pasos`, y desde r1 se aplica en todos los píxeles.
    """
    def fn(x, y):
        d = ((x - cx) ** 2 + ((y - cy) * squash) ** 2) ** 0.5
        n = 0
        for r0, r1, pasos in tramos:
            if pasos < 0:
                t = (d - r0) / max(1, r1 - r0)
            else:
                t = (r1 - d) / max(1, r1 - r0)
            if t >= 1 or (t > 0 and t * 16 > BAYER4[y % 4][x % 4]):
                n += pasos
        return n
    cv.add_light_fn(fn)


# ---------------------------------------------------------------- hojas


def mascara_rect(x0, y0, x1, y1, rnd, mordidas=0.06, muescas=3, esquinas=None):
    """Conjunto de píxeles de una hoja con el borde gastado: píxeles comidos en el canto y alguna muesca."""
    m = {(x, y) for y in range(y0, y1) for x in range(x0, x1)}
    w, h = x1 - x0, y1 - y0
    for x in range(x0, x1):
        for y in (y0, y1 - 1):
            if rnd.random() < mordidas:
                m.discard((x, y))
    for y in range(y0, y1):
        for x in (x0, x1 - 1):
            if rnd.random() < mordidas:
                m.discard((x, y))
    for _ in range(muescas):                                    # pequeñas roturas de 2-4 px
        lado = rnd.choice("NSEO")
        n = rnd.randint(2, 4)
        if lado in "NS":
            x = rnd.randint(x0 + 4, x1 - 6)
            y, dy = (y0, 1) if lado == "N" else (y1 - 1, -1)
            for k in range(n):
                m.discard((x + k, y))
                if 0 < k < n - 1:
                    m.discard((x + k, y + dy))
        else:
            y = rnd.randint(y0 + 4, y1 - 6)
            x, dx = (x0, 1) if lado == "O" else (x1 - 1, -1)
            for k in range(n):
                m.discard((x, y + k))
                if 0 < k < n - 1:
                    m.discard((x + dx, y + k))
    for (cx, cy) in (esquinas or [(x0, y0), (x1 - 1, y0), (x0, y1 - 1), (x1 - 1, y1 - 1)]):
        m.discard((cx, cy))                                     # esquinas romas
    return m


def pintar_hoja(cv, mascara, rampa="papel", base=3, semilla=0, fibra=0.05, borde=-1, borde_col=None,
                tono=None):
    """Rellena una máscara de papel: canto un tono más oscuro, fibra (motas de ±1) y la textura del grano.

    tono(x, y) -> desplazamiento opcional del tono base (amarilleo hacia los bordes, luz, etc.).
    """
    rnd = random.Random(semilla)
    p = cv.img.load()
    for (x, y) in mascara:
        if not (0 <= x < cv.w and 0 <= y < cv.h):
            continue
        b = base + (tono(x, y) if tono else 0)
        canto = any((x + dx, y + dy) not in mascara for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if canto:
            p[x, y] = borde_col or K(rampa, b + borde)
            continue
        r = rnd.random()
        if r < fibra * 0.8:
            t = b - 1
        elif r < fibra:
            t = b + 1
        else:
            t = b
        p[x, y] = K(rampa, t)


def hoja(cv, x0, y0, x1, y1, rampa="papel", base=3, semilla=0, mordidas=0.06, muescas=3, fibra=0.05,
         sombra_mesa=True, tono=None, borde=-1, borde_col=None, amarilleo=0):
    """Una hoja rectangular con sombra sobre la mesa. amarilleo: n px de canto un tono más viejo."""
    rnd = random.Random(semilla)
    if sombra_mesa:
        sombra(cv, x0, y0, x1, y1)
    m = mascara_rect(x0, y0, x1, y1, rnd, mordidas, muescas)
    if amarilleo:
        t0 = tono

        def tono(x, y, t0=t0):
            e = min(x - x0, x1 - 1 - x, y - y0, y1 - 1 - y)
            return (t0(x, y) if t0 else 0) - (1 if e < amarilleo and (x * 7 + y * 3) % 5 else 0)
    pintar_hoja(cv, m, rampa, base, semilla + 1, fibra, borde, borde_col, tono)
    return m


def manchas_papel(cv, x0, y0, x1, y1, n, semilla, pasos=-1, rampa="papel", radio=(2, 6)):
    """Manchas de humedad y óxido (foxing): racimos irregulares un tono más oscuros."""
    rnd = random.Random(semilla)
    p = cv.img.load()
    for _ in range(n):
        cx, cy = rnd.randint(x0, x1 - 1), rnd.randint(y0, y1 - 1)
        r = rnd.randint(*radio)
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if not (x0 <= x < x1 and y0 <= y < y1):
                    continue
                d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if d < r and rnd.random() < 0.85 - d / r * 0.6:
                    col = p[x, y]
                    if col in LOOKUP and LOOKUP[col][0] == rampa:
                        p[x, y] = K(rampa, LOOKUP[col][1] + pasos)


def pliegue(cv, x0, x1, y, rampa="papel"):
    """Pliegue horizontal: una línea de sombra y otra de luz."""
    desplazar(cv, x0, y, x1, y + 1, -1, solo=(rampa,))
    desplazar(cv, x0, y + 1, x1, y + 2, 1, solo=(rampa,))


def renglones(cv, x0, x1, ys, col, punteado=False):
    for y in ys:
        for x in range(x0, x1):
            if not punteado or x % 2 == 0:
                cv.px(x, y, col)


# ---------------------------------------------------------------- impresos del Partido


def piramide(cv, x, y, alto=12, col=None, luz=None):
    """La pirámide de los ministerios (membrete). (x, y) = esquina superior izquierda; ancho = 2*alto."""
    col = col or K("gris", 2)
    for k in range(0, alto, 2):
        a = k + 2
        cx = x + alto
        cv.rect(cx - a, y + k, cx + a, y + k + 2, col)
        if luz:
            cv.px(cx - a, y + k, luz)
    cv.rect(x + alto - 1, y - 2, x + alto + 1, y, col)        # la antena del tejado


def texto_c(cv, cx, y, s, col):
    cv.text(cx - cv.text_width(s) // 2, y, s, col)


def sello_redondo(cv, cx, cy, r, col, texto=None, semilla=0, tinta=0.82):
    """Sello de tinta: dos anillos y un rótulo, con la tinta desigual (faltan píxeles)."""
    rnd = random.Random(semilla)
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if (r - 1.2 <= d < r or r - 3.6 <= d < r - 2.6) and rnd.random() < tinta:
                cv.px(x, y, col)
    if texto:
        w = cv.text_width(texto)
        tmp = Canvas(w, 5, ("gris", 0))
        tmp.text(0, 0, texto, (255, 0, 255))
        for yy in range(5):
            for xx in range(w):
                if tmp.img.getpixel((xx, yy)) == (255, 0, 255) and rnd.random() < tinta + 0.1:
                    cv.px(cx - w // 2 + xx, cy - 2 + yy, col)


def sello_rect(cv, x0, y0, x1, y1, col, texto, semilla=0, tinta=0.8):
    rnd = random.Random(semilla)
    for x in range(x0, x1):
        for y in (y0, y1 - 1):
            if rnd.random() < tinta:
                cv.px(x, y, col)
    for y in range(y0, y1):
        for x in (x0, x1 - 1):
            if rnd.random() < tinta:
                cv.px(x, y, col)
    if not texto:
        return
    w = cv.text_width(texto)
    tmp = Canvas(w, 5, ("gris", 0))
    tmp.text(0, 0, texto, (255, 0, 255))
    tx, ty = (x0 + x1 - w) // 2, (y0 + y1 - 5) // 2
    for yy in range(5):
        for xx in range(w):
            if tmp.img.getpixel((xx, yy)) == (255, 0, 255) and rnd.random() < tinta + 0.1:
                cv.px(tx + xx, ty + yy, col)


def agujeros(cv, x, ys, fondo, canto):
    """Taladros de archivador en el margen."""
    for y in ys:
        cv.ellipse(x - 2, y - 2, x + 3, y + 3, fondo)
        cv.px(x - 1, y - 2, canto); cv.px(x, y - 2, canto); cv.px(x + 1, y - 2, canto)


# ---------------------------------------------------------------- mesas


def chapa(cv, x0, y0, x1, y1, base=4, semilla=0, rampa="gris"):
    """Tablero de acero cepillado visto desde arriba: vetas horizontales y algún arañazo."""
    rnd = random.Random(semilla)
    cv.rect(x0, y0, x1, y1, K(rampa, base))
    for y in range(y0, y1):
        if rnd.random() < 0.35:
            a = rnd.randint(x0, x1 - 10); b = min(x1, a + rnd.randint(20, 120))
            cv.hline(a, b, y, K(rampa, base + rnd.choice([-1, 1])))
    for _ in range((x1 - x0) * (y1 - y0) // 1800):                            # arañazos
        x, y = rnd.randint(x0, x1 - 12), rnd.randint(y0, y1 - 4)
        L = rnd.randint(4, 12)
        for k in range(L):
            cv.px(x + k, y + k // 5, K(rampa, base + 2))


def madera_mesa(cv, x0, y0, x1, y1, base=3, semilla=0, rampa="madera", tabla=18, vertical=False):
    """Tablero de madera de tablas largas con vetas y nudos (vista cenital)."""
    rnd = random.Random(semilla)
    cv.rect(x0, y0, x1, y1, K(rampa, base))
    if vertical:
        for x in range(x0, x1, tabla):
            cv.vline(x, y0, y1, K(rampa, base - 2)); cv.vline(x + 1, y0, y1, K(rampa, base + 1))
            for _ in range(5):
                vx = rnd.randint(x + 3, x + tabla - 3)
                a = rnd.randint(y0, y1 - 20)
                cv.vline(vx, a, a + rnd.randint(10, 50), K(rampa, base - 1))
    else:
        for y in range(y0, y1, tabla):
            cv.hline(x0, x1, y, K(rampa, base - 2)); cv.hline(x0, x1, y + 1, K(rampa, base + 1))
            for _ in range(max(3, (x1 - x0) // 40)):
                vy = rnd.randint(y + 3, y + tabla - 2)
                a = rnd.randint(x0, x1 - 20)
                cv.hline(a, a + rnd.randint(12, 70), vy, K(rampa, base - 1))
            for _ in range(rnd.randint(0, 2)):                                   # nudo
                nx, ny = rnd.randint(x0 + 6, x1 - 8), rnd.randint(y + 4, y + tabla - 4)
                cv.ellipse(nx - 2, ny - 1, nx + 3, ny + 2, K(rampa, base - 1))
                cv.px(nx, ny, K(rampa, base - 2))


def vela(cv, x, y, alto=12, ancho=4, encendida=True, cera=("papel", 4)):
    """Vela vista en 3/4: (x, y) = base. Devuelve el punto de la llama."""
    cv.ellipse(x - ancho - 2, y - 2, x + ancho + 3, y + 3, K(*cera))            # charco de cera
    cv.ellipse(x - ancho - 1, y - 1, x + ancho + 2, y + 2, K(cera[0], cera[1] - 1))
    cv.rect(x - ancho // 2, y - alto, x + ancho - ancho // 2, y, K(cera[0], cera[1] - 1))
    cv.vline(x - ancho // 2, y - alto, y, K(*cera))
    cv.px(x + ancho - ancho // 2 - 1, y - alto + 3, K(*cera))                    # gota
    cv.px(x + ancho - ancho // 2 - 1, y - alto + 4, K(*cera))
    if encendida:
        cv.vline(x, y - alto - 2, y - alto, K("gris", 1))                       # pabilo
        cv.px(x, y - alto - 3, K("ocre", 4)); cv.px(x, y - alto - 4, K("ocre", 4))
        cv.px(x - 1, y - alto - 3, K("ocre", 3)); cv.px(x + 1, y - alto - 3, K("ocre", 3))
        cv.px(x, y - alto - 5, K("ocre", 3)); cv.px(x, y - alto - 2, K("ocre", 4))
        cv.add_emissive(x - 1, y - alto - 5, x + 2, y - alto - 1)
    return (x, y - alto - 3)


# ---------------------------------------------------------------- exportación


MODULOS = ("papel_ficha", "papel_parte", "papel_diario", "papel_libro", "papel_copiar", "papel_comparar",
           "papel_declaracion", "papel_capitulo")


def exportar(destino=DESTINO):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    hechos = []
    for nombre in MODULOS:
        m = __import__(nombre)
        hechos += m.exportar(destino)
    return hechos


def previa(destino, nombres, salida, escala=2):
    """Hoja de contactos ampliada para revisar (no se exporta al juego)."""
    ims = [Image.open(Path(destino) / n) for n in nombres]
    for im, n in zip(ims, nombres):
        im.resize((im.width * escala, im.height * escala), Image.NEAREST).save(Path(salida) / n.replace(".png", f"@{escala}x.png"))


if __name__ == "__main__":
    for f in exportar(Path(sys.argv[1]) if len(sys.argv) > 1 else DESTINO):
        print("ok", f)
