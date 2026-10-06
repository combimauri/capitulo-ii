# CAPÍTULO II — Diseño técnico (v0.2)

> Cómo se construye el juego: motor, arquitectura, formato de datos, sistemas, controles, guardado y plan de desarrollo.
>
> **v0.2:** perspectiva **cenital 3/4** (estilo Stardew Valley / Pokémon / Final Fantasy VI) con cuadrícula de 16×16, personajes de 20×40 y **control mixto**: movimiento directo más tocar o hacer clic para ir a un objeto y usarlo.
> Referencias: [guion.md](guion.md) (biblia) · [guion-detallado/](guion-detallado/) (guion por actos) · [convenciones](guion-detallado/00-convenciones.md).

---

## 1. Resumen de decisiones

| Área | Decisión | Motivo |
|---|---|---|
| **Motor** | **Phaser** (v4 si es estable al iniciar el proyecto; si no, 3.x) + **TypeScript** | Motor 2D web maduro, con buen soporte de pixel art, cámaras, input táctil, audio, carga por escenas y mapas de Tiled. Corre en cualquier navegador sin instalación. |
| **Narrativa** | **ink** (lenguaje de inkle) ejecutado con **inkjs** | Diseñado para narrativa ramificada con variables, condiciones, listas e inventario. La notación del guion (`SI…`, `⟶ DUDA +10`, decisiones ◆) se traduce casi uno a uno. El estado completo se serializa en JSON para guardar partida. |
| **Perspectiva** | **Cenital 3/4** con tiles de 16×16 y personajes de 20×40 | Estilo Stardew Valley, Pokémon o Final Fantasy VI. Los tiles reutilizables abaratan mucho la producción de arte. |
| **Escenarios** | **Tiled** (editor de mapas por tiles) → JSON | Capas de tiles (suelo, paredes, objetos), colisiones, puntos interactivos, salidas, conos de telepantalla y rutas de guardias. Phaser carga Tiled de forma nativa. |
| **Sprites** | **Aseprite** (o LibreSprite/Pixelorama, gratuitos) → hojas de sprites + JSON | Formato que Phaser entiende directamente, con animaciones etiquetadas. |
| **Build** | **Vite** | Arranque instantáneo y recarga en caliente, incluida la de los `.ink` mediante un plugin propio. |
| **Pruebas** | **Vitest** + bot de recorrido de ink en Node | Verifica que todos los finales se alcanzan y que no hay callejones sin salida. |
| **Guardado** | `localStorage` con esquema versionado + exportar/importar JSON | No necesita servidor. |
| **Distribución** | Sitio estático (sin backend) | Por ahora solo en local. Si se publica, sirve cualquier hosting estático. |

### Alternativas descartadas

| Alternativa | Por qué no |
|---|---|
| **Godot (exportación web)** | Ejecutables web pesados (~30–40 MB), problemas históricos con Safari en iOS y arranque lento en móvil. |
| **Motor propio sobre Canvas o PixiJS** | Habría que reconstruir cargador, escenas, input, audio y cámaras: semanas de trabajo sin valor narrativo. |
| **Angular / React para todo** | Excelentes para interfaz, pero no para un bucle de juego con sprites, colisiones y shaders. Mezclar un framework de UI con el canvas complica el escalado de píxeles. |
| **Diálogos en JSON/YAML propios** | Habría que inventar condiciones, variables y saltos: es reinventar ink peor. |

---

## 2. Arquitectura general

```
┌─────────────────────────────────────────────────────────────────┐
│                          NAVEGADOR                              │
│                                                                 │
│  ┌──────────────┐   etiquetas / comandos   ┌─────────────────┐  │
│  │  inkjs       │ ───────────────────────► │  NarrativeBridge│  │
│  │  (historia,  │ ◄─────────────────────── │  (puente)       │  │
│  │  variables,  │   resultados minijuegos  └────────┬────────┘  │
│  │  inventario) │                                   │           │
│  └──────────────┘                                   ▼           │
│         ▲                              ┌──────────────────────┐ │
│         │ estado JSON                  │   GameDirector       │ │
│  ┌──────┴───────┐                      │ (cambia escenas,     │ │
│  │  SaveSystem  │ ◄────────────────────│  lanza minijuegos)   │ │
│  └──────────────┘                      └──────────┬───────────┘ │
│                                                   │             │
│     ┌──────────────────┬───────────────┬──────────┴──────┐      │
│     ▼                  ▼               ▼                 ▼      │
│ LocationScene     MinigameScenes    UIScene         FX/Palette  │
│ (mapa cenital,    (CF, sigilo,      (diálogo, inv., (shader de  │
│  Tiled, A*)        documentos,       diario, log,    Duda)      │
│                    mapas…)           HUD Sospecha)              │
└─────────────────────────────────────────────────────────────────┘
```

**Principio rector:** **ink es la única fuente de verdad del estado narrativo** (Duda, Sospecha, flags, inventario, entradas de diario). El motor **lee** ese estado para pintar y **escribe** en él solo a través de funciones del puente, como el resultado de un minijuego. Así, guardar partida es guardar el estado de ink más la posición en el mundo.

### 2.1 Responsabilidades

| Módulo | Hace | No hace |
|---|---|---|
| **ink (contenido)** | Diálogos, decisiones, condiciones, variables, inventario, efectos (`~ duda += 10`), qué minijuego toca y con qué parámetros. | Nada visual. |
| **NarrativeBridge** | Avanza la historia, interpreta las etiquetas (`# cf:…`, `# dp:…`), expone variables observables al resto del juego y registra funciones externas. | Lógica de juego. |
| **GameDirector** | Máquina de estados de alto nivel: qué escena está activa, transiciones, pausa, ir a jornada X. | Texto. |
| **LocationScene** | Escena genérica de exploración cenital: carga un mapa de Tiled, mueve al protagonista (directo o tocando), gestiona colisiones, *y-sort*, puntos interactivos y conos de telepantalla. | Minijuegos. |
| **Minijuegos** | Escenas Phaser independientes que reciben parámetros y devuelven un resultado. | Modificar el estado directamente: siempre devuelven el resultado al puente. |
| **UIScene** | Capa siempre activa encima de todo: caja de diálogo, elecciones, inventario, diario, registro de diálogos, indicador de Sospecha y menú de pausa. | — |
| **SaveSystem** | Serializar, deserializar, migrar versiones, autoguardado, ranuras y exportación. | — |

---

## 3. Resolución, escalado y render

