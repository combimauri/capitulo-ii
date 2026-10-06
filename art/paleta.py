"""Lámina de la paleta: una fila por rampa de material (de oscuro a claro)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from pixel import Canvas, K, RAMPS  # noqa: E402

SW, ROW, LABEL = 12, 14, 40
ancho = LABEL + max(len(v) for v in RAMPS.values()) * SW + 8
cv = Canvas(ancho, len(RAMPS) * ROW + 8, bg=("gris", 1))
for r, (nombre, cols) in enumerate(RAMPS.items()):
    y = 4 + r * ROW
    cv.text(4, y + 4, nombre, K("papel", 3))
    for i in range(len(cols)):
        cv.rect(LABEL + i * SW, y, LABEL + i * SW + SW - 2, y + ROW - 2, K(nombre, i))
prev = cv.save(Path(__file__).parent / "paleta.png", preview_scale=4)
print("ok", prev)
