"""J2.05 — Centro de la Comunidad: ping-pong, piano desafinado y pancartas a medio pintar."""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 20, 84, 246


def dibujar():
    rnd = random.Random(5)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    P.papel_pintado(cv, X0, WT, X1, WB, rampa="pared", base=3, motivo="rombo")
    P.zocalo(cv, X0, X1, WB)
    # cartel nuevo de los mártires: diez caras, Ivy en primera fila
    mx0, my0 = 180, 24
    cv.rect(mx0, my0, mx0 + 96, my0 + 54, K("rojo", 4)); cv.frame(mx0, my0, mx0 + 96, my0 + 54, K("rojo", 2))
    for i in range(10):
        fx = mx0 + 6 + (i % 5) * 18 + (0 if i < 5 else 0)
        fy = my0 + 6 + (i // 5) * 18
        cv.ellipse(fx, fy, fx + 12, fy + 14, K("papel", 4 if i == 7 else 3))
        cv.ellipse(fx, fy - 1, fx + 12, fy + 6, K("rojo", 1))
    cv.text(mx0 + 48 - cv.text_width("MARTIRES") // 2, my0 + 44, "MARTIRES", K("papel", 4))
    P.cartel_gran_hermano(cv, 300, 26, w=40, h=48)
    P.cartel_consignas(cv, 60, 30, w=84, h=42)
    # suelo de tablones
    P.tablones(cv, X0, WB, X1, FB, rampa="madera", base=3, semilla=12)
    # mesa de ping-pong
    cv.rect(70, 120, 170, 170, K("tele", 2)); cv.frame(70, 120, 170, 170, K("papel", 3))
    cv.vline(120, 120, 170, K("papel", 3)); cv.rect(118, 116, 122, 174, K("gris", 6))
    cv.rect(70, 170, 170, 175, K("tele", 1))
    # piano
    cv.rect(360, 92, 430, 128, K("madera", 1)); cv.rect(362, 112, 428, 122, K("papel", 4))
    for k in range(364, 428, 5):
        cv.vline(k, 112, 122, K("gris", 3))
        if (k // 5) % 7 not in (2, 6):
            cv.rect(k + 3, 112, k + 5, 117, K("gris", 0))
    cv.rect(360, 128, 430, 134, K("madera", 0))
    cv.rect(382, 140, 408, 148, K("madera", 2))                                  # banqueta
    # pancartas a medio pintar extendidas en el suelo y botes de pintura
    cv.rect(190, 190, 330, 222, K("papel", 3)); cv.frame(190, 190, 330, 222, K("papel", 1))
    cv.text(200, 196, "MUERTE A", K("rojo", 3))
    cv.rect(250, 206, 262, 214, K("rojo", 3))
    for (bx, by) in [(340, 196), (352, 204), (178, 214)]:
        cv.ellipse(bx, by, bx + 10, by + 6, K("rojo", 3), outline=K("gris", 2)); cv.rect(bx, by + 3, bx + 10, by + 10, K("gris", 4))
    for _ in range(40):
        cv.px(rnd.randint(176, 360), rnd.randint(186, 230), K("rojo", 3))         # salpicaduras
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, 224, FB + 12, K("gris", 3)); cv.rect(256, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(224, FB, 256, FB + 12, K("madera", 2))
    for lx in (150, 330):
        cv.vline(lx, WT, 30, K("gris", 1)); cv.ellipse(lx - 3, 29, lx + 4, 36, K("ocre", 4)); cv.add_emissive(lx - 3, 29, lx + 4, 36)
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(150, 80, 150, 0.16, limite=(X0, WT, X1, FB))
    cv.add_glow_suave(330, 80, 150, 0.16, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
