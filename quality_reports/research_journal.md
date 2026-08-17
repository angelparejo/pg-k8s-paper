# Research Journal

### 2026-07-05 22:25 — Reconocimiento (Ronda 5: verificación de versiones CSI/Calico)
**Phase:** Execution (recon desacoplado, solo-lectura)
**Target:** articulo_angelparejov2-experimental.md §IV.E (hilo abierto 🟡)
**Score:** N/A
**Verdict:** Verificadas contra el clúster real las dos versiones que quedaban asertadas sin confirmar en IV.E: **Huawei CSI = 4.10.1** (imágenes `huawei-csi:4.10.1`, `storage-backend-controller/sidecar/extender:4.10.1`) y **Calico = v3.31.4** (`clusterinformation.spec.calicoVersion` + `calico-node:v3.31.4`). **Ambas COINCIDEN** con IV.E → no requiere corrección; hilo cerrado. Dato adicional corroborante: el CSIDriver `csi.huawei.com` declara `ATTACHREQUIRED: true`, lo que respalda empíricamente el argumento de IV.E/VI de que la latencia de detach/attach del volumen dominaría el RTO en un fallo de nodo real (justificando que el escenario (ii) sea una cota inferior). Tigera operator v1.40.7.
**Report:** journal (recon; sin cambios en el paper)

### 2026-07-05 22:05 — Writer (correcciones factuales del testbed real en IV.E del v2)
**Phase:** Execution (re-entrada por hallazgos del reconocimiento)
**Target:** articulo_angelparejov2-experimental.md §IV.E
**Score:** N/A
**Verdict:** Llevadas al paper solo las **correcciones factuales scope-neutrales** del reconocimiento (decisión del usuario: no tocar aún el alcance de operadores): (1) Chaos Mesh 2.7.x → **2.8.3** (compatibilidad K8s 1.34); (2) storage — añadidos provisioner `csi.huawei.com` y propiedades verificadas de la SC (`Retain`, `WaitForFirstConsumer`); (3) párrafo de aislamiento enriquecido con hechos verificados: nodo dedicado que co-aloja otras cargas → la contención descansa en Chaos Mesh namespaced + doble filtro + dry-run de selectores (no en exclusividad de nodo), y exclusión de Linkerd (coincide con prod: pg-* no meshado). **DECISIÓN DIFERIDA (abierta):** el paper afirma comparación empírica de 2 operadores (CNPG + Zalando) pero el piloto Fase B ejecutable es SOLO CNPG (no hay Zalando en el clúster productivo, no se puede instalar). Pendiente resolver: piloto CNPG + Zalando analítico, o segundo entorno para Zalando. **Sin verificar (versiones asertadas en IV.E):** Huawei CSI 4.10.1 y Calico 3.31.4 — se pueden confirmar en una ronda de recon.
**Report:** articulo_angelparejov2-experimental.md §IV.E (líneas 146, 148)

### 2026-07-05 21:35 — Coder/Data-engineer (instanciación del paquete Fase B con reconocimiento real del clúster)
**Phase:** Execution (preparación del piloto empírico para la v2)
**Target:** paper/replication/paquete-ejecucion-fase-b/ (11 archivos) + memory/
**Score:** N/A (documentación/manifiestos; no ejecutado contra clúster)
**Verdict:** Reconocido el clúster productivo real en **modo desacoplado** (solo-lectura; el usuario ejecutó por VPN y pegó salidas) y actualizado el paquete Fase B en consecuencia. Tres refutaciones materiales de los supuestos previos: (1) **no son 3 clústeres productivos sino 4 CNPG preexistentes** (pg-alfa, pg-beta, pg-gamma, ns-delta/pg-delta); el experimental es el 5.º. (2) **Chaos Mesh 2.7.x es incompatible** con K8s v1.34.6 → subido a **v2.8.3** (soporta 1.30–1.35; parches "Chaotic Deputy"; verificado por WebSearch/WebFetch en chaos-mesh.org). (3) El nodo del lab **nodo-lab-01 co-aloja 3 primaries CNPG ajenos** (pg-beta-1, pg-gamma-3, pg-delta-2) → la barrera #2 y G5 (que asumían "nodo vacío") se **reescribieron**: la contención descansa en filtro de namespace + doble selector + nombre único + dry-run G1, no en aislamiento de nodo (decisión del usuario: mantener nodo-lab-01). Además: placeholders resueltos (`cnpg-operator`, SC `huawei-ch-xfs` con reclaimPolicy Retain → teardown de PV a mano, nodo `nodo-lab-01`); Linkerd excluido del lab vía `linkerd.io/inject: disabled` en namespace + `inheritedMetadata` del clúster (coincide con prod: pg-* no meshado → sin salvedad de validez externa). Verificado: 0 placeholders, 0 residuos de encuadre viejo, YAML parsea. Memoria del proyecto corregida.
**Report:** quality_reports/plans/2026-07-05_actualizar-paquete-fase-b.md (plan aprobado) · paper/replication/paquete-ejecucion-fase-b/

