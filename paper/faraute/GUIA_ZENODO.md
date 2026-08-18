# Guía paso a paso — depositar en Zenodo y obtener el DOI

**Para:** el depósito de reproducibilidad del artículo de Faraute
**Archivo a subir:** `paper/faraute/zenodo-deposito-fase1.zip` (179 KB, 43 archivos)
**Tiempo estimado:** 15–20 minutos
**Verificado contra la documentación oficial de Zenodo el 2026-08-18**

---

## 1. ¿Es gratis? Sí

Zenodo lo construyen y operan **el CERN y OpenAIRE**, con financiación europea. **No cobra
nada por depositar** ni por el DOI: no hay cuota de publicación ni de mantenimiento.

- Límite de tamaño: **50 GB por registro** (ampliable caso por caso). Tu ZIP pesa 179 KB, así
  que ni te acercas.
- El DOI lo emite Zenodo a través de DataCite y es permanente.
- No hay letra pequeña ni versión de pago: es infraestructura pública de investigación.

---

## 2. Qué necesitas antes de empezar

| | |
|---|---|
| **Una cuenta de Zenodo** | Regístrate **con ORCID** — ya tienes uno: `0009-0001-9737-7116`. Así el depósito queda ligado a tu identidad de investigador automáticamente |
| **El ZIP** | `paper/faraute/zenodo-deposito-fase1.zip`. Está listo y verificado (sin identificadores reales de la infraestructura) |
| **Una terminal abierta en el proyecto** | Vas a volver a ella a mitad del proceso, antes de publicar |
| **Nada más** | Ni tarjeta, ni institución que te avale, ni permiso de nadie |

**Cómo crear la cuenta:** entra en <https://zenodo.org>, botón naranja **Sign up** → **Sign up
with ORCID** → te lleva a orcid.org, inicias sesión → vuelves a Zenodo y confirmas tu correo.
Recomendación de Zenodo: ten activada la verificación en dos pasos en ORCID.

---

## 3. El paso a paso

### Paso 1 — Crear el borrador y subir el archivo
1. Entra en <https://zenodo.org> con tu cuenta.
2. Botón **New upload** (arriba a la derecha).
3. Arrastra `zenodo-deposito-fase1.zip` a la zona de subida. Espera a que termine.

> **No pulses «Publish» todavía.** Tienes que pasar antes por el paso 3.

### Paso 2 — Reservar el DOI
En el formulario, en el apartado **Digital Object Identifier**:

1. A la pregunta *«Do you already have a DOI for this upload?»* responde **No**.
2. Pulsa el botón **Get a DOI now!**
3. Zenodo te muestra un DOI del tipo `10.5281/zenodo.1234567`. **Cópialo.**

> ⚠️ **Si borras el borrador, pierdes el DOI reservado.** No borres ni empieces de cero
> después de este punto.

### Paso 3 — Rellenar la ficha
Copia y pega de la tabla del §4. Guarda con **Save draft** cuando termines.

### Paso 4 — Meter el DOI en el artículo (vuelve a la terminal)

```bash
cd /home/asolar/proyectos/pg-k8s-paper
python3 scripts/set_zenodo_doi.py 10.5281/zenodo.1234567
```

Con el número que te dio Zenodo. El guion, solo:

- sustituye el marcador en los **7 sitios** donde vive (manuscrito, versión extendida de
  18 pp, suplemento ×2, `CITATION.cff`, `.zenodo.json`, `README.md` del depósito y la carta
  al editor);
- recompila los **tres PDF** y sincroniza `main_final_12pp.pdf`;
- **rearma el ZIP** con el DOI ya dentro;
- verifica que no quede ningún marcador y te lo dice.

### Paso 5 — Reemplazar el ZIP en el borrador
Vuelve a Zenodo, al mismo borrador:

1. En la sección de archivos, **borra** el ZIP que subiste en el paso 1.
2. **Sube** el ZIP recién rearmado (misma ruta, ya actualizado).

Esto es lo que evita la pescadilla que se muerde la cola: que el paquete depositado cite un
DOI que aún no existía cuando lo empaquetaste.

### Paso 6 — Publicar
Repasa la ficha una última vez y pulsa **Publish**.

> ⚠️ **Publicar es un acto público y casi definitivo.** Después:
> - la **ficha** (título, autores, descripción) la puedes editar siempre;
> - los **archivos** solo se pueden tocar durante un plazo de gracia de 45 días, y pasado ese
>   plazo hay que escribir al soporte de Zenodo o publicar una **versión nueva**;
> - el registro **no se puede borrar**: los DOI son permanentes por diseño.
>
> Por eso el paso 5 va antes que el 6.

