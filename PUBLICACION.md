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

## Estado

- [ ] **Precondición:** v1-6 citable (DOI Zenodo) — ver `quality_reports/zenodo_deposito_v1-6.md` en main
- [ ] Descargar plantilla oficial LNCS de CACIC y confirmar anonimización
- [ ] Recorte ~49% del v2 a ~4.500 palabras (ver `quality_reports/plans/2026-07-09_recorte-lncs-cacic.md`)
      → comprimir Secs. III–IV apoyándose en el v1-6
- [ ] Reformatear a LNCS (LaTeX `llncs.cls` o variante `md2lncs_docx.py`)
- [ ] Insertar autocita al preprint v1-6 en III–IV
- [ ] Tablas/figura a 1 columna; refs a estilo LNCS/Springer
- [ ] Verificar ≤10 pp; writer-critic ≥80 sobre la versión recortada
- [ ] Elegir workshop y enviar por SAC

## Archivo de trabajo (en esta rama)

- Fuente canónica: `articulo_angelparejov2-experimental.md` (en main; NO editar aquí el fondo)
- Derivado CACIC: `articulo_angelparejov2-cacic.md` (crear al ejecutar el recorte)

## Notas

- El recorte se apoya en que el marco conceptual (III–IV) es el v1-6 → aquí solo recap + cita.
- Traer correcciones de fondo desde main con `git merge main`.
