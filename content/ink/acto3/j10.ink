// ACTO III · JORNADA 10 — Semana del Odio (guion: docs/guion-detallado/03-acto-3.md)
// La confesión de Amory, el mitin en el que Eurasia se convierte en Estasia, la Gran Rectificación
// (con la misión de Nell dentro) y la detención de Parsons.

// ==================================================================== J10.01 — Las Mansiones Victoria · Mañana
=== j10_piso ===
{ hilda_j10:
    -> DONE
}
PENSAMIENTO: La telepantalla toca marchas desde las seis. Hoy empieza la Semana del Odio. # id:j10_01_pens_00
-> DONE

=== j10_escalera ===
{ rectificacion_hecha:
    -> j10_parsons
}
{ hilda_j10:
    -> DONE
}
~ hilda_j10 = true
PENSAMIENTO: La escalera, cubierta de banderines. Un soldado euroasiático gigantesco avanza hacia mí desde cada rellano. Y el cartel de Ivy, por todas partes. # id:j10_01_pens_01
PENSAMIENTO: Hilda lleva una diadema de cartón con la cara del Gran Hermano. # id:j10_01_pens_02
HILDA: ¡{nombre}! ¡Hoy es el gran día! Mitin en la plaza de la Victoria a las doce. ¡Y esta noche quemamos la efigie de Goldstein! # id:j10_01_hilda_01
HILDA: ¿Te has enterado? Syme, el del Miniver, el del diccionario… ya no viene a los ensayos. # esperar:0.8 # id:j10_01_hilda_02
HILDA: Será que lo han trasladado. # id:j10_01_hilda_03
PENSAMIENTO: Trasladado. # id:j10_01_pens_03
{ hilda_aprecio <= 0:
    HILDA: Por cierto. El Subdirector Voss es un hombre encantador. # id:j10_01_hilda_04
    HILDA: Me pidió que le avisara de cualquier… cosa. Por lo de la Semana del Odio. Por seguridad. # id:j10_01_hilda_05
    ~ sube_sospecha(5)
    PENSAMIENTO: Voss. Hilda habla con Voss. # id:j10_01_pens_04
}
-> DONE

=== j10_hilda_otra ===
HILDA: ¡A las doce, {nombre}! ¡En primera fila! # id:j10_01_hilda_otra
-> DONE

=== j10_bajar ===
CARTEL: Cantina del Minipax. Antes del mitin. # fx:negro # id:j10_02_cartel # escena:cantina # pos:puerta
-> DONE

// ==================================================================== J10.02 — Cantina del Minipax · La confesión de Amory
=== j10_cantina ===
{ cantina_j10:
    -> DONE
}
~ cantina_j10 = true
PENSAMIENTO: Toda la cantina mira la telepantalla grande. El ambiente es eléctrico. # id:j10_02_pens_00
TELEPANTALLA: …y a continuación, la confesión del traidor, que ha pedido voluntariamente hablar a su pueblo antes de recibir su justo castigo. # id:j10_02_tp_01
PENSAMIENTO: Amory. Irreconocible: delgadísimo, sin gafas, la cara hinchada, el pelo rapado. Huecos donde había dientes. # id:j10_02_pens_01
AMORY: Yo, Felix Amory, confieso haber trabajado al servicio de Eurasia desde mil novecientos setenta y seis. # id:j10_02_amory_01
AMORY: Confieso haber saboteado los mapas del frente de Malabar. Confieso haber dibujado señales para el enemigo en los márgenes de documentos oficiales. # id:j10_02_amory_02
AMORY: Pájaros. Dibujé pájaros. Eran señales. # esperar:1 # id:j10_02_amory_03
AMORY: Amo al Gran Hermano. Merezco morir. Pido morir. # id:j10_02_amory_04
{ amory_reaccion == "denuncia":
    PENSAMIENTO: La cantina abuchea. Alguien tira un trozo de pan a la pantalla. # cf:id=CF-J10-AMORY,bpm=132 # id:j10_02_pens_02
- else:
    PENSAMIENTO: La cantina abuchea. Alguien tira un trozo de pan a la pantalla. # cf:id=CF-J10-AMORY # id:j10_02_pens_02b
}
{ cf_j10_amory == "fallo":
    ~ sube_sospecha(10)
    PENSAMIENTO: Alguien me ha mirado. No sé quién. # id:j10_02_fallo
}
PENSAMIENTO: En la mesa de al lado, Pell come sin levantar la vista. # id:j10_02_pens_03
PELL: Traidor. Menos mal que lo cogieron. # id:j10_02_pell_01
PELL: ¿Usted lo conocía? # id:j10_02_pell_02
* [«Nunca le había visto.»] # decision:D-J10-PELL
    ~ pell_j10 = "negacion"
    PELL: Ni yo. # id:j10_02_pell_03
