# Depósito Zenodo — v1-6 conceptual (para hacerlo citable)

**Objetivo:** publicar el v1-6 conceptual como **preprint con DOI** en Zenodo, para que el
v2-experimental (y su versión CACIC) puedan citarlo — precondición del plan de recorte LNCS
(`plans/2026-07-09_recorte-lncs-cacic.md`, §2) y de la estrategia de publicación secuencial.

**Estado:** preparado 2026-07-09. Falta el paso manual del usuario (subir PDF + confirmar DOI).

---

## Paso manual del usuario (único bloqueo)

El entorno es air-gapped (sin LibreOffice/pandoc), así que la conversión a PDF y la subida las haces tú:

1. Abre `articulo_angelparejov1-6_IEEE.docx` en Word → **Archivo → Guardar como / Exportar → PDF**.
   (La Fig. 1 ya está incrustada en el DOCX —SVG nativo + PNG de respaldo—, no hay que insertar nada.
   Verifica solo que Word la renderice bien; en Word 2016+ el SVG se ve correctamente.)
2. Entra a https://zenodo.org → **New upload** → sube el PDF.
3. Rellena los metadatos con la tabla de abajo (copiar/pegar).
4. **Reserve DOI** (Zenodo permite reservar el DOI antes de publicar) → cópialo.
5. Publica.
6. Pásame el **DOI real** y lo sustituyo en la cita `[REF-V1-6]` (placeholder abajo) en el v2 / v2-CACIC.

> Nota licencia: **CC BY 4.0** es la opción estándar para preprint y compatible con un envío
> posterior a CACIC / Springer CCIS. Si prefieres otra (CC BY-NC, o "todos los derechos
> reservados"), dímelo y ajusto.

---

## Metadatos Zenodo (copiar/pegar)

| Campo | Valor |
|---|---|
| **Resource type** | Publication → **Preprint** |
| **Title** | Hacia un Análisis Multicapa de Operadores de PostgreSQL y Almacenamiento CSI en Kubernetes: Taxonomía, Modelo Formal y Protocolo Experimental Reproducible |
| **Authors** | Parejo R., Angel A. — Universidad de Carabobo (Valencia, Estado Carabobo, Venezuela) |
| **ORCID** | *(pegar el tuyo si tienes; si no, dejar vacío)* |
| **Publication date** | 2026-07-09 |
| **Language** | Spanish (es) |
| **License** | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| **Version** | v1 |
| **Keywords** | Kubernetes; PostgreSQL; operadores de bases de datos; CSI; arquitecturas nativas de la nube; sistemas distribuidos; consistencia; resiliencia; failover |

### Description (pegar como descripción / abstract)

> La creciente adopción de Kubernetes como plataforma de orquestación de contenedores ha impulsado
> el surgimiento de operadores de bases de datos (PostgreSQL) y de la Container Storage Interface (CSI).
> Su interacción es crítica en arquitecturas nativas de la nube, pero rara vez se analiza de forma
> integrada. Este artículo propone un marco conceptual para dicho análisis: una taxonomía de operadores
> y almacenamiento CSI, un modelo formal de interacción multicapa S=(O,K,M,D), y un conjunto de
> invariantes de consistencia, disponibilidad y durabilidad. Con base en el comportamiento documentado
> de los operadores, se analiza cómo esta interacción puede influir en la recuperación y la consistencia
> de cargas PostgreSQL gestionadas mediante operadores. Como contribución adicional, se especifica un
> protocolo experimental reproducible —con inyección controlada de fallos y análisis no paramétrico—
> para validar empíricamente el marco; su ejecución queda como trabajo futuro. El aporte de este
> artículo es el marco conceptual y el protocolo, no resultados empíricos.

---

## Cita lista para insertar (tras confirmar DOI)

Placeholder actual: `10.5281/zenodo.XXXXXXX` → reemplazar por el DOI real.

**IEEE (para el v2-experimental, estilo `[n]`):**

> [N] A. A. Parejo R., "Hacia un análisis multicapa de operadores de PostgreSQL y almacenamiento CSI
> en Kubernetes: taxonomía, modelo formal y protocolo experimental reproducible," preprint, Zenodo,
> jul. 2026, doi: 10.5281/zenodo.XXXXXXX.

**LNCS/Springer (para el v2-CACIC):**

> Parejo R., A.A.: Hacia un análisis multicapa de operadores de PostgreSQL y almacenamiento CSI en
> Kubernetes: taxonomía, modelo formal y protocolo experimental reproducible. Preprint, Zenodo (2026).
> https://doi.org/10.5281/zenodo.XXXXXXX

**BibTeX (para `Bibliography_base.bib`):**

```bibtex
@misc{parejo2026marco,
  author       = {Parejo R., Angel A.},
  title        = {Hacia un An\'alisis Multicapa de Operadores de {PostgreSQL} y
                  Almacenamiento {CSI} en {Kubernetes}: Taxonom\'ia, Modelo Formal
                  y Protocolo Experimental Reproducible},
  howpublished = {Preprint, Zenodo},
  year         = {2026},
  doi          = {10.5281/zenodo.XXXXXXX},
  note         = {Versi\'on conceptual; el estudio emp\'irico se reporta en un trabajo posterior}
}
```

---

## Dónde se insertará la cita en el v2 (al ejecutar el recorte LNCS)

Según `plans/2026-07-09_recorte-lncs-cacic.md`, la cita a este preprint sostiene la compresión de las
Secciones III (Modelo y Marco) y IV (Análisis Comparativo) del v2 → un recap breve + "…detallado en
[REF-V1-6]". Esto refuerza además la cadena de citas anti-"salami slicing" (el v2 declara explícitamente
que el marco fue establecido en el v1-6).
