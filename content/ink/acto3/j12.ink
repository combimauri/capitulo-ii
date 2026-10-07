// ACTO III · JORNADA 12 — La oferta (guion: docs/guion-detallado/03-acto-3.md)
// La ejecución en el parque, el carrito vacío, la foto del sótano, Crane y su grabadora,
// la persecución por Limehouse y la despensa de Dot.

// ==================================================================== J12.01 — Parque de la Victoria · La ejecución
=== j12_piso ===
{ ejecucion_vista:
    -> DONE
}
PENSAMIENTO: Asistencia obligatoria. Toda la plantilla del Minipax. # id:j12_00_pens_00
-> DONE

=== j12_parque ===
{ ejecucion_vista:
    # escena:escalera # pos:piso
    -> DONE
}
~ ejecucion_vista = true
CARTEL: Parque de la Victoria. # fx:negro # id:j12_01_cartel
PENSAMIENTO: El parque, lleno. Familias con niños, vendedores de cacahuetes. Los Espías en primera fila, con Hilda. Un patíbulo con cinco cuerdas. # vineta:vineta-patibulo5 # fx:aclarar # musica:odio_altavoz # id:j12_01_pens_00
{ len_salvado:
    PENSAMIENTO: Suben los prisioneros. Los reconozco de la lista: Chen, Koval, Hogan… y en el lugar de Pike, {len_sustituto}. # id:j12_01_salvado_01
    { len_chico:
        PENSAMIENTO: Dieciséis años. No tenía cara de nada. Ahora tiene cara. # id:j12_01_chico
    }
    PENSAMIENTO: Entre la multitud, al fondo, Dot. Sola, con su pañuelo. Mira el patíbulo. No llora. # id:j12_01_dot_01
    PENSAMIENTO: Luego me mira a mí. En sus ojos hay algo que no sé leer. Gratitud o terror. # id:j12_01_dot_02
    ~ dot_confianza += 2
- else:
    PENSAMIENTO: Suben los prisioneros. El cuarto es Len Pike. Con el ancla en el cuello. Busca algo entre la multitud con los ojos. # id:j12_01_len_01
    PENSAMIENTO: Entre la multitud, Dot. Grita. Es el único grito de dolor en una multitud que grita de júbilo. Dos hombres la sujetan. # id:j12_01_len_02
    { len_decision != "":
        PENSAMIENTO: Diez segundos. Tuve la lista diez segundos. # id:j12_01_len_03
    }
}
PENSAMIENTO: La multitud ruge. # cf:id=CF-J12-EJECUCION # id:j12_01_pens_01
{ cf_j12_ejecucion == "fallo":
    ~ sube_sospecha(10)
}
PENSAMIENTO: Las trampillas se abren. # fx:negro # musica:silencio # id:j12_01_pens_02
PENSAMIENTO: La madera. La multitud que ruge. # sfx:trampilla # sfx:multitud # esperar:1.5 # id:j12_01_pens_03
PENSAMIENTO: Y, después, un niño que aplaude. # vineta:fin # id:j12_01_pens_04
CARTEL: Ministerio de la Paz. # id:j12_02_cartel # escena:pasillo # pos:escalera
-> DONE

// ==================================================================== J12.02 — El carrito vacío
=== j12_pasillo ===
{ nell_aviso:
    -> DONE
}
PENSAMIENTO: En el pasillo, junto al cuarto de suministros, el carrito de Nell. Abandonado. Un cubo volcado, lejía derramada. Nadie lo recoge. # fx:aclarar # id:j12_02_pens_00
-> DONE

=== j12_carrito_mirar ===
PENSAMIENTO: El carrito de Nell. # esperar:0.8 # id:j12_02_carrito_01
PENSAMIENTO: Nadie lo mira. Nadie la mira nunca. Y ahora tampoco miran que no esté. # id:j12_02_carrito_02
-> DONE

=== j12_carrito_usar ===
{ nell_aviso:
    PENSAMIENTO: El doble fondo, vacío. # id:j12_02_carrito_vacio
    -> DONE
}
~ nell_aviso = true
PENSAMIENTO: El doble fondo está vacío. Solo un trozo de papel arrugado, escrito a lápiz, deprisa. # sfx:papel # id:j12_02_carrito_03
PENSAMIENTO: Nell. # documento:nota_carrito # id:j12_02_carrito_04
-> DONE