| Parámetro | Valor |
|---|---|
| **Resolución del arte** | **480 × 270** (16:9). Escala exacta a 1920×1080 (×4) y 1440×810 (×3). |
| **Resolución interna del juego** | **960 × 540** |
| **Cámara del mundo** | `zoom = 2`: el arte de 480×270 se dibuja a 2× con píxeles enteros |
| **Cámara de UI** | `zoom = 1`: la interfaz se dibuja a 960×540, con texto pixel art más fino y legible |
| **Vista** | 30 × 17 tiles visibles. La cámara sigue al protagonista en mapas mayores que la pantalla (calles, ministerios, túneles). |
| **Escalado a pantalla** | `Phaser.Scale.FIT` + escalado **entero** cuando sea posible (CSS `image-rendering: pixelated`). Bandas negras en relaciones de aspecto distintas de 16:9. |
| **Antialias** | Desactivado (`pixelArt: true`, `roundPixels: true`) |
| **Renderer** | WebGL (necesario para el shader de paleta). Respaldo en Canvas sin efectos de color. |

> **Ordenación por profundidad:** todos los objetos con altura (personajes, muebles, farolas) se ordenan por su `y` de base en cada frame (*y-sort*), para que el protagonista pase por delante o por detrás de forma natural.

> **Por qué dos resoluciones:** el juego tiene mucho texto en español, con tildes, eñes y frases largas. Con el arte a 480×270, la UI se dibuja al doble (960×540) con una fuente pixel de 12–16 px y mantiene la estética sin sacrificar legibilidad en móvil.

### 3.1 Fuentes

- **Fuentes pixel en formato bitmap** con juego de caracteres Latin-1 completo (á é í ó ú ü ñ ¿ ¡ « » — …).
- Candidatas: familia *m5x7 / m6x11* (Daniel Linssen), *Pixel Operator* y *Monogram*. **Verificar la licencia de cada una antes de usarla.**
- Tres usos:
  1. **Diálogo:** fuente proporcional, ~11 px.
  2. **Documentos del Partido:** fuente monoespaciada tipo máquina de escribir.
  3. **Diario:** fuente "manuscrita" pixel, para la letra del protagonista.

### 3.2 Paleta y shader de la Duda

- La paleta base está **limitada** (definida en la biblia visual). Todo el arte se dibuja con ella.
- **Shader de post-proceso** en la cámara del mundo con dos texturas LUT:
  - `lut_partido.png`: grises, verde de telepantalla y rojo propaganda.
  - `lut_memoria.png`: la misma paleta con ocres, verdes y pieles cálidas.
  - Mezcla: `mix(lutPartido, lutMemoria, t)` con `t = f(duda, contexto)`.
- **Reglas de `t`:**

| Contexto | `t` |
|---|---|
| Ministerios, Minimor | `0` siempre (salvo flashbacks) |
| Piso del protagonista | `duda / 200` (hasta 0,5) |
| Barrio prole | `0,3 + duda / 200` |
| Cripta de San Clemente | `1` |
| Final A (Semana del Odio) | Interpolación hasta `−0,2`: gris total, incluso el rojo |

- Cuando aparece el *glitch* del doblepensar, el shader añade un **desplazamiento de canales y ruido** durante 1–2 s.

---

## 4. Narrativa en ink

### 4.1 Organización de archivos

```
content/ink/
├── main.ink               ← punto de entrada; incluye todo
├── globals.ink            ← VAR y LIST globales (duda, sospecha, inventario…)
├── funciones.ink          ← funciones de género, efectos, utilidades
├── prologo.ink
├── acto1/
│   ├── j1.ink
│   ├── j2.ink
│   └── j3.ink
├── acto2/ …
├── acto3/ …
├── acto4/ …
├── finales/
│   ├── final_a.ink … final_e.ink
└── comunes/
    ├── hotspots_piso.ink  ← descripciones "MIRAR" reutilizables con variantes
    └── diario.ink         ← entradas de diario y sus variantes
```

Cada escena del guion (`J2.04`) es un **knot** de ink (`=== j2_04 ===`). Cada punto interactivo es un **stitch** o un knot con nombre predecible (`j2_04.mapa_mirar`).

### 4.2 Equivalencia entre la notación del guion y ink

| Guion | ink |
|---|---|
| `⟶ DUDA +10` | `~ sube_duda(10)` (función que limita a 0–100 y avisa al motor) |
| `⟶ SOSPECHA +5` | `~ sube_sospecha(5)` (comprueba el umbral de arresto) |
| `⟶ FLAG amory_reaccion = "risa"` | `~ amory_reaccion = risa` (con `LIST amory_reacciones = risa, reprimenda, denuncia`) |
| `⟶ ITEM +item_lapiz_amory` | `~ inventario += lapiz_amory` (`LIST inventario`) |
| `⟶ DIARIO +diario_sammy` | `~ diario_disponible += sammy` |
| `SI duda >= 20:` | `{ duda >= 20: … }` |
| `◆ D-J2-AMORY` (opciones) | Opciones de ink `* [Reírse]` con la etiqueta `# decision:D-J2-AMORY` |
| `PERSONAJE: texto` | `AMORY: texto # id:j2_04_amory_03` |
| `PENSAMIENTO:` | `PENSAMIENTO: texto` (el motor lo renderiza en cursiva y sin bocadillo) |
| `CF[Odio, media]` | `# cf:id=CF-J2-ODIO,expr=odio,dif=media` |
| `DP[…]` | `# dp:id=DP-J3-AMORY,lineas=j2_04_amory_*` |
| Minijuego | `# minijuego:partes,directiva=malabar_1404` |
| `→ salida a J1.03` | `-> j1_03` + `# escena:calle_avenida` |
| `CARTEL:` | `CARTEL: texto` (el motor lo muestra como rótulo) |

### 4.3 Género y nombre

La notación `{o|a}` del guion **choca con la sintaxis de ink**, donde `{a|b}` significa "secuencia". Se resuelve con **variables cortas** que se fijan al crear el personaje:

```ink
// globals.ink
VAR genero = "m"
VAR nombre = ""
VAR apellido = ""
VAR o = "o"        // cansad{o}
VAR a_ = ""        // traidor{a_}  → traidor / traidora
VAR el = "el"      // {el} camarada
VAR El = "El"
VAR un = "un"      // {un} camarada
VAR del_ = "del"   // dirigido {del_} camarada → del / de la
VAR lo_ = "lo"     // {lo_} vi → lo / la
```

```ink
// funciones.ink
=== function fijar_genero(g) ===
~ genero = g
{ g == "f":
    ~ o = "a"
    ~ a_ = "a"
    ~ el = "la"
    ~ El = "La"
    ~ un = "una"
    ~ del_ = "de la"
    ~ lo_ = "la"
}

// Para casos raros: {g("varón", "mujer")}
=== function g(m, f) ===
{ genero == "f": ~ return f }
~ return m
```

