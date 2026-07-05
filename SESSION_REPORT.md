# Session Report — clo-author

<!-- NOTA: el encabezado y la entrada de 2026-05-08 debajo son contenido heredado del scaffold
     clo-author original (no son historial de este proyecto, pg-k8s-paper). Se dejan intactos;
     limpiar si se desea. Las entradas de pg-k8s-paper empiezan en 2026-07-04. -->

## 2026-07-05 — Paquete de ejecución Fase B (piloto CNPG para terceros)

**Operations:**
- Leído completo el kit `paper/replication/pg-chaos-lab.zip` (49 archivos) como base
- Creado `paper/replication/paquete-ejecucion-fase-b/` — paquete de ejecución para terceros (Camino B: piloto SOLO CloudNativePG, sin operador nuevo)
- 6 documentos: README.md, PROCEDIMIENTO.md, SEGURIDAD.md, CHECKLIST-GONOGO.md, ABORTO.md, RESPONSABLES.md
- `manifiestos/` adaptado: renombrado `pg-cnpg`→`pglab-cnpg-exp` en todos los manifiestos/servicios/secret; excluido todo Zalando; cuota reducida a 1 clúster; run-experiment.sh variante solo-CNPG
- Auditoría de selectores: 6/6 experimentos doblemente acotados (namespace + `cnpg.io/cluster`)

**Decisions:**
- Nombre único del clúster experimental: `pglab-cnpg-exp` (evita colisión con los 3 clústeres CNPG productivos que comparten el operador)
- Riesgo #1 (inyección alcanza producción) contenido por 4 barreras: Chaos Mesh clusterScoped=false+enableFilterNamespace, chaos-daemon nodeSelector al lab, doble filtro en cada manifiesto, nombre único
- 3 adiciones sobre lo pedido en turno previo: paso 0.9 snapshot línea base, Fase 6.3 diff de igualdad final producción, sección Planificación de Ventanas (V1 setup+F1+F3 ~4h / V2 F4 ~7h / V3 F2 ~2.5h) con reentrada R1-R6

**Results:**
- Paquete completo (26 archivos) verificado; CHECKLIST-GONOGO mostrado al usuario y aprobado
- NO ejecutado — es documentación + manifiestos para que otra área lo corra

**Commits:**
- `[pendiente]` Añade paquete de ejecución Fase B (piloto CNPG aislado) para terceros

**Status:**
- Done: paquete de ejecución Fase B listo para entregar al área ejecutora
- Pending: ejecución del piloto (3 ventanas) → rellenar Sección V de `articulo_angelparejov2-experimental.md` con RTO/RPO reales. **La v2 sigue NO sometible hasta entonces.**

## 2026-07-05 — Creación de la versión experimental v2 (bifurcación de línea)

**Operations:**
- Creado `articulo_angelparejov2-experimental.md` como copia byte-idéntica de `articulo_angelparejov1-6.md` (v1-6 conceptual verificada intacta en git)
- Revertido el reencuadre Ruta B: título a Opción 3 ("Análisis Multicapa… Evaluación Empírica de Recuperación y Consistencia bajo Fallos Inyectados"); resumen (137 palabras), introducción (contribución 5 + disclaimer conceptual) y conclusiones reencuadrados a estudio empírico
- IV.E reclasificada de "Diseño experimental propuesto" a "Metodología experimental" (tiempos verbales propuesto→ejecutado)
- Añadida Sección V. Resultados como plantilla vacía (Tabla II, Figura 2, contraste predicho-vs-observado — todos "pendiente de ejecución", sin datos inventados); Discusión→VI, Conclusiones→VII
- Corregidos residuos de "validación futura" en II, III.C, III.D, IV.D
- Entrada añadida al research journal (2026-07-05 08:30 — Writer)

**Decisions:**
- Título Opción 3 elegido por el usuario — conserva el espinazo de la v1-6 para reforzar el vínculo de publicación secuencial entre ambos artículos
- v2 es una LÍNEA EXPERIMENTAL SEPARADA: la v1-6 conceptual sigue siendo la versión lista para el tier primario; la v2 espera datos del piloto
- Honestidad de alcance conservada y reforzada: el fallo de nodo NO se reproduce (clúster productivo sin drenaje de nodos), se aproxima con pod-failure sostenido (escenario ii) = cota inferior del RTO; explícito en IV.E, V.A y limitaciones de VI

**Results:**
- `articulo_angelparejov2-experimental.md` completa como plantilla empírica; numeración I–VII coherente; 6 referencias pendientes ([5][10][11][14][15]) heredadas sin re-verificar

**Commits:**
- `[pendiente]` Crea versión experimental v2: revierte framing a estudio empírico, añade plantilla de Sección V Resultados

