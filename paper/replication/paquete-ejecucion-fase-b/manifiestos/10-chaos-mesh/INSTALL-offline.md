# Instalación offline de Chaos Mesh (air-gapped)

## 1. En una máquina CON internet
```bash
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm pull chaos-mesh/chaos-mesh --version 2.8.3          # genera chaos-mesh-2.8.3.tgz
docker pull ghcr.io/chaos-mesh/chaos-mesh:v2.8.3
docker pull ghcr.io/chaos-mesh/chaos-daemon:v2.8.3
docker save ghcr.io/chaos-mesh/chaos-mesh:v2.8.3  -o chaos-mesh_v2.8.3.tar
docker save ghcr.io/chaos-mesh/chaos-daemon:v2.8.3 -o chaos-daemon_v2.8.3.tar
```

## 2. Transferir e importar en CADA nodo del laboratorio
El chaos-daemon es un DaemonSet: la imagen debe existir en **todos** los nodos
etiquetados `pg-chaos-lab/member=true` (el controlador solo en donde se programe).
```bash
sudo ctr -n k8s.io images import chaos-mesh_v2.8.3.tar
sudo ctr -n k8s.io images import chaos-daemon_v2.8.3.tar
```

## 3. Renderizar el chart offline y aplicar
`helm template` no necesita red; los CRDs vienen en el chart.
```bash
helm template chaos-mesh ./chaos-mesh-2.8.3.tgz \
  --namespace pg-chaos-lab \
  --include-crds \
  -f values-airgapped.yaml > chaos-mesh-rendered.yaml
kubectl apply -f chaos-mesh-rendered.yaml
kubectl -n pg-chaos-lab get pods -l app.kubernetes.io/instance=chaos-mesh
```

## Notas de seguridad (para el change de producción)
- `chaos-daemon` corre privilegiado y monta el socket de containerd. Con el
  `nodeSelector` queda confinado a los nodos del laboratorio.
- `clusterScoped: false` + `enableFilterNamespace: true` hacen imposible
  seleccionar pods fuera de `pg-chaos-lab` aunque un manifiesto lo intente.
- Desinstalación limpia: `kubectl delete -f chaos-mesh-rendered.yaml`.
