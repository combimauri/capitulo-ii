// FINALES QUE SE DECIDEN EN EL ACTO II (guion: 02-acto-2.md «Final A» · 05-finales.md «Final B», variante temprana)
// Los montajes usan viñetas fijas (# vineta:clave) bajo el texto.

// ==================================================================== FINAL A — «Doblemásbueno»
=== final_a ===
// FA.01 — El piso · Esa misma noche
{ inventario ? diario:
    PENSAMIENTO: En el hueco junto al armario, con el cuaderno en las manos. La telepantalla, a mi espalda, emite el himno. # id:fa_01_pens_00
- else:
    PENSAMIENTO: En el hueco junto al armario, con las manos vacías. La telepantalla, a mi espalda, emite el himno. # id:fa_01_pens_00b
}
PENSAMIENTO: Un cuaderno de un hombre que no existió. Una prole que dice cosas imposibles. Un papel azul que no existe. # id:fa_01_pens_01
PENSAMIENTO: Estoy cansad{o}. Voss tenía razón: el cansancio produce recuerdos que no existen. # id:fa_01_pens_02
PENSAMIENTO: Salgo del hueco. A la vista de la telepantalla. # fx:negro # id:fa_01_pens_03

// FA.02 — La puerta de Hilda
HILDA: ¿{nombre}? ¿A estas horas? # vineta:loc-escalera # fx:aclarar # id:fa_02_hilda_01
{ inventario ? diario:
    PROTAGONISTA: Lo encontré. En el Minipax. Creo que… creo que el Comité debería verlo. # id:fa_02_prot_01
    ~ inventario -= diario
    PENSAMIENTO: Lo abre. Lee. Levanta la vista. En su cara hay emoción verdadera. # id:fa_02_pens_00
- else:
    PROTAGONISTA: Hiciste bien en llevarte el cuaderno, Hilda. Quería decírtelo. # id:fa_02_prot_02
    PENSAMIENTO: Se le humedecen los ojos. # id:fa_02_pens_01
}
HILDA: Ay, {nombre}. # id:fa_02_hilda_02
HILDA: Lo sabía. Sabía que eras de los buenos. # id:fa_02_hilda_03
PENSAMIENTO: Me abraza. # id:fa_02_pens_02

// FA.03 — Montaje · Las semanas siguientes
CARTEL: Las semanas siguientes. # vineta:fin # id:fa_03_cartel
PENSAMIENTO: En el Minipax, el carrito de la limpieza, abandonado en mitad del pasillo. Otra limpiadora, más joven, vacía las papeleras. # vineta:loc-pasillo # id:fa_03_01
PENSAMIENTO: Voss me estrecha la mano. En la mesa, una mención enmarcada: «Por su vigilancia ejemplar». # vineta:loc-despacho_voss # id:fa_03_02
PENSAMIENTO: En el mercado de Watney Street, el puesto de Dot, vacío, con el toldo arrancado. # vineta:loc-mercado # id:fa_03_03
PENSAMIENTO: El cartel de Ivy, recto y perfecto. Ya no hay nada detrás. # vineta:loc-piso_noche # id:fa_03_04
PENSAMIENTO: En la telepantalla de la cantina, Amory, demacrado y sin dientes, confiesa ser espía euroasiático. # vineta:loc-cantina # id:fa_03_05
PENSAMIENTO: Lo miro. Escupo en el suelo. # id:fa_03_06
PENSAMIENTO: Traidor. # id:fa_03_07

