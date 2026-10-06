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
{
- inventario ? tarjeta_crane:
    PENSAMIENTO: «Le devolveré la cara de su hermana.» # id:objetos_foto_crane_01
    PENSAMIENTO: Ya tengo su cara. Está en el cartel. # id:objetos_foto_crane_02
- genero == "f":
    PENSAMIENTO: Dos niños en un parque. La cara de Ivy, casi borrada por el agua. # vineta:vineta-foto_ivy_m # id:objetos_foto_01m
    PENSAMIENTO: Ya casi no se le ve la cara. # vineta:fin # id:objetos_foto_02m
- else:
    PENSAMIENTO: Dos niños en un parque. La cara de Ivy, casi borrada por el agua. # vineta:vineta-foto_ivy_h # id:objetos_foto_01
    PENSAMIENTO: Ya casi no se le ve la cara. # vineta:fin # id:objetos_foto_02
}
-> DONE

= nota_mirar
PENSAMIENTO: «¿Por qué nunca en el centro?» Letra apretada. En la esquina, un pájaro diminuto. # id:objetos_nota_01
-> DONE

= diario_mirar
PENSAMIENTO: Tapas negras. Papel crema. Un pájaro dibujado por dentro. Aquí no puedo abrirlo. # id:objetos_diario_01
-> DONE

= foto_restaurada_mirar
{ genero == "f":
    PENSAMIENTO: Ivy sonríe. Le falta un diente. Yo le tiro de una trenza. # vineta:vineta-foto_ivy_restaurada_m # id:objetos_foto_restaurada_01m
- else:
    PENSAMIENTO: Ivy sonríe. Le falta un diente. Yo le tiro de una trenza. # vineta:vineta-foto_ivy_restaurada_h # id:objetos_foto_restaurada_01
}
PENSAMIENTO: En el cartel tiene la boca cerrada. # vineta:fin # id:objetos_foto_restaurada_02
-> DONE

= llave_mirar
PENSAMIENTO: Una llave. Mañana a las once. # id:objetos_llave_01
PENSAMIENTO: Si la Planilla Azul no existe, no habré hecho nada malo. Solo habré mirado un papel en mi propio ministerio. # id:objetos_llave_02
PENSAMIENTO: Si existe… # id:objetos_llave_03
-> DONE

= directiva_mirar
PENSAMIENTO: «Ref directiva rectif. 0305.» # documento:directiva_j8 # id:objetos_directiva_01
PENSAMIENTO: Cero tres, cero cinco. # id:objetos_directiva_02
-> DONE

= copia_mirar
PENSAMIENTO: Mi letra, torcida, a lápiz. Bermondsey. Poplar. Folkestone. # id:objetos_copia_01
{ copia_firma:
    PENSAMIENTO: «Autoriza: H.V.» # id:objetos_copia_firma
}
-> DONE

= hoja_mirar
PENSAMIENTO: Papel azul. «Hora punta de mercado.» # documento:planilla_s16 # id:objetos_hoja_01
-> DONE

= libro_mirar
PENSAMIENTO: {libro_fragmentos} de 4. Hojas cosidas con hilo, contra la piel. # id:objetos_libro_01
{ libro_fragmentos:
- 1:
    PENSAMIENTO: «Basta con que el pueblo crea que lo hizo.» # id:objetos_libro_02a
- 2:
    PENSAMIENTO: «Pero para eso tendrían que saber.» # id:objetos_libro_02b
- 3:
    PENSAMIENTO: «El doblepensar no es un engaño. Es una disciplina.» # id:objetos_libro_02c
- else:
    PENSAMIENTO: «Un reloj parado es un acto de rebeldía.» # id:objetos_libro_02d
}
-> DONE

= times_mirar
PENSAMIENTO: «Cae un cohete en el distrito este.» A las 21:40. # documento:times_1979 # id:objetos_times_01
-> DONE

= foto_sotano_mirar
PENSAMIENTO: Ivy sonríe. Le falta un diente. A su lado, Nell. Y Barlow, con más pelo. # id:objetos_foto_sotano_01
PENSAMIENTO: Desde un ángulo bajo. Como a través de un hueco en la pared. # id:objetos_foto_sotano_02
-> DONE

= dibujos_mirar
PENSAMIENTO: Pájaros en los márgenes. Pozos de ventilación, salidas, estaciones tapiadas. # id:objetos_dibujos_01
PENSAMIENTO: Una ciudad debajo de la ciudad. # id:objetos_dibujos_02
-> DONE

= carta_mirar
PENSAMIENTO: «…tan dificil salir de ella.» Sin tilde. # documento:carta_ivy # id:objetos_carta_01
PENSAMIENTO: Su letra. # id:objetos_carta_02
-> DONE
