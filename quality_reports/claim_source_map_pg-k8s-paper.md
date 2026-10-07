# Claim-Source Map — Piloto Fase B (CloudNativePG)

INV-22: cada cifra del manuscrito debe trazarse a una fuente (dato/script/output). Este mapa cubre
los resultados del piloto.

> **Aviso de procedencia (verificado el 2026-10-07).** `verifier-cnpg.log` y `results.csv` **nunca
> entraron en el repositorio** y ya no son recuperables: quedaron en el clúster productivo, cuyo
> acceso se cerró al concluir el piloto. Se rastrearon el árbol de trabajo, las ramas locales y
> remotas (243 revisiones) y las 808 rutas que han existido en todo el historial; no aparecen.
> Las entradas de este mapa que los citan como fuente documentan **cómo se obtuvo la cifra en su
> momento**, no una fuente auditable hoy. Lo auditable es `paper/faraute/replication/data/*.csv`
> más `truth_summary_cnpg.csv`.

Fuentes: `verifier-cnpg.log` (crudo, servidor, **no conservado**), `results.csv`
(marcas T0 por rep, servidor, **no conservado**), `data/cleaned/*.csv` (series limpias, repo). Scripts:
`manifiestos/scripts/parse-verifier.py` (RTO=gap entre COMMITs; RPO=ids no visibles en `truth`),
`analyze.py` (medianas/percentiles).

Estado: F1, F2 y F3 con datos completos; F4 sin cifras (bloqueo cualitativo).

**Precisión reportable (revisión de arbitraje, 2026-10-07).** La resolución del instrumento es
≈0,2 s, de modo que el manuscrito publica **una décima**. Las medianas exactas son F1 = 7,905 s
(→ **7,9 s**), F2 = 36,745 s (→ **36,7 s**) y F3 fija = 60,750 s (→ **60,8 s**). Redondear primero
a dos decimales y luego a una décima desplaza la cifra: 36,745 → 36,75 → 36,8 es **incorrecto**.
`analyze.py` imprime desde esta revisión el valor exacto y el reportable, para evitar la recaída.

| # | Afirmación (valor) | Fuente (archivo / columna) | Cómo se obtiene |
|---|---|---|---|
| C1 | F1 RTO mediana **7.905 s** (reportable **7,9 s**) | `data/cleaned/f1_rto_cnpg.csv` col `rto_s` (n=10) | `parse-verifier.py` (gap COMMITs) → mediana |
| C2 | F1 RTO media **7.69 s**, sd **0.54**, min **6.61**, max **8.17**, IQR **[7.62, 8.01]** | `data/cleaned/f1_rto_cnpg.csv` col `rto_s` | estadística sobre las 10 filas |
| C3 | F1 **failover 10/10** (primario alterna) | `f1_rto_cnpg.csv` cols `primary_before`≠`primary_after` | comparación por fila |
| C4 | F1 **RPO = 0** | `parse-verifier.py` (args RPO) sobre tabla `truth` | ids con COMMIT no presentes en `truth` = 0 |
| C5 | F3 **no promoción 0/12** | `data/cleaned/f3_partition_cnpg.csv` col `promocion`=no (12 filas) | `currentPrimary` invariable por rep |
| C6 | F3 outage ≈ **duración de la partición** (60 s → 60.75 s mediana; rango 60.73–60.78) | `f3_partition_cnpg.csv` cols `partition_dur_s`, `outage_s` (filas `fija`, n=10) | gap del verificador vs. duración inyectada |
| C7 | F3 pod **`Ready=True`** durante la partición | `f3_partition_cnpg.csv` col `pod_ready_durante` (sonda larga 300 s) | muestreo de `pod.status` |
| C8 | F3 **RPO = 0** (por construcción) | — | sin promoción ⇒ sin divergencia |
| C9 | F3 recuperación **< 1 s** al sanar | `f3_partition_cnpg.csv` (outage − partition_dur) | resto tras eliminar la NetworkPolicy |
| C10 | **F2 no promoción 0/10** (recreación en sitio) | `data/cleaned/f2_podfailure_cnpg.csv` col `promocion`=no (10 filas) | `currentPrimary`=exp-2 en las 10 reps |
| C11 | **F2 RTO mediana 36.745 s** (reportable **36,7 s**) (IQR ~[36.2,37.1], rango 35.5–38.3, n=10) | `f2_podfailure_cnpg.csv` col `rto_s` | gap del verificador atribuido por T0 (validación ~80 s excluida) |
| C12 | F2 **RPO = 0** (y RPO=0 global) | `truth`: filas=613253, min=1, max=613253, **faltantes=0**; 11/11 ids-frontera presentes | `kubectl exec` primario → `psql` in-cluster (contigüidad + IN de 11 ids) |
| C13 | F4 **no ejecutable** (hardening rootfs RO ↔ FUSE) | eventos PodIOChaos `Read-only file system (os error 30)`; `f4-VALIDACION-*.log` | validación 100 ms: latencia == baseline |

## Estadística derivada (añadida en la revisión adversarial 2026-07-07)

