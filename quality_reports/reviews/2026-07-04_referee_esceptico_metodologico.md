# Reporte de Arbitraje — Árbitro Escéptico/Metodológico
**Fecha:** 2026-07-04
**Artículo:** Análisis Sistemático de Operadores de PostgreSQL y Almacenamiento basado en CSI en Kubernetes: Arquitectura, Manejo de Fallos e Implicaciones en la Consistencia
**Recomendación:** Revisión Mayor
**Puntaje global:** 57/100

## Resumen

El artículo propone una taxonomía útil de operadores de PostgreSQL y almacenamiento CSI en Kubernetes, y un "marco formal" S=(O,K,C,D) con cuatro dimensiones R/C/P/I(S). Sin embargo, ninguna de las funciones f(·) se especifica u opera analíticamente en ningún punto del texto, el aparato formal contiene una colisión de notación (C usado para dos conceptos distintos) y una inconsistencia interna (K desaparece de la función de interacción multicapa pese a ser miembro de la tupla del sistema), y la Tabla I —la parte más sustantiva y verificable del artículo— corre en paralelo al marco formal sin conectarse a él. El artículo no ejecuta ningún experimento; todo el diseño empírico (Sección IV.E) es propuesto, no realizado.

## Puntajes por dimensión

| Dimensión | Peso | Puntaje | Notas |
|-----------|------|---------|-------|
| Contribución y novedad | 30% | 57 | Taxonomía razonable, pero se solapa con comparativas ya disponibles en documentación de proveedores/comunidad CNCF, no discutidas como estado del arte a superar. |
| Posicionamiento en la literatura | 25% | 62 | Cubre bien Borg/Omega, CAP, CSI, CockroachDB, WAL. Faltan referencias centrales sobre fault injection / chaos engineering. |
| Argumentos sustantivos | 20% | 45 | Las funciones f(·) nunca se resuelven; colisión de notación (C) e inconsistencia (I(S) omite K). Tabla I sólida pero no anclada a la notación formal. |
| Validez externa y alcance | 15% | 68 | El artículo reconoce explícitamente sus límites de cobertura y de entorno de validación. |
| Ajuste a la revista objetivo | 10% | 52 | Perfil compatible con trabajo conceptual, pero usa retórica de "análisis sistemático" con diseño experimental inminente sin ejecutar nada. |
| **Ponderado** | 100% | **57** | |

## Resultados de los chequeos de cordura

- **Consistencia de notación:** NO es consistente. **C** se usa simultáneamente para la capa de almacenamiento en S=(O,K,C,D) y para la dimensión de consistencia C(S)=f(Tx_confirmadas, Tx_visibles). **K** desaparece de I(S)=f(O×C×D) pese a ser miembro explícito de la tupla y pese a que la Tabla I le asigna un rol decisivo.
- **¿Se definen las funciones f(·)?** No. Nunca se especifica forma funcional, desigualdad, rango o regla de composición.
- **Tabla I vs. modelo formal:** Son dos análisis paralelos que no se conectan. Ninguna celda usa notación O, K, C, D o I(S).

## Comentarios mayores

1. Las funciones f(·) nunca se definen operacionalmente. — **Qué cambiaría mi opinión:** derivar al menos una proposición o desigualdad no trivial (p. ej., una cota del RPO en función de la latencia de replicación y del modo síncrono/asíncrono del backend CSI).
2. Colisión de notación: **C** denota simultáneamente la capa de almacenamiento y la dimensión de consistencia. — **Qué cambiaría mi opinión:** renombrar una de las dos y verificar consistencia en todo el documento.
3. I(S)=f(O×C×D) omite **K**, pese a ser miembro de la tupla S y actor central en la Tabla I. — **Qué cambiaría mi opinión:** incluir K explícitamente en I(S) con un ejemplo concreto, o justificar la exclusión.
4. La Tabla I y el aparato formal corren en paralelo sin integrarse. — **Qué cambiaría mi opinión:** anotar al menos una fila con la notación formal.
5. Ausencia total de validación empírica en un artículo con diseño experimental completamente especificado pero sin ejecución alguna. — **Qué cambiaría mi opinión:** ejecutar al menos el escenario (i) y reportar RTO/RPO reales.
6. Novedad frente a comparativas de industria no discutidas como estado del arte a superar. — **Qué cambiaría mi opinión:** una subsección que compare el modelo contra 2-3 comparativas técnicas ya publicadas.

## Comentarios menores

1. Tabla I atribuye tiempos de Kubernetes a [5]/[14], que no son la fuente primaria.
2. Verificar recuento de palabras del resumen contra el límite del perfil de revista.
3. Normalizar "conmutación por error (failover)" tras la primera aparición.
4. IV.E tiene detalle operativo que desentona con el resto conceptual — considerar apéndice.
5. Sin mención de pre-registro público para el diseño experimental propuesto.
6. El ejemplo de IV.C no se conecta a ningún término formal.

## Literatura faltante

- Kingsbury, "Jepsen: Distributed Systems Safety Research."
- Yuan et al., "Simple Testing Can Prevent Most Critical Failures," OSDI 2014.
- Basiri et al., "Chaos Engineering," IEEE Software 2016.
- Ongaro & Ousterhout, "In Search of an Understandable Consensus Algorithm (Raft)," USENIX ATC 2014.
- Documentación/literatura sobre Chaos Mesh, LitmusChaos.
- Literatura sobre corrección de reconciliación en Kubernetes Operators más allá de Kulkarni 2020 y el blog de Red Hat.

## Preguntas para los autores

1. ¿Pueden especificar la forma funcional de al menos una f(·)?
2. ¿Por qué K está ausente de I(S) si es miembro de S y actor central en la Tabla I?
3. ¿Se consideró ejecutar un escenario piloto antes de esta versión? ¿Qué lo impidió específicamente?
4. ¿Cómo se seleccionaron [5]/[14] como fuente de los tiempos NotReady/eviction?
5. ¿Considerarían reposicionar el artículo como "propuesta metodológica" o "position paper"?
6. ¿Cómo se relaciona formalmente la Tabla I con S=(O,K,C,D)?

## Lo que el artículo hace bien

1. Declara honestamente en la Discusión las limitaciones de no contar con validación empírica directa.
2. La Tabla I es una síntesis concreta y útil de responsabilidad por capa y tipo de fallo.
3. El diseño experimental de IV.E demuestra comprensión real de los desafíos de fault injection en producción air-gapped.
