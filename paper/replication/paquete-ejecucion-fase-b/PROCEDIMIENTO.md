# PROCEDIMIENTO — Piloto Fase B (solo CloudNativePG) · pg-chaos-lab

**Audiencia:** equipo ejecutor (puede no conocer el contexto de la investigación).
**Regla de oro:** este piloto crea **un quinto clúster CNPG nuevo y aislado** (`pglab-cnpg-exp`) gestionado por el operador CNPG **ya instalado y compartido**. Los **cuatro clústeres CNPG preexistentes NO se tocan** (`pg-prod`, `pg-cert`, `pg-dev`, `gitlab/pg-gitlab`). Toda inyección de fallos está acotada por **doble filtro: namespace `pg-chaos-lab` + nombre de clúster `pglab-cnpg-exp`**.

**Qué hace / qué NO hace:**
- ✅ Crea `pglab-cnpg-exp` en el namespace nuevo `pg-chaos-lab`, le mete carga e inyecta fallos **solo a él**.
- ❌ NO instala ni actualiza ningún operador. NO drena/acordona nodos. NO toca la SAN Huawei (IOChaos es FUSE dentro del pod). NO toca los cuatro clústeres CNPG preexistentes.

**Orden estricto:** Fase 0 → 1 → 2 → 3 → **4 (GO/NO-GO, obligatoria)** → 5 → 6. No se salta ninguna fase.

**Documentos hermanos (leer antes de ejecutar):** `SEGURIDAD.md`, `CHECKLIST-GONOGO.md`, `ABORTO.md`, `RESPONSABLES.md`.

**Parámetros de este piloto (ya resueltos contra el clúster real; verificados 2026-07-05):**
| Parámetro | Valor |
|---|---|
| Namespace del operador CNPG | `cnpg-operator` (deploy `cnpg-cloudnative-pg`, imagen `...cloudnative-pg:1.28.0`) |
| StorageClass del CSI Huawei | `huawei-ch-xfs` (default · `csi.huawei.com` · `reclaimPolicy: Retain` · `WaitForFirstConsumer`) |
| Nodo del laboratorio | `tcolp293` (worker con `storage=huawei-san`, `fc=true`) |
| Entorno verificado | Kubernetes v1.34.6 · RHEL 9.8 · kernel 5.14 · containerd 2.2.4 |

> ⚠️ `tcolp293` **co-aloja hoy 3 primaries CNPG ajenos** (pg-cert-1, pg-dev-3, pg-gitlab-2), además de ArgoCD/Harbor/Prometheus. El aislamiento del piloto **no** depende de que el nodo esté vacío, sino del filtro de namespace + doble selector + nombre único + dry-run G1 (ver `SEGURIDAD.md` y `CHECKLIST-GONOGO.md` G1/G5).
> Todos los comandos asumen `kubectl` con el contexto correcto. Verificar: `kubectl config current-context`.

---

## PLANIFICACIÓN DE VENTANAS (leer antes de agendar el change)

El piloto completo son **~12–14 h** de ejecución efectiva. No cabe en una sola ventana de mantenimiento porque **F2** (`pod-failure`, 10 min/inyección) y **F4** (`IOChaos`, 10 min/inyección) son largas. Se fracciona en **tres ventanas**. El laboratorio **se deja desplegado entre ventanas** (no se desmonta ni se vuelve a montar).

### Estimación de tiempos por fase

| Bloque | Detalle | Tiempo estimado |
|---|---|---|
| Fases 0–4 (setup + GO/NO-GO) | prerrequisitos, snapshot, aislamiento, Chaos Mesh, clúster, compuerta | ~2–2.5 h |
| F1 (`pod-kill`) | 10 rep × (~1 min recuperación + 120 s cool-down) | ~40 min |
| F3 (partición Calico) | 10 rep × (~1 min + 120 s) | ~40 min |
| F4 (`IOChaos` 0/20/50/100 ms, Opción A) | 4 niveles × 5 corridas × (5 min + 30 s) | ~2 h |
| F2 (`pod-failure` 10 min) | 10 rep × (10 min inyección + recuperación + 120 s) | ~2–2.5 h |