**Status:**
- Done: v2 experimental creada, registrada y reencuadrada; v1-6 conceptual intacta
- Pending: **La v2 NO es sometible hasta ejecutar el piloto (`paper/replication/pg-chaos-lab.zip`) y rellenar la Sección V con RTO/RPO reales.** Dashboard sin actualizar (pospuesto a petición del usuario)

## 2026-07-04 — Reorientación del scaffold + peer review simulado + revisión conceptual v1-6

**Operations:**
- Reorientado el scaffold de economía empírica a sistemas distribuidos / infraestructura cloud-native: `CLAUDE.md`, `.claude/references/domain-profile.md` reescritos; `README-PROYECTO.md` creado (README.md del scaffold intacto)
- Preferencia de idioma establecida: comunicación en español, paper en español, traducción al inglés como fase final
- Copiados `articulo_angelparejov1-5.docx` (raíz) y `paper/replication/pg-chaos-lab.zip` al proyecto
- Extraído el texto del .docx (script Python stdlib, sin dependencias externas) para su lectura
- Peer review simulado (`/review --peer`, tier primario): editor (desk review) + 2 árbitros ciegos (escéptico/metodológico, sistemas/reproducibilidad) + decisión editorial — reportes en `quality_reports/reviews/`
- Plan de revisión creado y ejecutado (`quality_reports/plans/2026-07-04_plan-revision-articulo-v1-5.md`): 7 MUST + 8 SHOULD rutados por sección, todos aplicados en bloques revisados uno a uno sobre `articulo_angelparejov1-6.md` (copia de trabajo; v1-5.docx intacto)
- Decisión M1 tomada: Ruta B (reencuadre de framing, no piloto empírico) por acceso incierto al clúster productivo — título, resumen, introducción, discusión y conclusiones reencuadrados como marco conceptual + protocolo experimental reproducible, sin insinuar resultados
- Verificadas por búsqueda web las 23 referencias del artículo: 18 volcadas limpias a `Bibliography_base.bib` ([1],[2],[4],[6]-[9],[12],[13],[16]-[23]); 6 problemáticas ([3] débil, [5],[10],[11],[14],[15] con errores de existencia/autoría/venue) documentadas con mapa de impacto en `quality_reports/referencias_por_verificar.md`
- `.gitignore` actualizado para excluir artefactos Windows (`Zone.Identifier`, `mshield`)
- Dashboard regenerado (`project_dashboard.html`)

**Decisions:**
- Ruta B sobre Ruta A para M1 — el acceso al clúster productivo es incierto; reencuadrar permite someter ya sin bloquear en un piloto que podría no poder ejecutarse pronto
- Trabajar sobre copia (`articulo_angelparejov1-6.md`) en vez del `.docx` original, para preservar v1-5 intacto como referencia histórica
- Separar referencias verificadas (`.bib`) de las problemáticas (`referencias_por_verificar.md`) en vez de mezclarlas o "arreglarlas" silenciosamente

**Results:**
- Peer review: Revisión Mayor, sin objeciones FATALES, ambos árbitros convergen sin verse entre sí
- 16/16 correcciones mecánicas + decisión M1 resueltas — plan de revisión CERRADO
- 6 referencias bibliográficas identificadas como bloqueantes para someter (2 de autoría/venue incorrectos, incluyendo un caso de venue con prestigio editorial muy superior al real)

**Commits:**
- `888c1e8` Reconfigura scaffold: dominio sistemas distribuidos, idioma español, datos del proyecto
- `02584aa` Peer review simulado v1-5 y revisión conceptual v1-6 del artículo

**Status:**
- Done: artículo v1-6 conceptual completo y reencuadrado; peer review y plan de revisión cerrados; 18/23 referencias verificadas
- Pending: resolver las 6 referencias de `quality_reports/referencias_por_verificar.md` antes de someter; conversión de formato (LaTeX o Word según la revista objetivo) queda para la próxima sesión

## 2026-05-08 — HTML Dashboard Pipeline + Guide Overhaul (v4.3.0)

**Operations:**
- Built `scripts/generate_html_report.py` — 5 subcommands (peer-review, code-audit, strategy-review, quality-gate, literature)
- Built `scripts/generate_dashboard.py` — project-level HTML dashboard
- Created `templates/html/base/styles.css` + `components.js` — shared thariqs design system
- Created `quality_reports/demo/` — demo markdown + 6 generated HTML files
- Created `quality_reports/demo/annotated_bibliography.md` — 12-paper demo for literature subcommand
- Wired HTML generation into skills: `/review`, `/analyze`, `/strategize`, `/discover lit`, `/submit final`, `/checkpoint`, `/tools dashboard`
- Rewrote `guide/custom.scss` — cyberpunk neon → thariqs ivory/clay/serif
- Created `guide/custom-dark.scss` — thariqs dark theme for Quarto dual-theme toggle
- Updated `guide/_quarto.yml` — switched base from `darkly` to `cosmo`, added light/dark toggle
- Updated 6 mermaid diagrams across `user-guide.qmd`, `architecture.qmd`, `customization.qmd`
- Readability pass on `user-guide.qmd`, `agents.qmd`, `architecture.qmd`, `changelog.qmd`
- Added v4.3.0 changelog entry
- Rendered all 7 guide pages successfully

