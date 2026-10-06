# ACTO III — LA HERMANDAD

> Jornadas 8–12 · Duración estimada: ~60 min
> Objetivo narrativo: que el jugador pase de **mirar** a **actuar**. Cada misión le da una verdad y le quita algo. Al final del acto ya no hay vuelta atrás: el protagonista sabe quién mató a Ivy, sabe que su vida entera fue diseñada y tiene que elegir entre venderse o huir.
> Notación: ver [00-convenciones.md](00-convenciones.md).

**Estado al entrar:** `nell_respuesta = "aceptar"` o `"aceptar_tarde"`. `duda` ≈ 30–90. `sospecha` ≈ 15–60.

### Reglas generales de las misiones de sigilo

- **Telepantallas:** conos de visión fijos o que barren (indicados con un halo verde tenue cuando el protagonista lleva algo comprometedor).
- **Guardias y funcionarios:** rutas visibles al pulsar sobre ellos (huella de pasos).
- **Ser visto:** el guardia grita "¡Alto!" y la escena se reinicia desde el último punto de control con **SOSPECHA +10**. Si la Sospecha llega a 100, arresto (Final C).
- **Esconderse:** armarios, detrás de carritos, bajo mesas, en ángulos muertos marcados con una sombra más oscura.
- **Ritmo:** cada misión dura 8–12 minutos. Ningún puzle debe bloquear más de 2 minutos: si el jugador se atasca, el protagonista dice en su monólogo una pista.

---

## JORNADA 8 — La guerra es la paz

### J8.00 — Cuarto de suministros · 22:30 *(solo si `nell_respuesta = "aceptar_tarde"`)*

(Nell espera sentada en un cubo vuelto del revés. No se levanta.)

NELL: Has tardado una noche. (Pausa.) Mejor una noche que nunca. Toma.

⟶ ITEM +item_llave_calderas

(Le explica el plan con las mismas palabras que en J7.04-ACEPTAR, en versión resumida.) → J8.03

### J8.01 — El piso · 07:15

(Gimnasia. `CF[Entusiasmo, media]`.)

TELEPANTALLA: …la gloriosa ofensiva de mayo en el frente de Malabar ha comenzado. ¡Nuestras tropas avanzan veinte kilómetros en el primer día!

PENSAMIENTO:
- `[D1]` Veinte kilómetros. Desde un frente que en abril no se movió. Porque yo escribí que no se movió. (Pausa.) Porque alguien escribió que yo escribí.
- `[D2]` Veinte kilómetros de corcho.

- **[Cartel de Ivy]** → MIRAR → PENSAMIENTO: Esta noche, Ivy.

### J8.02 — Departamento de Partes y Cartografía · Día

(Jornada laboral comprimida: un parte y un registro de impactos, con la novedad de que los impactos de anoche ya no sorprenden al protagonista.)

**Registro (2 impactos):** Bermondsey H-10, 01:30 · Poplar K-7, 03:50.

PENSAMIENTO: Dos más. En pardo. (Pausa.) Esta noche sabré si estaban escritos antes de caer.

**Detalle clave para el puzle de la noche.** La directiva de cartografía del día es:

CARTEL (directiva):
```
minipax.carto 03.5.84 malabar
ofensiva mayo · desplazar línea +20km
ref directiva rectif. 0305
```

PENSAMIENTO (al procesarla, automático): Cero tres, cero cinco. La primera rectificación de mayo.

> **Diseño:** el código "0305" es la combinación del Archivo Restringido. El jugador no lo sabe todavía. Queda guardado en el **Registro de documentos** del inventario, consultable en cualquier momento.

(A la salida, Brooke se cruza con el protagonista en el ascensor. Están solos.)

BROOKE: (mirando al frente) Las combinaciones de la planta once cambian cada vez que cambia el frente. (Pausa.) Es lo que dicen. Yo no sé nada.

(Se abren las puertas. Brooke sale sin mirar atrás.)

⟶ `FLAG pista_combinacion = true`

### J8.03 — Sala de calderas del Minipax · 22:50

**Localización:** sótano oscuro y caluroso. Calderas enormes que resoplan. Tuberías por todas partes. Un **montacargas viejo** de reja plegable, cubierto de polvo, con una palanca de latón.

(El protagonista entra por la puerta de servicio con la llave de calderas.)

- **[Calderas]** → MIRAR → PENSAMIENTO: Aquí abajo hace un calor de horno. (Pausa.) Aquí es donde acaba lo que tiramos al agujero de la memoria.
- **[Rejilla de la caldera]** → MIRAR → (A través de la rejilla se ven papeles ardiendo.) PENSAMIENTO: El lápiz de Amory acabaría aquí. *(Si `lapiz_destruido`:)* El lápiz de Amory acabó aquí.
- **[Montacargas]** → USAR → (La reja chirría. El jugador debe accionar la palanca **despacio**, manteniendo pulsado sin soltar: si sube demasiado rápido, chirría y SOSPECHA +5.)

→ J8.04

### J8.04 — Planta once · Pasillo · 23:00

**Localización:** pasillo largo, con suelo de linóleo y luces de neón a medio gas. Al fondo, una **garita de guardia** con un panel de llaves. Más allá, una puerta de acero con **dos cerrojos**: uno de llave y otro de **combinación de cuatro ruedas**. Placa: *ARCHIVO RESTRINGIDO — SOLO PERSONAL AUTORIZADO DEL PARTIDO INTERIOR*. Dos telepantallas: una fija sobre la garita y otra que barre el pasillo cada 6 segundos.

**Secuencia (ventana de cuatro minutos con un reloj visible en pantalla):**

1. **23:00:00.** Cambio de guardia: el guardia saliente abandona la garita, firma en un libro al fondo del pasillo y se marcha. El entrante tarda.
2. El jugador debe avanzar por el pasillo **entre los barridos** de la telepantalla móvil (puntos de cobertura: un extintor, una columna, un carrito de correo).
3. **Coger la llave** del panel de la garita. Hay 12 llaves con etiquetas. La correcta pone *"A.R. – 1"*. (Si coge otra, pierde 10 segundos.)
4. Abrir el **cerrojo de llave**.
5. **Cerrojo de combinación:** cuatro ruedas numeradas. En la placa, grabado pequeño: *"Código: última rectificación vigente"*.
   - Si `pista_combinacion`: PENSAMIENTO: "Cambian cada vez que cambia el frente." La última rectificación… (El jugador puede consultar el Registro de documentos.) → **0305**.
   - Si el jugador falla tres veces: PENSAMIENTO: Una fecha. Una rectificación. Lo he tenido en la mano esta misma mañana.
6. Entrar. La puerta se cierra sola detrás.

> **Si el reloj llega a 23:04:00** sin haber entrado: el guardia entrante aparece al fondo. El jugador debe esconderse (detrás del carrito de correo) y esperar a que haga su primera ronda (30 s), con SOSPECHA +5. La ventana se reabre durante 90 segundos más.

### J8.05 — Archivo Restringido

**Localización:** sala sin ventanas, de techo bajo, iluminada por una única bombilla con pantalla verde. Filas de estanterías con carpetas **azules** idénticas, numeradas por semanas. Al fondo, estanterías más viejas con carpetas por años: *1975… 1979… 1983*. Una mesa de lectura con un tampón y una lupa. No hay telepantalla. Hay algo peor: el **silencio**.

PENSAMIENTO: No hay telepantalla. (Pausa.) Aquí no necesitan vigilar. Aquí nadie entra.

**Puntos interactivos:**

- **[Carpetas de la semana en curso]** → USAR → J8.06 *(objetivo)*
- **[Carpeta: semana del 16 al 22 de abril]** → USAR → J8.06-B *(el mercado)*
- **[Estantería de años: 1979]** → USAR → (El protagonista alarga la mano. Se oyen pasos en el pasillo. El guardia entrante prueba el picaporte. Un segundo eterno. Los pasos se alejan.) PENSAMIENTO: 1979. (No hay tiempo.) Otro día. *(Imposible abrirla en esta misión. Es una provocación intencionada para el jugador.)*

### J8.06 — La Planilla Azul

(El protagonista abre la carpeta de la semana. Dentro, hojas de papel azul pálido, mecanografiadas. Primer plano a pantalla completa.)

CARTEL (documento):
```
MINIPAX · DIRECCIÓN DE MORAL INTERIOR · ALTO SECRETO
PLANILLA DE IMPACTOS PROGRAMADOS · SEMANA 18/84

BATERÍA   ORIGEN               OBJETIVO              CUADR.  FECHA    HORA   CARGA
B-4       Folkestone (Kent)    Bermondsey            H-10    03.5.84  01:30  media
B-2       Dover (Kent)         Poplar                K-7     03.5.84  03:50  ligera
B-4       Folkestone (Kent)    Wapping               I-9     04.5.84  02:10  media
B-7       Hythe (Kent)         Southwark (Borough)   F-10    05.5.84  22:45  pesada
...
Objetivo de la semana: sostener índice de odio > 82 previo a Semana del Odio.
Prioridad: distritos proletarios densos. Excluir radio 2 km de edificios ministeriales.
Autoriza: H.V. · Dir. Moral Interior
```

(Silencio. El protagonista lee las dos primeras líneas: **Bermondsey, H-10, 01:30. Poplar, K-7, 03:50.** Son los dos impactos que registró esta misma mañana.)

PENSAMIENTO: (las líneas aparecen una a una, con pausa)
"Batería cuatro. Folkestone. Kent."
Kent está en Oceanía.
Los cohetes salen de Oceanía.
(Pausa larga.)
"Excluir radio dos kilómetros de edificios ministeriales."
"Índice de odio."
(Pausa.)
Nos bombardeamos. Nosotros. A nosotros.

⟶ DUDA +20 · `FLAG planilla_vista = true`

**Si `patron_conclusion = "proles"`:** PENSAMIENTO: Lo sabía. Lo sabía desde las chinchetas. Saberlo no sirve para nada. Verlo escrito… *(No termina la frase.)*

**Si `patron_conclusion = "cobardes"` o `"casualidad"`:** PENSAMIENTO: Cobardes, dije. Casualidad, dije. (Se ríe, sin sonido, tapándose la boca.) Lo dije yo.

#### J8.06-B — La semana del mercado *(opcional pero recomendado)*

CARTEL (documento, misma cabecera, semana 16/84):
```
B-7       Hythe (Kent)         Limehouse (mercado Watney St.)   J-8   19.4.84  08:12  pesada
Nota: hora punta de mercado. Impacto de alta visibilidad.
Autoriza: H.V.
```