| # | Afirmación (valor) | Fuente / cómo se obtiene |
|---|---|---|
| C14 | Razón de medianas F2/F1 = **4.65×** (36.745/7.905) | derivada de C1/C11 |
| C15 | **Mann–Whitney F1 vs F2:** U=0, z=−3.78, **p≈1.6×10⁻⁴**, rank-biserial=**1.00** (separación completa) | `analyze.py`-equivalente sobre `f1_rto_cnpg.csv` y `f2_podfailure_cnpg.csv` (n=10 c/u) |
| C16 | **Hodges–Lehmann** (F2−F1) = **28.96 s** (diferencia de medianas robusta) | mediana de las diferencias pareadas de los dos conjuntos |
| C17 | IC de mediana (distribución-libre, estad. de orden [x(2),x(9)], cobertura ~97.9%): F1 **[6.85, 8.15]**, F2 **[36.05, 37.66]**, F3 fija **[60.74, 60.77]** | `data/cleaned/*.csv` |
| C18 | IC binomial (regla de tres, cota sup. 95% una cola): no-promoción **0/10 ⇒ ≤25.9%**, **0/12 ⇒ ≤22.1%** | 1−0.05^(1/n); la conclusión de no-promoción se apoya sobre todo en el **mecanismo** (recreación con misma identidad/PVC), no solo en el conteo |
| C19 | Replicación de CNPG **asíncrona** (sincronía no variada) | `paper/replication/.../manifiestos/20-cluster/cluster-cnpg.yaml` (sin config `synchronous`; comentario explícito) |
| C20 | Las **3 instancias co-residen en `nodo-lab-01`** (nodo único del lab; anti-afinidad `topologyKey=hostname` anulada por pool de un nodo) ⇒ failover intra-nodo | `cluster-cnpg.yaml` (affinity) + observación `kubectl get pods -o wide` (exp-1/2/3 en nodo-lab-01) |
| C21 | Verificador: id **BIGINT monótono de cliente**; reintenta el mismo id ante fallo (outages no crean huecos); cadencia bucle apretado + `sleep 0.2 s`/`PGCONNECT_TIMEOUT 2 s` ⇒ **granularidad RTO ≈0.2 s** | `paper/replication/.../manifiestos/30-workload/tx-verifier-cnpg.yaml` |
| C22 | **Mann–Whitney F1 vs F2 EXACTA bilateral: p ≈ 1.1×10⁻⁵** (U=0, n1=n2=10; = 2/C(20,10)) | cálculo exacto; z=−3.78/p≈1.6×10⁻⁴ era la aproximación normal (C15) |
| C23 | **Spearman(índice de repetición, RTO) en F2 = 0.62** (n=10; crítico ≈0.65 a α=0.05 ⇒ **no significativa**) → posible efecto de orden/calentamiento, no descartable | `data/cleaned/f2_podfailure_cnpg.csv` (cols `rep`,`rto_s`) |
| C24 | **Outlier de F2 excluido: primera inyección (validación) = 80.54 s @22:11 UTC** (depositado en `data/f2_podfailure_cnpg_excluida.csv`) — excluido del lote n=10; efecto de primera-inyección/arranque en frío | `f4-VALIDACION-*.log`/`verifier-cnpg.log`; ver [[project_pilot_execution_state]] |

**Notas de fiabilidad ligadas a cifras:** el id espurio negativo en `truth` (ts 04:56 UTC, previo a
las ventanas) NO cuenta como RPO (ver results_summary § Nota de fiabilidad). Para F2, el RTO **no** es
la columna `rto` de `results.csv` (esa es t1−t0≈120 s del poll sin failover); es el gap del verificador.


## Afirmaciones añadidas en la revisión de arbitraje (2026-10-07)

| # | Afirmación (valor) | Fuente / cómo se obtiene |
|---|---|---|
| C25 | **F2 mediana con la inyección descartada = 36,920 s** (reportable **36,9 s**, n=11) | `analyze.py` sobre `f2_podfailure_cnpg.csv` + `f2_podfailure_cnpg_excluida.csv` |
| C26 | **Bloques horarios**: F1 de 13:54:35 a 14:21:16 UTC (cadencia ≈2,5 min); F2 de 22:22:52 a 23:03:20 UTC (cadencia ≈4,5 min) | col `injection_utc` de `f1_rto_cnpg.csv` y `f2_podfailure_cnpg.csv` |
| C27 | **La imagen de pausa no estaba precargada** en el entorno air-gapped | `execution-package/manifiestos/images/image-list.txt`: lista cinco imágenes, ninguna de pausa |
| C28 | **`primaryUpdateStrategy: unsupervised`**, sin `failoverDelay` ni `primaryUpdateMethod` explícitos (rigen los valores por defecto: 0 s y reinicio) | `manifiestos/20-cluster/cluster-cnpg.yaml:14` |
| C29 | **F1 sin `gracePeriod` explícito** ⇒ valor por defecto de Chaos Mesh (terminación abrupta) | `manifiestos/40-experiments/f1-podkill-cnpg.yaml` |
| C30 | **Antiafinidad preferente**, no obligatoria: el manifiesto fija `topologyKey` y CNPG aplica `preferred` por defecto | `manifiestos/20-cluster/cluster-cnpg.yaml:49-53` |
| C31 | **Tabla de verdad**: 613 253 filas, min 1, max 613 253, faltantes 0, 11/11 ids-frontera presentes ⇒ RPO = 0 | **depositado** en `data/truth_summary_cnpg.csv` (antes solo en prosa) |
| C32 | **Un id espurio negativo descartado** (ts 04:56 UTC, fuera de toda ventana de inyección) | `truth_summary_cnpg.csv` col `ids_espurios_descartados`; declarar en el manuscrito |
| C33 | **Evento del operador en F1**: «Current primary isn't healthy, initiating a failover», observado durante la ejecución | `quality_reports/results_summary.md:101`. **El flujo completo de eventos no se conservó**: la cita documenta el disparador observado, no una traza recuperable |
