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


def main():
    (DESTINO / "locations").mkdir(parents=True, exist_ok=True)
    (DESTINO / "sprites").mkdir(parents=True, exist_ok=True)
    iconos = RAIZ / "public" / "icons"
    iconos.mkdir(parents=True, exist_ok=True)

    subprocess.run([sys.executable, str(ART / "pruebas" / "piso_hd.py"), "--sin-protagonista",
                    f"--salida={DESTINO / 'locations' / 'piso.png'}"], check=True)

    import protagonista
    print("ok", protagonista.hoja_sprites(DESTINO / "sprites" / "protagonista_h.png"))

    import icono
    for t in (192, 512):
        icono.icono(t).save(iconos / f"icono-{t}.png")
    print("ok iconos")


if __name__ == "__main__":
    main()