PENSAMIENTO: "Hora punta de mercado." (Pausa.) Sammy. Lo escribieron dos días antes. Alguien escribió a máquina "alta visibilidad" y se fue a comer.

⟶ DUDA +5 · DIARIO +diario_planilla

**Si `sammy_intento`:** PENSAMIENTO: Corrí hacia él como si se pudiera hacer algo. Estaba escrito a máquina.

#### ◆ D-J8-PLANILLA · ¿Cómo sacar la prueba?

| Opción | Mecánica | Efecto |
|---|---|---|
| **Copiar a mano** | Minijuego contrarreloj (30 s): el jugador elige qué líneas copiar con el lápiz (de Amory, si lo tiene). Cada línea copiada tarda 5 s. | ⟶ ITEM +item_copia_planilla. Sin riesgo posterior. La prueba es más débil ("¿quién no puede inventarse una lista?"). |
| **Llevarse la hoja del mercado** | Instantáneo. | ⟶ ITEM +item_hoja_planilla · `FLAG hoja_robada = true`. Prueba irrefutable. En J9, Voss nota que falta (SOSPECHA +10). |

### J8.07 — Salida

(Secuencia inversa: salir del Archivo, devolver la llave **al panel** (si no la devuelve, SOSPECHA +10 al día siguiente), esquivar al guardia nuevo, que ahora hace rondas, y bajar en el montacargas.)

(En la sala de calderas, una sombra con un carrito. Nell.)

NELL: ¿Lo tienes?

(El protagonista asiente. No puede hablar.)

NELL: (le mira a la cara, mucho rato) Ya lo sabes. (Pausa.) Ven. Esta noche no deberías estar sol{o|a}.

### J8.08 — Sótano del pub "La Campana" · Medianoche

**Localización:** bodega bajo el pub, a la que se baja por una trampilla detrás de la barra. Barriles, una mesa de madera, una vela y sillas desparejadas. En la pared, un hueco cuadrado con ladrillos sueltos. El **tabernero** (Tom Barlow) baja detrás de ellos y cierra la trampilla.

(Son tres en la mesa: Nell, Barlow y el protagonista. La vela es la única luz. La paleta es la más cálida que el jugador ha visto: ocres y naranjas.)

NELL: Ponla en la mesa.

(El protagonista deja la copia o la hoja. Barlow la lee a la luz de la vela y silba bajito.)

BARLOW: Folkestone. Sabía que era Folkestone. Mi cuñado trabajaba en el puerto. Decía que de noche se oían "los ensayos". (Pausa.) Lo vaporizaron en el 81.

**Si `prueba_parte`:** el protagonista también pone sobre la mesa el **parte alterado**. NELL: (lo mira, luego mira al protagonista) "Resistido con firmeza." Y tu firma. (Casi sonríe.) Has traído tu propia mentira. Bien. Eso dice más de ti que cualquier juramento. ⟶ `FLAG nell_confianza +1`

NELL: Ahora escúchame. Lo que viene a continuación no es una ceremonia. Es una advertencia. Te voy a hacer unas preguntas. Contesta la verdad. No a mí: a ti.

#### J8.08-I — La iniciación

> **Nota de diseño:** homenaje a la escena de O'Brien con Winston y Julia, con preguntas nuevas. **Cada respuesta se guarda.** En el Final C y en el Final D, O'Brien las reproduce desde la grabación de Crane (el ladrillo suelto del hueco de la pared esconde un micrófono; el jugador no puede saberlo).

NELL: ¿Estás dispuest{o|a} a dar tu vida?
- **Sí** · **No** ⟶ `iniciacion_vida`

NELL: ¿Estás dispuest{o|a} a matar? ¿A alguien que no conoces, que quizá no ha hecho nada, si eso sirve a la causa?
- **Sí** · **No** ⟶ `iniciacion_matar`

NELL: ¿Estás dispuest{o|a} a mentir, a falsificar, a hacer el trabajo del Partido mejor que nadie para que nadie sospeche, durante años?
- **Sí** · **No** ⟶ `iniciacion_mentir`

NELL: ¿Estás dispuest{o|a} a que la próxima planilla lleve el nombre de un barrio donde vive gente que quieres, y a no avisar a nadie, si avisar nos delata?
- **Sí** · **No** ⟶ `iniciacion_callar`

NELL: ¿Estás dispuest{o|a} a que tu hermana deje de ser una mártir? ¿A que su cartel siga en la pared y tú sepas que es mentira, cada mañana, durante el resto de tu vida?
- **Sí** · **No** ⟶ `iniciacion_ivy`

NELL: Y si te cogen, y te cogerán… ¿estás dispuest{o|a} a traicionarnos?
- **No** ⟶ NELL: "Mientes. Todos traicionan. La pregunta es cuándo. Aguanta veinticuatro horas. Es todo lo que te pido."
- **Sí** ⟶ NELL: "Bien. Es la primera respuesta honesta de la noche. Aguanta veinticuatro horas. Es todo lo que te pido."
- ⟶ `iniciacion_traicion`

**Efectos:** cada "No" a las preguntas 1–5 → `nell_confianza −1`, sin efecto de Duda. NELL reacciona a cada "No" con una línea breve: "Al menos lo sabes." / "Eso te honra. Y te hace inútil para algunas cosas." / "Lo anoto. No con papel."

NELL: (pausa) Ya está. No hay carné, no hay contraseña más allá de la canción. No conocerás a más de tres de nosotros. Nunca sabrás cuántos somos. (Pausa.) Puede que seamos cien. Puede que seamos estos tres.

PROTAGONISTA: ¿Y Goldstein?

BARLOW: (ríe por lo bajo) Todos preguntan por el viejo.

NELL: Existe. (Pausa.) Y escribió un libro. (Mete la mano en el hueco de los ladrillos y saca un fajo de hojas mecanografiadas, gastadas, cosidas con hilo.) No lo tenemos entero. Nadie lo tiene. Lo tenemos a trozos, repartidos. Cada célula guarda unas páginas. Si cae una célula, cae un trozo, no el libro.

(Le da unas hojas.)

NELL: Lee esto aquí. No te lo puedes llevar todavía.

### J8.09 — Fragmento I · *Capítulo III: La guerra es la paz* (parte 1)

**Mecánica de lectura:** pantalla a pantalla, papel mecanografiado con tachaduras y manchas. El jugador avanza tocando. Algunas frases quedan **subrayadas** automáticamente si coinciden con algo que el protagonista ya vio, y se puede tocar cada subrayado para recordar la escena relacionada.

> *TEORÍA Y PRÁCTICA DEL COLECTIVISMO OLIGÁRQUICO*
> *por Emmanuel Goldstein*
>
> *Capítulo III — La guerra es la paz*
>
> *Las tres potencias que se reparten el mundo no pueden vencerse entre sí, y lo saben. Cada una es demasiado grande, demasiado autosuficiente y está demasiado bien defendida por la geografía. La guerra entre ellas no es una lucha por la victoria. Es una institución.*
>
> *Una guerra que nunca termina sirve para gastar lo que una sociedad produce de más. Un pueblo que tiene más de lo que necesita empieza a pensar. Un pueblo que racionaba el chocolate y ahora lo racionará aún más, en nombre del frente, no tiene tiempo de pensar.* <u>[subrayado si `chocolate_visto`]</u>
>
> *Por eso los frentes apenas se mueven.* <u>[subrayado: los agujeros de alfiler en el mapa de Malabar]</u> *Los mapas se corrigen, los partes se reescriben, pero el frente real es casi una abstracción. A veces ni siquiera eso: unas banderas sobre un corcho.*
>
> *Y cuando la guerra lejana no basta para sostener el miedo, el Partido la trae a casa. Un cohete que cae sobre un mercado es más útil que cien victorias en Malabar. El enemigo no necesita lanzarlo. Basta con que el pueblo crea que lo hizo.* <u>[subrayado: la Planilla Azul]</u>
>
> *La guerra ya no la hace un Estado contra otro. La hace cada grupo dirigente contra sus propios súbditos. Su objetivo no es conquistar territorio, sino mantener intacta la estructura de la sociedad.*

⟶ ITEM +item_libro (fragmentos: 1/4) · DIARIO +diario_libro_guerra

PENSAMIENTO: "Basta con que el pueblo crea que lo hizo." (Pausa.) Yo lo creí. Cinco años. Cada mañana.

NELL: (recoge las hojas) El resto, otro día. Si hay otro día.

(Barlow abre la trampilla. Es casi de madrugada.)

### J8.10 — El piso · 03:00

(El protagonista entra sin encender la luz. La telepantalla emite el himno en volumen nocturno.)

- **[Cartel de Ivy]** → MIRAR →
  PENSAMIENTO: "¿Estás dispuest{o|a} a que tu hermana deje de ser una mártir?" (Pausa.) Ya no lo es. Ahora es otra cosa. No sé qué. (Pausa.) Ya no sé quién eras.
- **[Hueco junto al armario]** → USAR con **item_diario** → composición de entradas. *Nuevas:*

**`diario_planilla`**
- a) *"Folkestone, Kent. Los cohetes salen de Kent. Kent está en Oceanía."*
- b) *"'Hora punta de mercado. Impacto de alta visibilidad.' Alguien lo escribió a máquina y se fue a comer."*

**`diario_libro_guerra`**
- a) *"La guerra no es contra Eurasia. Es contra nosotros."*
- b) *"Un cohete sobre un mercado vale más que cien victorias."*

CARTEL: **JORNADA 9**

---

## JORNADA 9 — La ignorancia es la fuerza

### J9.01 — El piso · 07:15

(Gimnasia. `CF[Entusiasmo, media]`. El protagonista apenas ha dormido.)

**Si `duda >= 60`:** durante la gimnasia el monólogo interfiere de verdad con el ritmo. Las frases aparecen encima de las flechas y tapan parte de la pantalla:

PENSAMIENTO: Uno, dos. Folkestone. Uno, dos. Kent. Uno, dos. Índice de odio. Uno…

⟶ La dificultad efectiva sube a "difícil" para este CF.

### J9.02 — Departamento de Partes y Cartografía

**Si `hoja_robada`:**

(Voss sale de su despacho. Recorre la sala despacio, mesa por mesa. Se detiene junto al protagonista.)

VOSS: Anoche alguien entró en la planta once. (Pausa.) Falta un documento. Sin importancia, en realidad. Una hoja vieja. (Sonríe.) Pero el Partido no tolera el desorden. ¿Usted no oyó nada, camarada? Trabaja usted hasta tan tarde…

