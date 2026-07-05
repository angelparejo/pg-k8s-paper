# CHECKLIST GO/NO-GO — Compuerta crítica antes de inyectar

**Cuándo:** Fase 4 del `PROCEDIMIENTO.md`, y de nuevo (ítems G1–G4) en la reanudación de cada ventana posterior (paso R6).
**Regla absoluta:** basta **un solo NO PASA** para **abortar**. No se inyecta nada hasta que TODOS los ítems estén en PASA. Ante la duda → NO-GO. Ver `ABORTO.md`.

**Contexto de riesgo:** el operador CNPG es **compartido** con tres clústeres productivos. Ninguna inyección puede alcanzarlos. La contención descansa en cuatro capas independientes que este checklist verifica una por una:
1. Chaos Mesh `clusterScoped:false` + `enableFilterNamespace:true` + `targetNamespace:pg-chaos-lab`.
2. `chaos-daemon` confinado por `nodeSelector` a los nodos del lab.
3. Todo selector acotado por `namespaces:[pg-chaos-lab]`.
4. Nombre de clúster único `pglab-cnpg-exp` (ningún productivo lo comparte).

---

## G1 — Dry-run de selectores: cada experimento resuelve SOLO al clúster experimental

**Es el ítem más importante.** El ítem **autoritativo** es **G1.2**: un dry-run que extrae el selector *del propio manifiesto* y pregunta a kubectl qué pods resolvería — sin que el operador teclee ningún selector. G1.1, G1.3 y G1.4 son verificaciones de apoyo, independientes.

**G1.1 — Inventario estático (mirada rápida, NO autoritativa):**
```bash
for f in manifiestos/40-experiments/*.yaml; do
  echo "== $f =="
  grep -E 'kind:|namespaces:|cnpg.io/cluster:|cnpg.io/instanceRole:' "$f"
done
```
- Vistazo rápido. La verificación real —vinculada al manifiesto— es G1.2.
- [ ] PASA / [ ] NO PASA

**G1.2 — Dry-run DERIVADO DEL MANIFIESTO (autoritativo): a qué pods apuntaría CADA experimento.**
No teclees selectores: el script los extrae del YAML, los valida y consulta esos pods exactos. Requiere Chaos Mesh instalado (Fase 2 ya hecha).
```bash
rc=0
for f in manifiestos/40-experiments/*.yaml; do
  echo "================ $(basename "$f") ================"
  if ! kubectl create --dry-run=client -o json -f "$f" \
        | python3 manifiestos/scripts/dry-run-selectores.py; then
    rc=1
  fi
  echo
done
echo "===================================================="
if [ "$rc" -eq 0 ]; then
  echo "G1.2 GLOBAL: PASA — todos resuelven solo a pglab-cnpg-exp en pg-chaos-lab"
else
  echo "G1.2 GLOBAL: NO PASA — al menos un manifiesto falla. ABORTAR (ABORTO.md)."
fi
```
- Esperado: para **cada** manifiesto, el script imprime `EL MANIFIESTO SELECCIONARÍA ESTOS PODS:` seguido de **exactamente 1 pod**, en `pg-chaos-lab`, del clúster `pglab-cnpg-exp`, y `VEREDICTO: PASA`. Cierre global `G1.2 GLOBAL: PASA`.
- **Regla inequívoca:** si aparece **CUALQUIER** pod fuera de `pg-chaos-lab` o que no sea de `pglab-cnpg-exp`, o **cualquier** `VEREDICTO: NO PASA` (segundo namespace, nombre de clúster alterado, rol aislado, mecanismo de selección no soportado) → **NO PASA, abortar** (`ABORTO.md`). No se interpreta, no se "arregla al vuelo": se aborta.
- [ ] PASA / [ ] NO PASA

**G1.3 — El label de clúster experimental es único en TODO el clúster K8s:**
```bash
kubectl get pods -A -l cnpg.io/cluster=pglab-cnpg-exp -o wide
```
- Esperado: **todos** los pods listados están en el namespace `pg-chaos-lab`. Ningún pod productivo comparte ese label.
- [ ] PASA / [ ] NO PASA

