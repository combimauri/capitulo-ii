# ACTO II — LA GRIETA

> Jornadas 4–7 · Duración estimada: ~50 min
> Objetivo narrativo: que el jugador **vea** antes de que el protagonista se atreva a decirlo. El fervor del protagonista es justo lo que le empuja a mirar: quiere un registro exacto, quiere verificar, quiere servir mejor. Al final del acto ya no puede dejar de ver.
> Notación: ver [00-convenciones.md](00-convenciones.md).

**Estado al entrar:** el que dejó el Acto I (`duda` ≈ 0–25, `sospecha` ≈ 0–35).

---

## JORNADA 4 — El registro de impactos

### J4.01 — El piso · 07:15

(Gimnasia. `CF[Entusiasmo, fácil]`.)

TELEPANTALLA: …anoche, un cobarde cohete euroasiático alcanzó una zona residencial del distrito de Limehouse. El Partido lamenta las víctimas y promete una respuesta implacable. ¡Muerte a Eurasia!

#### CF-J4-NOTICIA · `CF[Duelo patriótico, fácil]`

PENSAMIENTO:
- `[D0]` El silbido de anoche. Lo oí. Otro más. Otro como el de Ivy.
- `[D1]` El silbido de anoche. Lo oí desde la cama. Ni siquiera me levanté. ¿Desde cuándo no me levanto?

**Puntos interactivos (nuevos o cambiados):**

- **[Cajón de la mesa]** *(nuevo)*
  - MIRAR → PENSAMIENTO: Ahí guardo lo único que saqué de la calle Stepney, aparte del reloj.
  - USAR → (Primer plano: una **fotografía** quemada por un borde, arrugada y desvaída. Dos niños en un parque: Ivy, de unos diez años, y el protagonista, algo mayor. La cara de Ivy está casi borrada por una mancha de agua.) PENSAMIENTO: Ya casi no se le ve la cara. En el cartel se le ve mejor. (Pausa.) No es la misma cara.
  ⟶ ITEM +item_foto_ivy
- **[Cartel de Ivy]** → MIRAR →
  - `[D0]` PENSAMIENTO: Buenos días, Ivy.
  - `[D1]` PENSAMIENTO: Buenos días, Ivy. (Pausa.) Te han cambiado la nariz.
- **[Puerta]** → salida a J4.02

### J4.02 — Departamento de Partes y Cartografía · Una tarea nueva

(El protagonista llega a su mesa. Pell teclea con dos dedos en la mesa de al lado. Voss sale de su despacho con una carpeta.)

VOSS: Camarada {APELLIDO}. A partir de hoy llevará también el **Registro de Impactos**.

PROTAGONISTA: ¿El registro, Subdirector? ¿Quién lo llevaba hasta ahora?

VOSS: (un segundo de silencio) Estaba vacante. (Le entrega la carpeta.) Cada parte de Defensa Civil se anota en el mapa y en el libro. Exactitud, camarada. El Partido necesita saber dónde golpea el enemigo para golpearle a él.

**Variante si `amory_reaccion = "denuncia"`:**

VOSS: (añade, sin mirarle) Usted ha demostrado tener buen ojo. Úselo.

PENSAMIENTO:
- Si `dp_j3_amory = "recordar"`: Vacante. Era de Amory. Amory llevaba el registro los jueves. Lo sé. Lo sé.
- Si `dp_j3_amory = "aceptar"`: Vacante. Una mesa vacante. (Un pinchazo en la sien.) Mejor así.

### J4.03 — La mesa del Registro

**Localización:** una mesa aparte, en un rincón, junto a la ventana tapiada. Encima, un **mapa de Londres** enorme bajo un cristal, con cuadrícula (A–L, 1–12) y nombres de distritos. A un lado, el **Libro de Registro**, un libro de contabilidad con tapas de tela gris. Un cajón con tirador de latón. Un frasco con chinchetas negras.

**Puntos interactivos:**

- **[Mapa de Londres]**
  - MIRAR → PENSAMIENTO: Toda la ciudad. Sin una sola chincheta. Alguien la ha limpiado.
- **[Libro de Registro]**
  - USAR → (Se abre por la página del día. Las páginas anteriores al **día siguiente de la desaparición de Amory** han sido **arrancadas**: se ven los restos de papel en el lomo.) PENSAMIENTO: Faltan todas las páginas anteriores. Empiezo de cero. (`[D1]`: ¿Por qué arrancarlas? Un registro arrancado no es un registro.)
- **[Cajón]** *(objetivo opcional, pero importante)*
  - USAR → Dentro: un **compás** de latón, gomas, un lápiz roto y, bajo el fieltro del fondo (requiere USAR otra vez: "El fieltro está despegado por una esquina"), dos cosas:
    1. Una **lámina transparente** con un sello oficial: *ZONIFICACIÓN URBANA — DISTRITOS DEL PARTIDO / DISTRITOS PROLETARIOS*. ⟶ ITEM +item_zonificacion · `FLAG zonificacion_encontrada = true`
    2. Un trozo de papel doblado con un **pájaro diminuto** dibujado en la esquina y una sola línea con letra apretada: **"¿Por qué nunca en el centro?"** ⟶ ITEM +item_nota_amory · DUDA +5
    PENSAMIENTO:
    - Si `dp_j3_amory = "recordar"`: Un pájaro. Es su letra. Es Amory. "¿Por qué nunca en el centro?" ¿Qué centro?
    - Si `dp_j3_amory = "aceptar"`: Un pájaro. Alguien dibujaba pájaros. (El pinchazo otra vez, más fuerte.) "¿Por qué nunca en el centro?" No sé qué significa.
  ⟶ ITEM +item_compas *(con el primer USAR)*

#### Minijuego 3: REGISTRO DE IMPACTOS *(tutorial)*

(El tubo neumático escupe varios cilindros seguidos.)

**Mecánica:** cada parte de Defensa Civil indica distrito, cuadrícula, hora y bajas. El jugador clava una chincheta negra en la casilla correcta y copia los datos en el Libro (las casillas se rellenan solas al acertar). Si se equivoca de casilla, la chincheta rebota y suena un "clac" seco (sin penalización; es un tutorial).

**Herramientas desbloqueables:**
- **Lámina de zonificación:** si `zonificacion_encontrada`, el jugador puede superponerla sobre el mapa. Los distritos del Partido se ven en **gris claro** y los proletarios en **pardo**. Los ministerios son cuatro rombos blancos.
- **Compás:** permite trazar un círculo de radio ajustable desde cualquier punto. La escala marca kilómetros.

**Partes de la Jornada 4 (6 impactos):**

| # | Distrito | Cuadrícula | Hora | Bajas | Zona |
|---|---|---|---|---|---|
| 1 | Limehouse | J-8 | 23:47 (anoche) | 4 | Prole |
| 2 | Bermondsey | H-10 | 02:15 | 2 | Prole |
| 3 | Stepney Este | J-7 | 04:30 | 0 | Prole |
| 4 | Southwark | F-10 | 19:05 | 6 | Prole |
| 5 | Poplar | K-7 | 21:20 | 3 | Prole |
| 6 | Shadwell | I-8 | 22:00 | 9 | Prole |

> **Diseño:** el jugador atento ya ve que las chinchetas se agrupan en el este y el sur, lejos del centro. Con la lámina superpuesta, **todas** caen en pardo. El protagonista **no comenta nada** todavía: el juego deja que el jugador lo note solo.

PENSAMIENTO (al terminar, `[D0]`): Seis. Seis en una noche. Eurasia no descansa. Nosotros tampoco.

**Si el jugador superpone la lámina y la mira (MIRAR sobre el mapa con lámina):**

PENSAMIENTO:
- `[D0]` Todas en zona prole. Lógico: allí las casas son de ladrillo viejo y los proles no se refugian a tiempo. Eurasia busca hacer daño.
- `[D1]` Todas en zona prole. (Mira la nota de Amory.) "¿Por qué nunca en el centro?"
⟶ DUDA +3 *(solo la primera vez)*

### J4.04 — Cantina del Minipax · Mediodía

(El protagonista come solo. La silla de enfrente está vacía. Pell come en otra mesa, mecánicamente. Brooke, al fondo, de espaldas.)

**Puntos interactivos:**

- **[Silla vacía]**
  - MIRAR →
    - Si `dp_j3_amory = "recordar"`: PENSAMIENTO: "Si no hay palabra, no hay retirada." Lo dijo aquí. Brindó con la ginebra.
    - Si no: PENSAMIENTO: Una silla vacía. Las sillas vacías no significan nada.
- **[Brooke]** → HABLAR →
  BROOKE: (sin girarse) Le han dado el registro.
  PROTAGONISTA: ¿Cómo lo sabe?
  BROOKE: Esa mesa da mala suerte, camarada. (Se levanta con la bandeja.) Coma algo. Se le nota en la cara cuando no come.
  ⟶ *(Sin efecto mecánico. Brooke sigue siendo un contacto pasivo.)*

### J4.05 — Fin de la jornada · El parte ilegible

(Último cilindro del día. El protagonista lo abre.)

