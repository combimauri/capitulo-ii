// SOSPECHA 100 (guion: docs/guion-detallado/05-finales.md)
// El motor lanza «arresto» cuando la Sospecha llega a 100 al terminar un diálogo.
// Acto I: Final C0 (vaporización). Desde la Jornada 4: Final C, que empieza con el arresto donde esté
// el protagonista (FC.01). La celda, O'Brien y la Habitación 101 llegan con el Acto IV.

=== arresto ===
{ jornada <= 3:
    -> final_c0
}
{
- escena_actual == "piso" or escena_actual == "piso_noche":
    -> en_casa
- escena_actual == "departamento" or escena_actual == "departamento_noche" or escena_actual == "pasillo" or escena_actual == "cantina" or escena_actual == "archivo" or escena_actual == "despacho_voss" or escena_actual == "suministros" or escena_actual == "vestibulo":
    -> en_el_minipax
- else:
    -> en_la_calle
}

// FC.01 — El arresto, en el piso
= en_casa
PENSAMIENTO: Noche. Tres golpes en la puerta. # sfx:golpes # fx:negro # id:fc_01_casa_00
PENSAMIENTO: La telepantalla cambia de voz. # fx:aclarar # id:fc_01_casa_01
TELEPANTALLA: {num} {apellido}. Quédese donde está. No se mueva. # id:fc_01_casa_tp
{ diario_escondite == "cartel" and not cartel_arrancado:
    PENSAMIENTO: Un hombre de negro arranca el cartel de Ivy de un tirón. El cuaderno cae al suelo. # sfx:papel # id:fc_01_casa_cartel_01
    PENSAMIENTO: La cara de Ivy queda boca abajo. # id:fc_01_casa_cartel_02
}
-> furgoneta

// FC.01 — El arresto, en el ministerio
= en_el_minipax
PENSAMIENTO: Voss sale de su despacho con dos guardias. # id:fc_01_minipax_00
VOSS: Camarada {apellido}. Acompáñeles. # id:fc_01_minipax_voss
PENSAMIENTO: Pell, Brooke y toda la sala siguen tecleando sin levantar la vista. # id:fc_01_minipax_01
-> furgoneta

// FC.01 — El arresto, en el barrio prole o en mitad de una misión
= en_la_calle
PENSAMIENTO: Un silbato. Linternas. # sfx:alto # id:fc_01_calle_00
PENSAMIENTO: Un golpe de porra en la nuca. # fx:destello # id:fc_01_calle_01
-> furgoneta

= furgoneta
PENSAMIENTO: Negro. # fx:negro # id:fc_01_negro
PENSAMIENTO: El sonido de una furgoneta. Una puerta metálica. # sfx:sello # esperar:1.5 # id:fc_01_puerta
CARTEL: Ministerio del Amor. # id:fc_01_cartel
CARTEL: FINAL C · HABITACIÓN 101¶Continuará en el Acto IV. # id:fc_01_continuara # final:demo
-> DONE

// ==================================================================== FINAL C0 — Vaporización (Sospecha 100 en el Acto I)
=== final_c0 ===
PENSAMIENTO: Noche. Duermo. # fx:negro # id:fc0_00
PENSAMIENTO: Tres golpes en la puerta. Antes de que me levante, la puerta se abre. Linternas. Siluetas negras. # sfx:golpes # id:fc0_01
PENSAMIENTO: … # esperar:2 # id:fc0_02
PENSAMIENTO: Una mano enguantada pasa un rodillo de tinta negra sobre la ficha: el nombre, el número, la foto, la firma. # documento:ficha_c0 # id:fc0_03
CARTEL: No hay registro de ningún afiliado con ese número. # id:fc0_04 # final:C0
-> DONE
