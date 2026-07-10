# Plan de trabajo — Ramas de publicación por venue

**Estado:** APPROVED (2026-07-09) · **Autor:** solo-autor
**Objetivo:** trabajar cada opción de publicación en su propia rama git, para poder volver a cada
una y adaptarla a la revista/congreso correspondiente sin interferencias.

---

## 1. Modelo de ramas

- **`main`** = fuente de verdad. Contiene los artículos canónicos en Markdown
  (`articulo_angelparejov1-6.md`, `articulo_angelparejov2-experimental.md`), el tooling
  (`scripts/`, `Bibliography_base.bib`) y todo `quality_reports/`. Aquí van las correcciones
  de **fondo** (datos, referencias, hechos, redacción de origen).
- **Ramas `pub/<venue>`** = una por opción de publicación, derivadas de `main`. Cada una contiene
  la **adaptación** del artículo a ese venue (formato, extensión, idioma, anonimización) y un
  archivo `PUBLICACION.md` en la raíz con su ficha y checklist.

### Regla de oro
- Cambio de **contenido/fondo** → se hace en `main` y se propaga a las ramas (`git merge main`).
- Cambio de **formato/adaptación** de un venue → se hace SOLO en su rama `pub/<venue>`.

---

## 2. Ramas

| Rama | Artículo | Venue | Formato | Extensión meta | Deadline | Prioridad |
|---|---|---|---|---|---|---|
| `pub/cacic-2026` | v2 | CACIC 2026 (WPDP/WBDDM/WARSO) | Springer LNCS 1-col, A4, 10pt | **≤10 pp** (recorte ~49%) | **29-jul-2026** | 🎯 ALTA |
| `pub/informatica-sistemas` | v2 | Rev. Informática y Sistemas (UTM, Ecuador) | plantilla UTM | 8–16 pp (encaja) | continuo (hasta 30-nov-2026) | Media |
| `pub/clei-2027` | v2 | CLEI 2027 (Scopus/IEEE Xplore) | IEEE 2-col | ~10 pp (encaja) | CFP ~ene-2027 | Media (espera CFP) |
| `pub/impacto` | v2 | Rev. Impacto (UNI Itapúa, Paraguay) | Arial 11 / 1.5 / A4 / 1-col | tope 10 pp (recorte ~50%) | anual continuo | Baja |

**v1-6 conceptual:** permanece en `main`; su paso inmediato es el preprint Zenodo
(`quality_reports/zenodo_deposito_v1-6.md`). Cuando se le elija revista, se abrirá `pub/v1-6-<venue>`.

---

## 3. Flujo de trabajo diario

```bash
# ver en qué rama estoy y cuáles hay
git branch

# cambiar a la revista que quiero trabajar hoy
git switch pub/cacic-2026        # (o el nombre de la rama)

# ... trabajar, luego commitear en ESA rama ...
git add -A && git commit -m "..."

# traer correcciones de fondo hechas en main a esta rama
git switch pub/cacic-2026
git merge main

# volver al tronco
git switch main
```

Al entrar a cualquier rama `pub/*`, leer primero su `PUBLICACION.md` (raíz) para saber
formato, extensión, estado y tareas pendientes de esa revista.

---

## 4. Tareas por rama (resumen; el detalle vive en cada PUBLICACION.md)

- **cacic-2026:** ejecutar `plans/2026-07-09_recorte-lncs-cacic.md` (recorte ~49% apoyando III–IV en
  el v1-6), reformatear a LNCS, insertar autocita al preprint v1-6, enviar por el sistema SAC.
  Precondición: DOI Zenodo del v1-6.
- **informatica-sistemas:** descargar plantilla/normas UTM, abstract+keywords en inglés, anonimizar
  (doble ciego), ajustar refs, enviar por OJS.
- **clei-2027:** monitorear CFP; el DOCX IEEE actual ya es casi la base; abstract EN; ajustar a
  plantilla CLEI cuando se publique.
- **impacto:** reformatear a plantilla Impacto, recorte ~50%, refs ISO 690 `(n)`, anonimizar,
  ORCID+ROR, carta de compromiso, figuras/tablas en ZIP.

---

## 5. Notas

- Flujo solo-autor: se trabaja localmente; push al cerrar sesión. Las ramas `pub/*` se pueden pushear
  a origin para respaldo (`git push -u origin pub/<venue>`).
- No se mezcla ninguna `pub/*` de vuelta a `main` (son destinos finales divergentes, no features).
- La estrategia secuencial sigue vigente: el v1-6 va primero / preprint; el v2 lo cita en cada venue.
