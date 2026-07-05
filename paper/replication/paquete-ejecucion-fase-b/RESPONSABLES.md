# RESPONSABLES — Roles, autoridad de aborto e inventario productivo

Rellenar **antes** de agendar la primera ventana. Es requisito del GO/NO-GO (ítem G9).

## Roles

| Rol | Nombre | Contacto | Responsabilidad |
|---|---|---|---|
| **Aprobador del change** | | | Aprueba la ventana y el alcance (solo `pg-chaos-lab`) |
| **Ejecutor** | | | Ejecuta el `PROCEDIMIENTO.md` paso a paso |
| **Monitor de producción** | | | Vigila los **4 clústeres CNPG preexistentes** durante toda la ventana |
| **Autoridad de aborto** | | | Puede detener el piloto en cualquier momento (ver `ABORTO.md`) |
| **DBA de producción (guardia)** | | | Punto de escalado ante cualquier anomalía en producción |
| **Responsable de almacenamiento (SAN)** | | | Coordina pool/QoS del lab y el borrado final de PVCs |
| **Responsable de plataforma / K8s** | | | Etiquetado de nodos, Chaos Mesh, plano de control |

> La **autoridad de aborto** debe estar presente o localizable durante toda cada ventana. No se inyecta sin ella.

## Inventario de los cuatro clústeres CNPG preexistentes (paso 0.7 — NO tocar)

Prellenado con el reconocimiento del **2026-07-05**. **Reconfirmar en el paso 0.7/0.9** — la ubicación por nodo puede cambiar (el operador reprograma pods):

| # | Nombre del clúster | Namespace | Nº instancias | Nodos (primario/réplicas) — al 2026-07-05 | Estado inicial |
|---|---|---|---|---|---|
| 1 | pg-prod | pg-prod | 3 | primario **pg-prod-2** (tcolp295); réplicas pg-prod-1 (tcolp296), pg-prod-3 (tcolp300) | healthy 3/3 |
| 2 | pg-cert | pg-cert | 2 | primario **pg-cert-1** (tcolp293 ⚠️ nodo del lab); réplica pg-cert-2 (tcolp300) | healthy 2/2 |
| 3 | pg-dev | pg-dev | 2 | primario **pg-dev-3** (tcolp293 ⚠️ nodo del lab); réplica pg-dev-1 (tcolp296) | healthy 2/2 |
| 4 | pg-gitlab | gitlab | 2 | primario **pg-gitlab-2** (tcolp293 ⚠️ nodo del lab); réplica pg-gitlab-1 (tcolp300) | healthy 2/2 |

> ⚠️ **Co-tenencia conocida:** 3 primarios preexistentes (pg-cert-1, pg-dev-3, pg-gitlab-2) co-residen en `tcolp293`, el nodo del lab. Aceptado: la protección es G1 (ningún manifiesto los selecciona), no el aislamiento de nodo. El primario de producción `pg-prod-2` **no** está en tcolp293.

- [ ] Ninguno se llama `pglab-cnpg-exp`.
- [ ] Ninguno está en el namespace `pg-chaos-lab`.
- [ ] Ninguno es objetivo de ningún manifiesto de fallo (garantizado por G1 — la co-tenencia de 3 primarios en tcolp293 es conocida y no compromete el aislamiento).
- [ ] `estado-inicial.txt` (paso 0.9) capturado y archivado.

## Parámetros del entorno (Fase 0 — ya resueltos 2026-07-05)

| Parámetro | Valor |
|---|---|
| Namespace del operador CNPG | `cnpg-operator` (deploy `cnpg-cloudnative-pg`, 1.28.0) |
| StorageClass del CSI Huawei | `huawei-ch-xfs` (default · `csi.huawei.com` · `reclaimPolicy: Retain` · `WaitForFirstConsumer`) |
| Nodo del laboratorio | `tcolp293` (`storage=huawei-san`, `fc=true`) |
| Entorno verificado | Kubernetes v1.34.6 · RHEL 9.8 · kernel 5.14 · containerd 2.2.4 · Chaos Mesh v2.8.3 |
| Contexto de `kubectl` | _(rellenar el ejecutor en su sesión)_ |

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

- [ ] Fase 6.3: diff `estado-inicial.txt` vs. `estado-final.txt` revisado — los 4 clústeres preexistentes **iguales** a la línea base.
- [ ] Evidencia archivada: `results.csv`, `verifier-cnpg.log`, `events-lab.log`, `estado-inicial.txt`, `estado-final.txt`.
- [ ] Laboratorio desmontado y PVCs borrados (coordinado con almacenamiento).
- [ ] **PersistentVolumes liberados borrados** — la SC `huawei-ch-xfs` usa `reclaimPolicy: Retain`, así que los PV **no** se borran al eliminar los PVCs/namespace: hay que borrarlos a mano (`kubectl get pv | grep pg-chaos-lab` → `kubectl delete pv <...>`), coordinado con almacenamiento.
- [ ] Firma del aprobador del change: __________
