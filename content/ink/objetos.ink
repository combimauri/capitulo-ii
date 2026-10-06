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

= foto_mirar
{ inventario ? tarjeta_crane:
    PENSAMIENTO: «Le devolveré la cara de su hermana.» # id:objetos_foto_crane_01
    PENSAMIENTO: Ya tengo su cara. Está en el cartel. # id:objetos_foto_crane_02
- else:
    PENSAMIENTO: Dos niños en un parque. La cara de Ivy, casi borrada por el agua. # id:objetos_foto_01
}
-> DONE

= nota_mirar
PENSAMIENTO: «¿Por qué nunca en el centro?» Letra apretada. En la esquina, un pájaro diminuto. # id:objetos_nota_01
-> DONE

= diario_mirar
PENSAMIENTO: Tapas negras. Papel crema. Un pájaro dibujado por dentro. Aquí no puedo abrirlo. # id:objetos_diario_01
-> DONE

= foto_restaurada_mirar
PENSAMIENTO: Ivy sonríe. Le falta un diente. Yo le tiro de una trenza. # id:objetos_foto_restaurada_01
PENSAMIENTO: En el cartel tiene la boca cerrada. # id:objetos_foto_restaurada_02
-> DONE

= llave_mirar
PENSAMIENTO: Una llave. Mañana a las once. # id:objetos_llave_01
PENSAMIENTO: Si la Planilla Azul no existe, no habré hecho nada malo. Solo habré mirado un papel en mi propio ministerio. # id:objetos_llave_02
PENSAMIENTO: Si existe… # id:objetos_llave_03
-> DONE
