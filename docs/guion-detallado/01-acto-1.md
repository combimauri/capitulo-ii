# ACTO I — BIENPENSANTE

> Prólogo + Jornadas 1–3 · Duración estimada: ~45 min
> Objetivo narrativo: que el jugador **crea** junto al protagonista. La rutina tiene que sentirse cómoda, casi heroica, antes de que se rompa.
> Notación: ver [00-convenciones.md](00-convenciones.md).

**Estado inicial:** `duda = 0` · `sospecha = 0`

---

## PRÓLOGO — Calle Stepney, 1979

### P.01 — Los escombros

**Localización:** calle estrecha de casas obreras, de noche. Polvo en suspensión, fuego al fondo. Media fachada derrumbada. Una telepantalla arrancada de la pared, boca abajo entre los cascotes, todavía encendida.

(Pantalla en negro. Silbido de cohete, cada vez más agudo. Silencio absoluto durante un segundo. Impacto. Pitido en los oídos.)

CARTEL: **Calle Stepney. Franja Aérea 1. 1979.**

(Fundido. El protagonista, años más joven, se incorpora entre los escombros. Tose. Camina con dificultad.)

TELEPANTALLA: (distorsionada, entrecortada) …cobarde ataque… euroasiático… población civil… el Partido… venganza…

**Puntos interactivos:**

- **[Telepantalla rota]**
  - MIRAR → PENSAMIENTO: Sigue hablando. Incluso aquí sigue hablando.
- **[Fuego al fondo]**
  - MIRAR → PENSAMIENTO: Nuestra casa. Eso era nuestra casa.
- **[Montón de cascotes]** *(objetivo)*
  - MIRAR → PENSAMIENTO: Algo se mueve debajo.
  - USAR → Microjuego: tocar o arrastrar los cascotes para apartarlos (5–6 piezas). Debajo aparece **una mano**.

### P.02 — Ivy

(Bajo una viga, el rostro de Ivy, cubierto de polvo. Respira con dificultad. Lleva el mono azul del Partido.)

> **Nota:** el protagonista tiene una edad fija de 34 años en 1984 (29 en el prólogo). Ivy era cinco años menor y muere con 24.

PROTAGONISTA: ¡Ivy! ¡Ivy, mírame! Te voy a sacar, ¿me oyes? Te voy a sacar.

IVY: (casi un susurro, intenta sonreír) Naranjas y limones… dicen las campanas de San Clemente…

PROTAGONISTA: No cantes. No gastes aire.

IVY: {NOMBRE}… escúchame. No les creas. No les…

(Ivy deja de hablar. Su mano cae. En su muñeca, un reloj con el cristal roto.)

**Punto interactivo:**

- **[Reloj de Ivy]**
  - MIRAR → PENSAMIENTO: Las nueve y cuarenta. Se ha parado a las nueve y cuarenta.
  - USAR → ⟶ ITEM +item_reloj_ivy

(Llegan siluetas desde el fondo: vecinos proles. Una mujer joven con pañuelo en la cabeza, **Nell**, aunque el jugador no lo sabe, se lanza a apartar cascotes con las manos desnudas.)

MUJER PROLE (NELL): ¡Aquí! ¡Hay alguien aquí! ¡Traed una palanca!

(Luz de linterna. Un **oficial del Partido** con abrigo largo aparta a la mujer de un empujón.)

OFICIAL: Apártense. Todos. (Mira a Ivy, luego al protagonista.) Esta camarada ya no les pertenece. Ahora es una mártir del Partido.

(La mujer prole mira al protagonista un instante, muy fijo, antes de desaparecer entre el humo.)

PROTAGONISTA: (sin apartar la vista de Ivy) …Eurasia.

PENSAMIENTO: Eurasia. Eurasia. Eurasia.

(Fundido a blanco.)

> **Nota de dirección:** el oficial lleva un abrigo y un andar que el jugador reconocerá en el Subdirector Voss. Sin primer plano: solo silueta, voz pausada y guantes. La mujer prole es Nell con 5 años menos.

### P.03 — Ficha de Afiliación del Partido

(Pantalla de creación del personaje, presentada como un formulario oficial sobre papel amarillento, con sellos y casillas mecanografiadas. Cada campo se escribe con efecto de máquina de escribir.)

CARTEL: **FICHA DE AFILIACIÓN — PARTIDO EXTERIOR — INGSOC**

| Campo | Entrada |
|---|---|
| Nombre | *(texto libre)* ⟶ `nombre` |
| Apellido | *(texto libre)* ⟶ `apellido` |
| Sexo | Varón / Mujer ⟶ `genero` |
| Edad | **34** *(mecanografiado, no editable)* |
| Número de afiliado | *(generado)* ⟶ `{NUM}` |
| Destino | **Ministerio de la Paz — Departamento de Partes y Cartografía del Frente** *(sellado, no editable)* |
| Familiares | **IVY {APELLIDO}** — *(sello rojo:)* **MÁRTIR. CALLE STEPNEY, 1979.** |
| ¿Ha tenido familiares implicados en crimental? | **NO** *(sellado previamente, no editable)* |

(Al final, una línea de firma.)

CARTEL: **Juro lealtad absoluta al Gran Hermano, al Partido y a los principios sagrados del Ingsoc.**

→ El jugador debe **mantener pulsado** sobre la línea para firmar. Se oye la plumilla.

(Un sello cae sobre la ficha: **APTO**. La ficha se archiva en un tubo neumático con un silbido.)

(Corte a negro. Silbato agudo y prolongado.)

---

## JORNADA 1 — La rutina

### J1.01 — El piso · 07:15

**Localización:** piso pequeño en las Mansiones Victoria. Una cama, una mesa, un hornillo, una estantería casi vacía y una ventana que da a la ciudad. La **telepantalla** ocupa media pared, imposible de evitar. Junto a la ventana, el **cartel de Ivy**: su cara en grabado heroico sobre fondo rojo con el texto *RECUERDA A LOS MÁRTIRES DE LA CALLE STEPNEY*.

(La telepantalla emite el silbato de despertar.)

TELEPANTALLA (INSTRUCTORA): ¡Buenos días, camaradas de entre treinta y cuarenta! ¡Arriba, arriba! ¡Tablas de gimnasia! ¡Brazos arriba! ¡Uno, dos! ¡Uno, dos!

#### CF-J1-GIMNASIA · `CF[Entusiasmo, fácil]` *(tutorial)*

