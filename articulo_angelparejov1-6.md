# Hacia un Análisis Multicapa de Operadores de PostgreSQL y Almacenamiento CSI en Kubernetes: Taxonomía, Modelo Formal y Protocolo Experimental Reproducible

Angel A. Parejo R., Universidad de Carabobo — Valencia, Estado Carabobo, Venezuela — angelparejo@gmail.com

**Resumen**—La creciente adopción de Kubernetes como plataforma de orquestación de contenedores ha impulsado el surgimiento de operadores de bases de datos (PostgreSQL) y de la Container Storage Interface (CSI). Su interacción es crítica en arquitecturas nativas de la nube, pero rara vez se analiza de forma integrada. Este artículo propone un marco conceptual para dicho análisis: una taxonomía de operadores y almacenamiento CSI, un modelo formal de interacción multicapa S=(O,K,M,D), y un conjunto de invariantes de consistencia, disponibilidad y durabilidad. Con base en el comportamiento documentado de los operadores, se analiza cómo esta interacción puede influir en la recuperación y la consistencia de cargas PostgreSQL gestionadas mediante operadores. Como contribución adicional, se especifica un protocolo experimental reproducible —con inyección controlada de fallos y análisis no paramétrico— para validar empíricamente el marco; su ejecución queda como trabajo futuro. El aporte de este artículo es el marco conceptual y el protocolo, no resultados empíricos.

**Palabras Clave**— Kubernetes, PostgreSQL, operadores de bases de datos, CSI, arquitecturas nativas de la nube, sistemas distribuidos, cargas de trabajo, consistencia, resiliencia y conmutación por error (failover)

## I. Introducción

Kubernetes se ha convertido en la plataforma de facto para la orquestación de cargas de trabajo en contenedores, incluyendo aplicaciones con estado como las bases de datos [1], [2]. Este avance ha favorecido el desarrollo de operadores de bases de datos, particularmente para PostgreSQL, como un mecanismo para automatizar la gestión del ciclo de vida, la replicación y los procesos de conmutación por error (failover) [5], [14].

En paralelo, la Container Storage Interface (CSI) ha introducido un modelo estandarizado para la integración de sistemas de almacenamiento en Kubernetes, lo que facilita el uso de backends de almacenamiento heterogéneos [3].

A pesar de la madurez de estos componentes, la literatura existente tiende a analizarlos de manera aislada, ya sea desde la perspectiva de la orquestación, la consistencia en sistemas distribuidos o la arquitectura de bases de datos [6], [7], [10].

Sin embargo, diversos estudios han demostrado que aspectos como la consistencia, la resiliencia y la recuperación ante fallos están profundamente influidos por la interacción entre múltiples capas del sistema [8], [9].

En entornos reales, la confiabilidad de un clúster PostgreSQL depende del comportamiento conjunto de la lógica del operador, la planificación de Kubernetes, la semántica de replicación y las garantías del almacenamiento, lo que introduce una dependencia multicapa que aún no ha sido suficientemente explorada en la literatura.

Este acoplamiento adquiere especial relevancia bajo condiciones de fallo, donde pequeñas variaciones en el comportamiento del almacenamiento pueden traducirse en diferencias significativas en la recuperación, la pérdida de datos o la consistencia observable.

El argumento central de este artículo es que la confiabilidad de las cargas con estado en Kubernetes debe entenderse como un problema inherentemente multicapa. Aunque un operador de PostgreSQL puede implementar una lógica de control correcta, su comportamiento de recuperación está condicionado por factores externos como la latencia, la durabilidad, la topología y las características de failover asociadas al backend.

De forma inversa, una configuración robusta en la capa de almacenamiento no garantiza por sí misma un comportamiento predecible de la base de datos si no existe alineación con los supuestos del operador y con la semántica de replicación.

En este contexto, este trabajo propone un análisis integrado del problema descrito y presenta las siguientes contribuciones:

- Se propone una taxonomía de operadores de PostgreSQL y de sistemas de almacenamiento basados en CSI en entornos Kubernetes.
- Se define un marco formal de evaluación que integra criterios de resiliencia, consistencia, rendimiento y dependencia multicapa.
- Se introduce un modelo de interacción multicapa que describe cómo la lógica del operador, la semántica de la base de datos y el almacenamiento respaldado por CSI determinan el comportamiento del sistema.
- Se establecen invariantes del sistema orientados a caracterizar la corrección en términos de durabilidad, disponibilidad y consistencia.
- Se especifica un protocolo experimental completo y reproducible, basado en la inyección controlada de fallos sobre un clúster productivo, diseñado para validar empíricamente el modelo y los invariantes propuestos — su ejecución se plantea como línea de trabajo futuro inmediata (Sección IV.E).

