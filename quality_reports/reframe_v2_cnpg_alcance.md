# Reencuadre del v2-experimental — estudio en profundidad de CNPG + marco para N operadores

**Fecha:** 2026-07-07 · **Estado:** decisión RESUELTA (restricción externa) · **Aplica a:** `articulo_angelparejov2-experimental.md`

## 1. La decisión quedó resuelta (no es elección, es restricción)

El equipo de producción **confirmó que NO se permite instalar Zalando Postgres Operator (Patroni/Spilo)**
en el clúster productivo por el riesgo que implica. Por tanto el piloto es **CNPG-solo de forma
definitiva**, no por falta de ambición sino por una restricción dura del entorno. Esto cierra
[[project_operator_scope_decision_pending]] a favor de la **opción A** (estudio de un operador).

## 2. Nuevo encuadre

`v2-experimental` pasa de *"comparación empírica de dos operadores"* a **"validación empírica en
profundidad del marco (taxonomía + modelo S=(O,K,M,D) + invariantes) sobre CloudNativePG, operador
representativo del enfoque cloud-native"**. La comparación multi-operador:
- se mantiene **analítica** (Tabla I, a partir de comportamiento documentado) — ya presente;
- se declara **trabajo futuro** (un tercer artículo empírico comparativo, en un entorno no productivo
  que permita instalar Zalando), citando este y el conceptual [[project-pg-k8s-sequential-publication]].

Coherente con la publicación secuencial: v1-6 (marco+protocolo) → v2 (validación en profundidad, CNPG)
→ v3 futuro (comparación multi-operador).

## 3. Qué se CONSERVA (ya es el "marco para N operadores")

- **§III taxonomía** (L57): CNPG / Zalando-Patroni / Crunchy — es conceptual, se queda.
- **§IV.A comparación entre operadores** (L103, L107): analítica, se queda.
- **Tabla I** (L121–L130): distribución de responsabilidades por capa y tipo de fallo, multi-operador,
  a partir de literatura/documentación — se queda (es el vehículo de generalización).

## 4. Qué CAMBIA (ediciones quirúrgicas, con líneas actuales)

| Línea | Ahora | Cambio |
|---|---|---|
| L5 Resumen | "Se comparan dos operadores representativos (CNPG y Zalando/Patroni)…" | "Se valida en profundidad sobre CloudNativePG (exponente cloud-native); el contraste con operadores basados en Patroni se aborda de forma analítica (Tabla I) y se plantea como trabajo futuro." |
| L33 Contribución | "para dos operadores representativos" | "para CloudNativePG" |
| L146 §IV.E | "Se compararon dos operadores… CNPG 1.28.0… y Zalando v1.13.x (Spilo 16)…" | Solo CNPG. **Justificar por restricción del entorno**: clúster productivo, no se permite instalar operadores nuevos (el operador CNPG es compartido con 4 clústeres); Zalando queda analítico + futuro. |
| L162 Tabla II | "RTO/RPO por operador × escenario… Columnas CNPG y Zalando… Mann–Whitney" | Un operador (CNPG) × escenarios F1/F2/F3; RTO/RPO mediana+IQR; **quitar Mann–Whitney entre operadores** (no aplica); añadir F4 = no ejecutable (hallazgo). |
| L186 Limitaciones | "cubre dos operadores (CNPG y Zalando/Patroni)…" | "cubre un operador (CNPG) por restricción del entorno productivo… comparación multi-operador analítica (Tabla I) y trabajo futuro." Añadir F4 (hardening↔FUSE) y matiz F2. |
| L196 Conclusión | "para dos operadores representativos" | "para CloudNativePG" |
| Título | plural "Operadores" / comparación | Enfatizar marco + caso CNPG (opciones abajo). |

## 5. Hallazgos empíricos del piloto que ENRIQUECEN el aporte single-operator

El piloto no solo "valida"; aporta resultados no triviales que refuerzan que un estudio en profundidad
de UN operador es contribución suficiente:
- **Gradiente F1/F2/F3 = tres comportamientos distintos** (kill→promoción, RTO mediana 7.91 s;
  pod-failure→recreación en sitio, sin promoción, RTO mediana 36.75 s; partición→CP, sin promoción).
  El RTO de "fallar" (~4.6×) > el de "matar".
- **Mecanismo causal:** el failover lo dispara la **visibilidad del fallo ante Kubernetes** (NotReady),
  refinado: promueve ante *eliminación* del pod, no ante mero NotReady si el pod se recrea con misma identidad.
- **F4 (hardening↔FUSE):** el `readOnlyRootFilesystem` de CNPG impide la inyección de E/S vía FUSE —
  interacción operador↔tooling de caos, hallazgo operator-general.

## 6. Riesgo de árbitro y mitigación

**"Un solo operador es estrecho"** → (a) el aporte primario es el **marco** (validado en profundidad),
no la comparación; (b) restricción **externa y honesta**, declarada; (c) CNPG es **representativo**
(CNCF, adopción amplia, activo); (d) varios hallazgos son **operator-general** (hardening↔caos,
asimetría kill-vs-fail); (e) la comparación es el **siguiente artículo**, citando este y el conceptual.

## 7. Opciones de título (v2-experimental)

1. *"Validación empírica de un marco de análisis de operadores de PostgreSQL y almacenamiento CSI en Kubernetes: un estudio en profundidad de CloudNativePG ante inyección de fallos."*
2. *"Fallos, consistencia y recuperación en operadores de PostgreSQL sobre Kubernetes: marco de análisis e instanciación empírica en CloudNativePG."*
3. *"Del modelo a la medición: caracterización empírica de CloudNativePG bajo inyección de fallos y su lectura mediante un marco de operador×almacenamiento."*

## 8. Próximo paso

Ejecutar estas ediciones sobre `articulo_angelparejov2-experimental.md` (vía `/write` + writer-critic)
una vez cerrado el lote F2 y la Fase 6 (para tener las cifras finales de la Tabla II). Este memo es el
plan de esa reescritura.
