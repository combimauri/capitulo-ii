"""A3 — Planta 11 del Minipax (960x270, la cámara sigue al jugador).

Un pasillo de servicio con los neones a medio gas: el montacargas a un extremo, la escalera al otro y, en medio,
la garita del guardia con su panel de llaves y la puerta de acero del Archivo Restringido, con cerradura y combinación.
Una telepantalla gira sobre su brazo y barre el suelo con un cono verde.
"""
import random

from pixel import Canvas, K
import props as P

W, H = 960, 270
WT, WB, FB = 14, 98, 196
NEONES = ((120, 2), (300, 1), (560, 2), (660, 0), (840, 2))     # (x, estado): 2 encendido, 1 a medio gas, 0 fundido


def reja_montacargas(cv, x0, y0, x1, y1, rnd):
    cv.rect(x0 - 4, y0 - 4, x1 + 4, y1, K("gris", 3))
    cv.hline(x0 - 4, x1 + 4, y0 - 4, K("gris", 5)); cv.vline(x0 - 4, y0 - 4, y1, K("gris", 4)); cv.vline(x1 + 3, y0 - 4, y1, K("gris", 1))
    cv.rect(x0, y0, x1, y1, K("gris", 0))
    for cx in (x0 + 18, x0 + 30):
        cv.vline(cx, y0, y1, K("gris", 2))
    cv.rect(x0, y0, x1, y0 + 3, K("gris", 4)); cv.hline(x0, x1, y0 + 3, K("gris", 1))
    cv.rect(x0, y1 - 3, x1, y1, K("gris", 4))
    paso, seg = 8, 10
    for bx in range(x0 + 2, x1, paso):
        cv.vline(bx, y0 + 3, y1 - 3, K("gris", 6)); cv.vline(bx + 1, y0 + 3, y1 - 3, K("gris", 3))
    for bx in range(x0 + 2, x1 - paso + 1, paso):
        for sy in range(y0 + 4, y1 - 4, seg):
            cv.d.line([(bx + 1, sy), (bx + paso, min(y1 - 4, sy + seg))], fill=K("gris", 5))
            cv.d.line([(bx + paso, sy), (bx + 1, min(y1 - 4, sy + seg))], fill=K("gris", 4))
    cv.rect(x1 - 5, y0 + 26, x1 - 2, y0 + 36, K("ocre", 2)); cv.px(x1 - 4, y0 + 28, K("ocre", 4))
    # indicador de planta: media esfera con aguja
    cx = (x0 + x1) // 2
    cv.rect(cx - 12, y0 - 14, cx + 13, y0 - 5, K("gris", 2)); cv.frame(cx - 12, y0 - 14, cx + 13, y0 - 5, K("gris", 1))
    cv.d.pieslice([cx - 9, y0 - 13, cx + 10, y0 + 4], 180, 360, fill=K("papel", 2))
    for k, (dx, dy) in enumerate(((-7, -6), (-4, -10), (0, -11), (4, -10), (7, -6))):
        cv.px(cx + dx, y0 + dy, K("gris", 2))
    cv.d.line([(cx, y0 - 6), (cx - 5, y0 - 10)], fill=K("rojo", 3))
    # un botón de llamada
    cv.rect(x1 + 6, y0 + 24, x1 + 12, y0 + 34, K("gris", 2)); cv.px(x1 + 8, y0 + 27, K("ocre", 3)); cv.px(x1 + 8, y0 + 31, K("gris", 5))