CARTEL (parte):
```
def.civil · impacto · 18.4.84 · 17:52
distrito: limehouse · cuadr: ?-8 (ilegible)
bajas: pendiente
```

PENSAMIENTO: Ilegible. No puedo registrar un impacto ilegible. (Pausa.) Limehouse está a veinte minutos andando. Si voy yo mism{o|a}…

#### ◆ D-J4-VERIFICAR

| Opción | Texto | Efecto |
|---|---|---|
| **Ir a verificarlo** | "Un registro debe ser exacto. Ivy merece un registro exacto." | → J4.06. ⟶ `FLAG visita_prole_j4 = true` |
| **Dejarlo en blanco** | "Lo completará Defensa Civil mañana." | La casilla queda vacía. → J4.10 (piso). *(La visita al barrio prole se traslada a la mañana de la Jornada 5, de forma obligatoria: el protagonista va a dejar la foto a Crane porque ve su anuncio en el periódico de Hilda. Variante en J5.01.)* |

> **Diseño:** la opción por defecto y más natural para el protagonista fanático es **ir**. Su celo le lleva al barrio prole.

### J4.06 — Limehouse · Atardecer

**Localización:** calles estrechas de casas de ladrillo ennegrecido, ropa tendida de lado a lado, charcos, gatos, niños descalzos. Mucho ruido: gritos, una radio, alguien que canta. **No hay telepantallas** en la calle, solo algún altavoz lejano. La paleta cambia: siguen los grises, pero aparecen el **ocre** de las farolas de gas y el **verde** de una puerta pintada.

(Al entrar en el barrio, la música del Partido se apaga. Se oye una melodía tarareada, de taberna.)

PENSAMIENTO:
- `[D0]` Proles. Cuánto ruido. Cuánta suciedad. Y ni una sola telepantalla. ¿Cómo saben qué tienen que pensar?
- `[D1]` Proles. Cuánto ruido. (Pausa.) Hace mucho que no oía a nadie reír tan alto.

⟶ SOSPECHA +3 *(un miembro del Partido en un barrio prole de noche llama la atención)*

**Puntos interactivos de la calle:**

- **[Altavoz lejano]** → MIRAR → PENSAMIENTO: Aquí el Partido habla desde lejos. Como si no hiciera falta acercarse.
- **[Ropa tendida]** → MIRAR → PENSAMIENTO: Sábanas, camisas… y vestidos de colores. Colores que no se ven en las Mansiones Victoria.
- **[Pub "La Campana"]** → USAR → J4.08 *(opcional)*
- **[Columna de humo al fondo]** → USAR → J4.07 *(objetivo)*

### J4.07 — Limehouse · La casa alcanzada

**Localización:** una casa partida por la mitad. Se ve el interior como en una casa de muñecas: una cama colgando, un papel pintado de flores. Proles apartando escombros. Una mujer de unos treinta años, robusta y de brazos fuertes, con un pañuelo en la cabeza, dirige a los demás a gritos: **Dot Pike**. Un niño de unos siete años rebusca entre los cascotes con una lata: **Sammy**.

(El protagonista reconoce al niño: es el que le pidió un cigarrillo en la Jornada 1. Lleva un trozo de metralla retorcida colgado al cuello con un cordel.)

- **[Niño] (SAMMY)** → MIRAR → PENSAMIENTO: El niño de la avenida. El del cigarrillo.
- **[Niño] (SAMMY)** → HABLAR →

SAMMY: (le enseña la lata, orgulloso) ¡Mire! Este es de cohete grande. Este de uno pequeño. Este no sé. Tengo ochenta y tres. ¡El Billy Hogan solo tiene cuarenta!

PROTAGONISTA: Eso es peligroso. Puede quedar alguno sin explotar.

SAMMY: ¡Qué va! Los cohetes explotan siempre. Mi madre dice que es lo único que funciona bien en Londres.

DOT: (desde los escombros) ¡Sammy! ¡Deja en paz a {el|la} camarada! (Se acerca, se limpia las manos en el delantal y mira el mono azul de arriba abajo.) ¿Viene del Partido? ¿A contar muertos?

PROTAGONISTA: Vengo a registrar el impacto. Mi parte era ilegible.

DOT: (ríe sin alegría) Ilegible. Mire, apúntelo: calle Narrow, número once. Los Hennessy. La abuela y los dos pequeños. El padre estaba en el turno de noche del muelle. (Pausa.) Eso es lo que hay que apuntar.

⟶ El parte ilegible se completa: `J-8`. *(Al día siguiente se registra automáticamente.)*

#### Diálogo con Dot (árbol)

- **"Eurasia pagará por esto."**
  DOT: (se encoge de hombros) Será. Aquí caen cada semana, ¿sabe? Cada semana. (Señala con la barbilla hacia el oeste, donde brillan las pirámides blancas de los ministerios.) Allí arriba nunca. Los euroasiáticos deben de tenernos mucho cariño.
  ⟶ DUDA +3
  PENSAMIENTO: `[D0]` Habla así porque es prole. No entiende de estrategia. `[D1]` Allí arriba nunca.
- **"Lo siento por los Hennessy."**
  DOT: (le mira un momento más largo, sorprendida) …Gracias. No suelen decir eso los de azul.
  ⟶ `FLAG dot_confianza +1`
- **"¿Por qué no se refugian?"**
  DOT: ¿Dónde? ¿En el metro? Lo cerraron hace dos años. "Por reformas." (Escupe a un lado.) Reforman muy despacio.

SAMMY: (le tira de la manga) ¿Quiere uno? (Le ofrece un trozo de metralla.) Para que le dé suerte. Nunca te cae un cohete donde ya tienes uno.

#### ◆ D-J4-METRALLA

| Opción | Efecto |
|---|---|
| Aceptarlo | ⟶ ITEM +item_metralla_sammy · SAMMY: "¡Ochenta y dos, entonces!" · `dot_confianza +1` |
| Rechazarlo | SAMMY: "Usted se lo pierde." (Se va corriendo.) |

(Al girarse para irse, el protagonista ve a un hombre con una cámara de fuelle fotografiando las ruinas.)

### J4.07b — Crane

**Localización:** la misma calle, con la luz de la farola encendiéndose.

(Un hombre de unos cincuenta años, bien afeitado, con chaleco de lana, sombrero y una cámara antigua sobre trípode: **Abel Crane**. Tiene una sonrisa fácil y voz cálida.)

CRANE: (sin apartar el ojo del visor) No se mueva, camarada. Usted, con el mono azul delante de la casa rota… Es una imagen. (Clic. Luego levanta la vista y sonríe.) Perdone. Deformación profesional. Abel Crane. Tengo el estudio en la calle Cable, junto al mercado.

PROTAGONISTA: ¿Para qué fotografía esto?

CRANE: Para el recuerdo. Aquí nadie tiene fotos de nada. Si no las hago yo, dentro de un año nadie sabrá que aquí vivían los Hennessy. (Pausa, le mira con atención.) Usted… perdone el atrevimiento… ¿no se parece a la chica del cartel nuevo? El de los mártires. La de primera fila.

PROTAGONISTA: Era mi hermana.

CRANE: (se quita el sombrero) Lo siento mucho. De verdad. (Pausa.) ¿Tiene fotos de ella? Fotos de verdad, digo, no carteles.

**Si `item_foto_ivy` en inventario:**

PROTAGONISTA: Una. Muy estropeada.

CRANE: Tráigamela. Restauro fotografías antiguas, es mi especialidad. Hago maravillas con el agua y el fuego. Le devolveré la cara de su hermana. (Le tiende una tarjeta.) Sin compromiso. Para mí sería un honor.

⟶ ITEM +item_tarjeta_crane

PENSAMIENTO:
- `[D0]` Un prole amable. Existen.
- `[D1]` Un prole amable. Con una cámara. (Pausa.) Es buena persona. Se le ve.

> **Nota de dirección:** Crane es la persona más agradable que el jugador ha conocido hasta ahora. La música se vuelve cálida cuando habla. Es intencionado.

### J4.08 — Pub "La Campana" *(opcional)*

**Localización:** pub prole lleno de humo, con barra de madera gastada, jarras de cerveza, dardos y una campana de latón colgada sobre la barra. Proles jugando a la lotería. Un **viejo** sentado solo, con una pinta.

(El ambiente se apaga cuando entra el protagonista con el mono azul. Silencio. Después, poco a poco, vuelven las conversaciones.)

- **[Campana sobre la barra]** → MIRAR → PENSAMIENTO: Una campana de barco. Vieja. Tiene algo grabado: "S. Clem…" El resto está borrado.
- **[Viejo]** → HABLAR →
  VIEJO: (sin mirarle) ¿Sabe lo que era una pinta? Antes. Una pinta de verdad. Ahora te ponen esto, medio litro, y te dicen que es más. (Bebe.) Y es menos. Yo lo sé porque me acuerdo. Los jóvenes no se acuerdan de nada.
  PROTAGONISTA: Antes de la Revolución los capitalistas les mataban de hambre.
  VIEJO: (le mira por fin, divertido) ¿Ah, sí? Pues yo me acuerdo de que estaba gordo. (Ríe hasta toser.)
  ⟶ DUDA +2
