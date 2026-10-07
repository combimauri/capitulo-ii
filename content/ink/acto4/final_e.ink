// FINAL E — «El nuevo Goldstein» (guion: docs/guion-detallado/05-finales.md)
// Quedarse en la cripta. Los años. La cara del protagonista en los Dos Minutos de Odio. El despacho donde
// O'Brien decide no clavar una chincheta. ¿Fuiste libre, o fuiste útil?

=== final_e ===
~ final_en_curso = "E"
// FE.01 — El té frío
PENSAMIENTO: Dejo la copia sobre la mesa. Me siento frente a él. # musica:cripta # id:fe_01_pens_00
PROTAGONISTA: ¿Queda té? # id:fe_01_prot_01
PENSAMIENTO: Me sirve. Está frío. Sonríe. # id:fe_01_pens_01
GOLDSTEIN: Siempre queda té. Nunca está caliente. # id:fe_01_gold_01
PENSAMIENTO: Vuelve a la máquina de escribir. Cojo un libro de la estantería. Un libro de verdad, viejo. Lo abro. # sfx:tecla # id:fe_01_pens_02
PENSAMIENTO: Nadie me buscará aquí. # esperar:1 # id:fe_01_pens_03
PENSAMIENTO: «Nunca buscan aquí.» # id:fe_01_pens_04
// FE.02 — Los años
CARTEL: 1985 # vineta:vineta-cripta_1985 # musica:maquina # id:fe_02_1985
PENSAMIENTO: Escribimos uno frente al otro. Brooke baja por la escalera con un cesto de comida y se lleva un fajo de copias. # sfx:tecla # id:fe_02_1985_txt
CARTEL: 1987 # vineta:vineta-cripta_1987 # id:fe_02_1987
PENSAMIENTO: Tose en el camastro. Le sostengo la taza. # sfx:tos # id:fe_02_1987_txt
CARTEL: 1988 # vineta:vineta-cripta_1988 # id:fe_02_1988
PENSAMIENTO: Una losa sin nombre entre las lápidas borradas. Encima, unas gafas remendadas con hilo. # id:fe_02_1988_txt
CARTEL: 1990 # vineta:vineta-cripta_1990 # id:fe_02_1990
PENSAMIENTO: Tengo canas. La estructura de las campanas, detrás, sigue vacía. # sfx:tecla # id:fe_02_1990_txt
CARTEL: 1993 # vineta:vineta-cripta_1993 # id:fe_02_1993
PENSAMIENTO: Alguien baja por la escalera. Una muchacha joven, con pañuelo y la mirada dura. # id:fe_02_1993_txt_01
MUCHACHA: Naranjas y limones, dicen las campanas de San Clemente. # id:fe_02_1993_muchacha
PROTAGONISTA: …me debes tres peniques, dicen las campanas de San Martín. # id:fe_02_1993_prot
PENSAMIENTO: Le sirvo té. Frío. # id:fe_02_1993_txt_02
// FE.03 — Los Dos Minutos de Odio
{ genero == "f":
    PENSAMIENTO: El Gran Salón del Minipax. Los Dos Minutos de Odio. El chirrido metálico de siempre. # vineta:vineta-salon_odio_m # sfx:chirrido # musica:silencio # id:fe_03_pens_00m
- else:
    PENSAMIENTO: El Gran Salón del Minipax. Los Dos Minutos de Odio. El chirrido metálico de siempre. # vineta:vineta-salon_odio_h # sfx:chirrido # musica:silencio # id:fe_03_pens_00
}
PENSAMIENTO: En la telepantalla gigante no aparece Goldstein. Aparece mi cara. Más vieja, con canas, con gafas. Con rasgos de enemigo. # id:fe_03_pens_01
TELEPANTALLA: …la libertad… la memoria… un reloj que vuelve a andar… # id:fe_03_tp_01
PENSAMIENTO: Hilda, más vieja, en primera fila. Lanza su zapato a la pantalla. # id:fe_03_pens_02
HILDA: ¡{g("TRAIDOR", "TRAIDORA")}! ¡{g("TRAIDOR", "TRAIDORA")}! ¡YO VIVÍA EN SU MISMO BLOQUE! ¡YO LO SABÍA! ¡LO APUNTÉ! # id:fe_03_hilda_01
PENSAMIENTO: Al fondo de la sala, un funcionario joven, uno solo, no grita. Se limpia las gafas. # id:fe_03_pens_03
// FE.04 — El despacho
{ crane_humillado:
    PENSAMIENTO: Un despacho del Partido Interior. Una ventana de verdad. Café de verdad. Una telepantalla apagada. # vineta:vineta-despacho_obrien_crane # musica:voss # id:fe_04_pens_00c
- else:
    PENSAMIENTO: Un despacho del Partido Interior. Una ventana de verdad. Café de verdad. Una telepantalla apagada. # vineta:vineta-despacho_obrien # musica:voss # id:fe_04_pens_00
}
PENSAMIENTO: Sobre la mesa, el mapa del Registro de Impactos. Miles de chinchetas negras. Y junto al Miniver, un círculo blanco perfecto, con una cruz pequeña dentro. # id:fe_04_pens_01
VOSS: El último fragmento ha llegado a Southwark. Y a Bermondsey. Lo cantan en los patios. # esperar:0.8 # id:fe_04_voss_01
VOSS: ¿Intervenimos? # id:fe_04_voss_02
O'BRIEN: No. # id:fe_04_obrien_01
VOSS: Es un riesgo. # id:fe_04_voss_03
O'BRIEN: Es una válvula. # esperar:1 # id:fe_04_obrien_02
O'BRIEN: Un Partido sin Goldstein no sabría a quién odiar. Y un pueblo sin libro prohibido no sabría qué es lo que no debe pensar. # id:fe_04_obrien_03
O'BRIEN: Lo necesitamos. Siempre lo hemos necesitado. Al viejo. Y ahora a este. # id:fe_04_obrien_04
{ crane_humillado:
    CRANE: Yo estuve allí. Les tenía a los dos. # id:fe_04_crane_01
    O'BRIEN: Lo sé. Me llamó usted. # esperar:1 # id:fe_04_obrien_05
    O'BRIEN: Hizo bien en colgar. # id:fe_04_obrien_06
}
VOSS: ¿Y si un día deja de ser una válvula? # id:fe_04_voss_04
PENSAMIENTO: Por primera vez, una pausa larga. Se quita las gafas. Las limpia. # esperar:1.5 # id:fe_04_pens_02
O'BRIEN: Entonces habremos perdido. # esperar:1 # id:fe_04_obrien_07
O'BRIEN: Pero no será este año. Ni el próximo. # id:fe_04_obrien_08
PENSAMIENTO: Coge una chincheta negra. La sostiene sobre el círculo blanco. Un segundo. Dos. # esperar:2 # id:fe_04_pens_03
PENSAMIENTO: La deja en la mesa, fuera del círculo. # id:fe_04_pens_04
// FE.05 — Cierre
PENSAMIENTO: La cripta. Una vela. Tecleo. # vineta:loc-cripta # sfx:tecla # musica:maquina # id:fe_05_pens_00
PENSAMIENTO: Arriba, muy lejos, un silbido de cohete. Me detengo. Escucho. # sfx:silbido # esperar:2 # id:fe_05_pens_01
PENSAMIENTO: El silbido se aleja. Nunca cae aquí. # id:fe_05_pens_02
PENSAMIENTO: Nunca cae aquí. # esperar:1 # id:fe_05_pens_03
PENSAMIENTO: Cada noche me pregunto si eso es la libertad. # esperar:1 # id:fe_05_pens_04
PENSAMIENTO: O si es la jaula más bonita de Oceanía. # id:fe_05_pens_05
CARTEL: ¿Fuiste libre? # vineta:fin # id:fe_05_cartel_01
CARTEL: ¿O fuiste útil? # esperar:1.5 # id:fe_05_cartel_02
CARTEL: FINAL E · EL NUEVO GOLDSTEIN # minijuego:creditos,final=E # id:fe_05_fin # final:E
-> DONE
