# Carta de respuesta punto por punto — Revista FARAUTE de Ciencias y Tecnología

**Manuscrito (versión original):** «Análisis multicapa de operadores de PostgreSQL y almacenamiento CSI en Kubernetes: un marco de análisis y un estudio empírico de CloudNativePG bajo fallos inyectados»

**Título revisado:** «Caracterización empírica de la conmutación por error de CloudNativePG en Kubernetes: RTO, RPO y los límites de la inyección de fallos»

**Autores:** Herrera, M.; Parejo, A. (autor de correspondencia)
**Fecha:** 7 de octubre de 2026

---

Estimados árbitros:

Agradecemos la exhaustividad de ambos informes. Nos han llevado a una conclusión incómoda y, creemos, valiosa: **de los cuatro escenarios de fallo diseñados, solo uno reprodujo el fallo que nominalmente modela**. Esa constatación obligó a reescribir el hallazgo central del artículo, a retirar dos de sus tres conclusiones empíricas y a reorientar la contribución hacia la validez de los inyectores frente a operadores declarativos. El manuscrito revisado es, por ello, más corto en afirmaciones y más firme en las que conserva.

Dos observaciones exigían volver al banco de pruebas. **No es posible:** el experimento se ejecutó sobre un clúster productivo cuya ventana de acceso se cerró al concluir el piloto, y los eventos del plano de control no se conservaron. Antes que afirmar sin prueba, hemos optado por declarar el límite en el propio texto y asignar esos puntos a la Fase 2, que se ejecutará en un entorno dedicado en el marco del Trabajo de Especialización en Desarrollo de Software de la FaCyT-UC. Detallamos abajo el plan.

Cada punto se responde con su número. Las referencias de sección remiten a la versión revisada.

---

## 1. Cambios obligatorios (Árbitro 1)

### Obligatorio 1 — Registros del operador en F2, manifiesto completo y repetición (O9; A2-1)

**ATENDIDO PARCIALMENTE. La repetición se difiere; la reinterpretación se aplica íntegra.**

Aceptamos la objeción sin reservas: el resultado de F2 es un artefacto del inyector. La Sección 5.1 lo desarrolla bajo el epígrafe «Qué mide F2», y hemos ido más allá de lo solicitado en un punto que el informe planteaba como pregunta abierta.

- **El manifiesto.** El clúster se declaró con `primaryUpdateStrategy: unsupervised` y sin fijar `failoverDelay` ni `primaryUpdateMethod`, de modo que rigen sus valores por defecto (0 s y reinicio). El manifiesto está depositado en `20-cluster/cluster-cnpg.yaml`; el artículo lo cita por su ruta.
- **La imagen `pause` en entorno air-gapped.** Su informe preguntaba qué ocurrió con ella. Lo hemos verificado: **no figura entre las imágenes precargadas** (`images/image-list.txt`), por lo que lo más probable es que no llegara a descargarse y el contenedor quedara en `ImagePullBackOff`. Esto explica además el arranque en frío de ≈80,5 s de la primera inyección, tal como usted sugería. Señalamos en el artículo que **la conclusión es robusta a cuál de los dos cursos ocurriera**: en ambos el proceso deja de atender, la especificación del pod queda alterada y el operador la reconcilia reiniciando en su sitio, sin llegar a evaluar una promoción.
- **Los registros del operador.** No se conservaron. Lo hemos verificado de forma exhaustiva: ni los eventos del plano de control, ni el registro crudo del verificador (`verifier-cnpg.log`), ni las marcas del arnés de ejecución (`results.csv`) existen en el repositorio del proyecto —243 revisiones, 808 rutas distintas en todo el historial, incluidas las ramas remotas— ni fuera de él. Quedaron en el clúster productivo, cuya ventana de acceso se cerró al concluir el piloto. **No se facilitan a petición porque no existen**, y así lo declaran ahora el manuscrito, el suplemento y el depósito; la redacción anterior, que los prometía a petición, era incorrecta y se ha corregido. En consecuencia, **el mecanismo se enuncia explícitamente como inferencia a partir de los manifiestos depositados y del comportamiento documentado de ambas herramientas, no como observación.** Hemos corregido también el `README` del depósito, el material suplementario y la sección de disponibilidad de datos, que prometían facilitarlos a petición.
- **La repetición.** Se difiere a la Fase 2 (plan en §3.1 de esta carta). Hasta entonces, la cifra de F2 se presenta como el coste de una reconciliación forzada y **no como un RTO**, y así consta en la Tabla 1 y en su nota.