Cabe precisar que las contribuciones de este trabajo son de naturaleza conceptual y metodológica: el marco formal, la taxonomía y el protocolo experimental constituyen el aporte central; la ejecución empírica del protocolo y sus resultados se abordan como continuación natural de este trabajo, no como parte del presente artículo.

## II. Trabajos Relacionados

La literatura existente en torno a este problema puede agruparse en tres líneas principales de investigación. Por un lado, los sistemas de orquestación como Borg y Omega sentaron las bases para la gestión de clústeres a gran escala, influyendo directamente en los principios de diseño adoptados posteriormente por Kubernetes [1], [2]. En este contexto, la Container Storage Interface (CSI) introduce una abstracción estandarizada para la gestión del almacenamiento persistente, lo que facilita la integración de backends heterogéneos en entornos Kubernetes [3]. Asimismo, los enfoques declarativos para sistemas stateful han puesto de manifiesto la relevancia del patrón operator y de la lógica de reconciliación como mecanismo de control [5].

En paralelo, la investigación sobre bases de datos distribuidas ha abordado de manera extensa los problemas de consistencia, resiliencia y tolerancia a fallos. Sistemas como CockroachDB evidencian la importancia de la replicación en entornos distribuidos, mientras que los fundamentos teóricos asociados al teorema CAP establecen los límites entre consistencia, disponibilidad y tolerancia a particiones [4], [6], [7]. Estudios más recientes profundizan en modelos de consistencia, incluyendo la verificación formal de consistencia eventual fuerte [8], así como en enfoques probabilísticos para la evaluación de la resiliencia bajo fallos [9].

Por otra parte, diversos trabajos han analizado mecanismos de recuperación, replicación y rendimiento en sistemas de bases de datos. En particular, los estudios basados en Write-Ahead Logging (WAL) destacan su papel central en la durabilidad y recuperación de datos [11], [12], mientras que evaluaciones comparativas de estrategias de replicación muestran su impacto en la calidad del failover y en la latencia de propagación [13]. Adicionalmente, investigaciones recientes han comenzado a explorar el despliegue de bases de datos en Kubernetes mediante operadores, lo que evidencia el creciente interés en la automatización de cargas stateful [14], [15].

Una línea de investigación complementaria, hasta ahora no discutida, es la de la verificación empírica de la resiliencia y la consistencia mediante la inyección controlada de fallos. El enfoque de chaos engineering, popularizado en entornos de producción a gran escala, propone experimentar deliberadamente con fallos para exponer debilidades del sistema antes de que ocurran de forma no controlada [16]. En una línea relacionada, la inyección de fallos dirigida por linaje (lineage-driven fault injection) —en la tradición de verificación de garantías de consistencia bajo fallo, popularizada por herramientas como Jepsen— ha aportado enfoques de referencia para exponer violaciones en sistemas distribuidos, en particular bajo particiones de red [17]. Asimismo, estudios empíricos sobre fallos de partición de red en sistemas cloud en producción han caracterizado la frecuencia y severidad de este tipo de fallos [18], reforzando la relevancia del escenario de partición contemplado en la Sección IV.E. Estas líneas de trabajo proveen fundamentos metodológicos directamente aplicables al diseño experimental propuesto en este artículo, particularmente en lo referente a la verificación de los invariantes de consistencia y disponibilidad definidos en la Sección III.D.

Cabe señalar que, más allá de la literatura académica, existen comparaciones técnicas de carácter práctico entre operadores de PostgreSQL para Kubernetes, publicadas por proveedores y practicantes de la industria [22], [23]. Estas comparaciones, sin embargo, se limitan típicamente a listas de características o recomendaciones de adopción, sin proponer un marco formal de evaluación, invariantes de corrección ni un diseño experimental de inyección de fallos que permita cuantificar las diferencias observadas — que es precisamente la brecha que este artículo busca cerrar.

Sin embargo, a pesar de estos avances, la literatura presenta una limitación significativa: la mayoría de los estudios analizan de forma independiente la capa de orquestación, la de almacenamiento o la de base de datos. En consecuencia, se carece de trabajos que aborden de manera integrada la interacción entre operadores de PostgreSQL y sistemas de almacenamiento basados en CSI. Esta falta de análisis conjunto resulta especialmente relevante en escenarios de fallo, donde la interacción entre estas capas puede afectar directamente la consistencia, la resiliencia y el comportamiento de recuperación del sistema.

## III. Modelo del Sistema y Marco de Evaluación

### III.A Taxonomía de operadores y almacenamiento

Para contextualizar el modelo propuesto, se establece una clasificación de los principales componentes del sistema en función de su diseño y comportamiento operativo. Esta clasificación no solo permite organizar los elementos involucrados, sino que también facilita identificar diferencias relevantes que suelen pasar desapercibidas cuando se analizan de forma aislada.

