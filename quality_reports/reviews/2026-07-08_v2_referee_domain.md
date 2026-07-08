# Informe de Árbitro de DOMINIO — v2-experimental (Fase 2)

**Fecha:** 2026-07-07 · **Disposición:** STRUCTURAL · **Tier:** primario iberoamericano
**Recomendación:** Revisión Mayor · **Puntuación: 72/100**

## Resumen
Marco conceptual multicapa + piloto empírico honesto y bien instrumentado sobre CloudNativePG bajo tres modos de fallo. Hallazgo genuino y contraintuitivo: **la visibilidad del fallo ante Kubernetes, no el fallo, determina el failover** (matar el pod se recupera ~4.6× más rápido que "fallarlo"). Ese resultado + la disciplina al declarar límites elevan claramente el trabajo respecto de la ronda previa (54→72). Debilidad estructural persistente: el aparato S=(O,K,M,D) no *predice* ni *discrimina* — es organizativo y de hecho se refinó *post hoc* cuando la evidencia lo contradijo. Con lagunas de posicionamiento, esto sitúa el artículo en Mayor, no Menor.

## Puntuaciones por dimensión
| Dimensión | Peso | Punt. |
|---|---|---|
| Contribución y novedad | 30% | 72 |
| Posicionamiento | 25% | 64 |
| Sustancia de argumentos | 20% | 82 |
| Validez externa | 15% | 70 |
| Ajuste a la revista | 10% | 80 |
| **Ponderado** | 100% | **72** |

## Comentarios mayores
1. **El marco no demuestra poder predictivo/discriminante.** El paper admite (III.C) que las f(·) son organizativas. Peor: en §VI.C el marco "anticipó" F1 (trivial: matar el primario dispara failover), pero **F2 falsó la predicción** (pod-failure no promovió) y se reencuadra como "refina el modelo"; F4 "motiva extensión". El hallazgo valioso (visibilidad ante K8s) es empírico y **ortogonal** a la tupla, que no contiene la variable Ready/NotReady/eliminado. *Cambiaría mi opinión:* (a) hacer la visibilidad V(fallo,K) dimensión de primera clase que **derive** el gradiente F1/F2/F3, o (b) rebajar el formalismo a vocabulario descriptivo y hacer del hallazgo la contribución central, sin reclamar "validación del modelo".
2. **Falta engagement con el chaos-testing del propio CloudNativePG** (LitmusChaos en CI, borrado del primario = F1). *Cambiaría mi opinión:* párrafo en Trabajos Relacionados que delimite qué añade F1 (cuantificación de RTO, contraste F1-vs-F2, hallazgo de visibilidad).
3. **Falta literatura reciente (arXiv 2025) de resiliencia K8s por inyección de fallos.** Reposicionar la brecha en positivo (operador-PostgreSQL + CSI + verificador a nivel de commit).
4. **[9] Avizienis mal caracterizado** (es taxonomía de dependabilidad, no "modelo probabilístico"); la taxonomía propia no se distingue de ella. *Cambiaría mi opinión:* corregir la caracterización y posicionar la taxonomía propia frente a Avizienis.
5. **Afirmaciones comparativas de §IV.A** (Zalando/Patroni latencia de detección/promoción) son inferencia de documentación, no medición. *Cambiaría mi opinión:* marcarlas como "esperado según documentación, no medido".

## Comentarios menores
1. [17] (Alvaro & Tymon) es lineage-driven fault injection, no el Jepsen de Kingsbury; precisar o citar Jepsen directamente.
2. Etiqueta "CP" de F3: añadir nota de matiz (CAP mal definido operacionalmente).
3. Declarar que la separación completa (U=0) hace irrelevante n para F1-vs-F2.
4. Fig. 1 en `.svg` → verificar PDF para XeLaTeX. *(Ya resuelto: TikZ→PDF.)*
5. Consolidar la repetición de "clúster productivo".
6. La distinción RPO nulo trivial (F2/F3) vs genuino (F1) es excelente — mantenerla.

## Preguntas para el autor
1. ¿Qué añade F1 sobre el chaos-CI del propio proyecto CNPG?
2. ¿Puede el modelo **derivar** el gradiente F1/F2/F3 o solo describirlo post hoc?
3. ¿La recreación "en su sitio" de F2 es configurable (`failoverDelay`) o default? (condiciona la generalización del RTO 36.75 s).
4. ¿La granularidad ≈0.2 s afecta cada escenario? (≈2.5% en F1, despreciable en F3).
5. Con las 3 instancias co-localizadas, ¿la replicación asíncrona viaja por red o es intra-nodo/loopback? (afecta si RPO=0 en F1 prueba durabilidad de red real).
