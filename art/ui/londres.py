"""Mapa de Londres del Registro de Impactos (J4) y su lámina de zonificación.

Cuadrícula de 12 x 12 casillas (A–L, 1–12) de 24 x 16 px: 288 x 192, el juego lo dibuja a 2x.
El Támesis cruza de oeste a este; el centro (ministerios) queda al noroeste del meandro.
Uso: python3 art/ui/londres.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from PIL import Image, ImageDraw  # noqa: E402
from pixel import Canvas, K  # noqa: E402

CW, CH, N = 24, 16, 12
W, H = CW * N, CH * N

# curso del río en coordenadas de casilla (columna, fila), de oeste a este
RIO = [(0, 7.0), (2, 7.4), (3.5, 8.3), (5, 8.6), (6.5, 8.3), (7.6, 9.0), (8.6, 9.1), (9.6, 8.7), (11, 8.2), (12, 8.6)]

DISTRITOS = [  # nombre, columna, fila (centro aproximado)
    ("MARYLEBONE", 3.4, 2.3), ("KENSINGTON", 1.5, 5.4), ("CHELSEA", 2.0, 7.7), ("WESTMINSTER", 4.2, 6.4),
    ("CITY", 6.6, 6.1), ("ISLINGTON", 6.4, 2.6), ("HACKNEY", 9.4, 3.2), ("STEPNEY", 9.5, 6.2),
    ("SHADWELL", 8.2, 7.3), ("LIMEHOUSE", 10.0, 8.0), ("POPLAR", 10.7, 6.7), ("SOUTHWARK", 5.5, 9.8),
    ("BERMONDSEY", 7.6, 10.4), ("LAMBETH", 3.8, 9.9), ("DEPTFORD", 9.7, 11.0),
]

# ministerios (rombos blancos de la lámina): la Verdad, el Amor, la Paz, la Abundancia
MINISTERIOS = [(4.5, 5.6), (3.5, 4.4), (5.4, 4.0), (5.9, 5.3)]


def px(c, f):
    return c * CW, f * CH


def rio(cv):
    pts = [px(c, f) for c, f in RIO]
    cv.d.line(pts, fill=K("cielo", 4), width=9)
    cv.d.line(pts, fill=K("cielo", 5), width=5)


def mapa():
    cv = Canvas(W, H, bg=("papel", 3))
    for x in range(0, W, 3):                       # textura del papel
        for y in range(0, H, 3):
            if (x * 13 + y * 7) % 17 == 0:
                cv.px(x, y, K("papel", 2))
    # manzanas y calles
    for c in range(N):
        for f in range(N):
            x, y = px(c, f)
            cv.rect(x + 3, y + 3, x + 10, y + 7, K("papel", 2)); cv.rect(x + 13, y + 9, x + 20, y + 13, K("papel", 2))
    for k in range(0, W, 12):
        cv.vline(k, 0, H, K("papel", 1)) if k % 48 == 6 else None
    # parques
    for (c, f, w, h) in [(2.6, 3.6, 1.2, 0.9), (1.0, 4.2, 0.9, 0.8), (9.0, 4.4, 1.0, 0.7)]:
        x, y = px(c, f)
        cv.rect(int(x), int(y), int(x + w * CW), int(y + h * CH), K("tele", 4))
    rio(cv)
    # cuadrícula
    for c in range(N + 1):
        cv.vline(min(c * CW, W - 1), 0, H, K("papel", 0))
    for f in range(N + 1):
        cv.hline(0, W, min(f * CH, H - 1), K("papel", 0))
    for nombre, c, f in DISTRITOS:
        x, y = px(c, f)
        cv.text(int(x - cv.text_width(nombre) / 2), int(y - 2), nombre, K("gris", 2))
    return cv.img


def zonas():
    """Lámina transparente: Partido en gris claro, proles en pardo, ministerios en rombos blancos."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    partido = [px(0, 0), px(7.5, 0), px(7.8, 3.5), px(7.2, 6.8), px(6.5, 8.3), px(3.5, 8.3), px(2, 7.4), px(0, 7.0)]
    d.polygon(partido, fill=(214, 214, 206, 120))
    prole_este = [px(7.5, 0), px(12, 0), px(12, 8.6), px(9.6, 8.7), px(8.6, 9.1), px(7.6, 9.0), px(6.5, 8.3), px(7.2, 6.8), px(7.8, 3.5)]
    prole_sur = [px(0, 7.0), px(2, 7.4), px(3.5, 8.3), px(5, 8.6), px(6.5, 8.3), px(7.6, 9.0), px(8.6, 9.1), px(9.6, 8.7), px(11, 8.2), px(12, 8.6), px(12, 12), px(0, 12)]
    for poly in (prole_este, prole_sur):
        d.polygon(poly, fill=(132, 92, 52, 120))
    d.line(partido + [partido[0]], fill=(90, 90, 86, 200), width=1)
    for c, f in MINISTERIOS:
        x, y = px(c, f)
        d.polygon([(x, y - 6), (x + 5, y), (x, y + 6), (x - 5, y)], fill=(250, 250, 244, 255), outline=(60, 60, 60, 255))
    # sello oficial en una esquina
    d.ellipse([W - 44, 4, W - 6, 30], outline=(160, 40, 40, 200), width=2)
    return img