En el caso de los operadores de PostgreSQL, es posible distinguir tres enfoques predominantes. CloudNativePG se caracteriza por un enfoque claramente cloud-native, en el que la lógica del operador se integra estrechamente con las primitivas y los bucles de reconciliación de Kubernetes. En contraste, Zalando Postgres Operator introduce una dependencia más explícita de herramientas externas de alta disponibilidad, en particular Patroni, que actúa como mecanismo de coordinación. Por su parte, Crunchy Postgres for Kubernetes adopta una posición intermedia, combinando capacidades nativas de Kubernetes con utilidades operativas adicionales; se incluye en esta taxonomía por completitud, aunque el diseño experimental de la Sección IV.E se limita a los dos operadores que representan los extremos del espectro de coordinación (véase justificación de alcance en IV.E). Estas diferencias no son meramente arquitectónicas; en la práctica, influyen en cómo se detectan fallos, se ejecutan procesos de conmutación por error (failover) y se gestionan las transiciones de estado [5], [14].

En la capa de almacenamiento se identifican tres categorías principales respaldadas por la Container Storage Interface (CSI) [3]. El almacenamiento local (CSI local) se distingue por su baja latencia y simplicidad operativa, aunque introduce una mayor sensibilidad a fallos a nivel de nodo. Por otro lado, el almacenamiento distribuido (CSI distribuido), como Ceph o Longhorn, ofrece mayor tolerancia a fallos mediante replicación, a costa de incrementar la complejidad operativa y la latencia. Finalmente, el almacenamiento en red (CSI en red) permite un mayor desacoplamiento topológico, aunque su comportamiento puede variar significativamente en función de las condiciones de red y de la infraestructura subyacente.

En conjunto, esta taxonomía establece el contexto sobre el cual se construye el modelo del sistema y permite interpretar, de forma más precisa, las variaciones de comportamiento observadas en distintos escenarios.

### III.B Modelo del sistema

A partir de la taxonomía descrita, el sistema se modela como una tupla:

**S = (O, K, M, D)**

Donde O representa la lógica del operador de PostgreSQL, K el plano de control de Kubernetes, M la capa de almacenamiento (el "medio" de persistencia) gestionada mediante CSI, y D el motor de base de datos. Se usa M en lugar de C para evitar una colisión de notación con la dimensión de Consistencia, C(S), definida en la Sección III.C. Esta representación se apoya en la arquitectura de sistemas orquestados en Kubernetes [1], [2], en el modelo de abstracción de almacenamiento definido por CSI [3] y en enfoques declarativos para la gestión de sistemas con estado (stateful) [5].

Más que una formulación estrictamente matemática, este modelo pretende capturar de forma estructurada las interacciones clave entre los distintos componentes. En particular, permite razonar sobre cómo decisiones en una capa pueden propagarse y afectar el comportamiento global del sistema bajo diferentes condiciones operativas. La Fig. 1 ilustra las capas del modelo y sus principales interacciones.

**Fig. 1.** Modelo de interacción multicapa S = (O, K, M, D): el operador coordina el ciclo de vida y el failover a través del plano de control de Kubernetes; el motor de base de datos persiste el WAL sobre el almacenamiento respaldado por CSI. El comportamiento emergente se captura mediante I(S) = f(O × K × M × D).

### III.C Dimensiones de evaluación

Con base en el modelo anterior, se definen cuatro dimensiones principales que permiten evaluar el comportamiento del sistema desde diferentes perspectivas:

**Resiliencia:** se modela como R(S) = f(F, T_recuperación, A), donde F representa el tipo de fallo, T_recuperación el tiempo necesario para restablecer el servicio y A el nivel de disponibilidad alcanzado tras la recuperación. Este enfoque es consistente con modelos probabilísticos de resiliencia en sistemas distribuidos [9].

**Consistencia:** se expresa como C(S) = f(Tx_confirmadas, Tx_visibles), estableciendo como condición fundamental que toda transacción confirmada debe permanecer visible después de un evento de fallo. Este planteamiento se fundamenta en los principios de consistencia en sistemas distribuidos y en el teorema CAP [6], [7].

**Rendimiento:** se aproxima mediante P(S) = f(latencia, throughput), lo que refleja cómo las decisiones de diseño y las características del almacenamiento influyen en la eficiencia del sistema, en línea con estudios comparativos de arquitecturas de bases de datos [10].

**Interacción multicapa:** se representa como I(S) = f(O × K × M × D), con el propósito de capturar la dependencia entre la lógica del operador, el plano de control de Kubernetes, el comportamiento del almacenamiento y la semántica de la base de datos. La inclusión explícita de K refleja el rol activo que el plano de control desempeña en la coordinación de fallos —por ejemplo, como punto único de coordinación durante una partición de red (véase Tabla I)— y no solo un papel pasivo de ejecución. Esta dimensión introduce una perspectiva integradora que trasciende los enfoques tradicionales, en los que dichas capas suelen analizarse por separado.