Uso en el texto: `PENSAMIENTO: Estoy cansad{o}. {El} camarada {apellido} no debería…`

> **Regla para el contenido:** se prohíbe escribir `{x|y}` literal en los `.ink`. El linter (ver §11) lo detecta.

### 4.4 Ejemplo: la decisión de Amory (J2.04)

```ink
=== j2_04 ===
# escena:minipax_cartografia
# minijuego:frente,directiva=carto_1504
AMORY: ¿Te has fijado en que el frente de Malabar lleva tres años en el mismo río? # id:j2_04_amory_01
AMORY: Mira los agujeros. Este mapa tiene más agujeros que un queso de la Minindancia. # id:j2_04_amory_02
AMORY: Toma, usa el mío. El tuyo no tiene punta. # id:j2_04_amory_03
~ inventario += lapiz_amory
PENSAMIENTO: ¿Lo habrá oído? # id:j2_04_pens_01

* [Reírse] # decision:D-J2-AMORY
    AMORY: ¡Ja! Sabía que tenías sentido del humor, {apellido}. # id:j2_04_amory_04
    ~ sube_duda(5)
    ~ sube_sospecha(5)
    ~ amory_reaccion = risa
* [Reprenderle]
    PROTAGONISTA: Amory. Eso suena a crimental.
    AMORY: Es… una broma geográfica, camarada. Olvídalo. # id:j2_04_amory_05
    ~ amory_reaccion = reprimenda
* [Denunciarle]
    ~ amory_reaccion = denuncia
    ~ baja_sospecha(10)
    -> j2_04_c
- -> j2_05
```

### 4.5 Etiquetas (tags) que entiende el motor

| Etiqueta | Parámetros | Efecto en el motor |
|---|---|---|
| `# id:<id>` | — | Identificador único de línea (registro de diálogos, doblepensar, traducción y voces futuras). **Obligatorio** en toda línea hablada. |
| `# escena:<loc>` | `loc` = id del mapa Tiled | Carga o transición a una localización. |
| `# pos:<x>,<y>` / `# pos:<spawn>` | — | Coloca al protagonista. |
| `# cf:` | `id, expr, dif, fases?` | Lanza el microjuego de crimen facial. Escribe `cf_<id>` en ink. |
| `# dp:` | `id, lineas` (patrón de ids) | Lanza el doblepensar: *glitch* en el registro y elección Aceptar/Recordar. |
| `# minijuego:<tipo>` | Depende del tipo | Lanza un minijuego (§6). |
| `# sigilo:<mision>` | `checkpoint?` | Lanza o reanuda una secuencia de sigilo. |
| `# decision:<id>` | — | Marca una decisión importante (estadísticas, depuración). |
| `# cartel` | — | La línea se muestra como rótulo a pantalla completa. |
| `# documento:<id>` | — | Abre el visor de documentos con un documento definido en JSON. |
| `# comparar:<idA>,<idB>` | — | Visor de comparación en dos columnas (J6, J9). |
| `# sfx:<id>` / `# musica:<id>` / `# ambiente:<id>` | — | Audio. |
| `# fx:<efecto>` | `glitch`, `blanco`, `negro`, `desaturar`, `temblor`… | Efectos de pantalla. |
| `# esperar:<seg>` | — | Pausa dramática sin input. |
| `# bloquear_input:<seg>` | — | Como en J11.04: el jugador no puede pulsar nada. |
| `# jornada:<n>` | — | Rótulo de jornada y autoguardado. |
| `# final:<id>` | — | Termina la partida, guarda el desbloqueo y lanza los créditos. |

> **Regla importante sobre las etiquetas de acción** (`cf`, `minijuego`, `esperar`, `fx`, `sfx`): ink ejecuta la lógica que hay **antes** de una línea en el mismo paso en que devuelve esa línea. Por eso la etiqueta de un minijuego se pone en la línea que debe mostrarse **después** de jugarlo, y toda la lógica que dependa del resultado (`{ cf_x == "fallo": … }`) va **detrás** de esa línea. Si la etiqueta va en una línea suelta justo antes de una condición, la condición se evalúa antes de jugar. Además, **después de esa lógica debe haber al menos otra línea de texto o de etiquetas**: si solo queda lógica hasta el final del fragmento, ink la ejecuta por adelantado. Cada minijuego tiene una prueba automática que simula su resultado y comprueba que cambia la historia.

### 4.6 Funciones externas (motor → ink)

ink puede **preguntar** al motor con funciones externas registradas en el puente:

```ink
EXTERNAL tiempo_restante()       // en secuencias contrarreloj
EXTERNAL objeto_en_mano()        // qué objeto del inventario tiene seleccionado el jugador
EXTERNAL escondite_diario()      // dónde lo ha arrastrado en el minijuego de Hilda
```

Cada función tiene un *fallback* en ink, para que el bot de pruebas pueda ejecutar la historia sin motor.

### 4.7 Compilación

- En desarrollo, un **plugin de Vite** compila `main.ink` con el compilador de `inkjs` en cada cambio y recarga solo la historia.
- En producción se precompila a `story.json`.
- Los errores de compilación de ink se muestran como overlay en el navegador, igual que los errores de TypeScript.

---

## 5. Localizaciones (mapas cenitales)

### 5.1 Formato: Tiled → JSON

Cada localización es un mapa de Tiled **por tiles de 16×16** con estas capas:

| Capa | Tipo | Contenido |
|---|---|---|
| `suelo` | Tiles | Tablones, baldosas, adoquines, agua (túneles). |
| `paredes` | Tiles | Pared del fondo vista de frente, tapas de muros vistas desde arriba. |
| `objetos_bajos` | Tiles | Alfombras, felpudos, manchas: siempre por debajo de los personajes. |
| `objetos` | Objetos con sprite | Muebles y atrezo con altura (cama, armario, mesa, farolas). Se ordenan por *y-sort* con los personajes. |
| `techo` | Tiles | Lo que siempre va por encima (vigas, copas de árboles, marquesinas). |
| `colisiones` | Objetos (rectángulos) o propiedad `colisiona` en los tiles | Lo que no se puede atravesar. Cada mueble tiene una **caja de colisión en su base**, no en todo el sprite. |
| `hotspots` | Objetos (rectángulos) | Puntos interactivos (ver propiedades abajo). |
| `salidas` | Objetos | Zonas que llevan a otra escena (puertas, bordes de calle, escaleras). |
| `spawns` | Puntos | Posiciones iniciales con nombre y orientación (`arriba`, `abajo`, `izquierda`, `derecha`). |
| `telepantallas` | Objetos (polígonos) | Conos de visión sobre la cuadrícula (fijos o con barrido). |
| `npcs` | Puntos | Personajes, con su sprite, orientación y stitch de ink. |
| `patrullas` | Polilíneas | Rutas de guardias (misiones de sigilo). |
| `escondites` | Objetos | Zonas donde ocultarse. |
| `luz` | Objetos (polígonos) | Zonas de luz o sombra que el motor aplica con la rampa de cada material (ver la biblia visual). |