- Microjuego de ritmo: el protagonista imita los movimientos (flechas o toques al compás) mientras mantiene la expresión de **entusiasmo**.
- Tutorial en pantalla:
  > *La telepantalla te ve. Tu cara también habla. Mantén la expresión correcta.*
- A mitad del ejercicio:

TELEPANTALLA (INSTRUCTORA): ¡{NUM} {APELLIDO}! ¡Eso es! ¡Así se mueve un{|a} camarada de verdad! ¡Mirad todos!

PENSAMIENTO: (orgullo) Me ha nombrado. Delante de todo el bloque.

⟶ Si perfecto: `FLAG cf_j1_gimnasia = "perfecto"` · Si falla: SOSPECHA +3 y la instructora dice "¡{NUM} {APELLIDO}! ¡Más energía! ¡Así no se gana una guerra!".

(Termina la gimnasia. El jugador tiene el control.)

**Puntos interactivos:**

- **[Cartel de Ivy]**
  - MIRAR → PENSAMIENTO: Ivy. Cada mañana te lo prometo. Cada mañana. Eurasia pagará cada piedra de la calle Stepney.
  - USAR → (El protagonista toca el borde del cartel.) PENSAMIENTO: Nunca la dibujaron sonriendo. Ella siempre sonreía. Pero así está bien: una mártir no sonríe.
- **[Reloj de Ivy]** *(en la estantería)*
  - MIRAR → PENSAMIENTO: Las nueve y cuarenta. Nunca le he dado cuerda. No quiero que vuelva a andar.
  - USAR → PENSAMIENTO: No. Se queda así.
- **[Telepantalla]**
  - MIRAR → PENSAMIENTO: Se le puede bajar el volumen, pero no apagarla. Nadie querría apagarla. Sería como quedarse a oscuras.
  - USAR → PENSAMIENTO: Está en el volumen justo. El Partido sabe cuál es el volumen justo.
- **[Ventana]**
  - MIRAR → (Vista de la ciudad: tejados ennegrecidos, solares bombardeados y, al fondo, cuatro pirámides blancas enormes.) PENSAMIENTO: Los cuatro ministerios. El de la Verdad, el del Amor, el de la Abundancia. Y el mío: el de la Paz. Desde aquí parecen montañas.
- **[Hornillo]**
  - USAR → (Animación: pan negro y una taza.) PENSAMIENTO: Café de la Victoria. Sabe a tierra mojada. Pero está caliente, y eso es más de lo que tienen en Eurasia.
- **[Puerta]**
  - USAR → *Solo después de desayunar (USAR Hornillo).* → salida a J1.02
  - Si no ha desayunado: PENSAMIENTO: Primero el desayuno. Un estómago vacío es un estómago desleal.

### J1.02 — La escalera de las Mansiones Victoria

**Localización:** escalera estrecha que huele a col hervida y a cañerías viejas. Pintura desconchada. Un cartel enorme del Gran Hermano en cada rellano: *EL GRAN HERMANO TE VIGILA*. En el ascensor, un letrero: *AVERIADO*.

**Punto interactivo:**

- **[Ascensor]**
  - MIRAR → PENSAMIENTO: Averiado. Desde la Semana del Odio pasada. Lo arreglarán cuando termine la guerra. O antes, si Hilda escribe otra carta.

(Bajando, el protagonista se cruza con un hombre delgado de unos cuarenta años que sube despacio, apoyándose en la barandilla. Tose. Lleva el mono azul del Partido.)

- **[Hombre en la escalera] (WINSTON)**
  - MIRAR → PENSAMIENTO: El camarada Smith, del séptimo. Trabaja en el Miniver. Siempre parece que acaba de despertarse de un mal sueño.
  - HABLAR →

PROTAGONISTA: ¡Buenos días, camarada Smith! Hoy hay colecta para la Semana del Odio. ¿Ha visto los carteles nuevos?

WINSTON: (sin levantar mucho la vista) …Sí. Buenos días.

PROTAGONISTA: ¿Vendrá esta noche al Centro de la Comunidad? Vamos a ensayar los cánticos.

WINSTON: Tengo… trabajo atrasado. (Tose.) Quizá.

(Winston sigue subiendo. Se detiene un instante a mirar el cartel del Gran Hermano y aparta la vista enseguida.)

PENSAMIENTO: "Quizá." Un miembro del Partido no dice "quizá".

(Desde abajo sube **Hilda Grubb**, con una lata de colecta y una carpeta llena de listas. Es menuda, enérgica y lleva el pelo tirante.)

HILDA: ¡{NOMBRE} {APELLIDO}! ¡Mi camarada más puntual! (Agita la lata.) Para la Semana del Odio. Este año vamos a hacer la efigie de Goldstein más grande del distrito. ¡Tres metros! ¡Con dientes!

#### ◆ D-J1-COLECTA

| Opción | Texto | Efecto |
|---|---|---|
| A | "Tome. Todo lo que llevo." | `hilda_aprecio +1` · HILDA: "¡Ojalá todo el bloque fuera como tú!" |
| B | "Tome, camarada." (lo normal) | Sin efecto. HILDA: "Gracias, gracias. Cada moneda es un clavo en el ataúd de Goldstein." |

HILDA: (bajando la voz, mirando hacia arriba) ¿Has visto a Smith? Nunca da más de lo justo. Nunca canta. Siempre tiene "trabajo atrasado". (Pausa significativa.) Yo solo lo digo.

#### ◆ D-J1-SMITH *(sin consecuencias mecánicas: sirve para fijar la voz del protagonista)*

| Opción | Texto |
|---|---|
| A | "Tiene razón. Lo vigilaré." → HILDA: "Ese es el espíritu." |
| B | "Estará enfermo. Tose mucho." → HILDA: "Hum. La tos no le impide escribir… lo que sea que escribe." |

HILDA: (vuelve a su tono alegre) ¡Ah! Y esta semana sale el cartel nuevo de los mártires. Tu Ivy sale en primera fila. Deberías estar orgullos{o|a}.

PROTAGONISTA: Lo estoy.

→ salida a J1.03

### J1.03 — La calle · Trayecto al Minipax

**Localización:** avenida gris y ancha. Carteles del Gran Hermano cada pocos metros. Un helicóptero de patrulla pasa entre los edificios y se asoma a las ventanas. Proles por las aceras. Al fondo crece la pirámide blanca del **Ministerio de la Paz**, sin ventanas, rodeada de alambre de espino.

(Escena breve de paseo con 3 puntos interactivos. La música de la calle es el himno del Partido, metálico, desde altavoces.)

