# Guía de trabajo — pg-k8s-paper (git + Claude)

Guía práctica para trabajar este proyecto: estructura de ramas, comandos git para moverte entre
revistas, gestión diaria y cómo trabajar con Claude Code. Vive en `main`.

> **Repo:** https://github.com/angelparejo/pg-k8s-paper · **Rama base:** `main` · Flujo **solo-autor**.

---

## 1. Estructura del proyecto

- **`main`** = fuente de verdad: artículos canónicos en Markdown (`articulo_angelparejov1-6.md`,
  `articulo_angelparejov2-experimental.md`), tooling (`scripts/`, `Bibliography_base.bib`) y
  todo `quality_reports/` (planes, reviews, journal).
- **Ramas `pub/<venue>`** = una por opción de publicación. Cada una adapta el artículo a esa
  revista/congreso (formato, extensión, idioma) y trae un `PUBLICACION.md` en la raíz con su
  ficha y checklist.

| Rama | Venue | Formato | Extensión | Estado |
|---|---|---|---|---|
| `main` | — | Markdown (origen) | — | tronco |
| `pub/cacic-2026` | CACIC 2026 | Springer LNCS 1-col | ≤10 pp (recorte ~49%) | 🎯 deadline **29-jul-2026** |
| `pub/informatica-sistemas` | Rev. Informática y Sistemas (UTM) | plantilla UTM | 8–16 pp (encaja) | sin prisa (hasta 30-nov) |
| `pub/clei-2027` | CLEI 2027 | IEEE 2-col | ~10 pp (encaja) | espera CFP (~ene-2027) |
| `pub/impacto` | Rev. Impacto (Itapúa) | Arial/A4/1-col | 10 pp (recorte ~50%) | baja prioridad |

El **v1-6 conceptual** se queda en `main`; su paso inmediato es el preprint Zenodo
(`quality_reports/zenodo_deposito_v1-6.md`).

---

## 2. Cambiar de revista (lo esencial)

```bash
git branch                     # listar ramas locales (* = actual)
git branch --show-current      # ¿en qué rama estoy?
git switch pub/cacic-2026      # ir a trabajar CACIC
git switch main                # volver al tronco
```

**Al entrar a cualquier `pub/*`, abre primero su `PUBLICACION.md`** (raíz) — ahí está todo lo que
esa revista necesita y el punto donde lo dejaste. En `main` ese archivo no existe (así sabes que
estás en el tronco).

---

## 3. Regla de oro: fondo vs. formato

- **Contenido / datos / referencias / redacción de origen** → se corrige en **`main`**.
- **Formato / plantilla / recorte / idioma de un venue** → se hace **solo en su rama `pub/<venue>`**.

Para llevar una corrección de fondo (hecha en main) a una revista:

```bash
git switch pub/cacic-2026
git merge main                 # trae los cambios de main a esta rama
```

Las ramas `pub/*` son **destinos finales**: nunca se mergean de vuelta a `main`.

---

## 4. Gestión git diaria

```bash
# ver estado y cambios
git status
git diff                       # cambios sin stage
git log --oneline -10          # historial reciente

# guardar trabajo
git add -A
git commit -m "mensaje claro"

# respaldar en GitHub
git push                       # rama actual (ya tienen tracking configurado)
git push -u origin pub/NUEVA   # primera vez de una rama nueva

# crear una rama de publicación nueva (siempre desde main)
git switch main
git switch -c pub/<venue>
```

**Guardar sin commitear (cambio de contexto rápido):**
```bash
git stash            # guarda cambios temporalmente
git switch otra-rama
git switch -         # vuelve a la rama anterior
git stash pop        # recupera los cambios
```

**Deshacer con cuidado:**
```bash
git restore ARCHIVO            # descarta cambios NO commiteados de un archivo
git revert <hash>              # crea un commit que revierte otro (seguro)
```
> Evita `git reset --hard` / `git push --force` salvo que sepas exactamente qué haces.