**Propiedades de un hotspot:**

```json
{
  "name": "cartel_ivy",
  "properties": {
    "nombre_visible": "Cartel de Ivy",
    "mirar": "piso.cartel_ivy_mirar",
    "usar": "piso.cartel_ivy_usar",
    "hablar": null,
    "usar_con": { "diario": "piso.esconder_diario" },
    "condicion": "jornada >= 1",
    "punto_aproximacion": "spawn_cartel",
    "orientacion_requerida": "arriba",
    "cursor": "ojo"
  }
}
```

- `mirar`, `usar` y `hablar` apuntan a **knots o stitches de ink**. Si son `null`, la acción no se ofrece (como pide el guion).
- `condicion` es una expresión evaluada contra las variables de ink, para que el hotspot aparezca o desaparezca según la historia.
- `orientacion_requerida`: hacia dónde debe mirar el protagonista para interactuar con el botón de acción (por ejemplo, objetos colgados en la pared del fondo = `arriba`).

### 5.2 Movimiento (control mixto)

**Dos formas de moverse, intercambiables en cualquier momento:**

1. **Movimiento directo** (como Stardew Valley):
   - Teclado (WASD o flechas), mando (stick o cruceta) o **joystick virtual** en móvil (aparece donde el pulgar toca la mitad izquierda de la pantalla).
   - Movimiento **libre en 8 direcciones** (no casilla a casilla), con colisiones de caja contra la capa `colisiones`.
   - **Botón de acción** (`E`, Espacio, botón A del mando o botón táctil): interactúa con el hotspot que está **delante** del protagonista, dentro de un pequeño radio y en la dirección a la que mira. El hotspot activo se resalta con un contorno y muestra un icono flotante (👁 mirar, ✋ usar, 💬 hablar).
   - **Mirar** con un segundo botón (`Q`, botón B o mantener pulsado el botón de acción).
2. **Tocar o hacer clic** en un hotspot, NPC o punto del suelo:
   - **Pathfinding A\*** sobre la cuadrícula de 16×16 (generada a partir de `colisiones`), con suavizado de la ruta.
   - Al llegar a `punto_aproximacion`, el protagonista se orienta y ejecuta la acción.
   - Tocar el suelo = caminar hasta allí. Mantener pulsado un hotspot = mirar.
   - Si el jugador toca el joystick o una tecla de dirección durante el trayecto, se cancela el camino automático.

**Animaciones del protagonista:** 4 direcciones (arriba, abajo, izquierda y derecha reflejada) × (quieto, caminar de 4 fotogramas). Gestos especiales (agacharse, escribir, esconderse, caer) como animaciones sueltas.

### 5.3 Telepantallas

- Cada telepantalla es un **cono de visión** (polígono) en la vista cenital, que puede ser fijo o barrer con un periodo dado. Las paredes y muebles altos (capa `colisiones` marcada como `opaca`) bloquean la visión mediante *raycast*.
- El cono **solo se ve** cuando el protagonista lleva en la mano un objeto comprometedor (`objeto.comprometedor = true`) o en las misiones de sigilo.
- Hacer ciertas acciones dentro del cono (abrir el diario, robar un documento) dispara `sube_sospecha` mediante un knot de ink asociado.

---

## 6. Minijuegos y sistemas reutilizables

Los ~30 minijuegos del guion se construyen con **siete sistemas reutilizables**, configurados por datos:

| Sistema | Minijuegos del guion |
|---|---|
| **A · Crimen facial (ritmo y expresión)** | Gimnasia, noticias, Dos Minutos de Odio, mitin con giro, confesión de Amory, ejecuciones, Voss (neutral), CF automático ante Goldstein |
| **B · Documentos y máquina de escribir** | Partes de guerra, Gran Rectificación (texto), copiar la Planilla Azul, declaración final (firma), Ficha de Afiliación, composición del Capítulo II |
| **C · Mapa con herramientas** | Mover el frente, Registro de impactos (lámina y compás), Gran Rectificación (banderas), mapa de los túneles con tres capas |
| **D · Sigilo** | Archivo Restringido (J8), Miniver "sigilo social" (J9), lavabos, carrito de Nell (J10), Minimor (J11), persecución en Limehouse (J12), Crane en los túneles |
| **E · Contrarreloj y QTE** | Sammy (J5), esconder el diario (J6), nichos del túnel, combinación del archivo, montacargas, ventana de cuatro minutos |
| **F · Tablero de deducción** | Patrón de los cohetes (J5), San Clemente (J13) |
| **G · Resistencia** | Celda del Minimor, dial de O'Brien, "¿Qué hora marca?", Habitación 101, aguantar 24 horas |

### 6.1 Contrato común

```ts
interface MinigameParams { id: string; [k: string]: unknown }

interface MinigameResult {
  id: string;
  resultado: 'perfecto' | 'aceptable' | 'fallo' | string;
  efectos?: { duda?: number; sospecha?: number };
  datos?: Record<string, unknown>;   // p. ej. { km: 12, prisioneros: 3000 } en el parte de J1
}
```

El motor llama a una función de ink (`~ resultado_minijuego(id, resultado)`) y escribe los `datos` en variables de ink (`parte_j1_km`…). **El minijuego nunca toca el estado directamente.**

### 6.2 A · Crimen facial

- La pantalla muestra **la cara del protagonista** (retrato grande en pixel art) y una **expresión objetivo**.
- Entrada:
  - Escritorio: teclas o clic en iconos de expresión.
  - Móvil: botones grandes en los laterales.
- **Pistas de ritmo:** marcas que llegan al compás de los gritos del público o de la música. Acertar mantiene la "máscara" y fallar la agrieta.
- **Fases** definidas en JSON (`expr`, `bpm`, `duración`, `cambios`), por ejemplo el giro Eurasia → Estasia de J10 o el paso a "Duelo patriótico" cuando aparece el Gran Hermano.
- **Monólogo interferente:** líneas de ink que aparecen sobre la pista (`# cf_pensamiento:…`). Con la Duda alta tapan parte de la pantalla, tal como pide el guion.
- **Asistencia** (opciones): ventana de acierto más amplia o *auto-CF* en el modo historia.

