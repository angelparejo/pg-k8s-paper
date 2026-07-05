#!/usr/bin/env bash
# Importa todos los .tar del directorio actual en el containerd del nodo.
# Ejecutar EN CADA nodo etiquetado pg-chaos-lab/member=true (chaos-daemon es DaemonSet).
set -euo pipefail
for t in *.tar; do
  echo ">> $t"
  sudo ctr -n k8s.io images import "$t"
done
sudo ctr -n k8s.io images ls | grep -E "cloudnative-pg|chaos" || true