#### CF-J9-VOSS · `CF[Neutral, difícil]`

PROTAGONISTA: No, Subdirector. Me fui a las siete.

⟶ SOSPECHA +10 (fijo) · Si falla el CF: SOSPECHA +10 adicional.

(Voss se aleja.)

**Siempre:**

VOSS: Camarada {APELLIDO}. Hoy hará de mensajero. Las cartas corregidas de la ofensiva de mayo deben llegar al **Departamento de Registro del Miniver** antes de mediodía. En mano. (Le entrega un tubo de cartón sellado.) No se entretenga.

PENSAMIENTO: El Miniver. (Pausa.) Nell dijo que la próxima vez me buscarían ellos.

(Al recoger el abrigo, el protagonista encuentra en el bolsillo un papel doblado. Letra de imprenta, sin firma.)

CARTEL (nota):
```
Registro. Planta 3. Lavabo del fondo.
Panel bajo el lavabo. Llévate lo que hay. Deja lo que traes.
Naranjas.
```

(Dentro del papel hay otro papel doblado: un ejemplar del *Times* actual, el de la fecha **corregida** de la muerte de Ivy. Es el señuelo que hay que dejar a cambio.)

⟶ ITEM +item_times_falso

### J9.03 — Ministerio de la Verdad · Vestíbulo y Departamento de Registro

**Localización:** pirámide blanca, idéntica por fuera al Minipax, pero por dentro con un **ruido** constante de tubos neumáticos, máquinas de escribir y altavoces. El Departamento de Registro es una sala enorme de cubículos de cristal, cada uno con su máquina de escribir, su habla-escribe y tres ranuras: tubo de entrada, tubo de salida y **agujero de la memoria**.

(El protagonista entrega el tubo en un mostrador. Una funcionaria firma el recibo y le indica la salida. Para llegar a los lavabos de la planta tres hay que cruzar la sala de cubículos sin justificación.)

**Mecánica:** "sigilo social". No hay que esconderse, sino **parecer ocupado**. El protagonista lleva una carpeta bajo el brazo (USAR la carpeta → "aparentar que lee"). Mientras camina con la carpeta abierta, los funcionarios no reparan en él. Si se detiene más de 3 segundos sin la carpeta abierta, un supervisor se acerca: "¿Busca algo, camarada?" → SOSPECHA +5 y vuelta al punto anterior.

**Cameos durante el recorrido (puntos interactivos solo MIRAR, sin detenerse demasiado):**

- **[Cubículo con un hombre de cuarenta años encorvado] (WINSTON)**
  - MIRAR → (Winston dicta algo en el habla-escribe con cara de concentración absoluta. Luego mete un papel en el agujero de la memoria con un gesto rapidísimo.) PENSAMIENTO: Smith. Así que esto es lo que hace todo el día. (Pausa.) `[D2]` Así que esto es lo que me hicieron a mí. A mi parte.
- **[Mujer de la faja escarlata] (JULIA)** *(cruza el pasillo con un brazo en cabestrillo)*
  - MIRAR → (Julia tropieza junto al cubículo de Winston y cae. Winston la ayuda a levantarse. Durante un segundo, sus manos se tocan. Ella se aleja.) PENSAMIENTO: La chica de la Liga Anti-Sex. Smith la ha ayudado. (Pausa.) Le ha dado algo. Un papel. ¿O me lo he imaginado?
  - *(El jugador que conozca la novela sabe qué pone ese papel. El protagonista no lo sabrá nunca.)*

### J9.04 — Cantina del Miniver *(paso obligado hacia la escalera de la planta tres)*

**Localización:** cantina en el sótano, abarrotada y ruidosa. Bandejas metálicas, guiso, ginebra. Un hombre pequeño y moreno, con gafas y ojos grandes, habla con entusiasmo a quien quiera oírle: **Syme**.

(Para cruzar hacia la escalera, el protagonista tiene que pasar junto a la mesa de Syme. Syme le ve el distintivo del Minipax en el mono.)

SYME: ¡Minipax! ¿Cartografía? (No espera respuesta.) Siéntese, siéntese un minuto. Estoy trabajando en la undécima edición del Diccionario. ¿Sabe lo que hacemos? Destruimos palabras. Cientos cada día. (Ríe, encantado.) Es precioso. Si no existe la palabra, no existe la idea.

PROTAGONISTA: Lo sé. Un compañero mío decía lo mismo.

SYME: ¡Un hombre sensato! ¿Cómo se llama? Me gustaría conocerle.

#### ◆ D-J9-SYME

| Opción | Efecto |
|---|---|
| "Felix Amory." | SYME: (se le borra la sonrisa por primera vez; baja la voz) "…No conozco a ningún Amory. (Pausa.) Y usted tampoco debería." (Se gira hacia otro comensal y sigue hablando como si nada.) ⟶ SOSPECHA +3 · DUDA +3 |
| "No me acuerdo." | SYME: "¡Ja! Eso es doblepensar del bueno. ¡Excelente!" · Sin efecto. |

SYME: (antes de que el protagonista se vaya) Ustedes en Cartografía también destruyen, ¿sabe? Nosotros destruimos palabras. Ustedes, lugares. Un río que se mueve, un frente que cambia de nombre… (Ríe.) Somos colegas.

PENSAMIENTO: Habla demasiado. Como Amory. (Pausa.) No tardará en desaparecer.

> **Nota:** en la novela, Syme es vaporizado poco después. En la Jornada 10, su ausencia se menciona en la cola de la Semana del Odio.

### J9.05 — Lavabos de la planta tres

**Localización:** lavabo de azulejo blanco, con cuatro lavamanos, un espejo largo, una telepantalla pequeña sobre la puerta (que mira a los lavamanos) y cubículos.

**Puzle:**

1. La telepantalla mira a los lavamanos. Hay que **bloquear su visión**:
   - Opción A: abrir los grifos de agua caliente hasta que el **vaho** empañe el espejo y la pantalla. Tarda 20 s; mientras, hay que "lavarse las manos" (CF Neutral).
   - Opción B: colgar el abrigo de la percha que hay justo bajo la pantalla. Es más rápido, pero un funcionario entra a mitad de la operación, ve el abrigo y comenta: "Ahí no se cuelga, camarada." SOSPECHA +3.
2. **Panel bajo el último lavabo:** se suelta con la uña (o con el compás si lo tiene: más rápido).
3. Dentro hay un **sobre de papel encerado**. Hay que dejar el *Times* falso en su lugar y volver a colocar el panel.

⟶ ITEM −item_times_falso · ITEM +item_sobre_miniver

### J9.06 — El *Times* original

(De vuelta en la calle, en un banco de un parque pequeño, frente a una telepantalla lejana a la que el protagonista da la espalda. Abre el sobre con cuidado. Dentro hay dos cosas.)

**1. Un ejemplar original del *Times*, amarillento, de 1979:**

> **CALLE STEPNEY: CAE UN COHETE EN EL DISTRITO ESTE**
> *Un proyectil alcanzó anoche, a las 21:40, el número 14 de la calle Stepney. Una víctima mortal: la camarada Ivy {APELLIDO}, del Partido Exterior. Agentes de la Policía del Pensamiento se presentaron en el lugar minutos después del impacto y requisaron diversos documentos de la vivienda.*

**2. Para comparar, el protagonista saca de memoria el ejemplar falso (en pantalla aparece en paralelo, como en J6):**

| | Original (1979) | Versión vigente |
|---|---|---|
| Fecha | Día X, 21:40 | **Día X + 1, 23:15** |
| Titular | *Cae un cohete en el distrito este* | ***Cobarde ataque euroasiático contra la juventud del Partido*** |
| Víctima | "la camarada Ivy {APELLIDO}" | "la heroica camarada Ivy {APELLIDO}, mártir del Ingsoc" |
| Policía del Pensamiento | "requisaron diversos documentos" | *(eliminado)* |
| Añadido | — | "El Gran Hermano ha ordenado una respuesta implacable. Mañana comienza la ofensiva de castigo en Malabar." |

- **[Reloj de Ivy]** → USAR → (El protagonista lo saca y lo pone junto al periódico.) PENSAMIENTO: Las nueve y cuarenta. (Pausa.) El reloj tenía razón. El periódico de hoy, no.

PENSAMIENTO:
- Movieron la fecha un día. Para que coincidiera con la ofensiva. Para que Ivy fuera *el motivo*.
- (Pausa.) "Agentes de la Policía del Pensamiento se presentaron minutos después." Minutos. ¿Por qué iba la Policía del Pensamiento a un bombardeo? ¿Qué documentos? (Pausa larga.) ¿Qué guardabas, Ivy?

⟶ DUDA +10 · `FLAG times_original = true` · DIARIO +diario_times · ITEM +item_times_original

**2b. Debajo del periódico, en el mismo sobre, unas hojas mecanografiadas cosidas con hilo.** La Hermandad le hace llegar el siguiente fragmento.

### J9.07 — Fragmento II · *Capítulo I: La ignorancia es la fuerza* (parte 1)

> *Capítulo I — La ignorancia es la fuerza*
>
> *Desde que existe la historia escrita ha habido tres clases de personas: los de Arriba, los del Medio y los de Abajo. Sus nombres han cambiado mil veces. Su relación, ninguna.*
>
> *Los de Arriba quieren quedarse donde están. Los del Medio quieren ocupar el lugar de los de Arriba. Los de Abajo, cuando tienen fuerzas para querer algo, quieren un mundo sin Arriba ni Abajo. Y los del Medio, para subir, siempre prometen ese mundo a los de Abajo. Lo prometen, los usan, suben… y los de Abajo vuelven a su sitio.*
>
> *El Partido ha estudiado esta rueda mejor que nadie. Y ha hecho algo que ningún grupo dirigente había conseguido: detenerla. Arriba, el Partido Interior. En medio, el Partido Exterior: vigilado, cansado, demasiado ocupado en odiar para mirar hacia arriba.* <u>[subrayado: Voss]</u> *Abajo, los proles: tan despreciados que el Partido no se molesta en vigilarlos.* <u>[subrayado: Limehouse sin telepantallas]</u>
>
> *Si los proles llegaran a ser conscientes de su fuerza, no necesitarían conspirar. Les bastaría con sacudirse, como un caballo se sacude las moscas. Pero para eso tendrían que saber. Y el Partido se asegura de que no sepan.*

⟶ ITEM item_libro (fragmentos: 2/4) · DIARIO +diario_libro_ignorancia

### J9.08 — El piso · Noche