### 6.3 B · Documentos

- **Visor de documentos** con aspecto de papel (fondo, sellos y manchas) y texto en fuente de máquina de escribir.
- **Huecos seleccionables:** un hueco abre un menú con 2–3 opciones (partes de guerra).
- **Palabras tocables:** para tachar o sustituir (Gran Rectificación).
- **Firma:** mantener pulsado sobre la línea, con barra de progreso, sonido de plumilla y sello.
- **Comparador:** dos columnas con las diferencias resaltadas (J6 y J9).
- Los documentos se definen en `content/documentos/*.json` con texto, variables interpoladas (`{parte_j1_km}`) y huecos.

### 6.4 C · Mapa con herramientas

- Mapa grande con *zoom* y desplazamiento (pellizco o rueda), cuadrícula opcional.
- **Chinchetas o banderas** que se arrastran a casillas.
- **Capas superponibles** (lámina de zonificación, dibujos de Amory) con un control de opacidad.
- **Compás:** se toca el centro y se arrastra el radio. Muestra kilómetros.
- **Validación** configurable: "chincheta en casilla J-8", "círculo de 2 km que no contiene chinchetas", "ruta que evita nodos derrumbados".

### 6.5 D · Sigilo

- Funciona **dentro de LocationScene**, activando una capa de sigilo:
  - Conos de visión (telepantallas y guardias) con raycast contra las paredes del mapa.
  - Guardias que siguen polilíneas de Tiled, con pausas y miradas.
  - **Medidor de detección** que se llena mientras el protagonista está en un cono y se vacía fuera.
  - **Escondites** (tocar para entrar o salir).
  - **Sonido:** zonas ruidosas (charcos o cubos) que atraen a los guardias.
  - **Linterna de dinamo** (túneles): un radio de luz que se reduce si no se pulsa.
- **Checkpoints:** si te ven, la escena se reinicia desde el último checkpoint y se aplica SOSPECHA +10 (o lo que dicte ink).
- **"Sigilo social" (J9):** sin conos ocultos. Hay que mantener la acción "leer carpeta" mientras se camina. Si te paras más de N segundos, el supervisor reacciona.

### 6.6 E · Contrarreloj y QTE

- **Temporizador visible:** el reloj de la pared o el de Ivy cuando lo lleva el protagonista.
- **Secuencias guionizadas:** obstáculos con una ventana de entrada cada uno (Sammy). Están **diseñadas para fallar**, pero cada obstáculo debe sentirse superable.
- **Arrastrar y soltar con tiempo** (esconder el diario).

### 6.7 F · Tablero de deducción

- Tarjetas con afirmaciones y evidencias del inventario o del registro.
- El jugador elige la afirmación que se queda el protagonista. Algunas afirmaciones solo se desbloquean con ciertas evidencias.

### 6.8 G · Resistencia

- **Medidores:** hambre, voluntad y respiración (polvo).
- **Interacción reducida:** las opciones son pocas y lentas, y a veces ninguna.
- **Opciones flotantes** (Habitación 101): varios botones se mueven sobre los escombros. Si se agota el tiempo, se elige uno por defecto.
- **Accesibilidad:** opción para reducir destellos y vibración en estas escenas (ver §9).

---

## 7. Interfaz (UIScene)

| Elemento | Comportamiento |
|---|---|
| **Caja de diálogo** | Abajo. Retrato del hablante a la izquierda. Texto con efecto de escritura (velocidad configurable). Tocar completa la línea; tocar otra vez avanza. |
| **Pensamiento** | Sin caja ni retrato: texto en cursiva semitransparente sobre la escena, en la parte superior. Con la Duda alta, el tono del texto se calienta. |
| **Telepantalla** | Texto verde con líneas de barrido y estática. |
| **Cartel** | Rótulo a pantalla completa sobre fondo negro, con fundido. |
| **Elecciones** | Lista vertical de opciones grandes (aptas para el dedo). Las decisiones ◆ llevan un pequeño ojo del Partido al lado. |
| **Inventario** | Tira inferior desplegable. Tocar un objeto lo "coge" (aparece en el cursor o junto al dedo) para `usar_con`. Mantener pulsado = mirar. |
| **Diario** | Libro a pantalla completa. Pestañas: *Entradas* (escritas), *Pistas* (automáticas), *Libro* (fragmentos de Goldstein). Solo se puede **escribir** en el ángulo muerto. |
| **Registro de diálogos** | Historial desplazable de todas las líneas con `id`. **Es un elemento jugable:** el doblepensar lo modifica. Las líneas aceptadas cambian; las recordadas aparecen tachadas. |
| **Indicador de Sospecha** | Un **ojo** en una esquina que se abre progresivamente: 0 = cerrado, 100 = abierto e inyectado en sangre. Sin números. |
| **Duda** | **Sin indicador visible.** Solo se nota en la paleta, en el tono del monólogo y en las opciones que aparecen. |
| **Menú de pausa** | Continuar · Diario · Registro · Opciones · Guardar y salir. |

### 7.1 Registro de diálogos y doblepensar

```ts
interface LogEntry {
  lineId: string;          // "j2_04_amory_01"
  speaker: string;         // "AMORY"
  text: string;            // texto ya renderizado
  original?: { speaker: string; text: string };  // si fue reescrita
  estado: 'normal' | 'reescrita' | 'tachada';
}
```

El doblepensar (`# dp:id=DP-J3-AMORY,lineas=j2_04_amory_*|j1_06_amory_*`):
1. Desplaza el registro hasta la primera línea afectada.
2. Anima el *glitch* (shader más sustitución letra a letra).
3. Muestra *Aceptar / Recordar*.
4. **Aceptar** → `estado = 'reescrita'` y el hablante pasa a "—". **Recordar** → `estado = 'tachada'`, se conserva el original y se marca la pista en el diario.
5. El registro forma parte de la partida guardada.

---

## 8. Controles

| Acción | Teclado | Mando | Móvil |
|---|---|---|---|
| Caminar | WASD / flechas | Stick o cruceta | **Joystick virtual** (mitad izquierda de la pantalla) **o** tocar el suelo |
| Ir a un objeto y usarlo | Clic izquierdo sobre él | — | Tocar el objeto |
| Acción (usar o hablar con lo que hay delante) | `E` / Espacio | A | Botón ✋ (abajo a la derecha) |
| Mirar | `Q` / clic derecho | B | Botón 👁 o mantener pulsado el objeto |
| Correr | Mantener `Shift` | Gatillo | Empujar el joystick al máximo |
| Avanzar diálogo | Espacio / Enter / clic | A | Toque en cualquier parte |
| Elegir opción | Flechas + Enter, teclas 1–5 o clic | Cruceta + A | Toque |
| Inventario | `I` | Y | Botón 🎒 |
| Usar objeto con… | Seleccionar en el inventario y luego acción frente al destino (o clic en el destino) | Igual | Seleccionar y tocar el destino |
| Diario | `J` | Select | Botón 📓 |
| Registro de diálogos | `L` | — | Deslizar hacia abajo desde el borde superior |
| Pausa | `Esc` | Start | Botón ☰ |
| Resaltar hotspots cercanos | `Tab` (mantener) | — | Botón 🔍 (resalta 2 s) |

