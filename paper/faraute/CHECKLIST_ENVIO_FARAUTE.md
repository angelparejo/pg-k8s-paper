# Checklist de envío — Revista FARAUTE de Ciencias y Tecnología (UC/FACYT)

**Manuscrito:** *Análisis multicapa de operadores de PostgreSQL y almacenamiento CSI en Kubernetes: un marco de análisis y un estudio empírico de CloudNativePG bajo fallos inyectados*
**Autor:** Angel A. Parejo R. — Universidad de Carabobo
**Tipo:** Artículo científico (≤ 12 páginas)
**Destino:** faraute@uc.edu.ve
**Fecha de esta checklist:** 2026-08-13

---

## A. Estado del manuscrito (LISTO ✅)

- [x] Versión final **12 páginas** — `paper/faraute/main_final_12pp.pdf` (= `main.pdf` / `main.tex`)
- [x] Compila limpio con `pdflatex` (2 pasadas), 0 referencias sin resolver, 0 *overfull*
- [x] **Corrección de registro (2026-08-17):** las notas previas decían "0 *underfull*". Era un
  falso negativo: `main.log` está en ISO-8859 y `grep` lo trataba como binario, silenciando la
  salida. El conteo real era 17. La Tabla 1 usaba columnas `X` justificadas mientras la Tabla 2
  ya llevaba `\raggedright` — inconsistencia corregida, y con ella desaparecen las 4 cajas
  sueltas de celdas estrechas (incluidas las dos de *badness* 10000). Quedan 4 en cuerpo y
  bibliografía, de *badness* 1127–2486 (cosméticas: una pizca de espacio interpalabra por
  identificadores largos como `readOnlyRootFilesystem` en una columna angosta), más 9 `\vbox`
  normales de una maqueta a dos columnas con flotantes. **La paginación no se movió: sigue en 12 pp.**
- [x] Versión extendida de referencia (18 pp) preservada — `main_referencia_extendida_18pp.pdf` (NO se envía; es para tu consulta)
- [x] Cifras verificadas 3× (reproducibles con `replication/execution-package/manifiestos/scripts/analyze.py`)
- [x] Revisiones de árbitros incorporadas (Jepsen/Elle; reencuadre a V(fallo,K); salvedades intra-nodo; semántica ACK-perdido; correcciones de referencias)

---

## B. PENDIENTE DE TU LADO (lo que falta antes de enviar) ⏳

### B1. Figuras a escala de grises + renombrado para entrega — RESUELTO 2026-08-16 ✅
La guía Faraute (punto 9) exige figuras en **blanco y negro o escala de grises**, JPEG/TIFF, **300 dpi**, nombradas `Fig`+número.

- [x] ImageMagick 6.9.12-98 instalado (el entorno no lo tenía; ver nota de red abajo).
- [x] Las 3 figuras convertidas: `Gray`, 1 canal, **300 dpi conservados**.
- [x] **Legibilidad revisada una por una.** El color era decorativo en las tres: toda la
  semántica vive en las etiquetas de texto. La Fig4 (timeline) aguanta bien — las barras
  F1/F2 se distinguen por longitud y por su etiqueta en el eje, no por el tono. No hizo
  falta regenerar ninguna con patrones.
- [x] Copias renombradas para la entrega en **`figuras-envio/`**:
  `Fig1.jpg` ← `figures/Fig2.jpg` (banco de pruebas) ·
  `Fig2.jpg` ← `figures/Fig4.jpg` (timeline) ·
  `Fig3.jpg` ← `figures/Fig5.jpg` (predicado de visibilidad).
  Los `\includegraphics` de `main.tex` no se tocaron.
- [x] Originales a color preservados en `figures/color-originales/`.
- [x] `main.pdf` regenerado: 12 pp, 0 overfull, 0 underfull, 0 refs sin resolver.
  El PDF quedó íntegramente en `DeviceGray` (0 `DeviceRGB`).

> **Nota de red:** el puerto 53 (DNS) está bloqueado en esta máquina por un conflicto entre
> NordVPN y la VPN Check Point corporativa. La instalación se hizo resolviendo los repos por
> DNS-over-HTTPS y fijándolos temporalmente en `/etc/hosts`. Si hace falta `apt` otra vez,
> hay que repetir ese parche.

### B2. Depósito Zenodo y DOI — automatizado 2026-08-17 ⚙️
- [ ] Subir a Zenodo el ZIP `paper/faraute/zenodo-deposito-fase1.zip` (o el contenido de `replication/`)
- [ ] **"Reserve DOI"** en el formulario de Zenodo (obtienes el DOI antes de publicar)
- [ ] Ejecutar desde la raíz del proyecto: `python3 scripts/set_zenodo_doi.py 10.5281/zenodo.<numero>`
- [ ] Volver a subir el ZIP rearmado y **publicar** el depósito en Zenodo

El guion sustituye el marcador donde realmente vive y hace el resto del trabajo:

