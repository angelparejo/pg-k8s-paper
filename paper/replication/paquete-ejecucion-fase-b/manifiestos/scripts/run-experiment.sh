#!/usr/bin/env bash
# UNA repeticion de un experimento (Camino B: SOLO CloudNativePG, cluster pglab-cnpg-exp).
# Orquesta: inyecta el fallo, confirma el failover (cambio de currentPrimary), espera
# recuperacion y limpia. Registra marcas de tiempo en results.csv para localizar el gap.
#
# El RTO/RPO NO se miden aqui con una sonda activa: kubectl exec ~1s es demasiado grueso
# para el outage breve del failover (la sonda no lo capta). Se obtienen del gap entre
# COMMITs del tx-verifier (resolucion ~100 ms) con parse-verifier.py. Este script solo
# marca inyeccion/failover y garantiza el cool-down por recuperacion.
#
# Uso: ./run-experiment.sh cnpg <manifiesto> <rep>
set -euo pipefail
OP="${1:-cnpg}"; MANIFEST="$2"; REP="${3:-1}"
NS=pg-chaos-lab
[ "$OP" = cnpg ] || { echo "solo cnpg. Uso: ./run-experiment.sh cnpg <manifiesto> <rep>"; exit 1; }
EXP=$(basename "$MANIFEST" .yaml)

P0=$(kubectl -n "$NS" get cluster pglab-cnpg-exp -o jsonpath='{.status.currentPrimary}')
T0=$(date -u +%FT%T.%3NZ)
kubectl apply -f "$MANIFEST" >/dev/null
echo "[i] $EXP rep $REP inyectado a $T0 (primario previo=$P0); esperando failover..."

P1="$P0"
for _ in $(seq 1 240); do            # hasta ~120 s
  P1=$(kubectl -n "$NS" get cluster pglab-cnpg-exp -o jsonpath='{.status.currentPrimary}')
  [ "$P1" != "$P0" ] && break
  sleep 0.5
done
TFO=$(date -u +%FT%T.%3NZ)
if [ "$P1" != "$P0" ]; then echo "[OK] rep $REP failover $P0 -> $P1 (t=$TFO)"; else echo "[WARN] rep $REP sin cambio de primario en ~120s"; fi
echo "$EXP,$OP,$REP,$T0,$TFO,$P0,$P1" >> results.csv

kubectl delete -f "$MANIFEST" --ignore-not-found >/dev/null
kubectl -n "$NS" wait --for=condition=Ready cluster/pglab-cnpg-exp --timeout=180s >/dev/null 2>&1 || true