Como usted anticipaba, el hallazgo central desaparece y el aporte pasa a ser la advertencia metodológica. Es ahora la tesis del artículo, desde el título.

### Obligatorio 2 — V(fallo, K) como hipótesis; ajustar conclusiones (O10, O17)

**ATENDIDO, y más allá de lo solicitado: el predicado se retira.** Su informe pedía degradarlo a hipótesis. Al hacerlo, y al revisar la evidencia disponible, comprobamos que ésta lo contradice por dos vías independientes, de modo que mantenerlo aun como hipótesis no estaba justificado.

La primera es la que usted mismo apuntó en O10: ante un fallo de nodo el objeto Pod **no desaparece** —permanece en `Terminating` hasta que se borre el objeto Node o se aplique `node.kubernetes.io/out-of-service`— y, sin embargo, CloudNativePG promueve. La segunda procede de la fuente que incorporamos a petición suya: en el experimento de aislamiento completo de Sivko (2026) hubo promoción con el pod del primario intacto y corriendo. Citábamos esa fuente sin advertir que refutaba nuestra propia hipótesis.

El disparador documentado es más simple y da cuenta de los tres escenarios: el operador promueve cuando detecta la instancia primaria como no sana, sujeto a `failoverDelay`. Se ha retirado, en consecuencia, el predicado de la lista de contribuciones, de la Sección 5.3, de las conclusiones y la figura que lo ilustraba, junto con las afirmaciones sobre «herramienta reutilizable» y sobre «acercar la teoría a la práctica».

### Obligatorio 3 — Imprecisiones técnicas (T1, T2, T4; A2-4)

**ATENDIDO.** Las cuatro, en la Sección 3.3 y en la 5.1:

| | Corrección |
|---|---|
| T1 | Patroni no despliega etcd propio en Kubernetes: emplea objetos nativos (`Endpoints`/`ConfigMaps`) como DCS, igual que Zalando (Spilo) y Crunchy PGO v5. Ambos enfoques descansan en el *API server*; lo que los separa es **quién decide** la promoción |
| T2a | El *kubelet* no recrea el pod eliminado: CNPG gestiona los pods directamente, sin `StatefulSet` |
| T2b | `node-monitor-grace-period` ≈50 s por defecto en Kubernetes v1.34; la documentación de CNPG sitúa en 40–55 s el intervalo hasta que el pod queda no listo |
| T2c | Un volumen RWO de un nodo caído no se desasocia hasta vencer el temporizador de *attach/detach* (≈6 min) o aplicarse `node.kubernetes.io/out-of-service` (Tabla S2) |
| T4 | CNPG es *shared-nothing*: cada instancia tiene su PVC y la réplica promovida ya lo tiene montado, de modo que la reasociación CSI **no está en el camino crítico del failover**. Se ha retirado por completo el argumento de que F2 fuera «cota inferior» del RTO ante fallo de nodo |

### Obligatorio 4 — Restringir F3, informar sobre el *API server* y la comprobación de aislamiento, incorporar Sivko (T3, O15; A2-2)

**ATENDIDO.** La Sección 5.1 («Qué mide F3») sustituye la lectura CP por lo que efectivamente ocurrió: **ausencia de detección**. Al verificar el mecanismo, sin embargo, encontramos que la explicación que manejábamos era incorrecta, y la correcta agrava el diagnóstico. Son dos efectos, no uno:

1. Las sondas del *kubelet* parten del espacio de red del nodo, y una `NetworkPolicy` gobierna el tráfico entre pods, no el que el propio nodo dirige a un pod local. El primario siguió, pues, `Ready` ante el plano de control.
2. Más importante: Calico aplica la política a las conexiones **nuevas**, pero exceptúa por *conntrack* las ya establecidas, que sobreviven hasta reiniciarse o expirar —tanto es así que Felix ofrece una opción experimental para purgarlas al cambiar la política—. Las conexiones de replicación en *streaming* y la vigilancia del gestor de instancias contra el *API server* precedían a la inyección, de modo que con toda probabilidad siguieron vivas. Lo único que la política cortó con seguridad fueron las conexiones nuevas, y nuestro verificador abre una por inserción.

