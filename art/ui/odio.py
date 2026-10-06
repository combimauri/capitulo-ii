"""Imágenes de la telepantalla de los Dos Minutos de Odio (80x60) y el mapa de corcho del frente (360x200)."""
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


def exportar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    for nombre, f in (("goldstein", goldstein), ("oveja", oveja), ("soldado", soldado),
                      ("diccionario", diccionario), ("gran_hermano", gran_hermano)):
        f().save(destino / f"cf-{nombre}.png")
    mapa_frente().save(destino / "mapa-frente.png")


if __name__ == "__main__":
    from PIL import Image
    S = Path(sys.argv[1])
    hoja = Image.new("RGB", (W * 5 + 20, H))
    for i, f in enumerate((goldstein, oveja, soldado, diccionario, gran_hermano)):
        hoja.paste(f(), (i * (W + 5), 0))
    hoja.resize((hoja.width * 3, H * 3), 0).save(S / "odio.png")
    mapa_frente().resize((720, 400), 0).save(S / "mapa.png")
