"""Prólogo — Calle Stepney, 1979, de noche. Dos variantes: con los escombros y con Ivy al descubierto."""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
FACHADA = 96          # línea donde acaban las fachadas y empieza el adoquín


def _casas(cv):
    rnd = random.Random(1979)
    # cielo nocturno con humo
    cv.rect(0, 0, W, 40, K("cielo", 0))
    for _ in range(300):
        cv.px(rnd.randint(0, W - 1), rnd.randint(0, 38), K("cielo", 1))
    # fachadas de ladrillo, una casa por bloque de 64 px
    for i, x in enumerate(range(0, W, 64)):
        if 112 <= x < 240:
            continue                                   # la casa derrumbada
        top = 14 + (i % 3) * 3
        cv.rect(x, top, x + 64, FACHADA, K("granate", 2))
        for y in range(top + 4, FACHADA, 4):
            cv.hline(x, x + 64, y, K("granate", 1))
            for bx in range(x + (y // 4 % 2) * 4, x + 64, 8):
                cv.vline(bx, y - 3, y, K("granate", 1))
        cv.rect(x - 1, top - 4, x + 65, top, K("gris", 2))                  # cornisa
        for wx in (x + 10, x + 38):                                          # ventanas oscuras
            cv.rect(wx, top + 12, wx + 14, top + 30, K("gris", 0)); cv.frame(wx - 1, top + 11, wx + 15, top + 31, K("papel", 1))
            cv.vline(wx + 7, top + 12, top + 30, K("papel", 1))
        cv.rect(x + 24, FACHADA - 26, x + 38, FACHADA, K("madera", 1))       # puerta
        cv.px(x + 35, FACHADA - 14, K("ocre", 2))


def _derrumbe(cv):
    # casa partida: queda media pared con papel pintado de flores y una cama colgando
    cv.rect(112, 30, 240, FACHADA, K("gris", 0))
    cv.poly([(112, 18), (150, 40), (170, 30), (200, 54), (240, 24), (240, FACHADA), (112, FACHADA)], K("granate", 1))
    cv.rect(122, 46, 168, 80, K("ocre", 1))                                  # papel pintado expuesto
    for y in range(48, 80, 6):
        for x in range(124, 166, 6):
            cv.px(x, y, K("granate", 4))
    cv.rect(176, 58, 214, 64, K("madera", 2)); cv.rect(176, 64, 214, 68, K("papel", 2))   # cama colgando
    cv.d.line([(206, 64), (222, 90)], fill=K("gris", 4))
    # fuego en el interior
    rnd = random.Random(5)
    for _ in range(60):
        x, y = rnd.randint(126, 230), rnd.randint(64, 94)
        h = rnd.randint(4, 14)
        cv.rect(x, y - h, x + 3, y, K("ocre", rnd.choice([2, 3, 4])))
        cv.px(x + 1, y - h - 1, K("ocre", 4))
    cv.add_emissive(126, 50, 230, 94)


def _calle(cv):
    P.adoquines(cv, 0, FACHADA, W, H, semilla=79, rampa="gris", base=3)
    cv.rect(0, FACHADA, W, FACHADA + 6, K("gris", 4)); cv.hline(0, W, FACHADA + 6, K("gris", 1))   # acera
    # cráter
    cv.ellipse(260, 196, 360, 236, K("gris", 1)); cv.ellipse(270, 202, 350, 232, K("gris", 0))
    P.escombros(cv, 100, 100, 260, 150, n=45, semilla=3)
    P.escombros(cv, 330, 110, 460, 160, n=25, semilla=8)
    P.escombros(cv, 20, 200, 140, 250, n=18, semilla=12)
    P.farola(cv, 420, 120)
    cv.d.line([(60, 150), (92, 116)], fill=K("gris", 2), width=3)            # farola caída
    cv.rect(52, 148, 64, 154, K("gris", 1))


def _monton(cv):
    """El montón de cascotes que cubre a Ivy."""
    rnd = random.Random(21)
    cv.ellipse(176, 160, 262, 206, K("granate", 1))
    for _ in range(60):
        w, h = rnd.randint(6, 16), rnd.randint(4, 10)
        x, y = rnd.randint(178, 250 - w), rnd.randint(160, 200 - h)
        b = rnd.choice([2, 3, 4])
        cv.rect(x, y, x + w, y + h, K("granate", b)); cv.hline(x, x + w, y, K("granate", b + 1))
    cv.poly([(170, 168), (262, 186), (260, 192), (168, 174)], K("madera", 1))   # viga
    cv.d.line([(170, 168), (262, 186)], fill=K("madera", 3))


def _ivy(cv):
    """Ivy tendida bajo la viga, con los cascotes apartados (más grande y legible)."""
    rnd = random.Random(22)
    P.escombros(cv, 140, 150, 176, 214, n=16, semilla=31)
    P.escombros(cv, 270, 158, 310, 216, n=16, semilla=32)
    cv.ellipse(174, 196, 278, 210, K("gris", 1))                             # sombra
    # cabeza (a la izquierda), pelo castaño, cara de perfil hacia arriba
    cv.ellipse(176, 172, 196, 194, K("madera", 1)); cv.ellipse(178, 174, 194, 192, K("madera", 2))
    cv.ellipse(186, 176, 202, 192, K("piel", 3), outline=K("piel", 1))
    cv.px(195, 182, K("gris", 1)); cv.px(196, 182, K("gris", 1))             # ojo cerrado
    cv.hline(194, 199, 187, K("piel", 1))                                    # boca
    # cuerpo con el mono azul del Partido
    cv.rect(200, 176, 262, 196, K("azul", 2)); cv.frame(200, 176, 262, 196, K("azul", 0))
    cv.hline(201, 261, 177, K("azul", 3)); cv.vline(230, 177, 195, K("azul", 4))
    cv.rect(262, 179, 284, 193, K("azul", 1)); cv.frame(262, 179, 284, 193, K("azul", 0))   # piernas
    cv.rect(284, 179, 290, 186, K("gris", 1)); cv.rect(284, 187, 290, 193, K("gris", 1))     # botas
    # brazo extendido hacia el jugador, con el reloj en la muñeca
    cv.rect(214, 196, 226, 206, K("azul", 2)); cv.frame(214, 196, 226, 206, K("azul", 0))
    cv.rect(224, 204, 236, 210, K("piel", 3)); cv.frame(224, 204, 236, 210, K("piel", 1))
    cv.rect(224, 202, 229, 206, K("gris", 3)); cv.px(226, 203, K("papel", 4))
    for _ in range(90):                                                      # polvo
        x, y = rnd.randint(178, 288), rnd.randint(174, 208)
        if cv.img.getpixel((x, y)) in (K("azul", 2), K("azul", 1), K("madera", 2)):
            cv.px(x, y, K("papel", 1))
    cv.poly([(168, 184), (300, 172), (300, 180), (168, 192)], K("madera", 1))   # viga sobre el pecho
    cv.d.line([(168, 184), (300, 172)], fill=K("madera", 3))


def _telepantalla_rota(cv):
    cv.poly([(330, 188), (366, 182), (370, 206), (334, 212)], K("gris", 2))
    cv.poly([(334, 190), (362, 185), (365, 203), (337, 208)], K("tele", 2))
    cv.d.line([(340, 192), (356, 202)], fill=K("tele", 5)); cv.d.line([(348, 188), (344, 206)], fill=K("tele", 0))
    cv.add_emissive(334, 185, 365, 208)


def dibujar(variante="escombros"):
    cv = Canvas(W, H)
    _casas(cv)
    _derrumbe(cv)
    _calle(cv)
    _telepantalla_rota(cv)
    _monton(cv) if variante == "escombros" else _ivy(cv)
    # humo/polvo en suspensión
    rnd = random.Random(9)
    for _ in range(500):
        cv.px(rnd.randint(0, W - 1), rnd.randint(0, H - 1), K("gris", 5))
    # luz: noche fría, resplandor del fuego y de la pantalla rota
    cv.add_light(0, 0, W, H, -1)
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(178, 80, 190, 0.34, squash=1.15)
    cv.bake_lighting()
    # segundo resplandor (verde) sobre el resultado
    cv.light = [[0] * W for _ in range(H)]
    cv.glow = [[0.0] * W for _ in range(H)]
    cv.glow_rgb = K("tele", 4)
    cv.add_glow_suave(350, 198, 52, 0.32, squash=1.4)
    cv.bake_lighting()
    return cv