Esto explica, sin recurrir a los eventos perdidos, por qué no se activó la comprobación de aislamiento, y encaja con la señal más nítida de los datos: la indisponibilidad iguala la duración de la política con precisión de centésimas. **F3 no fue una partición parcial: fue una denegación de conexiones nuevas que afectó sobre todo al cliente de medición.** El protocolo de la Fase 2 incorpora, en consecuencia, la purga del estado de *conntrack* como requisito del escenario de aislamiento.

Señalamos que `probes.liveness.isolationCheck` (CNPG ≥ 1.27) era aplicable, pero que **no puede determinarse si llegó a activarse**, por la pérdida de los eventos.

Incorporamos Sivko (2026) con sus cifras, y conviene aclarar una discrepancia aparente con su informe: la fuente reporta **177 s** de escrituras del primario aislado tras la promoción y **99 s** de ventana en que *ambos* primarios recibían escrituras de clientes. Son magnitudes distintas; su informe citaba la segunda. El artículo recoge ahora las dos, junto con el mecanismo que usted señaló —`failoverDelay` (0 s) y `smartShutdownTimeout` (180 s)—, más la promoción a los 38 s, 291 escrituras confirmadas perdidas y 562 con identificador reasignado. Se retira toda generalización de que CNPG «evita el *split-brain*»: lo que el piloto mostró es que una `NetworkPolicy` que deja intacto el tráfico de *host* no basta para construir ese escenario.

Añadimos una precisión que el informe no pedía: **la salvedad sobre el tráfico de *host* ya constaba en los comentarios del manifiesto depositado**. El error no estuvo en el registro experimental, sino en su traslado a la interpretación. Así se dice en el artículo.

### Obligatorio 5 — Marco formal, título y taxonomía (O5, O1, O7)

**ATENDIDO.**

- **Ecuaciones (2)–(5): retiradas.** Compartimos su diagnóstico: una función no especificada no aporta información. Se conserva `S = (O, K, M, D)` como vocabulario descriptivo en prosa y el reparto por capas (Tabla S2), que es la única relación de la que damos cuenta. La Ec. (6) también se retira: era, como usted indica, una definición de conjunto.
- **Dimensión de rendimiento: eliminada** (O6). No se midió, de modo que hemos optado por suprimirla en lugar de declararla.
- **Título:** ajustado al alcance real.
- **Taxonomía:** rehecha con criterios explícitos y excluyentes. Los operadores se ordenan por **quién decide la promoción** (central en CNPG; distribuida vía Patroni en Zalando y Crunchy v5), lo que resuelve la incoherencia que usted señalaba sobre Crunchy. El almacenamiento se ordena por **dónde reside el dominio de fallo del volumen** (adosado al nodo / replicado / externo al clúster), lo que elimina el solapamiento entre «distribuido» y «en red» que hacía ambiguos Ceph RBD y la SAN.

### Obligatorio 6 — Literatura omitida y citas inadecuadas (O3, O4)

**ATENDIDO.** Verificamos cada alta contra la fuente primaria.

