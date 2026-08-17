# Diccionario de datos

Tres CSV con los resultados limpios de la Fase 1 (CloudNativePG). Codificación UTF-8,
separador coma, encabezado en la primera fila. Tiempos en segundos; marcas de tiempo en UTC (ISO 8601).

## `data/f1_rto_cnpg.csv` — F1 (pod-kill), n=10
| Columna | Tipo | Descripción |
|---|---|---|
| `rep` | entero | Índice de repetición (1–10) |
| `rto_s` | real | RTO: hueco entre el último COMMIT reconocido antes del fallo y el primero tras la recuperación (s) |
| `primary_before` | texto | Pod primario antes de la inyección |
| `primary_after` | texto | Pod primario tras el failover (promovido) |
| `injection_utc` | ISO 8601 | Instante de la inyección (UTC) |

## `data/f2_podfailure_cnpg.csv` — F2 (pod-failure), n=10
| Columna | Tipo | Descripción |
|---|---|---|
| `rep` | entero | Índice de repetición (1–10) |
| `rto_s` | real | Ventana de indisponibilidad de escritura (s) |
| `promocion` | texto | ¿Promovió una réplica? (`no` en las 10 repeticiones) |
| `primary_before` / `primary_after` | texto | Pod primario antes/después (idéntico: recreación in situ) |
| `injection_utc` | ISO 8601 | Instante de la inyección (UTC) |

## `data/f3_partition_cnpg.csv` — F3 (partición de red), 12 inyecciones
| Columna | Tipo | Descripción |
|---|---|---|
| `tipo` | texto | `fija` (10, 60 s, usadas en el RTO), `exploratoria` (149 s) o `sonda_larga` (300 s) — las dos últimas excluidas del cálculo del RTO |
| `rep` | entero | Índice dentro del tipo |
| `partition_dur_s` | real | Duración inyectada de la partición (s) |
| `outage_s` | real | Indisponibilidad de escritura observada (s) |
| `promocion` | texto | ¿Promovió? (`no` en las 12) |
| `pod_ready_durante` | texto | ¿El pod aislado permaneció `Ready` durante la partición? |
| `primary_before` / `primary_after` | texto | Pod primario antes/después (idéntico: sin promoción) |
| `injection_utc` | ISO 8601 | Instante de la inyección (UTC) |

## Notas
- **RPO:** no aparece como columna porque fue **0 en todos los escenarios** (tabla de verdad
  del verificador contigua, ids 1–613 253 sin huecos). El RPO se deriva de los registros del
  `tx-verifier`; los CSV resumen el RTO/indisponibilidad y la promoción.
- **Exclusiones** (declaradas en el artículo y el suplemento): 1.ª inyección de F2 (~80,5 s,
  arranque en frío), las 2 inyecciones exploratorias de F3, y un identificador espurio negativo.
  Los CSV contienen ya el conjunto analizado; el suplemento incluye el análisis de sensibilidad.
- Reproducir todas las cifras: `python3 execution-package/manifiestos/scripts/analyze.py`
