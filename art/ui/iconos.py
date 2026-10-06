"""Iconos de inventario (16x16) e ilustraciones del minijuego de los escombros."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from PIL import Image  # noqa: E402
from pixel import Canvas, K  # noqa: E402


def _rgba(cv):
    """Convierte el fondo (gris 0) en transparente."""
    img = cv.img.convert("RGBA")
    fondo = K("gris", 0) + (255,)
    datos = [(0, 0, 0, 0) if p == fondo else p for p in img.getdata()]
    img.putdata(datos)
    return img


def icono_reloj():
    cv = Canvas(16, 16)
    cv.rect(6, 1, 10, 4, K("madera", 2)); cv.rect(6, 12, 10, 15, K("madera", 2))
    cv.ellipse(2, 3, 14, 14, K("papel", 3), outline=K("gris", 2))
    cv.px(8, 8, K("gris", 0)); cv.px(8, 7, K("gris", 0)); cv.px(8, 6, K("gris", 0)); cv.px(9, 9, K("gris", 0))
    cv.d.line([4, 5, 12, 11], fill=K("cielo", 5))  # cristal roto
    return _rgba(cv)


def icono_ficha():
    cv = Canvas(16, 16)
    cv.rect(2, 2, 14, 14, K("papel", 2)); cv.frame(2, 2, 14, 14, K("papel", 0))
    cv.rect(4, 4, 8, 9, K("gris", 5)); cv.px(6, 5, K("piel", 3)); cv.rect(5, 6, 7, 8, K("azul", 2))
    for y in (5, 7, 9):
        cv.hline(9, 13, y, K("gris", 3))
    cv.ellipse(8, 9, 13, 14, None, outline=K("rojo", 3))
    return _rgba(cv)


def icono_lapiz():
    cv = Canvas(16, 16)
    cv.d.line([3, 13, 12, 4], fill=K("ocre", 2), width=2)
    cv.px(13, 3, K("gris", 1)); cv.px(12, 3, K("madera", 4))
    cv.px(3, 13, K("madera", 1)); cv.px(4, 12, K("madera", 1))
    return _rgba(cv)


def icono_foto():
    cv = Canvas(16, 16)
    cv.rect(2, 3, 14, 13, K("papel", 3)); cv.rect(3, 4, 13, 11, K("gris", 5))
    cv.px(6, 7, K("piel", 3)); cv.px(10, 7, K("piel", 3))
    cv.poly([(2, 3), (5, 3), (2, 7)], K("madera", 0))  # borde quemado
    return _rgba(cv)


def icono_diario():
    cv = Canvas(16, 16)
    cv.rect(3, 2, 13, 14, K("gris", 1)); cv.frame(3, 2, 13, 14, K("gris", 3))
    cv.vline(5, 2, 14, K("gris", 3)); cv.px(9, 7, K("papel", 3)); cv.px(10, 6, K("papel", 3))
    return _rgba(cv)


ICONOS = {"icono-reloj": icono_reloj, "icono-ficha": icono_ficha, "icono-lapiz": icono_lapiz,
          "icono-foto": icono_foto, "icono-diario": icono_diario}


def cascotes_fondo():
    """Primer plano: polvo, escombros y la mano de Ivy asomando (480x270)."""
    random.seed(79)
    cv = Canvas(480, 270, bg=("gris", 1))
    for _ in range(2600):
        x, y = random.randint(0, 479), random.randint(0, 269)
        cv.px(x, y, K("gris", random.choice([2, 2, 3])))
    # resplandor del fuego (arriba a la derecha), con caída gradual
    cv.glow_rgb = K("ocre", 2)
    cv.add_glow_suave(420, 20, 260, 0.35, squash=1.3)
    cv.bake_lighting()
    # escombros del fondo
    for _ in range(40):
        x, y = random.randint(140, 360), random.randint(150, 230)
        w, h = random.randint(16, 40), random.randint(8, 18)
        cv.rect(x, y, x + w, y + h, K("granate", random.choice([2, 3, 4])))
        cv.hline(x, x + w, y, K("granate", 5))
    # viga
    cv.poly([(110, 120), (370, 170), (366, 184), (106, 134)], K("madera", 1))
    cv.d.line([(110, 120), (370, 170)], fill=K("madera", 3))
    # la mano de Ivy (abierta, polvorienta) y la manga azul
    cv.poly([(168, 176), (226, 158), (232, 172), (172, 192)], K("azul", 1))
    cv.ellipse(222, 152, 246, 176, K("piel", 2))
    for i, (x0, y0) in enumerate([(244, 150), (246, 156), (246, 163), (244, 169)]):
        cv.rect(x0, y0, x0 + 9 - i, y0 + 4, K("piel", 3)); cv.hline(x0, x0 + 9 - i, y0, K("piel", 4))
    cv.rect(228, 147, 236, 153, K("piel", 3))  # pulgar
    # el reloj en la muñeca, parado
    cv.rect(214, 158, 222, 170, K("gris", 2)); cv.ellipse(215, 160, 221, 168, K("papel", 3))
    cv.px(218, 162, K("gris", 0)); cv.px(219, 164, K("gris", 0))
    for _ in range(140):  # polvo sobre la piel
        x, y = random.randint(214, 256), random.randint(148, 176)
        if cv.img.getpixel((x, y)) in (K("piel", 2), K("piel", 3), K("piel", 4)):
            cv.px(x, y, K("papel", 1))
    return cv.img


def cascote(i):
    random.seed(i * 13)
    cv = Canvas(52, 36)
    pts = [(4, 10), (20, 2), (46, 6), (50, 24), (34, 34), (8, 30)]
    cv.poly(pts, K("granate", 3 + i % 2))
    cv.poly([(4, 10), (20, 2), (46, 6), (40, 12), (12, 14)], K("granate", 5))
    cv.d.line(pts + [pts[0]], fill=K("granate", 1))
    for _ in range(30):
        cv.px(random.randint(10, 44), random.randint(10, 28), K("granate", 2))
    if i == 2:
        cv.rect(14, 16, 36, 22, K("papel", 2))   # trozo de yeso
    return _rgba(cv)


def exportar(iconos_dir, minijuegos_dir):
    iconos_dir, minijuegos_dir = Path(iconos_dir), Path(minijuegos_dir)
    iconos_dir.mkdir(parents=True, exist_ok=True)
    minijuegos_dir.mkdir(parents=True, exist_ok=True)
    for nombre, f in ICONOS.items():
        f().save(iconos_dir / f"{nombre}.png")
    cascotes_fondo().save(minijuegos_dir / "cascotes-fondo.png")
    for i in (1, 2, 3):
        cascote(i).save(minijuegos_dir / f"cascote-{i}.png")