- **[Cartel: LA GUERRA ES LA PAZ / LA LIBERTAD ES LA ESCLAVITUD / LA IGNORANCIA ES LA FUERZA]**
  - MIRAR → PENSAMIENTO: Tres verdades. Las aprendí antes de aprender a leer. Ivy las cantaba saltando a la comba.
- **[Helicóptero]**
  - MIRAR → PENSAMIENTO: La Patrulla. No me preocupa: quien no tiene nada que esconder no tiene nada que temer.
- **[Proles discutiendo junto a un puesto]**
  - MIRAR → (Dos proles discuten a gritos sobre un número de lotería.) PENSAMIENTO: Proles. Como animales. El Partido dice que a los proles y a los animales hay que dejarlos en paz. Es generoso por su parte.
- **[Niño prole]** *(se acerca y tira de la manga)*
  - HABLAR → NIÑO: ¿Tiene un cigarrillo, camarada? ¿Una moneda? PENSAMIENTO: Los Cigarrillos de la Victoria son para el Partido. (El protagonista se aparta.) El niño se va silbando. *(Seed de Sammy: el niño colecciona metralla y lleva un trozo colgado al cuello. El jugador lo reconocerá en la Jornada 4.)*

→ salida a J1.04 al llegar a la puerta del Minipax.

### J1.04 — Vestíbulo del Ministerio de la Paz

**Localización:** vestíbulo de mármol, frío y altísimo. Guardias de uniforme negro con porras. Torniquetes. Encima de todo, en letras enormes: **MINISTERIO DE LA PAZ**. Debajo, más pequeño: *La guerra es la paz*.

GUARDIA: Ficha.

→ Microjuego mínimo: el jugador toca la ficha en el inventario y la entrega. El guardia compara la foto con la cara.

GUARDIA: (devuelve la ficha) Departamento de Partes y Cartografía. Planta catorce. El ascensor de la izquierda funciona.

PENSAMIENTO: Aquí los ascensores siempre funcionan.

→ salida a J1.05

### J1.05 — Departamento de Partes y Cartografía del Frente

**Localización:** sala diáfana con decenas de mesas en hileras. Cada mesa tiene un tubo neumático, una máquina de escribir y una telepantalla pequeña. En la pared del fondo, un **mapa enorme del frente de Malabar** clavado sobre corcho, con banderitas rojas (Oceanía) y negras (Eurasia). A un lado, la puerta de cristal esmerilado del **despacho del Subdirector**. Una ranura en la pared: el **agujero de la memoria**.

(El protagonista llega a su mesa. En la mesa de al lado, un hombre joven y flaco de ojos rápidos y gafas redondas está dibujando con la lengua entre los dientes: **Felix Amory**. Se oye el rumor de las máquinas de escribir y algún tubo neumático. La puerta del despacho se abre.)

VOSS: (cuarenta y tantos, abrigo largo aunque está en interiores, guantes, voz suave) Camarada {APELLIDO}. Un momento.

PENSAMIENTO: El Subdirector Voss. Partido Interior. Me habla a mí.

VOSS: Hoy sale el cartel nuevo de los mártires. Su hermana… (deja la frase en el aire un segundo de más) …calle Stepney. Una tragedia. De esas tragedias que nos hacen fuertes.

PROTAGONISTA: Sí, Subdirector. Gracias, Subdirector.

VOSS: El Partido no olvida a los suyos. (Se quita un guante, despacio.) Tiene un parte urgente en su tubo. Malabar. Que sea… memorable.

(Vuelve a su despacho. Amory se gira en cuanto se cierra la puerta.)

AMORY: (en voz baja, emocionado) ¿Te ha hablado Voss? ¿A ti? En dos años a mí solo me ha dicho "su lápiz hace ruido". (Le enseña lo que dibuja: un mapa precioso, con pájaros minúsculos en los márgenes.) Mira. Nueva proyección. Con esta, Oceanía ocupa un cuarenta por ciento más de papel. Y no he mentido en nada, ¿eh? Solo he… estirado el mundo.

#### Diálogo con Amory (opcional, árbol corto)

- **"¿Para qué son los pájaros?"**
  AMORY: Para que los mapas tengan algo vivo. Los quito antes de entregarlos, tranquil{o|a}. (Guiña un ojo.)
- **"¿Eso está autorizado?"**
  AMORY: Todo lo que hace más grande a Oceanía está autorizado. Es casi una ley natural.
- **"Tengo que trabajar."**
  AMORY: ¡El deber! Ve, ve. Malabar no se va a conquistar sola.

#### Minijuego 1: PARTES DE GUERRA *(tutorial)*

(Del tubo neumático sale un cilindro con un papel enrollado.)

CARTEL (directiva, en neolengua):
```
minipax.partes 14.4.84 malabar
victoria plusbuena confirmada
redactar parte · cifras doblemásbuenas
prisioneros euroasiáticos · bajas enemigas
```

**Mecánica:** el parte aparece en la máquina de escribir con huecos. El jugador elige cada hueco entre 3 opciones. Las opciones "correctas" son las más grandilocuentes; las tibias suben ligeramente la Sospecha.

> **PARTE DEL FRENTE · MALABAR**
> Nuestras gloriosas fuerzas han **[avanzado / aplastado al enemigo / resistido]** en el sector del río Malabar, ganando **[4 / 12 / 30]** kilómetros de terreno. Han sido capturados **[800 / 3.000 / 12.000]** prisioneros euroasiáticos. Las bajas enemigas se estiman en **[2.000 / 9.000 / 40.000]**. El Gran Hermano ha felicitado personalmente a las tropas.

- Opción tibia ("avanzado", "resistido") → SOSPECHA +2 cada una. PENSAMIENTO: No. Más fuerza. Ivy merece más fuerza.
- ⟶ `FLAG parte_j1 = {verbo, km, prisioneros, bajas}` con los valores elegidos. *(Reaparecerán alterados en la Jornada 6.)*
- El parte se mete en el tubo de salida. PENSAMIENTO: Esta noche lo leerán en todas las telepantallas de Oceanía. Mis palabras.

(Mientras el protagonista termina, aparece una **limpiadora** con un carrito que vacía las papeleras de las mesas, una por una, sin levantar la cabeza.)

- **[Limpiadora] (NELL)**
  - MIRAR → PENSAMIENTO: Una prole de la limpieza.
  - *(No hay más acciones disponibles. Si el jugador intenta tocarla de nuevo:)* PENSAMIENTO: Tengo trabajo.

