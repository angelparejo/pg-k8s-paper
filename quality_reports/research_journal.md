# Research Journal

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