def extintor(cv, x0, y0, x1, y1):
    cv.rect(x0 - 2, y0 + 6, x1 + 2, y0 + 9, K("gris", 2))                                # abrazadera
    cv.rect(x0 + 2, y0 + 2, x1 + 2, y1 + 2, K("pared", 0))                                 # sombra en la pared
    cv.rect(x0, y0 + 4, x1, y1, K("rojo", 3)); cv.frame(x0, y0 + 4, x1, y1, K("rojo", 1))
    cv.vline(x0 + 2, y0 + 6, y1 - 2, K("rojo", 5)); cv.vline(x0 + 3, y0 + 6, y1 - 2, K("rojo", 4))
    cv.rect(x0 + 3, y0, x1 - 3, y0 + 4, K("gris", 4)); cv.hline(x0 + 3, x1 - 3, y0, K("gris", 6))   # válvula
    cv.d.line([(x1 - 3, y0 + 1), (x1 + 2, y0 + 3), (x1 + 2, y0 + 20)], fill=K("gris", 1))          # manguera
    cv.rect(x0 + 2, y0 + 12, x1 - 2, y0 + 18, K("papel", 3)); cv.hline(x0 + 3, x1 - 3, y0 + 14, K("gris", 3))
    cv.hline(x0 + 3, x1 - 4, y0 + 16, K("gris", 3))
    cv.rect(x0 - 4, y0 - 12, x1 + 4, y0 - 5, K("rojo", 2)); cv.text(x0 - 3, y0 - 11, "FUEGO", K("papel", 4), spacing=0)


def columna(cv, x0, x1, y1):
    cv.rect(x1, WB + 2, x1 + 5, y1 + 3, K("tela", 0))                                       # sombra en el suelo
    cv.rect(x0, 0, x1, y1, K("pared", 3))
    cv.vline(x0, 0, y1, K("pared", 1)); cv.vline(x0 + 1, 0, y1, K("pared", 5)); cv.vline(x0 + 2, 0, y1, K("pared", 4))
    cv.vline(x1 - 2, 0, y1, K("pared", 2)); cv.vline(x1 - 1, 0, y1, K("pared", 1))
    cv.rect(x0 - 2, WT - 4, x1 + 2, WT + 2, K("pared", 4)); cv.hline(x0 - 2, x1 + 2, WT + 2, K("pared", 1))   # capitel
    cv.rect(x0 - 1, y1 - 7, x1 + 1, y1, K("gris", 3)); cv.hline(x0 - 1, x1 + 1, y1 - 7, K("gris", 5))       # rodapié
    for y in range(30, y1 - 10, 23):                                                         # grietas del yeso
        cv.px(x0 + 8 + y % 7, y, K("pared", 2)); cv.px(x0 + 9 + y % 7, y + 1, K("pared", 2))
    cv.rect(x0 + 6, 54, x1 - 6, 66, K("papel", 2)); cv.text(x0 + 7, 56, "P11", K("gris", 1))    # número de planta


def telepantalla_giratoria(cv, x0, y0, x1, y1):
    # brazo: placa en la pared, codo y eje
    cv.rect(x0 + 10, y1 + 8, x0 + 20, y1 + 16, K("gris", 2)); cv.frame(x0 + 10, y1 + 8, x0 + 20, y1 + 16, K("gris", 1))
    cv.rect(x0 + 14, y1, x0 + 17, y1 + 9, K("gris", 4)); cv.vline(x0 + 14, y1, y1 + 9, K("gris", 6))
    cv.rect(x0 + 12, y1 - 1, x0 + 19, y1 + 2, K("gris", 3))
    # carcasa girada: se le ve un costado
    cv.rect(x0 + 2, y0 + 2, x1 + 2, y1 + 2, K("pared", 0))
    cv.poly([(x0, y0 + 2), (x0 + 5, y0), (x0 + 5, y1), (x0, y1 - 2)], K("gris", 1))
    cv.rect(x0 + 5, y0, x1, y1, K("gris", 2)); cv.frame(x0 + 5, y0, x1, y1, K("gris", 1))
    cv.hline(x0 + 5, x1, y0, K("gris", 4))
    sx0, sy0, sx1, sy1 = x0 + 8, y0 + 3, x1 - 3, y1 - 4
    cv.rect(sx0, sy0, sx1, sy1, K("tele", 2))
    cx, cy = (sx0 + sx1) // 2 + 1, (sy0 + sy1) // 2
    cv.ellipse(cx - 6, cy - 4, cx + 7, cy + 5, K("tele", 4))                                 # el ojo
    cv.ellipse(cx - 2, cy - 2, cx + 3, cy + 3, K("tele", 1)); cv.px(cx, cy - 1, K("tele", 6))
    cv.px(x1 - 3, y1 - 2, K("rojo", 4))
    cv.add_emissive(sx0, sy0, sx1, sy1)


