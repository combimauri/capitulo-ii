// FINAL D — «Capítulo II» (guion: docs/guion-detallado/05-finales.md)
// El libro sale de la cripta y llega a la caja de metralla de Sammy. Después, el Minimor en versión abreviada:
// aguantar veinticuatro horas. El café. Y una nota, años más tarde, sobre el texto conocido como «Capítulo II».

=== final_d ===
~ final_en_curso = "D"
// FD.01 — Regreso por los túneles
{ crane_humillado:
    PENSAMIENTO: Crane camina detrás de mí por los túneles, en silencio, con la pistola enfundada. # vineta:loc-tunel_carteles # id:fd_01_escoltado
- else:
    PENSAMIENTO: Los túneles otra vez, al revés. Con el libro contra el pecho. # vineta:loc-tunel_carteles # id:fd_01_pens_00
}
PENSAMIENTO: El taller. La pared de los nombres. En el suelo, un trozo de tiza. # vineta:loc-anden_taller # id:fd_01_pens_01
* [Escribir mi nombre debajo del de Ivy.] # decision:D-FD-TIZA
    ~ fd_nombre_tiza = true
    PENSAMIENTO: {nombre}. Junto a ella. # sfx:plumilla # id:fd_01_tiza
    { crane_humillado:
        CRANE: Qué sentimental. # id:fd_01_crane
    }
* [Seguir.]
    PENSAMIENTO: Sigo. # id:fd_01_seguir
- PENSAMIENTO: Amanecer. La boca de metro de Shadwell. # vineta:loc-shadwell # id:fd_01_amanecer
PENSAMIENTO: Limehouse. Una puerta verde con un once. # vineta:fin # id:fd_01_verde # escena:casa_dot # pos:puerta
-> DONE

// FD.02 — La puerta verde
=== fd_dot ===
{ fd_dot_vista:
    -> DONE
}
~ fd_dot_vista = true
PENSAMIENTO: Llamo tres veces. Canto muy bajo: «Naranjas y limones…» # sfx:golpes # fx:aclarar # id:fd_02_pens_00
PENSAMIENTO: Dot abre. # id:fd_02_pens_01
{ len_salvado:
    PENSAMIENTO: Detrás de ella, en la cocina, sentado a la mesa, Len Pike. Más delgado, con una venda en la cabeza y el ancla en el cuello. # id:fd_02_len_00
    PENSAMIENTO: Se levanta. No sabe quién soy. Dot se lo dice al oído. Me mira largo y me tiende una mano enorme de estibador. # id:fd_02_len_01
    LEN: Había un chico en mi lugar. # esperar:1 # id:fd_02_len_02
    LEN: Dot me lo ha contado. # esperar:1 # id:fd_02_len_03
    LEN: No sé si darle las gracias. # id:fd_02_len_04
    PROTAGONISTA: No me las dé. # id:fd_02_prot_00
}
PENSAMIENTO: Saco el libro de debajo del mono y lo pongo sobre la mesa de la cocina, junto a la colección de metralla de Sammy. # id:fd_02_pens_02
PROTAGONISTA: Es el libro. Entero. # esperar:0.8 # id:fd_02_prot_01
PROTAGONISTA: Hay un capítulo que es… mío. Y de mi hermana. # id:fd_02_prot_02
DOT: Yo no sé leer muy bien. # id:fd_02_dot_01
PROTAGONISTA: Alguien de por aquí sabrá. # id:fd_02_prot_03
PENSAMIENTO: Asiente despacio. # id:fd_02_pens_03
DOT: Billy Hogan. El de los cuarenta trozos. Va a la escuela del Partido. # esperar:0.8 # id:fd_02_dot_02
DOT: Lee de maravilla. # id:fd_02_dot_03
{ crane_humillado:
    PENSAMIENTO: Crane espera en la calle, fumando, apoyado en la farola. La puerta está abierta. Mira hacia dentro de vez en cuando. # id:fd_02_crane_00
    PENSAMIENTO: Dot vacía la caja de metralla sobre la mesa. # cf:id=CF-FD-DOT,expr=neutral,dif=dificil,golpes=12 # id:fd_02_crane_cf
    { cf_fd_dot == "fallo":
        PENSAMIENTO: Crane entra. Dot ya ha cerrado la caja. # id:fd_02_crane_entra
        CRANE: Bonita colección. # id:fd_02_crane_01
        PENSAMIENTO: No la toca. Sale. # id:fd_02_crane_sale
    }
- else:
    PENSAMIENTO: Dot coge el libro y vacía la caja de metralla de Sammy sobre la mesa. # id:fd_02_pens_04
}
PENSAMIENTO: Mete el libro en el fondo de la caja. Vuelve a poner la metralla encima, trozo a trozo, en el mismo orden. # id:fd_02_pens_05
DOT: Aquí no lo buscará nadie. Nadie busca en las cosas de un niño muerto. # id:fd_02_dot_04
~ inventario -= libro
{ reloj_en_marcha and inventario ? reloj_ivy:
    PENSAMIENTO: Me quito el reloj de Ivy. Sigue andando. Se lo doy. # sfx:tic # id:fd_02_reloj_00
    PROTAGONISTA: Que no se pare. # id:fd_02_reloj_01
    PENSAMIENTO: Se lo pone en la muñeca. # id:fd_02_reloj_02
    DOT: Le daré cuerda cada mañana. # id:fd_02_reloj_03
    ~ inventario -= reloj_ivy
}
// FD.03 — Las últimas horas
PENSAMIENTO: Salgo. No huyo. Limehouse por la mañana: el mercado reconstruido a medias, los niños, la ropa tendida, alguien que canta. # vineta:vineta-limehouse_manana # fx:negro # id:fd_03_pens_00
PENSAMIENTO: Podría correr. # fx:aclarar # esperar:1 # id:fd_03_pens_01
PENSAMIENTO: ¿Adónde? # esperar:1 # id:fd_03_pens_02
PENSAMIENTO: Me cogerán hoy o dentro de un mes. Prefiero hoy. Hoy todavía sé quién soy. # vineta:fin # id:fd_03_pens_03 # escena:escalera # pos:abajo
-> DONE

