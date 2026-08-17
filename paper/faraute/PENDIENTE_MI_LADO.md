# Pendiente de mi lado — antes de enviar a FARAUTE

Lista corta y accionable. Detalle completo en `CHECKLIST_ENVIO_FARAUTE.md`.

## 1. Figuras a grises (guía Faraute, punto 9) — HECHO 2026-08-16 ✅
- [x] Las 3 figuras convertidas a escala de grises, 300 dpi conservados (`Gray`, 1 canal).
- [x] Legibilidad revisada una por una: el color era decorativo (toda la semántica está en
      las etiquetas de texto), así que no se perdió información. La Fig4 (timeline) aguanta:
      las barras F1/F2 se distinguen por longitud y por su etiqueta en el eje.
- [x] Copias renombradas para el envío en `figuras-envio/`:
      `Fig1.jpg` (banco de pruebas) · `Fig2.jpg` (timeline) · `Fig3.jpg` (predicado de visibilidad).
- [x] Originales a color preservados en `figures/color-originales/` por si hay que rehacer algo.
- [x] `main.pdf` regenerado: 12 pp, PDF íntegro en `DeviceGray` (0 `DeviceRGB`).

## 2. DOI en Zenodo — automatizado 2026-08-17 ⚙️
Ya no hay que editar archivos a mano: un solo comando hace la sustitución, recompila los
PDF y rearma el ZIP.

- [ ] Subir `paper/faraute/zenodo-deposito-fase1.zip` a Zenodo.
- [ ] Pulsar **"Reserve DOI"** en el formulario (da el DOI antes de publicar).
- [ ] Ejecutar, desde la raíz del proyecto:

      python3 scripts/set_zenodo_doi.py 10.5281/zenodo.<numero>

      Sustituye el marcador en los 7 sitios donde vive (manuscrito, versión extendida,
      suplemento, `CITATION.cff`, `.zenodo.json`, `README.md` del depósito y la carta al
      editor), recompila `main.tex`, la versión de 18 pp y el suplemento, sincroniza
      `main_final_12pp.pdf`, rearma el ZIP y verifica que no quede ningún marcador.
      Con `--check` informa el estado sin tocar nada; con `--dry-run` muestra sin escribir.
- [ ] Volver a subir el ZIP rearmado (ahora lleva el DOI dentro) y **publicar** el depósito.

## 3. Revisión final
- [ ] Leer el PDF de 12 pp completo (`main_final_12pp.pdf`).
- [ ] Confirmar autor / afiliación / correo / ORCID.

## 4. Envío
- [ ] Enviar PDF + 3 figuras (grises, 300 dpi) a **faraute@uc.edu.ve**.
- [x] Carta al editor redactada: `carta_al_editor.md` (lista para pegar como cuerpo del
      correo; solo falta la fecha y, si se conoce, el nombre del editor en ejercicio).
- [ ] Guardar acuse y fecha.

---
**Nota:** se envía la versión de **12 pp**. La de **18 pp** (`main_referencia_extendida_18pp.pdf`) y el **suplemento** son tu respaldo para el arbitraje.