- **[Hueco junto al armario]** → USAR con **item_diario** → *Nuevas entradas:*

**`diario_times`**
- a) *"El reloj de Ivy marca las 21:40. El periódico de hoy dice otra hora. El reloj no sabe mentir."*
- b) *"Movieron su muerte un día para que sirviera de algo."*

**`diario_libro_ignorancia`**
- a) *"Los proles no necesitan conspirar. Solo necesitan saber."*
- b) *"Yo soy el Medio. Vigilado, cansado, odiando hacia abajo."*

- **[Cartel de Ivy]** → MIRAR → PENSAMIENTO: ¿Qué documentos, Ivy? ¿Qué escribías?

CARTEL: **JORNADA 10**

---

## JORNADA 10 — Semana del Odio

### J10.01 — Las Mansiones Victoria · Mañana

(La escalera está cubierta de banderines, gracias a Parsons. Carteles nuevos en cada rellano: un soldado **euroasiático** gigantesco, con botas, que avanza hacia el espectador. El cartel de los mártires con Ivy está por todas partes.)

HILDA: (radiante, con una diadema de cartón con la cara del Gran Hermano) ¡{NOMBRE}! ¡Hoy es el gran día! Mitin en la plaza de la Victoria a las doce. ¡Y esta noche quemamos la efigie de Goldstein! (Baja la voz.) ¿Te has enterado? Syme, el del Miniver, el del diccionario… ya no viene a los ensayos. (Encoge los hombros.) Será que lo han trasladado.

PENSAMIENTO: Trasladado.

**Si `hilda_aprecio <= 0`:**

HILDA: (con la sonrisa algo rígida) Por cierto. El Subdirector Voss es un hombre encantador. (Pausa.) Me pidió que le avisara de cualquier… cosa. Por lo de la Semana del Odio. Por seguridad.

⟶ SOSPECHA +5 · PENSAMIENTO: Voss. Hilda habla con Voss.

### J10.02 — Cantina del Minipax · Antes del mitin

(Toda la cantina mira la telepantalla grande. El ambiente es eléctrico.)

TELEPANTALLA: …y a continuación, la confesión del traidor, que ha pedido voluntariamente hablar a su pueblo antes de recibir su justo castigo.

(Aparece **Amory**. Está irreconocible: delgadísimo, sin gafas, con la cara hinchada, el pelo rapado y huecos donde había dientes. Mira a cámara sin enfocar.)

AMORY: (voz plana, como recitando) Yo, Felix Amory, confieso haber trabajado al servicio de Eurasia desde mil novecientos setenta y seis. Confieso haber saboteado los mapas del frente de Malabar para confundir a nuestras tropas. Confieso haber dibujado señales para el enemigo en los márgenes de documentos oficiales. (Pausa.) Pájaros. Dibujé pájaros. Eran señales. (Pausa.) Amo al Gran Hermano. Merezco morir. Pido morir.

(La cantina abuchea. Alguien tira un trozo de pan a la pantalla.)

#### CF-J10-AMORY · `CF[Desprecio, difícil]`

PENSAMIENTO (ráfagas durante el microjuego):
- "Pájaros." (Pausa.) Eran pájaros. Solo eran pájaros.
- Ojos de pájaro. Mordía los lápices.
- **Si `amory_reaccion = "denuncia"`:** Yo dije su nombre. Yo dije su nombre. Yo dije su nombre.
- **Si `dp_j3_amory = "aceptar"`:** (La imagen de Amory parpadea con *glitch* y su nombre aparece en pantalla como "—", luego "F. AMORY", luego "—" otra vez.) No sé quién es. Sé quién es. No sé quién…

⟶ Si falla: SOSPECHA +10. Si `amory_reaccion = "denuncia"`, la dificultad sube un grado.

(Al terminar, Pell, en la mesa de al lado, come sin levantar la vista.)

PELL: (sin mirarle) Traidor. Menos mal que lo cogieron. (Pausa.) ¿Usted lo conocía?

#### ◆ D-J10-PELL

| Opción | Efecto |
|---|---|
| "Nunca le había visto." | PELL: "Ni yo." · Sin efecto. DIARIO +diario_amory_confesion (variante "negación") |
| "Se sentaba en su silla." | PELL: (deja de masticar; le mira con algo parecido al miedo) "…Mi silla siempre ha sido mía." ⟶ SOSPECHA +5 · DIARIO +diario_amory_confesion (variante "verdad") |

### J10.03 — Plaza de la Victoria · El mitin (pista D)

**Localización:** plaza enorme, abarrotada. La columna con la estatua del Gran Hermano. Tribuna con colgaduras rojas. Pancartas de *¡MUERTE A EURASIA!* (una de ellas, la que pintó el protagonista en J2.05). Efigies de Goldstein. Altavoces. Helicópteros.

(El protagonista está entre la multitud, junto a Hilda y los Parsons. El orador, un hombre pequeño y huesudo con voz atronadora, lleva veinte minutos de discurso.)

ORADOR: …¡las hordas euroasiáticas, que bombardean a nuestros niños en los mercados…!

(La multitud ruge.)

#### CF-J10-MITIN · `CF[Odio → Odio, difícil]` *(con giro)*

**Fase 1 (30 s):** Odio contra Eurasia. Ritmo normal.

PENSAMIENTO: "Bombardean a nuestros niños en los mercados." (Pausa.) Batería siete. Hythe. Kent.

**Fase 2: el giro.** Un hombre sube a la tribuna y le pasa un papel al orador. El orador lo lee **sin dejar de hablar ni cambiar el tono**.

ORADOR: …¡y Estasia, con su barbarie, que desde siempre…! ¡Estasia, nuestro enemigo eterno…!

(La multitud se queda **medio segundo** en silencio absoluto. El jugador ve en pantalla la expresión de cientos de caras: la duda congelada. Luego, un murmullo. Alguien grita: "¡Los carteles! ¡Los carteles son de Eurasia! ¡Sabotaje! ¡Es obra de Goldstein!")

(La multitud enloquece y empieza a **arrancar sus propias pancartas**. Hilda arranca la del protagonista. Los niños Parsons pisotean un cartel del soldado euroasiático.)

**Fase 3 (30 s):** el jugador debe mantener la cara de **Odio** mientras el objetivo cambia **de Eurasia a Estasia**, y además **arrancar pancartas** (tocar rápidamente las que tienen "EURASIA") sin tocar las del Gran Hermano. Si toca una del Gran Hermano: SOSPECHA +10.

PENSAMIENTO (ráfagas):
- Estasia. Estasia. Siempre fue Estasia.
- Doce kilómetros en Malabar. Contra Eurasia.
- Sammy. Contra… ¿contra quién?
- Ivy murió por Eurasia. Ahora Ivy murió por Estasia. Ivy murió por quien haga falta.

⟶ DUDA +10 · DIARIO +diario_estasia

(El mitin termina. Hilda, sudorosa, abraza al protagonista.)

HILDA: ¡Qué emoción! ¡Estasia! (Pausa.) ¡Siempre lo supe!

### J10.04 — Departamento de Partes y Cartografía · Noche

(Toda la plantilla ha sido convocada. Nadie dormirá en cuarenta y ocho horas. La sala hierve. Voss, en mangas de camisa por primera vez, de pie en el centro.)

VOSS: Camaradas. Durante los últimos cuatro años, en todos los documentos de este ministerio, Oceanía ha estado en guerra con Estasia. (Pausa.) Los documentos que digan otra cosa contienen errores. Corríjanlos.

#### Minijuego 4: LA GRAN RECTIFICACIÓN *(contrarreloj, ~3 minutos)*

**Mecánica combinada:**
1. **Mapas:** arrancar las banderitas negras de Eurasia del frente de Malabar y clavar banderitas amarillas (Estasia) en otro frente (Manchuria, Mongolia, Indonesia). El corcho de Malabar queda lleno de agujeros vacíos.
2. **Partes:** reescribir partes antiguos, cambiando "euroasiático" por "estasiático" en textos que pasan por la máquina de escribir (tocar las palabras resaltadas).
3. **Registro de impactos:** la cabecera del Libro de Registro dice *"Impactos euroasiáticos"*. Hay que tachar y escribir *"estasiáticos"*. En cada página.

PENSAMIENTO (mientras tacha):
- `[D1]` Los cohetes de la semana pasada eran euroasiáticos. Ahora son estasiáticos. Siguen saliendo de Folkestone.
- `[D2]` Bermondsey, estasiático. Poplar, estasiático. Watney Street, estasiático. Sammy murió por Estasia. Ya está corregido.

#### ◆ Misión de la Hermandad: LA PRUEBA *(sigilo dentro del minijuego)*

(A mitad del minijuego aparece Nell con su carrito, recogiendo papeleras. Al pasar junto al protagonista, deja caer un trapo. Bajo el trapo, una nota.)

CARTEL (nota):
```
Un mapa sin corregir. Un parte sin corregir.
Al doble fondo del carro antes de las 3.
```

**Mecánica:** el protagonista debe **apartar** un mapa de Malabar sin corregir (el antiguo, con Eurasia) y un parte original sin rectificar, y meterlos en el doble fondo del carrito de Nell (que está aparcado al fondo de la sala) **sin que Voss lo vea**. Voss recorre la sala en una ruta fija. Pell y Brooke trabajan cerca.

- Si el jugador lo consigue: ⟶ `FLAG prueba_rectificacion = true` · Nell, al recoger el carro, toca el borde dos veces (señal de "recibido").
- **Ayuda de Brooke:** si el jugador se acerca al carrito mientras Voss mira hacia esa zona, Brooke **tira una pila de carpetas** al suelo para distraerle. VOSS: "¡Cuidado, camarada!" BROOKE: "Perdone, Subdirector. El cansancio." *(Solo una vez. Si el jugador lo vuelve a necesitar, Brooke no hace nada.)*
- Si Voss lo ve: SOSPECHA +20 y la misión falla. (No se reintenta.) VOSS: "¿Qué hace con ese mapa, camarada?" PROTAGONISTA: "Lo llevaba al agujero de la memoria." VOSS: "El agujero está aquí." (Señala la ranura.) "Úselo." (El protagonista tiene que tirar el mapa al agujero delante de él.)

### J10.05 — Madrugada · Fragmento III

(04:00. La sala casi vacía. El protagonista se queda dormido sobre la mesa. Al despertar, entre los papeles de su mesa hay unas hojas mecanografiadas cosidas con hilo, bajo un mapa nuevo de Estasia.)

