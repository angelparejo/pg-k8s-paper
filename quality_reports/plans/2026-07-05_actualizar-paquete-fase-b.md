# Plan — Actualizar el paquete Fase B con el reconocimiento real del clúster productivo

**Status:** COMPLETED (aprobado y ejecutado 2026-07-05)
**Fecha:** 2026-07-05

## Context

Durante esta sesión, en **modo desacoplado** (Claude genera comandos de solo-lectura, el usuario los ejecuta por VPN y pega la salida), reconocimos el clúster Kubernetes productivo real donde se ejecutará el piloto de Fase B. El paquete `paper/replication/paquete-ejecucion-fase-b/` se había escrito con **placeholders** y con **supuestos** que el reconocimiento ha refutado en tres puntos materiales:

1. **No son 3 clústeres CNPG productivos, sino 4 preexistentes.** El operador CNPG 1.28.0 (compartido) gestiona `pg-prod`, `pg-cert`, `pg-dev` y `gitlab/pg-gitlab`. El experimental sería el **5.º**, no el 4.º.
2. **Chaos Mesh 2.7.x es incompatible con el clúster real.** Corre Kubernetes **v1.34.6**; Chaos Mesh 2.7 solo soporta hasta K8s 1.28. Hay que subir a **Chaos Mesh v2.8.3** (soporta 1.30–1.35 e incluye los parches de seguridad "Chaotic Deputy").
3. **El nodo del lab (tcolp293) NO está vacío de bases de datos ajenas.** Co-aloja **3 primaries CNPG** (pg-cert-1, pg-dev-3, pg-gitlab-2). La barrera #2 y la compuerta G5, que asumían "ningún pod productivo en el nodo del lab", quedan **falsas** y darían NO-GO. Decisión del usuario: **mantener tcolp293** (es el worker nonprod designado por convención de ops) y **reescribir** la narrativa de seguridad para reconocer la co-tenencia honestamente.

**Resultado buscado:** el paquete queda instanciado para ESTE clúster (valores reales, versión correcta de Chaos Mesh) y su modelo de seguridad es verdadero respecto al entorno (co-tenencia reconocida; la contención descansa en filtro de namespace + doble selector + nombre único + dry-run G1, no en el aislamiento de nodo). Además se corrige la memoria del proyecto.

## Valores reales descubiertos (fuente de verdad para las sustituciones)

| Parámetro | Valor real |
|---|---|
| Kubernetes | v1.34.6 · RHEL 9.8 (Plow) · kernel 5.14 · containerd 2.2.4 |
| Operador CNPG | 1.28.0 · namespace `cnpg-operator` · deploy `cnpg-cloudnative-pg` (2/2) |
| Clústeres CNPG preexistentes (4) | `pg-prod/pg-prod` (3 inst, primary pg-prod-2) · `pg-cert/pg-cert` (2, primary pg-cert-1) · `pg-dev/pg-dev` (2, primary pg-dev-3) · `gitlab/pg-gitlab` (2, primary pg-gitlab-2) |
| Clasificación | pg-prod = producción · pg-gitlab = infra crítica (GitLab) · pg-cert, pg-dev = no productivos. **Término operativo: "preexistentes" (no tocar ninguno).** |
| StorageClass | `huawei-ch-xfs` (default) · `csi.huawei.com` · `reclaimPolicy: Retain` · `WaitForFirstConsumer` |
| Nodo del lab | `tcolp293` (worker, `storage=huawei-san`, `fc=true`, 64c/~503GiB, ocioso: 4% CPU / 2% mem) |
| Co-residentes ajenos en tcolp293 | primaries pg-cert-1, pg-dev-3, pg-gitlab-2 (+ ArgoCD, Harbor, Prometheus) |
| Chaos Mesh | **v2.8.3** (era 2.7.2) |
| Gobernanza | Kyverno inerte · Argo Rollouts ninguno · ArgoCD con apps `sar-suite-*` (no tocan `pg-*` ni el lab) · Linkerd activo pero **pg-\* NO meshado** |

## Cambios

### A. Rellenar placeholders con valores reales
Sustituir en `PROCEDIMIENTO.md` y `RESPONSABLES.md`:
- `<NS-OPERADOR>` → `cnpg-operator`
- `<SC-HUAWEI>` → `huawei-ch-xfs`
- `<WORKER-LAB>` → `tcolp293`
- `<NS-PROD-1> <NS-PROD-2> <NS-PROD-3>` (CHECKLIST G2.2, l.91) → **4 namespaces**: `pg-prod pg-cert pg-dev gitlab`
- Contexto de `kubectl` en RESPONSABLES → dejar en blanco (específico de la sesión del ejecutor).