* [«Se sentaba en su silla.»]
    ~ pell_j10 = "verdad"
    PENSAMIENTO: Deja de masticar. Me mira con algo parecido al miedo. # id:j10_02_pens_04
    PELL: …Mi silla siempre ha sido mía. # id:j10_02_pell_04
    ~ sube_sospecha(5)
- ~ diario_amory_confesion = true
-> j10_mitin

// ==================================================================== J10.03 — Plaza de la Victoria · El mitin
=== j10_mitin ===
CARTEL: Plaza de la Victoria. Las doce. # fx:negro # id:j10_03_cartel
PENSAMIENTO: La plaza, abarrotada. Banderas, efigies de Goldstein, helicópteros. Estoy entre la multitud, junto a Hilda y los Parsons. # vineta:vineta-plaza # fx:aclarar # id:j10_03_pens_00
{ pancarta_j2 != "":
    PENSAMIENTO: Entre las pancartas de ¡MUERTE A EURASIA!, la mía. La que pinté en el Centro. # id:j10_03_pancarta
}
ORADOR: …¡las hordas euroasiáticas, que bombardean a nuestros niños en los mercados…! # id:j10_03_orador_01
PENSAMIENTO: «Bombardean a nuestros niños en los mercados.» Batería siete. Hythe. Kent. # id:j10_03_pens_01
PENSAMIENTO: La multitud ruge. # cf:id=CF-J10-MITIN # id:j10_03_pens_02
{ cf_j10_mitin == "fallo":
    ~ sube_sospecha(10)
}
{ cf_j10_mitin_bh > 0:
    ~ sube_sospecha(10)
    PENSAMIENTO: He tocado la del Gran Hermano. Un hombre de la fila de atrás lo ha visto. # id:j10_03_bh
}
~ sube_duda(10)
~ diario_estasia = true
PENSAMIENTO: La multitud arranca sus propias pancartas. Hilda arranca la mía. Los niños Parsons pisotean un soldado euroasiático. # id:j10_03_pens_03
PENSAMIENTO: Estasia. Siempre fue Estasia. # id:j10_03_pens_04
PENSAMIENTO: Hilda, sudorosa, me abraza. # id:j10_03_pens_05
HILDA: ¡Qué emoción! ¡Estasia! # id:j10_03_hilda_01
HILDA: ¡Siempre lo supe! # id:j10_03_hilda_02
CARTEL: Esa noche. Departamento de Partes y Cartografía. # vineta:fin # id:j10_04_cartel # escena:departamento_noche # pos:puerta
-> DONE

// ==================================================================== J10.04 — La Gran Rectificación
=== j10_depto ===

