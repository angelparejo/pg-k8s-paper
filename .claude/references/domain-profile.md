# Domain Profile

## Field

**Primary:** Distributed Systems / Cloud-Native Databases (PostgreSQL sobre Kubernetes)
**Adjacent subfields:** Storage Systems (CSI, SAN/Fibre Channel), Site Reliability Engineering / Chaos Engineering, Container Orchestration, Database Replication & Consensus

---

## Target Journals (ranked by tier)

| Tier | Revistas | Notas |
|------|----------|-------|
| **PRIMARIO** (objetivo inmediato, español) | CLEI Electronic Journal; RISTI — Revista Ibérica de Sistemas e Tecnologias de Informação; Ingeniare — Revista Chilena de Ingeniería; Computación y Sistemas (CIC-IPN, México) | Envío en español. Indexación Scopus/SciELO y cuartil de las **cuatro** revistas: **pendientes de verificar** en el portal de cada revista antes de someter — no asumir el estado a partir de este documento. |
| **SECUNDARIO** (futuro, inglés) | Future Generation Computer Systems (FGCS); Journal of Systems and Software (JSS); IEEE Access | Requiere, en este orden: (1) validación empírica completa de los experimentos, (2) traducción íntegra al inglés + pase de language editing. No se somete a este tier hasta cumplir ambas condiciones. |

---

## Common Data Sources

| Dataset | Type | Access | Notes |
|---------|------|--------|-------|
| Trazas de carga pgbench / sysbench | Benchmark OLTP sintético | Local (generado en el testbed) | Benchmark estándar de throughput/latencia de PostgreSQL bajo carga |
| Logs de inyección de fallos de Chaos Mesh | Inyección de fallos experimental | Local (generado en el testbed) | Registros de pod-failure y fallos de red con timestamps |
| Telemetría de Prometheus / kube-state-metrics | Telemetría del clúster | Local (generado en el testbed) | Estado de pods, eventos de attach/detach del volumen CSI, condiciones de nodo |
| Logs de operador CloudNativePG / Zalando-Patroni | Logs del plano de control del operador | Local (generado en el testbed) | Decisiones de failover, elección de líder, lag de replicación |

---

## Common Evaluation Methodologies

<!-- Renombrado desde "Common Identification Strategies" — este proyecto no hace afirmaciones causales. -->

| Estrategia | Aplicación típica | Supuesto clave a defender |
|----------|---------------------|---------------------------|
| Inyección de fallos controlada (Chaos Mesh) | Comparar el comportamiento de recuperación entre configuraciones de operador/CSI bajo fallos inducidos | El fallo inyectado es representativo del modo de fallo reclamado — ver limitación conocida sobre pod-failure vs. fallo real de nodo |
| Comparación entre dos operadores (CloudNativePG vs. Zalando/Patroni) | Aislar el efecto de la capa de operador sobre RTO/RPO manteniendo fijas las capas de almacenamiento y red | La configuración del testbed se mantiene constante entre operadores; las diferencias observadas son atribuibles a la lógica del operador, no a variación de infraestructura |
| Comparación no paramétrica de medidas repetidas | Muestras pequeñas de RTO/RPO con distribuciones no normales | Independencia entre corridas; comparación distribucional vía Mann-Whitney/Kruskal-Wallis, no inferencia paramétrica |

---

## Field Conventions

- **Stack del testbed (reproducibilidad):** Kubernetes 1.34.6, CloudNativePG 1.28.0, PostgreSQL 16.13, CSI Huawei 4.10.1 (Fibre Channel/SAN), Calico 3.31.4 (CNI)
- **Herramienta de inyección de fallos:** Chaos Mesh
- **Operadores comparados:** CloudNativePG y Zalando/Patroni
- **Métricas primarias:** RTO (Recovery Time Objective) y RPO (Recovery Point Objective)
- **Análisis estadístico:** exclusivamente no paramétrico — Mann-Whitney U (dos grupos), Kruskal-Wallis (más de dos grupos), correlación de Spearman (asociación) — justificado por distribuciones no normales y n pequeño. Sin lenguaje de inferencia causal, sin pruebas paramétricas que asuman normalidad.
- Reportar medianas y RIC (rango intercuartílico) para RTO/RPO, no medias/DE, dada la no normalidad.
- Especificar las comparaciones antes de ejecutar pruebas no paramétricas repetidas, para evitar "fishing" de comparaciones múltiples.