def carrito_correo(cv, x0, y0, x1, y1, rnd):
    cv.rect(x0 + 3, y1 - 2, x1 + 4, y1 + 2, K("tela", 0))                                    # sombra
    for wx in (x0 + 2, x1 - 6):                                                              # ruedas
        cv.rect(wx, y1 - 4, wx + 5, y1, K("gris", 1)); cv.hline(wx + 1, wx + 4, y1 - 4, K("gris", 4))
    cv.rect(x0, y1 - 12, x1, y1 - 4, K("gris", 3)); cv.frame(x0, y1 - 12, x1, y1 - 4, K("gris", 1))   # caja
    cv.hline(x0, x1, y1 - 12, K("gris", 6))
    cv.rect(x0 + 2, y1 - 22, x1 - 2, y1 - 12, K("gris", 2))                                   # interior del cajón
    for vx in (x0, x1 - 1):
        cv.vline(vx, y1 - 22, y1 - 4, K("gris", 5))
    cv.hline(x0, x1, y1 - 22, K("gris", 6))
    cv.d.line([(x1 - 1, y1 - 22), (x1 + 5, y1 - 30)], fill=K("gris", 5)); cv.hline(x1 + 3, x1 + 8, y1 - 30, K("madera", 3))  # asa
    # sacas de lona, rebosando
    for (sx, sy, sw, sh, c) in ((x0 - 1, y1 - 30, 18, 16, 1), (x0 + 22, y1 - 31, 18, 17, 1), (x0 + 10, y1 - 36, 19, 18, 2)):
        cv.ellipse(sx, sy + 3, sx + sw, sy + sh, K("papel", c), outline=K("papel", 0))
        cv.ellipse(sx + 2, sy + 4, sx + sw - 6, sy + sh - 5, K("papel", c + 1))
        cv.rect(sx + sw - 7, sy, sx + sw - 3, sy + 5, K("papel", c)); cv.hline(sx + sw - 7, sx + sw - 3, sy + 4, K("rojo", 2))
        cv.d.line([(sx + 4, sy + sh - 4), (sx + sw - 5, sy + sh - 6)], fill=K("papel", 0))
        cv.rect(sx + 3, sy + 7, sx + 7, sy + 10, K("papel", 4))                                 # etiqueta
    cv.rect(x0 + 4, y1 - 11, x0 + 18, y1 - 6, K("papel", 3)); cv.text(x0 + 5, y1 - 11, "MP", K("rojo", 3))
    for k in range(3):                                                                        # cartas sueltas
        cv.rect(x0 + 20 + k * 5, y1 - 15 + k, x0 + 24 + k * 5, y1 - 12 + k, K("papel", 4))


