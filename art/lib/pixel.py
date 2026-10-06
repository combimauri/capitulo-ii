"""Librería mínima de pixel art por código para CAPÍTULO II.

- Paleta organizada en rampas de material (de oscuro a claro).
- Primitivas de dibujo sobre una cuadrícula de píxeles.
- Iluminación por pasos dentro de cada rampa (sin tramado) + resplandores tintados.
- Fuente 3x5 para rótulos de carteles y documentos.
"""
from pathlib import Path
from PIL import Image, ImageDraw

RAMPS = {
    "gris":   ["#0b0c0f", "#16181c", "#22252a", "#2f3338", "#3f444a", "#52585e",
               "#686f75", "#828a8f", "#a0a7aa", "#c1c6c6", "#e2e3dd"],
    "pared":  ["#252b28", "#2f3732", "#3a433d", "#4a544d", "#5c6760", "#707c74", "#879389"],
    "madera": ["#1a1411", "#2e221b", "#422f24", "#57402f", "#6e523b", "#87674a", "#a07e5b"],
    "azul":   ["#141c2e", "#1f2b45", "#2c3d60", "#3e5480", "#5470a0"],
    "rojo":   ["#2e0a0c", "#4f1114", "#7a1a1d", "#a4262a", "#c8382f", "#e05a45"],
    "papel":  ["#6f6a5c", "#8f8a7a", "#b5af9c", "#d8d2bd", "#eeead9"],
    "tele":   ["#071712", "#0f2a22", "#1a4335", "#2c654d", "#48906c", "#7fc496", "#b8e6c0"],
    "piel":   ["#5e3d2f", "#7e5543", "#a77b62", "#c99a7c", "#e2b896"],
    "pelo":   ["#1d1511", "#2e2119", "#463226", "#5e4532"],
    "ocre":   ["#4a3a1c", "#6b5428", "#a8863e", "#e0bf68", "#f4dc94"],
    "granate": ["#241414", "#2f1a1a", "#45231f", "#5e302a", "#774035", "#8e5545"],
    "cielo":  ["#2c3138", "#3a4049", "#4e5662", "#66707c", "#828c97", "#a3acb4", "#c6ccd1"],
    "tela":   ["#262a33", "#353b47", "#47505e", "#5c6676", "#76808e"],
}


def hex2rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


RGB = {name: [hex2rgb(h) for h in hexes] for name, hexes in RAMPS.items()}
LOOKUP = {rgb: (name, i) for name, cols in RGB.items() for i, rgb in enumerate(cols)}


def K(ramp, i):
    """Color de una rampa por índice (se recorta a los límites)."""
    cols = RGB[ramp]
    return cols[max(0, min(len(cols) - 1, i))]


FONT3x5 = {
    "A": "010101111101101", "B": "110101110101110", "C": "011100100100011", "D": "110101101101110",
    "E": "111100110100111", "F": "111100110100100", "G": "011100101101011", "H": "101101111101101",
    "I": "111010010010111", "J": "001001001101010", "K": "101101110101101", "L": "100100100100111",
    "M": "101111111101101", "N": "110101101101101", "O": "010101101101010", "P": "110101110100100",
    "Q": "010101101110011", "R": "110101110101101", "S": "011100010001110", "T": "111010010010010",
    "U": "101101101101111", "V": "101101101101010", "W": "101101111111101", "X": "101101010101101",
    "Y": "101101010010010", "Z": "111001010100111", "0": "111101101101111", "1": "010110010010111",
    "2": "110001010100111", "3": "110001010001110", "4": "101101111001001", "5": "111100110001110",
    "6": "011100110101010", "7": "111001010010010", "8": "010101010101010", "9": "010101011001110",
    ".": "000000000000010", ",": "000000000010100", "-": "000000111000000", " ": "000000000000000",
}


