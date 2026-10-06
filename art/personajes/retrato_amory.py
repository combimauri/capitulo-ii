"""Retrato de Felix Amory para el crimen facial de los Dos Minutos de Odio (96x96).

Reutiliza las piezas del retrato del protagonista y añade lo suyo: pelo rubio despeinado,
cara más flaca y gafas redondas. En el clímax del Odio grita como todos, pero hay un
segundo en el que se queda callado limpiándose las gafas.

Uso: python3 art/personajes/retrato_amory.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pixel import Canvas, K  # noqa: E402
import retrato_protagonista as rp  # noqa: E402

S = rp.S
OJOS = ((38, 1), (58, -1))


def pelo_despeinado(cv):
    contorno = [(24, 44), (22, 36), (23, 26), (27, 18), (33, 12), (40, 8), (48, 6), (56, 7), (63, 10),
                (69, 15), (73, 23), (75, 33), (74, 44), (70, 44), (69, 37), (66, 30), (62, 33), (59, 26),
                (55, 33), (51, 27), (47, 34), (43, 28), (39, 33), (35, 28), (31, 35), (29, 44)]
    cv.poly(contorno, K("ocre", 2))
    # mechones que se escapan hacia arriba y a los lados
    for mechon in ([(44, 7), (47, 1), (51, 2), (50, 7)], [(53, 7), (58, 3), (57, 8)], [(30, 15), (27, 10), (34, 12)],
                   [(66, 13), (72, 11), (70, 17)], [(23, 32), (19, 30), (23, 27)], [(74, 30), (78, 31), (75, 37)]):
        cv.poly(mechon, K("ocre", 2))
    # sombra a la derecha y en las raíces
    cv.poly([(63, 12), (69, 15), (73, 23), (75, 33), (74, 44), (70, 44), (69, 36), (67, 26)], K("ocre", 1))
    cv.poly([(66, 13), (72, 11), (70, 17)], K("ocre", 1))
    cv.poly([(74, 30), (78, 31), (75, 37)], K("ocre", 1))
    # brillos
    for trazo in ([(27, 28), (30, 19), (37, 13), (45, 10)], [(32, 25), (37, 18)], [(49, 9), (57, 10), (62, 14)],
                  [(47, 3), (48, 7)]):
        cv.d.line(trazo, fill=K("ocre", 3))
    for (a, b) in [((47, 34), (48, 26)), ((55, 33), (55, 25)), ((39, 33), (41, 25)), ((62, 33), (62, 25))]:
        cv.d.line([a, b], fill=K("ocre", 1))
    cv.d.line(contorno[:12], fill=K("ocre", 0))
    cv.rect(29, 44, 30, 48, K("ocre", 1)); cv.rect(67, 44, 68, 48, K("ocre", 1))


def mejillas_hundidas(cv):
    """Amory es flaco: sombra bajo los pómulos."""
    cv.d.line([(33, 55), (35, 60), (38, 63)], fill=K("piel", 2))
    cv.d.line([(63, 55), (61, 60), (58, 63)], fill=K("piel", 1))


def gafas(cv):
    for cx, _ in OJOS:
        cv.d.ellipse([cx - 7, 40, cx + 7, 53], outline=K("gris", 3))
        cv.px(cx - 4, 42, K("cielo", 6)); cv.px(cx - 3, 42, K("cielo", 6)); cv.px(cx - 5, 43, K("cielo", 6))
    cv.hline(45, 51, 45, K("gris", 3))                                     # puente
    cv.hline(24, 31, 45, K("gris", 3)); cv.hline(65, 72, 45, K("gris", 3))   # patillas


def manos_con_gafas(cv):
    """Las manos suben hasta el pecho: un pañuelo arrugado y las gafas entre los dedos."""
    for x0, lado in ((24, 1), (60, -1)):
        cv.rect(x0, 79, x0 + 13, 92, K("piel", 3))
        cv.rect(x0 + 1, 77, x0 + 12, 78, K("piel", 3))
        for k in range(1, 4):                                               # dedos
            cv.vline(x0 + k * 3 + 1, 78, 85, K("piel", 2))
        cv.vline(x0 if lado > 0 else x0 + 13, 79, 92, K("piel", 1))
        cv.vline(x0 + 13 if lado > 0 else x0, 80, 92, K("piel", 2))
        pulgar = x0 + 12 if lado > 0 else x0 - 3
        cv.rect(pulgar, 82, pulgar + 3, 86, K("piel", 4))
    # pañuelo entre las manos
    cv.poly([(36, 79), (47, 77), (49, 90), (38, 92)], K("papel", 3))
    cv.d.line([(38, 83), (43, 84), (47, 82)], fill=K("papel", 1))
    cv.d.line([(40, 88), (46, 87)], fill=K("papel", 1))
    # gafas: una lente envuelta en el pañuelo, la otra al aire
    cv.hline(48, 50, 84, K("gris", 3))
    cv.d.ellipse([50, 78, 60, 89], outline=K("gris", 3))
    cv.px(53, 80, K("cielo", 6)); cv.px(54, 80, K("cielo", 6)); cv.px(52, 81, K("cielo", 6))
    cv.d.line([(60, 83), (63, 84)], fill=K("gris", 3))


FOTOGRAMAS = {
    "neutral": dict(ojos=dict(apertura=3), cejas=dict(alza=1, inclinacion=0), boca="cerrada", gafas=True),
    "grita":   dict(ojos=dict(apertura=2, inclinacion=2), cejas=dict(alza=-2, inclinacion=3), boca="grito",
                    gafas=True, tendones=True, arrugas="odio"),
    "grita2":  dict(ojos=dict(apertura=2, inclinacion=2), cejas=dict(alza=-2, inclinacion=3), boca="dientes",
                    gafas=True, tendones=True, arrugas="odio", aletas=True),
    "gafas":   dict(ojos=dict(apertura=2, mirada=(0, 1)), cejas=dict(alza=1, inclinacion=-1), boca="cerrada",
                    manos=True),
}


def retrato(nombre):
    f = FOTOGRAMAS[nombre]
    cv = Canvas(S, S, bg=("pared", 1))
    rp.hombros(cv)
    rp.cuello(cv, tendones=f.get("tendones", False))
    rp.cabeza(cv, femenina=True)          # mandíbula más estrecha
    pelo_despeinado(cv)
    mejillas_hundidas(cv)
    rp.nariz(cv, aletas=f.get("aletas", False))
    for cx, lado in OJOS:
        rp.ojo(cv, cx, 46, lado, **f["ojos"])
        rp.ceja(cv, cx, 37, lado, color=K("ocre", 1), **f["cejas"])
    rp.boca(cv, f["boca"])
    if f.get("arrugas"):                  # ceño fruncido (sin la vena: caería sobre el pelo)
        cv.vline(46, 37, 43, K("piel", 1)); cv.vline(50, 37, 43, K("piel", 1))
    if f.get("gafas"):
        gafas(cv)
    if f.get("manos"):
        manos_con_gafas(cv)
    rp.luz_telepantalla(cv)
    return cv.img


def exportar(destino):
    destino.mkdir(parents=True, exist_ok=True)
    for n in FOTOGRAMAS:
        retrato(n).save(destino / f"amory_{n}.png")
    return list(FOTOGRAMAS)


if __name__ == "__main__":
    CW, CH = 104, 112
    hoja = Canvas(len(FOTOGRAMAS) * CW + 8, CH + 4, bg=("gris", 1))
    for i, n in enumerate(FOTOGRAMAS):
        x = 4 + i * CW
        hoja.img.paste(retrato(n), (x, 4))
        hoja.text(x + (S - hoja.text_width(n.upper())) // 2, 4 + S + 4, n.upper(), K("papel", 3))
    print("ok", hoja.save(Path(__file__).parent / "retratos_amory.png", preview_scale=3))