### Fraccionamiento propuesto

| Ventana | Contenido | Duración |
|---|---|---|
| **Ventana 1** | Fases 0–4 (setup + GO/NO-GO) **+ F1 + F3** | **~4 h** |
| **Ventana 2** | **F4** (0/20/50/100 ms, Opción A) | **~2 h** |
| **Ventana 3** | **F2** (sustituto de fallo de nodo) | **~2.5 h** |

> El orden V1→V2→V3 es deliberado: Ventana 1 deja el laboratorio montado y **validado** (GO/NO-GO superado) con los dos experimentos de menor riesgo ya hechos; V2 y V3 solo añaden inyecciones sobre esa base ya probada.

### Qué se deja desplegado entre ventanas

- **SE CONSERVA:** namespace `pg-chaos-lab`, Chaos Mesh (acotado), el clúster `pglab-cnpg-exp` (3/3), el `tx-verifier-cnpg` (para no perder continuidad del registro de verdad) y el archivo local `results.csv` (acumula todas las repeticiones de todas las ventanas — **no borrar ni rotar**).
- **OPCIONAL (reducir huella entre ventanas):** escalar la carga pgbench a cero para no cargar el clúster mientras nadie ejecuta:
  ```bash
  kubectl -n pg-chaos-lab scale deploy pgbench-cnpg --replicas=0     # al cerrar la ventana
  ```
  El `tx-verifier-cnpg` se deja **en marcha** (su carga es mínima y mantiene el log continuo; escalarlo a cero introduciría un hueco temporal que parse-verifier interpretaría como un RTO falso).
- **NO se borra** nada del laboratorio entre ventanas. El desmontaje total es solo al final (Fase 6).

### Reanudación al inicio de las Ventanas 2 y 3 (checklist de reentrada)

Antes de inyectar en una ventana posterior, ejecutar en orden:

- [ ] **R1.** Contexto correcto: `kubectl config current-context`.
- [ ] **R2.** Producción intacta vs. la línea base (mini-comparación del snapshot):
  ```bash
  kubectl get clusters.postgresql.cnpg.io -A          # -> siguen los 4 preexistentes, saludables
  kubectl get deploy -A -l app.kubernetes.io/name=cloudnative-pg -o wide   # operador sin cambios
  ```
  Confirmar contra `estado-inicial.txt` (paso 0.9): mismos 4 clústeres, mismos namespaces, operador igual. Si algo cambió en producción → **pausar y avisar al DBA** antes de continuar.
- [ ] **R3.** Aislamiento del laboratorio intacto:
  ```bash
  kubectl get pods -A -l app.kubernetes.io/instance=chaos-mesh -o wide     # solo en pg-chaos-lab
  kubectl -n pg-chaos-lab get pods -o wide | grep chaos-daemon             # solo en tcolp293
  kubectl get ns pg-chaos-lab --show-labels | grep chaos-mesh.org/inject   # label intacto
  kubectl -n pg-chaos-lab get resourcequota                                # cuota activa
  kubectl get nodes -l pg-chaos-lab/member=true                            # nodos del lab intactos
  ```
- [ ] **R4.** Clúster experimental sano y verificador vivo:
  ```bash
  kubectl -n pg-chaos-lab get cluster pglab-cnpg-exp        # healthy, 3/3
  kubectl -n pg-chaos-lab logs deploy/tx-verifier-cnpg --tail=3   # COMMITs recientes
  ```
- [ ] **R5.** Carga según la ventana:
  - **Ventana 2 (F4):** NO hace falta la carga de fondo `pgbench-cnpg`; desplegar el runner ocioso:
    ```bash
    kubectl apply -f manifiestos/30-workload/pgbench-runner-cnpg.yaml
    kubectl -n pg-chaos-lab rollout status deploy/pgbench-runner-cnpg --timeout=90s
    ```
  - **Ventana 3 (F2):** restaurar la carga de fondo si se escaló a cero:
    ```bash
    kubectl -n pg-chaos-lab scale deploy pgbench-cnpg --replicas=1
    ```
  - El `tx-verifier-cnpg` debe seguir corriendo en ambas (log continuo de RTO/RPO).
