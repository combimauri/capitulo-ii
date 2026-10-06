"""Ayudas compartidas por el arte de los minijuegos (no es un minijuego).

- sprite(w, h): lienzo con un color clave de fondo que luego se vuelve transparente.
- a_rgba(cv): convierte el color clave en transparencia (después de bake_lighting, que lo respeta
  porque el color clave no pertenece a ninguna rampa).
- hoja(fotogramas): pega varios lienzos del mismo tamaño en fila (spritesheet horizontal).
- vista_previa(img, ruta, escala): ampliación para revisar a ojo.
"""
import sys
from pathlib import Path

ART = Path(__file__).resolve().parents[1]
for sub in ("lib", "escenarios"):
    p = str(ART / sub)
    if p not in sys.path:
        sys.path.insert(0, p)

from PIL import Image  # noqa: E402
from pixel import Canvas, K, FONT3x5  # noqa: E402

CLAVE = (255, 0, 255)


def sprite(w, h):
    cv = Canvas(w, h)
    cv.img.paste(CLAVE, (0, 0, w, h))
    return cv


def a_rgba(cv_o_img, clave=CLAVE):
    img = cv_o_img.img if hasattr(cv_o_img, "img") else cv_o_img
    out = img.convert("RGBA")
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            if px[x, y][:3] == clave:
                px[x, y] = (0, 0, 0, 0)
    return out


def hoja(fotogramas):
    w, h = fotogramas[0].size
    out = Image.new("RGBA", (w * len(fotogramas), h), (0, 0, 0, 0))
    for i, f in enumerate(fotogramas):
        out.paste(f, (i * w, 0))
    return out


def texto_escalado(cv, x, y, s, col, ex=2, ey=2, spacing=1):
    """Fuente 3x5 con escala horizontal y vertical independientes."""
    for ch in s.upper():
        bits = FONT3x5.get(ch, FONT3x5[" "])
        for i, b in enumerate(bits):
            if b == "1":
                cv.rect(x + (i % 3) * ex, y + (i // 3) * ey, x + (i % 3 + 1) * ex, y + (i // 3 + 1) * ey, col)
        x += (3 + spacing) * ex


def ancho_escalado(s, ex=2, spacing=1):
    return (len(s) * (3 + spacing) - spacing) * ex


def guardar(img, destino, nombre):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    img.save(destino / f"{nombre}.png")
    return nombre


def vista_previa(img, ruta, escala=3, fondo=(40, 40, 40)):
    img = img.convert("RGBA")
    base = Image.new("RGBA", img.size, fondo + (255,))
    base.alpha_composite(img)
    base.resize((img.width * escala, img.height * escala), Image.NEAREST).save(ruta)
