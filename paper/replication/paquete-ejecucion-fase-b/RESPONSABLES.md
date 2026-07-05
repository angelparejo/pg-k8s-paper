# RESPONSABLES — Roles, autoridad de aborto e inventario productivo

Rellenar **antes** de agendar la primera ventana. Es requisito del GO/NO-GO (ítem G9).

## Roles

| Rol | Nombre | Contacto | Responsabilidad |
|---|---|---|---|
| **Aprobador del change** | | | Aprueba la ventana y el alcance (solo `pg-chaos-lab`) |
| **Ejecutor** | | | Ejecuta el `PROCEDIMIENTO.md` paso a paso |
| **Monitor de producción** | | | Vigila los **3 clústeres productivos** durante toda la ventana |
| **Autoridad de aborto** | | | Puede detener el piloto en cualquier momento (ver `ABORTO.md`) |
| **DBA de producción (guardia)** | | | Punto de escalado ante cualquier anomalía en producción |
| **Responsable de almacenamiento (SAN)** | | | Coordina pool/QoS del lab y el borrado final de PVCs |
| **Responsable de plataforma / K8s** | | | Etiquetado de nodos, Chaos Mesh, plano de control |

> La **autoridad de aborto** debe estar presente o localizable durante toda cada ventana. No se inyecta sin ella.

## Inventario de los tres clústeres CNPG productivos (paso 0.7 — NO tocar)

Rellenar con la salida de `kubectl get clusters.postgresql.cnpg.io -A`:

| # | Nombre del clúster | Namespace | Nº instancias | Nodos (primario/réplicas) | Estado inicial |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

- [ ] Ninguno se llama `pglab-cnpg-exp`.
- [ ] Ninguno está en el namespace `pg-chaos-lab`.
- [ ] Ninguno tiene su primario en un nodo `pg-chaos-lab/member=true`.
- [ ] `estado-inicial.txt` (paso 0.9) capturado y archivado.

## Parámetros del entorno (Fase 0)

| Parámetro | Valor |
|---|---|
| `<NS-OPERADOR>` (namespace del operador CNPG) | |
| `<SC-HUAWEI>` (StorageClass del CSI Huawei) | |
| `<WORKER-LAB>` (nodos del laboratorio) | |
| Contexto de `kubectl` | |

## Planificación de ventanas

| Ventana | Contenido | Fecha/hora prevista | Duración estimada | Ejecutor | Autoridad de aborto |
|---|---|---|---|---|---|
| **1** | Fases 0–4 + F1 + F3 | | ~4 h | | |
| **2** | F4 (20/50/100 ms) | | ~7 h | | |
| **3** | F2 (pod-failure) | | ~2.5 h | | |

## Hoja de registro de la ventana (una por ventana)

| Campo | Ventana 1 | Ventana 2 | Ventana 3 |
|---|---|---|---|
| Fecha/hora inicio (UTC) | | | |
| GO/NO-GO (veredicto + firma) | | | |
| Reanudación R1–R6 en verde (V2/V3) | n/a | | |
| Experimentos completados (n) | | | |
| Incidencias / abortos | | | |
| Estado de producción al cerrar | | | |
| Fecha/hora fin (UTC) | | | |

## Cierre del piloto

- [ ] Fase 6.3: diff `estado-inicial.txt` vs. `estado-final.txt` revisado — los 3 clústeres productivos **iguales** a la línea base.
- [ ] Evidencia archivada: `results.csv`, `verifier-cnpg.log`, `events-lab.log`, `estado-inicial.txt`, `estado-final.txt`.
- [ ] Laboratorio desmontado y PVCs borrados (coordinado con almacenamiento).
- [ ] Firma del aprobador del change: __________
