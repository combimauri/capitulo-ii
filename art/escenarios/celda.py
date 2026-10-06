"""FC.02 — Ministerio del Amor: la celda.

Celda blanca sin ventanas. Una luz blanca y plana que no se apaga nunca: ni sombras ni resplandores,
solo blancos y grises. Un banco de acero corrido a lo largo de tres paredes, una telepantalla en cada
pared (apagada a la vista: pantallas casi negras que miran), un cubo en la esquina y la puerta de
acero, cerrada, en el muro de abajo. Detalle narrativo: muescas rayadas en el azulejo junto al banco
(alguien contó los días) y una mancha seca junto al cubo.
"""
from pixel import Canvas, K

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 20, 92, 246
PUERTA = (224, 256)                                    # hueco del muro inferior (cerrado)
BANCO_FONDO = (40, 92, 440, 108)                       # huellas en el suelo (colisiones)
BANCO_IZQ = (40, 92, 56, 246)
BANCO_DER = (424, 92, 440, 246)
TELE_FONDO = (220, 30, 260, 60)
CUBO = (60, 214, 76, 230)

BLANCO, BLANCO2, JUNTA, FILO = K("gris", 10), K("papel", 4), K("gris", 9), K("gris", 8)
ALTO = 8                                               # altura aparente del asiento


def _tapa(cv, x0, y0, x1, y1):
    cv.rect(x0, y0, x1, y1, K("gris", 9)); cv.hline(x0, x1, y0, BLANCO)


def _pantalla(cv, x0, y0, x1, y1):
    """Telepantalla empotrada en el azulejo: marco de acero y cristal casi negro (no emite, mira)."""
    cv.rect(x0 - 3, y0 - 3, x1 + 3, y1 + 4, K("gris", 7)); cv.frame(x0 - 3, y0 - 3, x1 + 3, y1 + 4, K("gris", 5))
    cv.hline(x0 - 2, x1 + 2, y0 - 2, K("gris", 8))
    cv.rect(x0, y0, x1, y1, K("tele", 0))
    for y in range(y0 + 1, y1, 2):
        cv.hline(x0, x1, y, K("tele", 1))
    cv.d.line([(x0 + 3, y0 + 9), (x0 + 9, y0 + 3)], fill=K("tele", 2))                # reflejo del cristal
    cv.d.line([(x0 + 3, y0 + 13), (x0 + 13, y0 + 3)], fill=K("tele", 2))
    cv.rect(x0 + 2, y0 + 2, x0 + 4, y0 + 3, K("gris", 5))
    cv.px(x1 + 1, y1 + 2, K("gris", 3))                                                 # piloto (apagado: aquí no hay rojo)
    cv.add_emissive(x0, y0, x1, y1)


def _pantalla_lateral(cv, x_muro, y0, y1, lado):
    """Telepantalla en un muro lateral, vista de canto: la caja de acero asoma del muro y el cristal,
    una franja estrecha, mira hacia el centro de la celda. lado = +1 muro izquierdo, -1 derecho."""
    fondo = 11                                                                          # cuánto sobresale
    if lado > 0:
        xa, xb = x_muro - 2, x_muro + fondo
    else:
        xa, xb = x_muro - fondo, x_muro + 2
    cv.rect(xa, y0 - 3, xb, y1 + 4, K("gris", 7)); cv.frame(xa, y0 - 3, xb, y1 + 4, K("gris", 5))
    cv.rect(xa + 1, y0 - 2, xb - 1, y0, K("gris", 8))                                   # tapa de la caja, al sol plano
    # cristal: la cara que mira a la celda
    cx0, cx1 = (xb - 5, xb - 1) if lado > 0 else (xa + 1, xa + 5)
    cv.rect(cx0, y0, cx1, y1, K("tele", 0))
    for y in range(y0 + 1, y1, 2):
        cv.hline(cx0, cx1, y, K("tele", 1))
    cv.vline(cx0 + (3 if lado > 0 else 1), y0 + 3, y0 + 11, K("tele", 2))
    cv.vline(cx0 + (2 if lado > 0 else 2), y0 + 5, y0 + 8, K("tele", 2))
    cv.vline(cx1 if lado > 0 else cx0 - 1, y0, y1, K("gris", 5))                      # bisel
    cv.add_emissive(cx0, y0, cx1, y1)
    # soporte atornillado al muro
    cv.rect(xa if lado > 0 else xb - 3, y1 + 4, (xa + 3) if lado > 0 else xb, y1 + 8, K("gris", 6))