Cabe precisar que las funciones f(·) definidas en esta sección cumplen un propósito organizativo: identifican las variables relevantes para cada dimensión y no constituyen, en esta etapa, relaciones funcionales cerradas ni derivadas analíticamente. Su especificación operacional —por ejemplo, una cota del RPO en función de la latencia de replicación y del modo síncrono o asíncrono del backend CSI— queda como línea de trabajo futuro, en conjunto con la validación empírica descrita en la Sección IV.E.

En conjunto, estas dimensiones permiten evaluar el sistema de forma más completa, especialmente en escenarios en los que intervienen fallos o variaciones en la infraestructura subyacente.

### III.D Invariantes del sistema

El modelo se complementa con un conjunto de invariantes que permiten caracterizar un comportamiento aceptable del sistema bajo condiciones normales y de fallo:

- **Invariante de consistencia:** toda transacción confirmada debe permanecer accesible tras un proceso de recuperación, en concordancia con los modelos de consistencia en sistemas distribuidos [6].
- **Invariante de disponibilidad:** el tiempo de recuperación (RTO) debe mantenerse dentro de un umbral aceptable, conforme a criterios ampliamente utilizados en estudios de resiliencia [9].
- **Invariante de durabilidad:** toda operación registrada en el log de escritura anticipada (WAL) debe ser recuperable tras un fallo, tal como se establece en estudios sobre mecanismos de recuperación en bases de datos [11], [12].

Estos invariantes no solo proporcionan un marco formal para evaluar la corrección del sistema, sino que también permiten vincular este análisis teórico con una futura validación empírica, en la que cada uno de ellos puede operacionalizarse mediante métricas observables como RPO, latencia de failover o pérdida de transacciones.

## IV. Análisis Comparativo y Discusión de Escenarios

### IV.A Comparación entre operadores de PostgreSQL

A partir de la taxonomía definida en la sección anterior, es posible identificar diferencias relevantes en el comportamiento de los operadores de PostgreSQL en distintos escenarios operativos. En particular, las variaciones en el diseño del plano de control y en el modelo de dependencias influyen directamente en la gestión de eventos de fallo y en los procesos de recuperación.

Los operadores con enfoque cloud-native, como CloudNativePG, tienden a integrarse de forma más estrecha con los mecanismos de Kubernetes, lo que favorece una mayor coherencia con el ciclo de vida de los recursos del clúster [5], [14]. En contraste, soluciones como Zalando Postgres Operator, al depender de herramientas externas como Patroni, introducen un nivel adicional de coordinación que puede afectar tanto la latencia de detección de fallos como los tiempos de promoción. Por su parte, enfoques híbridos como Crunchy Postgres presentan un comportamiento intermedio, combinando automatización nativa con herramientas operativas más avanzadas.

Estas diferencias sugieren que la resiliencia del sistema, expresada como R(S), no depende únicamente del operador en sí, sino de cómo este se articula con los mecanismos de coordinación, replicación y recuperación, lo cual ha sido ampliamente discutido en sistemas distribuidos y plataformas stateful [5], [14].

### IV.B Impacto del tipo de almacenamiento CSI

El tipo de almacenamiento introduce variaciones significativas en el comportamiento del sistema, particularmente en la latencia, la durabilidad y el dominio de fallo.

El uso de almacenamiento local (CSI local) tiende a reducir la latencia, lo que puede favorecer el rendimiento P(S). No obstante, esta ventaja se ve limitada por una mayor exposición a fallos a nivel de nodo, lo que puede afectar negativamente la resiliencia R(S). En cambio, el almacenamiento distribuido (CSI distribuido) ofrece mayores garantías de persistencia y replicación, lo que reduce el riesgo de pérdida de datos, aunque introduce latencias adicionales que pueden afectar la visibilidad de las transacciones, en línea con los compromisos descritos en modelos de consistencia distribuida [6], [7].

Por otro lado, el almacenamiento en red presenta un comportamiento menos predecible, ya que depende en gran medida de factores externos como la conectividad y la estabilidad de la infraestructura. Esta dependencia introduce variabilidad en la interacción multicapa I(S), especialmente en escenarios de carga elevada o fallos parciales, lo cual puede afectar tanto la disponibilidad como el tiempo de recuperación [9].

### IV.C Interacción operador–almacenamiento

Uno de los aspectos más relevantes que surge de este análisis es la dependencia entre el operador y el tipo de almacenamiento utilizado. Esta interacción resulta especialmente crítica, ya que el comportamiento del sistema no puede explicarse de forma aislada en cada capa. La Tabla I sintetiza, a partir del comportamiento documentado de CloudNativePG [19], Zalando Postgres Operator (Patroni) [20] y Crunchy Postgres for Kubernetes [21], la distribución de responsabilidades de detección y recuperación entre capas para los principales tipos de fallo.

