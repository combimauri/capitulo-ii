# ACTO IV — CAPÍTULO II

> Jornada 13 + decisión final · Duración estimada: ~30 min (más el final elegido)
> Objetivo narrativo: el **sentido**. Todo lo que el jugador ha visto, recordado y escrito se convierte en un texto. Después, el juego le pregunta qué hace con él.
> Notación: ver [00-convenciones.md](00-convenciones.md). Finales: ver [05-finales.md](05-finales.md).

**Estado al entrar:** el protagonista ha pasado la noche en la despensa de Dot. Tiene los dibujos de Amory y el mensaje de Nell.

---

## JORNADA 13 — Bajo las campanas

### J13.00 — Comprobación de entrada

**Si `duda < 30`** (posible si el jugador aceptó el doblepensar de J11 y casi todos los demás):

(Amanecer. El protagonista sale de la despensa sin hacer ruido. Dot duerme en una silla junto a la estufa. El protagonista mira los dibujos de Amory, el mensaje de Nell y la colección de metralla de Sammy. Luego deja el paquete sobre la mesa, abre la puerta y camina hacia la calle Cable.)

PENSAMIENTO: Un día, dijo Crane. (Pausa.) Quiero que me devuelvan mi cansancio. Quiero que todo vuelva a estar en su sitio.