class Canvas:
    def __init__(self, w, h, bg=("gris", 0)):
        self.w, self.h = w, h
        self.img = Image.new("RGB", (w, h), K(*bg))
        self.d = ImageDraw.Draw(self.img)
        self.light = [[0] * w for _ in range(h)]      # pasos de luz (+/-) por píxel
        self.glow = [[0.0] * w for _ in range(h)]     # intensidad de resplandor
        self.glow_rgb = K("tele", 4)
        self.emissive = []                            # rectángulos que no reciben luz

    # --- primitivas ------------------------------------------------------
    def rect(self, x0, y0, x1, y1, col):
        if x1 > x0 and y1 > y0:
            self.d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=col)

    def frame(self, x0, y0, x1, y1, col):
        self.d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=col)

    def hline(self, x0, x1, y, col):
        self.d.line([x0, y, x1 - 1, y], fill=col)

    def vline(self, x, y0, y1, col):
        self.d.line([x, y0, x, y1 - 1], fill=col)

    def px(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.img.putpixel((x, y), col)

    def poly(self, pts, col):
        self.d.polygon(pts, fill=col)

    def ellipse(self, x0, y0, x1, y1, col, outline=None):
        self.d.ellipse([x0, y0, x1 - 1, y1 - 1], fill=col, outline=outline)

    def grid(self, x, y, rows, palette):
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                if ch in palette:
                    self.px(x + c, y + r, palette[ch])

    def text(self, x, y, s, col, spacing=1):
        for ch in s.upper():
            bits = FONT3x5.get(ch, FONT3x5[" "])
            for i, b in enumerate(bits):
                if b == "1":
                    self.px(x + i % 3, y + i // 3, col)
            x += 3 + spacing

    def text_width(self, s, spacing=1):
        return len(s) * (3 + spacing) - spacing

    # --- iluminación --------------------------------------------------------
    def add_light(self, x0, y0, x1, y1, steps):
        for y in range(max(0, y0), min(self.h, y1)):
            row = self.light[y]
            for x in range(max(0, x0), min(self.w, x1)):
                row[x] += steps

    def add_light_fn(self, fn):
        """fn(x, y) -> pasos de luz adicionales."""
        for y in range(self.h):
            row = self.light[y]
            for x in range(self.w):
                row[x] += fn(x, y)

    def add_glow(self, cx, cy, radii, strengths, squash=1.0):
        for y in range(self.h):
            for x in range(self.w):
                dx, dy = x - cx, (y - cy) * squash
                dist = (dx * dx + dy * dy) ** 0.5
                for r, s in zip(radii, strengths):
                    if dist < r:
                        self.glow[y][x] = max(self.glow[y][x], s)
                        break

    def add_glow_suave(self, cx, cy, radio, fuerza, squash=1.0, pasos=7, limite=None):
        """Resplandor con caída gradual cuantizada en `pasos` niveles (sin anillos duros)."""
        x0, y0, x1, y1 = limite or (0, 0, self.w, self.h)
        for y in range(max(0, y0), min(self.h, y1)):
            for x in range(max(0, x0), min(self.w, x1)):
                dx, dy = x - cx, (y - cy) * squash
                d = (dx * dx + dy * dy) ** 0.5 / radio
                if d < 1:
                    k = fuerza * (1 - d) ** 1.6
                    k = round(k * pasos / fuerza) / pasos * fuerza
                    if k > self.glow[y][x]:
                        self.glow[y][x] = k

    def add_emissive(self, x0, y0, x1, y1):
        self.emissive.append((x0, y0, x1, y1))

    def bake_lighting(self):
        src = self.img.copy().load()
        out = self.img.load()
        g = self.glow_rgb
        for y in range(self.h):
            for x in range(self.w):
                if any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in self.emissive):
                    continue
                col = src[x, y]
                n = self.light[y][x]
                if n and col in LOOKUP:
                    ramp, i = LOOKUP[col]
                    col = K(ramp, i + n)
                k = self.glow[y][x]
                if k:
                    col = tuple(int(col[c] * (1 - k) + g[c] * k) for c in range(3))
                out[x, y] = col

    # --- salida -----------------------------------------------------------------
    def save(self, path, preview_scale=3):
        path = Path(path)
        self.img.save(path)
        prev = path.with_name(path.stem + f"@{preview_scale}x.png")
        self.img.resize((self.w * preview_scale, self.h * preview_scale), Image.NEAREST).save(prev)
        return prev