### 2026-07-05 15:32 — Coder (mejora de seguridad — compuerta GO/NO-GO)
**Phase:** Execution
**Target:** paper/replication/paquete-ejecucion-fase-b/ (CHECKLIST-GONOGO.md, manifiestos/scripts/dry-run-selectores.py)
**Score:** N/A
**Verdict:** Cerrado hueco en G1 del checklist GO/NO-GO. El dry-run de selectores dependía de transcripción manual (el operador tecleaba el selector, no se leía del manifiesto), por lo que un manifiesto alterado —segundo namespace, nombre de clúster cambiado, rol aislado— habría pasado inadvertido. Nuevo `dry-run-selectores.py` (solo stdlib + kubectl, sin yq) extrae el selector del propio YAML vía `kubectl create --dry-run=client -o json`, lo valida, y `verify_pods` comprueba los pods reales como red final; rechaza por precaución cualquier mecanismo de selección no previsto (expressionSelectors, pods:, etc.). G1.2 reescrito como ítem autoritativo; G1.1/G1.3/G1.4 quedan como apoyo. Crítico dado el riesgo del escenario: operador CNPG compartido entre 3 clústeres productivos y el experimental.
**Report:** commit descriptivo (ver git log); paper/replication/paquete-ejecucion-fase-b/CHECKLIST-GONOGO.md §G1

### 2026-07-04 09:00 — Editor (desk review)
**Phase:** Peer Review
**Target:** articulo_angelparejov1-5.docx — tier primario (CLEI/RISTI/Ingeniare/Computación y Sistemas)
**Score:** N/A
**Verdict:** ENVIAR A ÁRBITROS — aporte claro, sin falla fatal visible; la ausencia de validación empírica se deja como eje central para arbitraje, no motivo de desk reject.
**Report:** quality_reports/reviews/2026-07-04_desk_review.md

### 2026-07-04 09:10 — domain-referee-equivalente (Escéptico/Metodológico)
**Phase:** Peer Review
**Target:** articulo_angelparejov1-5.docx
**Score:** 57/100
**Verdict:** Revisión Mayor — el modelo formal S=(O,K,C,D) no realiza trabajo analítico operacional; colisión de notación (C) e inconsistencia (K ausente de I(S)); sin experimentos ejecutados.
**Report:** quality_reports/reviews/2026-07-04_referee_esceptico_metodologico.md

### 2026-07-04 09:15 — methods-referee-equivalente (Sistemas/Reproducibilidad)
**Phase:** Peer Review
**Target:** articulo_angelparejov1-5.docx
**Score:** 58/100
**Verdict:** Revisión Mayor — diseño experimental de IV.E no reproducible tal como está redactado (falta nombrar herramienta de inyección de fallos, mecanismo de latencia sobre SAN/FC, parámetros de carga); Tabla I técnicamente plausible.
**Report:** quality_reports/reviews/2026-07-04_referee_sistemas_reproducibilidad.md

### 2026-07-04 09:20 — Editor (decisión editorial)
**Phase:** Peer Review
**Target:** articulo_angelparejov1-5.docx
**Score:** N/A
**Verdict:** REVISIÓN MAYOR. Sin objeciones FATALES. Ambos árbitros convergen sin verse entre sí (57/58, mismo diagnóstico central). Hallazgo propio: `paper/replication/pg-chaos-lab.zip` ya resuelve técnicamente varias dudas de reproducibilidad de los árbitros (Chaos Mesh 2.7.x, IOChaos vía FUSE, pgbench, Zalando v1.13.x/Spilo 16) — falta trasladarlo al texto, no rediseñar el experimento.
**Report:** quality_reports/reviews/2026-07-04_editorial_decision.md

