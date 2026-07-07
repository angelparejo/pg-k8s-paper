
## 2026-07-06 — Ejecución piloto Fase B, Ventana 1: FASE 2 COMPLETA (Chaos Mesh v2.8.3)

**Modo:** DESACOPLADO (Claude genera kubectl; usuario ejecuta por VPN desde TCOLP292, dir `paquete-ejecucion-fase-b/`).

**Operations:**
- Render offline `helm template chaos-mesh ./chaos-mesh-2.8.3.tgz --include-crds -f values-airgapped.yaml` → `chaos-mesh-rendered.yaml`.
- Inspección de confinamiento (solo lectura): inventario de kinds, objetos cluster-scoped, flags de alcance, nodeSelector, webhooks, imágenes.
- Re-render con `--set-string 'controllerManager.nodeSelector.pg-chaos-lab/member=true'` tras detectar que faltaba el nodeSelector del controller.
- Pre-flight de tabla rasa (0 CRDs/webhooks/CR/pods de chaos-mesh).
- ⚠️ `kubectl apply --server-side -f chaos-mesh-rendered.yaml` (única mutación de la fase).

**Decisions:**
- La copia de `values-airgapped.yaml` en TCOLP292 era anterior al commit `219e2dc` → sin `controllerManager.nodeSelector`. Corregido vía `--set-string` en el render (no se editó el archivo en el host); el chart 2.8.3 sí soporta la clave (`controller-manager-deployment.yaml:214`). `--set-string` para forzar cadena "true" (nodeSelector es map[string]string).
- `--server-side` en el apply: los CRDs grandes de Chaos Mesh rompen el apply client-side por el límite de anotación last-applied.
- Webhooks aprobados sin `namespaceSelector`: todas las reglas son `apiGroups: chaos-mesh.org` (incluido `validation-auth` con `resources:["*"]` acotado a ese grupo); no interceptan pods/core → sin dependencia de admisión sobre producción. Confinamiento por `CLUSTER_SCOPED=false` + `ENABLE_FILTER_NAMESPACE=true` + RBAC namespaced.

**Results:**
- 23 CRDs establecidas; RBAC + 3 webhooks cluster-scoped creados; controller + daemon confinados.
- `chaos-controller-manager` y `chaos-daemon` **1/1 Running, ambos en tcolp293**; daemon único (1 nodo del lab); endpoints del controller poblados (`:10250,:10081,:10080`); rollout OK.
- FASE 2 = PASA.

**Status:**
- Done: Fases 0, 1 y 2 de la Ventana 1 ejecutadas y verificadas en el clúster real.
- Pending: Fase 3 (clúster experimental `pglab-cnpg-exp` + carga/verificador), Fase 4 GO/NO-GO (obligatoria), Fase 5 (F1+F3). Decisión de alcance de operadores sigue abierta.

## 2026-07-07 — Fase B Ventana 1: FASE 3 completa + FASE 4 (GO/NO-GO) en curso + FIX crashloop del controller Chaos Mesh

**Modo:** DESACOPLADO (usuario ejecuta por VPN desde TCOLP292).

**Operations:**
- FASE 3: creado `pglab-cnpg-exp` (3 instancias healthy en tcolp293, 3 PVCs Bound 15Gi huawei-ch-xfs); desplegados pgbench + tx-verifier; `pgbench -i -s 10` (1M filas); pgbench en régimen (tps≈478, 0 fallidas), verificador con COMMITs crecientes. PASA.
- FASE 4 PASO A (12/12 PASA): G1.1-G1.5, G2.1-G2.3, G4, G5, G7, G8. G1.2 (dry-run autoritativo) confirma que los 6 manifiestos resuelven a 1 solo pod (pglab-cnpg-exp-1) en pg-chaos-lab.
- Recuperación de archivos que no se copiaron a TCOLP292: recreado `manifiestos/scripts/dry-run-selectores.py` (ASCII heredoc, base64 falló por corrupción de pegado); `estado-inicial.txt` reubicado al dir del paquete.
- FIX del webhook/crashloop (ver Decisions).

