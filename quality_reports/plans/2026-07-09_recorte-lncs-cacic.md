# Plan — Recorte y reformateo del v2-experimental a LNCS para CACIC 2026

**Estado:** DRAFT (pendiente de aprobación + de decidir si vamos a CACIC — ver §7 de `convocatorias_y_venues.md`)
**Fecha:** 2026-07-09
**Deadline duro:** 29/07/2026 (~20 días)
**Objetivo:** producir `articulo_angelparejov2-cacic.*` en **formato Springer LNCS (1 col, A4, 10 pt), ≤10 páginas**, en español, apto para envío a CACIC 2026 (workshop WPDP / WBDDM / WARSO).
**Fuente:** `articulo_angelparejov2-experimental.md` (NO se toca; el v2-CACIC es un derivado).

---

## 1. Diagnóstico cuantitativo

Cuerpo actual ≈ **8.800 palabras** (+ ~630 de refs). En IEEE 2-col ≈ 10 pp; en **LNCS 1-col ≈ 16–18 pp**.
Un paper LNCS de 10 pp (con abstract, 2 tablas, 1 figura y ~21 refs) admite ≈ **4.500 palabras de prosa**.
→ Recorte necesario ≈ **45–50%**, concentrado en las secciones conceptuales (III–IV), que duplican el v1-6.

### Presupuesto por sección (palabras)

| Sección | Actual | Meta LNCS | Acción |
|---|---:|---:|---|
| Abstract + Keywords | ~180 | ~180 | Mantener (revisar) |
| I. Introducción | 620 | ~400 | Trim: quitar redundancia con Trabajos Relacionados |
| II. Trabajos Relacionados | 792 | ~450 | Comprimir; parte solapa con v1-6 |
| **III. Modelo y Marco** | 1254 | **~350** | **Recorte fuerte → recap de 1 párrafo + cita a [v1-6]** |
| **IV. Análisis Comparativo** | 1275 | **~300** | **Recorte fuerte → conservar solo lo que enmarca el estudio empírico; resto → [v1-6]** |
| V. Metodología Experimental | 1350 | ~850 | Trim moderado; es contribución central, se conserva |
| VI. Resultados | 2254 | ~1200 | Trim: conservar tablas y cifras, recortar prosa explicativa |
| VII. Discusión | 639 | ~400 | Trim |
| VIII. Conclusiones | 538 | ~300 | Trim |
| Disponibilidad de datos | 79 | ~79 | Mantener |
| **Total prosa** | **~8.800** | **~4.500** | **≈ −49%** |

**Tesis del recorte:** el aporte del v2 para CACIC es el **estudio empírico de CloudNativePG bajo fallos** (V–VI).
El marco conceptual (III–IV) es el objeto del **v1-6**; aquí se resume y se cita, lo que además refuerza la
cadena de citas anti-"salami slicing".

---

## 2. Precondición (bloqueante para la vía secuencial)

El recorte apoya III–IV en una cita a [v1-6]. Para que esa cita sea legítima, el v1-6 debe estar **citable**:
- **Opción A (preferida):** subir el v1-6 a un preprint con DOI (Zenodo/arXiv) y citarlo.
- **Opción B:** someter el v1-6 en paralelo (a CACIC u otra vía) y citarlo como "en prensa / bajo revisión".
- **Opción C (si no hay v1-6 citable):** el v2-CACIC debe ser autocontenido → III–IV no se pueden externalizar,
  y el recorte a 10 pp LNCS se vuelve mucho más agresivo sobre V–VI (pierde profundidad empírica). No recomendada.

> **Decisión de usuario requerida antes de ejecutar.** Ver §7 de `convocatorias_y_venues.md`.

---

## 3. Pasos de ejecución

1. **Obtener la plantilla oficial CACIC** (`LaTeX2e.zip` o `Word`) desde el CFP; confirmar si exige anonimización.
2. **Duplicar fuente:** crear `articulo_angelparejov2-cacic.md` a partir del v2 (marcador de derivado).
3. **Recortar por sección** según el presupuesto de §1 (empezar por III–IV, que dan el mayor ahorro).
4. **Insertar la cita a [v1-6]** en III y IV donde se externaliza el marco conceptual.
5. **Reformatear a LNCS:**
   - Ruta LaTeX (recomendada): usar `llncs.cls`; estructura `\title/\author/\institute/\abstract/\keywords`,
     secciones `\section` (numeración LNCS 1, 1.1), refs con `splncs04.bst`.
   - Ruta Word: adaptar el script `scripts/md2ieee_docx.py` → nueva variante `md2lncs_docx.py` sobre la
     plantilla LNCS de CACIC (mismo enfoque air-gapped, stdlib; reutiliza el parser de markdown).
6. **Ajustar tablas/figuras a 1 columna** (LNCS): Tabla I, Tabla II y Fig. 1 a ancho de columna simple.
7. **Convertir refs a estilo LNCS/Springer** (numérico [n], orden de campos Springer).
8. **Elegir workshop** (WPDP recomendado por el eje sistemas distribuidos + tolerancia a fallos).
9. **Redactar título ≤ (no hay tope estricto en CACIC, pero acortar el actual de 24 palabras es sano).**

---

## 4. Verificación (compuerta de calidad)

- [ ] Compila/renderiza en la plantilla LNCS oficial sin errores.
- [ ] **≤ 10 páginas A4**, sin numerar, sin encabezado/pie.
- [ ] Idioma español; abstract + keywords presentes.
- [ ] Todas las cifras de VI coinciden con `results_summary.md` (INV-11) tras el recorte.
- [ ] Tablas con notas (INV-1), figura con pie (INV-2); sin `\hline` si es LaTeX (INV-3).
- [ ] La cita a [v1-6] resuelve a una fuente citable (preprint/DOI o "bajo revisión").
- [ ] Paso de writer-critic ≥ 80 sobre la versión recortada (el recorte no debe romper el argumento).
- [ ] Workshop seleccionado y datos de envío del sistema SAC verificados.

---

## 5. Riesgos

- **Tiempo:** ~20 días para recorte + reformateo + (posible) preprint del v1-6. Ajustado pero factible.
- **Pérdida de contexto conceptual:** al externalizar III–IV, el revisor de CACIC debe poder seguir el paper sin
  leer el v1-6 → conservar un recap mínimo autosuficiente, no una remisión seca.
- **Estilo de refs:** LNCS ≠ IEEE; revisar orden de campos y abreviaturas de venues.
- **Anonimización:** si CACIC resultara doble ciego, quitar nombre/afiliación/email y ajustar autocitas al v1-6.