### B. Reencuadre "3 productivos" → "4 preexistentes" (afecta README, SEGURIDAD, PROCEDIMIENTO, CHECKLIST, ABORTO, RESPONSABLES)
- "tres clústeres productivos" / "los 3 productivos" → **"los cuatro clústeres CNPG preexistentes"** (con nota única de clasificación prod/infra/no-prod donde tenga sentido narrativo).
- "cuarto clúster" (el experimental) → **"quinto clúster"** (README l.7, SEGURIDAD l.8, PROCEDIMIENTO l.4).
- G1.4 y SEGURIDAD l.25: "aparecen **4 primarios**" → "**5 primarios** (los 4 preexistentes + el experimental)".
- Tabla de inventario en `RESPONSABLES.md` (§ paso 0.7): pasar de 3 filas a **4 filas rellenas** con los datos reales de la tabla de valores; añadir nota "3 de estos primarios (pg-cert-1, pg-dev-3, pg-gitlab-2) co-residen hoy en tcolp293".
- Checklist de inventario en RESPONSABLES: el ítem "Ninguno tiene su primario en un nodo `pg-chaos-lab/member=true`" → **reformular** (ver C): con tcolp293 como nodo del lab, 3 primaries ajenos SÍ están ahí; el ítem correcto es "ninguno es objetivo de ningún manifiesto de fallo (garantizado por G1)".

### C. Reescritura semántica del modelo de seguridad (co-tenencia) — el cambio de fondo
- **SEGURIDAD.md, barrera #2 (l.19):** hoy dice que el chaos-daemon está confinado por `nodeSelector: pg-chaos-lab/member=true` y que "ningún pod productivo corre en los nodos del lab". Reescribir: el daemon sigue confinado a tcolp293, **pero tcolp293 co-aloja 3 primaries CNPG ajenos**. Por tanto la contención **no depende del aislamiento de nodo**; descansa en las barreras #1 (label de opt-in `chaos-mesh.org/inject` que los namespaces ajenos no tienen), #3 (doble selector namespace + `cnpg.io/cluster`) y #4 (nombre único), verificadas por el dry-run G1. Declarar la co-tenencia de forma explícita y por qué los vecinos están a salvo (el daemon solo actúa bajo instrucción del controlador, que solo emite recursos acotados a `pg-chaos-lab`; y ningún manifiesto los selecciona — G1).
- **CHECKLIST-GONOGO.md, G5 (l.152):** hoy es compuerta dura "ningún pod productivo en el nodo del lab" → con tcolp293 sería NO-GO. Reformular a: **inventariar** las cargas co-residentes en tcolp293 y **confirmar** que (a) ninguna es objetivo de ningún manifiesto de fallo (redundante con G1, que es la barrera real) y (b) los escenarios son estrictamente pod-scoped (F1/F2 pod-failure, F4 IOChaos-FUSE), sin fallos de nodo/StressChaos que pudieran alcanzar a los vecinos. Ajustar el comando para listar co-residentes y el "Esperado" en consecuencia.
- **CHECKLIST G1** (contexto, l.6) y **SEGURIDAD** "Riesgo único": añadir una línea de que el riesgo se agudiza porque 3 primaries ajenos comparten el nodo del lab → G1 es la barrera crítica.

### D. Subir Chaos Mesh 2.7.2 → v2.8.3 (compatibilidad K8s 1.34 + seguridad)
Editar las 5 ubicaciones halladas por grep:
- `PROCEDIMIENTO.md` l.234–238 (ctr import + helm template)
- `manifiestos/images/image-list.txt` l.11–14
- `README.md` l.36
- `manifiestos/10-chaos-mesh/INSTALL-offline.md` l.6–24
- `manifiestos/10-chaos-mesh/values-airgapped.yaml` l.1–2 (comentarios)
Añadir nota: "v2.8.3 es la última de la línea 2.8; verificar el último parche 2.8.x vigente al momento de instalar. Chaos Mesh 2.7 queda descartado (tope K8s 1.28)."

