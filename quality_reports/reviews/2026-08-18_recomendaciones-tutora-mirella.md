# Recomendaciones de la Prof. Mirella — análisis y estado frente al artículo actual

**Fecha:** 2026-08-18
**Fuente:** `correcionesa.txt` (correo de la Prof. Mirella, recibido 2026-08-18)
**Artículo evaluado:** `paper/faraute/main.tex` (12 pp, Revista FARAUTE)
**Antecedente:** `quality_reports/reviews/2026-08-17_consecuencia-con-documento-revisado-tutora.md`
(contraste de fidelidad con el documento que ella revisó)

---

## 1. Qué contiene realmente el correo

Conviene separar las voces, porque no todas pesan igual y ella misma las distingue.

**De la Prof. Mirella, en primera persona:**
- Valoración general: *"me gustó mucho la adaptación que realizaste y me parece que tiene un
  muy buen nivel"*. Cierra con *"EXCELENTE TRABAJO!!! Cada vez más cerca de la meta"*.
- **Estrategia:** propone presentarlo como **trabajo en progreso**, lo que —dice— *"cabe
  perfectamente como TG de la Especialización"*.
- **Venue:** *"Busquemos cuál es el congreso al cual se pudiera enviar"*, a conversar en una
  llamada de WhatsApp.
- **Una corrección técnica propia**, al final y separada del resto: *"por favor revisa el
  tiempo verbal de la redacción, el cual debería estar en pasado pues el trabajo ya fue
  realizado"*.
