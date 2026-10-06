"""Retrato de O'Brien para el Minimor (96x96).

Reutiliza las piezas del retrato del protagonista y añade lo suyo: corpulento, cuello de toro, cara ancha y
cansada de hombre bueno, pelo corto que empieza a encanecer, gafas de montura gruesa y el mono negro del
Partido Interior. Fondo blanco del Minimor y luz plana: aquí no hay telepantalla que dé contraluz.

  - neutral: amable y paternal; casi sonríe.
  - sonrisa: sonríe por primera vez de verdad («¿Las ve? ¿De verdad las ve?»).

Uso: python3 art/personajes/retrato_obrien.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pixel import Canvas, K  # noqa: E402
import retrato_protagonista as rp  # noqa: E402

S = rp.S
FONDO = ("gris", 10)
OJOS = ((38, 1), (58, -1))


def hombros_negros(cv):
    """Mono negro del Partido Interior sobre unos hombros enormes."""
    cv.poly([(0, 96), (0, 86), (10, 76), (28, 70), (68, 70), (86, 76), (96, 86), (96, 96)], K("gris", 1))
    cv.poly([(62, 70), (68, 70), (86, 76), (96, 86), (96, 96), (72, 96)], K("gris", 0))        # sombra derecha
    cv.poly([(0, 96), (0, 86), (10, 76), (20, 72), (12, 96)], K("gris", 2))                   # luz izquierda
    cv.d.line([(2, 85), (10, 77), (20, 73)], fill=K("gris", 3))
    # cuello del mono (solapas en V), costuras y cremallera
    cv.poly([(34, 70), (48, 88), (40, 70)], K("gris", 2))
    cv.poly([(62, 70), (48, 88), (56, 70)], K("gris", 0))
    cv.d.line([34, 70, 48, 88], fill=K("gris", 0)); cv.d.line([62, 70, 48, 88], fill=K("gris", 0))
    cv.vline(48, 88, 96, K("gris", 3))
    cv.d.line([26, 80, 24, 96], fill=K("gris", 0)); cv.d.line([70, 80, 72, 96], fill=K("gris", 0))
    cv.rect(14, 84, 22, 87, K("gris", 2))                                                     # bolsillo
    cv.hline(14, 22, 84, K("gris", 3))


def cuello_ancho(cv):
    cv.rect(35, 56, 62, 76, K("piel", 2))
    cv.rect(35, 56, 62, 64, K("piel", 1))                                         # sombra de la mandíbula
    cv.poly([(35, 70), (48, 86), (61, 70)], K("piel", 2))
    cv.vline(35, 58, 72, K("piel", 1)); cv.vline(61, 58, 72, K("piel", 0))


def cabeza_ancha(cv):
    mandibula = [(25, 40), (26, 56), (31, 66), (40, 73), (56, 73), (65, 66), (70, 56), (71, 40)]
    cv.ellipse(25, 11, 72, 60, K("piel", 3))
    cv.poly(mandibula, K("piel", 3))
    for x0 in (19, 68):                                                           # orejas grandes
        cv.ellipse(x0, 37, x0 + 10, 56, K("piel", 3), outline=K("piel", 1))
        cv.d.arc([x0 + 2, 40, x0 + 8, 53], 90 if x0 > 40 else 270, 270 if x0 > 40 else 90, fill=K("piel", 1))
    cv.poly([(61, 24), (70, 38), (69, 56), (63, 66), (55, 73), (59, 62), (64, 48), (63, 32)], K("piel", 2))
    cv.poly([(29, 48), (32, 45), (37, 47), (38, 52), (35, 55), (30, 54)], K("piel", 4))           # pómulo
    cv.rect(33, 25, 45, 29, K("piel", 4))                                                          # frente
    cv.d.line([(27, 42), (27, 52), (30, 60)], fill=K("piel", 4))
    # papada y carrillos: la cara pesada de un hombre corpulento
    cv.d.arc([38, 66, 58, 78], 20, 160, fill=K("piel", 2))
    cv.d.line([(30, 58), (33, 64)], fill=K("piel", 2)); cv.d.line([(66, 58), (63, 64)], fill=K("piel", 1))
    cv.d.line(mandibula, fill=K("piel", 1))
    cv.d.line([mandibula[-3], mandibula[-2], mandibula[-1]], fill=K("piel", 0))
    # arrugas de la frente: años de paciencia
    cv.d.arc([38, 22, 58, 30], 200, 340, fill=K("piel", 2))


def pelo_corto(cv):
    """Pelo corto, peinado hacia atrás, gris en las sienes."""
    contorno = [(25, 38), (24, 30), (26, 22), (31, 15), (38, 10), (48, 8), (58, 10), (65, 15), (70, 22),
                (72, 30), (71, 38), (68, 38), (67, 30), (64, 24), (56, 21), (48, 20), (40, 21), (32, 24),
                (29, 30), (28, 38)]
    cv.poly(contorno, K("gris", 4))
    cv.poly([(62, 13), (70, 22), (72, 30), (71, 38), (68, 38), (67, 30), (64, 24)], K("gris", 3))   # sombra
    for trazo in ([(30, 22), (36, 15), (46, 11)], [(50, 11), (58, 12), (64, 17)], [(34, 19), (42, 15), (52, 14)]):
        cv.d.line(trazo, fill=K("gris", 6))                                       # peinado hacia atrás
    cv.d.line([(28, 30), (27, 36)], fill=K("gris", 7)); cv.d.line([(69, 30), (69, 36)], fill=K("gris", 6))   # sienes
    cv.d.line([(40, 21), (48, 20), (56, 21)], fill=K("gris", 3))
    cv.rect(26, 38, 29, 46, K("gris", 6)); cv.rect(67, 38, 70, 46, K("gris", 5))   # patillas canosas
    cv.d.line(contorno[:11], fill=K("gris", 2))


def nariz_ancha(cv):
    rp.nariz(cv)
    cv.px(42, 54, K("piel", 2)); cv.px(54, 54, K("piel", 2))
    cv.hline(43, 54, 57, K("piel", 2))
    cv.px(43, 55, K("piel", 1)); cv.px(53, 55, K("piel", 1))


def surcos(cv, hondos=False):
    """Pliegues de la nariz a la boca; con la sonrisa se marcan y suben."""
    if hondos:
        cv.d.line([(41, 54), (37, 58), (37, 62)], fill=K("piel", 1))
        cv.d.line([(55, 54), (59, 58), (59, 62)], fill=K("piel", 1))
    else:
        cv.d.line([(41, 55), (39, 60)], fill=K("piel", 2)); cv.d.line([(55, 55), (57, 60)], fill=K("piel", 2))


def boca_amable(cv):
    """Boca cerrada con las comisuras apenas levantadas."""
    cv.hline(43, 54, 61, K("piel", 0))
    cv.px(42, 60, K("piel", 0)); cv.px(54, 60, K("piel", 0)); cv.px(41, 59, K("piel", 1)); cv.px(55, 59, K("piel", 1))
    cv.hline(44, 53, 60, K("piel", 2)); cv.hline(44, 53, 62, K("piel", 4))
    cv.hline(45, 52, 64, K("piel", 2))


def gafas_gruesas(cv, brillo=True):
    for cx, _ in OJOS:
        cv.d.rounded_rectangle([cx - 9, 39, cx + 8, 52], radius=4, outline=K("gris", 1))
        cv.d.rounded_rectangle([cx - 8, 40, cx + 7, 51], radius=3, outline=K("gris", 2))
        if brillo:
            cv.d.line([(cx - 6, 42), (cx - 4, 42)], fill=K("gris", 10))
            cv.px(cx + 5, 49, K("gris", 9))
    cv.hline(46, 51, 43, K("gris", 1)); cv.hline(46, 51, 44, K("gris", 2))      # puente
    cv.hline(22, 29, 43, K("gris", 1)); cv.hline(67, 74, 43, K("gris", 1))     # patillas


def patas_de_gallo(cv):
    for x0, s in ((27, -1), (69, 1)):
        cv.d.line([(x0, 46), (x0 + 2 * s, 45)], fill=K("piel", 1))
        cv.d.line([(x0, 49), (x0 + 2 * s, 50)], fill=K("piel", 1))
        cv.d.line([(x0, 47), (x0 + 3 * s, 47)], fill=K("piel", 2))


FOTOGRAMAS = {
    "neutral": dict(ojos=dict(apertura=3, mirada=(0, 0)), cejas=dict(alza=2, inclinacion=-2), boca="amable"),
    "sonrisa": dict(ojos=dict(apertura=3, mirada=(0, -1)), cejas=dict(alza=3, inclinacion=-1), boca="sonrisa",
                    mejillas=True),
}


def retrato(nombre):
    f = FOTOGRAMAS[nombre]
    cv = Canvas(S, S, bg=FONDO)
    hombros_negros(cv)
    cuello_ancho(cv)
    cabeza_ancha(cv)
    pelo_corto(cv)
    nariz_ancha(cv)
    for cx, lado in OJOS:
        rp.ojo(cv, cx, 46, lado, **f["ojos"])
        rp.ceja(cv, cx, 37, lado, color=K("gris", 5), **f["cejas"])
    if f["boca"] == "amable":
        surcos(cv)
        boca_amable(cv)
    else:
        rp.mejillas(cv, alzadas=True)
        surcos(cv, hondos=True)
        rp.boca(cv, "sonrisa")
        patas_de_gallo(cv)
        for cx, _ in OJOS:                       # los carrillos empujan los párpados de abajo
            cv.d.arc([cx - 6, 50, cx + 6, 56], 200, 340, fill=K("piel", 2))
    gafas_gruesas(cv)
    return cv.img


def exportar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    for n in FOTOGRAMAS:
        retrato(n).save(destino / f"obrien_{n}.png")
    return list(FOTOGRAMAS)


if __name__ == "__main__":
    CW, CH = 104, 112
    hoja = Canvas(len(FOTOGRAMAS) * CW + 8, CH + 4, bg=("gris", 1))
    for i, n in enumerate(FOTOGRAMAS):
        x = 4 + i * CW
        hoja.img.paste(retrato(n), (x, 4))
        hoja.text(x + (S - hoja.text_width(n.upper())) // 2, 4 + S + 4, n.upper(), K("papel", 3))
    print("ok", hoja.save(Path(__file__).parent / "retratos_obrien.png", preview_scale=3))