=== j12_entrar ===
{ brooke_j12:
    -> DONE
}
~ brooke_j12 = true
PENSAMIENTO: Brooke se acerca a la máquina de café, junto a mi mesa. Ninguno de los dos se mira. # id:j12_02_pens_01
{ len_salvado:
    BROOKE: Mi hermano no estaba en el patíbulo. # esperar:0.8 # id:j12_02_brooke_01
    BROOKE: Sé lo que hizo. No sé si darle las gracias. Había un chico… # esperar:1 # id:j12_02_brooke_02
    PENSAMIENTO: Se calla. # id:j12_02_pens_02
- else:
    BROOKE: Mi hermano estaba en el patíbulo. # esperar:1 # id:j12_02_brooke_03
    BROOKE: No le culpo. No podía hacer nada. Ninguno podemos. # id:j12_02_brooke_04
}
BROOKE: A Nell se la llevaron anoche. Y a Barlow, el de La Campana. # id:j12_02_brooke_05
BROOKE: Alguien estaba en ese sótano, además de ustedes tres. # esperar:0.8 # id:j12_02_brooke_06
BROOKE: Váyase a casa por la ruta de siempre. No se pare en ningún sitio. Y no hable con nadie amable. # id:j12_02_brooke_07
~ sube_duda(5)
{ crane_sospechado:
    PENSAMIENTO: «Nadie amable.» Crane. # id:j12_02_crane
}
-> j12_sobre

// ==================================================================== J12.03 — Un sobre en el tubo
=== j12_sobre ===
PENSAMIENTO: Vuelvo a mi mesa. El tubo neumático silba. # sfx:tubo # id:j12_03_pens_00
PENSAMIENTO: Dentro del cilindro no hay una directiva. Hay un sobre de papel marrón. Como el de la foto de Ivy. # id:j12_03_pens_01
PENSAMIENTO: Una fotografía. # documento:sobre_crane # musica:crane_oscuro # id:j12_03_pens_02
PENSAMIENTO: El sótano de La Campana. La vela, Nell, Barlow… y yo, de perfil, contestando a sus preguntas. # id:j12_03_pens_03
PENSAMIENTO: Tomada desde un ángulo bajo. A través del hueco de la pared. # esperar:1 # id:j12_03_pens_04
{ inventario ? foto_sotano:
    PENSAMIENTO: Saco la foto del expediente de Ivy y las pongo una al lado de la otra. # id:j12_03_fotos_01
    PENSAMIENTO: El mismo ángulo. El mismo hueco en la pared. # esperar:1 # id:j12_03_fotos_02
    PENSAMIENTO: Hace cinco años ya estaba ahí. # id:j12_03_fotos_03
    ~ sube_duda(5)
    PENSAMIENTO: Crane hizo la foto de Ivy. Crane la mató antes que Voss. # id:j12_03_fotos_04
- else:
    PENSAMIENTO: El mismo ángulo que la foto del expediente de Ivy. Hace cinco años ya estaba ahí. # id:j12_03_fotos_05
}
~ crane_revelado = true
PENSAMIENTO: «A. C.» # id:j12_03_pens_05
* [Acudir a la calle Cable esta noche.] # decision:D-J12-HUIR
    PENSAMIENTO: Tengo que saber. # id:j12_03_acudir
    CARTEL: Calle Cable, 7. Las diez. # fx:negro # id:j12_04_cartel # escena:estudio # pos:puerta
* [No ir. Huir a casa de Dot.]
    ~ crane_decision = "huir"
    PENSAMIENTO: No voy. Esta noche no voy a casa. Voy a Limehouse. # id:j12_03_huir
    CARTEL: Limehouse. De noche. # fx:negro # id:j12_06_cartel_huir # escena:callejones # pos:inicio
- -> DONE

// ==================================================================== J12.04 — Estudio Crane · La trastienda
=== j12_estudio ===
{ estudio_j12_visto:
    -> DONE
}
~ estudio_j12_visto = true
PENSAMIENTO: El estudio, a oscuras salvo la bombilla roja del cuarto oscuro. Que ahora está abierto. # fx:aclarar # id:j12_04_pens_00
PENSAMIENTO: Crane, en mangas de camisa, sirve té. Como siempre. # id:j12_04_pens_01
CRANE: Pase, pase. Siéntese. El té está recién hecho. # id:j12_04_crane_01
CRANE: Usted y yo tenemos mucho de qué hablar. Y por fin podemos hacerlo con sinceridad. # id:j12_04_crane_02
-> DONE

