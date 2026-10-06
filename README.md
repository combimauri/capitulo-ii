# Capítulo II

Aventura narrativa en pixel art, basada libremente en *1984* de George Orwell. Juego web (escritorio y móvil, instalable como PWA) hecho con **Phaser 4 + TypeScript + ink**.

## Comandos

```bash
npm install        # dependencias
npm run dev        # servidor de desarrollo (http://localhost:5173)
npm test           # pruebas: compilación de ink, linter de contenido, estado
npm run build      # comprobación de tipos + compilación de producción (dist/)
npm run art        # regenera el arte (Python + Pillow) y lo exporta a public/assets
```

## Controles (demo técnica)

| Acción | Teclado / ratón | Táctil |
|---|---|---|
| Caminar | WASD / flechas (Mayús = correr) · clic en el suelo | Tocar el suelo |
| Usar lo que tienes delante | `E` / Espacio · clic en el objeto | Tocar el objeto |
| Mirar | `Q` · clic derecho | Mantener pulsado el objeto |
| Avanzar diálogo | Espacio / Enter / clic | Tocar |
| Elegir opción | 1–9, flechas + Enter, clic | Tocar |
| Depuración | `F1` | — |

## Estructura

```
docs/        guion, guion detallado, diseño técnico y biblia visual
content/     historia en ink (content/ink) y mapas de Tiled (content/locations)
art/         arte generado por código (Python) → public/assets
src/         juego: core (puente narrativo, guardado, mapas), scenes, systems, ui
tools/       plugin de Vite que compila ink
tests/       pruebas de Vitest
```