### 2026-07-04 10:30 — Fase mecánica de revisión (7 MUST + 8 SHOULD + afiliación)
**Phase:** Peer Review (post-decisión, fase mecánica)
**Target:** articulo_angelparejov1-6.md (copia de trabajo; v1-5.docx intacto)
**Score:** N/A
**Verdict:** 16/16 ítems mecánicos resueltos por bloques revisados y aprobados uno a uno: M6 (colisión de notación C→M), M7 (K incluido en I(S) con justificación), S1 (f(·) declaradas organizativas), M8 (literatura chaos engineering/Jepsen — corregida cita Jepsen de Kingsbury a Alvaro&Tymon 2018), M2-M5 (Chaos Mesh, FUSE/SAN, pgbench, versión Zalando), S2-S3 (n=10 honesto, fallo de nodo como cota inferior de RTO), S4-S8 (docs oficiales, fila de Tabla I conectada a I(S), NTP, alcance 2 vs 3 operadores, comparación con industria), afiliación corregida a Valencia/Universidad de Carabobo. Referencias [16]-[23] añadidas al texto y a Bibliography_base.bib (verificadas por WebSearch antes de incorporarlas).
**Report:** quality_reports/plans/2026-07-04_plan-revision-articulo-v1-5.md (sección "Estado")

### 2026-07-04 11:15 — Decisión M1 y reencuadre de framing (Ruta B)
**Phase:** Peer Review (cierre del ciclo de revisión)
**Target:** articulo_angelparejov1-6.md
**Score:** N/A
**Verdict:** M1 resuelto vía Ruta B (reencuadre, no piloto) por acceso incierto al clúster productivo. Título cambiado a "Hacia un Análisis Multicapa de Operadores de PostgreSQL y Almacenamiento CSI en Kubernetes: Taxonomía, Modelo Formal y Protocolo Experimental Reproducible". Resumen, Introducción, Discusión y Conclusiones reencuadrados para declarar el aporte como marco conceptual + protocolo reproducible, sin insinuar resultados empíricos. Estrategia de publicación secuencial documentada en el plan: v1-6-conceptual se somete ahora al tier primario; segundo artículo futuro con piloto empírico deberá citar a este explícitamente (evitar salami slicing). Plan de revisión CERRADO — 16/16 ítems mecánicos + M1 resueltos.
**Report:** quality_reports/plans/2026-07-04_plan-revision-articulo-v1-5.md (sección "Cierre del plan")

### 2026-07-05 08:30 — Writer (creación de la versión experimental v2)
**Phase:** Execution (re-entrada por bifurcación de versión)
**Target:** articulo_angelparejov2-experimental.md (copia de v1-6; v1-6 conceptual intacta)
**Score:** N/A
**Verdict:** Creada la rama EMPÍRICA a partir de la v1-6 conceptual. Hereda sin cambios: notación S=(O,K,M,D), I(S)=f(O×K×M×D), C(S) sin colisión, Tabla I + fila ligada a I(S), cuerpo técnico de IV.E (Chaos Mesh 2.7.x, FUSE/SAN, pgbench, Zalando v1.13.x/Spilo 16, NTP, escenarios i/ii/iii, IOChaos 0-100 ms, n=10, Mann-Whitney/Kruskal-Wallis/Spearman), literatura chaos [16]-[18], industria [22]-[23], docs oficiales [19]-[21], afiliación Valencia/UC, y las 6 referencias pendientes [5][10][11][14][15] (mismo estado, no re-verificadas). Revertido el reencuadre Ruta B: título Opción 3 ("Análisis Multicapa… Evaluación Empírica de Recuperación y Consistencia bajo Fallos Inyectados"), resumen (137 palabras) + introducción + conclusiones reencuadrados a estudio empírico, IV.E reclasificada de "Diseño experimental propuesto" a "Metodología experimental" (tiempos verbales propuesto→ejecutado), residuos de "validación futura" corregidos en II/III.C/III.D/IV.D. Añadida Sección V. Resultados como PLANTILLA VACÍA (Tabla II, Figura 2, contraste predicho-vs-observado — todos "pendiente de ejecución", sin datos inventados); Discusión→VI, Conclusiones→VII. Honestidad de alcance conservada y reforzada: fallo de nodo NO reproducido (clúster productivo sin drenaje de nodos), aproximado con pod-failure sostenido (escenario ii) = cota inferior del RTO, explícito en IV.E, V.A y limitaciones de VI. NO se somete hasta tener datos del piloto.
**Report:** articulo_angelparejov2-experimental.md