def garita(cv, x0, x1, y1, rnd):
    top = 36
    cv.rect(x1, top + 6, x1 + 5, y1 + 3, K("tela", 0))                                       # sombra
    cv.rect(x0, top, x1, top + 8, K("madera", 4)); cv.hline(x0, x1, top, K("madera", 5))        # tejadillo (cara de arriba)
    cv.hline(x0, x1, top + 7, K("madera", 1))
    cv.rect(x0, top + 8, x1, y1, K("madera", 2))                                              # cara frontal
    cv.vline(x0, top + 8, y1, K("madera", 1)); cv.vline(x1 - 1, top + 8, y1, K("madera", 0))
    for k in range(x0 + 6, x1, 10):                                                          # tablas
        cv.vline(k, 82, y1, K("madera", 1))
    cv.rect(x0, 80, x1, 84, K("madera", 3)); cv.hline(x0, x1, 80, K("madera", 4))
    cv.rect(x0, y1 - 4, x1, y1, K("madera", 1))
    # ventanilla con cristal y trampilla
    wx0, wy0, wx1, wy1 = 752, 48, 786, 80
    cv.rect(wx0 - 2, wy0 - 2, wx1 + 2, wy1 + 2, K("madera", 1))
    cv.rect(wx0, wy0, wx1, wy1, K("gris", 1))
    cv.rect(wx0 + 2, wy0 + 14, wx1 - 2, wy1, K("gris", 2))                                    # mesa del guardia
    cv.rect(wx0 + 4, wy0 + 8, wx0 + 12, wy0 + 15, K("tela", 1)); cv.hline(wx0 + 4, wx0 + 12, wy0 + 8, K("tela", 2))  # respaldo de silla
    cv.rect(wx0 + 20, wy0 + 10, wx0 + 30, wy0 + 15, K("papel", 2))                           # registro abierto
    cv.vline(wx0 + 25, wy0 + 10, wy0 + 15, K("papel", 0))
    cv.rect(wx0 + 14, wy0 + 6, wx0 + 18, wy0 + 15, K("gris", 3)); cv.px(wx0 + 15, wy0 + 6, K("gris", 6))   # termo
    for k in range(wx0 + 3, wx1 - 1, 7):                                                      # reflejos del cristal
        cv.d.line([(k, wy0 + 1), (k - 3, wy0 + 6)], fill=K("cielo", 4))
    cv.vline((wx0 + wx1) // 2, wy0, wy0 + 12, K("madera", 1))
    cv.rect(wx0 + 6, wy1 - 6, wx1 - 6, wy1, K("gris", 0))                                    # el hueco de la ventanilla
    cv.rect(wx0 - 4, wy1 + 2, wx1 + 4, wy1 + 6, K("madera", 4)); cv.hline(wx0 - 4, wx1 + 4, wy1 + 2, K("madera", 5))  # repisa
    cv.hline(wx0 - 4, wx1 + 4, wy1 + 6, K("madera", 0))
    cv.rect(wx0 + 2, wy1 - 1, wx0 + 10, wy1 + 2, K("papel", 3))                               # un formulario
    # panel de llaves: 12 ganchos con etiquetas
    px0, py0, px1, py1 = 706, 46, 746, 74
    cv.rect(px0 + 2, py0 + 2, px1 + 2, py1 + 2, K("madera", 0))
    cv.rect(px0, py0, px1, py1, K("madera", 4)); cv.frame(px0, py0, px1, py1, K("madera", 1))
    cv.hline(px0 + 1, px1 - 1, py0 + 1, K("madera", 5))
    cv.text(px0 + 4, py0 + 2, "LLAVES", K("madera", 1))
    for fila in range(2):
        for col in range(6):
            gx, gy = px0 + 5 + col * 6, py0 + 10 + fila * 9
            cv.px(gx, gy, K("gris", 6)); cv.px(gx, gy + 1, K("gris", 3))
            if (fila, col) == (1, 4):                                                        # falta una llave
                cv.px(gx, gy + 3, K("madera", 3)); continue
            cv.vline(gx, gy + 2, gy + 5, K("ocre", 3)); cv.px(gx + 1, gy + 4, K("ocre", 2))
            cv.rect(gx - 1, gy + 5, gx + 2, gy + 8, K("papel", 4 if (fila + col) % 2 else 3))


def puerta_acero(cv, x0, y0, x1, y1):
    cv.rect(x0 - 4, y0 - 4, x1 + 4, y1, K("gris", 2))                                         # marco
    cv.hline(x0 - 4, x1 + 4, y0 - 4, K("gris", 5)); cv.vline(x0 - 4, y0 - 4, y1, K("gris", 4))
    cv.rect(x0, y0, x1, y1, K("gris", 4))
    cv.vline(x0, y0, y1, K("gris", 6)); cv.vline(x1 - 1, y0, y1, K("gris", 2)); cv.hline(x0, x1, y0, K("gris", 6))
    for by in (y0 + 6, (y0 + y1) // 2, y1 - 8):                                               # refuerzos remachados
        cv.rect(x0 + 2, by, x1 - 2, by + 4, K("gris", 5)); cv.hline(x0 + 2, x1 - 2, by + 4, K("gris", 2))
        for rx in range(x0 + 4, x1 - 3, 6):
            cv.px(rx, by + 2, K("gris", 7))
    cv.rect(x0 + 10, y0 + 14, x1 - 10, y0 + 20, K("gris", 1)); cv.hline(x0 + 10, x1 - 10, y0 + 15, K("gris", 0))   # mirilla cerrada
    # cerradura
    kx, ky = 846, 62
    cv.rect(kx - 3, ky - 4, kx + 4, ky + 6, K("ocre", 2)); cv.frame(kx - 3, ky - 4, kx + 4, ky + 6, K("ocre", 1))
    cv.px(kx, ky - 1, K("gris", 0)); cv.px(kx, ky, K("gris", 0)); cv.px(kx, ky + 1, K("gris", 0)); cv.px(kx - 1, ky - 1, K("gris", 0)); cv.px(kx + 1, ky - 1, K("gris", 0))
    cv.rect(x1 - 12, ky + 8, x1 - 4, ky + 11, K("gris", 6)); cv.hline(x1 - 12, x1 - 4, ky + 10, K("gris", 2))   # tirador
    # cerrojo de combinación: caja con cuatro ruedas numeradas
    cx0, cy0, cx1, cy1 = 854, 56, 866, 72
    cv.rect(cx0 + 1, cy0 + 1, cx1 + 1, cy1 + 1, K("gris", 0))
    cv.rect(cx0, cy0, cx1, cy1, K("gris", 3)); cv.frame(cx0, cy0, cx1, cy1, K("gris", 1)); cv.hline(cx0, cx1, cy0, K("gris", 5))
    for i in range(4):
        ry = cy0 + 2 + i * 3
        cv.rect(cx0 + 3, ry, cx1 - 3, ry + 2, K("papel", 3)); cv.px(cx0 + 5, ry, K("gris", 2)); cv.px(cx0 + 7, ry + 1, K("gris", 2))
        cv.px(cx0 + 2, ry + 1, K("gris", 6)); cv.px(cx1 - 3, ry + 1, K("gris", 6))
    cv.d.line([(cx0 - 2, cy0 + 4), (cx0, cy0 + 4)], fill=K("gris", 6))                      # pestillo que entra en la puerta
    # placa
    cv.rect(800, 20, 868, 34, K("gris", 1))
    cv.rect(801, 21, 867, 33, K("ocre", 2)); cv.hline(801, 867, 21, K("ocre", 3)); cv.hline(801, 867, 32, K("ocre", 1))
    for t, y in (("ARCHIVO", 22), ("RESTRINGIDO", 28)):
        cv.text(834 - cv.text_width(t) // 2, y, t, K("ocre", 0))
    cv.px(802, 23, K("ocre", 4)); cv.px(865, 23, K("ocre", 4))


def atril(cv, x0, y0, x1, y1):
    cv.rect(x0 + 3, y1 - 3, x1 + 4, y1 + 1, K("tela", 0))                                   # sombra
    cv.rect(x0 + 2, y1 - 3, x1 - 2, y1, K("madera", 1))                                       # pie
    cv.rect(x0 + 6, 90, x1 - 6, y1 - 3, K("madera", 2)); cv.vline(x0 + 6, 90, y1 - 3, K("madera", 4))
    cv.poly([(x0 - 2, 90), (x1 + 2, 90), (x1, 82), (x0, 82)], K("madera", 3))                # tablero inclinado
    cv.hline(x0 - 2, x1 + 2, 90, K("madera", 1))
    cv.poly([(x0, 88), (x0 + 8, 89), (x0 + 8, 82), (x0 + 1, 82)], K("papel", 4))               # libro abierto
    cv.poly([(x0 + 8, 89), (x1, 88), (x1 - 1, 82), (x0 + 8, 82)], K("papel", 3))
    cv.vline(x0 + 8, 82, 90, K("papel", 1))
    for k in range(3):
        cv.hline(x0 + 2, x0 + 7, 84 + k * 2, K("gris", 5)); cv.hline(x0 + 10, x1 - 2, 84 + k * 2, K("gris", 5))
    cv.d.line([(x1 + 1, 86), (x1 + 4, 80)], fill=K("gris", 1))                                # pluma y cadenita
    cv.px(x1 + 2, 88, K("gris", 4)); cv.px(x1 + 1, 89, K("gris", 4))


def puerta_escalera(cv, x0, y0, x1, y1):
    cv.rect(x0 - 3, y0 - 3, x1 + 3, y1, K("madera", 1))
    cv.rect(x0, y0, x1, y1, K("gris", 0))
    for k in range(6):                                                                        # primeros peldaños
        yy = y1 - 8 - k * 10
        cv.rect(x0 + 2, yy, x1 - 2, yy + 2, K("gris", 2 + (k % 2))); cv.hline(x0 + 2, x1 - 2, yy, K("gris", 4))
    cv.vline(x0 + 4, y0 + 6, y1, K("gris", 3)); cv.rect(x0 + 2, y0 + 6, x0 + 7, y0 + 8, K("gris", 4))    # pasamanos
    cv.poly([(x1 - 2, y0), (x1 + 6, y0 + 4), (x1 + 6, y1 + 2), (x1 - 2, y1)], K("madera", 3))   # la hoja, entornada
    cv.vline(x1 + 5, y0 + 4, y1 + 2, K("madera", 1)); cv.px(x1 + 2, (y0 + y1) // 2, K("ocre", 3))
    cv.rect(x0 - 2, y0 - 10, x1 + 2, y0 - 4, K("papel", 3))
    cv.text((x0 + x1) // 2 - cv.text_width("ESCALERA") // 2, y0 - 10 + 1, "ESCALERA", K("gris", 1))


def dibujar(variante=None):
    rnd = random.Random(1111)
    cv = Canvas(W, H)
    P.tapa_muro(cv, 0, 2, W, WT)
    P.papel_pintado(cv, 0, WT, W, WB, rampa="pared", base=2, motivo="rayas")
    cv.rect(0, WT, W, WT + 4, K("pared", 1))                                                   # friso
    for i, ty in enumerate((WT + 6, WT + 10)):                                                 # tubos neumáticos
        cv.hline(0, W, ty, K("gris", 5 - i)); cv.hline(0, W, ty + 1, K("gris", 2))
    P.zocalo(cv, 0, W, WB, rampa="gris", base=3)
    for _ in range(18):                                                                        # humedad
        x, y = rnd.randint(0, W - 20), rnd.randint(WT + 14, WB - 20)
        for k in range(rnd.randint(4, 14)):
            cv.px(x + rnd.randint(0, 6), y + k, K("pared", 1))
    # neones: unos encienden, otros parpadean, uno está fundido
    for nx, est in NEONES:
        cv.rect(nx - 24, 2, nx + 24, 8, K("gris", 2)); cv.rect(nx - 22, 4, nx + 22, 6, K("papel", (1, 2, 4)[est]))
        cv.hline(nx - 22, nx + 22, 7, K("cielo", (2, 4, 6)[est]))
        if est == 1:                                                                           # media barra apagada
            cv.rect(nx + 4, 4, nx + 22, 6, K("papel", 0))
        if est:
            cv.add_emissive(nx - 22, 4, nx + 22, 8)
    # suelo de linóleo, gastado por el centro
    P.baldosas(cv, 0, WB, W, FB, K("tela", 2), K("tela", 1), t=16, linea=K("tela", 0))
    for x in range(0, W, 3):
        for y in range(136, 162, 5):
            if (x * 7 + y * 3) % 11 == 0:
                cv.px(x, y, K("tela", 3))
    # elementos de la pared
    reja_montacargas(cv, 24, 34, 72, 96, rnd)
    cv.rect(110, 40, 160, 76, K("papel", 2)); cv.frame(110, 40, 160, 76, K("papel", 0))         # tablón de avisos
    for k, t in enumerate(("TURNOS", "PLANTA 11")):
        cv.text(113, 43 + k * 7, t, K("gris", 2))
    for k in range(4):
        cv.hline(113, 156 - (k * 7) % 16, 59 + k * 4, K("gris", 6))
    cv.rect(146, 64, 156, 74, K("rojo", 3)); cv.px(150, 66, K("papel", 4))
    P.puerta(cv, 300, 50, w=28, h=46, rampa="gris", base=3)                                     # puerta de un cuarto cerrado
    cv.rect(296, 38, 332, 45, K("papel", 3)); cv.text(314 - cv.text_width("11-C") // 2, 39, "11-C", K("gris", 1))
    extintor(cv, 236, 60, 248, 90)
    P.cartel_gran_hermano(cv, 360, 30, w=36, h=46)
    columna(cv, 420, 448, 130)
    telepantalla_giratoria(cv, 470, 24, 500, 44)
    P.puerta(cv, 560, 50, w=28, h=46, rampa="madera", base=1, cristal=True)
    cv.rect(554, 38, 594, 45, K("papel", 3)); cv.text(574 - cv.text_width("CORREO") // 2, 39, "CORREO", K("gris", 1))
    garita(cv, 700, 790, 128, rnd)
    P.telepantalla(cv, 748, 26, 22, 7, cara=False)
    cv.rect(752, 28, 766, 32, K("tele", 3)); cv.px(758, 29, K("tele", 6)); cv.px(759, 29, K("tele", 6))
    puerta_acero(cv, 812, 34, 852, 96)
    atril(cv, 880, 100, 896, 114)
    puerta_escalera(cv, 900, 30, 944, 96)
    # marca roja pintada en el suelo, delante del extintor
    cv.frame(234, 99, 250, 108, K("rojo", 2))
    for k in range(236, 248, 4):
        cv.d.line([(k, 107), (k + 3, 100)], fill=K("rojo", 1))
    carrito_correo(cv, 588, 150, 628, 168, rnd)
    # muro inferior
    cv.rect(0, FB, W, FB + 12, K("gris", 3)); cv.hline(0, W, FB, K("gris", 5))
    # luz: neones (fríos), cada uno a su manera
    cv.add_light(0, WB, W, FB, -1)
    cv.glow_rgb = K("cielo", 6)
    for nx, est in NEONES:
        if est:
            cv.add_glow_suave(nx, 100, 110 if est == 2 else 70, 0.26 if est == 2 else 0.14, squash=1.5, limite=(0, WT, W, FB))
    cv.bake_lighting()
    # segunda pasada: las telepantallas y el cono de barrido
    cv.light = [[0] * W for _ in range(H)]
    cv.glow = [[0.0] * W for _ in range(H)]
    cv.glow_rgb = K("tele", 4)
    cv.add_glow_suave(485, 34, 40, 0.3, limite=(0, WT, W, FB))
    cv.add_glow_suave(759, 30, 34, 0.25, limite=(0, WT, W, FB))
    ax, ay = 488, 44                                                                           # el cono que barre el suelo
    for y in range(WB, FB):
        t = (y - ay) / (FB - ay)
        cxx, half = ax + 64 * t, 6 + 40 * t
        for x in range(int(cxx - half), int(cxx + half)):
            if 0 <= x < W:
                borde = abs(x - cxx) / half
                k = 0.16 if borde < 0.6 else 0.1 if borde < 0.85 else 0.05
                cv.glow[y][x] = max(cv.glow[y][x], k)
    cv.bake_lighting()
    return cv
