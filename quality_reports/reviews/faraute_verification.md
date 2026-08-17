# Informe de Verificación — Manuscrito Faraute

**Fecha:** 2026-08-12
**Modo:** Estándar (infraestructura)
**Objetivo:** `paper/faraute/main.tex`
**Motor:** pdflatex (2 pasadas). Sin biber/latexmk (correcto para este entorno).
**Bibliografía:** autor-año a mano (`thebibliography` manual / lista `Referencias`) — correcto para Faraute; NO se evalúa como INV-9.

---

## Resultados por comprobación

| # | Comprobación | Estado | Detalle |
|---|--------------|--------|---------|
| 1 | Compilación pdflatex (x2) | PASS | EXIT=0 en ambas pasadas. PDF generado: `main.pdf`, 19 páginas, 1.975 MB. |
| 2 | Referencias sin resolver | PASS | 0 `undefined`, 0 `multiply defined`, sin `LaTeX Warning`, sin aviso `rerun`. |
| 3 | Integridad de figuras | PASS | Las 5 figuras existen y se incrustan (páginas 5, 10, 13, 15, 16). |
| 4 | Integridad de referencias cruzadas | PASS | 13 labels definidos = 13 referenciados. Sin huérfanos ni colgantes. |
| 5 | Higiene de rutas (INV-16) | PASS | Todas las rutas relativas (`figures/FigN.jpg`). Sin rutas absolutas, sin `\input` externo. |
| 6 | Overfull/Underfull | PASS* | 1 Overfull hbox (menor, ver abajo); resto son underfull tipográficos benignos. |

**Overall: PASS**

---

## Detalle

### 1. Compilación
- Pasada 1: EXIT=0. Pasada 2: EXIT=0.
- `Output written on main.pdf (19 pages, 1974991 bytes).`
- Sin aviso de re-ejecución (`main.out` estable, checksum sin cambios).

### 2. Cajas (Overfull/Underfull)
- **Overfull \hbox: 1** — `(39.95pt too wide) detected at line 379`.
  - Ubicación: ecuación de visibilidad (`eq:visibilidad`), display de una columna:
    `V(fallo,K) ∈ {eliminado, NotReady-recreado, Ready}`.
  - Causa: el conjunto con tres términos textuales largos ("NotReady-recreado") no cabe
    en el ancho de columna (~7,95 cm) del formato a dos columnas.
  - Severidad: BAJA/cosmética (~0,5 cm de desborde al margen). No rompe la maqueta.
  - Sugerencia (NO aplicada; solo lectura): envolver en `\small`, o partir el conjunto con
    `\begin{aligned}` / `\resizebox`, o abreviar los estados.
- **Underfull \hbox: 18** y **Underfull \vbox: 17** — todos benignos:
  los vbox ocurren "while \output is active" (balanceo de columnas del `twocolumn`),
  y los hbox son estiramiento de justificación en columnas estrechas. No requieren acción.
- Overfull \vbox: 0.

### 3. Figuras — existencia, formato y resolución
Las 5 figuras existen en `paper/faraute/figures/` y se incrustan correctamente.

| Fig | Archivo | Píxeles | Densidad nativa | Render | DPI efectivo aprox. |
|-----|---------|---------|-----------------|--------|---------------------|
| 1 | Fig1.jpg | 2040×1980 | 300×300 | `\linewidth` (~3,13 in) | ~652 |
| 2 | Fig2.jpg | 2340×1860 | 300×300 | `\linewidth` (~3,13 in) | ~748 |
| 3 | Fig3.jpg | 1620×1380 | 300×300 | `\linewidth` (~3,13 in) | ~518 |
| 4 | Fig4.jpg | 2280×1170 | 300×300 | `0.92\textwidth` (~6,01 in) | ~379 |
| 5 | Fig5.jpg | 2100×1380 | 300×300 | `\linewidth` (~3,13 in) | ~671 |

- **DPI:** todas ≥ 300 dpi efectivos al tamaño de render (mínimo Fig4 ≈ 379). Densidad nativa 300 dpi. CUMPLE el requisito de 300 dpi de la guía Faraute.
- **Formato/color (ADVISORY):** las 5 son **JPG a color** (3 componentes RGB). La guía Faraute pide **escala de grises**. No es un fallo de compilación, pero es una desviación de la guía de autor: convertir a grises antes del envío final. Además JPG es con pérdida; para diagramas/vectores (Fig1, Fig2, Fig5 parecen esquemas) sería preferible PDF/PNG sin pérdida, aunque la guía admite el tamaño actual.

### 4. Referencias cruzadas
- **13 labels definidos** (.aux) = **13 en fuente** = **13 referenciados**. Correspondencia exacta.
- Ecuaciones (`eq:modelo`, `eq:resiliencia`, `eq:consistencia`, `eq:rendimiento`, `eq:interaccion`, `eq:visibilidad`): cada una citada 1× vía macro `\Ec{}` ("Ec. (n)").
- Figuras (`fig:modelo`, `fig:testbed`, `fig:boxplot`, `fig:timeline`, `fig:visibilidad`): cada una citada 1×.
- Tablas: `tab:responsabilidad` citada 11×; `tab:rto` citada 1×.
- Sin `\ref` a labels inexistentes; sin labels no citados.

### 5. Higiene
- Rutas 100% relativas (INV-16 OK). Sin `setwd`/rutas absolutas (no aplica a .tex, sin infracciones).
- **Archivos auxiliares/dispersos en el directorio** (no afectan compilación, limpieza opcional):
  `pass1.txt`, `pass2.txt`, `notext.log`, `diag.tex`, `diag.pdf`. Los `.aux/.log/.out` son normales de pdflatex.

---

## Notas de invariantes
- INV-9 (biblatex+biber): **NO aplica** por decisión de formato Faraute (bibliografía manual autor-año). No se marca como fallo.
- INV-16 (sin rutas absolutas): **OK**.
- INV-10/14/15/19: no aplican (documento LaTeX sin scripts embebidos; sin hyperref/cleveref exigidos por Faraute — el orden hyperref/xurl es correcto).

## Veredicto
**PASS.** Compila limpio a 19 páginas, sin referencias sin resolver, 13/13 cruces íntegros, 5/5 figuras incrustadas a ≥300 dpi, rutas relativas. Único punto no bloqueante: 1 overfull hbox de baja severidad en `eq:visibilidad` (línea 379) y figuras a color en vez de escala de grises (desviación de la guía Faraute, corregir antes del envío final).
