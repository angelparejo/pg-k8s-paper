# Convocatorias y Venues de Publicación — v2-experimental

> **Propósito:** registro de opciones de publicación para el artículo **v2-experimental**
> ("Análisis Multicapa de Operadores de PostgreSQL y Almacenamiento CSI en Kubernetes:
> un Marco de Análisis y un Estudio Empírico de CloudNativePG bajo Fallos Inyectados").
> Documento vivo — ampliar en próximas sesiones.
>
> **Última actualización:** 2026-07-09 (deadlines verificados vía web)
> **Artículo evaluado:** `articulo_angelparejov2-experimental_IEEE_rev.docx`

---

## 1. Características del artículo (estado actual)

| Atributo | Valor |
|---|---|
| Idioma | Español (sin resumen/título/keywords en inglés) |
| Formato | Plantilla **IEEE dos columnas**, Times New Roman, tamaño Carta |
| Extensión | **~9.800 palabras de cuerpo ≈ ~10 páginas IEEE** a dos columnas |
| Tablas/figuras | 2 tablas + 1 figura (3 elementos) |
| Referencias | ~21, estilo IEEE `[n]` |
| Autoría | Autor único (Angel A. Parejo R., Universidad de Carabobo, Venezuela) |
| Tipo | Estudio empírico original + marco conceptual (taxonomía, vocabulario S=(O,K,M,D), invariantes) |

**Insight transversal (corregido 2026-07-09):** el formato IEEE **favorece** en CLEI y CONCAPAN (usan IEEE),
pero **CACIC usa Springer LNCS (una columna), NO IEEE** — dato clave que obliga a reformatear. La extensión
"~10 pp IEEE" es engañosa: son ~9.100 palabras, que en LNCS 1-col ocupan ~16–18 pp (excede el tope de 10 de
CACIC) y en revistas con plantilla propia (Impacto, 1-col) también se dispara. El conteo bajo IEEE 2-col es el
único donde "cabe en 10 pp". Ver §8.

---

## 2. Revista Impacto (UNI Itapúa, Paraguay) — análisis detallado

- **URL:** https://revistas.uni.edu.py/index.php/impacto/
- **Editor:** Facultad de Ciencias y Tecnología, Universidad Nacional de Itapúa (Paraguay)
- **Alcance:** ciencias exactas y naturales, biotecnología, ingeniería (alimentos, ambiente, sociedad, tecnológica). Multidisciplinaria.
- **ISSN:** 2789-861X (e-ISSN) · **Indexación:** ROAD, LATINDEX · **Licencia:** CC BY-NC 4.0
- **Periodicidad:** anual con publicación continua · **Costos:** sin cuotas
- **Revisión:** doble ciego, ≥2 pares
- **Idioma:** español, con resumen en inglés obligatorio

### Elegibilidad de contenido (dejando formato aparte)
- ✅ Área temática (encaja en "ingeniería"/"tecnológica")
- ✅ Tipo de artículo (Artículo de investigación)
- ✅ Contribución original arbitrable
- ⚠️ **Obstáculo mayor: extensión.** Todos los tipos topan en **10 páginas** (opinión 8). En la plantilla
  de la revista (Arial 11, interlineado 1.5, 1 columna, A4) el artículo se estima en **~18–22 páginas** →
  requeriría **recortar ~a la mitad** o dividir en dos piezas.
- ❌ **Falta resumen/keywords/título en inglés** (contenido, no formato)
- ❌ Manuscrito debe ir **anonimizado** para doble ciego (hoy tiene nombre/afiliación/email)

### Incumplimientos de formato (abordar luego)
Arial 11 (tiene Times), interlineado 1.5 (tiene IEEE), A4 (tiene Carta), 1 columna (tiene 2),
márgenes 3cm sup / 2.5cm resto (tiene ~1.9/1.57), título ≤15 palabras (tiene 24),
referencias ISO 690 numérico entre paréntesis `(n)` tam. 10 sangría francesa 1.27cm,
ORCID de autores + ROR en afiliación, carta de compromiso firmada, figuras/tablas en ZIP `.png/.pdf`.

**Veredicto:** elegible temáticamente pero **no enviable tal cual**; el tope de 10 páginas es vinculante.

---

## 3. Panorama de venues (2026-07-09)

### Congresos (con convocatoria/deadline)

| Venue | Deadline | Congreso | Idioma | Formato/ext. | Estado / encaje |
|---|---|---|---|---|---|
| **CACIC 2026** (Argentina, UTN-FRCU) | **29-jul-2026 — ✅ ABIERTA (verificado 2026-07-09, ~20 días)** | 5–9 oct 2026 | **Español** | **LNCS 1-col, máx 10 pp** (⚠️ NO IEEE) | 🎯 Ventana inmediata. Idioma ✅ pero **requiere reformatear IEEE→LNCS + recortar ~40%** (ver §8) |
| **CLEI 2026** (México, CDMX) | Abstract 19-abr-2026 — **CERRADA** | 7–11 sep 2026 | Es/En | IEEE, **Scopus** vía IEEE Xplore | ⭐ Hogar natural — apuntar a **CLEI 2027** (aún sin anunciar sede/CFP a jul-2026) |
| **CONCAPAN 2026** (IEEE, Centroamérica) | **15-jul-2026** | 11–13 nov 2026 | Presenta Es, **publica en inglés** | IEEE, **máx 6 pp** | ❌ Tope 6 pp + inglés → no cabe, sin tiempo |

Venues top en inglés (NSDI'27, OSDI'27, ICDCS, IEEE CLOUD): fuera de alcance realista para
este paper (idioma, formato regional, competitividad). Solo aspiracional.

### Revistas (envío continuo, sin deadline)

| Revista | Institución | Idioma | Indexación | Notas |
|---|---|---|---|---|
| **Informática y Sistemas** | UTM, Ecuador | Es/En | Latindex, **DOAJ**, Dialnet, Redalyc | ⭐ Más accionable. **Extensión 8–16 pp → nuestro ~10 pp ENCAJA (verificado)**. e-ISSN 2550-6730, semestral, doble ciego externo, sin cuotas. `revista.iys@utm.edu.ec` |
| **Rev. Latinoamericana de Computación (LAJC)** | EPN, Ecuador | Es/En | Open access, par revisado | Buen encaje |
| **Rev. Científica de Sistemas e Informática (RCSI)** | UNSM, Perú | Es | Par revisado | Cola de publicación (backlog) |
| **Revista Impacto** | UNI Itapúa, Paraguay | Es (+abstract EN) | ROAD, Latindex | Ver §2 — tope 10 pp obliga a recortar |

---

## 4. Recomendación (2026-07-09, tras verificar deadlines)

1. 🎯 **Ventana urgente → CACIC 2026 (deadline 29-jul-2026, ~20 días).** Español, formato IEEE
   ya listo (~10 pp), congreso de referencia en Argentina (RedUNCI). Es la única venue con
   deadline abierto y encaje total idioma+formato. **Decisión bloqueante:** choca con la
   estrategia secuencial (v1-6-conceptual debe ir primero y el v2 lo cita). Ver §7.
2. **Vía sin prisa → Informática y Sistemas (UTM, Ecuador).** Revista de informática (no
   generalista), español, DOAJ, sin cuotas, árbitros especialistas externos, extensión 8–16 pp
   (encaja). Envío continuo — no compite con el deadline de CACIC.
3. **Objetivo de congreso a futuro → CLEI 2027.** Máximo prestigio/indexación regional (Scopus),
   formato IEEE ya listo, admite español. CLEI 2027 **aún sin anunciar** sede/CFP (a jul-2026);
   CLEI 2026 (CDMX, 7–11 sep) ya cerró abstracts (19-abr).

---

## 5. Acciones pendientes (para próximas sesiones)

- [x] ~~Verificar si **CACIC 2026** sigue abierta~~ → **ABIERTA, deadline 29-jul-2026** (CONFEDI + CFP oficial, 2026-07-09)
- [x] ~~Revisar **límite de páginas** de *Informática y Sistemas*~~ → **8–16 pp, encaja** (2026-07-09)
- [x] ~~Revisar bases/formato de CACIC 2026~~ → **LNCS 1-col, máx 10 pp, es/en/pt** (ver §8, 2026-07-09)
- [ ] **DECISIÓN URGENTE:** ¿someter v2 a CACIC 2026 (implica reformatear a LNCS + recortar ~40%) antes del 29-jul, o ir sin prisa a Informática y Sistemas / CLEI 2027? Ver §7.
- [ ] Descargar plantilla oficial CACIC (LaTeX2e / Word) y confirmar si exige anonimización
- [ ] Ejecutar el **plan de recorte/reformateo LNCS** si se elige CACIC → `quality_reports/plans/2026-07-09_recorte-lncs-cacic.md`
- [ ] Redactar **título corto (≤15 palabras)** + **Abstract/Keywords en inglés** (requisito común a varias vías)
- [ ] Preparar **versión anonimizada** (doble ciego) — para las revistas; probablemente NO para CACIC
- [ ] Si se opta por Impacto: decidir estrategia de **recorte ~50%** o material suplementario, y reformateo a plantilla Impacto
- [ ] Monitorear anuncio de **CLEI 2027** (aún sin CFP a jul-2026)
- [ ] Alinear con la **estrategia de publicación secuencial** (v1-6-conceptual va primero; v2 cita al v1)

---

## 6. Fuentes consultadas

- Revista Impacto — Directrices y Enfoque/Alcance: https://revistas.uni.edu.py/index.php/impacto/es/about
- CLEI 2026 CFP: https://clei.org/en/2026/01/08/call-for-papers-clei-2026/ · https://conferencia2026.clei.org/
- CACIC 2026 sede/fechas: https://frcu.utn.edu.ar/index.php/vida-educativa/noticias/la-utn-frcu-sera-sede-del-cacic-2026
- CACIC 2026 Call for Full Papers (bases): https://frcu.utn.edu.ar/index.php/congreso-cacic/call-for-full-papers-cacic
- CACIC 2026 deadline (CONFEDI): https://confedi.org.ar/evento/fecha-limite-recepcion-de-trabajos-para-el-cacic-2026/
- CACIC 2024 CFP (workshops + publicación CCIS): https://cacic2024.info.unlp.edu.ar/call-for-papers-2/
- CACIC 2018 formato (LNCS): https://cacic2018.exa.unicen.edu.ar/formato.html
- CONCAPAN 2026 CFP: https://attend.ieee.org/concapan-2026/es/call-for-papers-es/
- Informática y Sistemas (UTM): https://revistas.utm.edu.ec/index.php/Informaticaysistemas/information/authors
- Rev. Latinoamericana de Computación (LAJC, EPN): https://webhistorico.epn.edu.ec/revista-latinoamericana-de-computacion/
- Rev. Científica de Sistemas e Informática (RCSI, UNSM): https://revistas.unsm.edu.pe/index.php/rcsi
- Ref. estructural on-topic (fault injection K8s): Chen, Goudarzi, Toosi, *Resilience Evaluation of Kubernetes via Failure Injection*, arXiv:2507.16109, 2025.

---

## 7. Conflicto con la estrategia de publicación secuencial (decisión pendiente)

La ventana de CACIC 2026 (29-jul) fuerza una decisión antes diferida:

- **Estrategia acordada:** v1-6-conceptual se somete PRIMERO; el v2-experimental lo cita y espera su turno.
- **Estado del v1-6:** ✅ **ya NO está bloqueado** — las 5 refs dudosas se corrigieron (commit `e6c8024`). Único pendiente: elegir venue.
- **Sinergia:** buena parte del volumen del v2 (Secs. III–IV: taxonomía, modelo S=(O,K,M,D), invariantes, análisis comparativo) ES el contenido del v1-6. Si el v1-6 va primero y el v2 lo cita, el v2-para-CACIC puede **comprimir III–IV a un resumen + cita a [v1-6]** y quedarse con la parte empírica → recorte natural a ~10 pp LNCS y refuerzo de la cita anti-"salami".

**Opciones:**
1. **Sprint dual (agresivo):** en ~20 días, elegir venue del v1-6 + producir el v2-CACIC recortado que lo cita. Alto esfuerzo.
2. **v2 a CACIC citando v1-6 como preprint** (Zenodo/arXiv). Aprovecha la ventana; rompe parcialmente el orden estricto.
3. **Respetar el orden, saltar CACIC 2026:** v1-6 primero sin prisa; v2 a Informática y Sistemas (envío continuo) o CLEI 2027. Sin presión de deadline.

---

## 8. Bases CACIC 2026 (Full Papers) + plan de adaptación

### 8.1 Bases verificadas (2026-07-09)

| Aspecto | Regla |
|---|---|
| Deadline envío | **29/07/2026** · Notificación 07/09/2026 · Congreso 5–9 oct 2026 (Concepción del Uruguay) |
| Extensión | **Máximo 10 páginas**, sin numerar, sin encabezado/pie |
| Papel / formato | **A4**, **plantilla Springer LNCS (una columna, 10 pt)** — *NO IEEE* |
| Archivos | Word, LaTeX o PDF (plantillas LaTeX2e / Office2007 / Word-97-2003) |
| Idioma | **Español**, inglés o portugués |
| Envío | Web del congreso (sistema SAC propio, no EasyChair) |
| Actas | ISBN en SEDICI; **mejores trabajos → Springer CCIS (Scopus/DBLP/EI)**; otros → revistas JCS&T, TE&E |
| Doble ciego | **No exigido explícitamente** (CACIC históricamente no anonimiza el envío) — confirmar en plantilla |

**Workshops candidatos** (se elige uno): **WPDP** (Procesamiento Distribuido y Paralelo, fuerte encaje) · **WBDDM** (Bases de Datos) · **WARSO** (Arquitecturas, Redes y S.O.).

### 8.2 Diagnóstico de encaje

- ✅ **Estructura:** el v2 ya cumple la estructura estándar del campo (Intro / Related Work / Modelo / Setup / Resultados / Discusión / Conclusiones / Datos). No requiere reorganización de fondo.
- ✅ **Idioma:** español, admitido.
- ⚠️ **Formato:** el DOCX IEEE actual **no sirve**; hay que producir versión **LNCS**.
- ❌ **Extensión (obstáculo principal):** ~9.100 palabras de cuerpo. En IEEE 2-col ≈ 10 pp, pero en **LNCS 1-col ≈ 16–18 pp** → excede el tope de 10 pp. Requiere **recorte de ~40%** (a ~5.500–6.000 palabras).

### 8.3 Plan de adaptación

Detallado en `quality_reports/plans/2026-07-09_recorte-lncs-cacic.md`. Resumen:
1. Poner el v1-6 en estado citable (someter o preprint con DOI).
2. Comprimir Secs. III–IV del v2 a un recap breve + cita a [v1-6].
3. Reformatear a plantilla LNCS de CACIC (Word o LaTeX).
4. Ajustar refs a estilo LNCS/Springer; verificar ≤10 pp; elegir workshop.