- **[Tabernero]** → HABLAR → TABERNERO: Aquí no servimos ginebra de la Victoria, camarada. Solo cerveza. Si quiere ginebra, vuelva a su barrio.

### J4.10 — El piso · Noche

(El protagonista vuelve. Al subir por la escalera:)

**Si `visita_prole_j4` y `hilda_aprecio < 2`:**

HILDA: (asomándose desde su puerta, en bata) Qué tarde, {NOMBRE}. Las once pasadas. (Sonrisa tirante.) ¿Mucho trabajo?

PROTAGONISTA: Verificación de un impacto. Para el Registro.

HILDA: Ah. (Pausa.) Qué celo. (Cierra la puerta despacio.)

⟶ SOSPECHA +3

(En el piso.)

- **[Foto de Ivy]** *(si está en inventario)* → MIRAR → PENSAMIENTO: "Le devolveré la cara de su hermana." (Pausa.) Ya tengo su cara. Está en el cartel.
- **[Cama]** → USAR → fin de la jornada.

CARTEL: **JORNADA 5**

---

## JORNADA 5 — El mercado

### J5.01 — El piso · 06:40

(El protagonista se despierta antes del silbato. La telepantalla aún está en silencio, con la imagen fija del Gran Hermano.)

PENSAMIENTO: Antes del silbato. No he dormido.

**Si tiene `item_foto_ivy` y `item_tarjeta_crane`:**

PENSAMIENTO: El estudio de la calle Cable abre a las siete. Me da tiempo antes del Minipax si voy por el mercado.

**Si eligió "Dejarlo en blanco" en J4 (no hay tarjeta):**

(Bajo la puerta hay un periódico doblado, el *Times* de la comunidad que Hilda reparte. En la última página, un anuncio pequeño:)

CARTEL: *ESTUDIO CRANE — Calle Cable, 7 — Se restauran fotografías antiguas. Recuerdos que el tiempo borra.*

PENSAMIENTO: Restaurar… (Mira la foto de Ivy.) Me da tiempo antes del Minipax si voy por el mercado.

#### ◆ D-J5-FOTO

| Opción | Efecto |
|---|---|
| Llevar la foto a Crane | → J5.02 · `FLAG foto_a_crane = true` |
| No llevarla | → J5.02 igualmente: el protagonista va por el mercado porque es el camino más corto hacia el Minipax desde las Mansiones Victoria cuando la avenida está cortada por obras. CARTEL: *"AVENIDA DE LA VICTORIA CERRADA POR REFORMAS."* |

> **Diseño:** el mercado es inevitable. La foto solo cambia lo que pasa en el estudio de Crane.

### J5.02 — Mercado de Watney Street · 07:45

**Localización:** mercado al aire libre, de madrugada. Puestos de madera con toldos remendados: patatas, retales, cacharros, cordones de zapatos, cuchillas de afeitar usadas. Mucha gente. Al fondo, el escaparate del **Estudio Crane**. En un puesto, **Dot** vende retales y canta mientras dobla telas.

DOT: (tararea, sin verle todavía, una canción de amor vieja y pegadiza; la letra no se entiende, solo la melodía)

> **Nota de dirección:** guiño a la mujer prole que canta en el patio en la novela. Aquí la canta Dot. Usaremos una melodía original, sin letra de la novela, que será el leitmotiv de la vida prole.

- **[Dot]** → HABLAR →
  - Si `dot_confianza >= 1`: DOT: ¡Mira quién vuelve! {El|La} de azul que dice "lo siento". (Sonríe.) ¿Retales? Tengo uno con flores. Ilegal no es, pero casi.
  - Si no: DOT: (seca) ¿Otra verificación?
- **[Sammy]** *(sentado en el bordillo, frente al puesto, ordenando su colección de metralla en filas)* → HABLAR →
  SAMMY: ¡Ochenta y cuatro! Anoche cayó uno en el muelle y Billy Hogan llegó tarde. (Le enseña un trozo brillante.) Este es el mejor. Parece plata.
- **[Puesto de cordones]** → MIRAR → PENSAMIENTO: Cordones de zapatos. Los vende un viejo con un solo ojo. (Seed: el vendedor que denunció la hija de Parsons era otro; este tiene suerte.)

→ USAR **[Estudio Crane]** → J5.03

### J5.03 — Estudio Crane · Interior

**Localización:** estudio pequeño y cálido. Fondos pintados enrollados (un jardín, una playa), una silla de terciopelo gastado, la cámara de fuelle, un mostrador con lupas y pinceles finos. Paredes llenas de **fotografías enmarcadas** de gente del barrio: bodas, niños, viejos. Una puerta con un cartel: *CUARTO OSCURO — NO ENTRAR*, con una bombilla roja apagada encima. Huele a químicos.

CRANE: (abriendo, en mangas de camisa) ¡Camarada! Qué alegría. Pase, pase. Aún no he encendido la estufa, perdone el frío.

**Si `foto_a_crane`:**

(El protagonista le entrega la foto. Crane la sujeta por los bordes con mucha delicadeza y la examina con una lupa.)

CRANE: Agua y fuego. Lo peor para una fotografía. (Pausa.) Pero la cara está ahí. Debajo de la mancha, la cara siempre sigue ahí. Deme tres días.

PROTAGONISTA: ¿Por qué hace esto?

CRANE: (sonríe) Porque en esta ciudad todo se olvida muy rápido, camarada. Alguien tiene que recordar. (Se gira hacia el mostrador.) ¿Cómo se llamaba?

PROTAGONISTA: Ivy.

CRANE: Ivy. (Lo apunta en un sobre.) Bonito nombre. (Sin girarse, como de pasada:) ¿Y cómo era Ivy? Quiero decir… ¿qué le gustaba?

#### Diálogo de Crane — primera prueba *(sistema de "confianza de Crane")*

Las respuestas **abiertas** dan información a Crane (`crane_info +1`) y suben la Sospecha. Las **cerradas** no.

| Opción | Tipo | Efecto |
|---|---|---|
| "Era una buena camarada. Leal." | Cerrada | CRANE: "Claro, claro." |
| "Cantaba todo el tiempo. Canciones viejas." | Abierta | CRANE: "¿Ah, sí? ¿Cuáles?" → si responde "Naranjas y limones": `crane_info +1` · SOSPECHA +3. CRANE: (anota algo, sonriendo) "La conozco. Las campanas de San Clemente. Ya no quedan campanas." |
| "No quiero hablar de ella." | Cerrada | CRANE: (alza las manos) "Por supuesto. Perdone." |

**Si no `foto_a_crane`:**

CRANE: ¿No me trae la foto? Es una pena. (Sonríe.) Bueno, la oferta sigue en pie. Las caras esperan. (Pausa.) Le invitaría a un té, pero llegará tarde a su ministerio.

**Puntos interactivos del estudio:**

- **[Fotografías de la pared]** → MIRAR → PENSAMIENTO: Bodas. Niños. Una anciana con un gato. Ningún cartel, ninguna consigna. Solo caras.
  - *(Detalle para el jugador atento:)* en una de las fotos, al fondo, se ve a **Brooke**, la colega del Minipax, más joven, en una boda prole. PENSAMIENTO: ¿Esa no es…? No. No puede ser.
- **[Cuarto oscuro]** → USAR → CRANE: (amable, pero rápido) Ahí no, camarada. La luz estropea el trabajo de semanas.
- **[Cámara]** → MIRAR → PENSAMIENTO: Una cámara antigua. De antes de la Revolución. ¿Cómo la conserva?

→ Salida al mercado: J5.04

### J5.04 — Mercado de Watney Street · El cohete

(El protagonista sale del estudio. El mercado está más lleno. Sammy sigue en el bordillo. Dot canta. Todo es normal durante 3 segundos de control del jugador.)

(De pronto, un **silbido**. Lejano al principio, agudo, creciente. El mismo silbido del prólogo. La música se corta en seco.)

(La gente se tira al suelo. Alguien grita "¡Al suelo!". Dot levanta la cabeza buscando a Sammy.)

(Sammy, en mitad de la calzada, se ha agachado a recoger un trozo de metralla brillante que se le ha caído. No oye nada. Está de espaldas.)

PENSAMIENTO: (muy rápido) Sammy.

#### ◆ D-J5-SAMMY · Secuencia contrarreloj (~8 segundos)

(El tiempo se ralentiza. Aparecen dos opciones grandes en pantalla.)

| Opción | |
|---|---|
| **CORRER HACIA SAMMY** | → J5.04-A |
| **PONERSE A CUBIERTO** | → J5.04-B |

*(Si el jugador no elige en 4 segundos, el protagonista se queda paralizado y se resuelve como B, con un monólogo distinto: "No me he movido. No me he movido.")*

#### J5.04-A — Intentarlo

**Mecánica:** el protagonista corre hacia Sammy y el jugador debe tocar en el orden correcto para esquivar obstáculos que aparecen uno tras otro. La secuencia está diseñada para fallar siempre, pero **el jugador no debe sentir que es injusta**: cada obstáculo es razonable y el jugador casi lo consigue.