### 2026-07-05 10:15 — Coder/Data-engineer (paquete de ejecución Fase B, piloto CNPG)
**Phase:** Execution (preparación del piloto empírico para la v2)
**Target:** paper/replication/paquete-ejecucion-fase-b/
**Score:** N/A (no ejecutado; paquete para terceros)
**Verdict:** Preparado el PAQUETE DE EJECUCIÓN PARA TERCEROS del Camino B (piloto SOLO CloudNativePG, sin instalar operador nuevo). Contexto crítico: el operador CNPG 1.28.0 ya gestiona TRES clústeres productivos; el piloto crea un CUARTO clúster aislado (`pglab-cnpg-exp`, nombre único propuesto y aprobado) gestionado por ese operador compartido. Riesgo #1: que la inyección alcance los pods productivos. Partí del kit `pg-chaos-lab.zip` (leído completo, 49 archivos). Auditoría de selectores: los 6 manifiestos de fallo CNPG ya estaban doblemente acotados (namespace pg-chaos-lab + cnpg.io/cluster); ninguno usa el label de rol aislado. Adaptaciones: renombrado pg-cnpg→pglab-cnpg-exp en todos los manifiestos/servicios/secret, excluido todo Zalando (Camino B), cuota reducida a 1 clúster. Paquete (6 docs + manifiestos/): README, PROCEDIMIENTO (Fase 0-6 + paso 0.9 snapshot estado-inicial.txt + Fase 6.3 diff de igualdad final + sección Planificación de Ventanas V1/V2/V3 con reentrada R1-R6), SEGURIDAD (4 barreras de aislamiento), CHECKLIST-GONOGO (G1 dry-run de selectores + G3 prueba cross-namespace + G4-G9), ABORTO (señales + reversión por fase), RESPONSABLES (roles + inventario productivo + hoja de registro). Fraccionamiento en 3 ventanas (~12-14h totales). NO ejecutado. Alimentará la Sección V de la v2-experimental cuando se corra.
**Report:** paper/replication/paquete-ejecucion-fase-b/PROCEDIMIENTO.md

### 2026-07-07 18:02 — Coder/Data-engineer (piloto Fase B, Ventana 2 F4)
**Phase:** Execution (piloto empírico CNPG, modo desacoplado)
**Target:** F4 (IOChaos latencia E/S) sobre pglab-cnpg-exp; quality_reports/results_summary.md
**Score:** N/A (experimento no ejecutable — bloqueo confirmado)
**Verdict:** F4 NO ejecutable: IOChaos/FUSE (toda) incompatible con readOnlyRootFilesystem:true de CNPG (`Read-only file system, os error 30`, AllInjected=False; baseline 0ms == 100ms). Config correcta y dry-run OK → incompatibilidad estructural hardening↔tooling, no bug. DECIDIDO (opción 1): reformular como hallazgo, dropear medición empírica; a trabajo futuro con mecanismo sin FUSE. La validación de 1 corrida (Opción A) atrapó el bloqueo antes del lote. Lab limpio y entre-ventanas; 4 preexistentes intactos. Pendiente: F2 (Ventana 3), escritura del hallazgo, Fase 6.
**Report:** quality_reports/results_summary.md (secc. Ventana 2); memoria project_f4_iochaos_readonly_incompat

