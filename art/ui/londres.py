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


def exportar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    mapa().save(destino / "londres.png")
    zonas().save(destino / "londres-zonas.png")


if __name__ == "__main__":
    prueba = Image.new("RGB", (W * 2 * 2 + 12, H * 2), (20, 20, 24))
    m = mapa()
    z = Image.alpha_composite(m.convert("RGBA"), zonas())
    prueba.paste(m.resize((W * 2, H * 2), Image.NEAREST), (0, 0))
    prueba.paste(z.resize((W * 2, H * 2), Image.NEAREST), (W * 2 + 12, 0))
    prueba.save(Path(__file__).parent / "londres_prueba.png")
    print("ok")