- [ ] **R6.** **Re-ejecutar el dry-run de selectores de CHECKLIST-GONOGO.md** (los nombres de pod y el primario pueden haber cambiado entre ventanas): confirmar que cada selector de la ventana en curso resuelve **solo** a pods de `pglab-cnpg-exp`. Si algo no resuelve como se espera → **abortar** (`ABORTO.md`).

Solo con R1–R6 en verde se procede a inyectar en la ventana.

---

## FASE 0 — Prerrequisitos (verificación; NO cambia nada)

**0.1 Versión de Kubernetes**
```bash
kubectl version -o yaml | grep -A3 serverVersion
```
- Esperado: `gitVersion: v1.34.6`.
- Si difiere: **detener**. El kit está validado para 1.34.6; escalar al responsable de la investigación.
- [ ] PASA

**0.2 El operador CNPG 1.28.0 YA existe (namespace `cnpg-operator`)**
```bash
kubectl get deploy -A -l app.kubernetes.io/name=cloudnative-pg -o wide
```
- Esperado: un Deployment `READY 2/2` en el namespace `cnpg-operator` (deploy `cnpg-cloudnative-pg`) con imagen `...cloudnative-pg:1.28.0`.
- Si no aparece: **detener y escalar**. Camino B **prohíbe instalar operadores**.
- [ ] PASA — operador presente en `cnpg-operator`

**0.3 Confirmar tag exacto del operador**
```bash
kubectl -n cnpg-operator get deploy -l app.kubernetes.io/name=cloudnative-pg \
  -o jsonpath='{.items[*].spec.template.spec.containers[*].image}{"\n"}'
```
- Esperado: termina en `:1.28.0`.
- Si es otra versión: detener y escalar (no actualizar).
- [ ] PASA

**0.4 Calico 3.31.4 presente**
```bash
kubectl get clusterinformation default -o jsonpath='{.spec.calicoVersion}{"\n"}' 2>/dev/null \
  || kubectl get ds -A -l k8s-app=calico-node -o jsonpath='{.items[*].spec.template.spec.containers[*].image}{"\n"}'
```
- Esperado: `v3.31.4` (o imagen `calico/node:v3.31.4`). F3 usa NetworkPolicy aplicada por Calico.
- Si difiere: registrar la versión real y consultar con el responsable antes de F3.
- [ ] PASA

**0.5 Nodo del laboratorio etiquetado (`tcolp293`)**
```bash
kubectl get nodes -l pg-chaos-lab/member=true
kubectl get pods -A -o wide --field-selector spec.nodeName=tcolp293 | grep -v pg-chaos-lab
```
- Esperado: `tcolp293` etiquetado. La segunda orden **sí** listará cargas ajenas: `tcolp293` es el worker nonprod designado y **co-aloja 3 primaries CNPG** (pg-cert-1, pg-dev-3, pg-gitlab-2) además de ArgoCD/Harbor/Prometheus. **Esto es esperado y aceptado**: el aislamiento del piloto NO depende de que el nodo esté vacío (ver `SEGURIDAD.md` barrera 2 y `CHECKLIST-GONOGO.md` G5), sino del filtro de namespace + doble selector + nombre único + dry-run G1. Los escenarios son estrictamente pod-scoped (F1/F2 `pod-failure`, F4 IOChaos-FUSE); no se ejecuta ningún fallo de nodo ni StressChaos que pudiera alcanzar a los vecinos.
- Si el nodo no está etiquetado: etiquetar (con visto bueno) `kubectl label node tcolp293 pg-chaos-lab/member=true`.
- [ ] PASA — nodo del lab = `tcolp293`

