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

**Insight transversal:** el formato IEEE **perjudica** en revistas con plantilla propia (p. ej. Impacto)
pero **favorece** en congresos latinoamericanos de informática (CLEI/CACIC/CONCAPAN usan IEEE).
La extensión (~10 pp IEEE) encaja bien en congresos, pero excede el tope de varias revistas.

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
| **CACIC 2026** (Argentina, UTN-FRCU) | **29-jul-2026 — ✅ ABIERTA (verificado 2026-07-09, ~20 días)** | 5–9 oct 2026 | **Español** | IEEE, ~10 pp | 🎯 **MEJOR OPCIÓN INMEDIATA.** Idioma+formato ya listos. VERIFICAR normas exactas en `frcu.utn.edu.ar/cacic-2026` |
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

- [ ] Verificar si **CACIC 2026** sigue abierta (deadline exacto) en `frcu.utn.edu.ar/cacic-2026`
- [ ] Revisar **normas y límite de páginas** de *Informática y Sistemas* (UTM)
- [ ] Redactar **título corto (≤15 palabras)** + **Abstract/Keywords en inglés** (requisito común a todas las vías)
- [ ] Preparar **versión anonimizada** (doble ciego) del manuscrito
- [ ] Si se opta por Impacto: decidir estrategia de **recorte ~50%** o material suplementario, y reformateo a plantilla Impacto
- [ ] Confirmar fecha de apertura de **CLEI 2027**
- [ ] Alinear con la **estrategia de publicación secuencial** (v1-6-conceptual va primero; v2 cita al v1)

---

## 6. Fuentes consultadas

- Revista Impacto — Directrices y Enfoque/Alcance: https://revistas.uni.edu.py/index.php/impacto/es/about
- CLEI 2026 CFP: https://clei.org/en/2026/01/08/call-for-papers-clei-2026/ · https://conferencia2026.clei.org/
- CACIC 2026: http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=194886 · https://frcu.utn.edu.ar/index.php/vida-educativa/noticias/la-utn-frcu-sera-sede-del-cacic-2026
- CONCAPAN 2026 CFP: https://attend.ieee.org/concapan-2026/es/call-for-papers-es/
- Informática y Sistemas (UTM): https://revistas.utm.edu.ec/index.php/Informaticaysistemas/index
- Rev. Latinoamericana de Computación (LAJC, EPN): https://webhistorico.epn.edu.ec/revista-latinoamericana-de-computacion/
- Rev. Científica de Sistemas e Informática (RCSI, UNSM): https://revistas.unsm.edu.pe/index.php/rcsi