**Decisions:**
- Literature report designed as "self-contained Zotero" per user request — filterable by category/proximity/method, sortable, searchable, with copy-cite buttons
- Guide site dark toggle via Quarto's native `light:`/`dark:` theme config rather than custom JS
- Removed "Multi-Model Strategy" section from agents.qmd (architecture topic, not agents)
- Removed duplicate "How It Works" table from user-guide.qmd (already on index page)

**Results:**
- All 5 HTML report subcommands verified against demo data
- Guide site builds cleanly (7/7 pages)
- Zero cyberpunk remnants in guide source files
- Dark/light toggle functional in navbar

**Commits:**
- None yet — all changes uncommitted

**Status:**
- Done: Phases A-F of HTML dashboard pipeline complete (v4.3.0 scope)
- Pending: Commit + deploy to GitHub Pages

## 2026-07-05 15:40 — Endurecimiento de seguridad G1 (compuerta GO/NO-GO, paquete Fase B)

**Operations:**
- Creado `paper/replication/paquete-ejecucion-fase-b/manifiestos/scripts/dry-run-selectores.py` (chmod +x, stdlib + kubectl, sin yq).
- Reescrito bloque G1 de `paper/replication/paquete-ejecucion-fase-b/CHECKLIST-GONOGO.md` (G1.2 autoritativo; G1.1/G1.3/G1.4 de apoyo; G1.5 semántica de F3).
- Corregida descripción de `scripts/` en `README.md` del paquete (pasada de consistencia cruzada).
- Actualizado `quality_reports/research_journal.md` (entrada Coder 15:32).

**Decisions:**
- Dry-run derivado del manifiesto (no tecleado por el operador) — el enlace manifiesto→pods debe ser mecánico, no transcripción humana.
- Rechazo por precaución ante mecanismos de selección no previstos (expressionSelectors, pods:, matchExpressions) — la ausencia no se lee como seguridad.
- `--dry-run=client` como primario (evita webhook), `--dry-run=server` como fallback documentado.
- Numeración G1.x mantenida estable para no romper referencias en SEGURIDAD/PROCEDIMIENTO.

**Results:**
- Hueco de G1 cerrado: un manifiesto alterado (2º namespace, nombre de clúster cambiado, rol aislado) ahora se detecta antes de inyectar.
- Consistencia cruzada verificada: nombres (`pglab-cnpg-exp`, `pg-chaos-lab/member=true`) sin variantes; única desalineación (README) corregida.
- Paquete Fase B declarado completo y entregable. Salvedad: script validado sintácticamente, no ejecutado contra clúster real (air-gap) — primera corrida en Ventana 1 es parte del ensayo.

**Commits:**
- `8b415be` Cierra hueco G1: dry-run de selectores derivado del manifiesto en la compuerta GO/NO-GO
- `0fe8987` README: registra el dry-run de selectores en el inventario de scripts/

**Status:**
- Done: endurecimiento G1, consistencia cruzada, paquete Fase B entregable.
- Pending: (entorno del usuario) rellenar RESPONSABLES.md (G9), placeholders <NS-PROD-1..3>/<WORKER-LAB> en Fase 0; ejecución real del piloto en las 3 ventanas.

## 2026-07-05 21:35 — Reconocimiento desacoplado del clúster real + instanciación del paquete Fase B

**Operations:**
- Reconocimiento en **modo desacoplado** (Claude genera comandos solo-lectura; usuario ejecuta por VPN y pega salida): 4 rondas (versión/nodos/namespaces/operador · etiquetas/taints/carga · gobernanza/co-tenencia/ubicación CNPG · recursos del nodo).
- WebSearch/WebFetch de compatibilidad Chaos Mesh ↔ K8s 1.34 (chaos-mesh.org/supported-releases + GitHub releases).
- Plan aprobado: `quality_reports/plans/2026-07-05_actualizar-paquete-fase-b.md`.
- Editados 11 archivos del paquete `paper/replication/paquete-ejecucion-fase-b/`: README, SEGURIDAD, PROCEDIMIENTO, CHECKLIST-GONOGO, ABORTO, RESPONSABLES + manifiestos (00-namespace/01-namespace.yaml, 20-cluster/cluster-cnpg.yaml, 10-chaos-mesh/INSTALL-offline.md, 10-chaos-mesh/values-airgapped.yaml, images/image-list.txt).
- Corregida memoria: `project_testbed_operador_compartido.md` + gancho `MEMORY.md`.