---

## Notation Conventions

| Symbol | Significado | Anti-patrón |
|--------|--------------|--------------|
| $RTO$ | Tiempo de Recuperación (Recovery Time Objective) — tiempo desde la inyección del fallo hasta la restauración del servicio | No confundir con el tiempo de sólo detección del failover |
| $RPO$ | Punto de Recuperación (Recovery Point Objective) — ventana de pérdida de datos (transacciones/WAL) | No reportarlo como duración sin especificar la unidad de pérdida |
| $L_{p50}, L_{p95}, L_{p99}$ | Percentiles de latencia bajo carga | No reportar solo la latencia media |
| $O_i$ | Configuración de operador $i$ (CloudNativePG, Patroni) | No usar "operador" sin especificar cuál |

---

## Seminal References

<!-- Verificar contra Bibliography_base.bib antes de citar — son anclas sugeridas, no entradas confirmadas. -->

| Paper | Why It Matters |
|-------|---------------|
| Ongaro & Ousterhout (2014), "In Search of an Understandable Consensus Algorithm" (Raft) | Base de consenso/elección de líder que subyace a la mayoría de los operadores HA de PostgreSQL |
| Kubernetes CSI Specification | Define el contrato de attach/detach de almacenamiento que este paper analiza en la capa de operador |
| Documentación/diseño de Zalando Patroni | La plantilla HA basada en consenso de la que descienden CloudNativePG y Patroni |

---

## Theoretical Foundational References

N/A — no se planea una sección de teoría formal. Si se añadiera, anclar a modelos de fallo de sistemas distribuidos (crash-stop, crash-recovery) y teoría de protocolos de consenso (Raft/Paxos), no a teoría econométrica.

---

## Paper Author Team

| Author | Foundational on |
|--------|----------------|
| Angel A. Parejo R. (autor único) | N/A — sin contribuciones fundacionales previas conocidas en el área; no aplica moderación de tono por autoría |

---

## Field-Specific Referee Concerns

- **Limitación conocida (a) — homogeneidad del almacenamiento:** todos los experimentos se ejecutan sobre almacenamiento SAN/Fibre-Channel homogéneo. No hay contraste empírico frente a almacenamiento local (NVMe) o distribuido en red (p. ej., Ceph, NFS). La validez externa está limitada a entornos FC-SAN; declararlo explícitamente en el paper antes de que un referí lo señale.
- **Limitación conocida (b) — aproximación del fallo de nodo:** el fallo de nodo se aproxima mediante inyección sostenida de pod-failure. Esto no reproduce el desalojo real del nodo, las transiciones kubelet node-not-ready, ni el ciclo de detach/attach del CSI que un fallo real de nodo activaría — la latencia de recuperación atribuible al reenganche del almacenamiento puede estar subestimada.
- "¿Por qué no incluir un tercer operador (p. ej., Crunchy PGO, StackGres)?" — estar preparado para justificar el alcance de dos operadores.
- Poder estadístico con n pequeño — las pruebas no paramétricas son apropiadas, pero los referís pueden cuestionar si n es suficiente y si se reportan intervalos de confianza.
- Reproducibilidad/generalización entre proveedores cloud, distribuciones de Kubernetes y proveedores de CSI más allá del probado.

---

## Quality Tolerance Thresholds

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Precisión de medición del RTO | ± 1s (según resolución de la herramienta) | Granularidad de timestamp de Chaos Mesh / kubectl |
| Precisión de medición del RPO | ± 1 transacción / registro WAL | Limitado por el intervalo de muestreo del lag de replicación |
| Repeticiones del experimento (n por condición) | Reportar el n real; justificar suficiencia para la prueba no paramétrica usada | Distribuciones pequeñas y no normales — sin atajos de normalidad asintótica |
| Pruebas estadísticas | Solo Mann-Whitney U, Kruskal-Wallis, Spearman | Coincide con datos no normales y n pequeño; sin inferencia causal/paramétrica |