=== j12_grabadora_mirar ===
PENSAMIENTO: Cubetas de revelado, fotos colgadas de pinzas… y una grabadora de bobinas. Cables que salen por un agujero de la pared. # id:j12_04_grab_01
PENSAMIENTO: Un panel con nombres. «La Campana. Mercado. Mansiones Victoria, 7.º.» Y mi piso. # esperar:1 # id:j12_04_grab_02
PENSAMIENTO: Mi piso está en ese panel. # id:j12_04_grab_03
-> DONE

=== j12_crane ===
CRANE: Ah, el panel. No se preocupe por eso. La telepantalla no siempre lo oye todo. Yo sí. # id:j12_04_crane_03
CRANE: Pero no se ofenda. Escucho a todo el mundo. Es mi oficio. Igual que el suyo es corregir el pasado. # id:j12_04_crane_04
PENSAMIENTO: Enciende la grabadora. Las bobinas giran. # sfx:chirrido # id:j12_04_pens_02
GRABACIÓN: «¿Estás dispuest{o} a dar tu vida?» # id:j12_04_grab_nell
GRABACIÓN: «{iniciacion_vida}.» # id:j12_04_grab_prot
PENSAMIENTO: Mi voz. # id:j12_04_pens_03
CRANE: Tiene buena voz. Firme. # esperar:0.8 # id:j12_04_crane_05
CRANE: La vieja Hask está en el Minimor desde anoche. No dice nada. Las viejas nunca dicen nada. # id:j12_04_crane_06
CRANE: Barlow ya ha dicho bastante, aunque poco útil. Usted, en cambio, puede decirme mucho. # id:j12_04_crane_07
{
- crane_info >= 3:
    CRANE: Me contó usted, en esta misma silla, que ya no sabía lo que era su hermana. Yo sí lo sabía. Yo lo supe antes que nadie. # id:j12_04_info_3
- crane_info >= 1:
    CRANE: Su hermana cantaba «Naranjas y limones». Me lo dijo usted. No hacía falta: yo la fotografié cantándola. # id:j12_04_info_1
- else:
    CRANE: Es usted una persona muy reservada. Eso me gustó desde el principio. Pero la grabación habla por usted. # id:j12_04_info_0
}
CRANE: Le propongo algo sencillo. Usted me dice quién más. La mujer del mercado, Dot. Su marido. # id:j12_04_oferta_01
{ len_salvado:
    CRANE: Su marido, al que usted tuvo la amabilidad de retirar de la lista. Lo sé. Yo también tengo copias. # id:j12_04_oferta_len
}
CRANE: Y una cosa más. La vieja Hask hablaba de «San Clemente». De «las campanas». Usted sabe dónde está el viejo. O lo sabrá. # id:j12_04_oferta_02
CRANE: Usted me ayuda a encontrarlo y su expediente desaparece. Nadie recordará nunca que usted dudó. Ni siquiera usted. # esperar:0.8 # id:j12_04_oferta_03
CRANE: Eso también se puede arreglar. # id:j12_04_oferta_04
PROTAGONISTA: ¿Y si me niego? # id:j12_04_prot_01
CRANE: Entonces mañana su foto estará en la mesa de Voss. Y Voss tiene mucha prisa por cerrar el expediente de su familia. # esperar:0.8 # id:j12_04_crane_08
CRANE: Lleva cinco años esperándolo. # id:j12_04_crane_09
* [«…¿Qué quiere saber?»] # decision:D-J12-CRANE
    ~ crane_decision = "aceptar"
    ~ fb_variante = "trato"
    -> final_b_trato
* [«Deme un día. Le traeré lo que quiere.»]
    ~ crane_decision = "fingir"
    ~ crane_sigue = true
    CRANE: Un día. Ni una hora más. # id:j12_05f_crane_01
    PENSAMIENTO: Sonríe. No se lo cree del todo. # id:j12_05f_pens_00
    PENSAMIENTO: La calle Cable, de noche, vacía. Demasiado vacía. Al girar la esquina, una sombra con sombrero me sigue a distancia. # fx:negro # id:j12_05f_pens_01
    PENSAMIENTO: Me sigue. Un día, dijo. Me va a seguir el día entero. # id:j12_05f_pens_02 # escena:callejones # pos:inicio
    -> DONE
