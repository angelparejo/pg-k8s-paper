# Fase 6 — Recolección, análisis y cierre del piloto (runbook listo para ejecutar)

Preparado mientras corre el lote F2. **Ejecutar apenas termine F2** (F4 quedó reformulada → F2 es
el último experimento; tras esto se cierra el piloto). Modo desacoplado: cada bloque se corre en el
servidor y se pega la salida. Rutas relativas a `/appl/k8s-admin/experimnetal/paquete-ejecucion-fase-b`.

Experimentos con datos: **F1** (pod-kill, n=10), **F3** (partición, 12 iny.), **F2** (pod-failure, n=10).
F4 sin datos (bloqueo documentado).

---

## 6.1 — Recolección de evidencia (LECTURA + escritura de archivos locales)

```bash
cd /appl/k8s-admin/experimnetal/paquete-ejecucion-fase-b
# 1) volcar el log completo del verificador (con timestamps) — base de RTO y RPO
kubectl -n pg-chaos-lab logs deploy/tx-verifier-cnpg --timestamps > verifier-cnpg.log
wc -l verifier-cnpg.log

# 2) RTO (huecos entre COMMITs) + RPO (ids no visibles en truth)
PW=$(kubectl -n pg-chaos-lab get secret pglab-cnpg-exp-app -o jsonpath='{.data.password}' | base64 -d)
manifiestos/scripts/parse-verifier.py verifier-cnpg.log pglab-cnpg-exp-rw lab "$PW" labdb

# 3) tabla de marcas por rep (T0) para ATRIBUIR cada hueco a su experimento
echo "--- results.csv (F1 + F3 + F2) ---"
cat results.csv

# 4) eventos del namespace del lab (para el contraste de eventos F1 vs F2 vs F3)
kubectl -n pg-chaos-lab get events --sort-by=.lastTimestamp > events-lab.log
tail -30 events-lab.log
```

**Atribución de huecos (clave):** `parse-verifier.py` lista todos los huecos `>= 1 s` con su
`@ timestamp`. Emparejar cada hueco con el `T0` de su fila en `results.csv`:
- **F1:** ~8 s, timestamps ~13:5x UTC (10 huecos).
- **F3:** ~60 s (+ una sonda 149 s + una 300 s), ~15:2x UTC (12 huecos).
- **F2:** ~77 s, ~22:1x UTC (10 huecos del lote + **1 extra de la validación ~22:11** que NO tiene
  fila en `results.csv` → se excluye emparejando solo con los T0 del lote).
- Los pgbench de la **validación F4** (~21:4x) NO generan huecos (no hubo inyección).

## 6.2 — Estadística no paramétrica

```bash
cd /appl/k8s-admin/experimnetal/paquete-ejecucion-fase-b
manifiestos/scripts/analyze.py results.csv
```
Da medianas/p95/p99 por (experimento, operador). **Nota:** el bloque Kruskal-Wallis/Spearman de
`analyze.py` es para los niveles de F4 (no hay) → saldrá vacío, es esperado. Mann-Whitney cnpg-vs-zalando
también vacío (solo CNPG). Lo útil aquí son las medianas/percentiles de F1/F2/F3.

> Nota sobre `results.csv` para F2: `run-experiment.sh` escribe `t1 = t0 + ~120 s` (no hubo cambio de
> primario), así que la **columna `rto` de `results.csv` NO es el RTO de F2**. El RTO real de F2 sale de
> `parse-verifier.py` (huecos ~77 s). Para F1 igual: el RTO bueno es el del verificador.

## 6.3 — Verificación de igualdad final vs. línea base

```bash
cd /appl/k8s-admin/experimnetal/paquete-ejecucion-fase-b
OUT=estado-final.txt
{
  echo "===== SNAPSHOT ESTADO FINAL ====="; echo "# Fecha (UTC): $(date -u +%FT%TZ)"; echo
  echo "----- Operador CNPG -----"
  kubectl get deploy -A -l app.kubernetes.io/name=cloudnative-pg \
    -o custom-columns='NS:.metadata.namespace,NAME:.metadata.name,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[*].image'
  echo; echo "----- Clusteres CNPG PREEXISTENTES -----"
  kubectl get clusters.postgresql.cnpg.io -A \
    -o custom-columns='NS:.metadata.namespace,NAME:.metadata.name,INSTANCES:.spec.instances,READY:.status.readyInstances,STATUS:.status.phase' \
    --sort-by=.metadata.name
} | tee "$OUT"
echo; echo "===== DIFF vs LINEA BASE ====="
diff -u estado-inicial.txt estado-final.txt && echo "== IGUAL ==" || echo "!! revisar diferencias"
```
Diferencias aceptables: fecha; ausencia del clúster experimental. **Disparan alerta:** cambio en
número/estado de los 4 preexistentes o en la imagen del operador → tratar como incidente (RESPONSABLES.md).

## 6.4 — ⚠️ Teardown total (DESTRUCTIVO — coordinar borrado de PVCs con almacenamiento)

Solo cuando 6.1–6.3 estén guardados y revisados. Borra el lab entero (F4 ya no se retoma en este piloto).

```bash
cd /appl/k8s-admin/experimnetal/paquete-ejecucion-fase-b
kubectl -n pg-chaos-lab delete podchaos,iochaos,networkpolicy --all
kubectl delete -f manifiestos/30-workload/                 # verifier + pgbench (+ runner ya borrado)
kubectl -n pg-chaos-lab delete cluster pglab-cnpg-exp
kubectl delete -f chaos-mesh-rendered.yaml                 # retirar Chaos Mesh
kubectl delete namespace pg-chaos-lab                       # borra PVCs del lab -> coordinar storage
# SC huawei-ch-xfs es Retain: los PV quedan Released -> borrarlos con storage tras confirmar
kubectl get pv | grep pg-chaos-lab
```

**Guardar del piloto:** `verifier-cnpg.log`, `events-lab.log`, `results.csv` (+ backups),
`estado-inicial.txt`, `estado-final.txt`, `f4-VALIDACION-*.log`. Son la evidencia para Resultados.
