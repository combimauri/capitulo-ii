"""J1.04 — Vestíbulo del Ministerio de la Paz: mármol frío, torniquetes y guardias."""
from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 16, 96, 246
TORNIQUETES_Y = 150


def dibujar():
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    # pared de mármol blanco altísima con las letras del ministerio
    cv.rect(X0, WT, X1, WB, K("papel", 4))
    for x in range(X0, X1, 40):
        cv.vline(x, WT, WB, K("papel", 3))
    for y in range(WT + 20, WB, 20):
        cv.hline(X0, X1, y, K("papel", 3))
    for (x, y) in [(70, 30), (71, 31), (72, 33), (300, 60), (301, 61), (390, 40), (391, 42)]:
        cv.px(x, y, K("papel", 1))                                          # vetas
    titulo = "MINISTERIO DE LA PAZ"
    tw = cv.text_width(titulo, spacing=2) * 2
    for i, ch in enumerate(titulo):                                         # letras al doble
        tmp = []
        bits = __import__("pixel").FONT3x5.get(ch, "0" * 15)
        for k, b in enumerate(bits):
            if b == "1":
                cv.rect(240 - tw // 2 + i * 10 + (k % 3) * 2, 24 + (k // 3) * 2,
                        240 - tw // 2 + i * 10 + (k % 3) * 2 + 2, 24 + (k // 3) * 2 + 2, K("gris", 2))
    lema = "LA GUERRA ES LA PAZ"
    cv.text(240 - cv.text_width(lema) // 2, 40, lema, K("rojo", 3))
    # ascensores
    for i, ex in enumerate((72, 118)):
        cv.rect(ex, 52, ex + 34, WB - 2, K("gris", 6)); cv.frame(ex, 52, ex + 34, WB - 2, K("gris", 3))
        cv.vline(ex + 17, 54, WB - 2, K("gris", 3))
        cv.rect(ex + 12, 46, ex + 22, 50, K("ocre", 3) if i == 0 else K("gris", 4))
    # telepantalla enorme y estandartes rojos
    P.telepantalla(cv, 300, 50, 64, 38, texto="VICTORIA")
    for sx in (44, 422):
        cv.rect(sx, WT + 4, sx + 14, WB - 6, K("rojo", 3)); cv.vline(sx + 7, WT + 8, WB - 10, K("papel", 3))
        cv.poly([(sx, WB - 6), (sx + 7, WB), (sx + 14, WB - 6)], K("rojo", 3))
    P.zocalo(cv, X0, X1, WB, alto=4, rampa="gris", base=4)
    # suelo de mármol en damero
    P.baldosas(cv, X0, WB, X1, FB, K("gris", 8), K("gris", 6), t=20, linea=K("gris", 5))
    # columnas
    for cx in (70, 410):
        cv.rect(cx - 10, WB, cx + 10, 236, K("papel", 3)); cv.rect(cx - 12, 228, cx + 12, 240, K("papel", 2))
        cv.vline(cx - 6, WB, 228, K("papel", 4)); cv.vline(cx + 7, WB, 228, K("papel", 1))
    # línea de torniquetes con la garita del guardia en el centro
    for tx in range(100, 380, 26):
        if 214 <= tx <= 254:
            continue
        cv.rect(tx, TORNIQUETES_Y - 10, tx + 10, TORNIQUETES_Y + 4, K("gris", 3))
        cv.rect(tx + 1, TORNIQUETES_Y - 12, tx + 9, TORNIQUETES_Y - 9, K("gris", 6))
        cv.hline(tx + 10, tx + 24, TORNIQUETES_Y - 4, K("gris", 2))
    cv.rect(206, TORNIQUETES_Y - 14, 214, TORNIQUETES_Y + 6, K("gris", 2))
    cv.rect(258, TORNIQUETES_Y - 14, 266, TORNIQUETES_Y + 6, K("gris", 2))
    # garita
    cv.rect(380, 128, 420, 168, K("madera", 2)); cv.rect(380, 124, 420, 130, K("madera", 4))
    cv.rect(384, 132, 416, 140, K("cielo", 5))
    # alfombra roja hacia los ascensores
    cv.rect(222, WB, 250, FB, K("rojo", 2)); cv.vline(222, WB, FB, K("rojo", 1)); cv.vline(249, WB, FB, K("rojo", 1))
    # muros laterales e inferior (puerta de entrada abajo, centrada)
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, 216, FB + 12, K("gris", 3)); cv.rect(264, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(216, FB, 264, FB + 12, K("gris", 6))
    cv.add_light_fn(lambda x, y: -1 if (x < X0 + 5 or x > X1 - 5) else 0)
    cv.add_glow_suave(332, 96, 90, 0.16, squash=1.4, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
