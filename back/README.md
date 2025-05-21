la carpeta 'db' contiene jsons que actuan  como la "base de datos".

ya se que me dijeron que lo haga con diccionarios nomas pero en lo de opcional decia algo de serializar el estado asi q xd

y tambien los usuarios tienen users y passwords (claramente sin criptografia ni nada porque xd) para eso mismo

y se tiene una tabla para currency en lugar de hacer que los usuarios tengan soles y dolares para tener soportes para multiples currencies en un futuro (es decir, un usuario tiene multiples currencies en lugar de estar forzado a solo ser soles o dolares, ej: escalabilidad)

tambien deje un dockerfile alli aunque no he verificado si funciona (lo hizo gpt xd) quizas para intentar contenerizar el backend y tenerlo separado del front

aun falta aplicar patrones de diseño como singletons y eso pero eso va despues diria yo xd