---

## 4. Ficha del depósito — para copiar y pegar

| Campo del formulario | Qué poner |
|---|---|
| **Resource type** | `Dataset` |
| **Title** | Datos y paquete de ejecución — Análisis multicapa de operadores de PostgreSQL y almacenamiento CSI en Kubernetes: estudio empírico de CloudNativePG bajo fallos inyectados (Fase 1 piloto) |
| **Creators** | Nombre: `Parejo R., Angel A.` · Afiliación: `Universidad de Carabobo, Valencia, Venezuela` · ORCID: `0009-0001-9737-7116` |
| **Description** | El texto completo está en `replication/.zenodo.json`, campo `description` (991 caracteres). Ábrelo y cópialo tal cual |
| **License** | `Creative Commons Attribution 4.0 International (CC-BY-4.0)` |
| **Version** | `1.0-fase1` |
| **Language** | `Spanish (spa)` |
| **Keywords** | Kubernetes · PostgreSQL · CloudNativePG · CSI · inyección de fallos · chaos engineering · failover · RTO · RPO · Chaos Mesh |
| **Access** | `Open` |
| **Additional notes** | Licencia dual: datos y documentación bajo CC-BY-4.0; código (scripts) bajo MIT (ver `LICENSE.md`) |
| **Related works** *(opcional)* | Puedes dejarlo vacío ahora y añadir el DOI del artículo cuando Faraute lo publique, con la relación *"is supplement to"* |

> **Ojo con `.zenodo.json`:** ese archivo es el formato que Zenodo lee automáticamente cuando
> el depósito viene **de una release de GitHub**. Si subes el ZIP a mano —que es lo que vas a
> hacer— Zenodo **no lo lee**: el formulario se rellena a mano. Por eso está esta tabla.

---

## 5. Una decisión: qué DOI citar en el artículo

Al publicar por primera vez, Zenodo registra **dos** DOI:

- el **DOI de versión**, que apunta a esta versión exacta y a estos archivos exactos;
- el **concept DOI**, que representa el depósito completo y siempre resuelve a la versión más
  reciente.

El DOI que reservas en el paso 2 es el **de versión**. El concept DOI aparece en la página del
registro solo **después** de publicar, en el recuadro *«Cite all versions»*.

**Mi recomendación: usa el DOI reservado (el de versión) en el artículo.** Razones:

1. Es el que ya tienes en la mano, y permite hacer todo en **una sola publicación**.
2. Para un paquete de reproducibilidad es la cita **más precisa**: apunta a los archivos
   exactos con los que se obtuvieron las cifras del artículo. Un árbitro que descargue ese
   DOI baja exactamente lo que auditó el paper, no una versión futura.
3. El concept DOI está pensado para artefactos que evolucionan (una biblioteca, un dataset
   vivo). Este depósito es una foto de la Fase 1.

Si prefirieras el concept DOI, el camino es más largo: publicar, leer el concept DOI de la
ficha, volver a ejecutar el guion con él, y subir una **versión 2** del depósito con el ZIP
corregido. Funciona, pero son dos publicaciones para el mismo contenido.

> Si eliges el DOI de versión, avísame: hay que ajustar una frase del `README.md` del depósito
> y del guion, que hoy dicen «concept DOI».

---

## 6. Después de publicar

- [ ] Copiar la URL del registro (`https://zenodo.org/records/…`) y guardarla.
- [ ] Comprobar que el PDF de 12 pp menciona el DOI correcto — el guion ya lo hizo, pero
      míralo con tus ojos en la sección de agradecimientos.
- [ ] Seguir con el envío: `PENDIENTE_MI_LADO.md` §3 y §4 (lectura final del PDF y correo a
      `faraute@uc.edu.ve` con la carta y las 3 figuras).

---

## Fuentes

- [Zenodo — Reservar un DOI](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/)
- [Zenodo — Crear una cuenta](https://help.zenodo.org/docs/get-started/create-an-account/)
- [Zenodo — Gestionar versiones](https://help.zenodo.org/docs/deposit/manage-versions/)
- [Zenodo — FAQ de versionado (dos DOI al publicar)](https://zenodo.org/help/versioning)
- [Zenodo — Editar registros publicados](https://support.zenodo.org/help/en-gb/1-upload-deposit/64-can-i-edit-records-after-they-have-been-published)
- [Zenodo — Cuota de almacenamiento](https://help.zenodo.org/docs/deposit/manage-quota/)
- [Zenodo — Políticas generales](https://about.zenodo.org/policies)
- [Zenodo — El archivo .zenodo.json (integración con GitHub)](https://help.zenodo.org/docs/github/describe-software/zenodo-json/)