1. **Un tenderete se derrumba** delante → tocar a la izquierda para rodearlo. *(Se puede superar.)*
2. **Una mujer cae** con un niño en brazos en el camino → tocar para ayudarla a levantarse o saltar por encima. Ayudarla cuesta un segundo; saltar, medio. *(Ambas opciones pierden tiempo.)*
3. **Un patrullero del Partido** aparece de un portal, le agarra del brazo y grita "¡Identifíquese, camarada! ¡Al suelo!" → tocar rápido varias veces para soltarse. *(Se suelta, pero tarde.)*
4. El protagonista estira el brazo. Sus dedos rozan la camisa de Sammy.

(Blanco. Impacto. Silencio total salvo un pitido agudo.)

⟶ `FLAG sammy_intento = true` · DUDA +10 · SOSPECHA +8 *(el patrullero ha tomado nota del miembro del Partido que corría hacia un prole)*

#### J5.04-B — Ponerse a cubierto

(El protagonista se tira detrás de un puesto de patatas. Se cubre la cabeza. A través de un hueco entre las cajas ve a Sammy, todavía agachado. Ve a Dot levantarse y echar a correr hacia él.)

(Blanco. Impacto. Silencio total salvo un pitido agudo.)

⟶ `FLAG sammy_intento = false` · DUDA +5

### J5.05 — Después

**Localización:** el mercado devastado. Polvo, toldos ardiendo, gritos ahogados por el pitido. La paleta se desatura casi por completo, salvo el **rojo**.

(El protagonista se levanta. Avanza despacio entre el polvo. El sonido vuelve poco a poco.)

(En mitad de la calzada, Dot, cubierta de polvo y con una brecha en la frente, de rodillas. Abraza algo pequeño. La lata de metralla, volcada, ha esparcido trozos por el suelo.)

DOT: (no grita; repite, muy bajo) Sammy. Sammy. Sammy. Sammy.

**Si `sammy_intento`:**

(Dot levanta la vista. Ve al protagonista, con el mono azul roto en el brazo y sangre en la mano. Le mira largo. No dice nada, pero asiente una vez, casi imperceptiblemente.)

⟶ `dot_confianza +2`

**Si no `sammy_intento`:**

(Dot levanta la vista. Ve al protagonista de pie, intacto, detrás del puesto de patatas. Le mira largo. Aparta la vista.)

⟶ `dot_confianza = 0`

(Llega una patrulla del Partido: tres hombres con uniforme negro y un oficial.)

OFICIAL: Despejen la zona. Circulen. (Ve a Dot con Sammy. Hace un gesto a sus hombres sin mirar.) Retiren eso.

PROTAGONISTA: (sin poder evitarlo) Es un niño.

OFICIAL: (le mira, ve el mono azul) ¿Es usted del Partido, camarada? Entonces no tiene nada que hacer aquí. Circule.

PENSAMIENTO:
- Siempre (en cualquier tramo de Duda; es el primer pensamiento "rebelde" obligatorio del juego):
  A Ivy le hicieron un cartel. "Esta camarada es ahora una mártir del Partido." (Pausa larga.) A Sammy le han dicho "eso". "Retiren eso."

- **[Trozo de metralla brillante]** *(en el suelo, el que Sammy recogía)* → USAR →
  ⟶ ITEM +item_metralla_brillante
  PENSAMIENTO: "Parece plata."

⟶ DIARIO +diario_sammy

→ Transición: el protagonista camina hacia el Minipax con la mano vendada con un pañuelo. Cartel: *09:20.*

### J5.06 — Departamento de Partes y Cartografía · Tarde

(El protagonista llega tarde. Voss está de pie junto a su mesa, esperándole.)

VOSS: Una hora y veinte minutos, camarada {APELLIDO}.

#### ◆ D-J5-RETRASO

| Opción | Texto | Efecto |
|---|---|---|
| **Verdad** | "Estaba en el mercado de Watney Street. Cuando cayó el cohete." | VOSS: (pausa) "Qué… coincidencia. ¿Y qué hacía usted en Limehouse a las ocho de la mañana?" → sub-opción: "Atajo por las obras" (verdad, sin efecto) / "Verificación para el Registro" (VOSS: "Qué celo. Entonces sabrá registrarlo bien.") · ⟶ SOSPECHA +3 |
| **Mentira** | "Me encontraba mal, Subdirector. El estómago." | VOSS: (mira el pañuelo ensangrentado de la mano) "Ya veo." ⟶ SOSPECHA +6 *(Voss sabe dónde estaba: la patrulla ha informado.)* · Si `sammy_intento`: VOSS: "Curioso. La patrulla de Limehouse ha informado de un miembro del Partido que corría por el mercado. Corría *hacia* el impacto." ⟶ SOSPECHA +4 adicional |

VOSS: (se aleja) Tiene partes pendientes. Uno de ellos le resultará familiar.

### J5.07 — El registro · El patrón (pista B)

(En la mesa del Registro, varios cilindros. Uno de ellos:)

CARTEL (parte):
```
def.civil · impacto · 19.4.84 · 08:12
distrito: limehouse · mercado watney st · cuadr: J-8
bajas: 7 (proles)
```

PENSAMIENTO: Siete. "Proles." Entre paréntesis. (Pausa.) Sammy es un paréntesis.

**Minijuego de registro** con el impacto del mercado y otros 3 de la noche anterior (todos en zona prole: Wapping I-9, Rotherhithe J-10, Deptford K-11).

(Al clavar la chincheta del mercado, el protagonista se queda mirando el mapa. **El juego fuerza el uso de las herramientas:**)

- Si **no** tiene `item_zonificacion`: PENSAMIENTO: "¿Por qué nunca en el centro?" (Abre el cajón con rabia. Encuentra el fieltro despegado.) ⟶ ITEM +item_zonificacion · ITEM +item_nota_amory *(si no los tenía)*

**Secuencia guiada:**

1. El jugador superpone la **lámina de zonificación**. *(Todas las chinchetas, 11 ya, caen en pardo.)*
2. El jugador usa el **compás** desde cada uno de los cuatro ministerios (rombos blancos) con un radio de **2 km**. *(Ningún círculo contiene una sola chincheta.)*
3. Se abre el **tablero de deducción**: tres afirmaciones, y el jugador elige con cuál se queda el protagonista.

#### ◆ D-J5-PATRON · Tablero de deducción

| Opción | Efecto | Monólogo |
|---|---|---|
| **"Los cohetes solo caen sobre los proles."** | ⟶ DUDA +10 · `patron_conclusion = "proles"` | PENSAMIENTO: Once de once. Ninguno a menos de dos kilómetros de un ministerio. Ninguno en un distrito del Partido. (Pausa.) Eurasia tiene cohetes que cruzan el mar… y nunca, ni una sola vez, se equivoca de barrio. |
| **"Eurasia es cobarde: ataca a los débiles."** | ⟶ DUDA +3 · `patron_conclusion = "cobardes"` | PENSAMIENTO: Cobardes. Atacan donde no hay defensas. Donde más duele. Es lo que harían ellos. (Pausa.) Es lo que harían… (Mira la nota de Amory.) Es lo que harían. |
| **"Es casualidad. Once impactos no son nada."** | ⟶ DUDA +0 · SOSPECHA −3 · `patron_conclusion = "casualidad"` | PENSAMIENTO: Casualidad. El azar. Once chinchetas no son una estadística. (Pausa.) Amory diría que sí lo son. Amory no existe. |

**En los tres casos**, el protagonista recuerda la calle Stepney:

PENSAMIENTO: Stepney estaba al borde. Medio Partido, medio prole. (Pausa.) Stepney fue la excepción. Eurasia apuntó a nosotros aquella vez. *(El jugador no puede saber todavía lo que eso significa. Ver J11.)*

⟶ DIARIO +diario_cohetes *(si `patron_conclusion = "proles"` o `"cobardes"`)*

(Brooke pasa junto a la mesa del Registro camino del archivo. Mira de reojo el mapa con la lámina puesta. Sigue andando.)

BROOKE: (sin detenerse, muy bajo) Quite eso del mapa antes de las seis. Voss hace la ronda a las seis.

⟶ Si el jugador **no** retira la lámina antes de terminar la escena: SOSPECHA +10.

### J5.08 — El piso · Noche · El diario

(El protagonista vuelve a casa. Se quita el abrigo. Al colgarlo nota un peso extraño en el bolsillo interior.)

- **[Abrigo]** → USAR →
  (Saca un **cuaderno** pequeño de tapas negras, de papel crema, de antes de la Revolución. Las primeras páginas han sido **arrancadas**. En la cara interior de la tapa, un **pájaro diminuto** dibujado a lápiz.)
  ⟶ ITEM +item_diario
  PENSAMIENTO:
  - Si `dp_j3_amory = "recordar"`: Un pájaro. Es de Amory. Era su cuaderno. ¿Quién…? (Recuerda: la limpiadora, el carrito, los dibujos.) ¿Ella?
  - Si `dp_j3_amory = "aceptar"`: Un pájaro. (El pinchazo en la sien es ahora un dolor sordo.) Alguien que dibujaba pájaros. (Pausa.) Felix. Se llamaba Felix. (Se tapa la boca, como si lo hubiera dicho en voz alta.)
  ⟶ Si `dp_j3_amory = "aceptar"`: DUDA +5 *(el recuerdo vuelve solo)*

