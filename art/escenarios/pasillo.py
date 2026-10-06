"""J3.05 — Pasillo de la planta 14 del Minipax, al salir: neones que fallan y el carrito de la limpieza."""
from pixel import Canvas, K
import props as P

W, H = 960, 270
WT, WB, FB = 16, 88, 200
NEONES = (110, 290, 470, 650, 830)


def carrito(cv, x, y):
    """Carrito de la limpieza: bastidor de metal, cubo con agua, fregona y trapos."""
    cv.rect(x + 2, y + 26, x + 36, y + 30, K("gris", 1))                       # sombra
    cv.rect(x, y + 8, x + 34, y + 10, K("gris", 6))                            # bandeja de arriba
    cv.rect(x, y + 22, x + 34, y + 24, K("gris", 5))                           # bandeja de abajo
    for px in (x, x + 33):
        cv.vline(px, y + 8, y + 26, K("gris", 4))
    for rx in (x + 3, x + 30):
        cv.rect(rx, y + 26, rx + 2, y + 28, K("gris", 1))                      # ruedas
    # cubo
    cv.rect(x + 18, y + 12, x + 31, y + 22, K("gris", 5)); cv.frame(x + 18, y + 12, x + 31, y + 22, K("gris", 3))
    cv.rect(x + 19, y + 12, x + 30, y + 14, K("cielo", 3))
    # fregona
    cv.vline(x + 24, y - 14, y + 14, K("madera", 3)); cv.vline(x + 25, y - 14, y + 14, K("madera", 2))
    # trapos (ahí debajo van los dibujos)
    cv.rect(x + 2, y + 2, x + 16, y + 8, K("tela", 3)); cv.rect(x + 4, y + 1, x + 13, y + 3, K("papel", 2))
    cv.hline(x + 3, x + 15, y + 5, K("tela", 1))
    cv.rect(x + 3, y + 16, x + 15, y + 22, K("granate", 3)); cv.hline(x + 4, x + 14, y + 18, K("granate", 1))
    # lejía
    cv.rect(x + 6, y + 11, x + 11, y + 21, K("papel", 3)); cv.rect(x + 7, y + 9, x + 10, y + 11, K("rojo", 3))


def cartel_puerta(cv, x, w, texto):
    cv.rect(x, 30, x + w, 36, K("papel", 3))
    cv.text(x + w // 2 - cv.text_width(texto) // 2, 31, texto, K("gris", 1))


def dibujar():
    cv = Canvas(W, H)
    P.tapa_muro(cv, 0, WT - 12, W, WT)
    P.papel_pintado(cv, 0, WT, W, WB, rampa="pared", base=2, motivo="rayas")
    P.zocalo(cv, 0, W, WB, rampa="gris", base=3)
    # tubos neumáticos y neones
    for i, ty in enumerate((20, 25)):
        cv.hline(0, W, ty, K("gris", 5 - i)); cv.hline(0, W, ty + 1, K("gris", 2))
    for nx in NEONES:
        cv.rect(nx - 24, 10, nx + 24, 16, K("gris", 2)); cv.rect(nx - 22, 12, nx + 22, 14, K("papel", 4))
        cv.hline(nx - 22, nx + 22, 15, K("cielo", 6))
    # puertas a lo largo del pasillo
    P.puerta(cv, 60, 40, w=32, h=48, rampa="madera", base=2, cristal=True)
    cartel_puerta(cv, 52, 48, "CARTOGRAFIA")
    P.puerta(cv, 240, 40, w=32, h=48, rampa="madera", base=1)
    cartel_puerta(cv, 236, 40, "ARCHIVO")
    P.telepantalla(cv, 352, 38, 46, 32)
    P.puerta(cv, 460, 40, w=32, h=48, rampa="madera", base=1, cristal=True)
    cartel_puerta(cv, 456, 40, "SALA 14-D")
    P.cartel_gran_hermano(cv, 586, 34, w=36, h=46)
    P.puerta(cv, 760, 40, w=32, h=48, rampa="gris", base=3)
    cartel_puerta(cv, 748, 56, "SUMINISTROS")
    # salida a la escalera: un hueco oscuro con los primeros peldaños
    cv.rect(886, 38, 922, WB, K("gris", 0))
    for k in range(5):
        cv.rect(888, 78 - k * 8, 920, 80 - k * 8, K("gris", 2 + (k % 2)))
    cartel_puerta(cv, 880, 48, "ESCALERA")
    # suelo de linóleo, gastado por el centro
    P.baldosas(cv, 0, WB, W, FB, K("tela", 2), K("tela", 1), t=16, linea=K("tela", 0))
    for x in range(0, W, 3):
        for y in range(132, 158, 5):
            if (x * 7 + y * 3) % 11 == 0:
                cv.px(x, y, K("tela", 3))
    carrito(cv, 700, 120)
    # muro inferior
    cv.rect(0, FB, W, FB + 12, K("gris", 3)); cv.hline(0, W, FB, K("gris", 5))
    # luz: cada neón ilumina su tramo; entre uno y otro, penumbra
    for nx in NEONES:
        cv.add_glow_suave(nx, 110, 95, 0.3, squash=1.5, limite=(0, WT, W, FB))
    cv.add_emissive(0, 12, W, 15)
    cv.bake_lighting()
    return cv
