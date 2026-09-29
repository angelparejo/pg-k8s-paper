# Pendiente de mi lado — antes de enviar a FARAUTE

Lista corta y accionable. Detalle completo en `CHECKLIST_ENVIO_FARAUTE.md`.

## 1. Figuras a grises (guía Faraute, punto 9) — HECHO 2026-08-16 ✅
- [x] Las 3 figuras convertidas a escala de grises, 300 dpi conservados (`Gray`, 1 canal).
- [x] Legibilidad revisada una por una: el color era decorativo (toda la semántica está en
      las etiquetas de texto), así que no se perdió información. La Fig4 (timeline) aguanta:
      las barras F1/F2 se distinguen por longitud y por su etiqueta en el eje.
- [x] Copias renombradas para el envío en `figuras-envio/`:
      `Fig1.jpg` (banco de pruebas) · `Fig2.jpg` (timeline) · `Fig3.jpg` (predicado de visibilidad).
- [x] Originales a color preservados en `figuras/color-originales/` por si hay que rehacer algo.
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
      `articulo_angel_parejo_final.pdf`, rearma el ZIP y verifica que no quede ningún marcador.
      Con `--check` informa el estado sin tocar nada; con `--dry-run` muestra sin escribir.
- [ ] Volver a subir el ZIP rearmado (ahora lleva el DOI dentro) y **publicar** el depósito.

## 2bis. Ronda de revisión — HECHA 2026-08-18 ✅
- [x] Ediciones del documento revisado aplicadas y *abstract* retraducido desde el resumen.
- [x] Tres defectos que el log **no** delataba: 92 rayas que se perdían, `«` `»` `¿` que se
      imprimían mal (`¿` salía como `£`) y la Tabla 2 aterrizando en la última página, encima
      de las referencias. Los tres corregidos y verificados en los *content streams* del PDF.
- [x] Nota al pie de tabla alineada a la izquierda (punto 8 de la guía); salía centrada.
- [x] Las 28 referencias verificadas contra fuente primaria; 5 corregidas. La importante:
      *Chen et al.* citaba un preprint de arXiv de un trabajo ya arbitrado en ACSW '26.
- [x] Versión de 18 pp sincronizada con los mismos arreglos.

## 2ter. Zenodo — CERRADO 2026-09-27 ✅ (no tocar)
- [x] Depósito publicado. **Concept DOI: `10.5281/zenodo.23004248`** — es el que cita el
      artículo y resuelve siempre a la última versión.
- [x] Versiones: `1.0-fase1` (`...23004249`) y `1.0.1-fase1` (`...23004520`, la vigente).
- [x] **Versión `1.0.2-fase1` publicada** — `10.5281/zenodo.23005296`. Corrige tres cajas
      desbordadas del suplemento, la peor de 111,7 pt, que hacían perder el `.py` de la ruta
      `execution-package/manifiestos/scripts/analyze.py` — precisamente el script que
      reproduce las cifras.
- [x] El ZIP del repositorio es **byte a byte** el publicado: md5
      `14c53cffec14d1d569fbbe386a52be73`, 114 637 bytes.
- [x] Versiones anteriores: `1.0-fase1` (`...23004249`) y `1.0.1-fase1` (`...23004520`).

> ⚠️ **DECISIÓN DELIBERADA (2026-09-28): no corregir `replication/supplement/suplemento.tex`.**
> Conserva la ortografía anterior a la regla RAE de prefijos —`co-localización`,
> `intra-nodo`, `inter-nodo`, `no-promoción`, `no-normalidad`, `distribución-libre`,
> 10 apariciones—, mientras que el artículo ya usa las formas soldadas.
>
> ⚠️ **Y no rearmes el ZIP sin necesidad.** `rearmar_zip()` **nunca** reproduce el mismo
> md5, ni siquiera con los archivos idénticos: `zipfile` guarda la fecha de modificación de
> cada fichero, y basta un `git checkout` o una recompilación para cambiarla. El ZIP **tal
> como está versionado** es el publicado; si lo rearmas y el md5 cambia, no significa que el
> contenido difiera. Para restaurarlo: `git checkout -- paper/faraute/zenodo-deposito-fase1.zip`.

> **No es un descuido.** Corregirlo cambiaría el ZIP, obligaría a publicar una tercera
> versión en Zenodo por 10 guiones y rompería la identidad byte a byte con el depósito.
> El suplemento es coherente consigo mismo. Cuando se depositen los datos de la Fase 2 como
> versión nueva, el suplemento corregido entrará de forma natural; hasta entonces, **se deja
> como está**.

## 2quater. Autoría de tres autores — CERRADO 2026-09-29 ✅
Requisito del postgrado: el artículo pasa a tres firmantes en este orden y formato literal.

- [x] Portada: `Herrera, M.` · `Grimón, F.` · `Parejo, A.` — correspondencia: Parejo, A.
- [x] Agradecimientos en plural, con los tres nombrados; fuera «(autoría única)».
- [x] Carta al editor en plural, firmada en nombre de los autores.
- [x] Depósito alineado: `.zenodo.json`, `CITATION.cff`, `README.md`, `LICENSE.md` y el
      suplemento llevan los tres.
- [x] **Zenodo v1.0.3-fase1** (`10.5281/zenodo.23027861`) publicada y verificada: ZIP byte a
      byte con el repositorio (md5 `453e66533890963bbf8a69a03ba5c690`) y los tres creators con
      la forma correcta en los metadatos web.
- [x] **Artículo reenviado a la revista** con la autoría corregida.
- [x] Variantes del nombre registradas en ORCID («Also known as»), que es lo que une las
      formas `Parejo, A.`, `Parejo R., Angel A.` y el nombre completo con y sin acentos.

> **No tocar `execution-package/RESPONSABLES.md`.** Conserva a Parejo, A. como operador único
> y así debe seguir: no es autoría, es el registro de quién tuvo la autoridad de aborto sobre
> un clúster en producción. Ponerle tres nombres sería falso.

## 3. Revisión final — HECHA 2026-09-27 ✅
- [x] PDF de 12 pp leído completo por el autor; conforme.
- [x] Autor, afiliación, correo y ORCID confirmados.

## 4. Envío — HECHO 2026-09-27 ✅
- [x] Enviado a **faraute@uc.edu.ve** el 2026-09-27, con acuse de recibo confirmado.
- [x] Adjuntos: `articulo_angel_parejo_final.pdf`, las 3 figuras de `figuras-envio/`
      (grises, 300 dpi) y `entrega-latex.zip` (fuente LaTeX + suplemento).
- [x] Carta al editor enviada como cuerpo del correo.
- [x] Entrega paralela a la tutora: `entrega-latex.zip`.
- [ ] Queda esperar el dictamen del arbitraje.

---
**Nota:** el artículo compila con **`xelatex`** (no `pdflatex`), y en este proyecto **un log
limpio no prueba que el PDF esté bien**: los literales UTF-8 que XeTeX no mapea a la fuente
Type1 se falsifican en silencio. Si añades algún carácter no-ASCII nuevo, verifícalo.

**Nota:** se envía la versión de **12 pp**. La de **18 pp** (`main_referencia_extendida_18pp.pdf`) y el **suplemento** son tu respaldo para el arbitraje.