PENSAMIENTO: Un cuaderno así es… no es ilegal. Nada es ilegal. Pero si me ven escribiendo en él…

#### Tutorial: EL DIARIO

**Ángulo muerto:** la telepantalla cubre todo el piso **salvo el pequeño hueco entre el armario y la pared del cartel de Ivy**. El jugador debe llevar al protagonista hasta allí (aparece un contorno del cono de visión de la telepantalla al tener el diario en la mano).

- Si intenta abrir el diario dentro del cono: TELEPANTALLA: (genérica) "…camaradas, recuerden la importancia del descanso…" PENSAMIENTO: Aquí no. Aquí me ve. ⟶ SOSPECHA +5 *(solo la primera vez; luego se bloquea la acción)*

**En el hueco:**

PENSAMIENTO: Si escribo algo, ya lo habré hecho. No se puede deshacer. El crimental no se comete escribiendo. Escribir solo lo demuestra.

#### ◆ D-J5-DIARIO

| Opción | Efecto |
|---|---|
| **Escribir** | → Composición de la primera entrada (ver abajo). ⟶ DUDA +5 · `diario_iniciado = true` |
| **Esconderlo sin escribir** | PENSAMIENTO: Todavía no. (Lo esconde detrás del cartel de Ivy.) ⟶ `diario_iniciado = false` · *(El diario queda disponible en el inventario. En J6 y J7 el jugador puede escribir desde el hueco si quiere.)* |

#### Composición de entradas *(mecánica que se repite todo el juego)*

**Mecánica:** el diario muestra una página en blanco. El jugador elige una de las **entradas disponibles** (las que ha desbloqueado con `DIARIO +…`) y, dentro de ella, **una frase** entre 2–3 variantes. Las variantes dependen del tramo de Duda y de decisiones previas. La frase elegida se escribe a mano con animación de lápiz (el de Amory si lo conserva; si no, "un lápiz cualquiera") y queda guardada para el Capítulo II.

**Entradas disponibles en la Jornada 5:**

**`diario_amory`** *(si `dp_j3_amory = "recordar"`, o en todo caso desde J5 si encontró la nota de Amory)*
- a) *"Felix Amory existió. Se sentaba a mi lado. Dibujaba pájaros."*
- b) *"Un hombre puede dejar de haber existido entre la noche y la mañana."*
- c) Si `amory_reaccion = "denuncia"`: *"Yo dije su nombre en voz alta. Después nadie volvió a decirlo."*

**`diario_sammy`**
- a) *"Hoy murió un niño que se llamaba Sammy. Tenía ochenta y cuatro trozos de metralla."*
- b) Si `sammy_intento`: *"Mis dedos tocaron su camisa. No fue suficiente."*
- c) Si no `sammy_intento`: *"Me escondí detrás de un puesto de patatas mientras un niño moría."*

**`diario_cohetes`**
- a) *"Los cohetes solo caen sobre los proles."*
- b) *"Eurasia nunca se equivoca de barrio."*
- c) Si `patron_conclusion = "cobardes"`: *"Eurasia es cobarde. ¿O es otra cosa?"*

**Firma:** cada entrada termina con la fecha. El protagonista duda al escribir el año.
PENSAMIENTO: 1984. Creo. Nadie lo sabe con seguridad.

(Al terminar, el protagonista esconde el diario **detrás del cartel de Ivy**. Animación: despega una esquina del cartel, mete el cuaderno y lo vuelve a pegar. La cara de Ivy queda un poco torcida.)

⟶ `FLAG diario_escondite = "cartel"`

PENSAMIENTO: Perdóname, Ivy. Eres el único sitio donde no miran.

- **[Cama]** → USAR → fin de la jornada.

CARTEL: **JORNADA 6**

---

## JORNADA 6 — El parte

### J6.01 — El piso · 07:15

(Gimnasia. `CF[Entusiasmo, media]`: la instructora acelera. Primera vez que la dificultad sube sin aviso.)

TELEPANTALLA: …el balance del cobarde ataque de ayer sobre Limehouse asciende a siete víctimas. El Partido…

#### CF-J6-NOTICIA · `CF[Duelo patriótico, media]`

PENSAMIENTO (durante el microjuego, en ráfagas que intentan distraer al jugador):
- `[D1]` Siete. Un paréntesis.
- `[D2]` Siete. "Retiren eso."

**Si `duda >= 20`:** la paleta del piso muestra el primer cambio visible: el cartel de Ivy tiene ahora un rojo **ligeramente más cálido** y la luz de la ventana es menos gris.

- **[Cartel de Ivy]** → MIRAR → PENSAMIENTO: Sigue un poco torcido. (Lo endereza.) Ya está.
- **[Puerta]** → salida a J6.02

### J6.02 — La escalera

HILDA: (bajando con prisas, carpeta bajo el brazo) ¡{NOMBRE}! ¿Te has enterado? Ayer cayó uno en Limehouse. En el mercado. Siete. (Pausa.) Bueno, siete proles. (Se encoge de hombros.) Ya sabes.

#### ◆ D-J6-HILDA

| Opción | Efecto |
|---|---|
| "Siete muertos son siete muertos." | HILDA: (se detiene, le mira con atención) "…Claro. Claro que sí." (Anota algo.) ⟶ SOSPECHA +5 · `hilda_aprecio −1` |
| "Eurasia pagará." | HILDA: "¡Eso es! Este sábado, ensayo del cántico de la efigie." · Sin efecto. |
| (Silencio.) | HILDA: "¿Estás bien? Tienes mala cara. ¿Y esa mano?" → "Me corté." · Sin efecto. |

HILDA: (recordando) ¡Ah! Esta tarde paso por tu piso. Inspección del Comité de la Casa. Rutina, rutina. Que no se diga que el bloque no está listo para la Semana del Odio.

PENSAMIENTO: Inspección. (Piensa en el cartel de Ivy.) Esta tarde.

### J6.03 — Departamento de Partes y Cartografía · El archivo

VOSS: Camarada {APELLIDO}. Necesito el **resumen trimestral** del frente de Malabar. Recupere del archivo todos los partes de abril.

**Localización:** sala de archivo del departamento, con estanterías metálicas de cajas grises numeradas por fecha y una mesa de consulta con lámpara verde. Una telepantalla pequeña en el techo, en un ángulo.

**Mecánica:** buscar la caja de *ABRIL 84 — MALABAR* (puzle sencillo de ordenación: las cajas están mal colocadas y hay que encontrar la buena por la numeración). Dentro, una pila de partes. El jugador los revisa uno por uno (4–5 partes con texto breve).

(El tercer parte es el del protagonista. Pero no dice lo que escribió.)

**Comparación en pantalla:** a la izquierda, en sepia, el **recuerdo** del parte de J1 con los valores de `parte_j1`. A la derecha, el **documento** actual.

| | Recuerdo (lo que escribió el jugador) | Documento del archivo |
|---|---|---|
| Fecha | 14.4.84 | **11.4.84** |
| Frente | Malabar | **Mysore** |
| Verbo | {parte_j1.verbo} | **"resistido con firmeza"** |
| Kilómetros | {parte_j1.km} | **0 km** ("posiciones mantenidas") |
| Prisioneros | {parte_j1.prisioneros} | **{parte_j1.prisioneros ÷ 10}** |
| Bajas enemigas | {parte_j1.bajas} | *(eliminado)* |
| Firma | {NOMBRE} {APELLIDO} | **{NOMBRE} {APELLIDO}** |

> **Lógica de la ficción:** una directiva posterior necesita que en abril Malabar "no se moviera" para justificar una ofensiva gloriosa en mayo. El parte de victoria del protagonista sobraba, así que se ha reescrito como un modesto parte de resistencia en otro frente, con fecha anterior. La firma sigue siendo suya porque el Partido no se equivoca: el protagonista siempre escribió eso.

PENSAMIENTO: Esto no es lo que escribí. (Lo lee otra vez.) Esto no es lo que escribí. La telepantalla lo leyó. Toda Oceanía lo oyó. Doce kilómetros… *(o el valor elegido)* …"aplastado al enemigo"… Yo lo oí en mi propia casa.

#### DP-J6-PARTE

(Efecto *glitch*: en el registro de diálogos, la escena J1.07, la del noticiero, se reescribe sola. La telepantalla ahora dice "…han resistido con firmeza en el frente de Mysore…".)

TELEPANTALLA: (íntima, como en J3) Quien controla el pasado controla el futuro. Usted escribió lo que está escrito.

| Opción | Texto | Efecto |
|---|---|---|
| **Aceptar** | *Siempre escribí "resistido con firmeza".* | ⟶ DUDA −5 · SOSPECHA −5 · `dp_j6_parte = "aceptar"` |
| **Recordar** | *Escribí "{parte_j1.verbo}". Escribí {parte_j1.km} kilómetros.* | ⟶ DUDA +15 · `dp_j6_parte = "recordar"` · DIARIO +diario_parte |