= entrar
{ rectificacion_1 != "":
    -> DONE
}
PENSAMIENTO: Toda la plantilla, convocada. Nadie dormirá en cuarenta y ocho horas. # id:j10_04_pens_00
PENSAMIENTO: Voss, en mangas de camisa por primera vez, de pie en el centro de la sala. # id:j10_04_pens_01
VOSS: Camaradas. Durante los últimos cuatro años, en todos los documentos de este ministerio, Oceanía ha estado en guerra con Estasia. # esperar:1 # id:j10_04_voss_01
VOSS: Los documentos que digan otra cosa contienen errores. # id:j10_04_voss_02
{ duda >= 60:
    VOSS: Corríjanlos. # minijuego:rectificacion,fase=1,duda=alta,resultado=rectificacion_1 # id:j10_04_voss_03
- else:
    VOSS: Corríjanlos. # minijuego:rectificacion,fase=1,duda=media,resultado=rectificacion_1 # id:j10_04_voss_03b
}
{ rectificacion_1 == "incompleta":
    ~ sube_sospecha(5)
    VOSS: Más deprisa, camarada {apellido}. Estasia no espera. # id:j10_04_voss_lento
}
PENSAMIENTO: Pasada la medianoche, la limpiadora entra con su carrito. Recoge papeleras. # id:j10_04_pens_02
PENSAMIENTO: Al pasar junto a mi mesa deja caer un trapo. Bajo el trapo, una nota. # sfx:papel # id:j10_04_pens_03
~ nota_nell_j10 = true
PENSAMIENTO: Deja el carrito aparcado al fondo de la sala y sigue con las papeleras. # documento:nota_nell_j10 # refrescar # id:j10_04_pens_04
PENSAMIENTO: Un mapa sin corregir. Un parte sin rectificar. Y Voss dando vueltas por la sala. # reloj:inicio=02:40:00,limite=300,agotar=j10_depto.tarde # id:j10_04_pens_05
-> DONE

= mesa
{ mision_j10 != "" or not nota_nell_j10:
    PENSAMIENTO: Mi mesa. Mapas de Estasia, banderitas amarillas. # id:j10_04_mesa
    -> DONE
}
{ inventario ? mapa_malabar:
    PENSAMIENTO: Ya tengo el mapa. # id:j10_04_mesa_ya
    -> DONE
}
~ inventario += mapa_malabar
~ cargando_prueba = true
PENSAMIENTO: Debajo de la pila, un mapa de Malabar sin corregir. Banderitas negras. Lo doblo. # objeto:mapa_malabar # id:j10_04_mesa_coger
-> DONE

= archivador
{ mision_j10 != "" or not nota_nell_j10:
    PENSAMIENTO: El archivador del personal. # id:j10_04_archivador
    -> DONE
}
{ inventario ? parte_original:
    PENSAMIENTO: Ya tengo el parte. # id:j10_04_archivador_ya
    -> DONE
}
~ inventario += parte_original
~ cargando_prueba = true
PENSAMIENTO: El cajón de abajo, el de lo que aún no se ha rectificado. Un parte de abril, con sello: «las fuerzas euroasiáticas…». # objeto:parte_original # id:j10_04_archivador_coger
-> DONE

= carrito_mirar
PENSAMIENTO: El carrito de la limpieza. El doble fondo está bajo el cubo. # id:j10_04_carrito_mirar
-> DONE

= carrito
{ mision_j10 != "":
    PENSAMIENTO: El carrito ya no es asunto mío. # id:j10_04_carrito_hecho
    -> DONE
}
{ inventario ? mapa_malabar and inventario ? parte_original:
    -> entregar
}
{ inventario ? mapa_malabar or inventario ? parte_original:
    PENSAMIENTO: Falta {inventario ? mapa_malabar:el parte sin rectificar|el mapa sin corregir}. # id:j10_04_carrito_falta
- else:
    PENSAMIENTO: Un mapa sin corregir. Un parte sin rectificar. Primero tengo que tenerlos. # id:j10_04_carrito_nada
}
-> DONE