### 2026-07-07 19:36 — Coder/Data-engineer (piloto Fase B, Ventana 3 F2 + Fase 6 + cierre)
**Phase:** Execution (piloto empirico CNPG, modo desacoplado)
**Target:** F2 pod-failure n=10; Fase 6 (RTO/RPO); teardown; reencuadre v2-experimental
**Score:** N/A (ejecucion empirica)
**Verdict:** F2 0/10 promociones (recreacion en sitio), RTO mediana 36.75s; RPO GLOBAL=0 (truth contiguo 1..613253). Piloto CERRADO con teardown total (produccion intacta). Alcance de operadores resuelto (restriccion externa) -> reencuadre a estudio en profundidad de CNPG. Bug ARG_MAX en parse-verifier.py (RPO) documentado + workaround.
**Report:** quality_reports/results_summary.md; reframe_v2_cnpg_alcance.md; claim_source_map_pg-k8s-paper.md

### 2026-07-08 05:00 — Writer + Editor + Domain/Methods referees (v2-experimental)
**Phase:** Execution + Peer Review (R&R)
**Target:** articulo_angelparejov2-experimental.md
**Score:** dominio 83/100, métodos 87/100 (R&R Ronda 2); writer-critic 98/100
**Verdict:** Reencuadre a estudio en profundidad de CNPG; peer review + R&R → REVISIÓN MENOR, listo para tier primario. MUST (R1) y residuos (R2) aplicados. Cuello de botella: v1-6 conceptual (5 refs pendientes, no sometido). Tier secundario gateado por evidencia nueva (2.º artículo).
**Report:** quality_reports/reviews/2026-07-08_v2_r2_editorial_decision.md

### 2026-07-08 — Coder (conversión DOCX plantilla IEEE)
**Phase:** Presentation / Submission-prep (empaquetado de formato)
**Target:** scripts/md2ieee_docx.py; articulo_angelparejov1-6_IEEE.docx; articulo_angelparejov2-experimental_IEEE.docx
**Score:** N/A (scripting stdlib, modo simplificado)
**Verdict:** Script stdlib air-gapped que convierte los .md al template IEEE Conference (OOXML Strict, 2 col) con cumplimiento 100%: conserva el esqueleto del zip byte a byte y regenera solo word/document.xml; elimina numeración manual (autonumeran los estilos); tablas anchas en interludios a 1 columna. Ambos .docx validados (esqueleto idéntico, pStyle definidos, XML bien formado, Strict). Único paso manual: insertar imagen de Fig. 1. Consolidado en main y pusheado (aa0dddd).
**Report:** SESSION_REPORT.md (entrada 2026-07-08 conversión DOCX); memoria project_docx_ieee_conversion_pending

### 2026-07-08 — coder (md2ieee_docx.py) + writer (v2 markdown)
**Phase:** Execution (refinamiento de formato, ronda 2)
**Target:** scripts/md2ieee_docx.py + articulo_angelparejov2-experimental.md → DOCX IEEE
**Score:** N/A (tarea de formato/edición, revisión visual del usuario)
**Verdict:** Aplicados 43 amarillos del usuario: backticks→monospace, imagen Markdown incrustada (sin duplicar), §→"Sección", nodo seudónimo nodo-lab-01, "matar"→"terminar", rutas internas→DOI Zenodo, encabezados Tabla II a 2 líneas. Ambos DOCX regenerados y validados (0 backticks/§/rutas; figura 1×).
**Report:** SESSION_REPORT.md (entrada 2026-07-08 ronda 2); plan quality_reports/plans/2026-07-08_docx-ieee-refinamiento-v2.md

### 2026-07-08 — Peer Review Ronda 3 (re-evaluación tras sesión DOCX IEEE)
**Phase:** Peer Review
**Target:** articulo_angelparejov2-experimental.md (commit 623aad8)
**Score:** dominio 83→85, métodos 87→89, writer-critic 98→98; promedio árbitros 85→87; agregado ≈88.7→90.2
**Verdict:** Revisión Menor — listo para tier primario. Terminología K8s (eliminación/fallo sostenido) sube dominio y métodos; residuos R2 cerrados. MUST único: corregir etiqueta "(regla de tres)"→Clopper–Pearson en §VI (línea 208, valores ya correctos).
**Report:** quality_reports/reviews/2026-07-08_v2_r3_editorial_decision.md (+ 3 reportes r3)

