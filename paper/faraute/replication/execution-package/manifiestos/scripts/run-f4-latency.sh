#!/usr/bin/env bash
# F4 - Sensibilidad a latencia de E/S (IOChaos FUSE) sobre el primario CNPG.
# Diseno "Opcion A" (metrica continua): por nivel (0/20/50/100 ms) N corridas de
# DUR s con muestreo por segundo (pgbench --progress=1). El IOChaos se aplica
# durante la corrida y se retira al terminar. NO usa run-experiment.sh: F4 no
# produce failover, y el detector de cambio-de-primario de aquel script retiraria
# el IOChaos a los ~120 s (bug), exponiendo la latencia mucho menos que lo declarado.
#
# Requisitos: deploy/pgbench-runner-cnpg desplegado (ocioso) y cluster healthy 3/3.
# El IOChaos se gobierna con CLUSTER_SCOPED=false + filtro de namespace (confinado).
#
# Uso: ./run-f4-latency.sh [DUR_s] [N_reps]   (por defecto 300 s, 5 reps)
# Salida: logs crudos por corrida en data-f4/f4-<lvl>ms-rep<r>.log
# Despues:  ./parse-f4.py data-f4 results.csv   (percentiles + filas-resumen)
set -uo pipefail
DUR="${1:-300}"; REPS="${2:-5}"
NS=pg-chaos-lab
RUNNER=deploy/pgbench-runner-cnpg
EXPDIR=manifiestos/40-experiments
OUT=data-f4; mkdir -p "$OUT"
LEVELS=(0 20 50 100)

sig() { kubectl get clusters -A --no-headers | grep -v pglab-cnpg-exp \
        | awk '{print $1"/"$2" ready="$5" primary="$NF}' | sort; }
BASELINE="$(sig)"

# pre-flight: runner presente
if ! kubectl -n "$NS" get "$RUNNER" >/dev/null 2>&1; then
  echo "FALTA $RUNNER. Aplica: kubectl apply -f manifiestos/30-workload/pgbench-runner-cnpg.yaml"; exit 1
fi
kubectl -n "$NS" rollout status "$RUNNER" --timeout=90s >/dev/null || { echo "runner no Ready"; exit 1; }

echo "F4 Opcion A: niveles=${LEVELS[*]} ms | DUR=${DUR}s | reps=${REPS}"
for LVL in "${LEVELS[@]}"; do
  MF="$EXPDIR/f4-iolatency-${LVL}ms-cnpg.yaml"
  for r in $(seq 1 "$REPS"); do
    RI=$(kubectl -n "$NS" get cluster pglab-cnpg-exp -o jsonpath='{.status.readyInstances}')
    if [ "$RI" != "3" ]; then echo "ABORTO: readyInstances=$RI antes de ${LVL}ms rep $r"; exit 1; fi
    P0=$(kubectl -n "$NS" get cluster pglab-cnpg-exp -o jsonpath='{.status.currentPrimary}')
    echo "########## F4 ${LVL}ms rep $r  ($(date -u +%FT%T.%3NZ))  primario=$P0 ##########"
    if [ "$LVL" != "0" ]; then
      kubectl apply -f "$MF" >/dev/null
      sleep 5                     # dar tiempo a que el FUSE se active antes de medir
    fi
    LOG="$OUT/f4-${LVL}ms-rep${r}.log"
    kubectl -n "$NS" exec "$RUNNER" -- \
      pgbench -h pglab-cnpg-exp-rw -U lab -c 4 -j 2 -T "$DUR" --no-vacuum --progress=1 -r labdb \
      > "$LOG" 2>&1 || echo "  [warn] pgbench devolvio error (ver $LOG)"
    if [ "$LVL" != "0" ]; then kubectl delete -f "$MF" --ignore-not-found >/dev/null; fi
    grep -E 'tps = |latency average' "$LOG" | sed 's/^/    /' || true
    P1=$(kubectl -n "$NS" get cluster pglab-cnpg-exp -o jsonpath='{.status.currentPrimary}')
    [ "$P0" != "$P1" ] && echo "    [NOTA] hubo cambio de primario durante la corrida: $P0 -> $P1"
    if [ "$(sig)" != "$BASELINE" ]; then echo "ABORTO: preexistentes cambiaron"; sig; exit 1; fi
    kubectl -n "$NS" wait --for=condition=Ready cluster/pglab-cnpg-exp --timeout=120s >/dev/null 2>&1 || true
    echo "    --- cool-down 30s ---"; sleep 30
  done
done
echo
echo "OK. Logs crudos en $OUT/. Siguiente: ./manifiestos/scripts/parse-f4.py $OUT results.csv"