def _banco(cv):
    """Banco de acero corrido en U. El asiento se dibuja ALTO px por encima de su huella."""
    acero, acero_luz, acero_cara, acero_filo = K("gris", 8), K("gris", 9), K("gris", 6), K("gris", 5)
    fx0, fy0, fx1, fy1 = BANCO_FONDO
    lx0, _, lx1, ly1 = BANCO_IZQ
    rx0, _, rx1, ry1 = BANCO_DER
    # caras frontales (lo que se ve del canto del asiento)
    cv.rect(lx1, fy1 - ALTO, rx0, fy1, acero_cara); cv.hline(lx1, rx0, fy1 - 1, acero_filo)
    cv.rect(lx0, ly1 - ALTO, lx1, ly1, acero_cara); cv.hline(lx0, lx1, ly1 - 1, acero_filo)
    cv.rect(rx0, ry1 - ALTO, rx1, ry1, acero_cara); cv.hline(rx0, rx1, ry1 - 1, acero_filo)
    # tapas del asiento
    cv.rect(fx0, fy0 - ALTO, fx1, fy1 - ALTO, acero)
    cv.rect(lx0, fy0 - ALTO, lx1, ly1 - ALTO, acero)
    cv.rect(rx0, fy0 - ALTO, rx1, ry1 - ALTO, acero)
    # filo interior (el borde del asiento que da a la celda)
    cv.hline(lx1, rx0, fy1 - ALTO - 1, acero_luz)
    cv.vline(lx1 - 1, fy1 - ALTO, ly1 - ALTO, acero_luz)
    cv.vline(rx0, fy1 - ALTO, ry1 - ALTO, acero_luz)
    cv.hline(lx1, rx0, fy1 - ALTO, acero_filo)
    cv.vline(lx1, fy1 - ALTO, ly1 - ALTO, acero_filo)
    cv.vline(rx0 - 1, fy1 - ALTO, ry1 - ALTO, acero_filo)
    # chapas atornilladas: juntas y remaches
    for x in range(lx1 + 40, rx0 - 10, 48):
        cv.vline(x, fy0 - ALTO, fy1 - ALTO - 1, K("gris", 7))
        for yy in (fy0 - ALTO + 2, fy1 - ALTO - 3):
            cv.px(x - 2, yy, K("gris", 6)); cv.px(x + 2, yy, K("gris", 6))
    for y in range(fy1 + 30, ly1 - 12, 44):
        for (a, b) in ((lx0, lx1), (rx0, rx1)):
            cv.hline(a, b - 1 if a == lx0 else b, y - ALTO, K("gris", 7))
            cv.px(a + 3, y - ALTO - 2, K("gris", 6)); cv.px(a + 3, y - ALTO + 2, K("gris", 6))
            cv.px(b - 4, y - ALTO - 2, K("gris", 6)); cv.px(b - 4, y - ALTO + 2, K("gris", 6))
    # ménsulas bajo el canto del banco del fondo
    for x in range(lx1 + 22, rx0 - 8, 48):
        cv.rect(x, fy1 - 3, x + 3, fy1, K("gris", 5))


