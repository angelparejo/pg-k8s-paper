# Decisión Editorial
**Fecha:** 2026-07-04
**Revista objetivo:** Tier primario (CLEI Electronic Journal / RISTI / Ingeniare / Computación y Sistemas)
**Artículo:** Análisis Sistemático de Operadores de PostgreSQL y Almacenamiento basado en CSI en Kubernetes: Arquitectura, Manejo de Fallos e Implicaciones en la Consistencia (v1-5)
**Decisión:** REVISIÓN MAYOR

## Evaluación del editor

Ambos árbitros — sin verse entre sí — convergen de forma notable: puntajes casi idénticos (57 y 58/100), la misma recomendación explícita (Revisión Mayor), y la misma preocupación central: el artículo no ejecuta ningún experimento, y el aparato formal S=(O,K,C,D)/R(S)/C(S)/P(S)/I(S) no realiza ningún trabajo analítico operacional. Que dos disposiciones distintas (una desconfiada de la formalización, otra centrada en reproducibilidad técnica) lleguen independientemente al mismo diagnóstico es una señal fuerte de que el problema es real, no un capricho de un árbitro.

Nota sobre la escala de puntaje: la rúbrica estándar (<65 → Rechazar) sugeriría técnicamente "Rechazar" para ambos puntajes. No sigo la regla mecánica aquí: ninguno de los dos árbitros identificó una falla FATAL (pregunta equivocada, diseño irreparable, contribución inexistente) — ambos, de hecho, recomendaron explícitamente "Revisión Mayor", no rechazo. Mi lectura sustantiva coincide con la de ambos: hay una contribución real (la taxonomía + Tabla I + protocolo experimental es información genuinamente útil y bien construida), pero el volumen de trabajo pendiente —no la inexistencia del aporte— es lo que impide un veredicto menor.

**Hallazgo propio, adicional a ambos árbitros:** revisé `paper/replication/pg-chaos-lab.zip`, el kit de laboratorio ya copiado al repositorio, y varias de las objeciones de "no reproducibilidad" del Árbitro 2 ya están resueltas en el kit — solo no están volcadas al texto del artículo:
- La herramienta de inyección de fallos SÍ está decidida: **Chaos Mesh 2.7.x** (instalación offline, scoped), con `PodChaos` (`pod-kill`/`pod-failure`) para F1/F2, **NetworkPolicy de Calico — no Chaos Mesh** — para F3, e `IOChaos` para F4.
- El mecanismo de la latencia de E/S (F4) es **vía FUSE dentro del pod** y, según el propio kit, **no toca la SAN Huawei ni otros consumidores del arreglo** — es una aproximación a nivel de aplicación, no una alteración real del path SAN/FC. El artículo no lo aclara; un lector podría entender lo contrario.
- La "carga sintética continua" ya está operacionalizada: **pgbench**, `-c 4 -j 2 -T 60` en bucle, `-s 10` de escala.
- La versión de Zalando/Patroni ya está fijada: **v1.13.x + Spilo 16**.

Esto cambia la severidad de esos puntos específicos: no son una laguna de diseño experimental (el diseño ya existe y está implementado), son una laguna de **redacción** — el artículo describe el protocolo en abstracto sin citar el kit que ya lo instancia. Los dejo como MUST porque un árbitro real no tiene por qué saber que existe un repositorio no mencionado en el texto, pero la corrección es mecánica y rápida, no una reformulación de fondo.

## Clasificación de objeciones

### FATAL
Ninguna. Ningún árbitro encontró una falla irreparable de diseño, pregunta mal planteada, o ausencia de contribución.

### SUBSANABLE

**MUST Address (no negociable para esta revisión):**

1. **Ausencia de validación empírica ejecutada** — el eje central señalado independientemente por ambos árbitros. Dos caminos, a elegir por el autor:
   (a) ejecutar al menos un piloto (una combinación operador × escenario) usando el kit `pg-chaos-lab` ya implementado y reportar RTO/RPO reales; o
   (b) reencuadrar explícitamente el artículo (título, resumen, framing de "análisis sistemático") como marco conceptual + protocolo experimental completamente especificado, sin dar a entender que hay resultados inminentes.