**Si `dp_j6_parte = "recordar"` y `diario_iniciado`:** PENSAMIENTO: Lo apuntaré. Esta noche. Cada número.

#### ◆ D-J6-COPIA *(opcional, arriesgada)*

- **[Parte alterado]** → USAR → "Guardarse el documento"
  - Si la telepantalla del techo está mirando (cono visible, rota cada 5 segundos): SOSPECHA +15 y Voss aparece en la puerta: "¿Encuentra lo que busca, camarada?". El jugador debe devolverlo.
  - Si lo hace en el ángulo muerto: ⟶ ITEM +item_parte_alterado. *(Servirá en la iniciación de J8 como prueba de buena fe ante la Hermandad: `FLAG prueba_parte = true`.)*

(El protagonista entrega a Voss el resumen trimestral. Voss lo hojea.)

VOSS: Correcto. Malabar resistió en abril. Mayo será otra historia. (Pausa.) Buen trabajo.

### J6.04 — Estudio Crane · Atardecer *(si `foto_a_crane`; si no, se salta a J6.05)*

(Crane le espera con un sobre de papel marrón.)

CRANE: Tres días, le dije. Han sido dos. (Sonríe.) No podía dormir. Ábralo.

(El protagonista abre el sobre. La **foto restaurada**: el mismo parque, los mismos dos niños. Ivy, de diez años, con el uniforme de los Espías, **sonríe** abiertamente, con un diente mellado. El protagonista, a su lado, le tira de una trenza.)

⟶ ITEM −item_foto_ivy · ITEM +item_foto_ivy_restaurada

PENSAMIENTO: Sonríe. (Pausa larga.) En el cartel no sonríe. (Pausa.) Esta es su cara. Esta es su nariz.

⟶ DUDA +5 · DIARIO +diario_ivy

CRANE: (suave) ¿Es ella?

PROTAGONISTA: Es ella.

CRANE: (se sienta frente al protagonista, sirve dos tazas de té de verdad, que huele distinto) Aquí no hay telepantalla, ¿sabe? (Ríe.) Bueno, eso ya lo habrá notado. En este barrio la gente habla. Es lo único que nos queda. (Pausa.) Usted parece alguien que tiene muchas cosas dentro.

#### Diálogo de Crane — segunda prueba

| Pregunta de Crane | Respuesta cerrada | Respuesta abierta |
|---|---|---|
| "¿Su hermana era tan… entusiasta como dicen los carteles?" | "Era una camarada ejemplar." | "No lo sé. Ya no sé lo que era." ⟶ `crane_info +1` · SOSPECHA +5 |
| "Ayer estuvo usted en el mercado, ¿verdad? Lo siento mucho por el niño de Dot." | "Fue un ataque euroasiático." | "Ese cohete… no debería haber caído ahí." ⟶ `crane_info +1` · SOSPECHA +5 |
| "Si alguna vez necesita un sitio donde pensar en voz alta… mi trastienda está siempre abierta." | "Gracias. No será necesario." | "Puede que lo necesite." ⟶ `crane_info +1` · SOSPECHA +3 · `FLAG crane_trastienda = true` |

**Puntos interactivos:**

- **[Recorte de periódico]** *(enmarcado junto al mostrador, entre otros recortes viejos que Crane usa "para practicar restauraciones")*
  - MIRAR → (Un recorte del *Times* de **marzo de 1984**: *"La ración de chocolate se mantiene en 30 gramos semanales, gracias a la gestión de la Minindancia."*)
  - PENSAMIENTO: Treinta gramos. En marzo. (Pausa.) Y hace unos días la telepantalla dijo que "aumentaba" a veinte.
  - ⟶ DUDA +5 · DIARIO +diario_chocolate · `FLAG chocolate_visto = true`
  - *(Si el jugador intenta llevarse el recorte:)* CRANE: (sin girarse) "Ese no, camarada. Es de mi colección." *(Crane lo ha dejado ahí a propósito: es un cebo. Lo que el protagonista haga después con esa información es lo que Crane quiere ver.)*
- **[Cuarto oscuro]** → MIRAR → (La bombilla roja de encima está **encendida**.) PENSAMIENTO: Hay alguien trabajando ahí dentro. ¿O es una máquina? Se oye un zumbido.
  - *(Seed para J12: es el equipo de grabación.)*

### J6.05 — El piso · La inspección de Hilda

(El protagonista llega a casa. Apenas cierra la puerta, llaman: tres golpes secos.)

HILDA: (desde fuera) ¡Inspección del Comité, {NOMBRE}! ¡Abre, que vengo cargada!

**Si `diario_iniciado` o el diario está en el inventario:**

#### Minijuego: ESCONDER EL DIARIO (contrarreloj, ~6 segundos)

El jugador tiene el diario (y opcionalmente el parte alterado y la foto restaurada) en el inventario. Debe arrastrarlos a un escondite antes de que Hilda abra.

| Escondite | Resultado |
|---|---|
| **Detrás del cartel de Ivy** | Seguro. Hilda nunca tocaría el cartel de una mártir. |
| **Bajo el colchón** | Hilda se sienta en la cama y nota el bulto. Ver "Descubierto" abajo. |
| **En el cajón** | Hilda abre el cajón "para ver si guardas propaganda vieja". Ver "Descubierto". |
| **Dentro del hornillo** | Seguro, pero el diario huele a hollín durante el resto del juego. (Detalle humorístico negro: en J8, Nell dice "Hueles a chimenea".) |
| **No esconderlo a tiempo** | Ver "Descubierto". |

**Descubierto:** Hilda encuentra el cuaderno y lo hojea. Si `diario_iniciado`, lee la primera página.

- Si `hilda_aprecio >= 2`: HILDA: (le mira, confusa) "¿"Felix Amory"? ¿Quién es…? (Se ríe, nerviosa.) ¿Estás escribiendo una novela? ¿Para el Departamento de Ficción?" PROTAGONISTA: "…Ejercicios. Para el comité de la Semana del Odio. Lemas." HILDA: (le devuelve el cuaderno, poco convencida) "…Mucho cuidado con los cuadernos, {NOMBRE}. A la gente le da por escribir y luego…" ⟶ SOSPECHA +15 · `hilda_aprecio = 0`
- Si `hilda_aprecio < 2`: HILDA: (lo cierra y se lo guarda bajo el brazo) "Esto me lo llevo. Lo revisará el Comité." ⟶ SOSPECHA +25 · ITEM −item_diario · `FLAG diario_confiscado = true`
  - *Consecuencia:* en J7, **Nell le devuelve el diario**, rescatado del despacho del Comité ("Los proles también limpian allí"). Esto resuelve el bloqueo, pero el Comité ha leído la primera página: `sospecha` no baja de 40 durante el resto del juego (suelo de Sospecha).

**La inspección (siempre):**

HILDA: (recorre el piso con la carpeta, marcando casillas) Telepantalla en funcionamiento… sí. Retrato del Gran Hermano… sí. Volumen adecuado… sí. (Se para delante del cartel de Ivy.) Ay, qué preciosidad. Está un poco torcido. (Alarga la mano.)

**Si el diario está detrás del cartel:**

#### ◆ D-J6-CARTEL

| Opción | Efecto |
|---|---|
| "¡No! No lo toque, por favor. Es… lo pegué yo. Con mis manos. Es lo único que me queda." | HILDA: (se emociona, retira la mano) "Ay, {NOMBRE}… Claro, claro. Perdona." · Seguro. Si `hilda_aprecio >= 1`, además `hilda_aprecio +1`. |
| (No decir nada.) | Hilda endereza el cartel con cuidado. Se oye un leve roce de papel. Pausa. HILDA: "…Ya está. Perfecto." *(No ha notado nada. Por esta vez.)* ⟶ SOSPECHA +5 *(nerviosismo visible)* |

HILDA: (en la puerta) Por cierto. (Baja la voz.) Me han dicho que te vieron en Limehouse. Dos veces. (Sonrisa.) No es asunto mío, claro. Pero la gente habla. Y yo apunto.

**Si `visita_prole_j4` y `foto_a_crane`:** ⟶ SOSPECHA +5

(Hilda se va. El protagonista se queda apoyado en la puerta.)

- **[Hueco junto al armario]** → USAR con **item_diario** → composición de entradas *(nuevas disponibles: `diario_parte`, `diario_ivy`, `diario_chocolate`)*.

**Nuevas entradas:**

**`diario_parte`**
- a) *"Escribí {parte_j1.km} kilómetros. Ahora he escrito cero. Las dos cosas llevan mi firma."*
- b) *"El pasado no ha ocurrido. Se redacta."*

**`diario_ivy`**
- a) *"Ivy sonreía. Tenía un diente mellado. En el cartel tiene la boca cerrada."*
- b) *"Le cambiaron la nariz para que fuera más fácil llorarla."*

