"""Ayudas de luz y letra compartidas por los escenarios nuevos (no es un escenario).

- glow_post: un segundo resplandor de otro color, aplicado DESPUÉS de bake_lighting
  (el Canvas solo admite un color de resplandor por pasada).
- texto_grande: la fuente 3x5 escalada (para carteles grandes).
"""
from pixel import FONT3x5


def glow_post(cv, cx, cy, radio, fuerza, rgb, squash=1.0, pasos=7, limite=None, respetar_emisivos=True):
    x0, y0, x1, y1 = limite or (0, 0, cv.w, cv.h)
    px = cv.img.load()
    for y in range(max(0, y0), min(cv.h, y1)):
        for x in range(max(0, x0), min(cv.w, x1)):
            dx, dy = x - cx, (y - cy) * squash
            d = (dx * dx + dy * dy) ** 0.5 / radio
            if d >= 1:
                continue
            if respetar_emisivos and any(a <= x < c and b <= y < e for a, b, c, e in cv.emissive):
                continue
            k = fuerza * (1 - d) ** 1.6
            k = round(k * pasos / fuerza) / pasos * fuerza
            if k <= 0:
                continue
            col = px[x, y]
            px[x, y] = tuple(int(col[c] * (1 - k) + rgb[c] * k) for c in range(3))


def texto_grande(cv, x, y, s, col, escala=2, spacing=1):
    for ch in s.upper():
        bits = FONT3x5.get(ch, FONT3x5[" "])
        for i, b in enumerate(bits):
            if b == "1":
                cv.rect(x + (i % 3) * escala, y + (i // 3) * escala, x + (i % 3 + 1) * escala, y + (i // 3 + 1) * escala, col)
        x += (3 + spacing) * escala


def ancho_grande(s, escala=2, spacing=1):
    return (len(s) * (3 + spacing) - spacing) * escala