// FA.04 — La Semana del Odio · La plaza
PENSAMIENTO: La Semana del Odio. La plaza, llena hasta los bordes. Banderas, efigies, pancartas. Estoy en primera fila, junto a Hilda y a Parsons. # vineta:vineta-plaza # id:fa_04_pens_00
ORADOR: …¡y Eurasia, con su barbarie…! # id:fa_04_orador_01
PENSAMIENTO: Un hombre le pasa un papel. Lo lee sin detenerse. # id:fa_04_pens_01
ORADOR: …¡Estasia! ¡Estasia, con su barbarie, que desde siempre…! # id:fa_04_orador_02
PENSAMIENTO: La multitud duda medio segundo. Luego ruge. Yo también rujo. La cara no necesita control. # id:fa_04_pens_02
PENSAMIENTO: Estasia. Siempre fue Estasia. Siempre. # vineta:vineta-plaza_gris # id:fa_04_pens_03
PENSAMIENTO: Qué alivio no tener que recordar nada. # esperar:1.2 # id:fa_04_pens_04

// FA.05 — Cierre
PENSAMIENTO: El rostro del Gran Hermano en la pantalla gigante. Me cae una lágrima. Sonrío. # id:fa_05_pens_00
CARTEL: Había vencido sobre sí mism{o}. # vineta:fin # id:fa_05_cartel_01
CARTEL: Amaba al Gran Hermano. # id:fa_05_cartel_02
CARTEL: FINAL A · DOBLEMÁSBUENO # id:fa_05_fin # final:A
-> DONE

// ==================================================================== FINAL B — «El fotógrafo»
// Variantes de entrada (05-finales.md): B-temprano (J7, denunciar a Nell ante Voss) y B-trato (J12, aceptar a Crane).
// J7.04-DENUNCIAR: el despacho de Voss (voss_despacho.entrar desvía aquí en la Jornada 7)
=== final_b ===
PROTAGONISTA: Subdirector. La limpiadora. La del carrito. Me ha… me ha hablado de una Planilla Azul. Me ha pedido que entre en el Archivo Restringido. # id:fb_00_prot_01
PENSAMIENTO: Deja la pluma. Por primera vez parece sinceramente interesado. # id:fb_00_pens_00
VOSS: Siéntese, camarada. # id:fb_00_voss_01
PENSAMIENTO: Apaga la telepantalla de su despacho con un gesto. # id:fb_00_pens_01
VOSS: Cuénteme todo. Despacio. Desde el principio. # id:fb_00_voss_02

// FB.01 — La entrega
PENSAMIENTO: Lo cuento todo. Durante horas. El cuarto de suministros. La canción. La Planilla Azul. # fx:negro # id:fb_01_pens_00
PENSAMIENTO: Voss escucha sin interrumpir, tomando notas con su pluma. # id:fb_01_pens_01
VOSS: Su hermana estaría orgullosa. # fx:aclarar # id:fb_01_voss_01
VOSS: De verdad lo creo. # id:fb_01_voss_02
-> caida

// FB.02 — La caída
= caida
PENSAMIENTO: La Campana: la puerta reventada. La campana de «S. Clem…», arrancada de la barra y tirada en el suelo. # vineta:loc-pub,gris=si # id:fb_02_01
PENSAMIENTO: En el Minipax, el carrito de la limpieza lo empuja ahora otra limpiadora, más joven, con la cabeza gacha. # vineta:loc-pasillo # id:fb_02_02
{
- fb_variante == "san_clemente":
    PENSAMIENTO: La casa de Dot: la puerta verde, abierta. La colección de metralla de Sammy, desparramada por el suelo de la cocina. Unas botas la pisan. # vineta:loc-casa_dot,gris=si # id:fb_02_dot_sc
    PENSAMIENTO: Parque de la Victoria. El patíbulo. En las cuerdas: Dot.{len_salvado: Len.} Nadie más. # vineta:vineta-patibulo # id:fb_02_03_sc
- fb_variante != "temprano":
    PENSAMIENTO: La casa de Dot: la puerta verde, abierta. La colección de metralla de Sammy, desparramada por el suelo de la cocina. Unas botas la pisan. # vineta:loc-casa_dot,gris=si # id:fb_02_dot
    PENSAMIENTO: Parque de la Victoria. El patíbulo. En las cuerdas: Nell, con su pañuelo. Barlow.{len_salvado: Len.} Dot. # vineta:vineta-patibulo5 # id:fb_02_03_trato
- else:
    PENSAMIENTO: Parque de la Victoria. El patíbulo. En las cuerdas, la limpiadora, con su pañuelo. A su lado, un hombre al que no conozco. # vineta:vineta-patibulo # id:fb_02_03
}
PENSAMIENTO: Abajo, la multitud. Los hijos de Parsons, con Hilda, en primera fila. Yo estoy en la tribuna, junto a Voss. # id:fb_02_04
PENSAMIENTO: Es fácil. Muy fácil. # cf:id=CF-FB-EJECUCION,expr=jubilo,dif=facil,golpes=8,coro=¡Muerte!/¡Traidores! # id:fb_02_05
PENSAMIENTO: Ya no cuesta. # id:fb_02_06
-> reclutamiento