* [«Usted mató a mi hermana.»]
    ~ crane_decision = "negar"
    PENSAMIENTO: Deja la taza, despacio. # id:j12_05n_pens_00
    CRANE: No. La mató un cohete. Yo solo hice una foto. # id:j12_05n_crane_01
    CRANE: Siempre hago solo una foto. # id:j12_05n_crane_02
    PENSAMIENTO: Saca un silbato del bolsillo del chaleco. Lo hace sonar. Fuera, botas. Gritos. # sfx:alto # musica:persecucion # id:j12_05n_pens_01
    PENSAMIENTO: Corro. # fx:negro # id:j12_05n_pens_02 # escena:callejones # pos:inicio
    -> DONE

// ==================================================================== J12.06 — Limehouse · La persecución
=== callejones ===

= entrar
{ persecucion_vista:
    -> DONE
}
~ persecucion_vista = true
{ crane_decision:
- "negar":
    PENSAMIENTO: Silbatos detrás de mí. Patrullas en la calle. Linternas. # fx:aclarar # id:j12_06_negar
- "fingir":
    PENSAMIENTO: El sombrero, a cincuenta pasos. Hay que despistarle sin que lo parezca. # fx:aclarar # id:j12_06_fingir
- else:
    PENSAMIENTO: Crane aún no ha dado la alarma. Solo una patrulla, haciendo su ronda. # fx:aclarar # id:j12_06_huir
}
PENSAMIENTO: Sábanas tendidas, portales hondos. Los charcos suenan. Al final de estos callejones, una puerta verde. # id:j12_06_pens_00
-> DONE

= visto
{ crane_decision == "fingir":
    CRANE: Buenas noches, camarada. Qué casualidad. # id:j12_06_visto_crane
- else:
    AGENTE: ¡Alto! # id:j12_06_visto_agente
}
PENSAMIENTO: Corro. Doblo dos esquinas. Me escondo hasta que pasan. # id:j12_06_visto_01
~ sube_sospecha_sigilo(25)
PENSAMIENTO: Vuelvo atrás. Otra vez. # id:j12_06_visto_02
-> DONE

= sabana_mirar
PENSAMIENTO: Sábanas tendidas. Detrás, una persona quieta no es más que una sombra. # id:j12_06_sabana
-> DONE

= portal_mirar
PENSAMIENTO: Un portal hondo. Huele a orines y a carbón. # id:j12_06_portal
-> DONE

= charco_mirar
PENSAMIENTO: Un charco. Si lo piso, me oirán. # id:j12_06_charco
-> DONE

= farola_mirar
PENSAMIENTO: Luz de gas. Mejor rodearla. # id:j12_06_farola
-> DONE

= atajo
{ dot_confianza >= 2:
    PENSAMIENTO: Llamo con los nudillos, sin esperanza. La puerta se abre una rendija. # id:j12_06_atajo_01
    VECINA: Corre, corre. Por el patio. # id:j12_06_atajo_02
    ~ atajo_usado = true
    PENSAMIENTO: Un patio, una cocina, otra puerta. Salgo más allá, al otro lado de la tapia. # fx:negro # pos:atajo # id:j12_06_atajo_03
    -> DONE
}
PENSAMIENTO: Llamo. Nadie abre. Detrás de la puerta, alguien contiene la respiración. # id:j12_06_atajo_cerrada
-> DONE

= atajo_vuelta
PENSAMIENTO: Una puerta cerrada. # id:j12_06_atajo_vuelta
-> DONE

= cubo_mirar
PENSAMIENTO: Un cubo de latón. Mejor no tocarlo. # id:j12_06_cubo
-> DONE

= puerta_verde
PENSAMIENTO: Una puerta verde con un once. # id:j12_06_verde_01
PENSAMIENTO: Se abre antes de que llame. # fx:negro # id:j12_06_verde_02 # escena:casa_dot # pos:puerta
-> DONE

// ==================================================================== J12.07 — Casa de Dot
=== casa_dot ===