**`diario_chocolate`**
- a) *"Treinta gramos en marzo. Veinte en abril. Y dimos las gracias."*
- b) *"Si no recuerdas cuánto tenías, cualquier cosa es un aumento."*

- **[Cama]** → USAR → fin de la jornada.

CARTEL: **JORNADA 7**

---

## JORNADA 7 — Naranjas y limones

### J7.01 — El piso · 07:15

(Gimnasia. `CF[Entusiasmo, media]`.)

TELEPANTALLA: ¡Camaradas! ¡Faltan diez días para la Semana del Odio! ¡Diez días para mostrar al enemigo la furia de Oceanía!

PENSAMIENTO:
- `[D0]` Diez días. Este año gritaré más que nunca.
- `[D1]` Diez días. (Mira el cartel de Ivy.) Gritaré. Tengo que gritar.
- `[D2]` Diez días para aprender a gritar sin creer.

### J7.02 — Departamento de Partes y Cartografía

(El protagonista se sienta. La cinta de su máquina de escribir se rompe al primer golpe.)

PELL: (sin mirarle) Cuarto de suministros. Al fondo del pasillo. Cintas en la tercera balda.

**Si `diario_confiscado`:** (Al pasar junto a la puerta de Voss, el protagonista ve a Hilda saliendo del despacho. Se cruzan. Hilda le sonríe sin enseñar los dientes.) ⟶ PENSAMIENTO: ¿Hilda? ¿Aquí? ¿En el Minipax?

### J7.03 — Cuarto de suministros

**Localización:** cuarto estrecho y sin ventanas, con estanterías de papel, cintas, tinta, frascos de chinchetas y cajas de lápices. Una bombilla desnuda. **No hay telepantalla**: hay un hueco cuadrado en la pared donde estuvo una, tapado con una tabla. (Es el único ángulo muerto de toda la planta.)

- **[Hueco tapado en la pared]** → MIRAR → PENSAMIENTO: Aquí había una telepantalla. La quitaron. ¿Por qué quitarían una telepantalla?

(El protagonista busca en la tercera balda. Detrás, la puerta se cierra con un clic. Se gira. **Nell** está delante de la puerta, con el carrito bloqueando la salida.)

NELL: (voz baja, ronca, sin ninguna amabilidad) No grites. Aquí no te oye nadie. Pero los pasillos tienen orejas.

PROTAGONISTA: ¿Qué…? Déjeme salir.

NELL: (canta, casi sin voz, mirándole fijamente) *Naranjas y limones, dicen las campanas de San Clemente.*

(El protagonista se queda helado. **Flashback rápido de 2 segundos:** la calle Stepney, la mano de Ivy, Ivy cantando; la mujer del pañuelo apartando cascotes; la misma mirada.)

PROTAGONISTA: …Usted. Usted estaba allí.

NELL: Yo estaba allí. Saqué tres piedras de encima de tu hermana antes de que llegara el hombre del abrigo. (Pausa.) Ella cantaba esa canción porque era la nuestra.

PROTAGONISTA: ¿La… nuestra?

NELL: (ignora la pregunta) Amory no fue el primero. Tu hermana tampoco.

#### Diálogo con Nell (árbol; el jugador puede hacer hasta 4 preguntas antes de que Nell corte)

- **"¿Qué sabe usted de mi hermana?"**
  NELL: Que no murió por lo que te contaron. Y que tú no estás preparad{o|a} para oír el resto. Todavía no.
- **"¿Usted me puso el cuaderno en el abrigo?"**
  NELL: El cuaderno era de Felix. Lo saqué de su papelera antes de que lo hicieran ceniza. (Pausa.) Felix no era de los nuestros. Solo era alguien que veía. Aquí, eso basta para desaparecer.
  - Si `diario_confiscado`: NELL: (saca el cuaderno del carrito) Y esto estaba en el despacho del Comité de tu casa. Los proles también limpian allí. (Se lo da.) Tu vecina lee muy despacio. Ha llegado a la primera página. ⟶ ITEM +item_diario · `diario_confiscado = false`
- **"¿Qué es lo "nuestro"? ¿Quiénes son ustedes?"**
  NELL: (sonrisa torcida, la primera) Eso lo sabrás si das el siguiente paso. Si no, mejor que no lo sepas nunca.
- **"¿Por qué los cohetes solo caen sobre los proles?"** *(solo si `patron_conclusion = "proles"`)*
  NELL: (le mira con algo parecido al respeto) Lo has visto tú solo. Bien. (Pausa.) Esa es exactamente la pregunta. Y la respuesta está a tres plantas de aquí.
- **"Debería denunciarla ahora mismo."**
  NELL: Deberías. (No se mueve.) La puerta está detrás de mí. Voss está a cuarenta pasos. (Pausa.) Ve.

#### La petición

NELL: Hay un papel azul. En el Archivo Restringido de este ministerio, planta once, sala de los cerrojos dobles. Lo llaman la **Planilla Azul**. En ese papel está escrito dónde caerá el próximo cohete. (Pausa.) Antes de que caiga.

PROTAGONISTA: Eso es imposible.

NELL: Entonces no tienes nada que temer al buscarlo.

PROTAGONISTA: ¿Y si lo encuentro?

NELL: Entonces sabrás quién mató a Sammy. (Pausa.) Y a tu hermana.

#### ◆ D-J7-NELL · Decisión clave del Acto II

| Opción | Texto | Resultado |
|---|---|---|
| **Aceptar** | "…¿Cómo entro en el Archivo?" | → J7.04-ACEPTAR |
| **Negarse** | "No. No sé quién es usted. No quiero saberlo." | Si `duda < 30` → **J7.04-NEGAR → FINAL A**. Si `duda >= 30` → J7.04-DUDAR |
| **Denunciar** | (Aparta el carrito de un empujón y sale.) | → **J7.04-DENUNCIAR → FINAL B (versión temprana)** |

### J7.04-ACEPTAR

NELL: (asiente una vez) Mañana por la noche. El turno de guardia de la planta once cambia a las once. Hay cuatro minutos en los que la escalera de servicio no la mira nadie. (Saca del carrito una llave grande y oxidada.) La sala de calderas comunica con el montacargas viejo. El montacargas para en la once.

⟶ ITEM +item_llave_calderas · `FLAG nell_respuesta = "aceptar"`

NELL: Si te cogen, no me conoces. Yo tampoco te conozco. Nunca te he visto. (Pausa.) Eso no es una amenaza. Es lo único que puedo hacer por ti.

(Nell abre la puerta y sale empujando el carrito, con la cabeza gacha, otra vez invisible.)

**Si `sospecha >= 50`:** (Antes de salir, Nell se detiene.) NELL: Te están mirando. Lo sé por cómo te mira tu jefe. Ten cuidado con quién hablas fuera de aquí. Sobre todo con la gente amable. ⟶ *(Pista temprana sobre Crane para el jugador atento.)*

→ J7.05

### J7.04-DUDAR *(negarse con `duda >= 30`)*

NELL: (no se aparta) Mientes mal. Lo veo en tu cara. Llevas días mintiendo mal. (Pausa.) Piénsalo esta noche. Mañana por la noche estaré aquí a las diez y media. Si no vienes, no volverás a verme.

(Sale. El protagonista se queda solo en el cuarto.)

→ J7.05 con la decisión pendiente. Al final de J7.05, en el piso, el jugador vuelve a decidir (ver **◆ D-J7-NOCHE** abajo).

### J7.04-NEGAR → FINAL A

NELL: (le mira largo; algo se apaga en su cara) Como tu hermana no. Ella habría dicho que sí. (Abre la puerta.) Que vivas mucho, camarada.

(Sale. El protagonista se queda solo. Coge la cinta de máquina de la tercera balda. Le tiemblan las manos. Vuelve a su mesa.)

→ **FINAL A — "Doblemásbueno"** (ver abajo)

### J7.04-DENUNCIAR → FINAL B (temprano)

(El protagonista aparta el carrito de un empujón, sale al pasillo y camina hacia el despacho de Voss. A cada paso, el pasillo se alarga, como en el sueño de Ivy.)

(Despacho de Voss.)

PROTAGONISTA: Subdirector. La limpiadora. La del carrito. Me ha… me ha hablado de una Planilla Azul. Me ha pedido que entre en el Archivo Restringido.

VOSS: (deja la pluma; por primera vez, parece sinceramente interesado) Siéntese, camarada. (Apaga la telepantalla de su despacho con un gesto.) Cuénteme todo. Despacio. Desde el principio.

(Fundido.)

→ **FINAL B — "El fotógrafo"** (versión temprana; ver [05-finales.md](05-finales.md#final-b--el-fotógrafo)). Diferencias con la versión de la Jornada 12: Nell es detenida esa misma tarde, la célula de la Hermandad no llega a conocer al protagonista y Crane le recluta en lugar de Voss ("El Subdirector me ha hablado mucho de usted. Tiene buen ojo. Igual que yo.").

### J7.05 — El piso · Noche

(El protagonista en su piso. La telepantalla emite música marcial.)

**Si `nell_respuesta = "aceptar"`:**

- **[Llave de calderas]** → MIRAR → PENSAMIENTO: Una llave. Mañana a las once. (Pausa.) Si la Planilla Azul no existe, no habré hecho nada malo. Solo habré mirado un papel en mi propio ministerio. (Pausa.) Si existe…
- **[Hueco junto al armario]** → USAR con **item_diario** → composición de entradas. *Nueva entrada desbloqueada:*

**`diario_nell`**
- a) *"Una mujer sin nombre sacó tres piedras de encima de Ivy. Llevo cinco años sin verla."*
- b) *"Los proles también limpian. Lo ven todo. Nadie les ve a ellos."*