### E. Excluir Linkerd del laboratorio (edición de manifiestos)
- `manifiestos/00-namespace/01-namespace.yaml`: añadir anotación `linkerd.io/inject: disabled` (junto al opt-in de chaos-mesh).
- `manifiestos/20-cluster/cluster-cnpg.yaml`: añadir `linkerd.io/inject: disabled` vía `spec.inheritedMetadata.annotations` para que se propague a los pods de Postgres.
- Documentar en SEGURIDAD/PROCEDIMIENTO la justificación: **pg-\* no está meshado en producción → excluir linkerd COINCIDE con producción, sin salvedad de validez externa**; además evita contaminar la medición de RTO/latencia con un proxy en la ruta.
(Leer ambos manifiestos antes de editar para respetar su estructura actual.)

### F. Teardown de PV con reclaimPolicy Retain
- `ABORTO.md` y `RESPONSABLES.md` (cierre): añadir paso explícito "borrar los **PersistentVolumes liberados** tras eliminar los PVCs — la SC `huawei-ch-xfs` usa `reclaimPolicy: Retain`, así que los PV no se borran solos". Coordinar con almacenamiento.

### G. Corregir la memoria del proyecto
- `memory/project_testbed_operador_compartido.md`: cambiar "tres clústeres productivos" → "**4 clústeres CNPG preexistentes** (pg-prod producción; pg-gitlab infra; pg-cert/pg-dev no prod) + experimental = 5". Añadir: nodo del lab = tcolp293, que **co-aloja 3 primaries ajenos** → contención por filtro de namespace + selector + G1, **no** por aislamiento de nodo. Registrar valores reales (SC `huawei-ch-xfs`, operador ns `cnpg-operator`, K8s 1.34.6, Chaos Mesh 2.8.3). Actualizar la línea `description:` del frontmatter.
- `memory/MEMORY.md`: actualizar el gancho de esa entrada (menciona "3 clústeres productivos").

## Archivos que se modifican
```
paper/replication/paquete-ejecucion-fase-b/
  README.md               (B, D)
  SEGURIDAD.md            (B, C, E)
  PROCEDIMIENTO.md        (A, B, D, E, + nota entorno verificado)
  CHECKLIST-GONOGO.md     (A, B, C)
  ABORTO.md               (B, F)
  RESPONSABLES.md         (A, B, F, + parámetros de entorno)
  manifiestos/00-namespace/01-namespace.yaml   (E)
  manifiestos/20-cluster/cluster-cnpg.yaml     (E)
  manifiestos/10-chaos-mesh/INSTALL-offline.md (D)
  manifiestos/10-chaos-mesh/values-airgapped.yaml (D)
  manifiestos/images/image-list.txt            (D)
memory/project_testbed_operador_compartido.md  (G)
memory/MEMORY.md                                (G)
```

## Verificación (air-gapped: sin acceso al clúster desde aquí)
- `grep -rn '2\.7' paquete-ejecucion-fase-b/` → **cero** referencias a Chaos Mesh 2.7.
- `grep -rnoE '<[A-Z0-9-]+>' paquete-ejecucion-fase-b/` → **cero** placeholders `<WORKER-LAB>`/`<SC-HUAWEI>`/`<NS-OPERADOR>`/`<NS-PROD-*>` (queda solo el contexto kubectl si se deja marcado como TBD del ejecutor).
- `grep -rniE 'tres cl|3 cl[uú]|3 productiv|cuarto cl|4 primarios'` → sin residuos del encuadre viejo.
- Pasada de consistencia cruzada de nombres: `pglab-cnpg-exp`, `tcolp293`, `huawei-ch-xfs`, `cnpg-operator`, "5 primarios", "4 preexistentes" sin variantes.
- Manifiestos YAML editados (E): validar sintaxis releyéndolos; la validación real (`kubectl apply --dry-run=client`) ocurre en la Ventana 1 del ejecutor.
- Registrar la sesión en `SESSION_REPORT.md` y `research_journal.md` al cerrar.

## Fuera de alcance (seguimiento posterior)
- **No** se edita el artículo (`articulo_angelparejov2-experimental.md`) en esta pasada: la descripción del testbed real (nodo, K8s 1.34, storage Huawei, 4 clústeres, linkerd) se incorporará a la Sección IV.E cuando se prepare la Sección V con datos del piloto.
- **No** se ejecuta nada contra el clúster (sigue el modo desacoplado; el ejecutor corre el piloto en las 3 ventanas).
- Los roles de `RESPONSABLES.md` (nombres/contactos) y las fechas de ventana los rellena el usuario en su entorno.