- **Altas:** Sieve (Sun et al., OSDI 22, pp. 143–159), Acto (Gu et al., SOSP '23, pp. 96–112), Sivko (2026) y PACELC (Abadi, 2012, *Computer* 45(2):37–42).
- **WAL:** sustituida Stonebraker & Kemnitz (1991) por ARIES (Mohan et al., 1992, *TODS* 17(1):94–162). Tiene usted razón: el gestor original de POSTGRES era de no sobrescritura.
- **Drees (2026):** matizado. El texto reconoce ahora que su integración continua incorpora comprobaciones de consistencia tipo Jepsen y métricas de tiempo de *failover*; precisamos que su objeto es la no regresión del proyecto, no la caracterización del coste en un despliegue concreto.
- **Bajas por tangenciales:** replicación en cadena, CockroachDB, consistencia eventual y la revisión SQL/NoSQL.

### Obligatorio 7 — Inyecciones de F2 y medianas con y sin la exclusión (E1, E2)

**ATENDIDO.** Hubo **once** inyecciones; se retuvieron diez. Su cálculo era correcto y el manuscrito original, ambiguo. La Sección 5.1 reporta ambas medianas: **36,7 s** con las diez retenidas y **36,9 s** con las once, y declara la exclusión como decisión posterior a la ejecución.

Para que sea auditable, hemos añadido al depósito `data/f2_podfailure_cnpg_excluida.csv` con la inyección descartada, y ampliado `analyze.py` para que reporte ambas medianas. Declaramos dos salvedades sobre esa fila: el valor se conservó de forma aproximada (≈80,5 s) y su marca de tiempo no se retuvo.

### Obligatorio 8 — Cliente de medición y descomposición del RTO de F1 (O11)

**ATENDIDO PARCIALMENTE.**

El cliente queda documentado en la Sección 4.2, a partir del manifiesto depositado: cada inserción es una invocación independiente de `psql` sobre libpq contra el servicio `-rw`, de modo que **abre una conexión nueva en cada iteración** y no media ningún *pooler*; `PGCONNECT_TIMEOUT` = 2 s; el resto de parámetros de libpq, incluido el *keepalive* de TCP, en sus valores por defecto; ante un fallo, espera 0,2 s y reintenta el mismo identificador. El artículo explicita que el RTO reportado engloba detección, promoción, actualización de `Endpoints` y restablecimiento de la conexión.

**La descomposición en línea de tiempo no es posible**: exige los eventos del plano de control, que no se conservaron. Se declara así en el texto y se incorpora al protocolo de la Fase 2, donde el registro de eventos es requisito de validez.

### Obligatorio 9 — Autorización y condiciones de carga compartida (O13)

**ATENDIDO.** La Sección 4.1 declara la autorización del equipo de operaciones, acotada a un espacio de nombres dedicado y con la prohibición expresa de instalar operadores nuevos. Declaramos también las dos fuentes de varianza fuera de control: el operador CNPG atendía otros **cuatro** clústeres del entorno, y el nodo del laboratorio alojaba instancias primarias ajenas al experimento. **Ni la CPU ni la E/S del nodo se registraron durante las rondas**, y así consta.

Sobre la antiafinidad: tiene usted razón. Era **preferente**, que es la modalidad que CNPG aplica por defecto; el planificador la incumplió sin bloquear el despliegue. Corregido.

---

## 2. Cambios recomendados (Árbitro 1)

| | Estado |
|---|---|
| **O12** — LSN y mayor carga de escritura | **Diferido.** El artículo declara que el *lag* ≈ 0 es inferencia y no medida, y la Fase 2 instrumenta `pg_current_wal_lsn()` y `pg_last_wal_replay_lsn()` bajo carga intensiva |
| **O6** — pgbench o eliminar P(S) | **Atendido:** dimensión eliminada |
| **O14** — valores individuales en el texto principal | **Atendido:** la Fig. 1 es ahora un gráfico de puntos con las veinte ejecuciones y sus medianas. Confirmamos que el depósito está abierto y completo |
| **E3, E4** — precisión y deriva | **Atendido** (véase abajo) |
| **O8** — condensar las Secciones 3 y 4 | **Atendido:** fusionadas en una sola, suprimidas tres subsecciones especulativas y trasladada la tabla de responsabilidades al suplemento (Tabla S2) |
| **T6** — período de gracia de pod-kill | **Atendido:** F1 se inyectó sin `gracePeriod`, luego rigió el valor por defecto de Chaos Mesh: terminación abrupta, sin apagado ordenado |
| **T5** — SAN frente a almacenamiento local | **Diferido** al estudio comparativo de la Fase 2 |
| Aspectos formales | **Atendidos** (véase abajo) |

### E3 — Precisión espuria
Las cifras se redondean a una décima, acorde con la resolución del instrumento: **7,9 s** y **36,7 s**. Los cuartiles se reportan como `Q1–Q3` y no como «IQR», según su observación.

### E4 — La correlación no es «débil», y la ejecución en bloques
Corregido: ρ = 0,62 es una asociación **moderada a fuerte**, no significativa con n = 10 **por falta de potencia, no por su magnitud**.

Su pregunta sobre bloques frente a intercalado nos llevó a un hallazgo que agradecemos y que el manuscrito original ocultaba. Las marcas de tiempo depositadas muestran que **los dos escenarios se ejecutaron en bloques separados por ocho horas**: F1 entre las 13:54 y las 14:21 UTC, F2 entre las 22:22 y las 23:03, con inyecciones cada ≈4,5 min. El escenario queda, por tanto, confundido con la hora del día y con la carga de un clúster productivo compartido. Lo declaramos en la Sección 5.1, señalando que el sentido del sesgo esperable es **contrario** al resultado —la franja de mayor actividad corresponde a F1, que es el lote rápido— y asignando la alternancia de escenarios a la Fase 2.

### E5 — La prueba de hipótesis aporta poco
De acuerdo. Se ha reducido a la separación de los lotes y la diferencia de Hodges–Lehmann, con los valores individuales en la Fig. 1. Hemos **retirado las cotas de Clopper–Pearson** sobre la no promoción en F2 y F3: dado que ninguno de los dos escenarios reprodujo su fallo, reportar un intervalo binomial sobre su resultado inducía a error.

### Aspectos formales
1. **Ecuaciones:** retiradas (O5).
2. **Figuras:** las tres observaciones están atendidas. La del banco de pruebas, que usted señaló por su texto ilegible al tamaño de impresión, se **rehízo en formato vectorial** —donde la legibilidad no depende de la resolución— y, por el límite de extensión, se traslada al material suplementario como Fig. S1, citada desde la Sección 4.1. La línea temporal esquemática se sustituye por el gráfico de puntos con las diez ejecuciones de F1 y F2 que usted propone. Y la del predicado de visibilidad se suprime, al haberse retirado el predicado.
3. **Tabla 1:** la columna pasa a «Indisp. (mediana)», se añade la columna `n` y una nota aclara que **solo F1 es un tiempo de recuperación en sentido propio** (O16).
4. **Terminología:** unificada; cuartiles como `Q1–Q3`; cursiva consistente en los términos en inglés.
5. **Referencias:** corregidas, incorporadas y depuradas. La bibliografía se compone ahora en bandera, lo que elimina las URL separadas por espacios.
6. **Autoría:** *(pendiente de incorporar el ORCID de la coautora.)*
7. **Ética y autorización:** declaradas (O13).

---

## 3. Puntos diferidos: justificación y plan de realización

Los siguientes requieren un entorno no productivo, desarrollo de instrumentación o reconfiguración a nivel de sistema operativo. Se ejecutarán en la Fase 2, en el marco del Trabajo de Especialización en Desarrollo de Software de la FaCyT-UC, sobre un clúster multinodo dedicado. **Su requisito previo es un protocolo de validación del inyector:** cada escenario deberá acreditar, mediante los eventos del operador y el estado del pod ante el plano de control, que indujo el fallo que nombra antes de que su medición se dé por válida.

### 3.1 Re-ejecución de F2 sin alterar la especificación del pod (O9; A2-1)
**Por qué se difiere:** exige reconfigurar el arnés con inyección a nivel de proceso —`container-kill` o `SIGKILL` periódico al proceso `postgres`— sin tocar el campo `image` ni las anotaciones del pod. El entorno productivo donde se ejecutó el piloto ya no está disponible.
**Plan:** nuevo protocolo en laboratorio no productivo, contrastando el resultado con los 36,7 s de la reconciliación por cambio de imagen y **registrando los eventos exactos emitidos por el controlador**, que es lo que faltó en el piloto.

### 3.2 Fallo de nodo real y replicación síncrona en clúster multinodo (O10, T4)
**Por qué se difiere:** las tres instancias residieron en un único nodo por restricciones del entorno compartido, lo que impedía probar el desalojo por *taints* y la reasociación de volúmenes.
**Plan:** clúster multinodo dedicado con antiafinidad **obligatoria** (`topologyKey: kubernetes.io/hostname`) y diseño factorial 2×2: replicación asíncrona frente a síncrona por quórum × topología colocalizada frente a distribuida, midiendo el RTO bajo desalojo real y el comportamiento de la capa CSI.

### 3.3 Aislamiento total en F3 para verificar *split-brain* (T3, O15; A2-2)
**Por qué se difiere:** las `NetworkPolicy` de Calico mantienen activo el tráfico de *host* por diseño.
**Plan:** partición estricta mediante iptables/eBPF que aísle al primario del *API server* y de las réplicas, para ejercitar `isolationCheck` y caracterizar si se producen *split-brain* o escrituras fantasma, incorporando el protocolo de Sivko (2026).

### 3.4 F4 mediante cgroups v2 (Sección 5.2)
**Por qué se difiere:** incompatibilidad entre el inyector IOChaos basado en FUSE y `readOnlyRootFilesystem: true`, con el que CNPG endurece sus contenedores.
**Plan:** estrangulamiento de E/S por la interfaz `io.max` de cgroups v2 en el nodo, sin sistemas de archivos en espacio de usuario.

### 3.5 Comparación empírica entre operadores y clases de almacenamiento (O7, T5; A2-4)
**Por qué se difiere:** el equipo de operaciones prohibió instalar operadores adicionales en el clúster productivo.
**Plan:** despliegue paralelo de CNPG, Zalando y Crunchy sobre Local PV, Ceph RBD y SAN Fibre Channel, evaluando latencia de *commit*, *throughput* y tiempo de recuperación.

### 3.6 Retardo de replicación bajo alta concurrencia (O12)
**Por qué se difiere:** exige instrumentación en tiempo real y un perfil de carga que el entorno productivo no admitía.
**Plan:** registro de `pg_current_wal_lsn()` y `pg_last_wal_replay_lsn()` en cada inyección, bajo carga con múltiples escritores concurrentes, para dar poder de detección al RPO.

---

## 3 bis. Sobre la auditabilidad del material empírico

Conviene que el editor y los árbitros conozcan con precisión el alcance de lo que puede comprobarse, porque condiciona el peso de cada afirmación.

**Lo auditable.** Las series de RTO e indisponibilidad por repetición, con sus marcas de tiempo; el recuento de la tabla de verdad del que se deriva el RPO; todos los manifiestos del clúster, de la carga y de cada inyección; el cliente verificador; y los scripts de análisis, que reproducen cada cifra derivada del artículo sin dependencias externas.

**Lo no auditable, y por qué.** El registro crudo del verificador línea a línea, las marcas del arnés de ejecución y los eventos del plano de control. El emparejamiento entre los huecos del verificador y el instante de cada inyección se hizo en su momento sobre esos materiales y no es, por tanto, reproducible desde el depósito.

Esto tiene dos consecuencias que asumimos. La primera: el mecanismo de cada escenario se sostiene en inferencia sobre los manifiestos, no en observación, **y eso vale también para F1** —el cambio de primario sí consta en los datos, pero el evento que lo disparó no—. La segunda: la limitación es ella misma un resultado transferible del piloto. La captura de eventos estaba prevista para la fase de desmontaje, cuando el plazo de retención por defecto de Kubernetes (una hora) hacía mucho que había vencido para las primeras ventanas. No fue un accidente: fue un defecto de diseño del procedimiento. El protocolo de la Fase 2 recoge ahora la captura de eventos **como requisito de validez de cada escenario**, no como tarea de cierre.

## 4. Qué sostiene el artículo revisado

Tras esta revisión, el manuscrito afirma menos y lo afirma mejor:

1. **Una medición defendible:** ante la eliminación del pod primario, CNPG promovió una réplica en las diez repeticiones, con RTO mediano de 7,9 s y sin pérdida de transacciones confirmadas, sobre un clúster productivo y con las restricciones declaradas.
2. **Un diagnóstico:** por qué las otras tres observaciones no son medidas válidas de lo que pretendían medir.
3. **Una advertencia metodológica:** en operadores declarativos, el mecanismo de inyección no es un detalle de implementación sino parte de lo que se mide. Acreditar que produce el fallo que nombra debe preceder a cualquier cifra de resiliencia. Las herramientas de prueba automática de controladores (Sieve, Acto) atacan el problema complementario y no cubren esta fidelidad.
4. **Una retractación**: la regularidad sobre la visibilidad que proponía la versión anterior se retira, porque la evidencia disponible la contradice.
5. **Un diseño corregido** y un paquete de ejecución público que reproduce todas las cifras (DOI: 10.5281/zenodo.23004248).

Quedamos a su disposición para las aclaraciones que estimen necesarias.

Atentamente,

**Herrera, M.** · **Parejo, A.** (autor de correspondencia)
Universidad de Carabobo — Valencia, Venezuela