### 2026-07-09 — Librarian / Orchestrator (venues + estructura de trabajo)
**Phase:** Presentation / Submission-prep
**Target:** opciones de publicación del v2; hacer citable el v1-6; ramas de publicación
**Score:** N/A
**Verdict:** Deadlines verificados (CACIC 2026 ABIERTO hasta 29-jul; bases = LNCS 1-col ≤10 pp, NO IEEE → v2 requiere recorte ~49%). v1-6 confirmado desbloqueado (5 refs corregidas en e6c8024) y preparado como preprint Zenodo (metadatos + cita lista, falta DOI del usuario). Creadas 4 ramas pub/<venue> (cacic-2026, informatica-sistemas, clei-2027, impacto) + main como fuente de verdad; guía de trabajo git+Claude. Todo pusheado.
**Report:** quality_reports/convocatorias_y_venues.md; plans/2026-07-09_recorte-lncs-cacic.md; plans/2026-07-09_ramas-publicacion.md; zenodo_deposito_v1-6.md; GUIA_TRABAJO.md

### 2026-07-10 — writer-critic
**Phase:** Execution
**Target:** paper/cacic/main.tex (v2-CACIC, recorte LNCS para CACIC 2026)
**Score:** 96/100
**Verdict:** Recorte ~49% preservó integridad del argumento y trazabilidad numérica íntegra; autosuficiente sin el v1-6; cadena de citas [parejo2026] honesta; convenciones LNCS correctas. Solo 3 retoques de estilo (C1–C3), aplicados. Apto para envío a CACIC.
**Report:** quality_reports/reviews/2026-07-10_v2-cacic_writer-critic.md

### 2026-08-12 22:40 — Conversión Faraute + validaciones + Grupo A
**Phase:** Execution / Peer Review
**Target:** paper/faraute/main.tex (conversión de articulo_angelparejo-ITC.docx a formato Revista FARAUTE)
**Score:** writer-critic 70→~84 (bloqueante de páginas persiste); verifier PASS; domain-referee 80; methods-referee 79
**Verdict:** Conversión fiel a Faraute (2-col, Times12, autor-año, bib alfabética), compila 19pp limpio. Estadística verificada 3× (correcta). Aplicado Grupo A (leyendas tabla debajo, resumen 145pal, silabeo ES, overfull Ec., "Fuente:" Fig3/4) + depósito Zenodo (paper/faraute/replication/). PENDIENTE de autorización: recorte a ≤12pp (usuario difirió), revisiones de árbitros (Jepsen, reencuadre visibilidad, semántica verificador), correcciones de refs (Burckhardt→S., Taft→R.), grises de figuras (sin tool local).
**Report:** quality_reports/reviews/faraute_*.md (5 archivos)

### 2026-08-12 23:10 — Grupo B (recorte nivel seguro) + racionalización de figuras
**Phase:** Execution
**Target:** paper/faraute/main.tex
**Score:** N/A (recorte autorizado nivel seguro)
**Verdict:** 19→17 pp. Eliminadas Fig1 (modelo, "tautológica" per domain-referee) y Fig3 (boxplot, redundante con Fig4 + criticada por methods-referee) → quedan 3 figs (testbed/timeline/visibilidad, renumeradas). Condensadas §7 (−370 pal, remite a §5-§6), §8 (−340, quita duplicación de Fase 2), §4.3/§4.4 (−200) y §1 (fusión). Cuerpo 8093→~7180 palabras. Compila limpio, 0 overfull, 0 refs sin resolver. Preservado el detalle metodológico/estadístico que los árbitros valoraron. PENDIENTE: 17→12 pp requiere recorte PROFUNDO (mover detalle a Zenodo) o holgura del editor — usuario debe decidir. Grises pospuestos (color por ahora, sin tool local).
**Report:** quality_reports/reviews/faraute_sintesis_recomendaciones.md