→ **FINAL B — versión "arrepentimiento"** (ver [05-finales.md](05-finales.md#final-b--el-fotógrafo))

**Si `duda >= 30`:** → J13.01

### J13.01 — Estación de Shadwell · Amanecer

**Localización:** boca de metro tapiada con tablones. Un cartel descolorido: *CERRADO POR REFORMAS — MINISTERIO DE LA ABUNDANCIA*. Pintadas de Espías: *¡MUERTE A ESTASIA!* (con *EURASIA* tachado debajo). Niebla del río.

(Dot acompaña al protagonista hasta la esquina. No se despiden. Dot le aprieta el brazo una vez y se va.)

**Si `crane_sigue`:**

(Al final de la calle, junto a una farola apagada, un sombrero. No se mueve.)

PENSAMIENTO: Sigue ahí. Toda la noche. (Pausa.) Si entro, me seguirá. Si no entro…

- **[Tablones]** → MIRAR → PENSAMIENTO: Clavos nuevos. Pero el tercer tablón… (En el dibujo de Amory, un pájaro diminuto posado justo en esa esquina de la entrada.) El pájaro está aquí.
- **[Tablones]** → USAR → (El tercer tablón gira sobre un solo clavo. Hueco suficiente para pasar.)

→ J13.02

### J13.02 — Los túneles · Navegación

**Localización:** túneles del metro cerrado. Oscuridad casi total, rota por la luz de una linterna de dinamo (hay que tocar repetidamente para mantenerla cargada: un ritmo suave que el jugador interioriza). Raíles oxidados, agua por los tobillos, carteles de estaciones de antes de la Revolución con nombres que el protagonista nunca ha oído. Ratas. Goteo constante.

> **Nota de dirección:** paleta subterránea. Negro, el cono ámbar de la linterna y un verde muy oscuro en el agua. El sonido de la ciudad llega amortiguado desde arriba.

#### Mecánica: EL MAPA DE LOS PÁJAROS

El inventario se convierte en una pantalla de mapa compuesta por **tres capas superponibles**, que el jugador ha ido reuniendo a lo largo del juego:

| Capa | Origen | Qué muestra |
|---|---|---|
| **Dibujos de Amory** | J12.08 | Túneles, estaciones tapiadas y pozos. **Pájaros** = salidas o ventilación. **Pájaros con las alas cerradas** = derrumbes. |
| **Lámina de zonificación** | J4 / J5 | Distritos del Partido (gris) y proles (pardo). Los cuatro ministerios. |
| **Compás** | J4 | Círculos de 2 km alrededor de cada ministerio. |

**El acertijo central.** El mensaje de Nell dice: *"Los cohetes no caen donde no quieren que caigan."* La Planilla Azul decía: *"Excluir radio 2 km de edificios ministeriales."*

Al superponer las tres capas, el jugador ve que **San Clemente**, una iglesia en ruinas en el Strand marcada en el mapa de Amory con un pájaro **dorado** (el único), está **dentro del círculo de exclusión del Ministerio de la Verdad**.

PENSAMIENTO (al descubrirlo):
- El único sitio de Londres donde no cae nunca un cohete. (Pausa.) Escondido a la sombra del Miniver. El viejo vive en el único lugar que el Partido protege.
- `[D2]` (Pausa.) ¿O es que el Partido le protege a él?

⟶ `FLAG san_clemente_deducido = true` *(si el jugador se atasca más de 2 minutos, el protagonista lo deduce solo al tercer intento)*

**Ruta:** de Shadwell a San Clemente en 5 tramos. El jugador elige el camino en el mapa entre bifurcaciones, evitando los derrumbes (pájaros con las alas cerradas).

#### Tramo 1 · Shadwell → Aldgate Este · *El cohete*

(A mitad del túnel, un silbido. Arriba. Cada vez más agudo.)

PENSAMIENTO: Arriba. Están bombardeando arriba. Whitechapel, la cuadrícula I-7. (Pausa.) Lo habría registrado yo mañana por la mañana.

**Mecánica:** cuando suena el silbido, el jugador tiene 3 segundos para meterse en un **nicho de seguridad** de la pared del túnel (están marcados con una franja blanca descolorida). Impacto: el túnel tiembla, cae polvo y cascotes donde estaba el protagonista. Hay dos silbidos en este tramo.

- **Si `reloj_en_marcha`:** el reloj de Ivy aparece en una esquina de la pantalla. Los impactos llegan a las horas exactas que el protagonista "sabe" por el patrón de la semana (05:10 y 05:18), y el jugador puede anticiparse.
- **Si no:** el silbido es el único aviso.
- **Ser alcanzado:** pantalla en blanco y reinicio del tramo. **Sin penalización de Sospecha** (aquí abajo no hay telepantallas). Es la primera vez en todo el juego en que el jugador no está siendo vigilado.

PENSAMIENTO (tras el segundo impacto):
- Ahí arriba alguien acaba de perder la casa. Mañana yo habría escrito "estasiático" en el libro.

#### Tramo 2 · Aldgate → Liverpool Street · *El taller*

**Localización:** andén de una estación tapiada. Velas consumidas. Una mesa de trabajo con herramientas. **Una docena de telepantallas desmontadas**, apiladas contra la pared, con cables al aire. Etiquetas a mano en cada una.

- **[Telepantallas desmontadas]** → MIRAR → (Primer plano de las etiquetas: *"Minimor, pasillo 9"* · *"Bloque 4, Southwark"* · ***"Minipax, planta 14, suministros"***.)
  PENSAMIENTO: El cuarto de suministros. El hueco tapado con una tabla. (Pausa.) No la quitaron ellos. La quitamos nosotros.
  ⟶ *(Semilla de J7 resuelta.)*
- **[Mesa de trabajo]** → MIRAR → (Un mono de trabajo con el distintivo *SERVICIO TÉCNICO DE TELEPANTALLAS · MINISTERIO DE LA VERDAD*. En el bolsillo, una tarjeta: *"T. Barlow"*.)
  PENSAMIENTO: Barlow. El tabernero. Entraba en los ministerios a "reparar" telepantallas. Y las arreglaba para que no vieran. (Pausa.) Barlow está en el Minimor.
- **[Pared]** → MIRAR → (Escrito con tiza, con letras de distintas manos, decenas de nombres. Algunos tachados. Entre ellos: ***Ivy***. Y debajo, con otra letra: ***Felix A. (sin saberlo)***.)
  PENSAMIENTO: Ivy. Escrito con tiza, en un andén donde no pasa ningún tren. (Pausa.) Es más que un cartel.
  ⟶ DUDA +5

#### Tramo 3 · Liverpool Street → Bank · *Crane* *(solo si `crane_sigue`)*

(Detrás, a lo lejos, el chapoteo de unos pasos en el agua. Una luz que no es la del protagonista.)

PENSAMIENTO: Me ha seguido. Está aquí abajo.

**Mecánica: despistar a Crane.** Persecución lenta y tensa, no frenética: Crane camina, no corre. El jugador tiene tres opciones según el mapa:

| Opción | Cómo | Resultado |
|---|---|---|
| **El derrumbe** | Llevar a Crane hasta un tramo marcado con un pájaro de alas cerradas, cruzarlo por un hueco estrecho y **golpear un puntal podrido** (USAR). El techo cede detrás. | ⟶ `crane_perdido = true`. Se oye a Crane toser al otro lado. CRANE (amortiguado, sin perder la calma): "Hay más túneles, camarada. Siempre hay más túneles." |
| **Apagar la linterna** | Dejar de cargar la dinamo y avanzar a oscuras guiándose por el sonido del agua y el tacto de la pared (pantalla negra con siluetas tenues). | ⟶ `crane_perdido = true` si el jugador llega al final sin chocar con nada más de 3 veces. Si choca, Crane le alcanza y se aplica el resultado "No perderlo". |
| **No perderlo** | Seguir sin más. | ⟶ `crane_perdido = false` · Crane le seguirá hasta la cripta (ver J13.07). |

#### Tramo 4 · Bank → Temple · *Los nombres*

**Localización:** túnel largo y seco. En las paredes, **carteles de antes de la Revolución**, medio despegados: anuncios de cosas que el protagonista no reconoce (un té, un teatro, una playa). Un cartel tiene a una niña sonriendo con un helado.

- **[Cartel de la niña]** → MIRAR →
  PENSAMIENTO: Una niña sonriendo. Con los dientes. (Pausa.) Ivy sonreía así. (Pausa.) Antes, alguien hacía carteles de gente sonriendo sin motivo.
- **[Plano de la red de metro (antiguo)]** → MIRAR → PENSAMIENTO: Cientos de estaciones. Toda una ciudad debajo de la ciudad. Y nadie la recuerda. (Pausa.) Amory la recordaba. La dibujó entera para que alguien la recordara.

#### Tramo 5 · Temple → San Clemente · *Las campanas*

(Una escalera de caracol de hierro sube desde un pozo de ventilación. Al subir, se oye algo que el protagonista nunca ha oído: el **silencio** de un lugar cerrado y antiguo. Y, muy débil, alguien teclea en una máquina de escribir.)

PENSAMIENTO: (casi sin voz) Naranjas y limones, dicen las campanas de San Clemente.

(Desde arriba, una voz de anciano, ronca, termina la canción.)

VOZ: *…me debes tres peniques, dicen las campanas de San Martín.* (Tos.) Sube. Llevo dos días con el té preparado. Ya estará frío.

### J13.03 — La cripta de San Clemente

**Localización:** cripta bajo una iglesia bombardeada hace treinta años. Bóvedas de piedra ennegrecida, lápidas en el suelo con nombres borrados. Velas en todas partes. Estanterías hechas con tablones y ladrillos, **llenas de libros**: libros de verdad, viejos, prohibidos. Montones de papel. Una mesa con una **máquina de escribir** antigua. Un camastro. En el centro, una **estructura de madera para campanas vacía**, con un solo gancho de hierro.

(La paleta más cálida de todo el juego: el ámbar de las velas, el marrón de la madera y el rojo apagado de los lomos de los libros. No es la paleta del Partido ni la de los proles: es otra.)

(Junto a la máquina de escribir, un anciano muy delgado, con una manta sobre los hombros, el pelo blanco y largo, perilla blanca y gafas remendadas con hilo. Es la cara de los Dos Minutos de Odio, pero treinta años más vieja, más pequeña y **más humana**: **Emmanuel Goldstein**.)

(La primera reacción del protagonista es física: un **crimen facial involuntario**.)

#### CF-J13-GOLDSTEIN · `CF[Odio, automático]`

(El jugador **no controla** este CF. La cara del protagonista se crispa sola durante 2 segundos y el puño se cierra. Un eco de los Dos Minutos de Odio suena distorsionado. Luego se relaja.)

PENSAMIENTO: Mi cara. Mi cara le odia sola. Cinco años de entrenamiento. (Pausa.) Es un viejo con una manta.

GOLDSTEIN: (sin ofenderse, sirviendo té en dos tazas desportilladas) Lo sé. A todos os pasa. (Sonríe.) La primera vez que alguien de la Hermandad me trajo un espejo, a mí también me pasó.

**Si `crane_sigue` y no `crane_perdido`:** (El protagonista mira hacia la escalera.) PROTAGONISTA: Me han seguido. Un hombre. Crane. Debe de estar cerca. GOLDSTEIN: (sin alterarse) Lo sé. Siempre viene alguien detrás. Siéntate. Tenemos un rato.

### J13.04 — La conversación

**Mecánica:** árbol de diálogo libre. Los temas se desbloquean según lo que el protagonista sabe. El jugador puede recorrerlos todos o ir directamente al tema final (*"El capítulo"*). Cada tema dura entre 1 y 2 minutos.

#### Tema: "¿Usted existe de verdad?"

GOLDSTEIN: (ríe, y la risa se convierte en tos) Eso me pregunto yo cada mañana. (Pausa.) Existo lo bastante para toser. Para escribir. Para que me odien dos minutos al día en todos los ministerios de Oceanía. (Pausa.) No sé si existo lo bastante para importar.

#### Tema: "La guerra" *(si `planilla_vista`)*

PROTAGONISTA: He visto la Planilla Azul. Folkestone. Kent.

GOLDSTEIN: Entonces ya sabes más de lo que sabía yo cuando escribí el capítulo tercero. (Pausa.) Yo intuía que la guerra era un teatro. No sabía que el Partido había empezado a poner las bombas en el patio de butacas.

PROTAGONISTA: ¿Y Eurasia? ¿Y Estasia?

GOLDSTEIN: Existen. Tienen sus propios partidos, sus propios Grandes Hermanos con otras caras. Sus propios mercados bombardeados, supongo. (Pausa.) Los tres se necesitan como se necesitan las piedras de una bóveda. Si una cae, caen todas.

#### Tema: "Ivy" *(si `ivy_revelada`)*

PROTAGONISTA: Mi hermana. Ivy {APELLIDO}. Era de la Hermandad.

GOLDSTEIN: (deja la taza; se quita las gafas; tarda en hablar) La recuerdo. Nunca la vi, pero la recuerdo. Nell me traía sus cartas. Escribía muy deprisa, con faltas de ortografía. Siempre con prisa. (Pausa.) Estaba escribiendo algo para mí. Para el libro.

PROTAGONISTA: ¿Qué?

GOLDSTEIN: El capítulo que yo no sé escribir.

(Silencio.)

PROTAGONISTA: Los documentos. La Policía del Pensamiento se llevó documentos de casa aquella noche.

GOLDSTEIN: Tres páginas. Me había mandado la primera frase en una carta, la semana anterior. Para ver si me gustaba. (Busca entre sus papeles con manos temblorosas. Saca un trozo de papel cuadriculado, arrancado de un cuaderno escolar, doblado muchas veces.) Me gustó.

(Primer plano del papel. Letra rápida, inclinada, con una falta de ortografía.)

> *"Nos dijeron que la libertad es la esclavitud. Nadie nos dijo que la esclavitud también puede ser un hogar, y que por eso es tan dificil salir de ella."*
> — I.

PENSAMIENTO: Su letra. "Dificil" sin tilde. Siempre se le olvidaba. (Pausa larga.) Ivy.

⟶ DUDA +10 · ITEM +item_carta_ivy · `FLAG carta_ivy = true`

**Si `dp_j11_ivy = "aceptar"`:** PENSAMIENTO: (el glitch del doblepensar tiembla sobre la carta y la palabra "TRAIDORA" aparece superpuesta un instante; luego se deshace) Traidora. (Pausa.) Su letra. (Pausa.) No puedo. No puedo sostener las dos cosas.
⟶ `dp_j11_ivy = "roto"` *(el doblepensar de J11 queda anulado: a efectos de los finales, cuenta como "recordar")*

#### Tema: "Los proles"

GOLDSTEIN: Escribí que la esperanza está en los proles. Lo sigo creyendo. Pero no como lo escribí. (Pausa.) Creía que un día se despertarían todos a la vez, como un gigante. No será así. Será una mujer que esconde a alguien en una despensa. Un niño que guarda metralla. Un tabernero que arregla telepantallas para que no vean. (Pausa.) Mil puertas que se abren, una a una. Es más lento. Es lo único que el Partido no sabe vigilar.

*(Si `dot_confianza >= 2`:)* GOLDSTEIN: Tú ya lo has visto. Te han abierto puertas.

#### Tema: "La Hermandad"

PROTAGONISTA: ¿Cuántos somos?

GOLDSTEIN: No lo sé. (Pausa.) De verdad que no lo sé. Puede que mil. Puede que treinta. Puede que la Hermandad sea, sobre todo, la idea de que existe. (Pausa.) Eso también es útil. Para nosotros. Y para ellos.

#### Tema: "Amory" *(si `item_dibujos_amory`)*

GOLDSTEIN: El de los pájaros. (Sonríe.) Nell me trajo copias. Ese muchacho dibujó la red entera, estación por estación, de memoria y por intuición, mirando los planos de alcantarillado del Minipax. Nunca supo que dibujaba para nosotros. (Pausa.) Dibujaba porque no soportaba que algo existiera y nadie lo supiera. Esa es, al final, la única rebeldía.

**Si `amory_reaccion = "denuncia"`:** PROTAGONISTA: Yo le denuncié. GOLDSTEIN: (le mira largo) Lo sé. Nell me lo dijo. (Pausa.) Y aquí estás, con sus dibujos en la mano. No sé qué significa eso. Pero significa algo.

#### Tema: "¿Por qué sigue vivo?" *(siempre disponible; es el tema más inquietante)*

PROTAGONISTA: Está a la sombra del Miniver. En el único sitio donde no cae ningún cohete. ¿De verdad no saben que está aquí?

GOLDSTEIN: (tarda mucho en contestar; mira la estructura vacía de las campanas) Me lo pregunto cada noche. (Pausa.) Hay dos respuestas. O soy más listo que el Partido, cosa que dudo. O el Partido necesita que yo exista, y que escriba, y que tosa, y que de vez en cuando alguien como tú baje por esa escalera. (Pausa.) No sé cuál es peor.

PROTAGONISTA: ¿Y qué hace con eso?

GOLDSTEIN: Escribir. Igual. (Se encoge de hombros.) Si es una jaula, es la única jaula de Oceanía donde se puede escribir la verdad. Prefiero esta.

⟶ `FLAG pregunta_jaula = true`

#### Tema: "El capítulo" *(tema final; cierra la conversación)*

→ J13.05

### J13.05 — El Capítulo II

GOLDSTEIN: (pone una mano sobre el fajo de papeles mecanografiados) *Teoría y práctica del colectivismo oligárquico*. Capítulo primero: la ignorancia es la fuerza. Capítulo tercero: la guerra es la paz. (Pausa.) Y en medio, nada. Treinta años sin el capítulo segundo.

PROTAGONISTA: La libertad es la esclavitud.

GOLDSTEIN: Lo he intentado cien veces. Siempre me sale un tratado. Explico por qué el individuo solo es débil y el Partido es inmortal, por qué rendirse al Partido parece una forma de no morir… y es mentira, porque nunca lo he sentido. (Pausa.) Yo nunca creí. Nunca grité en los Dos Minutos de verdad. Nunca lloré delante de un cartel.

(Mira al protagonista.)

GOLDSTEIN: Tú sí. (Pausa.) Solo quien ha creído puede explicar qué se entrega al creer. Y por qué cuesta tanto devolverlo.

*(Si `carta_ivy`:)* GOLDSTEIN: Tu hermana empezó. Termínalo tú.

GOLDSTEIN: (señala el diario que asoma del bolsillo del protagonista) Nell me dijo que escribías. Empieza por ahí.

#### Mecánica: COMPOSICIÓN DEL CAPÍTULO II

**Herramienta de escritura:**
- Si conserva el lápiz de Amory (`lapiz_destruido = false`): el protagonista saca el lápiz mordido. GOLDSTEIN: "Ese lápiz ha sufrido." PROTAGONISTA: "Era de un amigo." Se escribe con él.
- Si no: GOLDSTEIN le presta uno. "Toma. Los lápices aquí abajo no son de nadie."

**Estructura:** el capítulo tiene **cinco movimientos**. En cada uno, el juego muestra las **entradas del diario** que el jugador ha escrito y que encajan en ese tema. El jugador elige **una** (con la frase concreta que eligió al escribirla). Si no tiene ninguna entrada para un movimiento, se usa una **frase por defecto** que Goldstein le dicta, y en el texto final queda en cursiva: es la voz de Goldstein, no la suya.

| Movimiento | Título | Entradas compatibles | Por defecto (voz de Goldstein) |
|---|---|---|---|
| **I** | *Lo que se entrega* | `diario_ivy`, `diario_ivy_verdad`, `diario_times` | *"El creyente entrega su memoria a cambio de no tener miedo."* |
| **II** | *El odio como alimento* | `diario_sammy`, `diario_cohetes`, `diario_planilla`, `diario_libro_guerra` | *"El Partido da de comer odio a quien tiene hambre de sentido."* |
| **III** | *El pasado redactado* | `diario_amory`, `diario_parte`, `diario_chocolate`, `diario_estasia`, `diario_amory_confesion`, `diario_libro_pasado`, `diario_libro_doblepensar` | *"Lo que no se recuerda no se puede echar de menos."* |
| **IV** | *Los de abajo* | `diario_dot`, `diario_nell`, `diario_len`, `diario_libro_ignorancia` | *"Nadie mira a quien limpia. Por eso quien limpia lo ve todo."* |
| **V** | *La libertad* | *(ver cierre abajo)* | — |

**Apertura (fija, siempre):**
- Si `carta_ivy`: el capítulo empieza con la frase de Ivy, **con su falta de ortografía**. El jugador puede corregirla o no (◆ pequeña decisión: tocar la palabra "dificil" para añadir la tilde). Si la corrige: GOLDSTEIN: "Ella no la habría corregido." Si no la corrige: GOLDSTEIN: "Bien."
- Si no: el capítulo empieza con *"Capítulo II — La libertad es la esclavitud."* y nada más.

**Conectores:** entre cada movimiento, el juego inserta una frase de enlace escrita por el protagonista, que depende del **tramo de Duda** y de la decisión de J11:

| Condición | Tono de los conectores (ejemplo) |
|---|---|
| `duda >= 70` y `dp_j11_ivy` ∈ {recordar, roto} | Lúcido, directo: *"Esto lo vi yo. No me lo contó nadie."* |
| `duda` 30–69 | Dubitativo: *"No sé si esto prueba algo. Sé que ocurrió."* |
| `dp_j11_ivy = "aceptar"` (no roto) | Quebrado: *"Escribo esto y no sé si lo creo. Lo escribo igual."* |

**Movimiento V — el cierre.** El jugador elige la última frase del capítulo entre las disponibles:

| Frase de cierre | Disponible si |
|---|---|
| *"La libertad no es un lugar. Es un reloj que alguien decide volver a poner en marcha."* | `reloj_en_marcha` |
| *"Fui libre catorce días. Lo bastante para saber exactamente lo que me van a quitar."* | siempre |
| *"No sé si la libertad existe. Sé que la esclavitud tenía la cara de mi hermana, y que me hacía sentir en casa."* | `carta_ivy` |
| *"Un niño coleccionaba metralla para que nunca le cayera un cohete. Eso era la fe. Esto es otra cosa."* | `sammy_intento` o `item_metralla_brillante` |
| *"Elegí quién moría con una máquina de escribir. Ya no puedo decir que no soy uno de ellos. Puedo decir que lo sé."* | `len_salvado` |

**Resultado:** el capítulo completo aparece en pantalla, **mecanografiado en directo por Goldstein** en la máquina de escribir, línea a línea, con el sonido de las teclas. El texto es único para cada partida.

⟶ `FLAG capitulo_ii = [apertura, mov1, mov2, mov3, mov4, cierre]` · ITEM item_libro (completo: 5/5)

**Variante si `lapiz_destruido`:** el movimiento III, si usa `diario_amory`, añade automáticamente una frase al final: *"Tiré su lápiz al fuego. Me pareció lo higiénico."*

(Goldstein termina de teclear. Saca la hoja. Cose las páginas del capítulo con hilo, en medio del fajo, entre el primero y el tercero. Se queda mirando el libro entero en sus manos.)

GOLDSTEIN: (muy bajo) Treinta años. (Pausa.) Ahora está entero. (Le mira.) Y ahora es peligroso de verdad.

### J13.06 — Copias

GOLDSTEIN: Hay dos copias. (Saca un segundo fajo, idéntico, de debajo del camastro.) Siempre hago dos. Una se queda aquí, conmigo. La otra tiene que salir.

PROTAGONISTA: ¿Adónde?

GOLDSTEIN: Adonde no la busquen. A una cocina. A una despensa. (Pausa.) A los de abajo.

(Pone la copia sobre la mesa, entre los dos.)

GOLDSTEIN: Si sales con ella, te cogerán. No hoy, quizá. Pero te cogerán. Tu cara está en el expediente de Voss desde hace cinco años. (Pausa.) Si te quedas, puedes quedarte. Hay sitio. Hay libros. Hay té, aunque siempre está frío. (Sonríe.) Y nadie te buscará aquí. Nunca buscan aquí.

PENSAMIENTO: "Nunca buscan aquí."

### J13.07 — Crane en la cripta *(solo si `crane_sigue` y no `crane_perdido`)*

(Pasos en la escalera de caracol. Lentos. **Crane** aparece en la entrada de la cripta, empapado hasta las rodillas, con el sombrero en la mano y una pistola en la otra. Sonríe.)

CRANE: Qué sitio tan… acogedor. (Mira los libros.) Cuánto papel. (Mira a Goldstein.) Y usted debe de ser el viejo. (Pausa.) Le hacía más alto. En las pantallas parece más alto.

GOLDSTEIN: (sin levantarse, sirviéndose más té) Todos me dicen lo mismo.

CRANE: Queda usted detenido. Los dos.

GOLDSTEIN: (sorbe el té) Antes de hacer nada, hijo, pregunte a sus superiores. (Señala con la taza un rincón de la cripta: un **teléfono de campaña** del Partido, verde y polvoriento, conectado a un cable que sube por la pared.) Esa línea funciona. Siempre ha funcionado. Nunca la he usado.

(Crane mira el teléfono. Duda por primera vez en todo el juego. Sin dejar de apuntar, va hasta él, descuelga y marca.)

CRANE: (al teléfono) Aquí Crane, distrito Este. Estoy en… (se lo piensa) …San Clemente. Tengo al viejo. (Pausa larga. Escucha.) …Sí. (Pausa.) Sí, señor. (Pausa.) Pero… (Pausa.) Entendido, señor.

(Cuelga despacio. Se le ha borrado la sonrisa. Por primera vez parece lo que es: un funcionario.)

CRANE: (a Goldstein, sin mirarle) Usted no está aquí. (Pausa.) Usted nunca ha estado aquí. (Al protagonista, con rabia contenida:) Usted sí.

⟶ `FLAG crane_humillado = true`

> **Voz al otro lado del teléfono:** el jugador no la oye. En el Final E, cuando O'Brien habla, el jugador atento reconocerá en la puesta en escena que era él.

**Consecuencia:** con Crane presente, **la decisión final cambia** (ver tabla en J13.08). Crane espera en la escalera. No dejará salir al protagonista sin escolta, pero no tocará a Goldstein ni la copia que se queda en la cripta.

PENSAMIENTO: "Pregunte a sus superiores." (Mira a Goldstein.) Lo sabían. Siempre lo han sabido.

GOLDSTEIN: (en voz baja, solo para el protagonista) Ahora ya sabes cuál de las dos respuestas era. (Pausa.) No cambia nada. El libro sigue siendo verdad.

### J13.08 — La decisión final

(Goldstein empuja la segunda copia hacia el protagonista. La vela parpadea. Arriba, muy lejos, un silbido de cohete que no cae aquí. Nunca cae aquí.)

#### ◆ D-J13-FINAL

**Si Crane no está en la cripta:**

| Opción | Texto | Resultado |
|---|---|---|
| **Sacar el libro** | (Coge la copia. La mete bajo el mono, contra el pecho.) "Se lo llevaré a los de abajo." | → **FINAL D — "Capítulo II"** |
| **Quedarse** | (Deja la copia en la mesa. Se sienta.) "¿Queda té?" | → **FINAL E — "El nuevo Goldstein"** |
| **Entregar a Goldstein** *(solo si `crane_decision = "fingir"`)* | (Se levanta. Sube la escalera. En la calle, Crane espera.) "Está abajo. Con el libro." | → **FINAL B — versión "San Clemente"** |

**Si Crane está en la cripta (`crane_humillado`):**

| Opción | Texto | Resultado |
|---|---|---|
| **Sacar el libro escondido** | El protagonista mete la copia bajo el mono **delante de Crane**. Microjuego de CF `[Neutral, difícil]` mientras Crane le mira. Crane, sin órdenes sobre el libro y humillado, decide no registrarle ("Ya le registrarán en el Minimor"). | → **FINAL D** (variante "escoltado": la captura ocurre después de entregar el libro a Dot; Crane ha dado tiempo sin saberlo). Si falla el CF: Crane le registra, encuentra la copia y la tira a una vela. → **FINAL C** (variante "sin libro"). |
| **Dejar el libro y dejarse llevar** | (Deja la copia sobre la mesa. Mira a Goldstein.) "Guárdelo usted." | → **FINAL C** (variante "el libro vive"): la secuencia del Minimor completa, pero en el epílogo una línea indica que la copia de la cripta sigue allí. |
| **Pedir quedarse** | "Déjeme aquí. Usted no tiene órdenes sobre mí en este sitio." | CRANE: (ríe sin alegría) "Sobre usted tengo todas las órdenes del mundo." → **FINAL C** |

---

## Resumen de variables del Acto IV

| Variable | Valores | Se fija en |
|---|---|---|
| `san_clemente_deducido` | bool | J13.02 |
| `crane_perdido` | bool | J13.02 (tramo 3) |
| `carta_ivy` | bool | J13.04 |
| `dp_j11_ivy` | `aceptar` / `recordar` / `roto` | J11.04 / J13.04 |
| `pregunta_jaula` | bool | J13.04 |
| `capitulo_ii` | lista de 6 frases | J13.05 |
| `crane_humillado` | bool | J13.07 |
| `final` | `A` / `B` / `C` / `D` / `E` + variante | J13.08 (o antes) |

## Semillas resueltas en el Acto IV

| Semilla | Resolución |
|---|---|
| Telepantalla retirada del cuarto de suministros (J7) | J13.02, tramo 2: la desmontó Barlow haciéndose pasar por técnico. |
| Campana de "S. Clem…" en La Campana (J4) | J13.03: la estructura vacía de las campanas. Goldstein: "Barlow se llevó la última para que no la fundieran. La tiene colgada en su bar. Así la oyen los proles cada noche." |
| Documentos requisados en Stepney (J9) | J13.04: eran el borrador del Capítulo II de Ivy. |
| "No les creas" (Prólogo) | J13.04: la carta de Ivy cierra el arco. |
| Los pájaros de Amory (J3, J10, J12) | J13.02: el mapa para llegar a la cripta. |
| El reloj de Ivy (Prólogo → J12) | J13.02 (anticipar cohetes) y J13.05 (frase de cierre). |
| "El Partido tolera a Goldstein" (biblia, Final E) | J13.04 ("¿Por qué sigue vivo?") y J13.07 (el teléfono de campaña). |

## Ajustes a la biblia ([guion.md](../guion.md)) introducidos aquí

- **San Clemente está dentro del radio de 2 km del Miniver** donde nunca caen cohetes. Así se llega a ella por deducción.
- **Ivy había empezado a escribir el Capítulo II.** Los "documentos requisados" eran su borrador. Goldstein conserva su primera frase en una carta.
- **El Capítulo II se compone en cinco movimientos** a partir de las entradas del diario, con una frase de cierre condicionada.
- **Si Crane sigue al protagonista hasta la cripta**, llama por un teléfono de campaña y recibe la orden de no tocar a Goldstein. Es una confirmación explícita, antes del Final E, de que el Partido tolera al viejo.
- **Nuevo camino al Final B ("San Clemente"):** entregar a Goldstein a Crane si se fingió en J12.
- **Barlow era técnico de telepantallas falso:** las saboteaba en los ministerios.