---

## 5. Trabajar con Claude Code

### Retomar el trabajo
- Abre Claude en el directorio del proyecto y di **"retoma la última sesión"**. Claude lee el
  `SESSION_REPORT.md`, el `quality_reports/research_journal.md`, el git log y su memoria.
- Dile en qué rama/revista quieres trabajar: *"trabajemos `pub/cacic-2026`"* → Claude hace el
  `git switch` y sigue el `PUBLICACION.md` de esa rama.

### Idioma
- Todo en **español** (respuestas, preguntas, redacción). El paper se escribe en español; la
  traducción al inglés es una fase final por venue.

### Comandos (skills) útiles
| Comando | Para qué |
|---|---|
| `/checkpoint` | Guardar el estado de la sesión (memoria + SESSION_REPORT + journal) antes de cerrar o compactar |
| `/write` | Redactar/revisar secciones del paper (+ pase humanizer) |
| `/review` | Revisión de calidad / peer review simulado |
| `/revise` | Procesar comentarios de árbitros (R&R) |
| `/submit` | Empaquetado y compuerta final de envío |
| `/tools` | Utilidades: commit, compilar, validar bib, etc. |

### Cómo mantiene contexto Claude
- **Memoria persistente:** preferencias y estado del proyecto se guardan solos entre sesiones.
- **Planes en disco:** `quality_reports/plans/` — sobreviven al cierre de sesión.
- **Journal:** `quality_reports/research_journal.md` — bitácora de cada avance.
- **Antes de cerrar sesión:** pídele **`/checkpoint`** para que persista todo.

### Buenas prácticas
- Para tareas grandes, Claude planifica primero (plan en `quality_reports/plans/`) y pide tu OK.
- Sesiones cortas y enfocadas (5–10 turnos); `/checkpoint` al terminar.
- Confirma la rama antes de editar formato: *"¿en qué rama estamos?"*

---

## 6. Documentos clave del proyecto

| Archivo | Contenido |
|---|---|
| `CLAUDE.md` | Instrucciones y arquitectura del proyecto (para Claude) |
| `GUIA_TRABAJO.md` | Esta guía |
| `PUBLICACION.md` (en cada `pub/*`) | Ficha y checklist de esa revista |
| `quality_reports/convocatorias_y_venues.md` | Análisis de todas las opciones de publicación |
| `quality_reports/plans/2026-07-09_ramas-publicacion.md` | Plan del modelo de ramas |
| `quality_reports/plans/2026-07-09_recorte-lncs-cacic.md` | Plan de recorte del v2 a LNCS |
| `quality_reports/zenodo_deposito_v1-6.md` | Paquete para hacer citable el v1-6 (preprint) |
| `SESSION_REPORT.md` | Bitácora de sesiones |

---

## 7. Estado actual (2026-07-09) y próximos pasos

- ✅ v1-6: refs corregidas; paquete Zenodo listo. **Falta:** subir PDF a Zenodo y pasar el DOI.
- ✅ v2-experimental: revisado (Revisión Menor, writer-critic 98). DOCX IEEE hecho.
- ✅ 4 ramas de publicación creadas y pusheadas.
- ⏭️ **Decisión abierta:** ¿ir a CACIC 2026 (deadline 29-jul, implica recorte LNCS ~49%) o vía sin prisa?
- ⏭️ Cuando llegue el DOI del v1-6: insertar la autocita en el v2 y ejecutar el plan de la rama elegida.

---

## 8. Notas del entorno

- **Air-gapped / stdlib:** los `scripts/` usan solo bash + Python estándar (sin `pip install`, sin R).
- **Sin conversores de documentos** en el entorno (LibreOffice/pandoc): DOCX→PDF lo haces tú desde Word.
- El `articulo_..._IEEE_rev.docx` (tu copia con amarillos) está sin trackear y aparece en todas las ramas.