**Hallazgos del reconocimiento (clúster real):**
- K8s v1.34.6 · RHEL 9.8 · containerd 2.2.4 · 8 nodos (3 control-plane + 5 workers).
- Operador CNPG 1.28.0 en `cnpg-operator`, gestiona **4 clústeres CNPG** (no 3): pg-prod (prod, primary pg-prod-2), pg-cert, pg-dev, gitlab/pg-gitlab.
- Nodo del lab = **tcolp293** (worker, huawei-san/fc, ocioso 4% CPU/2% mem) — pero **co-aloja 3 primaries ajenos** (pg-cert-1, pg-dev-3, pg-gitlab-2) + ArgoCD/Harbor/Prometheus.
- SC única `huawei-ch-xfs` (default, Retain, WaitForFirstConsumer). Kyverno inerte; Argo Rollouts ninguno; ArgoCD con apps sar-suite (no tocan pg-*/lab); Linkerd activo pero pg-* NO meshado.

**Decisions:**
- Mantener tcolp293 como worker-lab (worker nonprod designado) pese a la co-tenencia — decisión del usuario. → Reescribir barrera #2 y G5 (contención por G1 + filtro namespace, no por aislamiento de nodo).
- Chaos Mesh 2.7.2 → **v2.8.3** (2.7 tope K8s 1.28; 2.8 soporta 1.34; parches "Chaotic Deputy").
- Excluir Linkerd del lab (`linkerd.io/inject: disabled` en namespace + inheritedMetadata) — coincide con prod, sin salvedad de validez externa.
- Framing "3 productivos" → "4 preexistentes"; experimental = 5.º clúster; "4 primarios" → "5".
- Teardown: borrar PV liberados (SC Retain).

**Results:**
- Paquete instanciado para ESTE clúster con valores reales; modelo de seguridad ahora verdadero respecto a la co-tenencia.
- Verificación: 0 placeholders, 0 residuos de encuadre viejo, YAML parsea (namespace + cluster). Salvedad: no ejecutado contra clúster (air-gap); validación `--dry-run` real es de la Ventana 1.

**Commits:**
- Ninguno aún — cambios sin commitear (pendiente decisión del usuario).

**Status:**
- Done: reconocimiento (4 rondas), plan aprobado, 11 archivos del paquete + memoria actualizados y verificados.
- Pending: commit (a decidir); rellenar roles/fechas en RESPONSABLES.md (entorno del usuario); reconfirmar ubicación de pods en paso 0.7 (puede cambiar); ejecución del piloto en las 3 ventanas.

## 2026-07-05 22:30 — Testbed real al paper v2 (IV.E) + verificación de versiones

**Operations:**
- Editada §IV.E de `articulo_angelparejov2-experimental.md` (solo correcciones factuales scope-neutrales; el marco de 2 operadores NO se tocó por decisión del usuario).
- Ronda 5 de recon desacoplado: verificación de versiones CSI Huawei y Calico.
- Commits `684d495` (IV.E), `55f5af9` (verificación de versiones).

**Decisions:**
- Aplicar solo correcciones factuales a IV.E ahora; **diferir** la decisión de alcance de operadores (CNPG-solo vs 2 operadores) — el usuario eligió "solo correcciones factuales".
- Chaos Mesh 2.7.x → 2.8.3 en IV.E; añadidos provisioner `csi.huawei.com` + SC (`Retain`, `WaitForFirstConsumer`); párrafo de aislamiento enriquecido (nodo co-residente → contención por namespaced+doble filtro+dry-run; Linkerd excluido).

**Results:**
- Versiones de IV.E **verificadas y correctas**: Huawei CSI **4.10.1** (imágenes `huawei-csi:4.10.1` + backends), Calico **v3.31.4** (`clusterinformation.calicoVersion`). No requirió corrección.
- `csi.huawei.com` con `ATTACHREQUIRED: true` → corrobora que detach/attach domina el RTO en fallo de nodo real (respalda que el escenario (ii) sea cota inferior). Tigera operator v1.40.7.

**Commits:**
- `684d495` IV.E (v2): correcciones factuales del testbed real (sin tocar alcance de operadores)
- `55f5af9` Verifica versiones CSI/Calico de IV.E contra el clúster real (coinciden)

**Status:**
- Done: IV.E con testbed real (factual), versiones CSI/Calico verificadas, todo commiteado (árbol limpio).
- Pending (🔴 decisión abierta): **alcance de operadores** — el v2 afirma comparación empírica de 2 operadores pero el piloto ejecutable es solo CNPG (no hay Zalando en el clúster productivo). Resolver antes de someter. Además: roles/fechas de RESPONSABLES.md y ejecución del piloto (entorno del usuario).