| Archivo | Qué contiene |
|---|---|
| `main.tex` | disponibilidad de datos (manuscrito) |
| `main_referencia_extendida_18pp.tex` | ídem, versión extendida de referencia |
| `replication/supplement/suplemento.tex` | 2 menciones (nota inicial y cierre) |
| `replication/CITATION.cff` | campo `doi:` |
| `carta_al_editor.md` | cuerpo del correo al editor |
| `replication/.zenodo.json` | campo `notes` — **texto instructivo**, se reescribe la frase |
| `replication/README.md` | sección "Cómo obtener el DOI" — **instructivo**, se reescribe |

> Los dos últimos no son campos DOI sino instrucciones que *mencionan* el marcador: una
> sustitución literal produciría un sinsentido ("sustituir `DOI: 10.5281/…` por el concept
> DOI"). Por eso el guion los reescribe en vez de reemplazar la cadena. La lista previa de
> "5 archivos" de esta checklist estaba incompleta y no distinguía ambos casos.

Además recompila `main.tex`, la versión de 18 pp y el suplemento (2 pasadas cada uno),
sincroniza `main_final_12pp.pdf`, rearma el ZIP y verifica que no quede ningún marcador.
`--check` informa el estado; `--dry-run` muestra los cambios sin escribirlos.

### B3. Revisión final del autor
- [ ] Lectura completa del PDF de 12 pp (coherencia tras el recorte)
- [ ] Confirmar datos de autor: nombre, afiliación, correo (`angelparejo@gmail.com`), ORCID `0009-0001-9737-7116`
- [ ] Confirmar que el correo de correspondencia es el correcto

### B4. Carta al editor — REDACTADA 2026-08-17 ✅
- [x] Borrador listo en `carta_al_editor.md`, para pegar como cuerpo del correo. Cubre:
  modalidad (artículo científico), aporte conceptual + empírico, hallazgo central con la
  salvedad de co-localización intra-nodo, material suplementario en Zenodo, declaraciones
  (originalidad, no envío simultáneo, sin financiamiento, sin conflictos, uso declarado de
  IA como apoyo de redacción) y cumplimiento de las normas de la revista.
- [ ] Poner la fecha y, si se conoce, el nombre del editor en ejercicio (hoy va como
  "Comité Editorial").
- [ ] Revisarla antes de enviar — es tu voz, no la mía.

---

## C. Cumplimiento de formato Faraute (verificado ✅)

Todos satisfechos por la plantilla LaTeX; deja constancia al revisar el PDF:

- [x] Times New Roman 12 (mathptmx)
- [x] Doble columna, excepto título, autores y resumen
- [x] Interlineado simple
- [x] Papel Carta, márgenes 2,5 cm por lado
- [x] Título español (TNR 14, MAYÚS, negrita, centrado) → título inglés (12, negrita)
- [x] Información de autor con superíndice y correo
- [x] Resumen ≤ 150 palabras (146) + 3–5 palabras clave alfabéticas; Abstract (144) + Keywords en inglés
- [x] Secciones numeradas en negrita
- [x] Figuras "Fig." y tablas "Tabla", TNR 10, alineadas a la izquierda, **debajo**
- [x] Ecuaciones numeradas entre paréntesis, citadas como "Ec."
- [x] Unidades SI
- [x] Referencias autor-año alfabéticas en formato Faraute; citas (Autor, año) / (A & B, año) / (A et al., año)
- [x] **Escala de grises 300 dpi** en las figuras (B1 resuelto; PDF sin `DeviceRGB`)
- [x] Silabeo castellano real (`texlive-lang-spanish` + patrones activos en `language.dat`)

---

## D. Logística de envío

- [ ] Manuscrito en **PDF** (aceptado por la guía; alternativa MSWord ≥ XP no necesaria)
- [ ] Adjuntar las **3 copias digitales de figuras** (Fig1/Fig2/Fig3, grises, 300 dpi, JPEG/TIFF)
- [ ] Cuerpo del correo: `carta_al_editor.md` (ver B4)
- [ ] (Recomendado) Mencionar en el cuerpo del correo el **DOI del material suplementario** (Zenodo)
- [ ] Enviar a **faraute@uc.edu.ve**
- [ ] Guardar acuse/fecha de envío

---

## E. Después del envío

- [ ] Registrar fecha de envío (los artículos van a arbitraje en extenso)
- [ ] Plazo de correcciones si hay modificaciones: **3 semanas** (guía; máx. 6 meses de espera)
- [ ] Tener a mano la **versión extendida de 18 pp** y el **suplemento** para responder al árbitro con detalle
- [ ] Preparar respuestas apoyadas en el depósito (reproducibilidad, sensibilidad de exclusiones, permutación, semántica del verificador)

---

## Notas
- La **versión de 12 pp es la que se envía**; la de 18 pp es solo tu referencia.
- El **suplemento** (`replication/supplement/suplemento.pdf`) carga el detalle que el recorte quitó del cuerpo — respalda las respuestas a árbitros.
- Informes de validación previos en `quality_reports/reviews/faraute_*.md`.
