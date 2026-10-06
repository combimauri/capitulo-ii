// PRÓLOGO — Calle Stepney, 1979 (guion: docs/guion-detallado/01-acto-1.md)

=== prologo ===
# fx:negro
# sfx:silbido # esperar:2.7
# sfx:impacto # sfx:pitido # fx:temblor # esperar:1.4
CARTEL: Calle Stepney. Franja Aérea 1. 1979. # id:p01_cartel
# fx:aclarar
TELEPANTALLA: …cobarde ataque… euroasiático… población civil… el Partido… venganza… # id:p01_tp_01
-> DONE

=== stepney ===

= tele_mirar
PENSAMIENTO: Sigue hablando. Incluso aquí sigue hablando. # id:p01_tele_mirar
-> DONE

= fuego_mirar
PENSAMIENTO: Nuestra casa. Eso era nuestra casa. # id:p01_fuego_mirar
-> DONE

= cascotes_mirar
PENSAMIENTO: Algo se mueve debajo. # id:p01_cascotes_mirar
-> DONE

= cascotes_usar
# minijuego:cascotes
PENSAMIENTO: Una mano. # id:p01_mano # escena:stepney_ivy # pos:ivy
-> DONE

// ------------------------------------------------------------------ P.02 — Ivy
= ivy
{ ivy_vista:
    -> DONE
}
~ ivy_vista = true
PROTAGONISTA: ¡Ivy! ¡Ivy, mírame! Te voy a sacar, ¿me oyes? Te voy a sacar. # id:p02_prot_01
IVY: Naranjas y limones… dicen las campanas de San Clemente… # id:p02_ivy_01
PROTAGONISTA: No cantes. No gastes aire. # id:p02_prot_02
IVY: Escúchame. No les creas. No les… # id:p02_ivy_02
PENSAMIENTO: Su mano cae. En su muñeca, un reloj con el cristal roto. # id:p02_pens_01 # esperar:0.8
-> DONE

= ivy_mirar
PENSAMIENTO: Ivy. # id:p02_ivy_mirar
-> DONE

= reloj_mirar
PENSAMIENTO: Las nueve y cuarenta. Se ha parado a las nueve y cuarenta. # id:p02_reloj_mirar
-> DONE

= reloj_usar
~ inventario += reloj_ivy
~ reloj_cogido = true
~ p_nell = true
MUJER PROLE: ¡Aquí! ¡Hay alguien aquí! ¡Traed una palanca! # refrescar # id:p02_nell_01
~ p_oficial = true
OFICIAL: Apártense. Todos. # refrescar # id:p02_oficial_01
OFICIAL: Esta camarada ya no les pertenece. Ahora es una mártir del Partido. # id:p02_oficial_02
~ p_nell = false
PROTAGONISTA: …Eurasia. # esperar:1.2 # refrescar # id:p02_prot_03
PENSAMIENTO: Eurasia. Eurasia. Eurasia. # id:p02_pens_02
// P.03 — Ficha de Afiliación del Partido, y cinco años después
~ inventario += ficha
# fx:blanco # minijuego:ficha # fx:negro # sfx:silbato
CARTEL: Mansiones Victoria. Franja Aérea 1. 1984. # id:p03_cartel # escena:piso # pos:cama
-> DONE
