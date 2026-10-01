# Carta al editor — Revista FARAUTE de Ciencias y Tecnología (UC/FACYT)

> Borrador listo para pegar como cuerpo del correo a **faraute@uc.edu.ve**.
> Antes de enviar: (1) sustituir el DOI de Zenodo — se hace solo al ejecutar
> `python3 scripts/set_zenodo_doi.py <DOI>`; (2) revisar el saludo si se conoce
> el nombre del editor en ejercicio; (3) confirmar la fecha.

---

**Asunto:** Postulación de artículo científico — Análisis multicapa de operadores de PostgreSQL y almacenamiento CSI en Kubernetes

---

Valencia, 27 de septiembre de 2026

Señores
**Comité Editorial**
Revista FARAUTE de Ciencias y Tecnología
Facultad Experimental de Ciencias y Tecnología
Universidad de Carabobo

Estimados señores:

Tenemos el agrado de someter a su consideración, para su evaluación y eventual publicación
en la Revista FARAUTE de Ciencias y Tecnología, el manuscrito titulado **«Análisis multicapa
de operadores de PostgreSQL y almacenamiento CSI en Kubernetes: un marco de análisis y un
estudio empírico de CloudNativePG bajo fallos inyectados»**, en la modalidad de **artículo
científico**.

El trabajo aborda un problema poco tratado de forma conjunta en la literatura: la
orquestación de contenedores, los operadores de bases de datos y el almacenamiento por
*Container Storage Interface* (CSI) suelen estudiarse por separado, pese a que la
recuperación ante fallos depende de su interacción. El artículo aporta dos elementos. En lo
conceptual, un marco descriptivo —taxonomía, vocabulario común y el modelo $S=(O,K,M,D)$ con
invariantes de consistencia, disponibilidad y durabilidad— que permite razonar sobre la
responsabilidad de cada capa ante un fallo. En lo empírico, un estudio de inyección de
fallos sobre CloudNativePG en un clúster Kubernetes en producción, bajo tres escenarios:
eliminación del pod primario, indisponibilidad sostenida y partición de red.

El hallazgo central es que la variable que gobierna la conmutación por error no es el fallo
en sí, sino su **visibilidad ante Kubernetes**: la eliminación del primario promueve una
réplica con un RTO mediano de 7,91 s, mientras que un fallo sostenido —igualmente
incapacitante desde la perspectiva del cliente— no promueve réplica alguna y eleva el
tiempo de recuperación a 36,75 s; la partición de red, por su parte, preserva la
consistencia. En ninguno de los escenarios se perdió una transacción confirmada (RPO nulo).
Este resultado tiene una consecuencia práctica directa para quien opera bases de datos sobre
Kubernetes, y se enuncia en el artículo con la salvedad que corresponde: por la
colocalización intranodo del banco de pruebas, se sostienen el contraste entre escenarios
y el mecanismo que lo explica, no las magnitudes absolutas.

En atención a la política de reproducibilidad, los datos limpios de RTO y RPO, el paquete de
ejecución (manifiestos de Kubernetes y de Chaos Mesh, el cliente verificador de
transacciones, la carga de trabajo y los guiones de análisis) y un material suplementario de
métodos y estadística extendidos se depositan públicamente en Zenodo
(**DOI: 10.5281/zenodo.23004248**). Todas las cifras del artículo se reproducen ejecutando el guion de
análisis incluido en ese depósito. Los registros crudos del verificador se facilitan a
petición, ya que el experimento se ejecutó sobre un clúster productivo bajo acceso
restringido.

Los autores declaramos que el manuscrito es original e inédito, que no ha sido publicado ni se
encuentra en proceso de evaluación simultánea en otra revista, y que su contenido es de nuestra
entera responsabilidad. La investigación no recibió financiamiento externo y no
existen conflictos de interés. Conforme a las buenas prácticas vigentes, dejamos constancia en
el propio manuscrito de que se emplearon herramientas de inteligencia artificial generativa
únicamente como apoyo de redacción y estilo; la concepción, la ejecución experimental, el
análisis y las conclusiones son obra de los autores, quienes revisaron y validaron la
totalidad del contenido.

El manuscrito se ajusta a las normas de la revista: doce páginas, doble columna, Times New
Roman 12, papel carta con márgenes de 2,5 cm, resumen de 149 palabras con su versión en inglés de 140, referencias en formato autor-año ordenadas alfabéticamente y figuras en escala de
grises a 300 dpi, que se adjuntan además como archivos independientes.

Quedamos a su disposición para cualquier aclaratoria o para atender las observaciones que el
arbitraje estime pertinentes, y agradezco de antemano la atención prestada.

Atentamente,

**Parejo, A.** — autor de correspondencia, en nombre de los autores
Herrera, M. · Parejo, A.
Universidad de Carabobo — Valencia, estado Carabobo, Venezuela
Correo: angelparejo@gmail.com
ORCID: 0009-0001-9737-7116

---

**Adjuntos:**

1. `articulo_angel_parejo_final.pdf` — manuscrito completo (12 páginas).
2. `Fig1.jpg` — banco de pruebas (escala de grises, 300 dpi).
3. `Fig2.jpg` — línea de tiempo de los escenarios F1 y F2 (escala de grises, 300 dpi).
4. `Fig3.jpg` — predicado de visibilidad (escala de grises, 300 dpi).
5. `entrega-latex.zip` — fuente LaTeX del manuscrito y sus figuras, que remito por
   adelantado para agilizar el arte final en caso de aceptación. Se compila con XeLaTeX;
   las instrucciones van en el `LEEME.txt` incluido.

---

> **Nota interna (no forma parte del correo).** La guía de la revista pide PDF o MS Word
> para el arbitraje inicial y reserva LaTeX para el arte final de los artículos aceptados,
> con su propia hoja de estilo (`CyT_UC.sty` + `CyT_UC.tex`, en
> facyt.uc.edu.ve/investigacion/faraute). El punto 5 se presenta por eso como adelanto
> voluntario. Si el artículo se acepta, habrá que migrar `main.tex` a esa plantilla.
