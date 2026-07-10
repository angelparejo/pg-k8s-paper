# PUBLICACIÓN — CACIC 2026

> **Rama:** `pub/cacic-2026` · **Artículo:** v2-experimental · **Prioridad:** 🎯 ALTA

## Ficha del venue

| Campo | Valor |
|---|---|
| Venue | XXXII Congreso Argentino de Ciencias de la Computación (CACIC 2026), UTN-FRCU |
| Workshop objetivo | **WPDP** (Proc. Distribuido y Paralelo) · alt: WBDDM (BD) / WARSO (Arq/Redes/SO) |
| **Deadline envío** | **29/07/2026** · Notificación 07/09/2026 · Congreso 5–9 oct 2026 |
| **Formato** | Springer **LNCS 1-columna**, A4, 10 pt, sin numerar, sin encabezado/pie |
| **Extensión** | **Máximo 10 páginas** |
| Idioma | Español |
| Doble ciego | No exigido explícitamente (confirmar en la plantilla) |
| Archivos | Word / LaTeX / PDF (plantillas LaTeX2e / Office2007 / Word-97-2003) |
| Envío | Sistema web SAC del congreso (no EasyChair) |
| Publicación | Actas ISBN en SEDICI; mejores trabajos → Springer CCIS (Scopus/DBLP) |

## Estado — LISTO PARA ENVÍO (2026-07-10)

- [x] Descargar plantilla oficial LNCS de CACIC → **es `sv-lncs`/`llncs.cls`; anonimización NO exigida**
- [x] Recorte ~49% del v2 (~9.100 → ~3.640 palabras) — comprimidas Secs. III–IV apoyándose en el v1-6
- [x] Reformatear a LNCS (**LaTeX `llncs.cls`**, ruta elegida) → `paper/cacic/main.tex`
- [x] Insertar autocita al preprint v1-6 (`[parejo2026]`) — Tabla I comparativa externalizada al v1-6
- [x] Tablas/figura a 1 columna; refs a estilo LNCS/Springer (20 refs)
- [x] Verificar ≤10 pp (**10 pp exactas**, sin overfull ni refs indefinidas); **writer-critic 96/100**
      (`quality_reports/reviews/2026-07-10_v2-cacic_writer-critic.md`)
- [x] **Workshop elegido: WPDP** (Procesamiento Distribuido y Paralelo)
- [ ] **Precondición de envío:** v1-6 citable (DOI Zenodo) → sustituir placeholder `10.5281/zenodo.XXXXXXX`
      en `paper/cacic/main.tex`. Ver `quality_reports/zenodo_deposito_v1-6.md`.
- [ ] Enviar por el sistema web **SAC** del congreso (antes del 29-jul)

## Archivo de trabajo (en esta rama)

- Fuente canónica: `articulo_angelparejov2-experimental.md` (en main; NO editar aquí el fondo)
- **Derivado CACIC: `paper/cacic/main.tex`** (+ `main.pdf`, `llncs.cls`, `splncs03.bst`) — compila con
  `cd paper/cacic && pdflatex main && pdflatex main`

## Notas

- El recorte se apoya en que el marco conceptual (III–IV) es el v1-6 → aquí solo recap + cita.
- Traer correcciones de fondo desde main con `git merge main`.