// FB.03 — El reclutamiento
= reclutamiento
{ fb_variante == "san_clemente":
    PENSAMIENTO: Allí abajo no había nadie. El Partido le protege. Lo sé. Y lo entierro. # id:fb_03_entierra
}
PENSAMIENTO: El despacho de Voss. Por primera vez se quita los dos guantes delante de mí. Tiene las manos muy blancas. # vineta:loc-despacho_voss # id:fb_03_pens_00
VOSS: Su expediente. Puede leerlo. Se lo ha ganado. # id:fb_03_voss_01
CARTEL: FAMILIAR DIRECTO: {apellido}, {nombre}¶Potencial de aprovechamiento: ALTO · CONFIRMADO.¶Reasignación: Policía del Pensamiento. Distrito Sur.¶Bajo supervisión de A. Crane. # id:fb_03_expediente
{ ivy_revelada:
    PENSAMIENTO: «Confirmado.» # esperar:1 # id:fb_03_confirmado_01
    PENSAMIENTO: Lo decidieron hace cinco años. Yo solo he llegado tarde a mi propio destino. # id:fb_03_confirmado_02
- else:
    PENSAMIENTO: «Familiar directo.» ¿Familiar de qué? # id:fb_03_pens_01
    PENSAMIENTO: Hojeo hacia atrás. «Sujeto: {apellido}, Ivy. Actividad: miembro de la organización conocida como la Hermandad.» # id:fb_03_pens_02
    PENSAMIENTO: Cierro la carpeta. No. No lo he leído. No lo he leído. # id:fb_03_pens_03
}
VOSS: Crane le enseñará el oficio. Es el mejor. # id:fb_03_voss_02
{ fb_variante != "temprano":
    VOSS: Tiene usted buen ojo, {apellido}. Su hermana también lo tenía. Lo usó mal. # id:fb_03_voss_03
}
CRANE: El Subdirector me ha hablado mucho de usted. Tiene buen ojo. Igual que yo. # vineta:loc-estudio_j6 # id:fb_03_crane_01
-> en_el_estudio

// FB.04 — El estudio
= en_el_estudio
CARTEL: Unos meses después. # vineta:fin # id:fb_04_cartel
PENSAMIENTO: Un estudio de fotografía pequeño y cálido, en Southwark. Suena la campanilla de la puerta. # vineta:loc-estudio_j6 # id:fb_04_pens_00
PENSAMIENTO: Entra una mujer prole joven con un pañuelo en la cabeza. Trae una foto estropeada por el agua: un niño pequeño, sonriendo. # id:fb_04_pens_01
MUJER: Me han dicho que usted… que restaura fotos. # id:fb_04_mujer_01
PENSAMIENTO: Detrás del mostrador, en mangas de camisa y con chaleco de lana: yo. # id:fb_04_pens_02
PROTAGONISTA: Pase, pase. Siéntese. Aún no he encendido la estufa, perdone el frío. # id:fb_04_prot_01
PROTAGONISTA: Agua. Lo peor para una fotografía. Pero la cara está ahí. Debajo de la mancha, la cara siempre sigue ahí. # id:fb_04_prot_02
MUJER: Era mi hijo. Le cayó un cohete. # id:fb_04_mujer_02
PROTAGONISTA: Lo siento mucho. De verdad. # id:fb_04_prot_03
PROTAGONISTA: ¿Y cómo era? Quiero decir… ¿qué le gustaba? # id:fb_04_prot_04
PENSAMIENTO: La bombilla roja del cuarto oscuro zumba. # id:fb_04_pens_03
CARTEL: Restauro fotografías antiguas. # vineta:fin # id:fb_04_cartel_01
CARTEL: Recuerdos que el tiempo borra. # id:fb_04_cartel_02
CARTEL: FINAL B · EL FOTÓGRAFO # id:fb_04_fin # final:B
-> DONE