> **Nota de dirección:** Nell se detiene medio segundo más en la papelera de Amory. Nadie más que el jugador atento lo notará.

**Puntos interactivos de la sala:**

- **[Mapa del frente]**
  - MIRAR → PENSAMIENTO: Malabar. Nuestras banderas rojas avanzan como sangre limpia. Las negras retroceden. Así es la historia.
- **[Agujero de la memoria]**
  - MIRAR → PENSAMIENTO: Lo que cae ahí deja de existir. Los borradores, los errores… Es higiénico.
- **[Despacho de Voss]**
  - USAR → PENSAMIENTO: No se entra sin ser llamad{o|a}.

### J1.06 — Cantina del Minipax · Mediodía

**Localización:** comedor de techo bajo, mesas metálicas y bandejas. Huele a guiso y a ginebra. Una telepantalla grande emite cifras de producción.

(El protagonista se sienta con Amory. Guiso gris y un vaso de Ginebra de la Victoria.)

AMORY: (con la boca llena) ¿Sabes lo que es un buen mapa? (No espera respuesta.) Un buen mapa no muestra dónde están las cosas. Muestra dónde el Partido necesita que estén. Es lo más bonito que existe.

PROTAGONISTA: Lo dices como si fuera poesía.

AMORY: ¡Es que lo es! (Entusiasmado.) En la próxima edición del Diccionario quitan "retirada". Ya no existirán las retiradas. Solo "avances rectificados". ¿No es precioso? Si no hay palabra, no hay retirada. Si no hay retirada…

PROTAGONISTA: …siempre ganamos.

AMORY: ¡Siempre ganamos! (Brinda con la ginebra.) Por Malabar.

PENSAMIENTO: Amory habla demasiado rápido. Pero es de los buenos. De los que creen.

TELEPANTALLA: …la producción de botas en el último trimestre ha superado el plan en un noventa y ocho por ciento…

→ Fundido a J1.07 (resumen de la tarde con un cartel: *"La tarde pasa entre partes y banderitas."*)

### J1.07 — El piso · Noche

(El protagonista vuelve a casa. La telepantalla emite el noticiero.)

TELEPANTALLA: ¡Atención! ¡Atención! ¡Noticia gloriosa del frente de Malabar! (Fanfarria.) Nuestras gloriosas fuerzas han {parte_j1.verbo} en el sector del río Malabar, ganando {parte_j1.km} kilómetros…

(El texto es exactamente el que redactó el jugador.)

#### CF-J1-NOTICIA · `CF[Júbilo, fácil]`

PENSAMIENTO: (en `[D0]`, siempre en el Acto I) Son mis palabras. Las está diciendo toda Oceanía. Ivy, ¿lo oyes? Esto es por ti.

**Puntos interactivos (opcional antes de dormir):**

- **[Cartel de Ivy]** → MIRAR → PENSAMIENTO: Hoy hemos ganado {parte_j1.km} kilómetros. Mañana ganaremos más.
- **[Cama]** → USAR → fin de la jornada.

(Fundido. Rótulo de jornada.)

CARTEL: **JORNADA 2**

---

## JORNADA 2 — Dos Minutos de Odio

### J2.01 — El piso · 07:15

(Silbato. Gimnasia, más corta. `CF[Entusiasmo, fácil]`.)

TELEPANTALLA: ¡Buenas noticias de la Minindancia! Gracias al esfuerzo de nuestro pueblo, la ración de chocolate **aumenta** a veinte gramos semanales. ¡Gracias, Gran Hermano!

PENSAMIENTO: Veinte gramos. ¡Veinte! El Partido cuida de nosotros.

> **Semilla:** no hay manera de saber todavía que la ración era de treinta. En la Jornada 6, un recorte de periódico viejo en el estudio de Crane lo menciona. El jugador atento atará cabos.

- **[Puerta]** → salida a J2.02

### J2.02 — La escalera · Los Parsons

(En el rellano del cuarto piso, la puerta de los Parsons está abierta. Dentro hay escándalo. Dos niños con uniforme de los **Espías** (pantalón corto azul, pañuelo rojo) juegan a ahorcar a un muñeco con una cuerda.)

NIÑO PARSONS: ¡Traidor! ¡Espía euroasiático! ¡A la horca!

(Aparece **Parsons**: gordo, sudoroso y radiante, con una pila de banderines bajo el brazo.)

PARSONS: ¡Camarada {APELLIDO}! ¡Magnífico, magnífico! ¿Has visto a mis pequeños? Llevan toda la semana pidiendo ir al ahorcamiento de prisioneros del parque. Les he dicho que si se portan bien… (Le da un banderín.) ¡Para la Semana del Odio! Estoy en el comité de banderines.

PROTAGONISTA: Gracias, camarada Parsons. Sus hijos son un ejemplo.

PARSONS: ¡Lo son! ¡Lo son! El mes pasado la pequeña denunció a un vendedor de cordones. ¡Por sus zapatos! Decía que eran zapatos extranjeros. Tenía un ojo… (Se ríe con orgullo.)

(La **hija de Parsons**, de unos nueve años, se acerca y mira fijamente al protagonista.)

HIJA PARSONS: Usted habla dormid{o|a}.

PROTAGONISTA: …¿Qué?

HIJA PARSONS: Por la noche. A través de la pared. Dice un nombre.

PARSONS: (riendo, la aparta) ¡Ja, ja! ¡Qué imaginación! Venga, venga, a vestirse.

PENSAMIENTO: Un nombre. Ivy, seguramente. No es ningún crimen soñar con una mártir.

⟶ SOSPECHA +2 *(la niña lo apunta en una libretita; detalle visible si el jugador se fija)*

→ salida a J2.03

### J2.03 — Gran Salón del Ministerio de la Verdad · Dos Minutos de Odio

CARTEL: *Sesión conjunta de los cuatro ministerios. Aniversario de la Victoria de Malabar.*

