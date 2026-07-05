# Research Journal

### 2026-07-05 21:35 — Coder/Data-engineer (instanciación del paquete Fase B con reconocimiento real del clúster)
**Phase:** Execution (preparación del piloto empírico para la v2)
**Target:** paper/replication/paquete-ejecucion-fase-b/ (11 archivos) + memory/
**Score:** N/A (documentación/manifiestos; no ejecutado contra clúster)
**Verdict:** Reconocido el clúster productivo real en **modo desacoplado** (solo-lectura; el usuario ejecutó por VPN y pegó salidas) y actualizado el paquete Fase B en consecuencia. Tres refutaciones materiales de los supuestos previos: (1) **no son 3 clústeres productivos sino 4 CNPG preexistentes** (pg-prod, pg-cert, pg-dev, gitlab/pg-gitlab); el experimental es el 5.º. (2) **Chaos Mesh 2.7.x es incompatible** con K8s v1.34.6 → subido a **v2.8.3** (soporta 1.30–1.35; parches "Chaotic Deputy"; verificado por WebSearch/WebFetch en chaos-mesh.org). (3) El nodo del lab **tcolp293 co-aloja 3 primaries CNPG ajenos** (pg-cert-1, pg-dev-3, pg-gitlab-2) → la barrera #2 y G5 (que asumían "nodo vacío") se **reescribieron**: la contención descansa en filtro de namespace + doble selector + nombre único + dry-run G1, no en aislamiento de nodo (decisión del usuario: mantener tcolp293). Además: placeholders resueltos (`cnpg-operator`, SC `huawei-ch-xfs` con reclaimPolicy Retain → teardown de PV a mano, nodo `tcolp293`); Linkerd excluido del lab vía `linkerd.io/inject: disabled` en namespace + `inheritedMetadata` del clúster (coincide con prod: pg-* no meshado → sin salvedad de validez externa). Verificado: 0 placeholders, 0 residuos de encuadre viejo, YAML parsea. Memoria del proyecto corregida.
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