> En móvil, los botones táctiles son semitransparentes y se colocan según la opción de mano dominante. En escritorio no se muestran.

### 8.1 Requisitos móviles

- **Orientación horizontal obligatoria**: en vertical aparece un aviso "Gira el dispositivo" con un icono de telepantalla.
- **Pantalla completa** al primer toque (Fullscreen API cuando el navegador lo permita; en iOS, la alternativa es instalar como PWA desde "Añadir a pantalla de inicio").
- **Zonas seguras** (`env(safe-area-inset-*)`): la UI no va bajo el *notch*.
- Bloquear el zoom del navegador, el *pull-to-refresh* y la selección de texto.
- Tamaño mínimo de objetivo táctil: **44 × 44 px CSS**. Los hotspots pequeños se amplían invisiblemente.
- **Audio:** desbloquear el `AudioContext` en el primer toque (pantalla de inicio "Toca para empezar").
- Objetivo de rendimiento: **60 fps** en un móvil de gama media de hace 4 años. Medir en un Android de gama baja real y en un iPhone con Safari.

---

## 9. Opciones y accesibilidad

| Opción | Valores |
|---|---|
| Velocidad del texto | Lenta · Normal · Rápida · Instantánea |
| Volumen | General · Música · Efectos · Ambiente |
| **Dificultad de crimen facial** | Normal · Asistida (ventanas amplias) · Automática (modo historia) |
| **Penalización de sigilo** | Normal · Reducida (Sospecha +5 en lugar de +10) |
| **Reducir destellos y vibración** | Sí / No. Afecta al dial, a los impactos, al *glitch* y a la Habitación 101. |
| Tamaño de la UI | 100 % · 125 % (fuente mayor, cajas más grandes) |
| Mano dominante (móvil) | Derecha / izquierda (para los botones de CF y del diario) |
| Aviso de contenido | Se muestra siempre al iniciar una partida nueva. |

---

## 10. Guardado

### 10.1 Qué se guarda

```ts
interface SaveData {
  version: number;            // esquema; para migraciones
  fecha: string;              // ISO
  ranura: 1 | 2 | 3 | 'auto';
  ink: string;                // story.state.toJson()
  mundo: {
    escena: string;           // id de la localización
    pos: { x: number; y: number };
    sigiloCheckpoint?: string;
  };
  registro: LogEntry[];
  opciones?: never;           // las opciones van en otra clave, no en la partida
  meta: { jornada: number; tiempoJugado: number; resumen: string };
}
```

- **Autoguardado** al empezar cada jornada (`# jornada:n`), al entrar en cada localización y en cada checkpoint de sigilo.
- **3 ranuras manuales** más la automática.
- **No se puede guardar** durante minijuegos ni en mitad de una conversación (se guarda el inicio del knot).
- **Desbloqueos globales** (finales vistos, galería de Capítulos II) en una clave aparte de `localStorage` que **no se borra** al empezar una partida nueva.

### 10.2 Robustez

- `localStorage` envuelto en `try/catch`: en modo privado o con el almacenamiento lleno, el juego avisa y sigue funcionando sin guardar.
- **Exportar partida:** descarga un `.json`. **Importar:** carga un `.json`. Sirve de copia de seguridad y para pasar la partida del ordenador al móvil.
- **Migraciones:** si cambia la `version`, se aplica una función de migración. Si el estado de ink no es compatible (por cambios en el guion), se ofrece reanudar desde el inicio de la última jornada guardada.

---

## 11. Herramientas de desarrollo y pruebas

### 11.1 Panel de depuración (solo en desarrollo, tecla `F1`)

- **Saltar a cualquier escena** (`J7.03`) con un estado prefabricado ("perfil curioso", "perfil fanático", "perfil arriesgado").
- **Editar variables** de ink en vivo (Duda, Sospecha, flags, inventario).
- Ver los **conos de visión**, las colisiones, la cuadrícula de pathfinding y los hotspots.
- Forzar el resultado de un minijuego (perfecto o fallo).
- Mostrar el `id` de cada línea en pantalla.

### 11.2 Pruebas automáticas

| Prueba | Qué comprueba |
|---|---|
| **Bot de recorrido de ink** (Node + inkjs) | Recorre la historia miles de veces con elecciones aleatorias y resultados de minijuegos aleatorios. Verifica que **se alcanzan los cinco finales más C0**, que no hay knots sin salida, que Duda y Sospecha se mantienen en 0–100 y que no hay errores de ink en tiempo de ejecución. |
| **Rutas dirigidas** | Perfiles fijos ("acepta todo", "recuerda todo", "denuncia a Amory", "salva a Len"…) que deben terminar en el final esperado. |
| **Linter de contenido** | Toda línea hablada tiene `# id:` único. No hay `{x\|y}` literal. Cada hotspot de Tiled apunta a un knot existente. Cada `# documento:`, `# minijuego:` o `# escena:` referencia algo que existe. Cada objeto del inventario tiene icono y descripción. |
| **Pruebas unitarias** (Vitest) | Puente narrativo, sistema de guardado, migraciones, validadores de minijuegos (compás, rutas). |
| **Pruebas de humo en navegador** | Arranque, menú, nueva partida y prólogo, en Chrome, Safari y Firefox (Playwright). |

---

## 12. Audio (técnico)

| Tipo | Formato | Carga |
|---|---|---|
| Música | `.ogg` + `.m4a` (Safari) | En *streaming*, por acto |
| Ambientes en bucle | `.ogg` + `.m4a` | Por localización |
| Efectos | `.ogg` + `.m4a`, o *audio sprite* | Precargados por acto |

- **Capas de ambiente:** zumbido de telepantalla, calle, pub, túnel… Cada localización define sus ambientes en Tiled.
- **Ducking:** la música baja automáticamente cuando habla la telepantalla o suena un silbido de cohete.
- **El silbido de cohete** es un evento de audio especial: se sintetiza en tiempo real con Web Audio (oscilador con barrido de tono más ruido) para que su duración se adapte exactamente a cada escena.
- **Leitmotivs:** *Naranjas y limones* (melodía tradicional de dominio público), himno del Partido (composición original) y la canción prole de Dot (composición original). La elección concreta de música y sonidos se hará en la biblia de audio.

