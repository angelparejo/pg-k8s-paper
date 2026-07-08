# Revisión por pares simulada — v2-experimental · Fase 1: Revisión de Escritorio

**Fecha:** 2026-07-07 · **Artículo:** *Análisis Multicapa de Operadores de PostgreSQL y Almacenamiento CSI en Kubernetes: un Marco de Evaluación y su Validación Empírica en CloudNativePG bajo Fallos Inyectados* · **Autor:** Angel A. Parejo R. (Universidad de Carabobo)
**Tier objetivo:** primario iberoamericano en español (CLEI EJ / RISTI / Ingeniare / Computación y Sistemas). Sin perfil de revista de sistemas en `journal-profiles.md`; calibrado genéricamente vía `domain-profile.md`. **Indexación/cuartil pendiente de verificar por el autor antes de someter.**

## Decisión: ENVIAR A ÁRBITROS

Ningún criterio de desk-reject se cumple:
1. **Ajuste:** correcto — estudio empírico de sistemas cloud-native sobre clúster productivo + marco conceptual.
2. **Contribución clara:** marco de evaluación multicapa (taxonomía + S=(O,K,M,D) + invariantes) + validación empírica en CNPG; hallazgo central no obvio = el failover lo determina la **visibilidad del fallo ante Kubernetes**, con gradiente de tres comportamientos (kill→promueve 7.91 s; failure→recrea en sitio 36.75 s; partición→CP). El contraste ~4.6× kill-vs-fail es genuino y publicable.
3. **Sin fallo fatal visible:** las tres limitaciones (un operador, un backend SAN/FC, fallo de nodo no testeable por co-localización en tcolp293) están declaradas con honestidad; F2 enmarcado como cota inferior; F4 reconvertido en hallazgo de instrumentación.
4. **Umbral:** en rango para el tier primario (borderline para el secundario FGCS/JSS por un operador + n=10 + sin fallo de nodo real).
5. **Sin scoop:** existe chaos-testing de CNPG (LitmusChaos CI) y comparativas de industria [22][23], pero ninguno propone el marco formal + invariantes ni aísla el mecanismo de visibilidad.

**Verificación de cifras (INV-11/22):** todas trazan a las fuentes de verdad (C1–C21). Sin discrepancias.
**Señalamiento para árbitros:** el paper no cita el chaos-testing del propio proyecto CNPG.

## Asignación de árbitros (Fase 2)
- **Árbitro 1 (Domain):** disposición **STRUCTURAL**. Crítico: exigir que el modelo formal *prediga*, no solo organice. Constructivo: premia trabajos que cambian cómo se piensa el problema.
- **Árbitro 2 (Methods):** disposición **SKEPTIC**. Crítico: sospecha de resultados demasiado limpios (RPO=0), quiere peor caso. Constructivo: crédito al reconocimiento honesto de límites.

Combinaciones alternativas para re-tirar: Domain=POLICY (generalizabilidad), Methods=MEASUREMENT (granularidad del instrumento).
