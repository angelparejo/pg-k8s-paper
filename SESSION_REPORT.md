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