**Decisions:**
- **Causa raíz del crashloop del controller:** en `clusterScoped:false`, los controladores `remotecluster` y `physicalmachine` intentan list/watch de CRDs cluster-scoped (`remoteclusters`, `physicalmachines`) sin RBAC → `forbidden at the cluster scope` → cache sync timeout → manager aborta → CrashLoopBackOff (16 reinicios). El webhook `mpodchaos` (failurePolicy:Fail) dependía del controller, así que toda creación de *Chaos daba `context deadline exceeded`.
- **Fix elegido:** acotar `controllerManager.enabledControllers: [podchaos, iochaos]` (los únicos que usan los experimentos; F3 es NetworkPolicy nativa). Preferido sobre conceder RBAC cluster-scoped: mantiene la narrativa de contención y reduce footprint. Repo `values-airgapped.yaml` actualizado.
- `kubectl apply --server-side` para instalar (evita límite de anotación de CRDs grandes). `enabledControllers` se cablea como env `ENABLED_CONTROLLERS` en el Deployment del controller.

**Results:**
- Tras el fix: controller `1/1 Running`, 0 reinicios, líder adquirido, `ENABLED_CONTROLLERS=podchaos,iochaos`, sin `forbidden`, endpoints poblados. Webhook operativo.
- Pendiente inmediato: re-test G3, G6, G9 → veredicto GO → Fase 5.

**Status:**
- Done: Fase 3; Fase 4 Paso A (12/12); fix del controller Chaos Mesh.
- Pending: G3/G6/G9, veredicto GO, Fase 5 (F1+F3). Falta commitear los cambios del repo (values-airgapped.yaml enabledControllers). Decisión de alcance de operadores sigue abierta.

## 2026-07-07 — CIERRE Ventana 1 día 1: F1 pod-kill VALIDADO end-to-end; pausa antes de las 10 reps

**Resultado principal:** F1 (pod-kill del primario) validado de punta a punta en el clúster real. Mató `pglab-cnpg-exp-1`, CNPG promovió `pglab-cnpg-exp-2` (failover real), **4 clústeres preexistentes intactos**. RTO del canario = **7.99 s** (gap del verificador). Compuerta GO/NO-GO: **GO** (G1–G9 en PASA).

**Los 3 fixes de Chaos Mesh (modo clusterScoped:false) — resueltos y en el repo:**
1. CrashLoopBackOff por informers de CRDs cluster-scoped (`remoteclusters`, `physicalmachines`) sin RBAC → ClusterRole de solo-lectura `chaos-mesh-lab-clusterscoped-read` (`11-rbac-clusterscoped-read.yaml`). (Intento previo `enabledControllers:[podchaos,iochaos]` DESCARTADO: desactivaba TODOS los reconcilers; se dejó `enabledControllers:["*"]`.)
2. Selección fallaba por `namespaces is forbidden at the cluster scope` → añadido `namespaces`+`services` (get/list/watch) al mismo ClusterRole.
3. `no pod is selected` / "namespace is not enabled" → `enableFilterNamespace` requiere el marcador como **ANNOTATION** `chaos-mesh.org/inject=enabled`, NO label. Corregido `01-namespace.yaml` (annotation) y G2.2 del checklist.

**Instrumentación de RTO (corregida):** la sonda activa de `run-experiment.sh` (kubectl exec ~1 s) es demasiado gruesa para el outage breve del failover (medía RTO≈0 y agotaba el guard de 120 s). **Decisión:** RTO/RPO se miden con el **gap del verificador** (~100 ms). `run-experiment.sh` reescrito a v3 (solo orquesta: inyecta → confirma failover por cambio de primario → recupera → limpia, con marcas de tiempo). `parse-verifier.py` mejorado: lista todos los gaps ≥1 s (= RTO por repetición) + RPO.

**Operaciones destacadas:**
- Chaos Mesh v2.8.3 instalado y confinado a tcolp293; clúster experimental + carga; GO/NO-GO completo (G1.2 dry-run: 6 manifiestos → 1 solo pod pglab-cnpg-exp-1).
- Recuperación de archivos no transferidos a TCOLP292 (scripts/) vía base64 en trozos + sha256 (MobaXterm suelta líneas en pegados grandes).

**Estado al cierre:** experimental healthy 3/3 (primario -2), sin experimentos activos, 4 preexistentes intactos. `results.csv` en TCOLP292 tiene ~3 filas espurias (intentos con la sonda vieja) — BORRAR mañana antes de las reps.

**Pendiente (mañana, Ventana 1 cont.):** copiar los archivos corregidos del repo al servidor; reescalar carga; 10 reps F1 con v3; diseñar y correr F3 (su NetworkPolicy sigue al primario dinámicamente → medición distinta); Fase 6 (RPO + análisis + diff vs estado-inicial.txt + teardown). Decisión de alcance de operadores (CNPG-solo vs 2) sigue abierta.

**Commits:** (este) documentación + fixes del paquete Fase B.