> *Capítulo III — La guerra es la paz (continuación)*
>
> *Las alianzas entre las tres potencias cambian de vez en cuando, y cada vez que cambian, el pasado cambia con ellas. Oceanía nunca ha estado aliada con el enemigo de hoy. Nunca ha estado en guerra con el aliado de hoy. Los documentos que digan otra cosa se corrigen en una noche.*
>
> *Esto sería imposible si quienes corrigen los documentos lo supieran y lo recordaran. Y lo saben, y lo recuerdan. Y lo olvidan. Y olvidan que lo han olvidado. A esta gimnasia mental el Partido la llama doblepensar: sostener a la vez dos ideas contrarias y creer en las dos.*
>
> *El funcionario que esta noche arranca banderas negras y clava banderas amarillas sabe que está mintiendo.* <u>[subrayado: esta misma noche]</u> *Y sin embargo, mañana por la mañana, si alguien le pregunta, dirá sin mentir que Oceanía siempre ha estado en guerra con Estasia. El doblepensar no es un engaño. Es una disciplina.*
>
> *Por eso el enemigo es intercambiable. No importa contra quién se luche. Importa que la lucha no termine.*

⟶ ITEM item_libro (fragmentos: 3/4) · DIARIO +diario_libro_doblepensar

PENSAMIENTO: "Sabe que está mintiendo." (Mira sus propias manos manchadas de tinta.) Sí.

### J10.06 — Las Mansiones Victoria · Noche siguiente · Parsons

(El protagonista vuelve a casa tras cuarenta y ocho horas. En la escalera hay gente. La puerta de los Parsons está abierta. Dos hombres de uniforme negro sacan a **Parsons**, que llora.)

PARSONS: (al pasar junto al protagonista, con los ojos desorbitados) ¡Camarada {APELLIDO}! ¡Ha sido mi hija! ¡Mi pequeña! ¡Me oyó hablar en sueños! ¡Dicen que dije…! (Le tapan la boca.) ¡Estoy orgulloso de ella! ¡Estoy orgulloso…!

(Se lo llevan. En el rellano, la **hija de Parsons**, con el pañuelo rojo de los Espías, junto a Hilda, que le acaricia el pelo.)

HILDA: (emocionada) Qué niña tan valiente. Tan valiente. (Al protagonista:) Le van a dar una mención.

(La hija de Parsons mira al protagonista. Muy fijamente.)

HIJA PARSONS: Usted también dice un nombre por las noches. (Pausa.) Ahora dice dos.

⟶ SOSPECHA +5

PENSAMIENTO: Dos. Ivy. Y… (No termina.) ¿Sammy? ¿Amory? ¿Nell?

- **[Hueco junto al armario]** → USAR con **item_diario** → *Nuevas entradas:*

**`diario_amory_confesion`**
- a, variante "verdad": *"Amory confesó que los pájaros eran señales. Eran pájaros."*
- b, variante "negación": *"Dije que no le conocía. Comíamos juntos los martes."*

**`diario_estasia`**
- a) *"A mediodía era Eurasia. A las doce y cuarto, Estasia. Nadie gritó."*
- b) *"Ivy murió por quien haga falta."*

**`diario_libro_doblepensar`**
- a) *"El doblepensar no es un engaño. Es una disciplina. Yo la practico desde niñ{o|a}."*
- b) *"Arranqué banderas negras toda la noche. Sabía que mentía. Ya casi no lo sé."*

CARTEL: **JORNADA 11**

---

## JORNADA 11 — El Ministerio del Amor

### J11.01 — Departamento de Partes y Cartografía · Mañana

VOSS: Camarada {APELLIDO}. (Le entrega una carpeta gris sellada con lacre rojo.) La lista de prisioneros estasiáticos para la ejecución pública de mañana en el parque. Llévela al **Ministerio del Amor**. Recepción de la planta baja. (Pausa.) Personalmente.

PROTAGONISTA: ¿Al Minimor, Subdirector?

VOSS: ¿Le supone algún problema, camarada?

#### CF-J11-VOSS · `CF[Neutral, difícil]`

PROTAGONISTA: Ninguno, Subdirector.

VOSS: (le mira un segundo de más) Es un edificio muy interesante. Todo el mundo debería visitarlo al menos una vez. (Vuelve a su despacho.)

PENSAMIENTO: Me está enseñando dónde voy a acabar.

(Al salir, Brooke se cruza con el protagonista en el pasillo. Sin detenerse, le pone algo en la mano: una **chapa metálica** con un número. Sigue caminando.)

BROOKE: (sin mirarle, en un susurro) Archivo B, pasillo cuatro. Tres minutos mientras sellan la lista. (Pausa.) Mi hermano está en esa lista.

⟶ ITEM +item_chapa_archivo · `FLAG brooke_revelada = true`

PENSAMIENTO: ¿Su hermano?

### J11.02 — Ministerio del Amor · Exterior y recepción

**Localización:** el Minimor no tiene ventanas. Ninguna. Está rodeado de alambradas, nidos de ametralladoras y guardias con porras articuladas. Dentro, todo es **blanco**: paredes, suelo, techo y una luz sin sombras que no parpadea. Silencio absoluto, salvo un **zumbido** constante y, muy de vez en cuando, algo que podría ser un grito lejano o una tubería.

(La paleta del Minimor: blanco puro, gris y nada más. Ni siquiera el rojo del Partido.)

FUNCIONARIA DEL MINIMOR: (mujer sin edad, voz de enfermera) Carpeta. (La abre, la sella, empieza a cotejar nombres con un fichero.) Siéntese. Tardaré unos minutos.

(El protagonista se sienta en un banco blanco. Junto a él, en el banco, hay una copia de la lista. **Primer plano de la lista:**)

CARTEL (lista):
```
PRISIONEROS ESTASIÁTICOS · EJECUCIÓN PÚBLICA · PARQUE DE LA VICTORIA
1. CHEN, W.         (captur. frente Manchuria)
2. KOVAL, D.        (captur. frente Manchuria)
3. PIKE, L.         (captur. frente Manchuria)
4. HOGAN, T.        (captur. frente Indonesia)
...
```

PENSAMIENTO: Pike. (Pausa.) Pike. Como Dot.

- **[Lista]** → MIRAR (zoom en "PIKE, L.") → junto a cada nombre hay una foto pequeña de ficha policial. La de Pike, L. es la de un **hombre fornido de unos treinta y cinco años**, con un tatuaje de ancla en el cuello, como el de los estibadores de Limehouse.
  - Si `dot_confianza >= 1`: PENSAMIENTO: Dot dijo que su marido trabajaba en el muelle. Turno de noche. (Pausa.) Len. Le llamaba Len.
  - Si no: PENSAMIENTO: Un estibador. "Capturado en el frente de Manchuria." Con un ancla de Limehouse en el cuello.
- **[Foto de Hogan, T.]** → MIRAR → PENSAMIENTO: Hogan. Sammy decía que Billy Hogan tenía cuarenta trozos de metralla. (Pausa.) ¿El padre de Billy?

⟶ DUDA +10 · `FLAG lista_proles_vista = true`

PENSAMIENTO: "Prisioneros estasiáticos." Hace tres días eran euroasiáticos. Hace un mes eran estibadores.

### J11.03 — Archivo B · Pasillo cuatro *(misión de sigilo, 3 minutos)*

(La funcionaria se levanta y se lleva la carpeta a una oficina interior. "Espere aquí.")

**Mecánica:** la chapa de Brooke abre una puerta lateral (un acceso de servicio de los proles de limpieza; la chapa es de Len). Pasillos blancos idénticos, puertas numeradas y ninguna telepantalla visible (las del Minimor están **empotradas y ocultas**: solo se las detecta por un pequeño zumbido al acercarse, que se representa como una vibración en pantalla y un sonido). El jugador navega guiándose por el sonido.

**Objetivo:** Archivo B, pasillo cuatro. Fichero de expedientes por apellido.

(El protagonista abre el cajón de su propio apellido. Dentro, entre otras fichas, una carpeta: **{APELLIDO}, IVY**.)

### J11.04 — El expediente de Ivy

(Primer plano a pantalla completa. Papel blanco, mecanografiado. Fotos.)

CARTEL (documento):
```
MINISTERIO DEL AMOR · EXPEDIENTE 79/0412
SUJETO: {APELLIDO}, IVY · PARTIDO EXTERIOR · MININDANCIA, SECC. RACIONES

ACTIVIDAD: miembro de la organización conocida como «la Hermandad»
           desde 1977. Correo entre células del distrito Este.
           Contacto conocido: HASK, N. (prole, sin filiación).
           Distribución de fragmentos del libro «T. y P. del C. O.»

RESOLUCIÓN: eliminación sin proceso.
            Motivo: evitar martirio de signo subversivo.
            Método: impacto programado.
                    PLANILLA AZUL 28/79 · Objetivo: calle Stepney 14
                    · 21:40 · carga ligera.
            Uso posterior: martirio de signo patriótico.
                    Campaña "Mártires de Stepney". Rectificación
                    de fecha para coincidir con ofensiva de castigo.

FAMILIAR DIRECTO: {APELLIDO}, {NOMBRE} · sin implicación.
            Perfil: alta lealtad, alta capacidad de odio canalizable.
            Potencial de aprovechamiento: ALTO.
            Recomendación: destino Minipax, Partes y Cartografía.
            Seguimiento personal.

AUTORIZA: H. VOSS · Dir. Moral Interior · Minipax
```

(Al fondo de la carpeta hay una foto: Ivy, sonriendo con el diente mellado, en un sótano a la luz de una vela, junto a una **Nell** cinco años más joven y un **Barlow** con más pelo. La foto está tomada desde un ángulo bajo, como a través de un hueco en la pared.)

(Silencio total. Ni zumbido. El jugador no puede pulsar nada durante 5 segundos.)

PENSAMIENTO: (línea a línea, muy despacio)
"Evitar martirio de signo subversivo."
La mataron para que la Hermandad no tuviera una mártir.
Y la convirtieron en la suya.
(Pausa.)
"Familiar directo. Sin implicación. Alta capacidad de odio canalizable."
Eso soy yo.
"Recomendación: destino Minipax."
Mi trabajo. Mi mesa. Mis partes. Mi odio.
(Pausa.)
Todo esto lo firmó el mismo hombre.
"H. Voss."
(Pausa larga.)
El abrigo. Los guantes. "Esta camarada es ahora una mártir del Partido."
Era él.
(Pausa.)
"No les creas." No hablaba de Eurasia, Ivy. Hablaba de ellos.

⟶ DUDA +25 · `FLAG ivy_revelada = true` · DIARIO +diario_ivy_verdad