- **Queda pendiente la revisión de la Prof. Francisca** (*"esperemos la revisión de la profe
  Francisca"*). Es decir: **va a llegar más retroalimentación.**

**Reenviado por ella, no escrito por ella:** el bloque titulado *"Análisis de la IA"*
(líneas 6–41). Ella lo presenta explícitamente como *"las observaciones que generó la IA"*.
Son tres secciones: viabilidad como WIP en congreso, idoneidad como TG, y **tres sugerencias
concretas de redacción** (título, resumen, limitaciones). Al reenviarlas las hace suyas como
orientación, pero no son un dictamen de lectura del manuscrito: el análisis no cita ni una
cifra, ni una sección concreta, ni discute el método.

**Un dato que hay que tener presente:** ese análisis se generó sobre **la versión que ella
revisó** (el DOCX del 9-jul, formato IEEE), no sobre el artículo de 12 páginas para Faraute.
Eso explica que una de sus tres sugerencias ya esté aplicada (§3, R5).

---

## 2. El asunto que hay que resolver antes que ninguna otra cosa

**La profesora propone un congreso en modalidad *Work in Progress*. El paquete que está
listo apunta a una revista.**

Todo lo que se cerró estos días —el recorte a 12 páginas con las normas de Faraute, la carta
al comité editorial, las figuras en escala de grises a 300 dpi, el depósito Zenodo, la
checklist de envío a `faraute@uc.edu.ve`— está construido para la **Revista FARAUTE de
Ciencias y Tecnología**, que es una revista arbitrada. **"Work in Progress" no es una
modalidad de revista: es una categoría de congreso.** Son dos destinos distintos y el mismo
trabajo no puede ir a los dos.

Conviene deshacer una confusión que el correo mezcla, porque no todo colisiona:

| Uso | ¿Choca con enviar a Faraute? |
|---|---|
| Presentarlo como **TG de la Especialización** | **No.** Un TG y un artículo en revista conviven sin problema; es lo normal |
| Enviarlo a un **congreso en modalidad WIP** | **Sí.** Sería el mismo trabajo en dos sitios a la vez |

O sea: la parte del TG se puede hacer pase lo que pase. Lo que exige decidir es **revista o
congreso**, y esa decisión es justo el tema de la llamada que ella propone.

Contexto para esa conversación, con lo verificado en `convocatorias_y_venues.md`:

- **CACIC 2026** (el congreso para el que ya existe un recorte a 10 pp en `paper/cacic/`)
  cerró el **29-jul-2026**. La ventana pasó.
- **CLEI** es el candidato natural que menciona el propio análisis: formato IEEE —que ya
  tienes—, admite español, indexado en Scopus vía IEEE Xplore. **CLEI 2026 cerró abstracts
  el 19-abr**; CLEI 2027 no tenía CFP publicado a julio. Habría que monitorearlo.
- **CONCAPAN 2026** cerró el 15-jul y además exige 6 páginas y publicación en inglés.
- **JISBD** (que menciona el análisis) es español, de ingeniería del software; habría que
  verificar convocatoria y encaje temático — no está estudiado en el repositorio.

**Consecuencia práctica: si se va a congreso, el envío a Faraute se detiene.** Y al revés.
No conviene mandar la carta al editor hasta que esto se decida con ella y con la Prof.
Francisca.

---

## 3. Estado de cada recomendación frente al artículo actual

| # | Recomendación | Origen | Estado |
|---|---|---|---|
| R1 | Presentarlo como trabajo en progreso / TG | Mirella | **Decisión pendiente** — ver §2 |
| R2 | Buscar congreso | Mirella | **Pendiente** — insumos en §2 |
| R3 | Marcar el título como WIP ("Hacia un…", "Resultados preliminares…") | IA | **No aplicado** |
| R4 | Que el resumen diga explícitamente que es un trabajo en curso | IA | **No aplicado** |
| R5 | Presentar las limitaciones como *características de la Fase 1 (Piloto)*, no como defectos | IA | **Ya aplicado en lo esencial** |
| R6 | Redacción en pasado | Mirella | **Parcial** — ver §4 |

### R3 — Título

Actual: *"Análisis multicapa de operadores de PostgreSQL y almacenamiento CSI en Kubernetes:
un marco de análisis y un estudio empírico de CloudNativePG bajo fallos inyectados."* No
lleva ninguna marca de trabajo en progreso.

Aplicarlo es trivial, pero **solo tiene sentido si se va a congreso**: en una revista
arbitrada, titular "(Work in Progress)" o "Hacia un…" **rebaja** el trabajo sin necesidad, y
Faraute no tiene esa modalidad. Queda supeditado a §2.

### R4 — Resumen

El resumen actual (146 palabras) abre con *"Este artículo presenta un marco descriptivo…"* y
**sí** lleva ya una salvedad de alcance al final: *"Por la co-localización intra-nodo, se
sostienen el contraste F1/F2 y el mecanismo, no las magnitudes absolutas."* Lo que no dice es
la fórmula *"este trabajo en progreso…"*. Mismo condicionante que R3: depende del destino.

### R5 — Limitaciones como características de la Fase 1 — **ya está hecho**

Esto es lo más interesante del contraste. La sugerencia describe exactamente el cambio que el
artículo **ya incorporó** después de que ella lo revisara:

- Introducción: *"El estudio empírico es una fase piloto (Fase 1) cuyo alcance está
  delimitado por las restricciones del clúster productivo."*
- Discusión: *"El alcance es una fase piloto acotada por el entorno productivo."*
- Y la Fase 2 ya no es un "trabajo futuro" difuso: *"La Fase 2 —ya diseñada, con protocolo de
  ejecución e instrumentación desarrollados— ampliará la validación mediante un diseño
  factorial 2×2 (replicación asíncrona frente a síncrona por quórum × topología co-localizada
  frente a anti-afinidad multi-nodo)."*

La versión que ella leyó no decía "piloto" ni una sola vez. O sea: **la revisión interna y la
recomendación de la IA convergieron sin saberlo.** Vale la pena decírselo en la llamada,
porque es una de las cinco cosas que ella todavía no ha visto.

Queda un matiz menor: la Discusión sigue encabezando el pasaje con *"Tres limitaciones, ya
detalladas: (i)… (ii)… (iii)…"*. Si se quiere apurar la sugerencia, bastaría reformular ese
encabezado como *"tres características del diseño de la Fase 1"*. **Recomiendo no ir más
lejos:** eliminar la palabra "limitaciones" del artículo sería contraproducente. El
arbitraje simulado premió justamente esa transparencia, y el propio análisis de la IA la cita
como la **primera** razón por la que el artículo sería aceptado (*"Honestidad y
Transparencia… Los revisores de congresos valoran mucho esta transparencia"*). Las dos ideas
son compatibles: encuadrar como Fase 1 **y** declarar limitaciones. Lo que no se debe hacer
es esconderlas.

---

## 4. R6 — El tiempo verbal: qué corregir y qué defender

Es la corrección propia de la profesora y la más concreta. Tiene razón en parte, y conviene
ser preciso, porque aplicar "todo en pasado" a rajatabla empeoraría el artículo.

### 4.1 Lo que ya está bien (en pasado)

La metodología y los resultados están mayoritariamente en pasado: *"se ejecutó un
experimento"*, *"se aplicaron tres escenarios"*, *"se planificó un cuarto escenario"*, *"el
operador desplegó"*, *"la replicación se mantuvo"*, *"CNPG ejecutó failover"*, *"no promovió
en ninguna"*, *"recreó el pod"*, *"resultó no ejecutable"*, *"el inyector FUSE falló"*. Las
conclusiones también: *"Este trabajo abordó…"*, *"se presentó…"*.

### 4.2 Defectos reales — mezcla de tiempos dentro de una misma frase

Son los que un lector atento detecta enseguida. Hay que corregirlos:

| Ubicación | Texto actual | Propuesta |
|---|---|---|
| §5.1 (l. 237) | *"El clúster **es** productivo y su equipo de operación no **permitía** instalar operadores nuevos"* | *"El clúster **era** productivo y su equipo de operación no permitía…"* |
| §5.1 (l. 241) | *"El manifiesto del clúster experimental **solicita** anti-afinidad… pero el pool de nodos elegibles **se reducía** a nodo-lab-01"* | *"El manifiesto **solicitaba** anti-afinidad… pero el pool **se reducía**…"* |

### 4.3 Presente que describe trabajo ya ejecutado — conviene pasarlo

| Ubicación | Texto actual | Propuesta |
|---|---|---|
| §5.1 | *"El alcance a un único operador **responde** a una restricción del entorno"* | *"respondió"* |
| §5.3 | *"por la no-normalidad esperada **se reportan** medianas y rangos intercuartílicos"* | *"se reportaron"* |
| §6 | *"Las mediciones sobre CNPG **son** descriptivas"* | *"fueron"* |
| §6 | *"por la no-normalidad de RTO y RPO **se reportan** medianas e IQR"* | *"se reportaron"* |
| §6.1 | *"solo F1 **pone** a prueba la durabilidad de forma no trivial"* | *"solo F1 puso a prueba"* |
| §6.1 | *"Dentro del lote de F2 **se observa** una asociación orden–RTO débil"* | *"se observó"* |
| §6.3 | *"F1 **confirma** esta expectativa casi trivial"* | *"F1 confirmó"* |

### 4.4 Presente que **no** se debe tocar

Aquí hay que sostener el criterio ante ella, con argumento:

- **Referencias a tablas y figuras:** *"La Tabla 2 **resume** los tres escenarios"*, *"La
  Tabla 1 **sintetiza**…"*. Convención universal: lo que el documento muestra se enuncia en
  presente, porque sigue mostrándolo cada vez que se lee.
- **El modelo y el marco:** *"el sistema **se modela** como una tupla"*, *"**se definen**
  cuatro dimensiones"*, *"las funciones f(·) **son** organizativas"*. Un marco conceptual no
  caduca: se enuncia en presente. Ponerlo en pasado insinuaría que dejó de valer.
- **Los invariantes:** *"toda transacción confirmada **debe permanecer** accesible"*, *"el RTO
  **se reporta** como cantidad observable"*. Son definiciones y reglas, no acciones ejecutadas.
- **Afirmaciones generales del dominio:** *"la confiabilidad **es** inherentemente
  multicapa"*, *"Estas diferencias **influyen** en cómo se detectan fallos"*.
- **Presentación del artículo:** *"Este artículo **presenta**…"*, *"el trabajo **presenta**:"*.
  Es la fórmula estándar de resumen e introducción en cualquier revista o congreso.

**Resumen del criterio:** pasado para lo que se hizo (montaje, ejecución, observación,
medición); presente para lo que el artículo afirma, define o muestra. El artículo ya sigue
esa regla en la mayor parte; lo que falta son las nueve frases de §4.2 y §4.3.

---

## 5. Qué propongo

**Acción inmediata y segura (no depende del destino):** aplicar el paso de tiempo verbal de
§4.2 y §4.3 — nueve frases. Verificando después que el PDF siga en 12 páginas, porque las
formas en pasado son ligeramente más largas y el límite de Faraute es duro.

**Acción condicionada a la decisión de §2** (título WIP, resumen WIP, encabezado de
limitaciones): no tocar hasta que se decida revista o congreso. Aplicarlas ahora estropearía
el envío a Faraute, y son cinco minutos de trabajo cuando haya decisión.

**Para la llamada con ella** conviene llevar tres cosas:
1. Que el envío a Faraute está **listo para salir** y que su propuesta de congreso lo detiene
   — hay que elegir.
2. Que R5 **ya está aplicado**, junto con las otras cuatro decisiones posteriores a su
   revisión que ella no ha visto (el modelo cediendo el primer plano al predicado
   $V(fallo,K)$ y la pérdida de su figura, la Fase 2 comprometida, la novedad de F2 rebajada,
   y el depósito público de datos). Están detalladas en el informe del 17-ago.
3. El estado real de los congresos: CACIC cerrado, CLEI como candidato pero sin CFP
   publicado, CONCAPAN descartado por extensión e idioma.

**Y queda un insumo por llegar:** la revisión de la Prof. Francisca. Conviene esperarla antes
de tocar el manuscrito más allá del tiempo verbal, para no hacer dos rondas de cambios.