**Tabla I.** Responsabilidad de detección y recuperación por capa y tipo de fallo

| Tipo de fallo | Operador (O) | Kubernetes (K) | Almacenamiento CSI (M) |
|---|---|---|---|
| Fallo del pod primario | Detecta la pérdida del líder y promueve una réplica (CloudNativePG: gestor de instancias propio; Zalando y Crunchy: Patroni) | Reinicia el pod (kubelet) y actualiza Services y Endpoints hacia el nuevo primario | Reasocia el PVC existente al pod recreado; sin acciones sobre los datos |
| Fallo de nodo | Ordena la promoción de una réplica si el primario residía en el nodo afectado | Marca el nodo NotReady (≈40 s) y desaloja los pods tras el umbral de tolerancia (≈5 min por defecto) | Local: datos inaccesibles hasta recuperar el nodo; distribuido: las réplicas permiten readjuntar el volumen en otro nodo |
| Fallo de disco / volumen | Recrea la instancia y solicita resincronización desde el primario o desde respaldo (Crunchy: pgBackRest) | Reporta el PV como degradado y reprograma el pod según la StorageClass | Distribuido (Ceph/Longhorn): reconstruye réplicas del volumen; local: pérdida del volumen, la durabilidad depende del WAL replicado |
| Partición de red | Debe evitar el split-brain: cercado del antiguo primario (Patroni: expiración del lease en el DCS; CloudNativePG: estado en el API server) | El API server actúa como punto único de coordinación; una minoría del plano de control bloquea la reconciliación | En red: E/S bloqueada o degradada; distribuido: la pérdida de quórum puede congelar las escrituras |

Tomando como ejemplo la primera fila de la Tabla I, el fallo del pod primario instancia la función I(S) = f(O × K × M × D) de la siguiente manera: O ejecuta la detección de pérdida de líder y la promoción de réplica; K (kubelet, Services/Endpoints) restablece el enrutamiento hacia el nuevo primario; M reasocia el volumen persistente sin intervención sobre los datos; y D retoma la aceptación de escrituras una vez el nuevo primario está disponible. El comportamiento emergente —el RTO observado— resulta de la composición temporal de estas cuatro acciones, no de ninguna de ellas por separado.

Por ejemplo, un operador que asume tiempos de persistencia bajos puede comportarse de manera subóptima cuando se despliega sobre un sistema de almacenamiento distribuido con mayor latencia. De forma similar, configuraciones basadas en almacenamiento local pueden incrementar el riesgo de inconsistencias si los mecanismos de failover no consideran adecuadamente la posible pérdida de datos en caso de fallo de nodo, particularmente en relación con la persistencia del WAL [11], [12].

En este contexto, la función de interacción multicapa I(S) = f(O × K × M × D) resulta útil para interpretar estos comportamientos, ya que permite analizar cómo decisiones en una capa pueden propagarse y afectar a las demás, lo que refuerza la necesidad de un enfoque integrado.

### IV.D Implicaciones para la evaluación del sistema

El análisis realizado pone de manifiesto que la evaluación de sistemas PostgreSQL en Kubernetes no puede abordarse desde una única dimensión. En particular, se observa un trade-off entre rendimiento, resiliencia y consistencia, fuertemente condicionado por la combinación de operador y tipo de almacenamiento, tal como se plantea en la literatura sobre sistemas distribuidos [6], [7], [9].

Este análisis refuerza la necesidad de un enfoque integrado como el propuesto en este trabajo, donde el modelo del sistema y las dimensiones de evaluación permiten analizar de forma conjunta estos factores. Asimismo, establece una base sólida para una futura evaluación empírica, en la que estos aspectos puedan medirse mediante métricas como RTO, RPO, latencia de transacciones y pérdida de datos.

### IV.E Diseño experimental propuesto

Con el fin de operacionalizar el marco anterior, se propone un diseño experimental sobre un clúster Kubernetes en producción (v1.34.6), con PostgreSQL 16.13, almacenamiento en red respaldado por el controlador CSI de Huawei 4.10.1 sobre Fibre Channel (SAN) y red gestionada mediante Calico 3.31.4. Se comparan dos operadores representativos de la taxonomía de la sección III: CloudNativePG 1.28.0, como exponente del enfoque cloud-native, y Zalando Postgres Operator v1.13.x (con Spilo 16 como imagen base de PostgreSQL), como exponente de la coordinación delegada en Patroni. Crunchy Postgres for Kubernetes, aunque forma parte de la taxonomía de la Sección III.A, queda fuera del alcance experimental de este diseño: al combinar mecanismos nativos con herramientas adicionales de forma similar a ambos operadores seleccionados, no ofrece un punto de contraste claramente diferenciado dentro de las restricciones de tiempo y acceso al clúster productivo disponibles para este piloto; su validación queda como extensión natural de este trabajo. La inyección de fallos se realiza con Chaos Mesh 2.7.x. Dado que el entorno se encuentra aislado de redes externas (air-gapped), tanto Chaos Mesh como las imágenes de los operadores se instalan a partir de imágenes importadas localmente en el entorno de ejecución de contenedores de cada nodo del laboratorio.