**Localización:** gran salón del Miniver, con hileras de sillas frente a una telepantalla gigantesca. Delegaciones de los cuatro ministerios. Amory está junto al protagonista. Unas filas más allá, **una mujer joven y morena con la faja escarlata de la Liga Juvenil Anti-Sex** (**Julia**). Más cerca de la pantalla, **un hombre corpulento con gafas, del Partido Interior** (**O'Brien**). **Winston** en otra fila.

(Puntos interactivos solo antes de que empiece, durante unos segundos:)

- **[Mujer de la faja escarlata] (JULIA)** → MIRAR → PENSAMIENTO: Liga Anti-Sex. Esas chicas son las más ortodoxas de todas. Da gusto verlas.
- **[Hombre del Partido Interior] (O'BRIEN)** → MIRAR → PENSAMIENTO: Partido Interior. Se ajusta las gafas de una forma… casi amable. Como un aristócrata de los libros de historia, antes de que la Revolución los barriera.
- **[Winston]** → MIRAR → PENSAMIENTO: Smith. Al menos ha venido.

(Las luces bajan. Un chirrido metálico insoportable sale de la telepantalla. Aparece el rostro de **Emmanuel Goldstein**: perilla blanca, gafas, cara de intelectual, voz de oveja balando.)

#### CF-J2-ODIO · `CF[Odio, media → difícil]` *(primer gran crimen facial)*

**Estructura del microjuego (~90 s):**

1. **Primer minuto:** Goldstein habla: libertad de expresión, paz con Eurasia, libertad de prensa. Tras él marchan columnas de soldados euroasiáticos. El jugador mantiene la cara de **Odio** mientras la barra de intensidad del público sube. Hay que pulsar al ritmo de los gritos.
2. **Segundo minuto:** el rostro de Goldstein se transforma en una oveja y luego en un soldado euroasiático que avanza hacia la pantalla. Ritmo más rápido.
3. **Clímax:** la mujer de la faja escarlata **lanza un diccionario de neolengua** contra la pantalla. El público grita.
4. **Desenlace:** aparece el rostro del **Gran Hermano**, sereno. El público entona "¡G-H!… ¡G-H!…". La expresión cambia a **Duelo patriótico** (veneración) y hay que acertar el cambio a tiempo.

Durante el microjuego, el monólogo interior aparece en ráfagas:

PENSAMIENTO: Goldstein. Goldstein. Tú diste la orden. Tú y tus perros. La calle Stepney. La mano de Ivy. ¡Te arrancaría los ojos con mis propias manos!

- ⟶ Perfecto: `FLAG cf_j2_odio = "perfecto"`. Al terminar, O'Brien mira de reojo al protagonista un instante. *(Nadie sabrá nunca si fue aprobación o archivo.)*
- ⟶ Fallo: SOSPECHA +5 (o +10 si falla la transición al Gran Hermano).

> **Detalle de Amory:** si el jugador lo mira durante el clímax, Amory grita, pero en el último tramo se queda callado limpiándose las gafas. Solo un segundo.

(Las luces vuelven. El público, agotado y sudoroso, se dispersa.)

AMORY: (todavía jadeando, sonríe) Uf. Siempre me deja como si hubiera corrido diez kilómetros. Tú gritabas de verdad, ¿eh? Te vi. Daba miedo.

PROTAGONISTA: Es lo mínimo que le debo a Ivy.

AMORY: (más serio, un momento) Claro. Claro que sí.

→ salida a J2.04

### J2.04 — Departamento de Partes y Cartografía · La broma

(De vuelta en el Minipax. Llega una directiva por el tubo.)

CARTEL (directiva):
```
minipax.carto 15.4.84 malabar
avance 12km confirmado · desplazar línea frente
ref parte 14.4.84
```
*(Si `parte_j1.km` ≠ 12, la directiva usa el valor que eligió el jugador.)*

#### Minijuego 2: MOVER EL FRENTE *(tutorial)*

**Mecánica:** primer plano del mapa de Malabar sobre corcho. El jugador arrastra las banderitas rojas según la directiva y la línea del frente se redibuja. Un indicador de escala muestra los kilómetros desplazados.

**Detalle visual clave:** el corcho alrededor del río Malabar está **lleno de agujeros de alfiler**, cientos y cientos, concentrados en la misma franja a ambos lados del río. Al hacer zoom se ven claramente. Las banderitas nunca se alejan de esa franja más que unos milímetros.

(El jugador termina de colocar las banderas. Amory se inclina sobre el mapa, en voz muy baja y con una sonrisa traviesa.)

AMORY: ¿Te has fijado en que el frente de Malabar lleva tres años en el mismo río? (Señala con el lápiz.) Mira los agujeros. Este mapa tiene más agujeros que un queso de la Minindancia. Avanzamos doce, retrocedemos… perdón, rectificamos doce. Avanzamos doce. Si sumas todos los partes del año, ya deberíamos estar desayunando en Pekín.

(Se ríe por lo bajo. Luego le pasa el lápiz al protagonista sin pensarlo.)

AMORY: Toma, usa el mío. El tuyo no tiene punta. Que no se diga que Cartografía no comparte.

⟶ ITEM +item_lapiz_amory *(lápiz mordido con las iniciales **F.A.** grabadas con la uña)*

PENSAMIENTO: (la telepantalla de la mesa está encendida, a medio metro) ¿Lo habrá oído?

#### ◆ D-J2-AMORY

| Opción | Texto | Respuesta | Efecto |
|---|---|---|---|
| **A · Reírse** | (Ríe con él, bajito.) "Pekín. Me gusta." | AMORY: "¡Ja! Sabía que tenías sentido del humor, {APELLIDO}. Lo escondes muy bien." | ⟶ DUDA +5 · SOSPECHA +5 · `amory_reaccion = "risa"` |
| **B · Reprenderle** | "Amory. Eso suena a crimental." | (Amory palidece. Tarda un segundo en volver a sonreír.) AMORY: "Es… una broma geográfica, camarada. Una broma de cartógrafos. Olvídalo." | ⟶ `amory_reaccion = "reprimenda"` |
| **C · Denunciarle** | (Se levanta y va al despacho de Voss.) | Ver escena J2.04-C | ⟶ SOSPECHA −10 · `amory_reaccion = "denuncia"` |

#### J2.04-C — Despacho de Voss *(solo si se elige denunciar)*

**Localización:** despacho austero, con una ventana estrecha (la única de la planta) y una telepantalla que Voss **puede apagar**. Sobre la mesa, carpetas y una taza de café de verdad (el vapor huele distinto).

VOSS: (sin levantar la vista de un papel) ¿Sí?

PROTAGONISTA: Subdirector. El camarada Amory ha hecho un comentario sobre el frente de Malabar. Ha dicho que… que el frente no se mueve.

(Voss levanta la vista despacio. Silencio largo.)

VOSS: ¿Con esas palabras?

PROTAGONISTA: Ha dicho que deberíamos estar en Pekín. Que los partes, sumados…

VOSS: (alza una mano enguantada) Suficiente. (Anota algo en una ficha pequeña.) Ha hecho usted lo correcto, camarada {APELLIDO}. El Partido valora la vigilancia. Especialmente en alguien con su… historia familiar.

PROTAGONISTA: Gracias, Subdirector.

VOSS: Vuelva a su mesa. Y, camarada… (Pausa.) No comente esto con nadie. Por su propio bien.

PENSAMIENTO: He hecho lo correcto. He hecho lo correcto. ¿Por qué me tiemblan las manos?

(Al volver, Amory le sonríe desde su mesa, ajeno a todo, y le saluda con la mano.)

→ salida a J2.05

### J2.05 — Centro de la Comunidad · Noche

**Localización:** salón ruidoso, con una mesa de ping-pong, un piano desafinado, pancartas a medio pintar extendidas por el suelo y botes de pintura roja. Grupos de camaradas ensayando cánticos. **Hilda** dirige, con un silbato.

HILDA: ¡{NOMBRE}! ¡Justo a tiempo! Necesito manos para las pancartas. La de Goldstein con colmillos está quedando divina.

#### Minijuego opcional: PANCARTA

Rellenar con pintura las letras de *¡MUERTE A EURASIA!* sin salirse.
- Bien hecho ⟶ `hilda_aprecio +1`.
- Mal hecho → HILDA: "Bueno… la intención es lo que cuenta. El Partido valora la intención."

(Parsons aparece con más banderines. Detrás de él, la hija de Parsons observa al protagonista y escribe en su libretita.)

**Puntos interactivos:**

- **[Hilda]** → HABLAR →
  HILDA: Smith no ha venido. Otra vez. (Saca un cuaderno y anota algo.) Tercera ausencia este mes. Yo solo apunto. Apuntar no es delatar, es ser ordenada.
  - Si `hilda_aprecio >= 1`: HILDA: Tú en cambio… Voy a proponer tu nombre para el comité de la Semana del Odio. ¡A la hermana de una mártir no le pueden decir que no!
- **[Parsons]** → HABLAR → PARSONS: ¿Sabes que el año pasado colgamos cuatro kilómetros de banderines en el distrito? ¡Cuatro! Este año quiero llegar a cinco. ¡Magnífico, magnífico!
- **[Cartel nuevo de los mártires]** *(colgado en la pared)*
  - MIRAR → (Diez rostros heroicos. En primera fila, Ivy.) PENSAMIENTO: Ahí estás. Entre los mejores. (Pausa.) Le han cambiado la nariz. Da igual. Es ella. Es lo que significa.
- **[Piano]** → USAR → (El protagonista toca unas teclas. Sin quererlo, salen las primeras notas de *Naranjas y limones*. Se detiene en seco.) PENSAMIENTO: ¿Por qué me sé esto? …Ivy. Ivy la cantaba.

(Fundido. El protagonista en la cama.)

### J2.06 — Sueño

(Pantalla en tonos sepia. Una calle sin bombardear. Una Ivy niña salta a la comba y canta.)

IVY (NIÑA): *Naranjas y limones, dicen las campanas de San Clemente…*

(El protagonista intenta acercarse. A cada paso, la calle se aleja. Al fondo, un silbido de cohete.)

IVY (NIÑA): (deja de saltar y mira directamente al protagonista) ¿Qué hora es?

(El protagonista mira su muñeca. Lleva el reloj de Ivy. **21:40.**)

(Impacto. Despertar con el silbato de la telepantalla.)

CARTEL: **JORNADA 3**

---

## JORNADA 3 — La grieta

### J3.01 — El piso · 07:15

(Gimnasia `CF[Entusiasmo, fácil]`. Sin incidencias.)

TELEPANTALLA: …y recuerden, camaradas: la Semana del Odio está cada vez más cerca. ¡El enemigo tiembla!

- **[Reloj de Ivy]** → MIRAR → PENSAMIENTO: Las nueve y cuarenta. Siempre las nueve y cuarenta.
- **[Puerta]** → salida a J3.02 *(la escalera y la calle se resuelven con una transición corta: el protagonista llega al Minipax)*

### J3.02 — Departamento de Partes y Cartografía · La mesa vacía

(El protagonista llega a su mesa. En la mesa de Amory hay **otra persona**: un hombre de mediana edad, gris y anodino, que escribe a máquina con dos dedos: el **camarada Pell**. Los dibujos de pájaros han desaparecido. La silla es la misma.)

PENSAMIENTO: ¿Amory se ha cambiado de mesa?

**Puntos interactivos (investigación libre, el jugador decide el orden):**

- **[Camarada Pell]** → HABLAR →
  PROTAGONISTA: Disculpe, camarada. ¿Sabe dónde se ha sentado hoy Amory?
  PELL: (sin dejar de teclear) ¿Quién?
  PROTAGONISTA: Felix Amory. Esta es su mesa.
  PELL: (para de teclear y le mira, sin expresión) Esta mesa es mía. Siempre ha sido mía. Llevo aquí… (piensa) …siempre.
  PENSAMIENTO: Miente. O está loco. O…

- **[Camarada Brooke]** *(mujer de la mesa de enfrente, de unos cincuenta años, que evita mirar)* → HABLAR →
  PROTAGONISTA: Camarada Brooke, ¿ha visto a Amory?
  BROOKE: (los ojos se le van un instante hacia la telepantalla) …No conozco a ningún Amory.
  PROTAGONISTA: Comíamos los tres juntos los martes.
  BROOKE: (muy bajo, casi sin mover los labios) No sé de qué me habla, camarada. Y usted tampoco.
  ⟶ SOSPECHA +3
  PENSAMIENTO: "Y usted tampoco." ¿Qué ha querido decir?

- **[Mapa de la nueva proyección]** *(clavado en la pared, el que dibujaba Amory)*
  - MIRAR → (Es el mismo mapa, idéntico, pero sin pájaros. En la esquina, la firma: **Pell, A.**) PENSAMIENTO: Es su mapa. Las mismas líneas. Su proyección "estirada". Y lo firma Pell.

- **[Registro de personal]** *(archivador junto a la entrada)*
  - USAR → (Primer plano de una ficha mecanografiada con la lista alfabética del departamento.)
    ```
    ...
    ALDRIDGE, M.
    AMES, T.
    ATKINS, R.
    ...
    ```
  PENSAMIENTO: Ames, Atkins… No hay Amory. (Pausa.) La ficha está más blanca que las demás. Como si la hubieran escrito esta mañana.

- **[Papelera de la mesa de Amory]**
  - MIRAR → PENSAMIENTO: Vacía. Limpia. Como si nunca hubiera tenido nada dentro.

- **[Despacho de Voss]** → USAR → *(si el jugador intenta entrar sin haber hablado con al menos dos personas:)* PENSAMIENTO: No se entra sin ser llamad{o|a}. Pero si nadie más me responde… *(Tras hablar con Pell y Brooke se habilita la escena J3.02-V.)*

#### J3.02-V — Despacho de Voss

PROTAGONISTA: Subdirector, disculpe. El camarada Amory no ha venido hoy y su mesa…

VOSS: (le mira con paciencia, como a un niño) No hay ningún Amory en esta sección, camarada {APELLIDO}.

**Variante según `amory_reaccion`:**

- **Si `"denuncia"`:**
  PROTAGONISTA: Pero ayer… ayer vine a este despacho. Le hablé de él. Usted anotó su nombre.
  VOSS: (sonríe muy levemente) Ayer usted vino a este despacho a informar de un… exceso de cansancio. Lo recuerdo perfectamente. Y aquí está otra vez, cansad{o|a}. (Pausa.) Le recomiendo descansar, camarada. El cansancio produce recuerdos que no existen.
  ⟶ DUDA +5 *(adicional)*
- **Si `"risa"` o `"reprimenda"`:**
  VOSS: ¿Se encuentra bien? Está pálid{o|a}. (Toma una ficha.) Quizá debería descansar. El cansancio produce… recuerdos que no existen.

#### ◆ Insistir o no

| Opción | Efecto |
|---|---|
| "Tiene razón, Subdirector. Estoy cansad{o\|a}." | VOSS: "Eso pensaba." · Sin efecto. |
| "Le vi ayer. Le vi con mis propios ojos." | VOSS: (silencio largo, luego escribe algo en la ficha) "Puede retirarse." ⟶ SOSPECHA +10 |
| "Amory existía. Y usted lo sabe." *(la temeridad, M7)* | (Voss deja la pluma y le mira de verdad.) VOSS: "Repítalo, camarada {apellido}. Despacio. Para la telepantalla." ⟶ SOSPECHA +30 y una segunda elección: |

| Opción | Efecto |
|---|---|
| Repetirlo, más alto. | PROTAGONISTA: "Felix Amory. Mesa catorce. Dibujaba pájaros en los márgenes de los mapas." VOSS: "Gracias. Eso es todo." ⟶ SOSPECHA 100 → **Final C0** |
| Callarse. | (No dice nada. Voss tampoco. Escribe algo en una ficha, muy despacio.) VOSS: "Puede retirarse." |

> Es la única puerta al Final C0: el resto de la Sospecha del Acto I suma como mucho 44.

→ salida a J3.03

### J3.03 — Doblepensar

(El protagonista vuelve a su mesa. Se sienta. La pantalla se oscurece por los bordes. Estática.)

(Se abre el **Registro de diálogos** del juego, el historial que el jugador ha visto durante dos jornadas, y se desplaza solo hasta la escena J2.04.)

```
AMORY: ¿Te has fijado en que el frente de Malabar lleva tres años en el mismo río?
AMORY: Toma, usa el mío. El tuyo no tiene punta.
```

(Efecto *glitch*: las letras de "AMORY" tiemblan, se desintegran píxel a píxel y se recomponen.)

```
—: ¿Te has fijado en que el frente de Malabar lleva tres años en el mismo río?
—: Toma, usa el mío. El tuyo no tiene punta.
```

(Lo mismo ocurre con las líneas de la cantina en J1.06 y con la presentación en J1.05.)

TELEPANTALLA: (en voz baja, casi íntima, solo en esta escena) El Partido no se equivoca. Si el Partido no lo recuerda, nunca existió.

#### DP-J3-AMORY

| Opción | Texto en pantalla | Efecto |
|---|---|---|
| **Aceptar** | *Nunca hubo ningún Amory.* | ⟶ DUDA −5 · SOSPECHA −5 · `dp_j3_amory = "aceptar"` · Los nombres quedan como "—" en el registro para el resto del juego. |
| **Recordar** | *Felix Amory se sentaba aquí.* | ⟶ DUDA +15 · `dp_j3_amory = "recordar"` · Los nombres vuelven a aparecer, pero **tachados**. ⟶ DIARIO +diario_amory *(disponible desde la Jornada 5)* |

**Monólogo posterior:**

- **Si Aceptar:**
  PENSAMIENTO: Me he confundido. El cansancio. Voss tiene razón: el cansancio produce recuerdos que no existen. Una mesa, una silla, un hombre gris que escribe con dos dedos. Siempre ha sido así.
- **Si Recordar:**
  PENSAMIENTO: Felix Amory. Ojos de pájaro. Mordía los lápices. Decía que los mapas eran poesía. (Pausa.) Felix Amory existía ayer. Y hoy no ha existido nunca.

### J3.04 — El lápiz

(El protagonista mete la mano en el bolsillo del mono. Hay algo.)

⟶ Se ilumina en el inventario: **item_lapiz_amory**.

- **[Lápiz]** → MIRAR →
  - Si `dp_j3_amory = "aceptar"`: PENSAMIENTO: Un lápiz mordido. "F.A." ¿De quién…? No significa nada. Iniciales cualesquiera.
  - Si `dp_j3_amory = "recordar"`: PENSAMIENTO: F.A. Felix Amory. Me lo prestó ayer. "Que no se diga que Cartografía no comparte." (Aprieta el lápiz.) Esto es una prueba. Esto existió.

#### ◆ D-J3-LAPIZ *(opcional: el jugador puede ignorarlo y simplemente salir)*

- **[Agujero de la memoria]** → USAR con **item_lapiz_amory** →

| Opción | Texto | Efecto |
|---|---|---|
| **Tirarlo** | (El lápiz cae por la ranura. Se oye el aire caliente que sube desde los hornos.) PENSAMIENTO: Higiénico. | ⟶ DUDA −10 · ITEM −item_lapiz_amory · `lapiz_destruido = true` |
| **Guardarlo** | (El protagonista retira la mano.) PENSAMIENTO: …Mañana. Lo tiraré mañana. | Sin efecto. *(El lápiz se queda en el inventario para todo el juego.)* |

> **Consecuencia futura:** si se guarda, el lápiz reaparece en momentos clave: en la Jornada 5 para escribir la primera entrada del diario, en la Jornada 13 para escribir el Capítulo II y, en el Final C, O'Brien lo saca de un cajón. Si se tira, en la Jornada 5 el protagonista escribe con un lápiz cualquiera y una línea del Capítulo II cambia.

### J3.05 — Pasillo del Minipax · Salida

(El protagonista sale de la sala al terminar la jornada. Pasillo largo, con luces de neón que parpadean. Al fondo, junto al cuarto de suministros, la **limpiadora** con su carrito.)

(Al acercarse, el jugador ve que tiene en la mano **unas hojas dibujadas**: mapas con pájaros diminutos en los márgenes. Los está doblando con cuidado y metiéndolos bajo los trapos del carrito.)

- **[Limpiadora] (NELL)** → MIRAR →
  - Si `dp_j3_amory = "recordar"`: PENSAMIENTO: Esos pájaros… Son los dibujos de Amory. Los de los márgenes.
  - Si `dp_j3_amory = "aceptar"`: PENSAMIENTO: Papeles con… pájaros. Alguien dibujaba pájaros. (Un pinchazo en la sien.) No sé quién.
- **[Limpiadora]** → HABLAR →

(En cuanto el protagonista da un paso hacia ella, Nell levanta la vista por primera vez en todo el juego. Le mira a los ojos. Es una mirada dura y larga, la misma de la mujer de la calle Stepney, aunque el jugador quizá aún no lo relacione.)

(Un guardia dobla la esquina del pasillo. El protagonista se gira un instante. Cuando vuelve a mirar, el carrito sigue ahí, **pero la limpiadora ya no está**.)

PENSAMIENTO: ¿Dónde…?

- **[Carrito]** → MIRAR → PENSAMIENTO: Trapos. Cubos. Lejía. Ni rastro de los dibujos.

→ salida a J3.06

### J3.06 — El piso · Noche · Cierre del Acto I

(El protagonista en su piso. La telepantalla emite música marcial. Se acerca a la ventana: el Ministerio de la Paz brilla blanco en la oscuridad.)

**Monólogo final del acto (según el estado):**

- **Si `dp_j3_amory = "aceptar"`:** *(la variante con `duda >= 10` se quitó en M7: aceptar deja siempre la Duda por debajo)*
  PENSAMIENTO: Un día largo. Un día raro. Mañana todo estará en su sitio. Siempre lo está. (Mira el cartel de Ivy.) Buenas noches, Ivy. Mañana ganaremos más kilómetros.
- **Si `dp_j3_amory = "recordar"`:**
  PENSAMIENTO: Felix Amory existía. Felix Amory existía. (Pausa.) Si alguien puede dejar de haber existido de un día para otro… (Se corta.) No. El Partido sabe lo que hace. Amory era un traidor. Lo de Pekín… era una señal. El Partido lo vio antes que yo. Eso es todo. (Mira el cartel de Ivy, mucho rato.) Eso es todo.
- **Añadido si `amory_reaccion = "denuncia"` (se suma a cualquiera de los anteriores):**
  PENSAMIENTO: Yo fui a ese despacho. Yo dije su nombre. (Silencio.) Hice lo correcto.

- **[Cama]** → USAR →

(Fundido lento. Durante el fundido se oye, muy lejos, un silbido de cohete. Un impacto amortiguado en otro barrio. El protagonista no se mueve.)

CARTEL: **FIN DEL ACTO I**

CARTEL: **ACTO II — LA GRIETA**

---

## Resumen de variables del Acto I

| Variable | Valores posibles al final del acto |
|---|---|
| `duda` | 0 (todo aceptado y lápiz destruido) a ~25 (risa + recordar + insistir) |
| `sospecha` | 0 a ~35 según crímenes faciales, insistencia con Voss y Brooke |
| `amory_reaccion` | `risa` / `reprimenda` / `denuncia` |
| `dp_j3_amory` | `aceptar` / `recordar` |
| `lapiz_destruido` | `true` / `false` |
| `parte_j1` | `{verbo, km, prisioneros, bajas}` elegidos |
| `hilda_aprecio` | 0–2 |
| `cf_j1_gimnasia`, `cf_j2_odio` | `perfecto` / `aceptable` / `fallo` |
| Inventario | `item_reloj_ivy`, `item_lapiz_amory` (si no se destruyó), ficha del Partido |

## Semillas plantadas para actos posteriores

| Semilla | Dónde | Se recoge en |
|---|---|---|
| Reloj de Ivy parado a las 21:40 | P.02, J2.06 | J9 (el *Times* original dice 21:40; la versión vigente cambia el día) |
| La mujer prole de Stepney es Nell | P.02, J3.05 | J7 ("Yo estaba en la calle Stepney") |
| La silueta del oficial es Voss | P.02, J1.05 | J11 (firma de la orden) |
| "Naranjas y limones" | P.02, J2.05, J2.06 | J7 (contraseña de Nell), J13 (San Clemente) |
| Ivy: "No les creas" | P.02 | J11 (el protagonista entiende a quién se refería) |
| La ración de chocolate "aumenta" a 20 g | J2.01 | J6 (recorte de periódico en el estudio de Crane) |
| La hija de Parsons: "Dice un nombre" | J2.02 | J10 (denuncia a su propio padre por hablar en sueños) |
| Agujeros de alfiler en el mapa de Malabar | J2.04 | J10 (cambio de enemigo: hay que arrancar todas las banderas) |
| El niño prole con metralla al cuello | J1.03 | J4 (es Sammy) |
| Parte del protagonista (`parte_j1`) | J1.05 | J6 (reaparece alterado con su firma) |
| Lápiz de Amory | J2.04, J3.04 | J5 (diario), J13 (Capítulo II), Final C (O'Brien) |
| Brooke: "Y usted tampoco" | J3.02 | Acto III (Brooke es contacto pasivo de la Hermandad) |

## Ajustes a la biblia ([guion.md](../guion.md)) introducidos aquí

- **Los Dos Minutos de Odio de la Jornada 2** son una **sesión conjunta en el Miniver** por el aniversario de Malabar. Así aparecen Julia, O'Brien y Winston, que trabajan en otros ministerios.
- **Nell estaba en la calle Stepney** en 1979, intentando sacar a Ivy.
- **El reloj de Ivy (21:40)** es objeto de inventario desde el prólogo.
- **El Minipax tiene personajes de fondo con nombre:** Pell (sustituto de Amory) y Brooke (colega que sabe más de lo que dice).
- **Amory presta su lápiz** al protagonista en la Jornada 2. Así se explica cómo llega a su bolsillo.
- **La Ficha de Afiliación pide también un apellido**, que Ivy comparte.
