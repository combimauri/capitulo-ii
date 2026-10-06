# Capítulo II

Aventura narrativa en pixel art, basada libremente en *1984* de George Orwell. Juego web (escritorio y móvil, instalable como PWA) hecho con **Phaser 4 + TypeScript + ink**.

## Comandos

```bash
npm install        # dependencias
npm run dev        # servidor de desarrollo (http://localhost:5173)
npm test           # pruebas: compilación de ink, linter de contenido, estado
npm run build      # comprobación de tipos + compilación de producción (dist/)
npm run art        # regenera el arte (Python + Pillow) y lo exporta a public/assets
python3 tools/generar_mapas.py   # regenera los mapas de Tiled (content/locations)
```

## Controles

| Acción | Teclado / ratón | Táctil |
|---|---|---|
| Caminar | WASD / flechas (Mayús = correr) · clic en el suelo | Arrastrar el dedo (joystick) o tocar el suelo |
| Usar lo que tienes delante | `E` / Espacio · clic en el objeto | Botón USAR o tocar el objeto |
| Mirar | `Q` · clic derecho | Botón MIRAR o mantener pulsado el objeto |
| Objetos (mirar, o «usar con…» algo del escenario) | `I` · `Esc` suelta el objeto | Botón OBJ. |
| Registro de diálogos | `L` | Botón REG. |
| Esconderse (sábanas, portales, carritos) | `E` junto al escondite; moverse para salir | Botón USAR |
| Abrir o cerrar la carpeta (sigilo social, Miniver) | `C` | Botón CARPETA |
| Dar a la manivela de la linterna (túneles) | `F` | Botón DINAMO |
| Avanzar diálogo | Espacio / Enter / clic | Tocar |
| Elegir opción | 1–9, flechas + Enter, clic | Tocar |
| Depuración | `F1` | — |

En desarrollo, la consola del navegador ofrece `saltar('departamento', 'depto.entrar')` para ir directamente a cualquier escena, y `audio` para probar música (`audio.musica.poner('himno')`), ambientes (`audio.ambiente.poner(['tunel'])`) y efectos (`audio.play('sirena')`).

Los volúmenes (general, música, efectos y ambiente) están en *Opciones*, en el menú principal.

## Estructura

```
docs/        guion, guion detallado, diseño técnico y biblia visual
content/     historia en ink (content/ink) y mapas de Tiled (content/locations)
art/         arte generado por código (Python) → public/assets
src/         juego: core (puente narrativo, guardado, mapas), scenes, systems, ui
tools/       plugin de Vite que compila ink
tests/       pruebas de Vitest
```