2. Nombrar explícitamente la herramienta de inyección de fallos (**Chaos Mesh 2.7.x**) y los mecanismos concretos por escenario (PodChaos para F1/F2, NetworkPolicy de Calico para F3, IOChaos vía FUSE para F4) — información ya existente en el kit de replicación, solo falta trasladarla al texto.
3. Aclarar que la inyección de latencia de E/S (F4) es vía FUSE a nivel de pod y **no altera el path real de la SAN** — evitar que el lector infiera manipulación directa del arreglo Huawei.
4. Operacionalizar "carga sintética continua": nombrar **pgbench** y sus parámetros (`-c 4 -j 2 -T 60`, escala `-s 10`).
5. Especificar la versión de Zalando Postgres Operator / Patroni (**v1.13.x + Spilo 16**) — actualmente solo se fija versión para CloudNativePG.
6. Resolver la colisión de notación: **C** se usa simultáneamente para la capa de almacenamiento (S=(O,K,C,D)) y para la dimensión de consistencia (C(S)).
7. Justificar o corregir la ausencia de **K** en I(S)=f(O×C×D), pese a ser miembro de la tupla S y actor central en la Tabla I.
8. Incorporar la literatura de chaos engineering y verificación de consistencia bajo partición (Basiri et al. 2016; Kingsbury/Jepsen; Alquraan et al. 2018) — señalada de forma independiente por ambos árbitros, lo que la hace un consenso fuerte.

**SHOULD Address (fuertemente recomendado):**

1. Dar contenido operacional mínimo a al menos una función f(·), o declarar explícitamente que la notación es organizativa, no matemático-operacional.
2. Justificar el tamaño muestral n=10 por combinación (cálculo de potencia o referencia comparable).
3. Discutir qué se pierde al aproximar "fallo de nodo" con indisponibilidad sostenida del primario (p. ej., la latencia de reattach del driver CSI de Huawei, que suele dominar el RTO real ante un fallo de nodo genuino).
4. Citar documentación oficial de cada operador (CloudNativePG, Patroni, Crunchy PGO) en la Tabla I, no solo [5]/[14].
5. Conectar al menos una fila de la Tabla I con la notación formal, para que el modelo y el análisis cualitativo no corran en paralelo.
6. Declarar sincronización de reloj (NTP) entre nodos del clúster y cliente de verificación.
7. Aclarar el alcance: la Sección III/IV.A discuten tres operadores (incluyendo Crunchy) mientras que el diseño experimental de IV.E solo instrumenta dos — justificar explícitamente por qué Crunchy queda fuera de la validación aunque esté en la taxonomía.
8. Comparar explícitamente el aporte frente a comparativas técnicas ya publicadas en la industria (blogs EDB/Ongres/Portworx, charlas KubeCon).

### DE ESTILO (MAY — se puede rebatir diplomáticamente)

1. **Nota editorial propia:** la afiliación del autor en el artículo dice "Caracas, Venezuela", pero la configuración del proyecto (`CLAUDE.md`, `domain-profile.md`) especifica "Valencia, Estado Carabobo, Venezuela — Universidad de Carabobo". Verificar cuál es la correcta antes de la versión final.
2. Normalizar "conmutación por error (failover)" tras la primera aparición.
3. Verificar el conteo de palabras del resumen contra el límite de la revista objetivo.
4. Fig. 1 no se recorre explícitamente en el cuerpo de III.B, solo en el pie de figura.
5. Mover el detalle operativo muy específico de IV.E a un apéndice, si se busca un cuerpo más conceptual (preferencia estilística).
6. Pre-registro público del protocolo (OSF u otro) — valorado por un árbitro, no obligatorio para este tier.

## Dónde los árbitros coinciden (sin discrepancia real)

No hay desacuerdo sustantivo entre los árbitros — ambos señalan, de forma independiente, la misma falla central (falta de ejecución empírica) y la misma laguna de literatura (chaos engineering / Jepsen). Esta convergencia refuerza la confianza en que ambos puntos son prioritarios, no artefactos de la disposición de un árbitro particular.

## Resumen para el autor

El artículo tiene una contribución real y bien organizada (taxonomía + Tabla I + protocolo experimental completamente especificado), y el propio kit `pg-chaos-lab` ya resuelve técnicamente la mayoría de las dudas de reproducibilidad de los árbitros — el trabajo pendiente es mayormente de **redacción** (trasladar al texto lo que el kit ya implementa) más un número menor de correcciones de notación y una decisión de fondo: ejecutar al menos un piloto o reencuadrar honestamente el artículo como marco conceptual + protocolo. Ninguno de los dos árbitros considera el trabajo irrecuperable.