**G1.4 — Demostrar por qué el filtro de nombre es imprescindible (label peligroso):**
```bash
kubectl get pods -A -l cnpg.io/instanceRole=primary -o wide
```
- Esperado: aparecen **4 primarios** (los 3 productivos + el experimental). Esto evidencia que un selector con **solo** `cnpg.io/instanceRole=primary` alcanzaría producción. G1.2 ya rechaza automáticamente cualquier manifiesto que use ese label sin el de clúster (regla "rol aislado").
- [ ] PASA / [ ] NO PASA

**G1.5 — Semántica de F3 (NetworkPolicy):**
```bash
grep -E 'kind:|namespace:|podSelector|cnpg.io/cluster:|cnpg.io/instanceRole:' \
  manifiestos/40-experiments/f3-partition-cnpg.yaml
```
- G1.2 ya validó mecánicamente que el `podSelector` de F3 resuelve al único primario experimental. Aquí solo se confirma la semántica: la NetworkPolicy vive en `pg-chaos-lab` y, por diseño de Kubernetes, una NetworkPolicy **solo** puede afectar pods de su propio namespace — no puede alcanzar producción aunque el selector fuese incorrecto.
- [ ] PASA / [ ] NO PASA

---

## G2 — Contención entre namespaces (estructural, sin riesgo)

**G2.1 — Configuración del controlador Chaos Mesh:**
```bash
grep -E 'clusterScoped|enableFilterNamespace|targetNamespace' \
  manifiestos/10-chaos-mesh/values-airgapped.yaml
# y en lo realmente desplegado:
kubectl -n pg-chaos-lab get deploy -l app.kubernetes.io/component=controller-manager \
  -o yaml | grep -iE 'cluster-scoped|filter-namespace|target-namespace|TARGET_NAMESPACE' || true
```
- Esperado: `clusterScoped: false`, `enableFilterNamespace: true`, `targetNamespace: pg-chaos-lab`.
- [ ] PASA / [ ] NO PASA

**G2.2 — Los namespaces productivos NO son inyectables** (les falta el label de opt-in):
```bash
# Sustituir <NS-PROD-1..3> por los namespaces de los 3 clústeres productivos (paso 0.7):
for ns in <NS-PROD-1> <NS-PROD-2> <NS-PROD-3>; do
  echo -n "$ns -> "; kubectl get ns "$ns" -o jsonpath='{.metadata.labels.chaos-mesh\.io/inject}{"\n"}'
done
```
- Esperado: cada uno imprime **vacío** (no tienen `chaos-mesh.org/inject=enabled`). Solo `pg-chaos-lab` lo tiene.
- [ ] PASA / [ ] NO PASA

**G2.3 — El controlador no tiene permisos de ámbito de clúster** (con `clusterScoped:false` usa Role, no ClusterRole):
```bash
kubectl get clusterrolebinding -o wide | grep -i chaos || echo "OK: sin ClusterRoleBinding de chaos-mesh"
```
- Esperado: sin ClusterRoleBinding que otorgue a Chaos Mesh acceso a otros namespaces (o solo los internos propios del chart, sin permiso sobre pods de producción).
- [ ] PASA / [ ] NO PASA

---

## G3 — Prueba funcional: un experimento apuntando a OTRO namespace no selecciona nada

**Advertencia de seguridad:** esta prueba se dirige a un namespace **sin cargas de base de datos productivas** (usar `default` u otro namespace inocuo) y con un selector que **no coincide con ningún pod**, de modo que es inofensiva por construcción. Su objetivo es confirmar que el filtro de namespace actúa.