= entrar
{ final_en_curso == "D":
    -> fd_dot
}
{ casa_dot_vista:
    -> DONE
}
~ casa_dot_vista = true
PENSAMIENTO: Una cocina pequeña y abarrotada. La estufa encendida, ropa secándose. Huele a té y a carbón. # fx:aclarar # id:j12_07_pens_00
PENSAMIENTO: En una repisa, la colección de metralla de Sammy. Intacta. # id:j12_07_pens_01
PENSAMIENTO: Dot cierra la puerta y echa el cerrojo. Me empuja hacia la despensa. # sfx:cerrojo # musica:sigilo # id:j12_07_pens_02
{
- dot_confianza >= 3:
    DOT: Dentro. Ni un ruido. # id:j12_07_dot_3_01
    PENSAMIENTO: Antes de cerrar la despensa, me mira. # id:j12_07_dot_3_02
    DOT: Tú corriste hacia mi niño. # id:j12_07_dot_3_03
    { len_salvado:
        DOT: Y mi Len está vivo en algún sitio. No sé qué hiciste. No me lo digas. # id:j12_07_dot_3_len
    }
    DOT: Dentro. # id:j12_07_dot_3_04
- dot_confianza >= 1:
    DOT: Dentro. # esperar:0.8 # id:j12_07_dot_1_01
    DOT: Lo hago porque me lo pidió Nell. No por ti. # id:j12_07_dot_1_02
- else:
    PENSAMIENTO: Me mira largo, con la mano en el cerrojo. Por un instante parece que va a abrir para entregarme. # esperar:1.2 # id:j12_07_dot_0_01
    DOT: …Dentro. # id:j12_07_dot_0_02
    DOT: Nell me hizo prometerlo. Por Nell. Solo por Nell. # id:j12_07_dot_0_03
}
PENSAMIENTO: Oscuridad. Por las rendijas de la despensa, la luz de la estufa. # fx:negro # id:j12_07_pens_03
PENSAMIENTO: Golpes en la puerta. Voces. Dot abre. # sfx:golpes # id:j12_07_pens_04
{ crane_decision == "fingir":
    CRANE: ¿Ha visto a alguien de azul? # id:j12_07_crane_01
- else:
    AGENTE: ¿Ha visto a alguien de azul? # id:j12_07_agente_01
}
DOT: ¿De azul? Aquí no vienen los de azul. Solo vienen a contar muertos. # esperar:0.8 # id:j12_07_dot_01
DOT: A mi niño ya lo contaron. # id:j12_07_dot_02
{ crane_decision == "fingir":
    PENSAMIENTO: Silencio. Crane mira la cocina con calma. La colección de metralla. # esperar:1.2 # id:j12_07_crane_02
    CRANE: Bonita colección. # esperar:1 # id:j12_07_crane_03
    CRANE: Volveré. # id:j12_07_crane_04
    PENSAMIENTO: Se va. Sabe que estoy aquí. Me deja ir. # id:j12_07_crane_05
    ~ crane_sigue = true
- else:
    PENSAMIENTO: Silencio. Pasos que se alejan. # id:j12_07_pasos
}
-> mensaje

// J12.08 — El mensaje de Nell
= mensaje
PENSAMIENTO: Dot abre la despensa. Me da un vaso de agua. Se sienta frente a mí, a la luz de la estufa. # fx:aclarar # musica:refugio # id:j12_08_pens_00
DOT: Nell vino hace tres noches. Me dejó esto. # id:j12_08_dot_01
DOT: Dijo que si alguna vez venías a mi puerta, era porque ella ya no podía venir a la tuya. # id:j12_08_dot_02
PENSAMIENTO: Un paquete envuelto en tela de flores. # id:j12_08_pens_01
~ inventario += dibujos_amory
PENSAMIENTO: Los dibujos de Amory. Los que Nell sacó de su papelera. # objeto:dibujos_amory # id:j12_08_dibujos_01
PENSAMIENTO: De cerca, no son mapas de Malabar. Son planos de las líneas de metro cerradas bajo Londres. # esperar:1 # id:j12_08_dibujos_02
PENSAMIENTO: Los pájaros de los márgenes marcan pozos de ventilación, salidas, estaciones tapiadas. # id:j12_08_dibujos_03
PENSAMIENTO: Pájaros. «Señales para el enemigo», confesó. # esperar:1 # id:j12_08_dibujos_04
PENSAMIENTO: Eran señales. Pero no para Eurasia. Felix dibujaba la ciudad que había debajo. Para él. Para nadie. Para mí. # id:j12_08_dibujos_05
~ sube_duda(5)
PENSAMIENTO: Y una nota, a lápiz, con letra lenta. # id:j12_08_nota_00
PENSAMIENTO: «Usa lo que sabes.» # documento:nota_nell_j12 # id:j12_08_nota_01
PENSAMIENTO: La Planilla Azul. Sé dónde caerán los cohetes esta semana. # esperar:1 # id:j12_08_nota_02
PENSAMIENTO: Sé dónde no caerán. # id:j12_08_nota_03
~ mensaje_nell = true
PENSAMIENTO: Dot se levanta. Coge un trozo de metralla de la colección de Sammy, el brillante, y me lo pone en la mano. # id:j12_08_metralla_00
DOT: Para que te dé suerte. Él decía que nunca te cae un cohete donde ya tienes uno. # id:j12_08_dot_03
{ inventario ? metralla_brillante:
    PENSAMIENTO: Abro la otra mano. Tengo el otro trozo brillante, el que Sammy recogía en el mercado. # id:j12_08_metralla_01
    PENSAMIENTO: Lo mira. Se le quiebra la voz por primera vez. # id:j12_08_metralla_02
    DOT: …Ese era el que más quería. # esperar:1 # id:j12_08_dot_04
    DOT: Llévatelos. # id:j12_08_dot_05
    PENSAMIENTO: Me cierra la mano sobre los dos. # id:j12_08_metralla_03
- else:
    ~ inventario += metralla_brillante
    PENSAMIENTO: Parece plata. # objeto:metralla_brillante # id:j12_08_metralla_04
}
DOT: Al amanecer, el metro de Shadwell está sin vigilancia. Lo cerraron «por reformas». # id:j12_08_dot_06
PENSAMIENTO: Escupe a un lado. # id:j12_08_pens_02
DOT: Nunca reforman nada. # id:j12_08_dot_07
~ diario_dot = true
-> cierre