#### DP-J11-IVY · Doblepensar extremo

(La pantalla se llena de estática. El expediente tiembla. Las palabras empiezan a reescribirse solas. La voz que habla no es la de la telepantalla: es la de **Voss**, suave.)

VOZ DE VOSS: Su hermana era una traidora. Una espía. Iba a destruir todo lo que usted ama. El Partido la detuvo antes de que pudiera hacerle daño. El Partido le protegió a usted. (Pausa.) Y además le dio una mártir. Le dio algo por lo que vivir. ¿No es eso amor?

| Opción | Texto en pantalla | Efecto |
|---|---|---|
| **Aceptar** | *Ivy era una traidora. El Partido me protegió.* | ⟶ DUDA −20 · SOSPECHA −10 · `dp_j11_ivy = "aceptar"`. El expediente vuelve a ser legible, pero la foto de Ivy en el sótano aparece **tachada**. PENSAMIENTO: Me protegió. Me protegió. (Las manos no paran de temblar.) |
| **Recordar** | *Ivy cantaba. Ivy me dijo: "No les creas".* | ⟶ DUDA +10 · `dp_j11_ivy = "recordar"`. La estática se rompe como un cristal. |

> **Diseño:** es el último doblepensar "suave" del juego. Si el jugador acepta aquí, puede seguir jugando (el Acto IV sigue disponible si `duda >= 30`), pero el Capítulo II tendrá un tono muy distinto, y en el Final D el protagonista se quiebra antes.

#### ◆ D-J11-EXPEDIENTE

| Opción | Efecto |
|---|---|
| **Llevarse la foto de Ivy en el sótano** | ⟶ ITEM +item_foto_sotano · SOSPECHA +5 *(al día siguiente notarán que falta)* |
| **Dejarlo todo como estaba** | Sin efecto. |

(Pasos en el pasillo. El protagonista vuelve al banco justo a tiempo.)

### J11.05 — La lista · Decisión sobre Len Pike

(La funcionaria vuelve con la carpeta, ya sellada, y una hoja más.)

FUNCIONARIA: Falta un dato. El Subdirector Voss debe firmar la lista definitiva en el Minipax. Llévesela. (Le da la carpeta abierta.) Y esta es la **lista de reserva**, por si alguno de los prisioneros… no estuviera en condiciones para mañana.

(La funcionaria se gira para atender un teléfono. Durante 10 segundos, el protagonista tiene la lista abierta en las manos y una máquina de escribir en el mostrador de al lado.)

PENSAMIENTO: Pike, L. Mañana. En el parque. (Pausa.) La lista de reserva. Si cambio un nombre… otro ocupará su lugar.

#### ◆ D-J11-LEN · Decisión moral

| Opción | Mecánica | Efecto |
|---|---|---|
| **Cambiar a Len por un nombre de la reserva** | Microjuego: tachar "PIKE, L." y escribir a máquina un nombre de la lista de reserva. **El jugador debe elegir cuál.** La lista de reserva tiene 5 nombres con foto. Ninguno conocido. Uno de ellos es un **chico de unos dieciséis años**. | ⟶ `FLAG len_salvado = true` · `FLAG len_sustituto = <nombre elegido>` · DUDA +5 · SOSPECHA +10 · DIARIO +diario_len (variante "cambio") |
| **No tocar nada** | — | ⟶ `len_salvado = false` · DIARIO +diario_len (variante "nada") |
| **Romper la lista** | El protagonista rompe la hoja. | La funcionaria se gira. FUNCIONARIA: "…Tenemos copias, camarada. Siempre tenemos copias." (Llama por teléfono.) ⟶ SOSPECHA +30 · `len_salvado = false` · DIARIO +diario_len (variante "rabia") |

PENSAMIENTO (tras cambiar el nombre, si `len_salvado`): He salvado a un hombre. He matado a otro. Los dos con la misma máquina de escribir. (Pausa.) Ya soy uno de ellos.

**Si `len_salvado` y el sustituto es el chico de dieciséis años:** PENSAMIENTO: Era el más joven. Lo elegí porque no tenía cara de nada. (Pausa.) Lo elegí porque no tenía cara de nada.

### J11.06 — Las Mansiones Victoria · Tarde · Winston

(De regreso. En la calle, delante del portal, hay una furgoneta negra. Vecinos asomados a las ventanas. Hombres de uniforme negro bajan cajas por la escalera. Entre ellos, un **anciano** de pelo blanco y espalda **perfectamente recta**, con uniforme negro, que da órdenes con voz seca y joven: **Charrington**.)

HILDA: (corriendo hacia el protagonista, sin aliento, emocionadísima) ¡{NOMBRE}! ¡Smith! ¡El del séptimo! ¡Lo han cogido! ¡Con una chica! En un cuarto encima de una tienda de antigüedades, en el barrio prole. ¡Llevaban meses! ¡Meses! (Le agarra del brazo.) ¡Yo lo sabía! ¡Lo apunté! ¡Tercera ausencia del mes!

- **[Anciano de uniforme] (CHARRINGTON)** → MIRAR → PENSAMIENTO: Ese hombre… parece un anticuario. Un viejo amable de barrio. Pero da órdenes como Voss. (Pausa.) ¿Cuántos hay como él? ¿Cuántos viejos amables?
  - *(Si `crane_info >= 2`:)* PENSAMIENTO: Un viejo amable con una tienda en el barrio prole. (Pausa.) Una tienda. Un estudio. (El protagonista se queda helado.) No. No puede ser.
  - ⟶ Si `crane_info >= 2`: `FLAG crane_sospechado = true`

(Charrington pasa junto al protagonista al subir a la furgoneta. Le mira un instante, sin ningún interés. Sube. La furgoneta arranca.)

HILDA: (todavía agarrada al brazo) Dicen que la chica era de la Liga Anti-Sex. ¡Anti-Sex! (Ríe, escandalizada.) Ya no se puede fiar una de nadie.

### J11.07 — El piso · Noche

(El protagonista entra. Se queda de pie frente al cartel de Ivy.)

- **[Cartel de Ivy]** → MIRAR →
  - Si `dp_j11_ivy = "recordar"`: PENSAMIENTO: Te pusieron en la pared para que yo te odiara a ti también sin saberlo. Para que gritara contra Goldstein con tu cara. Y yo grité. Cinco años. (Pausa.) No eras su mártir. Eras de los nuestros. Eras de los suyos. (Pausa.) Eras tuya.
  - Si `dp_j11_ivy = "aceptar"`: PENSAMIENTO: Traidora. (Pausa.) Traidora. (La palabra suena hueca.) El Partido me protegió.
- **[Cartel de Ivy]** → USAR → *(solo si `dp_j11_ivy = "recordar"`)*

#### ◆ D-J11-CARTEL

| Opción | Efecto |
|---|---|
| **Arrancar el cartel** | (El protagonista lo arranca de un tirón. El diario cae al suelo. Detrás del cartel, la pared desnuda tiene una mancha más clara con su forma.) ⟶ SOSPECHA +15 *(la telepantalla lo ha visto)* · TELEPANTALLA: "{NUM} {APELLIDO}. Los símbolos del Partido no se destruyen." ⟶ `FLAG cartel_arrancado = true`. El diario necesita un nuevo escondite (el hornillo). |
| **Dejarlo** | PENSAMIENTO: No. Sigue siendo su cara. Aunque no lo sea. ⟶ Sin efecto. |

- **[Hueco junto al armario]** → USAR con **item_diario** → *Nuevas entradas:*

**`diario_ivy_verdad`**
- a) *"Ivy era de la Hermandad. La mataron para que no fuera mártir de nadie, y la hicieron mártir de ellos."*
- b) *"'Alta capacidad de odio canalizable.' Eso dice mi expediente. Eso soy."*
- c) Si `dp_j11_ivy = "aceptar"`: *"Ivy era una traidora. El Partido me protegió. Lo escribo para creerlo."*

**`diario_len`**
- variante "cambio": *"Cambié un nombre por otro. Un hombre vivirá. Otro morirá en su lugar. Elegí con la misma máquina con que escribía partes."*
- variante "nada": *"Tuve la lista en las manos diez segundos. No hice nada. Diez segundos."*
- variante "rabia": *"Rompí la lista. Tienen copias. Siempre tienen copias."*

### J11.08 — Fragmento IV · *Capítulo I: La ignorancia es la fuerza* (parte 2)

(Al esconder el diario, el protagonista encuentra entre sus páginas unas hojas mecanografiadas que no estaban ahí. Alguien ha entrado en su piso.)

PENSAMIENTO: ¿Quién…? ¿Cuándo…? (Pausa.) Los proles también limpian. (Pausa.) No. Aquí no limpia nadie. (Mira la telepantalla.) Alguien que sabe cuándo no mira.

> *Capítulo I — La ignorancia es la fuerza (continuación)*
>
> *El Partido no se hereda. Un hijo del Partido Interior puede caer al Exterior, y un prole especialmente dotado puede ser elevado al Partido Exterior, separado de su familia, reeducado, y convertido en el más leal de los funcionarios.* <u>[subrayado si `brooke_revelada`: "Mi hermano está en esa lista"]</u> *Lo que perpetúa al Partido no es la sangre. Es la mentalidad.*
>
> *Y esa mentalidad depende de una sola cosa: que el pasado sea maleable. Si el pasado existe solo en los documentos y en la memoria, quien controla los documentos y la memoria controla el pasado. Los documentos se queman. La memoria se disciplina.* <u>[subrayado: el reloj de Ivy · el Times original]</u>
>
> *No hay crimen más grave en Oceanía que recordar con exactitud. Un reloj parado es un acto de rebeldía.*

⟶ ITEM item_libro (fragmentos: 4/4) · DIARIO +diario_libro_pasado

PENSAMIENTO: "Un reloj parado es un acto de rebeldía." (Saca el reloj de Ivy.) Nunca le di cuerda. Pensé que era por pena. (Pausa.) Era otra cosa.

**`diario_libro_pasado`**
- a) *"Un reloj parado es un acto de rebeldía. Llevo cinco años de rebeldía en un estante."*
- b) *"El pasado está en los documentos y en la memoria. Los documentos se queman."*

CARTEL: **JORNADA 12**

---

## JORNADA 12 — La oferta

### J12.01 — Parque de la Victoria · Mañana · La ejecución

(No es opcional. Toda la plantilla del Minipax tiene asistencia obligatoria. El parque está lleno. Familias con niños, vendedores de cacahuetes. Los niños de los Espías en primera fila, con los hijos de Parsons y Hilda. Un patíbulo con cinco cuerdas.)

