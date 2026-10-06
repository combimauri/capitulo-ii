"""Icono de la app: el ojo de la telepantalla sobre rojo propaganda."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from pixel import Canvas, K  # noqa: E402


def icono(tam=32):
    cv = Canvas(32, 32, bg=("rojo", 3))
    cv.rect(2, 2, 30, 30, K("rojo", 4))
    cv.ellipse(5, 10, 27, 22, K("papel", 4), outline=K("rojo", 0))
    cv.ellipse(12, 11, 21, 21, K("tele", 3))
    cv.ellipse(14, 13, 19, 19, K("gris", 0))
    cv.px(14, 13, K("papel", 4))
    cv.hline(5, 27, 9, K("rojo", 1)); cv.hline(7, 25, 23, K("rojo", 2))
    return cv.img.resize((tam, tam), 0)


if __name__ == "__main__":
    for t in (192, 512):
        icono(t).save(sys.argv[1] + f"/icono-{t}.png" if len(sys.argv) > 1 else f"icono-{t}.png")