# ---------------------------------------------------------------- los túneles de Amory (J13.02)
# El plano de las líneas de metro cerradas, dibujado a lápiz por Amory, en la misma cuadrícula que el mapa
# (se superpone exactamente sobre londres.png). Pájaros con las alas abiertas: salidas o ventilación.
# Pájaros con las alas cerradas: derrumbes. Un solo pájaro dorado: San Clemente, dentro del círculo del Miniver.
# La ruta buena son cinco tramos: Shadwell → Aldgate Este → Liverpool Street → Bank → Temple → San Clemente.
# Cada estación intermedia tiene una o dos ramas falsas que acaban en derrumbe.

ESTACIONES = [  # id, nombre, x, y (píxeles de la imagen de 288x192)
    ("shadwell", "Shadwell", 222, 120),
    ("aldgate", "Aldgate Este", 196, 96),
    ("liverpool", "Liverpool Street", 182, 72),
    ("bank", "Bank", 170, 106),
    ("temple", "Temple", 140, 118),
    ("san_clemente", "San Clemente", 120, 96),
    # finales de las ramas falsas
    ("whitechapel", "Whitechapel", 224, 82),
    ("old_street", "Old Street", 172, 50),
    ("moorgate", "Moorgate", 156, 64),
    ("monument", "Monument", 190, 108),
    ("cannon_street", "Cannon Street", 178, 128),
    ("blackfriars", "Blackfriars", 156, 124),
    ("embankment", "Embankment", 112, 124),
]
# a, b, derrumbe, desvío del trazo (punto de control relativo al punto medio; el lápiz no va recto)
TRAMOS = [
    ("shadwell", "aldgate", False, (3, -1)),
    ("aldgate", "liverpool", False, (-2, 1)),
    ("liverpool", "bank", False, (2, 1)),
    ("bank", "temple", False, (0, 2)),
    ("temple", "san_clemente", False, (4, -3)),
    ("aldgate", "whitechapel", True, (1, 2)),
    ("liverpool", "old_street", True, (-2, 0)),
    ("liverpool", "moorgate", True, (1, -2)),
    ("bank", "monument", True, (0, 2)),
    ("bank", "cannon_street", True, (-2, 0)),
    ("temple", "blackfriars", True, (0, 2)),
    ("temple", "embankment", True, (0, -2)),
]
# pozos de ventilación (pájaros con las alas abiertas sobre el plano, junto a la ruta) y pájaros del margen
VENTILACION = [(207, 110), (184, 88), (156, 105), (134, 103)]
MARGEN = [(10, 8), (19, 4), (26, 11), (264, 158), (274, 166), (256, 172)]

LAPIZ, LAPIZ_SUAVE, PAPEL = K("gris", 2), K("gris", 5), K("papel", 4)
PAJARO_ABIERTO = [".XX...XX.", "X..X.X..X", "....X...."]       # en vuelo: salida o ventilación
PAJARO_CHICO = [".X...X.", "X.X.X.X", "...X..."]                      # los del margen
PAJARO_CERRADO = [".XX....", "XeXX...", ".XXXXXX", "..XXXX.", "..X.X.."]   # posado, alas recogidas: derrumbe
PAJARO_DORADO = [".OOO.....OOO.", "OYYYO...OYYYO", "O..YOOYOOY..O", ".....OYO.....", "......O......"]


def _bezier(a, b, desvio, pasos=None):
    (x0, y0), (x1, y1) = a, b
    cx, cy = (x0 + x1) / 2 + desvio[0], (y0 + y1) / 2 + desvio[1]
    pasos = pasos or max(4, int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5))
    return [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1)
            for t in (i / pasos for i in range(pasos + 1))]


