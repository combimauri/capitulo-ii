"""Exporta el arte generado a public/assets (lo que carga el juego).

Uso: npm run art   (o python3 art/exportar.py)
"""
import subprocess
import sys
from pathlib import Path

ART = Path(__file__).resolve().parent
RAIZ = ART.parent
DESTINO = RAIZ / "public" / "assets"

sys.path.insert(0, str(ART / "lib"))
sys.path.insert(0, str(ART / "personajes"))
sys.path.insert(0, str(ART / "ui"))
sys.path.append(str(ART / "escenarios"))


def main():
    (DESTINO / "locations").mkdir(parents=True, exist_ok=True)
    (DESTINO / "sprites").mkdir(parents=True, exist_ok=True)
    iconos = RAIZ / "public" / "icons"
    iconos.mkdir(parents=True, exist_ok=True)

    subprocess.run([sys.executable, str(ART / "pruebas" / "piso_hd.py"), "--sin-protagonista",
                    f"--salida={DESTINO / 'locations' / 'piso.png'}"], check=True)

    import protagonista
    protagonista.hoja_sprites(DESTINO / "sprites" / "protagonista_h.png")
    protagonista.hoja_sprites(DESTINO / "sprites" / "protagonista_m.png", femenina=True)
    protagonista.hoja_sprites(DESTINO / "sprites" / "protagonista_h_preso.png", preso=True)
    protagonista.hoja_sprites(DESTINO / "sprites" / "protagonista_m_preso.png", femenina=True, preso=True)
    print("ok protagonista H y M")

    import npcs
    print("ok npcs", npcs.exportar(DESTINO / "sprites" / "npc"))

    import retrato_protagonista as rp
    (DESTINO / "retratos").mkdir(exist_ok=True)
    for g, fem in (("h", False), ("m", True)):
        for e in ["NEUTRAL", "ENTUSIASMO", "ODIO", "JUBILO", "DESPRECIO", "DUELO"]:
            rp.retrato(e, fem).save(DESTINO / "retratos" / f"prot_{g}_{e.lower()}.png")
            rp.retrato(e, fem, agrietada=True).save(DESTINO / "retratos" / f"prot_{g}_{e.lower()}_grieta.png")
    import retrato_amory
    retrato_amory.exportar(DESTINO / "retratos")
    import retrato_obrien
    retrato_obrien.exportar(DESTINO / "retratos")
    print("ok retratos")

    import iconos as ic
    ic.exportar(DESTINO / "iconos", DESTINO / "minijuegos")
    import odio
    odio.exportar(DESTINO / "minijuegos")
    import londres
    londres.exportar(DESTINO / "minijuegos")
    import vinetas
    vinetas.exportar(DESTINO / "vinetas")
    import vinetas_finales
    vinetas_finales.exportar(DESTINO / "vinetas")
    import cripta_anios
    for anio in ("1985", "1987", "1988", "1990", "1993"):
        cripta_anios.dibujar(anio).img.save(DESTINO / "vinetas" / f"cripta_{anio}.png")
    print("ok iconos y minijuegos")

    import icono
    for t in (192, 512):
        icono.icono(t).save(iconos / f"icono-{t}.png")
    print("ok icono de la app")

    import escenarios
    for nombre in escenarios.exportar(DESTINO / "locations"):
        print("ok escenario", nombre)


if __name__ == "__main__":
    main()