---

## 13. Estructura del proyecto

```
1984/
├── docs/                          ← guion y diseño (ya existe)
├── content/
│   ├── ink/                       ← historia (ver §4.1)
│   ├── locations/                 ← mapas Tiled (.tmj) por localización
│   ├── documentos/                ← documentos del Partido (JSON)
│   ├── minijuegos/                ← configuraciones (CF, partes, mapas, sigilo…)
│   ├── items.json                 ← inventario: id, nombre, icono, descripción, comprometedor
│   └── i18n/                      ← tablas de texto de UI (es.json; en.json en el futuro)
├── assets/
│   ├── sprites/                   ← Aseprite (.aseprite) + exportados (.png + .json)
│   ├── backgrounds/
│   ├── portraits/
│   ├── ui/
│   ├── fonts/
│   ├── luts/
│   └── audio/{music,ambient,sfx}/
├── src/
│   ├── main.ts                    ← configuración de Phaser
│   ├── core/
│   │   ├── NarrativeBridge.ts
│   │   ├── GameDirector.ts
│   │   ├── SaveSystem.ts
│   │   ├── Settings.ts
│   │   └── i18n.ts
│   ├── scenes/
│   │   ├── BootScene.ts, PreloadScene.ts, MenuScene.ts
│   │   ├── LocationScene.ts
│   │   ├── UIScene.ts
│   │   └── minigames/
│   │       ├── FacecrimeScene.ts
│   │       ├── DocumentScene.ts
│   │       ├── MapToolScene.ts
│   │       ├── DeductionScene.ts
│   │       ├── QteScene.ts
│   │       └── EnduranceScene.ts
│   ├── systems/
│   │   ├── Movement.ts, Pathfinding.ts, Stealth.ts, VisionCone.ts
│   │   ├── VirtualJoystick.ts
│   │   ├── PaletteFx.ts            ← shader de Duda y glitch
│   │   ├── DialogueLog.ts
│   │   └── AudioDirector.ts
│   ├── ui/                        ← componentes de UI de Phaser
│   └── debug/                     ← panel F1
├── tools/
│   ├── vite-plugin-ink.ts
│   ├── lint-content.ts
│   └── ink-bot.ts                 ← recorrido automático
├── tests/
├── index.html
├── package.json
└── vite.config.ts
```

---

## 14. Internacionalización (inglés más adelante)

- **Fase 1:** solo español, escrito directamente en los `.ink`.
- **Preparación desde el primer día:**
  1. Toda línea de ink lleva `# id:`.
  2. Los textos de la UI van en `content/i18n/es.json`, nunca fijos en el código.
  3. Los documentos y objetos usan claves de texto.
- **Fase 2 (inglés):** un script extrae todas las líneas por `id` a un CSV o PO para traducir. En tiempo de ejecución, si el idioma es `en`, el puente **sustituye el texto de cada línea por su traducción según el `id`** y mantiene la lógica del `.ink` en español. En inglés no hay género gramatical en la mayoría de frases, así que las variables `{o}` y `{el}` se resuelven a cadenas neutras.
- Las fuentes elegidas deben cubrir también el inglés (no supone ningún problema).

---

## 15. Plan de desarrollo (hitos)

| Hito | Contenido | Criterio de "hecho" |
|---|---|---|
| **M0 · Esqueleto** ✅ | Proyecto Vite + Phaser + inkjs. Escalado de píxeles. Puente narrativo con un `.ink` de prueba. Caja de diálogo, elecciones y guardado básico. Panel de depuración mínimo. | Se puede jugar una conversación ramificada de prueba en escritorio y en móvil, guardar y cargar. |
| **M1 · Corte vertical** ✅ | **Prólogo + Jornada 1 completos:** escombros, ficha de afiliación, piso, escalera, calle, Minipax, cantina. Crimen facial (gimnasia y noticia). Minijuego de partes. Inventario. Arte provisional de calidad aceptable para 3 localizaciones. | Se juega de principio a fin en ~15 min, en escritorio y móvil, con audio. Sirve para validar tono, controles y legibilidad. |
| **M2 · Acto I** ✅ | J2 y J3: Dos Minutos de Odio (CF completo), mover el frente, decisión de Amory, doblepensar y registro de diálogos, pancarta y sueño. | Acto I jugable con todas sus ramas. Bot de ink sin errores. |
| **M3 · Acto II + Final A** | Registro de impactos (mapa y compás), Limehouse, Sammy (QTE), deducción, diario (escribir y esconder), comparador de documentos, inspección de Hilda, Nell. Final A. | Jugable hasta J7 con las tres ramas. |
| **M4 · Sistema de sigilo + Acto III** | Sigilo completo. Las tres misiones. Gran Rectificación. Expediente de Ivy. Lista de Len. Crane. Persecución. Final B. | Jugable hasta J12. |
| **M5 · Acto IV + finales** | Túneles (mapa de tres capas y cohetes), cripta, conversación, composición del Capítulo II, finales C, C0, D y E, créditos y desbloqueos. | Los cinco finales y C0 se alcanzan. Bot y rutas dirigidas en verde. |
| **M6 · Arte y audio finales** | Sustitución del arte provisional, música, ambientes y efectos. | — |
| **M7 · Pulido** | Equilibrio de Duda y Sospecha, accesibilidad, rendimiento móvil, PWA y pruebas con jugadores. | Partida completa sin bloqueos en Chrome, Safari iOS y Android. |

> **Sobre el arte:** el desarrollo puede avanzar con arte provisional (bloques de color con la paleta definitiva y siluetas). Por eso conviene hacer la **biblia visual** en paralelo a M0–M1.

---

### Estado de M0 (hecho)

- Vite 8 + Phaser 4.2 + inkjs 2.4 + TypeScript 7, con PWA (vite-plugin-pwa).
- Plugin de Vite que compila ink con `INCLUDE` y recarga en caliente.
- Puente narrativo (`src/core/NarrativeBridge.ts`), lector de etiquetas y de líneas, lector de mapas de Tiled y guardado automático.
- Escena de exploración cenital: movimiento directo y por toque o clic (A*), colisiones por los pies, foco de objetos, mirar/usar y *y-sort*.
- Interfaz: diálogo con máquina de escribir, pensamientos, telepantalla, carteles, elecciones, ojo de la Sospecha y depuración (F1).
- Piso de la Jornada 1 jugable con sus puntos interactivos en ink.
- 17 pruebas: compilación de ink, regla `{x|y}`, ids de línea únicos, rutas de los hotspots, colisiones y estado.