**0.6 Imágenes importadas en CADA nodo del lab** (ejecutar en el nodo, no en kubectl)
```bash
sudo ctr -n k8s.io images ls | grep -E 'cloudnative-pg/postgresql:16.13'
```
- Esperado: aparece `ghcr.io/cloudnative-pg/postgresql:16.13`. (Las imágenes de Chaos Mesh se verifican en Fase 2.)
- Si falta: importar con `manifiestos/images/import-images.sh` (ver `manifiestos/10-chaos-mesh/INSTALL-offline.md`).
- [ ] PASA

**0.7 CRÍTICO — Inventariar los cuatro clústeres CNPG preexistentes (para NO tocarlos)**
```bash
kubectl get clusters.postgresql.cnpg.io -A
```
- Esperado: exactamente **4** clústeres preexistentes (`pg-prod`, `pg-cert`, `pg-dev`, `gitlab/pg-gitlab`). **Anotarlos** (nombre + namespace + nodos) en `RESPONSABLES.md`.
- Verificaciones de seguridad sobre esa lista:
  - Ninguno se llama `pglab-cnpg-exp`. Si alguno coincide → cambiar el nombre experimental (p. ej. `pglab-cnpg-exp2`) en **todos** los manifiestos antes de seguir.
  - Ninguno está en el namespace `pg-chaos-lab`.
```bash
# Ubicación de TODOS los primarios preexistentes (cuáles co-residen en el nodo del lab):
kubectl get pods -A -l cnpg.io/instanceRole=primary -o wide
```
  - Nota: **3 de los primarios preexistentes (pg-cert-1, pg-dev-3, pg-gitlab-2) co-residen hoy en `tcolp293`**, el nodo del lab. Esto es **conocido y aceptado**; la protección no descansa en su ausencia sino en G1 (ningún manifiesto de fallo los selecciona) — se demuestra en la compuerta (`CHECKLIST-GONOGO.md`, G1 y G5). El primario de producción `pg-prod-2` **no** está en `tcolp293`.
- [ ] PASA — clústeres preexistentes anotados: ____________________

**0.8 El namespace del laboratorio NO existe todavía**
```bash
kubectl get ns pg-chaos-lab
```
- Esperado: `Error ... "pg-chaos-lab" not found`.
- Si existe: investigar/limpiar restos de una ejecución previa antes de continuar (coordinar con storage si hay PVCs).
- [ ] PASA

**0.9 SNAPSHOT DE ESTADO INICIAL (línea base — obligatorio antes de tocar nada)**

Capturar y **guardar** un retrato documentado del estado del clúster ANTES de crear nada. Este archivo es la línea base contra la que se compara al final (Fase 6.3).

```bash
OUT=estado-inicial.txt
{
  echo "===== SNAPSHOT ESTADO INICIAL (linea base) ====="
  echo "# Fecha (UTC): $(date -u +%FT%TZ)"
  echo "# Operador de la captura: <RELLENAR NOMBRE>"
  echo
  echo "----- Versiones -----"
  kubectl version -o yaml | grep -A3 -E 'serverVersion'
  echo
  echo "----- Operador CNPG (imagen y estado) -----"
  kubectl get deploy -A -l app.kubernetes.io/name=cloudnative-pg \
    -o custom-columns='NS:.metadata.namespace,NAME:.metadata.name,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[*].image'
  echo
  echo "----- Clusteres CNPG PREEXISTENTES (los 4 que NO se tocan) -----"
  # Nombre, namespace, nº de instancias, estado e instancias listas:
  kubectl get clusters.postgresql.cnpg.io -A \
    -o custom-columns='NS:.metadata.namespace,NAME:.metadata.name,INSTANCES:.spec.instances,READY:.status.readyInstances,STATUS:.status.phase' \
    --sort-by=.metadata.name
  echo
  echo "----- Pods de los clusteres productivos y su nodo -----"
  kubectl get pods -A -l cnpg.io/podRole=instance \
    -o custom-columns='NS:.metadata.namespace,POD:.metadata.name,CLUSTER:.metadata.labels.cnpg\.io/cluster,ROLE:.metadata.labels.cnpg\.io/instanceRole,NODE:.spec.nodeName,STATUS:.status.phase' \
    --sort-by=.metadata.namespace
  echo
  echo "----- Nodos y etiquetas relevantes -----"
  kubectl get nodes -o custom-columns='NODE:.metadata.name,STATUS:.status.conditions[-1].type,LAB:.metadata.labels.pg-chaos-lab/member' --sort-by=.metadata.name
} | tee "$OUT"
```
- Esperado: `estado-inicial.txt` generado, con **exactamente los 4 clústeres preexistentes**, su nº de instancias, su estado saludable, sus nodos, el operador y su imagen, y las versiones. Revisar visualmente que todo esté sano.
- **Guardar `estado-inicial.txt`** junto a `results.csv` (no se borra hasta cerrar el piloto). Es la línea base de la comparación final.
- [ ] PASA — `estado-inicial.txt` capturado y revisado