=== fd_escalera ===
{ fd_escalera_vista:
    -> DONE
}
~ fd_escalera_vista = true
PENSAMIENTO: Las Mansiones Victoria. Hilda, en el rellano, con una pancarta nueva. # id:fd_03_hilda_00
PENSAMIENTO: Me mira con los ojos muy abiertos. Entra en su piso dando un portazo. # sfx:sello # id:fd_03_hilda_01
PENSAMIENTO: Se la oye descolgar un teléfono. # id:fd_03_hilda_02 # escena:piso # pos:puerta
-> DONE

=== fd_piso ===
{ fd_piso_visto:
    -> DONE
}
~ fd_piso_visto = true
{ cartel_arrancado:
    PENSAMIENTO: El piso. La mancha clara en la pared. La telepantalla. # id:fd_03_piso_mancha
- else:
    PENSAMIENTO: El piso. El cartel de Ivy. La telepantalla. # id:fd_03_piso
}
-> DONE

=== fd_cartel ===
{ fd_foto_pegada:
    PENSAMIENTO: Ivy sonríe. # id:fd_03_cartel_ya
    -> DONE
}
PENSAMIENTO: Me pongo de pie delante, dentro del cono de la telepantalla. A plena vista. # id:fd_03_cartel_00
{ inventario ? foto_ivy_restaurada:
    ~ fd_foto_pegada = true
    PENSAMIENTO: Saco la foto restaurada y la pego con saliva sobre la cara del cartel. Ivy sonriendo, con el diente mellado, sobre la Ivy del Partido. # id:fd_03_cartel_01
    TELEPANTALLA: {num} {apellido}. Los símbolos del Partido no se modifican. # id:fd_03_cartel_tp
    PENSAMIENTO: Ya lo sé. # id:fd_03_cartel_02
- else:
    PENSAMIENTO: La miro. Me miran. Ya da igual. # id:fd_03_cartel_03
}
-> DONE

=== fd_silla ===
PENSAMIENTO: Me siento frente a la telepantalla. Espero. # id:fd_03_silla_00
PENSAMIENTO: Pasos en la escalera. Muchos. Botas. # sfx:golpes # esperar:1.5 # id:fd_03_silla_01
PENSAMIENTO: Veinticuatro horas, dijo Nell. Es todo lo que me pidió. # id:fd_03_silla_02
PENSAMIENTO: Negro. # fx:negro # id:fd_03_negro
-> final_c.llegada

// FD.04 — El Minimor (versión abreviada)
=== fd_celda ===
{ celda_vista:
    -> DONE
}
~ celda_vista = true
PENSAMIENTO: La celda blanca. Winston está aquí. Parsons ya no. # fx:aclarar # id:fd_04_pens_00
-> DONE