El experimento se ejecuta en un espacio de nombres dedicado, con cuotas de recursos y un alcance de inyección restringido por control de acceso, de modo que las cargas productivas permanecen fuera del dominio de fallo. Cada operador despliega un clúster de tres instancias (un primario y dos réplicas) sometido a una carga sintética continua generada con pgbench (escala `-s 10`, 4 clientes y 2 hilos concurrentes, en rondas sucesivas de 60 segundos que toleran failovers), junto con un cliente de verificación que registra cada transacción confirmada y comprueba su visibilidad tras la recuperación. Esto permite operacionalizar los invariantes de la sección III: el RPO se mide como transacciones confirmadas no visibles tras el fallo, y el RTO como el tiempo transcurrido hasta la primera escritura aceptada por el nuevo primario. El protocolo contempla la sincronización de reloj (NTP) entre los nodos del clúster y el cliente de verificación, dado que el RTO se mide en el orden de segundos; esta sincronización se validará como parte de la puesta a punto del laboratorio, previa a la ejecución de los experimentos.

Se contemplan tres escenarios de fallo reproducibles de forma segura en un entorno productivo: (i) la terminación del pod primario, mediante el experimento `PodChaos` en modo `pod-kill` de Chaos Mesh; (ii) la indisponibilidad sostenida del primario durante 10 minutos, mediante `PodChaos` en modo `pod-failure`, como aproximación observable de un fallo de nodo desde la perspectiva del operador; y (iii) la partición de red del primario mediante una `NetworkPolicy` de Calico —sin intervención de Chaos Mesh—, aplicada y revertida mediante `kubectl`. Como eje central, se aplica un análisis de sensibilidad paramétrico que inyecta niveles crecientes de latencia de E/S (0, 20, 50 y 100 ms) mediante el experimento `IOChaos` de Chaos Mesh, actuando a nivel de FUSE dentro del pod del primario. Es importante precisar que esta inyección opera sobre la capa de acceso a archivos del contenedor y no altera el camino de E/S real hacia la SAN Huawei ni afecta a otros consumidores del arreglo; por lo tanto, aproxima la latencia percibida por la aplicación ante una degradación del backend, sin reproducir una degradación real del arreglo de almacenamiento. El nivel de 0 ms corresponde a la línea base sin manifiesto de `IOChaos` activo.

Cada combinación de operador, escenario y nivel de latencia se repite diez veces. Este tamaño muestral responde a un compromiso práctico entre las ventanas de mantenimiento disponibles en el clúster productivo y la necesidad de estimar medianas y percentiles mediante pruebas no paramétricas; no se realizó un cálculo formal de potencia estadística, y n=10 se declara como suficiente para detectar diferencias de magnitud práctica entre operadores y niveles de latencia, no efectos marginales. Dada la distribución no normal esperada de RTO y RPO, se reportan medianas y percentiles y se emplean pruebas no paramétricas (Mann–Whitney y Kruskal–Wallis), así como la correlación de Spearman para la relación entre latencia inyectada y tiempo de recuperación. Los fallos de nodo en la capa de orquestación —expulsión de pods y readjunte de volúmenes— no se reproducen empíricamente por restricciones del entorno productivo y se abordan de forma analítica mediante la Tabla I. Esta aproximación —indisponibilidad sostenida del primario en lugar de un fallo de nodo real— no captura la latencia de reasociación (detach/attach) del volumen respaldado por el CSI de Huawei, que en un fallo de nodo genuino suele ser un componente dominante del RTO observado; el escenario (ii) debe interpretarse, por tanto, como una cota inferior del RTO real ante pérdida de nodo, no como una réplica completa de dicho evento.

## V. Discusión

El análisis conceptual desarrollado evidencia que el comportamiento de sistemas PostgreSQL en Kubernetes no puede explicarse adecuadamente considerando únicamente una de sus capas. En particular, la interacción entre el operador, el sistema de almacenamiento y la semántica de la base de datos introduce efectos emergentes que los enfoques tradicionales, centrados en un solo componente, no logran capturar.

Desde una perspectiva arquitectónica, este hallazgo refuerza la idea de que la confiabilidad en entornos cloud-native es un fenómeno inherentemente multicapa. Aunque la literatura en sistemas distribuidos ha abordado de manera extensa aspectos como la consistencia, la resiliencia y la tolerancia a fallos [6], [7], [9], estos estudios rara vez consideran el impacto específico de los mecanismos de orquestación y de las abstracciones de almacenamiento como CSI en el comportamiento final del sistema.