**Pendiente para M1:** joystick virtual y botones táctiles, Ficha de Afiliación, crimen facial, minijuego de partes, escalera, calle y Minipax.

### Estado de M1 (hecho)

- **Prólogo + Jornada 1 jugables de principio a fin**, en 9 escenarios: calle Stepney (dos variantes), piso (día y noche), escalera, avenida (con cámara que sigue al jugador), vestíbulo del Minipax, Departamento de Partes y Cartografía y cantina.
- **Minijuegos:** escombros, Ficha de Afiliación (con campos de texto reales), crimen facial (ritmo con retratos y máscara agrietada) y parte de guerra (documento con huecos).
- **Sistemas:** acciones bloqueantes desde ink (minijuegos, pausas, efectos de pantalla, sonidos en secuencia), transiciones entre escenarios con punto de aparición, personajes no jugables con diálogo, objetos y colisiones condicionales, zonas automáticas, inventario, sonidos sintetizados con Web Audio y controles táctiles (botones y joystick).
- **Arte:** protagonista H y M en 4 direcciones con animación de caminar, 14 personajes no jugables, 14 retratos de crimen facial, iconos e ilustraciones.
- **40 pruebas**, entre ellas las que simulan resultados de minijuegos y verifican que cambian la historia, y las que comprueban que cada transición apunta a un mapa y a un punto de aparición existentes.
- **Atajos de depuración** en la consola del navegador (solo en desarrollo): `saltar('escena', 'knot', { variables })`.

### Estado de M2 (Acto I completo)

- **Jornada 2 jugable de principio a fin:** mañana en el piso, Parsons en la escalera, Dos Minutos de Odio, mover el frente, reacción ante Amory (tres ramas, una lleva al despacho de Voss), Centro Comunitario y sueño con Ivy. El sueño lleva a la Jornada 3.
- **4 escenarios nuevos:** salón del Odio, despacho de Voss, Centro Comunitario y sueño (este último con cámara que sigue al jugador).
- **Minijuegos nuevos:**
  - Crimen facial de los Dos Minutos de Odio, definido por datos (`content/cf/`) y con cuatro fases que cambian de pantalla y de ritmo.
  - Mover el frente: arrastrar banderas a sus destinos.
  - Pintar la pancarta: trazos interpolados, que puntúan la cobertura y el derrame.
- **Sistemas:**
  - Personajes que huyen del jugador (Ivy en el sueño).
  - Resultados de minijuego guardados en una variable de ink (`resultado=var`).
  - Nuevos sonidos sintetizados: «Naranjas y limones» en piano desafinado y el chirrido de la telepantalla.
- **Pulido:**
  - Durante el Odio, Amory se ve de reojo: si el jugador lo mira (tecla A o tocándolo) en el clímax, le ve callarse un segundo para limpiarse las gafas (`cf_j2_odio_amory`).
  - El piano toca «Oranges and Lemons» transcrita nota a nota, con cuerdas desafinadas y bajo.
  - Caminar con zancada, balanceo de brazos y rebote. Al correr, la animación se acelera.
  - Joystick con zona muerta y centro que sigue al dedo. No se queda andando solo con un segundo dedo, al salir de la pantalla ni al pasar la app a segundo plano.
- **Jornada 3 jugable de principio a fin**, que cierra el Acto I: la mesa vacía (Pell y Brooke), el archivador del personal, el despacho de Voss, el doblepensar, el lápiz y el agujero de la memoria, el pasillo con la limpiadora que desaparece y el monólogo final según el estado. Termina en «FIN DEL ACTO I» y vuelve al menú.
- **Registro de diálogos** (`src/core/Registro.ts`, `RegistroScene`): anota cada línea con id, se consulta con `L` o el botón REG. y se guarda con la partida.
- **Doblepensar** (`# dp:id=…`, configurado en `content/doblepensar/`): el registro se desplaza solo, los nombres se deshacen y el jugador decide. Aceptar los borra («—»), también en lo que se anote después. Recordar los tacha.
- **Usar con:** en el inventario, MIRAR (con knot de ink si el texto depende de la historia) y USAR CON… El objeto queda en la mano hasta usarlo en un hotspot con la propiedad `con`.
- **Mapas:**
  - Fondo alternativo por condición (`fondo_alt`, `fondo_alt_si`). El departamento cambia cuando Amory deja de existir.
  - Luces de neón que fallan (`parpadeo`).
  - Comando `prota:dir` para girar al protagonista.
- **Nuevos personajes y escenarios:** Pell, Brooke, el pasillo de la planta 14 y la variante del departamento.
- **74 pruebas**, con todas las ramas de la Jornada 3 y el registro.

**Pendiente:**
- Probar el joystick en un móvil real.
- Pulir el arte provisional del pasillo.
- La música y los ambientes llegan en M6.

---

## 16. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| **Volumen de arte** (unas 40 localizaciones y 20 personajes con retrato) | Reutilizar escenarios (el piso, el Minipax y la escalera aparecen en casi todas las jornadas). Variantes de color y atrezo en lugar de escenarios nuevos. Montajes con viñetas fijas en lugar de escenas animadas. |
| **Legibilidad del texto en móvil** | Resolución de UI a 960×540, opción de UI al 125 % y pruebas tempranas en M1 con un móvil real. |
| **Safari en iOS** (audio, pantalla completa, rendimiento WebGL) | Probar en iOS desde M0. Desbloqueo de audio en el primer toque. PWA para pantalla completa. Respaldo en Canvas sin shader. |
| **Explosión combinatoria de ramas** | Muchas variables solo cambian líneas, no escenas. El bot de ink verifica todas las combinaciones relevantes. |
| **Cambios de guion que rompen partidas guardadas** | Guardado por inicio de knot y migraciones con la opción de reanudar desde el inicio de la jornada. |
| **Contenido explícito** | Aviso de contenido, opción de reducir destellos y escenas de violencia resueltas con fuera de campo sonoro y sprites, no con gore detallado de pixel art. Es igual de duro y más fácil de producir. |

---

## 17. Decisiones confirmadas

1. **Tecnología:** Phaser + TypeScript + ink. Confirmado.
2. **PWA:** el juego será instalable (manifest y service worker) y jugable sin conexión. En iPhone es la forma de tener pantalla completa.
3. **Versionado:** repositorio git inicializado en la raíz del proyecto.
4. **Arte:** lo produce Claude **mediante código** (escenarios con primitivas, iluminación y tramado sobre la paleta; personajes y retratos como rejillas de píxeles escritas a mano). Pipeline en `art/`. Ver la prueba en `art/pruebas/`.