=== fd_winston ===
WINSTON: ¿Ha hecho algo que valiera la pena? # id:fd_04_winston_01
PROTAGONISTA: Creo que sí. # id:fd_04_prot_01
PENSAMIENTO: Me mira con una envidia que no esconde. # id:fd_04_pens_01
WINSTON: Yo creí que sí. Ahora no me acuerdo de qué era. # id:fd_04_winston_02
PENSAMIENTO: La puerta se abre. # sfx:sello # id:fd_04_pens_02 # escena:sala_obrien # pos:camilla
-> DONE

=== fd_obrien ===
{ obrien_visto:
    -> DONE
}
~ obrien_visto = true
PENSAMIENTO: La sala blanca. La camilla. El dial. O'Brien. # fx:aclarar # id:fd_04_pens_03
O'BRIEN: Hay una segunda copia del libro. Con un capítulo nuevo. # id:fd_04_obrien_01
PENSAMIENTO: Sonríe. # id:fd_04_pens_04
O'BRIEN: Lo sabemos porque usted no lo tenía encima, y porque el señor Goldstein siempre hace dos. # esperar:1 # id:fd_04_obrien_02
O'BRIEN: ¿Dónde está? # minijuego:resistencia,resultado=resistencia_d # id:fd_04_obrien_03
{ resistencia_d == "aguanto":
    ~ aguanto_24h = true
    PENSAMIENTO: El reloj de pared marca la hora. # id:fd_04_aguanto_00
    PENSAMIENTO: O'Brien mira el reloj. Luego me mira a mí, con algo parecido al respeto. # id:fd_04_aguanto_01
    O'BRIEN: Veinticuatro horas. Como le pidió la señora Hask. # esperar:1 # id:fd_04_aguanto_02
    O'BRIEN: Es usted muy disciplinad{o}. Le servirá cuando sea uno de los nuestros. # id:fd_04_aguanto_03
- else:
    ~ libro_delatado = true
    PENSAMIENTO: Dot. # id:fd_04_delatado_00
    O'BRIEN: Gracias. # id:fd_04_delatado_01
}
O'BRIEN: En realidad no importa. # esperar:1 # id:fd_04_obrien_04
O'BRIEN: Leerán su capítulo. Lo copiarán. Se lo aprenderán de memoria. # esperar:1 # id:fd_04_obrien_05
O'BRIEN: Y dentro de diez años diremos que lo escribimos nosotros. Y será verdad. # id:fd_04_obrien_06
// FD.05 — Habitación 101 (abreviada)
PENSAMIENTO: El techo bajo. El hueco. La tolva. # vineta:vineta-habitacion101 # id:fd_05_pens_00
O'BRIEN: Su hermana estuvo once minutos debajo. # vineta:fin # id:fd_05_obrien_01
-> sala_obrien.traicion

// FD.06 — El café termina como el del Final C; después, el silencio y el epílogo
=== fd_epilogo ===
PENSAMIENTO: … # fx:negro # esperar:5 # id:fd_06_silencio
// FD.07 — Nota sobre el Capítulo II
PENSAMIENTO: … # minijuego:epilogo # id:fd_07_nota
// FD.08 — Última imagen
{ len_salvado:
    PENSAMIENTO: Un patio de Limehouse por la mañana. Ropa tendida de lado a lado. Una niña tiende sábanas y canta. # vineta:vineta-patio_limehouse_len # fx:aclarar # id:fd_08_pens_00b
- else:
    PENSAMIENTO: Un patio de Limehouse por la mañana. Ropa tendida de lado a lado. Una niña tiende sábanas y canta. # vineta:vineta-patio_limehouse # fx:aclarar # id:fd_08_pens_00
}
NIÑA: ♪ {cap_mov4} ♪ # sfx:naranjas # id:fd_08_nina
PENSAMIENTO: En la ventana de la cocina, una mujer mayor con un pañuelo en la cabeza. Dot, con el pelo canoso. # id:fd_08_pens_01
{ reloj_en_marcha:
    PENSAMIENTO: En su muñeca, el reloj de Ivy. Tic. Tic. # sfx:tic # id:fd_08_reloj
}
{ len_salvado:
    PENSAMIENTO: A su lado, un hombre mayor con un ancla tatuada en el cuello lee un fajo de papeles cosidos con hilo. # id:fd_08_len
}
PENSAMIENTO: La niña termina la frase y vuelve a empezar. # id:fd_08_pens_02
CARTEL: FINAL D · CAPÍTULO II # vineta:fin # minijuego:creditos,final=D # id:fd_08_fin # final:D
-> DONE