En términos prácticos, este análisis sugiere que decisiones aparentemente locales —como la selección de un operador o de un tipo de almacenamiento— pueden tener implicaciones globales en métricas críticas como RTO, RPO o la visibilidad de las transacciones. Esto plantea desafíos importantes para el diseño de arquitecturas robustas, ya que optimizaciones en una dimensión pueden introducir degradaciones en otras.

Asimismo, el modelo propuesto en este trabajo ofrece una base conceptual útil para analizar estas dependencias. En particular, la función de interacción multicapa I(S) permite interpretar cómo la combinación de operador, almacenamiento y base de datos influye en el comportamiento del sistema, extendiendo enfoques previos que tienden a analizar estos elementos de forma independiente.

No obstante, este trabajo presenta ciertas limitaciones. En primer lugar, el análisis es de carácter conceptual y no incluye una validación empírica directa. Aunque el modelo y los invariantes definidos permiten razonar sobre el comportamiento del sistema, su validación requiere experimentación en condiciones controladas, especialmente mediante la inyección de fallos. En segundo lugar, la taxonomía propuesta, aunque representativa, no abarca la totalidad de operadores ni de implementaciones CSI existentes, lo que podría limitar la generalización de los resultados. En tercer lugar, el entorno de validación disponible se basa exclusivamente en almacenamiento en red (SAN sobre Fibre Channel) con hardware homogéneo en todos los nodos, por lo que el contraste empírico entre las categorías de almacenamiento local, distribuido y en red, así como los fallos de nodo en la capa de orquestación, se abordan de forma analítica y se declaran como trabajo futuro.

A pesar de estas limitaciones, el enfoque adoptado representa una contribución relevante al establecer un marco integrador que conecta distintas líneas de investigación. Además, define una base clara para futuros trabajos empíricos, en los que los invariantes propuestos puedan operacionalizarse mediante métricas observables como pérdida de datos, tiempos de recuperación o consistencia percibida por las aplicaciones.

En este sentido, una línea natural de trabajo futuro consiste en ejecutar el protocolo experimental especificado en la Sección IV.E, con el fin de validar y refinar el modelo presentado.

## VI. Conclusiones

Este trabajo abordó el análisis de sistemas PostgreSQL en Kubernetes desde una perspectiva multicapa, considerando de manera integrada la interacción entre operadores, almacenamiento basado en CSI y la semántica de la base de datos. A diferencia de enfoques tradicionales que estudian estos componentes de forma aislada, se propuso un marco conceptual que permite caracterizar su comportamiento conjunto.

Como contribución principal, se presentó una taxonomía de operadores y sistemas de almacenamiento, un modelo formal del sistema S = (O, K, M, D) que facilita el análisis estructurado de sus interacciones, y un protocolo experimental completamente especificado y reproducible para su validación empírica (Sección IV.E). Sobre esta base, se definieron dimensiones de evaluación —resiliencia, consistencia, rendimiento e interacción multicapa— y un conjunto de invariantes orientados a caracterizar la corrección del sistema en presencia de fallos.

El análisis desarrollado evidencia que la confiabilidad de cargas de trabajo stateful en Kubernetes no depende exclusivamente de la calidad de un operador o de las propiedades del almacenamiento, sino del comportamiento emergente derivado de su interacción. En particular, se identifican decisiones de diseño en las que se debe sacrificar un atributo para obtener otro (trade-offs), en aspectos como el rendimiento, la disponibilidad y la consistencia, condicionados por elecciones que atraviesan múltiples capas del sistema.

Estos resultados ponen de manifiesto la necesidad de adoptar enfoques integrados para el diseño y la evaluación de arquitecturas cloud-native, especialmente en contextos donde la persistencia de datos y la tolerancia a fallos son críticas. Asimismo, el modelo propuesto establece una base formal que puede utilizarse para analizar configuraciones heterogéneas y guiar decisiones arquitectónicas.

Como trabajo futuro inmediato, se plantea la ejecución del protocolo experimental especificado en la Sección IV.E —ya definido en términos de herramientas, mecanismos de inyección de fallos, carga sintética y plan de análisis estadístico— para medir RTO, RPO, latencia de recuperación y pérdida de datos en los escenarios descritos, y validar así los invariantes propuestos. Esta línea de investigación permitirá no solo validar los invariantes propuestos, sino también refinar el modelo a partir de observaciones empíricas.

En conjunto, este trabajo contribuye a cerrar la brecha existente entre la teoría de sistemas distribuidos y las implementaciones prácticas en Kubernetes, proporcionando un marco conceptual y analítico que facilita la comprensión y la evaluación de sistemas PostgreSQL en entornos cloud-native.

## Referencias