- **[Cartel de Ivy]** → MIRAR →
  PENSAMIENTO: "Ella habría dicho que sí." (Pausa.) Eso no lo ha dicho. Pero lo ha pensado. Lo he visto en su cara. (Toca el borde del cartel, donde está escondido el diario.) ¿Habrías dicho que sí, Ivy?

**Si `duda >= 30` y negó (◆ D-J7-NOCHE):**

PENSAMIENTO: "Si no vienes, no volverás a verme."

| Opción | Resultado |
|---|---|
| **Volver mañana al cuarto de suministros** | Escena corta en J8.00 (al inicio del Acto III): Nell espera a las diez y media, le da la llave sin decir nada y le explica el plan. ⟶ `nell_respuesta = "aceptar_tarde"` |
| **No volver** | → **FINAL A** |

(Fundido lento. Un silbido lejano. Un impacto, en algún barrio prole.)

**Si `nell_respuesta` = aceptar:**

PENSAMIENTO: Mañana sabré dónde caerá el próximo.

CARTEL: **FIN DEL ACTO II**

CARTEL: **ACTO III — LA HERMANDAD**

---

## FINAL A — "Doblemásbueno"

> Se dispara al negarse a Nell en la Jornada 7 (con Duda baja, o tras dudar una noche). Duración: ~5 min. Es un final completo, no un game over.

### FA.01 — El piso · Esa misma noche

(El protagonista en el hueco junto al armario, con el diario en las manos. La telepantalla, a su espalda, emite el himno.)

PENSAMIENTO: Un cuaderno de un hombre que no existió. Una prole que dice cosas imposibles. Un papel azul que no existe. (Pausa.) Estoy cansad{o|a}. Voss tenía razón: el cansancio produce recuerdos que no existen.

(El protagonista sale del hueco, a la vista de la telepantalla, con el diario en la mano.)

### FA.02 — La puerta de Hilda

HILDA: (en bata, con la luz del pasillo detrás) ¿{NOMBRE}? ¿A estas horas?

PROTAGONISTA: (le tiende el diario) Lo encontré. En el Minipax. Creo que… creo que el Comité debería verlo.

(Hilda lo abre. Lee. Levanta la vista. En su cara hay emoción verdadera.)

HILDA: Ay, {NOMBRE}. (Le abraza.) Lo sabía. Sabía que eras de los buenos.

### FA.03 — Montaje · Las semanas siguientes

(Secuencia de 4–5 viñetas fijas en pixel art, con la telepantalla de fondo y música marcial cada vez más alta:)

1. **Minipax:** el carrito de la limpieza, abandonado en mitad del pasillo. Otra limpiadora, más joven, vacía las papeleras.
2. **Despacho de Voss:** Voss estrecha la mano del protagonista. En la mesa, una mención enmarcada: *"Por su vigilancia ejemplar."*
3. **Mercado de Watney Street:** el puesto de Dot, vacío, con el toldo arrancado.
4. **El piso:** el cartel de Ivy, recto y perfecto. Ya no hay nada detrás.
5. **La telepantalla de la cantina:** **Amory**, demacrado y sin dientes, confiesa ser espía euroasiático. El protagonista lo mira y escupe en el suelo. PENSAMIENTO: Traidor.

### FA.04 — La Semana del Odio · La plaza

(La gran plaza llena hasta los bordes. Banderas, efigies, pancartas. El protagonista en primera fila, junto a Hilda y Parsons. El orador grita desde la tribuna.)

ORADOR: …¡y Eurasia, con su barbarie…! (Un hombre le pasa un papel. El orador lo lee sin detenerse.) …¡Estasia! ¡Estasia, con su barbarie, que desde siempre…!

(La multitud duda medio segundo y luego ruge. El protagonista también ruge. No hay crimen facial: **la cara del protagonista no necesita control**.)

PENSAMIENTO: (es el último pensamiento del juego y no tiene variantes de Duda) Estasia. Siempre fue Estasia. Siempre. (Pausa.) Qué alivio no tener que recordar nada.

(La paleta pierde todo el color que hubiera ganado. Solo grises. Incluso el rojo de las banderas se vuelve gris.)

### FA.05 — Cierre

(Primer plano del protagonista mirando el rostro del Gran Hermano en una pantalla gigante. Le cae una lágrima. Sonríe.)

CARTEL: *Había vencido sobre sí mism{o|a}.*

CARTEL: *Amaba al Gran Hermano.*

(Negro. Créditos con el himno del Partido, perfectamente afinado.)

> **Desbloqueo:** al terminar el Final A, el menú principal muestra una línea nueva bajo "Nueva partida": *"Naranjas y limones…"* (pista para otra partida).

---

## Resumen de variables del Acto II

| Variable | Valores | Se fija en |
|---|---|---|
| `zonificacion_encontrada` | bool | J4.03 / J5.07 |
| `visita_prole_j4` | bool | J4.05 |
| `dot_confianza` | 0–4 | J4.07, J4.07 (metralla), J5.02, J5.05 |
| `foto_a_crane` | bool | J5.01 |
| `crane_info` | 0–4 | J5.03, J6.04 |
| `crane_trastienda` | bool | J6.04 |
| `sammy_intento` | bool | J5.04 |
| `patron_conclusion` | `proles` / `cobardes` / `casualidad` | J5.07 |
| `diario_iniciado` | bool | J5.08 / J6.05 / J7.05 |
| `diario_escondite` | `cartel` / `hornillo` / … | J5.08, J6.05 |
| `diario_confiscado` | bool | J6.05 (se resuelve en J7.03) |
| `dp_j6_parte` | `aceptar` / `recordar` | J6.03 |
| `prueba_parte` | bool | J6.03 |
| `chocolate_visto` | bool | J6.04 |
| `nell_respuesta` | `aceptar` / `aceptar_tarde` / `negar` / `denunciar` | J7.03 / J7.05 |

**Inventario posible al final del acto:** reloj de Ivy, lápiz de Amory, foto de Ivy (original o restaurada), tarjeta de Crane, lámina de zonificación, compás, nota de Amory, metralla de Sammy, metralla brillante, diario, parte alterado, llave de calderas.

**Entradas de diario posibles:** `diario_amory`, `diario_sammy`, `diario_cohetes`, `diario_parte`, `diario_ivy`, `diario_chocolate`, `diario_nell`.

## Equilibrio estimado de la Duda al llegar a J7

| Perfil de jugador | Duda aproximada | Resultado más probable |
|---|---|---|
| Lo acepta todo y no se arriesga | 10–25 | Final A |
| Curioso pero prudente | 35–55 | Acto III |
| Lo recuerda todo y se arriesga | 60–90 | Acto III con mucha Sospecha |

## Semillas plantadas en este acto

| Semilla | Dónde | Se recoge en |
|---|---|---|
| Stepney "estaba al borde": la excepción | J5.07 | J11 (orden de Voss sobre calle Stepney 14) |
| Cuarto oscuro con zumbido y bombilla encendida | J6.04 | J12 (equipo de grabación de Crane) |
| Brooke en una foto de boda prole del estudio de Crane | J5.03 | Acto III (Brooke es pariente de alguien del barrio y contacto pasivo de la Hermandad; Crane también la vigila) |
| Campana de "S. Clem…" en el pub | J4.08 | J13 (la campana robada de San Clemente) |
| El metro "cerrado por reformas" | J4.07 | J13 (los túneles hacia San Clemente) |
| Telepantalla retirada del cuarto de suministros | J7.03 | J8 (la Hermandad la quitó haciéndose pasar por reparadores) |
| Nell: "Cuidado con la gente amable" | J7.04 | J12 (revelación de Crane) |
| Hilda en el despacho de Voss | J7.02 | J10–J11 (Hilda informa a Voss, no solo al Comité) |
| Metralla de Sammy | J4.07, J5.05 | J13 (llave simbólica para Dot; Final D) |

## Ajustes a la biblia ([guion.md](../guion.md)) introducidos aquí

- **El diario se esconde detrás del cartel de Ivy.** El único ángulo muerto del piso está junto a él.
- **Hilda puede confiscar el diario** en J6 y Nell lo recupera en J7. Si eso ocurre, la Sospecha queda con un mínimo de 40 durante el resto del juego.
- **El parte alterado cambia también de frente** (de Malabar a Mysore), además de la fecha y las cifras.
- **Brooke** aparece como contacto pasivo y ambiguo, que avisa al protagonista dos veces.
- **El Final A** se escribe completo en este acto, porque solo se puede activar aquí.
