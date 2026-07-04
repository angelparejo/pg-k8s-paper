# Referencias por Verificar — articulo_angelparejov1-6.md

**Fecha:** 2026-07-04
**Estado:** PENDIENTE — bloqueante para someter el artículo
**Alcance:** [5], [10], [11], [14], [15] no están en `Bibliography_base.bib`. Las 9 restantes ([1],[2],[4],[6],[7],[8],[9],[12],[13]) y [3] (con URL corregida) ya están verificadas y añadidas.

---

## [5] — S. Kulkarni et al., "Declarative stateful systems in Kubernetes," IEEE Cloud Computing, vol. 7, no. 2, pp. 52–61, 2020.

**Diagnóstico:** NO CONFIRMADA. Búsqueda web (2026-07-04) no localizó ningún artículo con este autor, título o venue. La búsqueda sí encontró a un S. G. Kulkarni real, pero coautor de "Understanding Container Network Interface Plugins" (2020, IEEE LANMAN) — un tema distinto (CNI, no operadores stateful).

**Dónde se cita y qué afirmación respalda:**
1. **I. Introducción** (línea 11): "...ha favorecido el desarrollo de operadores de bases de datos... como un mecanismo para automatizar la gestión del ciclo de vida, la replicación y los procesos de conmutación por error (failover) [5], [14]."
2. **II. Trabajos Relacionados** (línea 39): "...los enfoques declarativos para sistemas stateful han puesto de manifiesto la relevancia del patrón operator y de la lógica de reconciliación como mecanismo de control [5]."
3. **III.A Taxonomía** (línea 57): "...influyen en cómo se detectan fallos, se ejecutan procesos de conmutación por error (failover) y se gestionan las transiciones de estado [5], [14]."
4. **III.B Modelo del sistema** (línea 69): "...en enfoques declarativos para la gestión de sistemas con estado (stateful) [5]."
5. **IV.A Comparación entre operadores** (líneas 107, 109): dos veces, respaldando el comportamiento comparativo de CloudNativePG/Zalando/Crunchy y la afirmación general sobre coordinación en "sistemas distribuidos y plataformas stateful."

**Impacto si resulta inexistente:** Alto en volumen (6 citas), pero bajo en originalidad de la afirmación — en todos los casos respalda el concepto general y bien establecido del "patrón operator" de Kubernetes, no una afirmación específica o cuantitativa. Es reemplazable sin debilitar el argumento.

**Fuente real verificada que respalda la misma afirmación:**
> Kubernetes, "Operator pattern," Kubernetes Documentation. [Online]. Available: https://kubernetes.io/docs/concepts/extend-kubernetes/operator/

Alternativa histórica/fundacional (también verificada):
> B. Philips, "Introducing Operators: Putting Operational Knowledge into Software," CoreOS/Red Hat Blog, 2016. [Online]. Available: https://www.redhat.com/en/blog/introducing-operators-putting-operational-knowledge-into-software

**Acción recomendada:** Sustituir [5] por la documentación oficial del patrón Operator (o por Philips 2016 si se prefiere la referencia histórica/fundacional). No requiere reformular ninguna afirmación del texto — el reemplazo respalda literalmente lo mismo.

---

## [10] — S. Nayak, "SQL and NoSQL database architectures: A performance evaluation and systematic review," Journal of Systems and Software, vol. 195, 2023.

**Diagnóstico:** NO CONFIRMADA. No se encontró ningún artículo de "Nayak" con este título en JSS. Se encontró un artículo de tema casi idéntico pero de otros autores y otra revista (ver abajo) — probable confusión de fuente, no necesariamente invención deliberada.

**Dónde se cita y qué afirmación respalda:**
1. **I. Introducción** (línea 15): "...la literatura existente tiende a analizarlos de manera aislada, ya sea desde la perspectiva de la orquestación, la consistencia en sistemas distribuidos o la arquitectura de bases de datos [6], [7], [10]."
2. **III.C Dimensiones de evaluación — Rendimiento** (línea 83): "Rendimiento: se aproxima mediante P(S) = f(latencia, throughput)... en línea con estudios comparativos de arquitecturas de bases de datos [10]."

**Impacto si resulta inexistente:** Moderado — es la única cita que respalda directamente la definición de la dimensión "Rendimiento" del marco formal (III.C). Sin reemplazo, esa dimensión queda sin anclaje bibliográfico.