> **Puerta de fase:** todas las casillas 0.1–0.9 en PASA. Si alguna falla, no se avanza.

---

## FASE 1 — Aislamiento (namespace, cuota, límites, RBAC)

```bash
kubectl apply -f manifiestos/00-namespace/
```
Verificar:
```bash
kubectl get ns pg-chaos-lab --show-labels          # label chaos-mesh.org/inject=enabled
kubectl -n pg-chaos-lab get resourcequota pg-chaos-lab-quota
kubectl -n pg-chaos-lab get limitrange pg-chaos-lab-limits
kubectl -n pg-chaos-lab get role,rolebinding,serviceaccount | grep chaos
```
- Esperado: namespace con label `chaos-mesh.org/inject=enabled`; ResourceQuota activa (tope duro del lab); LimitRange; ServiceAccount `chaos-operator` + Role/RoleBinding `chaos-experiments`.
- Si falla: revisar el error de `apply` y reintentar. No avanzar sin la cuota activa (es la protección primaria de capacidad).
- [ ] PASA

---

## FASE 2 — Chaos Mesh acotado, offline

> **Versión:** se usa **Chaos Mesh v2.8.3** (última de la línea 2.8; soporta K8s 1.30–1.35 e incluye los parches de seguridad "Chaotic Deputy"). Chaos Mesh 2.7.x queda **descartado**: solo soporta hasta K8s 1.28 y este clúster corre 1.34.6. Verificar el último parche 2.8.x vigente al momento de instalar.

Seguir `manifiestos/10-chaos-mesh/INSTALL-offline.md`. Resumen:
```bash
# 2.1 Importar imágenes de Chaos Mesh en CADA nodo del lab (en el nodo):
sudo ctr -n k8s.io images import chaos-mesh_v2.8.3.tar
sudo ctr -n k8s.io images import chaos-daemon_v2.8.3.tar

# 2.2 Renderizar el chart offline con los values acotados y aplicar:
helm template chaos-mesh ./chaos-mesh-2.8.3.tgz \
  --namespace pg-chaos-lab --include-crds \
  -f manifiestos/10-chaos-mesh/values-airgapped.yaml > chaos-mesh-rendered.yaml
kubectl apply -f chaos-mesh-rendered.yaml
```
Verificar el confinamiento (clave de seguridad):
```bash
# El controlador y el daemon SOLO en pg-chaos-lab:
kubectl get pods -A -l app.kubernetes.io/instance=chaos-mesh -o wide
# chaos-daemon SOLO en nodos del lab (cuenta == nº de nodos del lab):
kubectl -n pg-chaos-lab get pods -o wide | grep chaos-daemon
```
- Esperado: todos los pods de Chaos Mesh en `pg-chaos-lab`; `chaos-daemon` únicamente en `tcolp293`; `clusterScoped:false`, `enableFilterNamespace:true`, `targetNamespace:pg-chaos-lab` en el rendered.
- Si algún `chaos-daemon` aparece en un nodo que no es del lab: **detener**, revisar `nodeSelector`, borrar el rendered y reinstalar.
- [ ] PASA

---

## FASE 3 — Desplegar SOLO el clúster experimental + carga (NO se instala operador)

**3.1 Ajustar la StorageClass** en `manifiestos/20-cluster/cluster-cnpg.yaml` (`storageClass: huawei-ch-xfs`).