= entregar
~ inventario -= mapa_malabar
~ inventario -= parte_original
~ cargando_prueba = false
~ mision_j10 = "hecha"
~ prueba_rectificacion = true
PENSAMIENTO: Levanto el cubo. El doble fondo. El mapa y el parte, dentro. El cubo, en su sitio. # sfx:papel # reloj:parar # id:j10_04_entregar_01
PENSAMIENTO: Al rato, la limpiadora vuelve a por su carro. Al recogerlo, toca el borde dos veces. # esperar:1.2 # id:j10_04_entregar_02
PENSAMIENTO: Recibido. # id:j10_04_entregar_03
-> fase2

// Voss le ve con la prueba encima (la primera vez, Brooke tira una pila de carpetas)
= visto
{ not brooke_distrae:
    ~ brooke_distrae = true
    PENSAMIENTO: Voss se gira hacia mí. # id:j10_04_visto_00
    PENSAMIENTO: Al otro lado de la sala, una pila de carpetas cae al suelo. # sfx:golpes # seguir # id:j10_04_brooke_00
    VOSS: ¡Cuidado, camarada! # id:j10_04_brooke_voss
    BROOKE: Perdone, Subdirector. El cansancio. # id:j10_04_brooke_01
    PENSAMIENTO: Brooke recoge las carpetas sin mirarme. # id:j10_04_brooke_02
    -> DONE
}
VOSS: ¿Qué hace con ese mapa, camarada? # id:j10_04_visto_01
PROTAGONISTA: Lo llevaba al agujero de la memoria. # id:j10_04_visto_02
VOSS: El agujero está aquí. # esperar:0.8 # id:j10_04_visto_03
VOSS: Úselo. # id:j10_04_visto_04
PENSAMIENTO: Lo tiro al agujero delante de él. Una corriente de aire caliente se lo lleva. # sfx:tubo # reloj:parar # id:j10_04_visto_05
~ inventario -= mapa_malabar
~ inventario -= parte_original
~ cargando_prueba = false
~ mision_j10 = "fallida"
~ sube_sospecha_sigilo(20)
PENSAMIENTO: Voss sigue su ronda. No ha anotado nada. No le hace falta. # id:j10_04_visto_06
-> fase2

// Dan las tres sin haber llegado al carro
= tarde
PENSAMIENTO: Las tres. La limpiadora se lleva el carrito sin mirar atrás. # reloj:parar # id:j10_04_tarde_01
{ cargando_prueba:
    PENSAMIENTO: Vuelvo a dejar lo que había apartado donde estaba. Nadie lo ha visto. # id:j10_04_tarde_02
}
~ inventario -= mapa_malabar
~ inventario -= parte_original
~ cargando_prueba = false
~ mision_j10 = "tarde"
-> fase2

// Segunda mitad: el Libro de Registro
= fase2
PENSAMIENTO: El Libro de Registro. «Impactos euroasiáticos.» En cada página. # id:j10_04_fase2_00
{ duda >= 60:
    PENSAMIENTO: Tacho. Escribo. Tacho. # minijuego:rectificacion,fase=2,duda=alta,resultado=rectificacion_2 # id:j10_04_fase2_01
- else:
    PENSAMIENTO: Tacho. Escribo. Tacho. # minijuego:rectificacion,fase=2,duda=media,resultado=rectificacion_2 # id:j10_04_fase2_01b
}
{ rectificacion_2 == "incompleta":
    ~ sube_sospecha(5)
}
-> fragmento

