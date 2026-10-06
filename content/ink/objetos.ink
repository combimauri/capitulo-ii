// Objetos del inventario: mirarlos y usarlos con algo del escenario (diseño técnico §7, «usar con»).
=== objetos ===

= no_sirve
PENSAMIENTO: No. Eso no sirve aquí. # id:objetos_no_sirve
-> DONE

= lapiz_mirar
{ dp_j3_amory:
- "aceptar":
    PENSAMIENTO: Un lápiz mordido. «F.A.» ¿De quién…? # id:objetos_lapiz_aceptar_01
    PENSAMIENTO: No significa nada. Iniciales cualesquiera. # id:objetos_lapiz_aceptar_02
- "recordar":
    PENSAMIENTO: F.A. Felix Amory. Me lo prestó ayer. «Que no se diga que Cartografía no comparte.» # id:objetos_lapiz_recordar_01
    PENSAMIENTO: Esto es una prueba. Esto existió. # id:objetos_lapiz_recordar_02
- else:
    PENSAMIENTO: El lápiz de Amory, mordido por la punta. Se lo devolveré mañana. # id:objetos_lapiz_01
}
-> DONE