**Fuente real verificada que respalda la misma afirmación:**
> W. Khan, T. Kumar, C. Zhang, K. Raj, A. M. Roy, and B. Luo, "SQL and NoSQL Database Software Architecture Performance Analysis and Assessments — A Systematic Literature Review," Big Data and Cognitive Computing, vol. 7, no. 2, art. 97, 2023. DOI: 10.3390/bdcc7020097.

**Acción recomendada:** Sustituir [10] por Khan et al. (2023) — mismo tema exacto (evaluación comparativa de rendimiento SQL/NoSQL), año idéntico, revista real e indexada (MDPI, Scopus). Es casi seguro que esta sea la fuente que el autor original tenía en mente.

---

## [11] — Y. Cao et al., "PALF: Replicated write-ahead logging for distributed databases," Proc. VLDB, 2024.

**Diagnóstico:** El paper SÍ existe y es real, pero la autoría citada es incorrecta. El primer autor real es **Fusheng Han**, no "Y. Cao" — "Cao" no aparece en ninguna posición de los 13 autores reales (Han, Liu, Chen, Jia, Zhou, Teng, Yang, Xi, Tian, Tao, Wang, Xu, Yang). Es un error de atribución, no de existencia del artículo.

**Dónde se cita y qué afirmación respalda:**
1. **II. Trabajos Relacionados** (línea 43): "...los estudios basados en Write-Ahead Logging (WAL) destacan su papel central en la durabilidad y recuperación de datos [11], [12]."
2. **III.D Invariantes del sistema — Invariante de durabilidad** (línea 97): "toda operación registrada en el log de escritura anticipada (WAL) debe ser recuperable tras un fallo, tal como se establece en estudios sobre mecanismos de recuperación en bases de datos [11], [12]."
3. **IV.C Interacción operador–almacenamiento** (línea 134): "...particularmente en relación con la persistencia del WAL [11], [12]."

**Impacto si resulta inexistente:** Sería alto — **respalda directamente uno de los tres invariantes centrales del marco formal** (Invariante de durabilidad, III.D). Afortunadamente el artículo SÍ existe (solo la autoría está mal citada), y en las tres ubicaciones está co-citado con [12] (Stonebraker & Kemnitz 1991, verificado), que ya provee respaldo independiente. El riesgo real es de integridad de citación, no de sustento del argumento.

**Cita corregida con datos reales verificados:**
> F. Han, H. Liu, B. Chen, D. Jia, J. Zhou, X. Teng, C. Yang, H. Xi, W. Tian, S. Tao, S. Wang, Q. Xu, and Z. Yang, "PALF: Replicated Write-Ahead Logging for Distributed Databases," Proc. VLDB Endow., vol. 17, no. 12, pp. 3745–3758, 2024. DOI: 10.14778/3685800.3685803.

**Acción recomendada:** Corregir la autoría en el artículo (de "Y. Cao et al." a "F. Han et al.") y añadir páginas 3745–3758. No requiere cambiar la afirmación ni buscar otra fuente — el paper real sustenta el mismo punto.

---

## [14] — Red Hat, "Orchestrating a stateful application using Kubernetes Operators," 2021.

**Diagnóstico:** NO CONFIRMADA con este título exacto. Búsqueda web no encontró ninguna entrada de Red Hat con este título literal en 2021. Se encontraron artículos relacionados de la misma época y editor:
- "Managing stateful applications with Kubernetes Operators in Golang," Red Hat Developer, ago. 2021.
- "Operators over easy: an introduction to Kubernetes Operators," Red Hat Blog.

**Dónde se cita y qué afirmación respalda:** Comparte las mismas 4 ubicaciones que [5] (Introducción línea 11, III.A línea 57, IV.A líneas 107 y 109) — siempre coemparejada con [5] — más una quinta ubicación propia:
5. **IV.C Interacción operador–almacenamiento — intro de Tabla I** (línea 121): "...a partir del comportamiento documentado de CloudNativePG [19], Zalando Postgres Operator (Patroni) [20] y Crunchy Postgres for Kubernetes [14], [21]..." — aquí respalda específicamente el comportamiento de Crunchy.

**Impacto si resulta inexistente:** Bajo-moderado. En las 4 ubicaciones compartidas con [5], el respaldo es redundante con [5] (ambas fallando simultáneamente sería más grave — ver acción recomendada). En la Tabla I (ubicación 5), Crunchy ya tiene respaldo independiente y verificado vía [21] (documentación oficial de Crunchy Data), por lo que [14] es allí complementaria, no crítica.

