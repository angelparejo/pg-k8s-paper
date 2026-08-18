# ¿Es el artículo actual consecuente con el documento revisado por la tutora?

**Fecha:** 2026-08-17
**Encargo:** verificar si el último artículo conserva las ideas y los planteamientos del
documento revisado por la tutora, y si respeta el espíritu de sus recomendaciones.
**Insumos aportados:** `articulo_angelparejov2-experimental_entregable-bea.docx`,
`correcionesa.txt`
**Artículo actual evaluado:** `paper/faraute/main.tex` (12 pp, Revista FARAUTE)

---

## 0. Advertencia sobre los insumos — leer antes que nada

La pregunta tiene dos mitades y **solo una es contestable con lo que hay en estos archivos.**

### `correcionesa.txt` no contiene correcciones

El archivo tiene 56 líneas y ninguna se refiere al artículo. Son dos cosas pegadas por error:

1. **Líneas 1–41:** un correo de trabajo sobre el *Centro Alterno Maracaibo* —
   reconfiguración de nodos de extranet, clúster Docker Swarm, incidencias de DNS —
   firmado por **Anibal Parejo**. Nada que ver con el paper.
2. **Líneas 44–56:** un fragmento del **transcript de la terminal** de la sesión del
   16-ago de este mismo proyecto ("Checklists actualizados. Ahora completo el registro
   documental…", el volcado del `cat >> SESSION_REPORT.md` y un `API error · Retrying`).

Es un accidente de portapapeles. No hay recomendaciones de nadie ahí.

### El DOCX no es el documento que ella anotó, pero **sí lleva su mano encima**

El archivo **no tiene comentarios ni control de cambios** (`w:comment`, `w:ins`, `w:del`:
cero apariciones; `trackChanges` desactivado). Sus metadatos dicen
`lastModifiedBy: Angel Parejo`, revisión 13, modificado el **2026-07-09**. Es decir: es el
entregable que **tú** produjiste con tu propio guion `md2ieee_docx.py` y le entregaste a
ella ("entregable-bea").

Pero al compararlo carácter a carácter con tu versión versionada en git
(`articulo_angelparejov2-experimental_IEEE.docx`) aparecen **exactamente 8 diferencias**, y
todas tienen la forma de correcciones humanas escritas directamente sobre el texto, sin
control de cambios. Esas 8 ediciones son, con toda probabilidad, **lo único que hay de tu
tutora en este material** (§2).

### Consecuencia para el encargo

| Pregunta | ¿Contestable? |
|---|---|
| ¿El artículo actual conserva las ideas y planteamientos del documento revisado? | **Sí** — el DOCX sirve de línea base y la comparación es completa (§3–§5) |
| ¿Sobreviven las correcciones concretas que ella marcó en el texto? | **Sí** — las 8 son rastreables (§2) |
| ¿Respeta el *espíritu de sus recomendaciones*? | **No, con este material.** Recomendaciones de fondo (qué reforzar, qué recortar, qué reencuadrar) no existen en ninguno de los dos archivos |

Para la tercera mitad necesito su insumo real: el DOCX con comentarios o control de cambios
activado, su correo, o una foto de las anotaciones en papel. Ver §7.

---

## 1. Qué se comparó

| | Documento revisado (9-jul) | Artículo actual (17-ago) |
|---|---|---|
| Archivo | `..._entregable-bea.docx` | `paper/faraute/main.tex` |
| Destino | plantilla IEEE (2 col) | Revista FARAUTE, UC/FACYT |
| Cuerpo | **~8.581 palabras** | **~4.270 palabras** (−50 %) |
| Secciones | 8 | **las mismas 8, mismo orden** |
| Resumen | 182 palabras, solo español | 146 español + 144 inglés |
| Palabras clave | 11 | 5 (límite de la revista) |
| Figuras | 1 (modelo $S=(O,K,M,D)$) | 3 (banco de pruebas, timeline, predicado) |
| Tablas | 2 | 2 (las mismas) |
| Referencias | 27, IEEE numerado | 27, autor-año alfabético |
| Citas | `[1]`…`[27]` | `(Autor, año)` |

---

## 2. Las 8 ediciones de tu tutora y qué fue de ellas

| # | Su edición sobre tu texto | Tipo | ¿Sobrevive en el artículo actual? |
|---|---|---|---|
| 1 | "los estudios analiza por separado" → **"analizan"** | corrige concordancia | **Sí** (§2 reescrita, la concordancia es correcta) |
| 2 | "cómo decisiones en una capa" → **"cómo las decisiones"** | estilo | **Sí**, literal (línea 149) |
| 3 | "que surge de este análisis" → **"que surgen"** | corrige concordancia | **Sí**, literal (línea 195) |
| 4 | "La no-promoción" → **"La no promoción"** | quita guion | **Sí**, literal (línea 304) |
| 5 | "queda como línea de trabajo futuro" → **"como una línea"** | estilo | Frase reescrita al recortar; el matiz se pierde sin consecuencia |
| 6 | "Palabras Clave—" → "Palabras **c lave**—" | *introduce* un error (espacio suelto) | No se arrastró: el artículo pone "Palabras clave:" correcto |
| 7 | "La Fig. 1 ilustra" → "La Fig. 1 **. Ilustra**" | *introduce* un error (punto y mayúscula) | No se arrastró: esa figura se eliminó (§5.9) |
| 8 | "Resumen — La" → "Resumen —La" | espaciado | N/A: la plantilla Faraute maqueta el resumen de otro modo |

**Balance: 4/4 de sus correcciones reales sobreviven; los 2 errores que ella introdujo sin
querer, no.** En el plano de la corrección de texto, el artículo actual es fiel a su
revisión y además la mejora.

Conviene que sepas algo: **eran 8 ediciones de palabra en un documento de 8.581 palabras, y
ninguna toca el contenido.** Si esperabas de ella una revisión de fondo, este archivo no la
trae — lo que no significa que no te la haya dado por otra vía.

---

## 3. Fidelidad conceptual: lo que se conserva íntegro

Revisado uno por uno. **Todo el andamiaje intelectual que ella leyó está en el artículo
actual**, con la misma formulación:

1. **Tesis central.** "La confiabilidad de las cargas con estado en Kubernetes es un
   problema inherentemente multicapa" — misma tesis, casi la misma redacción.
2. **Las contribuciones.** Las 5 viñetas pasan a 4: taxonomía / marco descriptivo /
   hallazgo empírico / predicado $V(\text{fallo},K)$. La quinta (invariantes) se fusionó en
   la del marco, pero **los invariantes conservan su propia subsección 3.4 íntegra**. No hay
   pérdida de contenido, solo de una viñeta.
3. **El modelo $S=(O,K,M,D)$**, con la justificación de notación (se usa $M$ y no $C$ para
   no colisionar con $C(S)$) — presente, textual.
4. **Las 4 dimensiones** $R(S)$, $C(S)$, $P(S)$, $I(S)$ con sus mismas fórmulas, y la
   salvedad clave: *"las funciones $f(\cdot)$ son organizativas: no relaciones cerradas ni
   derivadas analíticamente"*. Presente.
5. **Los 3 invariantes**, incluida la sutileza de que la disponibilidad se enuncia como
   **métrica** y no como invariante duro por falta de un SLO declarado a priori. Presente.
6. **Tabla I** (responsabilidad por capa y tipo de fallo) — idéntica, con su nota de que es
   *síntesis analítica del comportamiento documentado, no una medición*.
7. **La restricción de alcance a un solo operador** y su motivo (el clúster productivo no
   permitía instalar Zalando ni Crunchy) — presente, con el mismo razonamiento.
8. **Toda la metodología**: entorno (K8s 1.34.6, PG 16.13, CNPG 1.28.0, CSI Huawei 4.10.1,
   Calico 3.31.4, Chaos Mesh 2.8.3), los tres controles de aislamiento, el `tx-verifier`, la
   granularidad de 0,2 s, $n=10$, la exclusión de la primera inyección de F2.
9. **Todas las cifras.** Comprobadas una a una: 7,91 · 36,75 · 4,65× · 613 253 · $U=0$ ·
   $p\approx1{,}1\times10^{-5}$ · Hodges–Lehmann 28,96 · Clopper–Pearson 25,9 %/22,1 % ·
   cobertura 97,9 % · Spearman 0,62 frente a crítico 0,65 · IQR y rangos de F1 y F2 ·
   80,5 s · 60,75 s. **Ninguna cifra cambió, ninguna se perdió.**
10. **El hallazgo central** (la visibilidad ante Kubernetes gobierna el failover), el
    encuadre de F2 como **refutación** y no confirmación, y $V(\text{fallo},K)$ como
    *extensión propuesta, no derivada formalmente*. Presente.
11. **Las limitaciones**: failover intra-nodo, F2 como cota inferior del RTO ante fallo de
    nodo, RPO nulo acotado por la co-localización, F4 como lección de instrumentación y no
    como propiedad general de Chaos Mesh. Todas presentes.
12. **El "no se reclama una validación del marco"** — presente, textual.

**Veredicto de esta sección: el artículo actual no traiciona ninguna idea del documento que
ella revisó.** El esqueleto argumental es el mismo, en el mismo orden, con las mismas
salvedades y las mismas cifras.

---

## 4. Recortes: dónde se perdió desarrollo (no ideas)

El cuerpo pasó de ~8.581 a ~4.270 palabras para caber en las 12 páginas de Faraute. Lo que
desapareció es **argumentación**, no tesis:

| Pasaje de la versión revisada | Qué pasó |
|---|---|
| Introducción, 6 párrafos desarrollando el acoplamiento multicapa | Comprimidos en 1 párrafo. Se pierde el *movimiento retórico* de instalar la brecha ("una dependencia multicapa aún no suficientemente explorada") como paso propio |
| Trabajos relacionados, 7 párrafos | 2 párrafos densos. Se conservan las 4 líneas de literatura y todos los contrastes (Mega, Drees/LitmusChaos, Chen et al., comparativas de industria) |
| "La limitación transversal es que la mayoría de los estudios analizan por separado…" | Absorbido en la última frase de §2. La idea sobrevive; el énfasis, no |
| §4: el ejemplo del "operador que asume tiempos de persistencia bajos" sobre almacenamiento distribuido | **Eliminado por completo.** Era el único ejemplo concreto que aterrizaba la interacción operador–almacenamiento |
| §4: el párrafo interpretativo de $I(S)$ y el de "Implicaciones para la evaluación" | Reducidos a una frase cada uno |
| Estadística fina: $z=-3{,}78$, los IC por escenario, sensibilidad de exclusiones, prueba de permutación | **Movidos al material suplementario** de Zenodo, con remisión explícita |
| Fig. 1 (diagrama del modelo $S=(O,K,M,D)$) | **Eliminada** (ver §5.9) |

Los recortes están bien hechos: se cortó desarrollo y se preservó estructura, cifras y
salvedades. Pero si ella valoraba la densidad argumental de la introducción y de §4, notará
que el artículo ahora **afirma** donde antes **razonaba**.

---

## 5. Los cambios de encuadre: lo que ella **no** ha visto

Esto es lo importante del informe. Nueve cambios que no son recortes sino **decisiones
sustantivas tomadas después de su revisión**, todas por el arbitraje simulado interno. Son
las que debes ponerle delante antes de enviar.

**5.1. El modelo $S=(O,K,M,D)$ fue degradado a "andamiaje".**
La versión que ella revisó lo presenta como la contribución conceptual (viñeta 2 de 5). El
artículo actual añade en las conclusiones: *"La contribución conceptual de mayor alcance es,
de hecho, ese predicado de visibilidad; la tupla $S=(O,K,M,D)$ actúa como andamiaje
descriptivo que organiza el análisis, no como un modelo predictivo."* El centro de gravedad
del artículo se desplazó del modelo al predicado $V(\text{fallo},K)$. Si ella tiene apego al
modelo — y por su lugar en las contribuciones, parece que sí — **este es el cambio que más
probablemente querrá discutir.**

**5.2. Se eliminó la figura del modelo.**
La única figura de la versión revisada era el diagrama de las capas de $S=(O,K,M,D)$. Ya no
está: las tres figuras actuales son banco de pruebas, *timeline* F1/F2 y predicado de
visibilidad. Combinado con 5.1, la mitad conceptual del artículo perdió a la vez su
ilustración y su primer puesto. Todo lo visual apunta ahora a lo empírico.

**5.3. "Trabajo futuro" se convirtió en "Fase 2 ya diseñada".**
Ella leyó: el contraste entre operadores *"se declara como trabajo futuro"*. El artículo
dice ahora: *"se asigna a la Fase 2 —ya diseñada, con protocolo de ejecución e
instrumentación desarrollados— mediante un diseño factorial 2×2 (replicación asíncrona
frente a síncrona por quórum × topología co-localizada frente a anti-afinidad
multi-nodo)"*. Es un **compromiso público** mucho más fuerte que una declaración de trabajo
futuro. Ojo con esto: el propio artículo explica que el clúster productivo no permite
instalar otros operadores, así que la Fase 2 depende de conseguir un entorno que hoy no
tienes. Prometerla con ese nivel de detalle es una deuda que un árbitro puede reclamarte.

**5.4. Todo el artículo se reencuadra como "Fase 1 piloto".**
La palabra "piloto" no aparecía en la versión revisada. Ahora estructura el discurso. Es más
honesto y rebaja la exposición, pero cambia el estatus de lo que se ofrece: de *un estudio
empírico* a *la primera fase de un programa*.

**5.5. La novedad de F2 se rebajó explícitamente.**
Ella leyó que la no-promoción en F2 iba *"en contra de lo que anticipaba el comportamiento
documentado"* y que esa refutación era *"el resultado de mayor fuerza probatoria"*. El
artículo actual mantiene eso pero añade: *"Un lector familiarizado con `pod-failure` podría
anticiparlo; el aporte no es la sorpresa, sino la confirmación empírica y el aislamiento del
mecanismo."* Es más defendible ante un árbitro, y es una concesión que **debilita el gancho
del artículo**. Decisión buena, pero es suya que la avale.

**5.6. El $p$-valor se reencuadró como saturado.**
Antes se reportaba $p\approx1{,}1\times10^{-5}$ como evidencia. Ahora se advierte que es *"el
mínimo alcanzable con $n=10$ —test saturado—, por lo que el peso probatorio recae en el
tamaño de efecto y el mecanismo, no en el $p$"*. Metodológicamente correcto; cambia cómo se
vende el resultado.

**5.7. Nueva salvedad en el propio resumen.**
Se añadió al final: *"Por la co-localización intra-nodo, se sostienen el contraste F1/F2 y el
mecanismo, no las magnitudes absolutas."* No estaba en el resumen que ella aprobó. Poner una
limitación en el resumen es una decisión editorial de peso: es lo primero que lee un árbitro.

**5.8. Disponibilidad de datos: de "a petición" a depósito público.**
La versión revisada dice que los datos *"se facilitan a petición"* porque el entorno es
restringido. El artículo actual anuncia un **depósito público en Zenodo con DOI**. Es un
cambio de política de datos sobre un experimento ejecutado en infraestructura productiva de
un tercero. (Hoy mismo se seudonimizaron los identificadores del clúster en ese paquete
antes de publicarlo; antes de esa corrección el depósito habría expuesto nombres de nodos y
el inventario de clústeres ajenos.) Si hay alguna autorización institucional detrás, este es
el punto donde debe constar.

**5.9. Se añadió el posicionamiento frente a Jepsen/Elle.**
Nueva referencia (Kingsbury & Alvaro, 2021) y una concesión explícita: el `tx-verifier`
*"comparte ese espíritu con un alcance más acotado"*. Refuerza el rigor y reconoce una
limitación que la versión revisada no admitía. Añadida también la doc de PostgreSQL 16. El
resto del corpus (27 referencias) es el mismo.

**5.10. Cambió la revista de destino.**
Ella revisó un artículo maquetado en plantilla IEEE con citas numeradas — el camino era
CACIC / venue tipo IEEE. El artículo actual está maquetado para **Revista FARAUTE (UC/FACYT)**
con citas autor-año. Si en algún momento acordaron un destino, esto es un cambio de plan que
le corresponde conocer, sobre todo porque hoy existen **tres versiones paralelas del mismo
trabajo** (IEEE/v2, LNCS 10 pp para CACIC, Faraute 12 pp) y solo una puede enviarse.

---

## 6. Veredicto

**En cuanto a ideas y planteamientos: sí, es plenamente consecuente.** Las 8 secciones, la
tesis multicapa, el modelo, las cuatro dimensiones, los tres invariantes, la Tabla I, toda
la metodología, todas las cifras y todas las salvedades del documento que ella revisó están
en el artículo actual. Sus 4 correcciones reales de texto sobrevivieron; sus 2 erratas
involuntarias, no. No hay ninguna idea abandonada ni ninguna cifra alterada.

**En cuanto al espíritu de sus recomendaciones: no puedo pronunciarme,** porque en los dos
archivos que me diste no hay recomendaciones de fondo — solo 8 ediciones de palabra.

**Y hay una advertencia que no depende de ella:** el artículo se movió en cuatro ejes que su
revisión no cubre — el modelo pasó a segundo plano frente al predicado de visibilidad (5.1,
5.2), la novedad del hallazgo se rebajó (5.5, 5.6), el trabajo futuro se convirtió en una
Fase 2 comprometida (5.3) y los datos pasaron a depósito público (5.8) — más el cambio de
revista (5.10). Son cinco decisiones defendibles, tomadas por criterio de arbitraje, pero
**son suyas de avalar, no mías de asumir.** Llévale esa lista.

---

## 7. Qué necesito para cerrar el análisis

Cualquiera de estas sirve:

1. El DOCX **con** sus comentarios (`Revisar → Nuevo comentario`) o con **control de cambios
   activado**, si lo tiene guardado así en otra copia.
2. Su **correo o mensaje** con las observaciones.
3. Una **foto o escaneo** de las anotaciones en papel.
4. Si fue una reunión: tus **notas** de lo que pidió, aunque sean telegráficas.

Con eso puedo contrastar recomendación por recomendación y decirte cuáles quedaron
atendidas, cuáles se atendieron a medias y cuáles el recorte a 12 páginas se llevó por
delante.