def _sprite(img, x, y, filas, colores, halo=True):
    """Dibuja un sprite de caracteres centrado en (x, y); el halo de papel lo separa de los trazos."""
    h, w = len(filas), len(filas[0])
    x0, y0 = x - w // 2, y - h // 2
    llenos = {(x0 + c, y0 + r) for r, f in enumerate(filas) for c, ch in enumerate(f) if ch != "."}
    if halo:
        for (px_, py_) in llenos:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (px_ + dx, py_ + dy)
                if q not in llenos and 0 <= q[0] < W and 0 <= q[1] < H:
                    img.putpixel(q, PAPEL + (255,))
    for r, f in enumerate(filas):
        for c, ch in enumerate(f):
            if ch in colores:
                img.putpixel((x0 + c, y0 + r), colores[ch] + (255,))


def tuneles():
    """Capa transparente de 288x192 con los túneles de Amory."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pos = {i: (x, y) for i, _, x, y in ESTACIONES}
    for k, (a, b, derrumbe, desvio) in enumerate(TRAMOS):
        pts = _bezier(pos[a], pos[b], desvio)
        if derrumbe:                                   # la rama se corta antes de llegar: el túnel acaba en escombro
            pts = pts[: int(len(pts) * 0.82)]
        # trazo de lápiz con un segundo repaso, más suave y algo desplazado
        d.line([(x + 1, y + 1) for x, y in pts[1:-1] if int(x * 7 + y * 3) % 5], fill=LAPIZ_SUAVE + (255,))
        d.line(pts, fill=LAPIZ + (255,))
        if derrumbe:
            (xa, ya), (xb, yb) = pts[-2], pts[-1]
            dx, dy = xb - xa, yb - ya
            n = (dx * dx + dy * dy) ** 0.5 or 1
            px_, py_ = -dy / n, dx / n                     # tope del derrumbe, perpendicular al túnel
            d.line([(xb + px_ * 3, yb + py_ * 3), (xb - px_ * 3, yb - py_ * 3)], fill=LAPIZ + (255,))
            for j, s_ in ((2, -1), (2, 1), (3, 0)):     # cascotes
                d.point([(round(xb + dx / n * j + px_ * s_), round(yb + dy / n * j + py_ * s_))], fill=LAPIZ + (255,))
            mx, my = pts[int(len(pts) * 0.55)]
            _sprite(img, round(mx), round(my) - 2, PAJARO_CERRADO, {"X": K("gris", 1), "e": PAPEL})
    # estaciones: circulitos a lápiz con el centro en blanco
    for i, _, x, y in ESTACIONES:
        if i == "san_clemente":
            continue
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=PAPEL + (255,), outline=LAPIZ + (255,))
    for x, y in VENTILACION:
        _sprite(img, x, y, PAJARO_ABIERTO, {"X": LAPIZ})
    for x, y in MARGEN:
        _sprite(img, x, y, PAJARO_CHICO, {"X": LAPIZ}, halo=False)
    # la entrada de Shadwell: el pájaro diminuto posado en la esquina de los tablones… con las alas abiertas
    _sprite(img, pos["shadwell"][0] + 6, pos["shadwell"][1] - 5, PAJARO_ABIERTO, {"X": LAPIZ})
    # San Clemente: el único pájaro dorado
    x, y = pos["san_clemente"]
    _sprite(img, x, y - 1, PAJARO_DORADO, {"O": K("ocre", 1), "Y": K("ocre", 3)})
    return img


def red_tuneles():
    """El grafo dibujado, en el formato de content/tuneles.json."""
    return {
        "nodos": [{"id": i, "nombre": n, "x": x, "y": y} for i, n, x, y in ESTACIONES],
        "tramos": [{"a": a, "b": b, "derrumbe": dr} for a, b, dr, _ in TRAMOS],
        "inicio": "shadwell",
        "fin": "san_clemente",
    }


def exportar_red(ruta):
    import json
    Path(ruta).write_text(json.dumps(red_tuneles(), ensure_ascii=False) + "\n", encoding="utf-8")


def exportar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    mapa().save(destino / "londres.png")
    zonas().save(destino / "londres-zonas.png")
    tuneles().save(destino / "londres-tuneles.png")


if __name__ == "__main__":
    prueba = Image.new("RGB", (W * 2 * 2 + 12, H * 2), (20, 20, 24))
    m = mapa()
    z = Image.alpha_composite(m.convert("RGBA"), zonas())
    prueba.paste(m.resize((W * 2, H * 2), Image.NEAREST), (0, 0))
    prueba.paste(z.resize((W * 2, H * 2), Image.NEAREST), (W * 2 + 12, 0))
    prueba.save(Path(__file__).parent / "londres_prueba.png")
    print("ok")
