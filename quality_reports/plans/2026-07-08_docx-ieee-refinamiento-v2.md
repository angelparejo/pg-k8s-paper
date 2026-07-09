# Plan — Refinamiento DOCX IEEE v2-experimental (ronda 2)

**Status:** APPROVED (decisiones vía AskUserQuestion 2026-07-08)
**Base:** commit aa0dddd + working tree sin commitear. Fuente: `articulo_angelparejov2-experimental.md`; render: `scripts/md2ieee_docx.py`.

## Decisiones del usuario
- Q1 Resultados → **Tabla II + repo público con DOI (Zenodo)**. Quitar rutas internas de la prosa; citar DOI (placeholder por asignar).
- Q2 Nodo → seudónimo **`nodo-lab-01`** (reemplaza `tcolp293` en todo el doc).
- Q3 Código → **monospace/typewriter** (Courier New), sin backticks.
- Q4 "matar" → **formalizar a "terminar/eliminar"** en prosa; identificador `pod-kill` se mantiene.

## Cambios en el SCRIPT (scripts/md2ieee_docx.py)
1. `run()`: nuevo parámetro `mono` → rPr con rFonts Courier New.
2. `parse_inline()`: manejar `` `código` `` → run mono; `<br>`/`<br/>` → `<w:br/>`.
3. `parse_markdown()`: reconocer `![alt](ruta)` como bloque `figure` (alt = pie); incrusta figura.
4. `build_body`: anchos Tabla II rebalanceados a `[56,38,76,22,59]` (headers en 2 líneas alivian ancho).

## Cambios en el MARKDOWN (articulo_angelparejov2-experimental.md)
- "matar el pod" → "terminar el pod" (L5 abstract, L206); "del kill" → "de la terminación" (L189).
- `tcolp293` → `nodo-lab-01` (L161 ×1, L163 ×2).
- `§X` → "Sección X" / "Secciones X y Y" (L163,181,189,200×2,202,204×2,236).
- L110: raya final "—en paralelo…" → coma.
- L200 nota Tabla II: quitar `(data/cleaned/*.csv)`.
- Encabezados Tabla II (L193): insertar `<br>` → "Escenario<br>(mecanismo)", "RTO /<br>indisponibilidad", "Comportamiento<br>observado".
- L258 Disponibilidad de datos: reescribir con DOI Zenodo (placeholder), sin rutas internas.

## Verificación
- Regenerar ambos DOCX; validar XML bien formado; conteo de estilos; 0 backticks literales; figura incrustada; § ausente; `nodo-lab-01` presente y `tcolp293` ausente.
