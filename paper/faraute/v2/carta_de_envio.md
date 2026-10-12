# Carta de envío — Revista FARAUTE de Ciencias y Tecnología

**A:** Comité Editorial, Revista FARAUTE de Ciencias y Tecnología (FACYT, Universidad de Carabobo)
**De:** Mirella Herrera C. y Angel Parejo R.
**Correspondencia:** Angel Parejo R. — angelparejo@gmail.com
**Fecha:** 11 de octubre de 2026
**Asunto:** Reenvío tras revisión mayor, en la plantilla v2

---

Estimado Comité Editorial:

Adjuntamos la versión revisada del manuscrito **«Caracterización empírica de la conmutación por error de CloudNativePG en Kubernetes: RTO, RPO y los límites de la inyección de fallos»**, junto con la respuesta punto por punto a los dos informes de arbitraje recibidos el 4 de octubre.

## Tipo de contribución

**Artículo científico.** Les agradeceríamos que confirmaran si esta clasificación es la correcta para el trabajo, dado que la carpeta de la plantilla no incluye el PDF de la guía nueva (`GUIA_PARA_LOS_AUTORES.tex` remite a `preliminares/guia.tex`, que no viene) y la guía anterior fijaba límites distintos por tipo. El manuscrito ocupa **11 páginas**, por debajo del límite de 20 que comprueba la clase, de modo que no requiere justificación de extensión.

## Originalidad

El trabajo es inédito, no ha sido publicado ni está sometido a consideración en otra revista. Presenta mediciones propias, obtenidas sobre un clúster Kubernetes en producción, y un paquete de replicación público que permite reproducir todas las cifras.

## Sobre esta revisión

Los dos informes coincidieron en una objeción de fondo que aceptamos sin reservas: el hallazgo central de la versión anterior era un artefacto del mecanismo de inyección. La revisión no se ha limitado a matizarlo.

- Se **retiran dos de las tres conclusiones empíricas** de la versión anterior.
- Se **retira la hipótesis** del predicado de visibilidad: al verificarla encontramos que la contradice la propia fuente que los árbitros nos pidieron incorporar.
- Se **corrige una afirmación que un árbitro había elogiado** como fortaleza —el tratamiento del *commit* fantasma por el verificador—, porque al revisar el código depositado comprobamos que ese mecanismo no está implementado.
- Se **declara que los registros crudos del verificador y los eventos del plano de control no se conservaron** y no pueden facilitarse. La versión anterior los prometía a petición; era incorrecto.

La contribución pasa a ser metodológica: de los cuatro escenarios diseñados, solo uno reprodujo el fallo que nominalmente modela. La respuesta punto por punto detalla cada observación.

## Formato

El manuscrito se ha rehecho sobre la plantilla `plantilla-autor-v2`. Se adjunta el PDF compilado con la opción `revision` (anónimo y con líneas numeradas) y la carpeta de fuentes.

Dos observaciones sobre la plantilla, por si resultan útiles:

1. **La clase no contempla un campo para el ORCID.** Uno de los árbitros pidió incluirlo para todos los autores. Indíquennos dónde desean que figure.
2. Para preservar el anonimato del arbitraje, la versión `revision` omite el DOI del depósito de datos y el nombre de la institución en la que se desarrollará la fase siguiente. **El depósito es público y su DOI es 10.5281/zenodo.23004248**; queda a su disposición y a la de los árbitros si lo consideran necesario para la evaluación, en cuyo caso revelaría la identidad de los autores.

## Declaración sobre el uso de inteligencia artificial

Conforme a la sección 7 de la guía, declaramos que durante la preparación de este trabajo se usó **Claude (Anthropic; modelos Claude Sonnet y Claude Opus) entre febrero y octubre de 2026**, con asistencia que excedió la corrección ortográfica y gramatical: redacción y edición del texto, escritura de los guiones de análisis en Python que calculan las cifras reportadas, verificación de las referencias contra sus fuentes primarias y obtención de los DOI, generación de las figuras a partir de los datos, y apoyo en la reinterpretación de los escenarios tras el arbitraje.

El diseño experimental, la ejecución de las inyecciones sobre el clúster, la obtención de las mediciones y las conclusiones son obra de los autores. Revisamos y editamos todo el contenido, comprobamos las cifras ejecutando los guiones depositados, verificamos una por una la existencia y exactitud de las referencias, y asumimos la responsabilidad íntegra por el artículo. La herramienta no figura como autora ni se cita como fuente.

Esta declaración figura también en el manuscrito, en la sección correspondiente.

## Material adjunto

| Archivo | Contenido |
|---|---|
| `articulo-arbitraje.pdf` | Manuscrito anónimo con líneas numeradas, 11 páginas |
| `carta_respuesta_arbitros.md` | Respuesta punto por punto a los dos informes |
| `fuentes/` | `articulo.tex`, `datos.tex`, `contenido.tex`, `referencias.bib` |
| `suplemento.pdf` | Material suplementario, 7 páginas |

Quedamos atentos a sus indicaciones.

Atentamente,

**Mirella Herrera C.** · **Angel Parejo R.**
Facultad Experimental de Ciencias y Tecnología, Universidad de Carabobo