**Si `len_salvado`:**

(Suben los prisioneros. El protagonista los reconoce de la lista: Chen, Koval, Hogan… y en el lugar de Pike, el sustituto que eligió.)

PENSAMIENTO: (si el sustituto es el chico) Dieciséis años. No tenía cara de nada. Ahora tiene cara.

(Entre la multitud, al fondo, el protagonista ve a **Dot**. Está sola, con un pañuelo en la cabeza. Mira el patíbulo. No llora. Luego mira al protagonista, y en sus ojos hay algo que el protagonista no sabe leer: si es gratitud o terror.)

⟶ `dot_confianza +2` *(Dot sabe que Len no está en el patíbulo y sospecha por qué.)*

**Si no `len_salvado`:**

(Suben los prisioneros. El cuarto es **Len Pike**. Con el ancla en el cuello. Busca algo entre la multitud con los ojos.)

(Entre la multitud, Dot. Grita. Es el único grito de dolor en una multitud que grita de júbilo. Dos hombres la sujetan.)

PENSAMIENTO: Diez segundos. Tuve la lista diez segundos.

**En ambos casos:**

#### CF-J12-EJECUCION · `CF[Júbilo, difícil]`

PENSAMIENTO (ráfagas):
- Estibadores. Capturados en Manchuria.
- El padre de Billy Hogan. Billy tiene cuarenta trozos de metralla. Ahora tiene un padre menos.
- Júbilo. Júbilo. Que no se me note.

⟶ Si falla: SOSPECHA +10.

(Las trampillas se abren. Corte a negro antes de verlo. Solo el sonido: la madera, la multitud que ruge y, después, un niño que aplaude.)

### J12.02 — Departamento de Partes y Cartografía · El carrito vacío

(El protagonista llega al Minipax. En el pasillo, junto al cuarto de suministros, está el **carrito de Nell**. Abandonado. Un cubo volcado, lejía derramada. Nadie lo recoge.)

- **[Carrito]** → MIRAR → PENSAMIENTO: El carrito de Nell. (Pausa.) Nadie lo mira. Nadie la mira nunca. Y ahora tampoco miran que no esté.
- **[Carrito]** → USAR → (El doble fondo está vacío. Solo hay un trozo de papel arrugado con algo escrito a lápiz, en letra rápida:) *"No vengas a La Campana."*
  ⟶ `FLAG nell_aviso = true`

(Brooke se acerca a la máquina de café, junto al protagonista. Ninguno de los dos se mira.)

BROOKE: (casi sin voz) Mi hermano no estaba en el patíbulo. *(Si `len_salvado`:)* Sé lo que hizo. No sé si darle las gracias. Había un chico… (Se calla.) *(Si no:)* Mi hermano estaba en el patíbulo. (Pausa.) No le culpo. No podía hacer nada. Ninguno podemos.

BROOKE: (en ambos casos) A Nell se la llevaron anoche. Y a Barlow, el de La Campana. Alguien estaba en ese sótano, además de ustedes tres. (Pausa.) Váyase a casa por la ruta de siempre. No se pare en ningún sitio. Y no hable con nadie amable.

⟶ DUDA +5 · Si `crane_sospechado`: PENSAMIENTO: "Nadie amable." Crane.

### J12.03 — Un sobre en el tubo

(El protagonista vuelve a su mesa. El tubo neumático silba. Sale un cilindro. Dentro no hay una directiva, sino un **sobre de papel marrón**, idéntico al de la foto restaurada de Ivy.)

(Dentro del sobre hay una **fotografía**: el sótano de La Campana, la vela, Nell, Barlow… y el protagonista, de perfil, respondiendo a las preguntas de la iniciación. Tomada desde un ángulo bajo, a través del hueco de la pared.)

(Al dorso, a lápiz, con letra elegante:)

CARTEL (nota):
```
Una imagen vale más que mil palabras.
Aunque tengo también las palabras.
Calle Cable, 7. Esta noche, a las diez. Venga sol{o|a}.
Su amigo,
A. C.
```

PENSAMIENTO: El mismo ángulo. (Saca la foto del expediente de Ivy, si la tiene, y las pone una al lado de la otra.) El mismo ángulo. El mismo hueco en la pared. (Pausa.) Hace cinco años ya estaba ahí.

⟶ `FLAG crane_revelado = true`

**Si `item_foto_sotano`:** ⟶ DUDA +5 · PENSAMIENTO: Crane hizo la foto de Ivy. Crane la mató antes que Voss.

#### ◆ D-J12-HUIR · ¿Acudir a la cita?

| Opción | Efecto |
|---|---|
| **Acudir** | → J12.04 (la opción "natural": el protagonista necesita saber). |
| **No acudir y huir directamente a casa de Dot** | → J12.06 directamente, sin conversación con Crane. Crane lo considera una negativa. ⟶ `crane_decision = "huir"` |

### J12.04 — Estudio Crane · 22:00 · La trastienda

(El estudio está a oscuras salvo la bombilla roja del cuarto oscuro, que ahora está **abierto**. Crane, en mangas de camisa, sirve té. Como siempre.)

CRANE: Pase, pase. Siéntese. El té está recién hecho. (Sonríe.) Usted y yo tenemos mucho de qué hablar. Y por fin podemos hacerlo con sinceridad.

(El cuarto oscuro, visto por la puerta abierta: cubetas de revelado, fotos colgadas de pinzas… y una **máquina de grabación de cinta** con bobinas, cables que salen por un agujero de la pared y un panel con nombres: *LA CAMPANA · MERCADO · MANSIONES VICTORIA 7º · MANSIONES VICTORIA {piso del protagonista}*.)

- **[Panel de la grabadora]** → MIRAR → PENSAMIENTO: Mi piso. (Pausa.) Mi piso está en ese panel.

CRANE: (sigue la mirada) Ah, sí. No se preocupe por eso. La telepantalla no siempre lo oye todo. Yo sí. (Pausa.) Pero no se ofenda. Escucho a todo el mundo. Es mi oficio. Igual que el suyo es corregir el pasado.

(Crane enciende la grabadora. Se oye la voz de Nell: "¿Estás dispuesto a dar tu vida?". Y la voz del protagonista: "{iniciacion_vida}".)

CRANE: (la apaga) Tiene buena voz. Firme. (Pausa.) La vieja Hask está en el Minimor desde anoche. No dice nada. Las viejas nunca dicen nada. Barlow ya ha dicho bastante, aunque poco útil. (Pausa.) Usted, en cambio, puede decirme mucho.

#### Lo que Crane sabe (según `crane_info`)

- `crane_info = 0`: CRANE: "Es usted una persona muy reservada. Eso me gustó desde el principio. Pero la grabación habla por usted."
- `crane_info >= 1`: CRANE: "Su hermana cantaba *Naranjas y limones*. Me lo dijo usted. No hacía falta: yo la fotografié cantándola."
- `crane_info >= 3`: CRANE: "Me contó usted, en esta misma silla, que ya no sabía lo que era su hermana. Yo sí lo sabía. Yo lo supe antes que nadie."

#### La oferta

CRANE: Le propongo algo sencillo. Usted me dice quién más. La mujer del mercado, Dot. Su marido. *(Si `len_salvado`: "Su marido, al que usted tuvo la amabilidad de retirar de la lista. Lo sé. Yo también tengo copias.")* Y una cosa más. (Se inclina hacia delante.) La vieja Hask hablaba de "San Clemente". De "las campanas". Usted sabe dónde está el viejo. O lo sabrá. (Pausa.) Usted me ayuda a encontrarlo y su expediente desaparece. Nadie recordará nunca que usted dudó. Ni siquiera usted. (Sonríe.) Eso también se puede arreglar.

PROTAGONISTA: ¿Y si me niego?

CRANE: (sorbe el té) Entonces mañana su foto estará en la mesa de Voss. Y Voss tiene mucha prisa por cerrar el expediente de su familia. (Pausa.) Lleva cinco años esperándolo.

#### ◆ D-J12-CRANE · Decisión clave del Acto III

| Opción | Texto | Resultado |
|---|---|---|
| **Aceptar el trato** | "…¿Qué quiere saber?" | → **FINAL B — "El fotógrafo"** (versión completa). ⟶ `crane_decision = "aceptar"` |
| **Fingir que acepta** | "Deme un día. Le traeré lo que quiere." | CRANE: (sonríe, sin creérselo del todo) "Un día. Ni una hora más." ⟶ `crane_decision = "fingir"` · `FLAG crane_sigue = true` → J12.05-F |
| **Negarse** | "Usted mató a mi hermana." | → J12.05-N ⟶ `crane_decision = "negar"` |

### J12.05-N — Negarse

CRANE: (deja la taza, despacio) No. La mató un cohete. Yo solo hice una foto. (Se levanta.) Siempre hago solo una foto.

(Crane saca un **silbato** del bolsillo del chaleco. Lo hace sonar. Fuera, botas y gritos.)

→ J12.06 (persecución), con dificultad **alta** (patrullas ya en la calle).

### J12.05-F — Fingir

(El protagonista sale del estudio. La calle Cable, de noche, está vacía. Demasiado vacía. Al girar la esquina, ve una sombra con sombrero que le sigue a distancia.)

PENSAMIENTO: Me sigue. Un día, dijo. Me va a seguir el día entero.

→ J12.06 (persecución), con dificultad **media**: hay que despistar a Crane, no huir de patrullas.

### J12.06 — Limehouse · La persecución

**Localización:** callejones de Limehouse de noche. Ropa tendida que se puede usar como cobertura, patios interiores comunicados, escaleras de incendios, tejados bajos, charcos que hacen ruido al pisarlos. Faroles de gas que crean conos de luz.

**Mecánica:** sigilo en tiempo real.
- Las patrullas (o Crane) tienen conos de visión y oído (pisar un charco o tirar un cubo atrae a la patrulla).
- **Escondites:** tras sábanas tendidas, en portales, bajo escaleras.
- **Atajos prole:** ciertas puertas solo se abren si `dot_confianza >= 2` (una vecina prole abre y deja pasar: "Corre, corre, por el patio."). Es la recompensa por haber tratado a los proles como personas.
- **Ser atrapado:** SOSPECHA +25 y reinicio desde el último punto de control. Si llega a 100 → Final C.
- Duración: 3–4 minutos.

**Si `crane_decision = "huir"`** (no fue a la cita), la persecución empieza más tarde y es más fácil: Crane aún no ha dado la alarma. La patrulla solo hace una ronda.

