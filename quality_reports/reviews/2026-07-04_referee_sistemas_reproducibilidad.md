# Reporte de Arbitraje — Árbitro Sistemas/Reproducibilidad
**Fecha:** 2026-07-04
**Artículo:** Análisis Sistemático de Operadores de PostgreSQL y Almacenamiento basado en CSI en Kubernetes: Arquitectura, Manejo de Fallos e Implicaciones en la Consistencia
**Recomendación:** Revisión Mayor
**Puntaje global:** 58/100

## Resumen

El artículo propone un marco conceptual (taxonomía, modelo formal S=(O,K,C,D), dimensiones de evaluación e invariantes) para analizar la interacción entre operadores de PostgreSQL y almacenamiento CSI en Kubernetes, junto con un diseño experimental futuro para validarlo. La síntesis de comportamiento por capa en la Tabla I es plausible y en general consistente con el comportamiento por defecto conocido de Kubernetes/Patroni/CloudNativePG, pero el artículo no presenta resultados empíricos, el aparato formal no tiene contenido operacional, y el diseño experimental de la Sección IV.E carece de suficiente detalle operativo (herramienta de inyección de fallos, mecanismo de inyección de latencia sobre SAN/FC, definición de la carga sintética) para que otro ingeniero con un clúster equivalente pueda replicarlo tal como está escrito.

## Puntajes por dimensión

| Dimensión | Peso | Puntaje | Notas |
|-----------|------|---------|-------|
| Contribución y novedad | 30% | 65 | Enfoque integrado razonable, pero no diferenciado explícitamente de comparativas técnicas de industria. |
| Posicionamiento en la literatura | 25% | 55 | Omite literatura central de chaos engineering y verificación de consistencia bajo partición. |
| Argumentos sustantivos / rigor técnico | 20% | 62 | Tabla I internamente consistente y plausible; cita fuentes genéricas para afirmaciones operador-específicas. Modelo formal sin contenido matemático operacional. |
| Validez externa, alcance y reproducibilidad | 15% | 45 | Limitaciones declaradas con honestidad, pero el diseño experimental no es reproducible tal como está redactado. |
| Ajuste a la revista objetivo | 10% | 60 | Rigor narrativo compatible con el tier, pero sin resultado empírico se lee como propuesta de protocolo. |
| **Ponderado** | 100% | **58** | |

## Resultados de los chequeos de cordura

1. **Tiempos y comportamientos de la Tabla I:** plausibles y consistentes con valores por defecto conocidos de Kubernetes (node-monitor-grace-period ≈40s, tolerationSeconds por defecto ≈300s) y con las arquitecturas conocidas de Patroni vs. CloudNativePG. No se detectaron imprecisiones técnicas, pero sí falta de soporte bibliográfico específico por operador.
2. **Plan estadístico vs. diseño factorial:** apropiado (no paramétrico dado el sesgo esperado de RTO/RPO), pero n=10 por celda se presenta sin cálculo de potencia estadística.
3. **Honestidad de la aproximación "fallo de nodo → indisponibilidad sostenida del primario":** declarada explícitamente en el lugar correcto, pero no se articula qué se pierde (p. ej., la latencia de detach/attach del driver CSI de Huawei).

## Comentarios mayores

1. El diseño experimental de IV.E no es reproducible tal como está redactado: no se nombra la herramienta de inyección de fallos ni su versión. — **Qué cambiaría mi opinión:** un apéndice o repositorio de replicación con los manifiestos YAML exactos y el nombre/versión de la herramienta.
2. No se especifica el mecanismo técnico para inyectar 0/20/50/100 ms de latencia de E/S sobre un backend Fibre Channel (SAN), donde `tc netem` no aplica directamente. — **Qué cambiaría mi opinión:** describir el mecanismo explícito y validar que la latencia medida corresponde a la nominal.
3. "Carga sintética continua" no está operacionalizada (herramienta, TPS, mezcla lectura/escritura, tamaño de dataset). — **Qué cambiaría mi opinión:** una tabla de parámetros del generador de carga.
4. Omite literatura central de chaos engineering y verificación de consistencia bajo partición (Jepsen/Kingsbury, Basiri et al.). — **Qué cambiaría mi opinión:** incorporar y discutir estas referencias, posicionando el método propio frente a Jepsen.
5. El modelo formal S=(O,K,C,D) e I(S)=f(O×C×D) carecen de contenido matemático operacional. — **Qué cambiaría mi opinión:** una definición operacional mínima de f, o una reformulación honesta como taxonomía + marco conceptual sin pretensión de formalismo matemático.
6. Ningún resultado empírico — solo un diseño propuesto para trabajo futuro. — **Qué cambiaría mi opinión:** al menos un piloto empírico ejecutado, o una reformulación explícita como "marco conceptual + protocolo experimental".

## Comentarios menores

1. Citar documentación oficial de cada operador, no solo [5]/[14].
2. No se especifica versión de Zalando Postgres Operator ni de Patroni.
3. No se indica el modo de red de Calico (eBPF/iptables), relevante para el escenario de partición.
4. No se menciona sincronización de reloj (NTP) entre nodos y cliente de verificación.
5. No se discute el RTO desde la perspectiva de sesiones de cliente ya conectadas durante la partición.
6. La Fig. 1 no se recorre explícitamente en el cuerpo de III.B.

## Literatura faltante

1. Kingsbury, "Jepsen: A framework for distributed systems verification."
2. Basiri et al., "Chaos Engineering," IEEE Software, 2016.
3. Alquraan et al., "An Analysis of Network-Partitioning Failures in Cloud Systems," OSDI 2018.
4. Yuan et al., "Simple Testing Can Prevent Most Critical Failures," OSDI 2014.
5. Pillai et al. (ALICE), "All File Systems Are Not Created Equal," OSDI 2014.
6. Comparativas técnicas existentes en la industria sobre CloudNativePG vs. Zalando vs. Crunchy.

## Preguntas para los autores

1. ¿Qué herramienta específica de inyección de fallos se usará y qué versión?
2. ¿Cómo se inyectará exactamente la latencia de E/S sobre un volumen SAN/FC?
3. ¿Qué generador de carga se usará para la "carga sintética continua" y con qué parámetros?
4. ¿Se publicará un repositorio de replicación?
5. ¿Existe cálculo de potencia estadística que respalde n=10?
6. ¿Se controla la sincronización de reloj (NTP)?
7. ¿Por qué no se incluye al menos un piloto empírico?

## Lo que el artículo hace bien

1. Declara las limitaciones metodológicas explícitamente y en el lugar correcto.
2. La Tabla I sintetiza de forma útil y técnicamente plausible la responsabilidad por capa.
3. El plan estadístico propuesto está bien elegido dada la distribución esperadamente sesgada de las métricas de recuperación.
