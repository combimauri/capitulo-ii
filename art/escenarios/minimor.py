"""J11 — Ministerio del Amor: recepción.

Todo blanco: paredes de azulejo, suelo, techo. Luz plana, sin sombras ni resplandores; solo blancos y
grises (ni rojo ni verde). Un banco largo, un mostrador con fichero, teléfono negro y máquina de escribir,
la puerta de la oficina interior, una puertecita gris de servicio y un reloj sin agujas.
"""
from pixel import Canvas, K

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 20, 92, 246
ENTRADA = (224, 256)
BANCO = (60, 150, 196, 164)
MOSTRADOR = (296, 110, 424, 140)
MAQUINA = (300, 112, 320, 124)
PUERTA_OFICINA = (380, 40, 410, 92)
PUERTA_SERVICIO = (56, 44, 80, 92)

BLANCO, BLANCO2, GRIS_JUNTA, GRIS_FILO = K("gris", 10), K("papel", 4), K("gris", 9), K("gris", 8)


def _tapa(cv, x0, y0, x1, y1):
    cv.rect(x0, y0, x1, y1, K("gris", 9)); cv.hline(x0, x1, y0, BLANCO)


def _banco(cv, x0, y0, x1, y1):
    alto = 8
    cv.rect(x0, y0 - alto, x1, y1 - alto, BLANCO); cv.frame(x0, y0 - alto, x1, y1 - alto, GRIS_FILO)
    cv.hline(x0 + 1, x1 - 1, y0 - alto + 1, BLANCO2)
    for k in range(x0 + 34, x1 - 4, 34):                                                   # juntas del asiento corrido
        cv.vline(k, y0 - alto + 1, y1 - alto - 1, GRIS_JUNTA)
    cv.rect(x0, y1 - alto, x1, y1 - 3, K("gris", 9)); cv.hline(x0, x1, y1 - 3, GRIS_FILO)
    for lx in (x0 + 3, x0 + (x1 - x0) // 2 - 1, x1 - 6):                                   # patas de acero
        cv.rect(lx, y1 - 3, lx + 3, y1, K("gris", 7))


def _mostrador(cv, x0, y0, x1, y1):
    alto = 14
    t = y0 - alto
    cv.rect(x0, t, x1, y1 - alto, BLANCO); cv.frame(x0, t, x1, y1 - alto, GRIS_FILO)
    cv.hline(x0 + 1, x1 - 1, t + 1, BLANCO2)
    cv.rect(x0, y1 - alto, x1, y1, K("gris", 9)); cv.hline(x0, x1, y1 - alto, GRIS_FILO); cv.hline(x0, x1, y1 - 1, GRIS_FILO)
    for k in range(x0 + 16, x1, 16):
        cv.vline(k, y1 - alto + 1, y1 - 1, GRIS_JUNTA)
    # máquina de escribir, exactamente en su sitio
    mx0, my0, mx1, my1 = MAQUINA
    cv.rect(mx0 + 2, my0, mx1 - 2, my0 + 4, K("gris", 6))                                  # carro
    cv.rect(mx0 + 4, my0 - 3, mx1 - 4, my0 + 1, BLANCO2)                                   # hoja en blanco
    cv.rect(mx0, my0 + 3, mx1, my1, K("gris", 4)); cv.frame(mx0, my0 + 3, mx1, my1, K("gris", 2))
    for k in range(3):
        cv.hline(mx0 + 2, mx1 - 2, my0 + 5 + k * 2, K("gris", 7))
    # fichero de cajones (tarjetas) en el centro
    fx = x0 + 40
    cv.rect(fx, t + 3, fx + 26, t + 22, K("gris", 8)); cv.frame(fx, t + 3, fx + 26, t + 22, K("gris", 6))
    for k in range(2):
        cy = t + 6 + k * 8
        cv.frame(fx + 2, cy, fx + 24, cy + 7, K("gris", 6)); cv.rect(fx + 10, cy + 2, fx + 16, cy + 4, BLANCO)
        cv.hline(fx + 11, fx + 15, cy + 5, K("gris", 5))
    for k in range(5):                                                                      # fichas sueltas
        cv.rect(fx + 30 + k, t + 6 + k, fx + 42 + k, t + 13 + k, BLANCO2 if k % 2 else BLANCO)
        cv.frame(fx + 30 + k, t + 6 + k, fx + 42 + k, t + 13 + k, GRIS_JUNTA)
    # teléfono negro: lo único oscuro de la sala
    px_ = x1 - 30
    cv.rect(px_, t + 8, px_ + 16, t + 18, K("gris", 1)); cv.frame(px_, t + 8, px_ + 16, t + 18, K("gris", 0))
    cv.ellipse(px_ + 4, t + 10, px_ + 12, t + 17, K("gris", 2), outline=K("gris", 0)); cv.px(px_ + 8, t + 13, K("gris", 6))
    cv.rect(px_ - 1, t + 4, px_ + 17, t + 8, K("gris", 1)); cv.rect(px_ - 2, t + 3, px_ + 2, t + 8, K("gris", 0))
    cv.rect(px_ + 14, t + 3, px_ + 18, t + 8, K("gris", 0)); cv.hline(px_ + 1, px_ + 15, t + 4, K("gris", 3))
    cv.d.line([(px_ + 16, t + 16), (px_ + 22, t + 20), (px_ + 20, t + 26)], fill=K("gris", 1))   # cable


def _puerta(cv, x0, y0, x1, y1, base, placa=None):
    cv.rect(x0 - 2, y0 - 2, x1 + 2, y1, K("gris", base - 1))
    cv.rect(x0, y0, x1, y1, K("gris", base))
    cv.frame(x0 + 3, y0 + 4, x1 - 3, y1 - 4, K("gris", base - 1))
    cv.rect(x1 - 7, y0 + (y1 - y0) // 2, x1 - 4, y0 + (y1 - y0) // 2 + 2, K("gris", base - 3))
    if placa:
        w = cv.text_width(placa) + 4
        cx = (x0 + x1) // 2
        cv.rect(cx - w // 2, y0 + 8, cx - w // 2 + w, y0 + 15, BLANCO); cv.frame(cx - w // 2, y0 + 8, cx - w // 2 + w, y0 + 15, K("gris", 7))
        cv.text(cx - w // 2 + 2, y0 + 9, placa, K("gris", 5))


def dibujar(variante=None):
    cv = Canvas(W, H, bg=("gris", 8))
    _tapa(cv, X0 - 12, WT - 12, X1 + 12, WT)
    # techo: fluorescentes (sin parpadeo, sin halo)
    for fx in (120, 240, 360):
        cv.rect(fx - 30, WT - 9, fx + 30, WT - 3, K("gris", 8)); cv.rect(fx - 28, WT - 8, fx + 28, WT - 4, BLANCO)
    # pared de azulejo blanco
    cv.rect(X0, WT, X1, WB, BLANCO)
    for y in range(WT, WB, 8):
        cv.hline(X0, X1, y, GRIS_JUNTA)
    for x in range(X0, X1, 8):
        cv.vline(x, WT, WB, GRIS_JUNTA)
    _puerta(cv, *PUERTA_SERVICIO, base=7)
    _puerta(cv, *PUERTA_OFICINA, base=9)
    # reloj de pared sin agujas
    cv.ellipse(214, 32, 232, 50, BLANCO2, outline=K("gris", 6))
    for (hx, hy) in [(223, 34), (230, 41), (223, 47), (216, 41)]:
        cv.px(hx, hy, K("gris", 6))
    cv.px(223, 41, K("gris", 7))
    # una placa sin texto legible: solo una línea (las normas, que nadie puede leer desde el banco)
    cv.rect(110, 40, 160, 66, BLANCO2); cv.frame(110, 40, 160, 66, K("gris", 7))
    for k in range(5):
        cv.hline(114, 156 - (k % 2) * 8, 45 + k * 4, K("gris", 8))
    cv.rect(X0, WB - 3, X1, WB, K("gris", 9))                                               # zócalo blanco
    # suelo: losas blancas, juntas finísimas
    cv.rect(X0, WB, X1, FB, BLANCO)
    for y in range(WB, FB, 24):
        cv.hline(X0, X1, y, GRIS_JUNTA)
    for x in range(X0, X1, 24):
        cv.vline(x, WB, FB, GRIS_JUNTA)
    # rejilla de desagüe en el centro del suelo
    cv.rect(234, 176, 246, 184, K("gris", 8))
    for k in range(235, 246, 2):
        cv.vline(k, 177, 183, K("gris", 6))
    _banco(cv, *BANCO)
    _mostrador(cv, *MOSTRADOR)
    # muros laterales e inferior, con la entrada
    a, b = ENTRADA
    _tapa(cv, X0 - 12, WT, X0, FB + 12); _tapa(cv, X1, WT, X1 + 12, FB + 12)
    _tapa(cv, X0 - 12, FB, a, FB + 12); _tapa(cv, b, FB, X1 + 12, FB + 12)
    cv.rect(a, FB, b, H, BLANCO)
    for y in range(FB, H, 24):
        cv.hline(a, b, y, GRIS_JUNTA)
    cv.vline(a, FB, H, K("gris", 8)); cv.vline(b - 1, FB, H, K("gris", 8))
    cv.bake_lighting()                                                                      # luz plana: nada que hornear
    return cv