**3.2 Crear el clúster experimental** (lo gestiona el operador CNPG ya existente):
```bash
kubectl apply -f manifiestos/20-cluster/cluster-cnpg.yaml
kubectl -n pg-chaos-lab get cluster pglab-cnpg-exp -w   # esperar estado saludable
```
- Esperado: `pglab-cnpg-exp` con 3 instancias, `Cluster in healthy state`.
```bash
kubectl -n pg-chaos-lab get pods -l cnpg.io/cluster=pglab-cnpg-exp -o wide
```
- Esperado: `pglab-cnpg-exp-1/2/3` en `Running`, en nodos `tcolp293`.

**3.3 Desplegar carga y verificador e inicializar pgbench (una sola vez):**
```bash
kubectl apply -f manifiestos/30-workload/
kubectl -n pg-chaos-lab exec deploy/pgbench-cnpg -- \
  pgbench -i -s 10 -h pglab-cnpg-exp-rw -U lab labdb
```
Verificar que el verificador registra COMMITs:
```bash
kubectl -n pg-chaos-lab logs deploy/tx-verifier-cnpg --tail=5
```
- Esperado: líneas `COMMIT <n> <timestamp>` en aumento.
- Si el verificador no conecta: revisar el secret `pglab-cnpg-exp-app` y el host `pglab-cnpg-exp-rw`.
- [ ] PASA

---

## FASE 4 — COMPUERTA GO/NO-GO (obligatoria antes de inyectar)

Ejecutar **CHECKLIST-GONOGO.md** en su totalidad. Incluye, como mínimo:
- Dry-run de **cada** selector de fallo: mostrar qué pods seleccionaría **antes** de ejecutar, y confirmar que **solo** aparecen pods de `pglab-cnpg-exp` (ningún pod de los cuatro clústeres preexistentes).
- Prueba de que un experimento apuntando a otro namespace **no selecciona nada / es rechazado**.
- `chaos-daemon` solo en nodos del lab.
- Alertas de producción **no** silenciadas.

**Regla:** si **cualquier** ítem marca NO PASA → **abortar** (ver `ABORTO.md`). No se inyecta nada.
- [ ] TODOS los ítems de CHECKLIST-GONOGO.md en PASA

---

## FASE 5 — Ejecución de experimentos (acotados al clúster experimental)

Reglas para todas las corridas: **n=10** por combinación, **cool-down ≥120 s** entre inyecciones, y esperar el estado saludable del clúster entre repeticiones. Tras **cada** inyección, revisar los criterios de `ABORTO.md`.

Espera de recuperación entre repeticiones:
```bash
kubectl -n pg-chaos-lab get cluster pglab-cnpg-exp   # -> healthy, 3/3, lag ~0
```

> **Reparto por ventanas:** F1 y F3 → Ventana 1 · F4 → Ventana 2 · F2 → Ventana 3.

**F1 — Terminación del pod primario (`pod-kill`, one-shot) · [Ventana 1]:**
```bash
cd manifiestos/scripts
for r in $(seq 1 10); do ./run-experiment.sh cnpg ../40-experiments/f1-podkill-cnpg.yaml $r; sleep 120; done
```
- [ ] 10 repeticiones · resultados en `results.csv`

**F3 — Partición de red del primario (NetworkPolicy Calico; reversión = borrar la política) · [Ventana 1]:**
```bash
for r in $(seq 1 10); do ./run-experiment.sh cnpg ../40-experiments/f3-partition-cnpg.yaml $r; sleep 120; done
```
- [ ] 10 repeticiones

**F4 — Sensibilidad a latencia de E/S (IOChaos FUSE) · [Ventana 2] · DISEÑO "Opción A" (métrica continua):**

> **Cambio de instrumento (leer NOTA METODOLÓGICA F4 más abajo):** F4 mide una métrica
> *continua* (latencia/tps bajo E/S degradada), no un evento. **NO se usa `run-experiment.sh`**
> (su detector de failover retiraría el IOChaos a los ~120 s). Se usa el arnés dedicado
> `run-f4-latency.sh`, que aplica el IOChaos, corre `pgbench --progress=1` la ventana completa
> y retira el IOChaos. Diseño: **5 corridas × 5 min por nivel** (0/20/50/100 ms), muestreo por
> segundo, descartando 30 s de calentamiento → ~1.4 M transacciones/nivel.