[1] B. Burns, B. Grant, D. Oppenheimer, E. Brewer, and J. Wilkes, "Borg, Omega, and Kubernetes," ACM Queue, vol. 14, no. 1, pp. 70–93, 2016.
[2] M. Schwarzkopf, A. Konwinski, M. Abd-El-Malek, and J. Wilkes, "Omega: Flexible, scalable schedulers for large compute clusters," in Proc. EuroSys, 2013, pp. 351–364.
[3] Kubernetes, "Container Storage Interface (CSI)," 2024. [Online]. Available: https://kubernetes.io
[4] A. Taft et al., "CockroachDB: The resilient geo-distributed SQL database," in Proc. ACM SIGMOD Int. Conf. Management of Data, 2020, pp. 1493–1509.
[5] Kubernetes, "Operator pattern," Kubernetes Documentation. [Online]. Available: https://kubernetes.io/docs/concepts/extend-kubernetes/operator/ [Consultado: 8 de julio de 2026]
[6] P. Bailis and A. Ghodsi, "Eventual consistency today: limitations, extensions, and beyond," Communications of the ACM, vol. 56, no. 5, pp. 55–63, 2013.
[7] S. Gilbert and N. Lynch, "Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services," ACM SIGACT News, vol. 33, no. 2, pp. 51–59, 2002.
[8] M. Burckhardt, "Principles of eventual consistency," Foundations and Trends in Programming Languages, vol. 1, no. 1–2, pp. 1–150, 2014.
[9] A. Avizienis, J.-C. Laprie, B. Randell, and C. Landwehr, "Basic concepts and taxonomy of dependable and secure computing," IEEE Trans. Dependable and Secure Computing, vol. 1, no. 1, pp. 11–33, 2004.
[10] W. Khan, T. Kumar, C. Zhang, K. Raj, A. M. Roy, and B. Luo, "SQL and NoSQL database software architecture performance analysis and assessments—A systematic literature review," Big Data and Cognitive Computing, vol. 7, no. 2, art. 97, 2023, doi: 10.3390/bdcc7020097.
[11] F. Han et al., "PALF: Replicated write-ahead logging for distributed databases," Proc. VLDB Endow., vol. 17, no. 12, pp. 3745–3758, 2024, doi: 10.14778/3685800.3685803.
[12] M. Stonebraker and G. Kemnitz, "The POSTGRES next-generation database management system," Communications of the ACM, vol. 34, no. 10, pp. 78–92, 1991.
[13] R. van Renesse and F. B. Schneider, "Chain replication for supporting high throughput and availability," in Proc. OSDI, 2004.
[14] J. Dobies and J. Wood, Kubernetes Operators: Automating the Container Orchestration Platform. Sebastopol, CA, USA: O'Reilly Media, 2020.
[15] C. Mega, "Orchestrating information governance workloads as stateful services using Kubernetes operator framework," in Service-Oriented Computing (SummerSOC 2023), Communications in Computer and Information Science, vol. 1847. Cham, Switzerland: Springer, 2023, pp. 125–143, doi: 10.1007/978-3-031-45728-9_8.
[16] A. Basiri, N. Behnam, R. de Rooij, L. Hochstein, L. Kosewski, J. Reynolds, and C. Rosenthal, "Chaos Engineering," IEEE Software, vol. 33, no. 3, pp. 35–41, 2016.
[17] P. Alvaro and S. Tymon, "Abstracting the Geniuses Away from Failure Testing," Communications of the ACM, vol. 61, no. 1, pp. 54–61, 2018.
[18] A. Alquraan, H. Takruri, M. Alfatafta, and S. Al-Kiswany, "An Analysis of Network-Partitioning Failures in Cloud Systems," in Proc. 13th USENIX Symposium on Operating Systems Design and Implementation (OSDI 18), Carlsbad, CA, 2018, pp. 51–68.
[19] CloudNativePG, "CloudNativePG Documentation," 2026. [Online]. Available: https://cloudnative-pg.io/docs/ [Consultado: 8 de julio de 2026]
[20] Patroni, "Patroni: A Template for PostgreSQL HA with ZooKeeper, etcd or Consul — Documentation," 2026. [Online]. Available: https://patroni.readthedocs.io/ [Consultado: 8 de julio de 2026]
[21] Crunchy Data, "PGO: the Postgres Operator from Crunchy Data — Documentation," 2026. [Online]. Available: https://access.crunchydata.com/documentation/postgres-operator/latest/ [Consultado: 8 de julio de 2026]
[22] Portworx, "Choosing a Kubernetes Operator for PostgreSQL." [Online]. Available: https://portworx.com/blog/choosing-a-kubernetes-operator-for-postgresql/
[23] simplyblock, "How to choose your Kubernetes Postgres Operator?" [Online]. Available: https://simplyblock.io/blog/choosing-a-kubernetes-postgres-operator/
