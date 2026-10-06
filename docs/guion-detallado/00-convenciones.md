# Convenciones del guion detallado

Notación común para todos los actos. Está pensada para que el guion pueda convertirse casi directamente en datos del juego (escenas, diálogos, condiciones y efectos).

---

## Identificadores

| Elemento | Formato | Ejemplo |
|---|---|---|
| Escena | `P.NN` (prólogo) / `JX.NN` (jornada X) | `J2.04` |
| Decisión | `◆ D-JX-NOMBRE` | `◆ D-J2-AMORY` |
| Doblepensar | `DP-JX-NOMBRE` | `DP-J3-AMORY` |
| Crimen facial | `CF-JX-NOMBRE` | `CF-J2-ODIO` |
| Objeto de inventario | `item_nombre` | `item_reloj_ivy` |
| Entrada de diario | `diario_nombre` | `diario_sammy` |

## Marcas en los textos

| Marca | Significado |
|---|---|
| `{NOMBRE}` / `{APELLIDO}` | Nombre y apellido elegidos en la Ficha de Afiliación. Ivy comparte el apellido. |
| `{NUM}` | Número de afiliado, generado (formato `6 cifras + inicial del apellido`, p. ej. `4417 0{A}`). |
| `{o\|a}` | Variante de género del protagonista: masculino \| femenino. Ej.: `cansad{o\|a}`. |
| `{el\|la}`, `{él\|ella}`… | Igual, para palabras completas. |
| `PERSONAJE:` | Línea de diálogo hablada. |
| `PENSAMIENTO:` | Monólogo interior del protagonista (en el juego, en cursiva y sin bocadillo). |
| `TELEPANTALLA:` | Voz de la telepantalla (en el juego, texto verde con estática). |
| `(acotación)` | Indicación de animación, sonido o puesta en escena. |
| `CARTEL:` | Texto que aparece en pantalla como rótulo o título. |

## Interacción point & click

- Cada escena tiene una lista de **puntos interactivos** con la forma **[Objeto]** y sus acciones:
  - `MIRAR`: descripción u observación del protagonista.
  - `USAR`: acción sobre el objeto.
  - `HABLAR`: abre un diálogo.
- Si un objeto no tiene una acción, el juego no la ofrece.
- Propuesta de controles (se decidirá en el diseño técnico): **tocar o clicar** ejecuta la acción principal; **mantener pulsado o clic derecho** ejecuta `MIRAR`.
- `→ salida` indica una transición a otra escena.

## Efectos y condiciones

```
⟶ DUDA +10                 sube la Duda
⟶ SOSPECHA +5              sube la Sospecha
⟶ FLAG amory_reaccion = "risa"
⟶ ITEM +item_lapiz_amory   añade un objeto al inventario (– para quitarlo)
⟶ DIARIO +diario_amory     añade una entrada disponible para el diario
SI duda >= 20: …           rama condicional
SI FLAG amory_denunciado: …
```

- La Duda y la Sospecha van de **0 a 100** y nunca bajan de 0.
- **Sospecha 100** dispara el arresto (en las Jornadas 1–3, vaporización inmediata; desde la Jornada 4, Final C).

## Crimen facial

`CF[expresión, dificultad]`

- **Expresiones:** Entusiasmo · Odio · Júbilo · Desprecio · Neutral · Duelo patriótico.
- **Dificultad:** fácil / media / difícil (velocidad y número de cambios).
- **Fallo:** SOSPECHA +3 (fácil) / +5 (media) / +10 (difícil).
- Con la Duda alta, el monólogo interior contradice la cara durante el microjuego.

## Doblepensar

`DP[id]`: el juego reescribe un diálogo o documento ya visto (con un efecto visual de *glitch* en el registro de diálogos) y ofrece dos opciones:

| Opción | Efecto base |
|---|---|
| **Aceptar** | DUDA −5 · SOSPECHA −5 |
| **Recordar** | DUDA +10 a +15. La versión original se guarda (en "memoria" antes de tener diario y en el diario desde la Jornada 5). |

## Monólogo interior según la Duda

Las líneas de `PENSAMIENTO` pueden tener variantes según el tramo de Duda:

| Tramo | Duda | Voz |
|---|---|---|
| `[D0]` | 0–19 | Fanática, segura, llena de consignas. |
| `[D1]` | 20–49 | Inquieta: preguntas que se corta a sí misma. |
| `[D2]` | 50–100 | Lúcida, amarga, cada vez más suya. |

En el Acto I casi todo está en `[D0]`.

## Variables globales

| Variable | Tipo | Se fija en | Uso |
|---|---|---|---|
| `duda` | 0–100 | Todo el juego | Desbloqueos y finales. Paleta de color. |
| `sospecha` | 0–100 | Todo el juego | Arresto al llegar a 100. |
| `genero` | `m` / `f` | P.03 | Concordancia de textos. |
| `nombre`, `apellido` | texto | P.03 | Textos. (La edad es fija: 34 años.) |
| `parte_j1` | `{verbo, km, prisioneros, bajas}` | J1.05 | Reaparece alterado en la Jornada 6. |
| `amory_reaccion` | `"risa"` / `"reprimenda"` / `"denuncia"` | J2.04 | Jornada 3, Capítulo II, Café del Castaño. |
| `dp_j3_amory` | `"aceptar"` / `"recordar"` | J3.03 | Monólogo y diario. |
| `lapiz_destruido` | bool | J3.04 | Prueba física de Amory. |
| `cf_*` | `"perfecto"` / `"aceptable"` / `"fallo"` | Cada CF | Reacciones de personajes. |
| `sammy_intento` | bool | J5 | Actitud de Dot en la Jornada 12. |
| `hilda_aprecio` | 0–3 | Varias | Facilita o dificulta las inspecciones de Hilda. |

## Umbrales de referencia (ajustables al equilibrar)

| Momento | Condición | Resultado |
|---|---|---|
| Jornada 7, negarse a Nell | `duda < 30` | Final A |
| Jornada 7, negarse a Nell | `duda >= 30` | Nell insiste una vez; si el jugador vuelve a negarse, Final A. |
| Cualquier momento | `sospecha >= 100` | Arresto |
| Cada jornada nueva, desde la 5 | — | SOSPECHA −5 (equilibrio, M7; respeta el suelo de 40 si el Comité leyó el diario) |