// J12.04 — Aceptar el trato de Crane (B-trato)
=== final_b_trato ===
PROTAGONISTA: …¿Qué quiere saber? # id:fbt_00_prot_01
PENSAMIENTO: Crane sonríe. Pone una bobina nueva en la grabadora. # id:fbt_00_pens_00
CRANE: Despacio. Que se oiga bien. # id:fbt_00_crane_01
PENSAMIENTO: Hablo mientras la grabadora gira. Dot. {len_salvado:Len, vivo. }San Clemente. Las campanas. # fx:negro # id:fbt_01_pens_00
PENSAMIENTO: Al terminar, Crane me sirve más té. # fx:aclarar # id:fbt_01_pens_01
CRANE: ¿Ve? No duele. # esperar:0.8 # id:fbt_01_crane_01
CRANE: Lo que duele es callar. # id:fbt_01_crane_02
-> final_b.caida

// J13.00 — Volver con Crane al amanecer (B-arrepentimiento)
=== final_b_arrepentimiento ===
PENSAMIENTO: La calle Cable. El estudio. Llamo una vez. # fx:negro # id:fba_00_pens_00
PENSAMIENTO: Crane abre la puerta sin sorpresa. # fx:aclarar # vineta:loc-estudio_j12 # id:fba_00_pens_01
CRANE: Sabía que vendría. # esperar:0.8 # id:fba_00_crane_01
PENSAMIENTO: Se aparta para dejarme pasar. # id:fba_00_pens_02
CRANE: Siempre vienen. El té está hecho. # id:fba_00_crane_02
PENSAMIENTO: Lo cuento todo. Los dibujos de Amory. El mensaje de Nell. La despensa de Dot. # fx:negro # id:fba_01_pens_00
PENSAMIENTO: La grabadora gira. # fx:aclarar # id:fba_01_pens_01
-> final_b.caida

// J13.08 — Entregar a Goldstein (B-San Clemente)
=== final_b_san_clemente ===
PENSAMIENTO: Salgo del metro a la calle. Crane espera en la esquina, apoyado en la farola. # vineta:loc-shadwell # id:fbs_00_pens_00
PROTAGONISTA: Está abajo. Con el libro. # id:fbs_00_prot_01
PENSAMIENTO: Crane sonríe y hace sonar el silbato. Botas. Diez hombres de negro bajan por la boca de metro. # sfx:alto # id:fbs_00_pens_01
PENSAMIENTO: Espero en la calle. Pasa una hora. # fx:negro # esperar:2 # id:fbs_00_pens_02
PENSAMIENTO: Los hombres suben. No traen a nadie. # fx:aclarar # id:fbs_00_pens_03
PENSAMIENTO: El oficial al mando habla con Crane en voz baja. A Crane se le borra la sonrisa. # id:fbs_00_pens_04
CRANE: Allí abajo no hay nadie. # esperar:1 # id:fbs_00_crane_01
CRANE: Nunca ha habido nadie. # esperar:1 # id:fbs_00_crane_02
PENSAMIENTO: Me mira con algo nuevo: miedo. # id:fbs_00_pens_05
CRANE: Hay presas que no se cobran, camarada. # esperar:1 # id:fbs_00_crane_03
CRANE: Usted y yo cobraremos las otras. # id:fbs_00_crane_04
-> final_b.caida