// J10.05 — Madrugada · Fragmento III
= fragmento
PENSAMIENTO: Las cuatro. La sala, casi vacía. Me quedo dormid{o} sobre la mesa. # fx:negro # id:j10_05_pens_00
PENSAMIENTO: Al despertar, entre mis papeles, unas hojas mecanografiadas cosidas con hilo. Bajo un mapa nuevo de Estasia. # fx:aclarar # id:j10_05_pens_01
PENSAMIENTO: «Sabe que está mintiendo.» # minijuego:libro,fragmento=3 # id:j10_05_pens_02
~ libro_fragmentos = 3
~ diario_libro_doblepensar = true
~ rectificacion_hecha = true
{ not (inventario ? libro):
    ~ inventario += libro
}
PENSAMIENTO: Me miro las manos, manchadas de tinta hasta la muñeca. # id:j10_05_pens_03
PENSAMIENTO: Sí. # id:j10_05_pens_04
CARTEL: La noche siguiente. Cuarenta y ocho horas sin dormir. # fx:negro # id:j10_06_cartel # escena:escalera # pos:abajo
-> DONE

= salir
PENSAMIENTO: Nadie sale de aquí hasta que el pasado esté corregido. # id:j10_04_salir
-> DONE

= voss_mirar
PENSAMIENTO: Voss, en mangas de camisa. Los guantes, puestos. Da vueltas a la sala sin prisa. # id:j10_04_voss_mirar
-> DONE

= mapa_mirar
PENSAMIENTO: El corcho de Malabar. Cientos de agujeros vacíos. # id:j10_04_mapa_mirar
-> DONE

= memoria_mirar
PENSAMIENTO: El agujero de la memoria no da abasto. Huele a papel quemado. # id:j10_04_memoria_mirar
-> DONE

= companeros_mirar
PENSAMIENTO: Pell y Brooke, tachando. Nadie habla. # id:j10_04_companeros
-> DONE

// ==================================================================== J10.06 — Las Mansiones Victoria · Parsons
=== j10_parsons ===
{ parsons_detenido:
    -> DONE
}
~ parsons_detenido = true
PENSAMIENTO: En la escalera hay gente. La puerta de los Parsons, abierta. # refrescar # id:j10_06_pens_00
PENSAMIENTO: Dos hombres de uniforme negro sacan a Parsons, que llora. # id:j10_06_pens_01
PARSONS: ¡Camarada {apellido}! ¡Ha sido mi hija! ¡Mi pequeña! ¡Me oyó hablar en sueños! ¡Dicen que dije…! # id:j10_06_parsons_01
PENSAMIENTO: Le tapan la boca. # id:j10_06_pens_02
PARSONS: ¡Estoy orgulloso de ella! ¡Estoy orgulloso…! # id:j10_06_parsons_02
PENSAMIENTO: Se lo llevan. En el rellano, la hija de Parsons, con el pañuelo rojo de los Espías. Hilda le acaricia el pelo. # id:j10_06_pens_03
HILDA: Qué niña tan valiente. Tan valiente. # id:j10_06_hilda_01
HILDA: Le van a dar una mención. # id:j10_06_hilda_02
PENSAMIENTO: La hija de Parsons me mira. Muy fijamente. # esperar:1.2 # id:j10_06_pens_04
HIJA PARSONS: Usted también dice un nombre por las noches. # esperar:1 # id:j10_06_hija_01
HIJA PARSONS: Ahora dice dos. # id:j10_06_hija_02
~ sube_sospecha(5)
PENSAMIENTO: Dos. Ivy. Y… # esperar:1 # id:j10_06_pens_05
PENSAMIENTO: ¿Sammy? ¿Amory? ¿Nell? # id:j10_06_pens_06
PENSAMIENTO: Cierro la puerta con llave. # fx:negro # id:j10_06_pens_07 # escena:piso_noche # pos:puerta
-> DONE

// ==================================================================== El piso · Noche
=== j10_noche ===
{ noche_j10_vista:
    -> DONE
}
~ noche_j10_vista = true
PENSAMIENTO: «Ahora dice dos.» # id:j10_06_noche_00
-> DONE

=== j10_dormir ===
~ nueva_jornada(11)
~ desayunado = false
CARTEL: JORNADA 11 # fx:negro # sfx:silbato # id:j10_06_jornada11
CARTEL: El Ministerio del Amor. # id:j10_06_fin # escena:piso # pos:cama
-> DONE