```bash
cat <<'YAML' | kubectl apply -f -
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: gonogo-crossns-test
  namespace: pg-chaos-lab
spec:
  action: pod-failure
  mode: one
  duration: 5s
  selector:
    namespaces: [default]                 # namespace SIN bases de datos productivas
    labelSelectors:
      gonogo-test: does-not-exist         # no coincide con ningun pod
YAML

sleep 5
kubectl -n pg-chaos-lab get podchaos gonogo-crossns-test \
  -o jsonpath='{.status.experiment.containerRecords}{"\n"}'; echo
kubectl -n pg-chaos-lab describe podchaos gonogo-crossns-test | grep -iE 'record|target|namespace|inject' | head
# Limpieza inmediata de la prueba:
kubectl -n pg-chaos-lab delete podchaos gonogo-crossns-test
```
- Esperado: **cero** registros/targets seleccionados; ningún pod afectado. El filtro de namespace impide alcanzar `default` (no está etiquetado), y el selector no coincidiría con nada aunque lo estuviera.
- Si aparece **cualquier** target seleccionado fuera de `pg-chaos-lab` → **NO-GO inmediato**, abortar y revisar la instalación de Chaos Mesh.
- [ ] PASA / [ ] NO PASA

---

## G4 — chaos-daemon solo en nodos del laboratorio

```bash
kubectl -n pg-chaos-lab get pods -o wide | grep chaos-daemon
kubectl get nodes -l pg-chaos-lab/member=true -o name
```
- Esperado: hay un `chaos-daemon` por **cada** nodo del lab y en **ningún** otro nodo. El daemon privilegiado (el que realmente mata/inyecta) no existe fuera del pool del lab.
- [ ] PASA / [ ] NO PASA

---

## G5 — Ningún pod productivo corre en los nodos del laboratorio

```bash
for n in $(kubectl get nodes -l pg-chaos-lab/member=true -o name | cut -d/ -f2); do
  echo "== nodo $n =="
  kubectl get pods -A -o wide --field-selector spec.nodeName="$n" | grep -v '^pg-chaos-lab ' | grep -viE 'kube-system|calico|chaos'
done
```
- Esperado: no aparecen bases de datos ni cargas productivas en los nodos del lab (solo componentes de sistema y del propio lab).
- [ ] PASA / [ ] NO PASA

---

## G6 — Alertas de producción NO silenciadas

```bash
# Si se usa Alertmanager, listar los silences activos y su matcher de namespace:
# amtool silence query   (o via la API/UI de Alertmanager)
```
- Esperado: **como mucho** existe un silence acotado a `namespace="pg-chaos-lab"`. **Ningún** silence global ni sobre namespaces productivos. La monitorización de los 3 clústeres productivos sigue **activa** durante toda la ventana.
- [ ] PASA / [ ] NO PASA

---

## G7 — Aislamiento de capacidad activo

```bash
kubectl -n pg-chaos-lab get resourcequota pg-chaos-lab-quota -o wide
kubectl -n pg-chaos-lab get limitrange pg-chaos-lab-limits
```
- Esperado: ResourceQuota con uso dentro del tope; LimitRange presente. El lab no puede crecer más allá de la cuota.
- [ ] PASA / [ ] NO PASA

---

## G8 — Línea base capturada

```bash
test -s estado-inicial.txt && echo "OK: estado-inicial.txt presente" || echo "FALTA la linea base"
```
- Esperado: `estado-inicial.txt` (paso 0.9) existe y contiene los 3 clústeres productivos sanos. Sin línea base no hay comparación final posible → NO-GO.
- [ ] PASA / [ ] NO PASA

---

## G9 — Roles y autoridad de aborto definidos

- [ ] `RESPONSABLES.md` está relleno: quién aprueba, quién ejecuta, quién monitorea los 3 clústeres productivos durante la ventana y quién tiene **autoridad de aborto**.
- [ ] Todos los presentes conocen `ABORTO.md` y saben ejecutar la reversión de la fase en curso.
- [ ] PASA / [ ] NO PASA

---

## Veredicto

- **GO** — solo si G1 a G9 están **todos** en PASA. Registrar hora, ventana y firma del responsable de aborto, y proceder a Fase 5.
- **NO-GO** — si **cualquier** ítem está en NO PASA. Ejecutar `ABORTO.md`, documentar el motivo y no inyectar.

| Campo | Valor |
|---|---|
| Ventana (1/2/3) | ______ |
| Fecha/hora (UTC) | ______ |
| Veredicto | GO / NO-GO |
| Responsable de aborto (firma) | ______ |
