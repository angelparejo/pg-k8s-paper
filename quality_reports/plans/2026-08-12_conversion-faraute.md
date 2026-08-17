# Plan — Conversión a formato FARAUTE + validaciones + análisis

**Estado:** DRAFT (pendiente aprobación de 2 decisiones bloqueantes)
**Fecha:** 2026-08-12
**Fuente:** `articulo_angelparejo-ITC.docx` (revisado por profesores) + fig1..fig5.jpg
**Destino:** Revista FARAUTE de Ciencias y Tecnología, UC/FACYT (`guia_autor_Faraute.pdf`)
**Ubicación salida:** `paper/faraute/`

## Contexto
El DOCX está maquetado para otra revista (RITC): encabezado Congreso/Póster, DOI ritc,
referencias IEEE numeradas [1]. Faraute exige formato distinto. Faraute es autoritativo
(supera working-paper-format.md del proyecto, que es IEEE/economics).

## Fase 1 — Conversión (cumplimiento estricto guía Faraute)
Clase: `\documentclass[12pt,twocolumn,letterpaper]{article}` + geometry 2,5cm + mathptmx (Times)
+ setspace (simple). Front matter (título/autores/resumen) a UNA columna vía `\twocolumn[...]`.
1. Reordenar título: español (TNR 14, MAYÚS, negrita, centrado) → línea en blanco → inglés (12, negrita).
2. Autor: nombre completo + inicial, apellido; dirección física; email; superíndices numéricos.
3. Resumen ≤150 palabras (actual 199 → recortar) + 3-5 palabras clave alfabéticas + Abstract + Keywords EN.
4. Secciones numeradas en negrita (1..8) — ya numeradas.
5. Figuras "Fig." / Tablas "Tabla", TNR 10, alineadas izquierda, DEBAJO. booktabs sin reglas verticales.
6. Ecuaciones: "Ec." cursiva, numeradas (S=(O,K,M,D), R(S), C(S), P(S), I(S), V(fallo,K)).
7. Bibliografía: hand-formatted `thebibliography`, autor-año ALFABÉTICO, formato Faraute exacto.
8. Citas en texto [n] → (Autor, año) según reglas guía (1 autor / 2 autores & / >2 et al. / múltiples ;).
9. Figuras insertadas (5) + Tabla 1, Tabla 2 con sus notas.

## Fase 2 — Dos validaciones profundas
- V1: writer-critic (formato/LaTeX/claims) + verifier (compila, integridad) + coherencia numérica INV-11/INV-22.
- V2: peer-review adversarial — domain-referee + methods-referee (contenido, método, aporte, extensión).
- Chequeo de cumplimiento Faraute punto por punto (checklist de la guía) como capa transversal.

## Fase 3 — Análisis + recomendaciones
Agregación de hallazgos; recomendaciones priorizadas (bloqueantes / mayores / menores) para publicación.
NO se aplican sin autorización del usuario.

## Compuerta
Autorización del usuario ANTES de aplicar recomendaciones (arreglos de contenido).

## Decisiones bloqueantes (pendientes)
1. Estilo de referencias: Faraute estricto (autor-año) vs. mantener IEEE numerado.
2. Tipo de artículo Faraute / presupuesto de páginas (científico ≤12 pp vs. actualización ≤20 pp).