(La persecución termina en una puerta verde, con un número 11. La puerta se abre antes de que el protagonista llame.)

### J12.07 — Casa de Dot

**Localización:** cocina pequeña y abarrotada, con una estufa encendida, ropa secándose y un cajón de madera con la **colección de metralla de Sammy**, intacta, en una repisa. Olor a té y a carbón.

(Dot cierra la puerta y echa el cerrojo. Le empuja hacia la despensa.)

**Si `dot_confianza >= 3` (intentó salvar a Sammy, y/o salvó a Len):**

DOT: (seca, rápida, sin vacilar) Dentro. Ni un ruido. (Antes de cerrar la despensa, le mira.) Tú corriste hacia mi niño. *(Si `len_salvado`:)* Y mi Len está vivo en algún sitio. No sé qué hiciste. No me lo digas. (Pausa.) Dentro.

**Si `dot_confianza` entre 1 y 2:**

DOT: Dentro. (Pausa.) Lo hago porque me lo pidió Nell. No por ti.

**Si `dot_confianza = 0`:**

DOT: (le mira largo, con la mano en el cerrojo, y por un instante parece que va a abrir para entregarle) …Dentro. (Pausa.) Nell me hizo prometerlo. Por Nell. Solo por Nell.

(Golpes en la puerta. Voces. Dot abre.)

**Escena desde la despensa (vista a través de las rendijas de la puerta):**

PATRULLERO (o CRANE, si `crane_decision = "fingir"`): ¿Ha visto a alguien de azul?

DOT: ¿De azul? Aquí no vienen los de azul. Solo vienen a contar muertos. (Pausa.) A mi niño ya lo contaron.

(Silencio. Pasos que se alejan.)

**Si `crane_decision = "fingir"`:** CRANE: (en la puerta, mirando la cocina con calma, la colección de metralla) "Bonita colección." (Pausa.) "Volveré." *(Se va. Sabe que el protagonista está ahí. Le deja ir porque quiere que le lleve hasta el viejo.)*

⟶ `FLAG crane_sigue = true` *(en cualquier caso, si fingió)*

### J12.08 — El mensaje de Nell

(Dot abre la despensa. Le da un vaso de agua. Se sienta frente a él a la luz de la estufa.)

DOT: Nell vino hace tres noches. Me dejó esto. Dijo que si alguna vez venías a mi puerta, era porque ella ya no podía venir a la tuya.

(Le da un paquete envuelto en tela de flores. Dentro:)

1. **Los dibujos de Amory**: los mapas que Nell sacó de su papelera en la Jornada 3. Al mirarlos de cerca, no son mapas de Malabar. Son planos de las **líneas de metro cerradas** bajo Londres. Los **pájaros** de los márgenes marcan pozos de ventilación, salidas y estaciones tapiadas. ⟶ ITEM +item_dibujos_amory
   PENSAMIENTO: Pájaros. "Señales para el enemigo", confesó. (Pausa.) Eran señales. Pero no para Eurasia. Felix dibujaba la ciudad que había debajo. Para él. Para nadie. Para mí.
   ⟶ DUDA +5
2. **Una nota de Nell**, escrita a lápiz con letra lenta:

CARTEL (nota):
```
San Clemente. Bajo las campanas.
Los cohetes no caen donde no quieren que caigan.
Usa lo que sabes.
Él te está esperando. Le hablé de ti.
Le dije que eras como ella.
                                       N.
```

PENSAMIENTO: "Usa lo que sabes." (Pausa.) La Planilla Azul. Sé dónde caerán los cohetes esta semana. (Pausa.) Sé dónde no caerán.

⟶ `FLAG mensaje_nell = true`

DOT: (se levanta, coge un trozo de metralla de la colección de Sammy, el brillante, y se lo pone en la mano) Para que te dé suerte. Él decía que nunca te cae un cohete donde ya tienes uno.

*(Si el protagonista ya tiene `item_metralla_brillante`:)* (El protagonista abre la otra mano. Tiene el trozo brillante, el que Sammy recogía en el mercado.) DOT: (lo mira; se le quiebra la voz por primera vez) …Ese era el que más quería. (Le cierra la mano sobre los dos.) Llévatelos.

DOT: Al amanecer el metro de Shadwell está sin vigilancia. Lo cerraron "por reformas". (Escupe a un lado.) Nunca reforman nada.

#### Cierre del acto

(Madrugada. El protagonista en la despensa, sin dormir, con el diario en las rodillas y la luz de la estufa entrando por la rendija.)

- **[Diario]** → USAR → *Entrada desbloqueada:*

**`diario_dot`**
- a) *"Una mujer a la que le mataron a su hijo me ha escondido en su despensa. No sé si la merezco."*
- b) *"Los proles no necesitan conspirar. Solo necesitan abrir una puerta."*

PENSAMIENTO:
- Si `dp_j11_ivy = "recordar"`: Mañana bajo las campanas. (Saca el reloj de Ivy.) Nunca le di cuerda. (Pausa larga.) Le da cuerda. El reloj empieza a andar. **Tic. Tic. Tic.** *(Primer sonido de reloj en todo el juego.)*
  ⟶ `FLAG reloj_en_marcha = true`
- Si `dp_j11_ivy = "aceptar"`: Mañana bajo las campanas. (Saca el reloj de Ivy.) Nueve y cuarenta. (Lo guarda.) No sé por qué voy. Ya no sé nada. Solo que no puedo volver.

CARTEL: **FIN DEL ACTO III**

CARTEL: **ACTO IV — CAPÍTULO II**

---

## Resumen de variables del Acto III

| Variable | Valores | Se fija en |
|---|---|---|
| `pista_combinacion` | bool | J8.02 |
| `planilla_vista` | bool | J8.06 |
| `hoja_robada` | bool | J8.06 |
| `nell_confianza` | −5 a +1 | J8.08 |
| `iniciacion_vida`, `_matar`, `_mentir`, `_callar`, `_ivy`, `_traicion` | sí / no | J8.08-I |
| `times_original` | bool | J9.06 |
| `prueba_rectificacion` | bool | J10.04 |
| `brooke_revelada` | bool | J11.01 |
| `lista_proles_vista` | bool | J11.02 |
| `ivy_revelada` | bool | J11.04 |
| `dp_j11_ivy` | `aceptar` / `recordar` | J11.04 |
| `len_salvado`, `len_sustituto` | bool / texto | J11.05 |
| `crane_sospechado` | bool | J11.06 |
| `cartel_arrancado` | bool | J11.07 |
| `nell_aviso` | bool | J12.02 |
| `crane_revelado` | bool | J12.03 |
| `crane_decision` | `aceptar` / `fingir` / `negar` / `huir` | J12.03–J12.04 |
| `crane_sigue` | bool | J12.05-F / J12.07 |
| `mensaje_nell` | bool | J12.08 |
| `reloj_en_marcha` | bool | J12.08 |

**Inventario nuevo:** copia u hoja de la Planilla Azul, libro (4/4 fragmentos), *Times* original, chapa del archivo, foto del sótano, dibujos de Amory, metralla brillante (de Dot).

**Entradas de diario nuevas:** `diario_planilla`, `diario_libro_guerra`, `diario_times`, `diario_libro_ignorancia`, `diario_amory_confesion`, `diario_estasia`, `diario_libro_doblepensar`, `diario_ivy_verdad`, `diario_len`, `diario_libro_pasado`, `diario_dot`.

## Semillas recogidas en este acto

| Semilla (de dónde) | Se recoge en |
|---|---|
| Reloj de Ivy, 21:40 (Prólogo) | J9.06 (*Times* original) · J12.08 (le da cuerda) |
| Silueta del oficial (Prólogo) | J11.04 (Voss) |
| "No les creas" (Prólogo) | J11.04 |
| Hija de Parsons: "Dice un nombre" (J2) | J10.06 |
| Agujeros de alfiler (J2) | J10.04 (Gran Rectificación) |
| Brooke: "Y usted tampoco" (J3); foto de boda en el estudio de Crane (J5) | J11.01 (Len es su hermano) |
| Dibujos de pájaros de Amory (J3) | J12.08 (planos del metro) |
| Stepney "al borde" (J5) | J11.04 (objetivo programado) |
| Cuarto oscuro con zumbido (J6) | J12.04 (grabadora) |
| Hilda en el despacho de Voss (J7) | J10.01 |
| Nell: "Cuidado con la gente amable" (J7) | J12.02–J12.04 |
| Telepantalla retirada del cuarto de suministros (J7) | *Pendiente para Acto IV o eliminar* |
| Metro "cerrado por reformas" (J4) | J12.08 → J13 |

## Semillas para el Acto IV

| Semilla | Uso previsto |
|---|---|
| `crane_sigue` | Crane aparece en los túneles (J13). El Final D llega antes y con menos margen. |
| Respuestas de la iniciación | O'Brien las reproduce en el Minimor (Finales C y D). |
| Lápiz de Amory | Se usa para escribir el Capítulo II. |
| `reloj_en_marcha` | En el Final D, el reloj sigue andando en el epílogo. |
| Campana de "S. Clem…" del pub | Barlow la había rescatado de San Clemente. Se reencuentra en la cripta. |
| `len_salvado` | Len aparece en el epílogo del Final D (con Dot y el libro). |
| `cartel_arrancado` | En el Final C, O'Brien tiene el cartel en su despacho, perfectamente restaurado. |

## Ajustes a la biblia ([guion.md](../guion.md)) introducidos aquí

- **Brooke es hermana de Len Pike**, el marido de Dot. Es una prole elevada al Partido Exterior de niña.
- **Len Pike era correo de la Hermandad.** Dot no es miembro, pero lo sabe.
- **Tom Barlow**, tabernero de La Campana, es miembro de la célula. Lo detienen con Nell.
- **El micrófono de Crane en el sótano de La Campana lleva ahí al menos cinco años.** Hizo la foto de Ivy en 1979.
- **El expediente de Ivy revela que el destino del protagonista en el Minipax fue diseñado** por Voss ("alta capacidad de odio canalizable").
- **Los dibujos de pájaros de Amory son planos del metro cerrado.** Así se llega a San Clemente.
- **Decisión moral nueva en J11:** salvar a Len cambiando su nombre por el de otro prisionero de la lista de reserva.
- **Opción de "fingir"** ante Crane en J12: Crane sigue al protagonista hasta el Acto IV.
- **Dot no es miembro de la Hermandad**, pero esconde al protagonista y le entrega el mensaje de Nell y los dibujos de Amory.