// Cierre del acto: la despensa, de madrugada
= cierre
PENSAMIENTO: Madrugada. En la despensa, sin dormir. La luz de la estufa entra por la rendija. # fx:negro # id:j12_08_cierre_00
{ inventario ? diario and not diario_confiscado:
    -> escribir
}
-> reloj

= escribir
PENSAMIENTO: El cuaderno, en las rodillas. # fx:aclarar # id:j12_08_diario_00
* [Escribir.]
    ~ temp antes = diario_entradas
    PENSAMIENTO: Cierro el cuaderno. # minijuego:diario,fecha=8 de mayo # id:j12_08_diario_01
    { diario_entradas > antes:
        ~ diario_escrito_hoy = jornada
        PENSAMIENTO: 1984. Ya no me importa si es verdad. # id:j12_08_diario_anio
    }
* [Solo tenerlo en las manos.]
    PENSAMIENTO: No escribo nada. Lo sostengo. # id:j12_08_diario_no
- -> reloj

= reloj
{ dp_j11_ivy == "aceptar":
    PENSAMIENTO: Mañana, bajo las campanas. # id:j12_08_aceptar_01
    PENSAMIENTO: Saco el reloj de Ivy. Nueve y cuarenta. Lo guardo. # esperar:1 # id:j12_08_aceptar_02
    PENSAMIENTO: No sé por qué voy. Ya no sé nada. Solo que no puedo volver. # id:j12_08_aceptar_03
- else:
    PENSAMIENTO: Mañana, bajo las campanas. # id:j12_08_recordar_01
    PENSAMIENTO: Saco el reloj de Ivy. Nunca le di cuerda. # esperar:1.4 # id:j12_08_recordar_02
    ~ reloj_en_marcha = true
    PENSAMIENTO: Le doy cuerda. # sfx:tic # id:j12_08_recordar_03
    PENSAMIENTO: Tic. # sfx:tic # esperar:0.6 # id:j12_08_recordar_04
    PENSAMIENTO: Tic. Tic. # sfx:tic # esperar:0.6 # id:j12_08_recordar_05
    PENSAMIENTO: El reloj anda. # sfx:tic # id:j12_08_recordar_06
}
CARTEL: FIN DEL ACTO III # fx:negro # musica:silencio # id:j12_08_fin_acto
~ nueva_jornada(13)
CARTEL: ACTO IV¶CAPÍTULO II # id:j12_08_acto4
CARTEL: JORNADA 13 # id:j12_08_jornada13
CARTEL: Bajo las campanas. # id:j12_08_bajo
-> j13_entrada

= despensa_mirar
PENSAMIENTO: La despensa. Una puerta con rendijas. # id:j12_07_despensa
-> DONE

= metralla_mirar
PENSAMIENTO: La colección de Sammy. Ochenta y cuatro trozos. Cada uno, con su cordel. # id:j12_07_metralla_mirar
-> DONE

= estufa_mirar
PENSAMIENTO: La estufa encendida. Lo único caliente de todo Londres. # id:j12_07_estufa
-> DONE

= dot_mirar
PENSAMIENTO: Dot. Seca, rápida. Las manos le tiemblan solo cuando no las usa. # id:j12_07_dot_mirar
-> DONE
