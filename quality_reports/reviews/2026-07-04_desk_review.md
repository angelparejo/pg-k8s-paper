# Decisión Editorial: Desk Review
**Fecha:** 2026-07-04
**Revista objetivo:** Tier primario (CLEI Electronic Journal / RISTI / Ingeniare / Computación y Sistemas)
**Artículo:** Análisis Sistemático de Operadores de PostgreSQL y Almacenamiento basado en CSI en Kubernetes: Arquitectura, Manejo de Fallos e Implicaciones en la Consistencia (v1-5)

## Decisión: ENVIAR A ÁRBITROS

## Razón

El artículo declara un aporte identificable en una frase clara ("la confiabilidad de las cargas con estado en Kubernetes debe entenderse como un problema inherentemente multicapa"), desglosado en cinco contribuciones concretas y verificables: taxonomía, marco formal, modelo de interacción, invariantes y agenda empírica. Encaja temáticamente sin fricción en el tier objetivo — es exactamente el tipo de artículo de sistemas/infraestructura aplicada, en español, con alcance de ingeniería, que CLEI-EJ, RISTI, Ingeniare y Computación y Sistemas publican regularmente. Se verificó la afirmación de novedad mediante búsqueda web: existen comparaciones prácticas de CloudNativePG vs. Zalando/Patroni (blogs de proveedores, Medium, Portworx), pero no se encontró ningún artículo académico publicado que integre taxonomía + marco formal + tabla de responsabilidades por capa + diseño experimental de inyección de fallos para este par de operadores sobre CSI. No hay paper que "scoopee" la contribución declarada.

No hay una falla fatal de diseño visible desde la introducción. La Tabla I (responsabilidad de detección/recuperación por capa y tipo de fallo) es una síntesis genuina, anclada en comportamiento documentado de tres operadores reales, y la Sección IV.E especifica un protocolo de validación futura con versiones fijadas del stack, tres escenarios de fallo, un barrido paramétrico de latencia y un plan estadístico no paramétrico — suficientemente concreto para que un árbitro de sistemas lo evalúe en términos de reproducibilidad real, no de vaguedad genérica.

Punto de tensión que corresponde resolver en arbitraje, no en desk review: el modelo S=(O,K,C,D) y las funciones R(S), C(S), P(S), I(S) no realizan ningún trabajo analítico derivado — no se resuelve ninguna ecuación, no se deriva ninguna proposición, y las funciones "f(...)" nunca se especifican. Sobre la limitación declarada en la Discusión ("el análisis es de carácter conceptual y no incluye validación empírica directa"): se considera aceptable para el tier objetivo *en la forma en que está presentada* — el autor la declara honestamente, no la oculta, y el artículo no usa lenguaje que sobrevenda resultados no obtenidos. Estas revistas de ingeniería aplicada sí aceptan marcos conceptuales con diseño experimental propuesto como género legítimo, siempre que la contribución conceptual sea sustancial por sí sola. Esa suficiencia es lo que debe testear el arbitraje.

## Asignación de árbitros
- Árbitro 1: Escéptico/Metodológico — evaluará si S=(O,K,C,D), R(S), C(S), P(S), I(S) hacen trabajo analítico real o son notación decorativa; y si un artículo sin experimentos ejecutados es publicable en esta forma para este tier.
- Árbitro 2: Sistemas/Reproducibilidad — evaluará si el diseño experimental de IV.E es reproducible tal como está descrito, si la aproximación del fallo de nodo es válida, si la limitación a almacenamiento SAN/FC homogéneo está bien tratada, y si la Tabla I es ejecutable/verificable.
