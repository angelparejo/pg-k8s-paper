# Claim-Source Map — Piloto Fase B (CloudNativePG)

INV-22: cada cifra del manuscrito debe trazarse a una fuente (dato/script/output). Este mapa cubre
los resultados del piloto. Fuentes: `verifier-cnpg.log` (crudo, servidor, gitignored), `results.csv`
(marcas T0 por rep, servidor), `data/cleaned/*.csv` (series limpias, repo). Scripts:
`manifiestos/scripts/parse-verifier.py` (RTO=gap entre COMMITs; RPO=ids no visibles en `truth`),
`analyze.py` (medianas/percentiles).

Estado: F1 y F3 con datos; **F2 pendiente del lote n=10**; F4 sin cifras (bloqueo cualitativo).

| # | Afirmación (valor) | Fuente (archivo / columna) | Cómo se obtiene |
|---|---|---|---|
| C1 | F1 RTO mediana **7.91 s** | `data/cleaned/f1_rto_cnpg.csv` col `rto_s` (n=10) | `parse-verifier.py` (gap COMMITs) → mediana |
| C2 | F1 RTO media **7.69 s**, sd **0.54**, min **6.61**, max **8.17** | `data/cleaned/f1_rto_cnpg.csv` col `rto_s` | estadística sobre las 10 filas |
| C3 | F1 **failover 10/10** (primario alterna) | `f1_rto_cnpg.csv` cols `primary_before`≠`primary_after` | comparación por fila |
| C4 | F1 **RPO = 0** | `parse-verifier.py` (args RPO) sobre tabla `truth` | ids con COMMIT no presentes en `truth` = 0 |
| C5 | F3 **no promoción 0/12** | `data/cleaned/f3_partition_cnpg.csv` col `promocion`=no (12 filas) | `currentPrimary` invariable por rep |
| C6 | F3 outage ≈ **duración de la partición** (60 s → 60.74 s) | `f3_partition_cnpg.csv` cols `partition_dur_s`, `outage_s` | gap del verificador vs. duración inyectada |
| C7 | F3 pod **`Ready=True`** durante la partición | `f3_partition_cnpg.csv` col `pod_ready_durante` (sonda larga 300 s) | muestreo de `pod.status` |
| C8 | F3 **RPO = 0** (por construcción) | — | sin promoción ⇒ sin divergencia |
| C9 | F3 recuperación **< 1 s** al sanar | `f3_partition_cnpg.csv` (outage − partition_dur) | resto tras eliminar la NetworkPolicy |
| C10 | **F2 no promoción 0/10** (recreación en sitio) | `data/cleaned/f2_podfailure_cnpg.csv` col `promocion`=no (10 filas) | `currentPrimary`=exp-2 en las 10 reps |
| C11 | **F2 RTO mediana 36.75 s** (IQR ~[36.2,37.1], rango 35.5–38.3, n=10) | `f2_podfailure_cnpg.csv` col `rto_s` | gap del verificador atribuido por T0 (validación ~80 s excluida) |
| C12 | F2 **RPO = 0** (y RPO=0 global) | `truth`: filas=613253, min=1, max=613253, **faltantes=0**; 11/11 ids-frontera presentes | `kubectl exec` primario → `psql` in-cluster (contigüidad + IN de 11 ids) |
| C13 | F4 **no ejecutable** (hardening rootfs RO ↔ FUSE) | eventos PodIOChaos `Read-only file system (os error 30)`; `f4-VALIDACION-*.log` | validación 100 ms: latencia == baseline |

**Notas de fiabilidad ligadas a cifras:** el id espurio negativo en `truth` (ts 04:56 UTC, previo a
las ventanas) NO cuenta como RPO (ver results_summary § Nota de fiabilidad). Para F2, el RTO **no** es
la columna `rto` de `results.csv` (esa es t1−t0≈120 s del poll sin failover); es el gap del verificador.