### 2026-08-12 23:45 — Depósito Zenodo Opción 2 (reproducibilidad + suplemento)
**Phase:** Submission (reproducibilidad)
**Target:** paper/faraute/replication/ (+ zenodo-deposito-fase1.zip)
**Score:** N/A
**Verdict:** Construida Opción 2. analyze.py REESCRITO (stdlib) reproduce TODAS las cifras del artículo (F1 7,91/F2 36,75; U=0 p=1,083e-5; z=-3,78; rb=1,00; HL 28,96; CP 25,9%/22,1%; IC cobertura 97,9%; Spearman 0,62<crít 0,648). Corregido bug: valor crítico Spearman por tabla exacta (0,648) en vez de aprox-t (0,62) → ahora "no significativa" como el paper. Añadidos: DATA_DICTIONARY.md, CITATION.cff, LICENSE.md (CC-BY-4.0 datos / MIT código), suplemento.pdf (4 pp) con métodos+estadística extendidos que responden a methods-referee MAJOR 1/3/5 (semántica ACK-perdido del verificador, sensibilidad de exclusiones, permutación). ZIP listo para Zenodo. PENDIENTE usuario: reservar DOI en Zenodo y sustituir 'DOI por asignar'.
**Report:** paper/faraute/replication/README.md

### 2026-08-13 00:05 — Grupos C y D aplicados (revisiones de árbitros + referencias)
**Phase:** Execution / Peer Review (respuesta a árbitros)
**Target:** paper/faraute/main.tex
**Score:** N/A (edición autorizada "Todo C+D")
**Verdict:** Verificado por web: Burckhardt→Sebastian(S.) y Taft→Rebecca(R.) CORREGIDOS; Han/Chen/Khan OK. Añadidas refs: Kingsbury & Alvaro "Elle" PVLDB 2021 (Jepsen, C1) y PostgreSQL 16 doc (D4); mejorada spec CSI (D3). C2 reencuadre a visibilidad (§3.2 andamiaje + §8 predicado V(fallo,K) como contribución destacada). C3 salvedad intra-nodo en resumen ES/EN (146/144 pal ≤150). C4 p-valor saturado, C5 permutación, C6 semántica ACK-perdido del verificador (§5.2), C8 sensibilidad de exclusiones, C9 anclaje del "comportamiento anticipado" (§6.3, evita hombre de paja), C10 Clopper-Pearson unilateral + cota inferior F2 en Tabla 2. Compila limpio 18pp (17→18 por las adiciones). Responde domain-referee MAJOR 1-5 y methods-referee MAJOR 1-5. PENDIENTE: recorte profundo a 12pp; grises.
**Report:** quality_reports/reviews/faraute_sintesis_recomendaciones.md

### 2026-08-13 01:10 — Recorte profundo a 12 pp (modo automático)
**Phase:** Execution
**Target:** paper/faraute/main.tex (versión final) + main_referencia_extendida_18pp.* (referencia)
**Score:** N/A
**Verdict:** Recorte profundo 18→12 pp apoyado en el suplemento. Condensadas TODAS las secciones (§1-§8) moviendo detalle fino (IC, sensibilidad de exclusiones, permutación, F4 completo, aislamiento) al material suplementario del Zenodo, con remisiones explícitas. PRESERVADO: 3 figuras (testbed/timeline/visibilidad), 2 tablas, 6 ecuaciones, todas las cifras (7,91/36,75/4,65×/U=0/p=1,1e-5/HL 28,96/613253/0-12/CP 25,9-22,1%/97,9%/Spearman 0,62), reencuadre a visibilidad (C2), Jepsen (C1), salvedades intra-nodo (C3), semántica ACK-perdido. Resumen 146/abstract 144 (≤150). Layout: Fig4 a 1 columna, titlespacing y parskip ajustados. Compila limpio 12 pp, 0 refs sin resolver, 1 overfull 1pt (cosmético). Versión 18pp preservada como referencia consultable. Entregable: main_final_12pp.pdf.