```bash
# 1) desplegar el runner ocioso (una sola vez en la ventana)
kubectl apply -f manifiestos/30-workload/pgbench-runner-cnpg.yaml
kubectl -n pg-chaos-lab rollout status deploy/pgbench-runner-cnpg --timeout=90s
# 2) ejecutar F4 (niveles 0/20/50/100 ms, 5 reps de 300 s c/u). El 0 ms es la linea base.
manifiestos/scripts/run-f4-latency.sh 300 5
# 3) parsear: percentiles por nivel + serie por segundo + filas-resumen a results.csv
manifiestos/scripts/parse-f4.py data-f4 results.csv
```
> IOChaos actúa a nivel de FUSE dentro del pod: **no toca la SAN Huawei** ni a otros consumidores.
> El nivel 0 ms (sin manifiesto) es la línea base sin inyección.
- [ ] Runner desplegado · niveles 0/20/50/100 ms · 5 corridas × 300 s cada uno · `f4-latency-series.csv` generado

**NOTA METODOLÓGICA F4 (documentar en la sección de Métodos del paper):**
El plan pre-registrado fijaba `n=10` repeticiones por combinación, apropiado para métricas de
*evento* (RTO/RPO de F1/F3). F4 mide una métrica *continua* (latencia/tps bajo E/S degradada),
donde el `n` estadístico son las transacciones muestreadas, no las corridas. Por ello F4 sustituye
las 10 repeticiones por **5 corridas × 5 min con muestreo por segundo** (~1.4 M transacciones y
~1350 puntos por-segundo por nivel tras descartar 30 s de calentamiento). Las 5 corridas aportan
la varianza entre-corridas (reproducibilidad); el muestreo por segundo aporta la distribución para
p50/p95/p99 y la prueba dosis-respuesta (Kruskal-Wallis entre niveles, Spearman latencia–nivel).
Este ajuste **adapta el diseño a la naturaleza de la métrica** y es una decisión consciente, no un
recorte. `n=10` se mantiene en F1/F3. (Instrumento: `run-f4-latency.sh` + `parse-f4.py`.)

**F2 — Indisponibilidad sostenida 10 min (`pod-failure`) — sustituto de fallo de nodo · [Ventana 3]:**
```bash
for r in $(seq 1 10); do ./run-experiment.sh cnpg ../40-experiments/f2-podfailure-cnpg.yaml $r; sleep 120; done
```
> Recordatorio de alcance: F2 **no** reproduce un fallo de nodo real (no hay detach/attach del volumen CSI); su RTO es una **cota inferior**. No se ejecuta drain/cordon.
- [ ] 10 repeticiones

---

## FASE 6 — Recolección de resultados, comparación con la línea base y limpieza total

**6.1 Recolectar evidencia:**
```bash
cd manifiestos/scripts
kubectl -n pg-chaos-lab logs deploy/tx-verifier-cnpg --timestamps > verifier-cnpg.log
PW=$(kubectl -n pg-chaos-lab get secret pglab-cnpg-exp-app -o jsonpath='{.data.password}' | base64 -d)
./parse-verifier.py verifier-cnpg.log pglab-cnpg-exp-rw lab "$PW" labdb   # RPO/RTO desde el log
./analyze.py results.csv                                                   # medianas, p95, Kruskal-Wallis, Spearman
kubectl -n pg-chaos-lab get events --sort-by=.lastTimestamp > events-lab.log
```
Guardar: `results.csv`, `verifier-cnpg.log`, `events-lab.log`.