def _cubo(cv):
    x0, y0, x1, y1 = CUBO
    cx = (x0 + x1) // 2
    # cuerpo cilíndrico (su altura se dibuja por encima de la huella)
    cv.ellipse(x0, y1 - 7, x1, y1 + 1, K("gris", 5))                                   # culo
    cv.rect(x0 + 1, y0 - 6, x1 - 1, y1 - 3, K("gris", 6))
    cv.vline(x0 + 1, y0 - 6, y1 - 3, K("gris", 5)); cv.vline(x1 - 2, y0 - 6, y1 - 3, K("gris", 5))
    cv.vline(x0 + 4, y0 - 4, y1 - 4, K("gris", 8))                                     # brillo del zinc
    for yy in (y0 + 1, y0 + 8):
        cv.hline(x0 + 1, x1 - 1, yy, K("gris", 5))                                     # aros
    # boca
    cv.ellipse(x0, y0 - 10, x1, y0 - 1, K("gris", 8), outline=K("gris", 5))
    cv.ellipse(x0 + 2, y0 - 8, x1 - 2, y0 - 3, K("gris", 3))
    cv.hline(x0 + 4, x1 - 4, y0 - 4, K("gris", 4))
    # asa levantada
    cv.d.arc([x0 + 1, y0 - 16, x1 - 2, y0 - 2], 200, 340, fill=K("gris", 4))
    # la mancha seca de alrededor (sin sombras: es el suelo, no la luz)
    for (mx, my) in [(x1 + 2, y1 - 1), (x1 + 4, y1 + 1), (x1 + 3, y1 + 3), (x0 - 2, y1 + 2), (cx + 6, y1 + 4),
                     (x1 + 6, y1 + 2), (cx, y1 + 3)]:
        cv.px(mx, my, K("papel", 3))


def dibujar(variante=None):
    cv = Canvas(W, H, bg=("gris", 8))
    _tapa(cv, X0 - 12, WT - 12, X1 + 12, WT)
    # la luz: un panel empotrado en el techo, enrejado, que nunca se apaga (sin halo)
    cv.rect(196, WT - 10, 284, WT - 2, K("gris", 7)); cv.rect(198, WT - 9, 282, WT - 3, BLANCO)
    for x in range(204, 280, 8):
        cv.vline(x, WT - 9, WT - 3, K("gris", 8))
    # pared del fondo: azulejo blanco
    cv.rect(X0, WT, X1, WB, BLANCO)
    for y in range(WT, WB, 8):
        cv.hline(X0, X1, y, JUNTA)
    for x in range(X0, X1, 8):
        cv.vline(x, WT, WB, JUNTA)
    _pantalla(cv, *TELE_FONDO)
    # muescas rayadas en el azulejo, a la altura de la mano de alguien sentado
    for k in range(4):
        cv.vline(366 + k * 2, 70, 76, K("gris", 7))
    cv.d.line([(365, 76), (373, 70)], fill=K("gris", 7))
    for k in range(3):
        cv.vline(378 + k * 2, 70, 76, K("gris", 7))
    cv.rect(X0, WB - 3, X1, WB, K("gris", 9))                                            # zócalo
    # suelo: losas blancas y un desagüe
    cv.rect(X0, WB, X1, FB, BLANCO)
    for y in range(WB, FB, 24):
        cv.hline(X0, X1, y, JUNTA)
    for x in range(X0, X1, 24):
        cv.vline(x, WB, FB, JUNTA)
    cv.rect(234, 176, 246, 184, K("gris", 8))
    for k in range(235, 246, 2):
        cv.vline(k, 177, 183, K("gris", 6))
    _banco(cv)
    _cubo(cv)
    # muros laterales e inferior (tapas blancas), con la puerta de acero cerrada
    a, b = PUERTA
    _tapa(cv, X0 - 12, WT, X0, FB + 12); _tapa(cv, X1, WT, X1 + 12, FB + 12)
    _tapa(cv, X0 - 12, FB, a, FB + 12); _tapa(cv, b, FB, X1 + 12, FB + 12)
    cv.rect(a - 2, FB, b + 2, H, K("gris", 7))                                           # marco
    cv.rect(a, FB + 1, b, H, K("gris", 6)); cv.hline(a, b, FB + 1, K("gris", 8))         # la hoja de acero, vista desde arriba
    cv.rect(a, FB + 4, b, FB + 6, K("gris", 5))
    for x in (a + 3, b - 4):
        for y in (FB + 3, FB + 9):
            cv.px(x, y, K("gris", 8))
    cv.rect(236, FB + 7, 244, FB + 9, K("gris", 3))                                      # la mirilla
    cv.add_light(0, 0, 0, 0, 0)
    # telepantallas de los muros laterales (encima de los bancos; vistas de canto)
    _pantalla_lateral(cv, X0, 112, 150, +1)
    _pantalla_lateral(cv, X1, 112, 150, -1)
    cv.bake_lighting()                                                                   # luz plana: nada que hornear
    return cv