### 2026-08-16 17:45 — Coder/Data-engineer (entorno + figuras + PDF definitivo Faraute)
**Phase:** Execution / Submission-prep
**Target:** entorno TeX/ImageMagick; paper/faraute/figures/; paper/faraute/main.pdf
**Score:** N/A (tarea de entorno y producción de entregable)
**Verdict:** Desbloqueado el envío a Faraute. (1) DIAGNÓSTICO DE RED: el puerto 53 está bloqueado en toda la máquina (Windows tampoco resuelve) por conflicto entre NordVPN —que secuestra la tabla de rutas con 0.0.0.0/1/128.0.0.0/1— y la VPN Check Point corporativa; la salida TCP/80 y TCP/443 sí funciona. Instalados `texlive-lang-spanish` y `imagemagick` resolviendo los repos por DNS-over-HTTPS y fijándolos temporalmente en /etc/hosts (parche ya retirado). Verificación independiente 4/4 + prueba funcional de silabeo (me-ca-nis-mos, al-ma-ce-na-mien-to, in-fra-es-truc-tu-ra). (2) HALLAZGO: `main.tex` NUNCA cargaba `silabeo-es.tex` —no hay \input ni \hyphenation—, de modo que el PDF del 13-ago se compiló sin silabeo español alguno (cortes con reglas inglesas). El parche de 254 líneas de scripts/silabeo_es.py es código muerto; pendiente decidir si se retira. (3) FIGURAS: las 3 del cuerpo (Fig2/Fig4/Fig5) convertidas a Gray 1-canal conservando 300 dpi; legibilidad revisada una por una —el color era decorativo, la semántica está en las etiquetas—; originales preservados en figures/color-originales/; copias renombradas para la entrega en figuras-envio/ (Fig1/Fig2/Fig3). (4) ENTREGABLE: main.pdf regenerado = 12 pp, 0 overfull, 0 underfull, 0 refs sin resolver, PDF íntegro en DeviceGray (0 DeviceRGB); main_final_12pp.pdf sincronizado (md5 idéntico). Mejora neta: el overfull de 1pt que registraba la versión previa desapareció y la paginación no se movió. PENDIENTE del usuario: DOI Zenodo, lectura final y envío.
**Report:** paper/faraute/CHECKLIST_ENVIO_FARAUTE.md (B1 resuelto); PENDIENTE_MI_LADO.md

### 2026-08-17 06:42 — Coder / Verifier (cierre de pendientes Faraute + seudonimización)
**Phase:** Execution / Submission-prep
**Target:** paper/faraute/ (entregable, depósito, carta); scripts/seudonimizar_infra.py; scripts/set_zenodo_doi.py
**Score:** N/A (tarea de producción, verificación y saneamiento)
**Verdict:** Cerrados todos los pendientes que no requieren al usuario. (1) HALLAZGO NO LISTADO: el paquete de reproducibilidad destinado a Zenodo publicaba los nombres reales de la infraestructura productiva de un tercero —38 apariciones de nodos, el inventario de los 4 clústeres CNPG ajenos con la ubicación de sus primarios, el correo corporativo (7×) y el servicio interno alojado—, mientras el manuscrito sí estaba seudonimizado. Consultado el usuario, eligió seudonimizar conservando la narrativa de gobernanza: 336 sustituciones en 25 archivos vía `scripts/seudonimizar_infra.py` (mapeo fijo, verificación de residuos, correspondencia privada en .claude/state/); ZIP rearmado con 0 identificadores reales sobre 43 archivos. (2) `scripts/set_zenodo_doi.py` convierte el pendiente del DOI en un comando: lo fija en los 7 sitios donde vive, recompila los 3 PDF, sincroniza el entregable, rearma el ZIP y verifica; probado de extremo a extremo con DOI falso. Se documentó que la checklist decía "5 archivos" y no distinguía campos DOI reales de texto instructivo. (3) Carta al comité editorial redactada. (4) CORRECCIÓN DE REGISTRO: el "0 underfull" del 2026-08-16 era un falso negativo de grep sobre un log ISO-8859; el conteo real era 17. La Tabla 1 usaba columnas X justificadas mientras la Tabla 2 ya llevaba \raggedright: corregida la inconsistencia, bajan a 13 y desaparecen las dos peores; sigue en 12 pp, 0 overfull, 0 refs sin resolver, 0 DeviceRGB. (5) `silabeo-es.tex` retirado (código muerto nunca cargado con \input, hoy además innecesario); se conserva el generador como contingencia. (6) CACIC 2026 cerró el 29-jul sin que conste el envío; señalado además que Faraute y el v2 son el mismo trabajo (riesgo de envío simultáneo). Todo agosto commiteado en 9d4cf31, 94da3d4, b800d21; sin pushear.
**Report:** SESSION_REPORT.md (entrada 2026-08-17); paper/faraute/CHECKLIST_ENVIO_FARAUTE.md; paper/faraute/PENDIENTE_MI_LADO.md
