#!/usr/bin/env bash
# Orquesta UNA repeticion de un experimento y registra el RTO en results.csv.
# Camino B: SOLO CloudNativePG. Clúster experimental: pglab-cnpg-exp.
# Uso: ./run-experiment.sh cnpg <manifiesto-chaos.yaml|networkpolicy.yaml> <rep>
# El RPO se calcula despues con parse-verifier.py sobre los logs del tx-verifier.
set -euo pipefail
OP="${1:-cnpg}"; MANIFEST="$2"; REP="${3:-1}"
NS=pg-chaos-lab
if [ "$OP" != "cnpg" ]; then
  echo "Camino B es solo CNPG (recibido: '$OP'). Uso: ./run-experiment.sh cnpg <manifiesto> <rep>"; exit 1
fi
HOST=pglab-cnpg-exp-rw
SECRET=pglab-cnpg-exp-app
PGPASSWORD=$(kubectl -n $NS get secret "$SECRET" -o jsonpath="{.data.password}" | base64 -d)
EXP=$(basename "$MANIFEST" .yaml)
PROBE="kubectl -n $NS run rto-probe-$$ --rm -i --restart=Never \
  --image=ghcr.io/cloudnative-pg/postgresql:16.13 \
  --env=PGPASSWORD=$PGPASSWORD --command -- \
  psql -h $HOST -U lab -d labdb -tAc"

echo "[i] verificando linea base de escritura..."
$PROBE "SELECT 1" >/dev/null

T0=$(date +%s.%N)
kubectl apply -f "$MANIFEST"
echo "[i] fallo inyectado: $EXP (t0=$T0)"

# Sondeo del RTO: primera escritura aceptada por el nuevo primario
while true; do
  if $PROBE "INSERT INTO truth(id) VALUES (-$(date +%s%N)) RETURNING id" >/dev/null 2>&1; then
    T1=$(date +%s.%N); break
  fi
  sleep 0.5
done
RTO=$(echo "$T1 - $T0" | bc)
echo "$EXP,$OP,$REP,$T0,$T1,$RTO" >> results.csv
echo "[OK] RTO=${RTO}s  (results.csv)"

# Limpieza del experimento (para NetworkPolicy esto ES el aborto/reversion)
kubectl delete -f "$MANIFEST" --ignore-not-found