**Fuente real verificada que respalda la misma afirmación:**
> Kubernetes, "Operator pattern," Kubernetes Documentation. [Online]. Available: https://kubernetes.io/docs/concepts/extend-kubernetes/operator/ (misma sustitución sugerida para [5])

O, si se prefiere mantener una fuente específica de Red Hat:
> "Managing stateful applications with Kubernetes Operators in Golang," Red Hat Developer, 2021. [Online]. Available: https://developers.redhat.com/articles/2021/08/04/managing-stateful-applications-kubernetes-operators-golang

**Acción recomendada:** Dado que [5] y [14] se citan casi siempre juntas y ambas tienen problemas, lo más simple es consolidarlas: sustituir el par [5],[14] por una única cita a la documentación oficial del patrón Operator en las 4 ubicaciones compartidas, y mantener [21] como respaldo suficiente para Crunchy en la Tabla I (ya no se necesitaría [14] ahí tampoco).

---

## [15] — J. Santos et al., "Deploying a scalable PostgreSQL database on Kubernetes: Toward serverless operations," Future Generation Computer Systems, 2025.

**Diagnóstico — el más serio de los seis.** No se encontró este artículo en FGCS. Se encontró un artículo de título casi idéntico, **"Deploying a scalable PostgreSQL database on a Kubernetes cluster in a data center: A path toward serverless operations,"** de un único autor, **Diwakar Krishnakumar**, publicado en ***World Journal of Advanced Research and Reviews* (WJARR), vol. 26, no. 1, pp. 1021–1027, 2025** — una revista de acceso abierto de un tier bibliométrico muy inferior a FGCS (Elsevier, Q1, indexada en Scopus/JCR). Si esta es la fuente real, el artículo le atribuye tanto un autor como una revista incorrectos, prestándole el prestigio editorial de FGCS a un trabajo publicado en un venue muy distinto.

**Dónde se cita y qué afirmación respalda:**
1. **II. Trabajos Relacionados** (línea 43, última frase): "Adicionalmente, investigaciones recientes han comenzado a explorar el despliegue de bases de datos en Kubernetes mediante operadores, lo que evidencia el creciente interés en la automatización de cargas stateful [14], [15]."

**Impacto si resulta inexistente:** Bajo en sustento argumentativo (una sola cita, respalda una afirmación genérica de "interés reciente creciente," no un dato ni un mecanismo específico) pero **alto en riesgo reputacional/de integridad** — es exactamente el tipo de discrepancia que un árbitro o un chequeo de plagio/fabricación detectaría con una sola búsqueda, y podría proyectarse sobre la credibilidad de todo el resto del artículo.

**Cita corregida con datos reales verificados (si se confirma que es la fuente pretendida):**
> D. Krishnakumar, "Deploying a Scalable PostgreSQL Database on a Kubernetes Cluster in a Data Center: A Path Toward Serverless Operations," World Journal of Advanced Research and Reviews, vol. 26, no. 1, pp. 1021–1027, 2025.

**Acción recomendada — prioridad alta:** No usar esta cita tal como está. Dos caminos:
(a) Confirmar que Krishnakumar/WJARR es la fuente pretendida y citarla correctamente, aceptando que es una revista de menor peso para esta afirmación (o buscar si el mismo autor tiene una versión revisada en otro venue); o
(b) Eliminar la cita y reformular la frase sin ella, apoyándose únicamente en [14] (una vez resuelta) — la afirmación en sí ("interés reciente en desplegar BD en K8s mediante operadores") ya está suficientemente respaldada por el resto de la sección II sin necesitar esta referencia adicional.

---

## Resumen de acciones pendientes (por prioridad)

| Ref | Prioridad | Acción |
|---|---|---|
| [15] | **Alta** | Decidir: citar correctamente a Krishnakumar/WJARR, o eliminar y reformular sin ella. |
| [11] | Media | Corregir autoría a "F. Han et al." — el paper es real, solo hay que arreglar el nombre y añadir páginas. |
| [5] + [14] | Media | Consolidar ambas en una sola cita a la documentación oficial del patrón Operator de Kubernetes (o Philips 2016 para [5], Red Hat Developer 2021 real para [14] si se prefieren dos fuentes distintas). |
| [10] | Media | Sustituir por Khan et al. (2023), Big Data and Cognitive Computing — mismo tema, año, y probablemente la fuente real pretendida. |

Ninguna de estas correcciones requiere reescribir el argumento del artículo — en los cinco casos, las afirmaciones sustantivas sobreviven con fuentes reales equivalentes. El artículo no ha sido editado; esta lista queda como trabajo pendiente para antes de someter.