**6.2 Limpieza total (coordinar el borrado de PVCs con el equipo de almacenamiento):**
```bash
kubectl -n pg-chaos-lab delete podchaos,iochaos,networkpolicy --all
kubectl delete -f manifiestos/30-workload/
kubectl -n pg-chaos-lab delete cluster pglab-cnpg-exp
kubectl delete -f chaos-mesh-rendered.yaml          # retirar Chaos Mesh
kubectl delete namespace pg-chaos-lab                # borra los PVCs del lab -> coordinar con storage
```

**6.3 VERIFICACIÓN DE IGUALDAD FINAL — producción idéntica a la línea base**

Regenerar el mismo retrato del paso 0.9 y **compararlo explícitamente** contra `estado-inicial.txt`. El objetivo no es solo "producción está sana", sino "producción quedó **igual** que antes de empezar".

```bash
OUT=estado-final.txt
{
  echo "===== SNAPSHOT ESTADO FINAL ====="
  echo "# Fecha (UTC): $(date -u +%FT%TZ)"
  echo
  echo "----- Versiones -----"
  kubectl version -o yaml | grep -A3 -E 'serverVersion'
  echo
  echo "----- Operador CNPG (imagen y estado) -----"
  kubectl get deploy -A -l app.kubernetes.io/name=cloudnative-pg \
    -o custom-columns='NS:.metadata.namespace,NAME:.metadata.name,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[*].image'
  echo
  echo "----- Clusteres CNPG PREEXISTENTES -----"
  kubectl get clusters.postgresql.cnpg.io -A \
    -o custom-columns='NS:.metadata.namespace,NAME:.metadata.name,INSTANCES:.spec.instances,READY:.status.readyInstances,STATUS:.status.phase' \
    --sort-by=.metadata.name
  echo
  echo "----- Pods de los clusteres productivos y su nodo -----"
  kubectl get pods -A -l cnpg.io/podRole=instance \
    -o custom-columns='NS:.metadata.namespace,POD:.metadata.name,CLUSTER:.metadata.labels.cnpg\.io/cluster,ROLE:.metadata.labels.cnpg\.io/instanceRole,NODE:.spec.nodeName,STATUS:.status.phase' \
    --sort-by=.metadata.namespace
  echo
  echo "----- Nodos y etiquetas relevantes -----"
  kubectl get nodes -o custom-columns='NODE:.metadata.name,STATUS:.status.conditions[-1].type,LAB:.metadata.labels.pg-chaos-lab/member' --sort-by=.metadata.name
} | tee "$OUT"

echo; echo "===== DIFF vs. LINEA BASE (estado-inicial.txt) ====="
diff -u estado-inicial.txt estado-final.txt && echo "== IGUAL: sin diferencias ==" \
  || echo "!! ATENCION: hay diferencias — revisar abajo antes de dar por cerrado el piloto"
```
Interpretación del diff:
- **Diferencias esperadas y aceptables:** la fecha/hora de la cabecera; la etiqueta `LAB` de los nodos (si se etiquetaron/desetiquetaron para el lab); la desaparición del clúster experimental (que no debe aparecer en ninguno de los dos snapshots productivos de todas formas).
- **Diferencias que disparan ALERTA** (los recursos preexistentes deben quedar **idénticos**): distinto número de clústeres preexistentes; cambio de `INSTANCES`/`READY`/`STATUS` en cualquiera de los 4; un primario preexistente en un nodo distinto por causa del piloto; imagen o estado del operador CNPG distintos. **Cualquiera de estas → tratar como incidente:** notificar al DBA/seguridad (ver `RESPONSABLES.md`) y NO dar el piloto por cerrado hasta aclararlo.
- [ ] PASA — `estado-final.txt` generado; diff revisado; los 4 clústeres preexistentes **iguales** a la línea base

**6.4 Confirmación final:**
```bash
kubectl get clusters.postgresql.cnpg.io -A           # -> siguen EXACTAMENTE los 4 preexistentes, saludables
kubectl get deploy -A -l app.kubernetes.io/name=cloudnative-pg   # operador intacto
```
- [ ] PASA — piloto cerrado; guardar `estado-inicial.txt`, `estado-final.txt`, `results.csv`, `verifier-cnpg.log`, `events-lab.log`

---

**Fin del PROCEDIMIENTO.md**
