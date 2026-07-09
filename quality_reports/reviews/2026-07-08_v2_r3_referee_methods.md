# Árbitro de MÉTODOS — v2-experimental (Ronda 3)

**Fecha:** 2026-07-08 · **Disposición:** SKEPTIC · **Recomendación:** Revisión Menor (esencialmente Aceptar) · **Puntuación: 89/100** (antes 87)

## Resumen
La Ronda 3 no toca datos ni análisis: cambios de terminología (F1=eliminación / F2=fallo sostenido), formato (Tabla II) y declaración (availability statement). Los tres residuos de la R2 quedan cerrados y la reestructuración de la Tabla II no perdió información metodológica. La precisión pod-kill/pod-failure refuerza la validez de constructo (definición operacional del tratamiento inequívoca a nivel del API). Coherencia numérica confirmada entre resumen, texto y tabla.

## Dimensiones (Base R2 → Ahora)
| Dimensión | Peso | Base R2 | Ahora |
|---|---|---|---|
| Validez de constructo | 30% | 89 | 91 |
| Construcción / replicabilidad | 25% | 86 | 87 |
| Validación | 25% | 85 | 85 |
| Calidad del análisis | 15% | 92 | 93 |
| Preparación para replicación | 5% | 85 | 89 |
| **Ponderado** | 100% | **87** | **89** |

## Residuos R2 — estado
1. lag≈0 como inferencia no instrumentada → **RESUELTO** (§VI.A: "inferencia de mecanismo, no una medición: no se registró el LSN lag").
2. Availability statement → **RESUELTO** (sección "Disponibilidad de datos y código", "a petición").
3. "base formal" en §VIII → **RESUELTO** ("marco descriptivo estructurado", "base conceptual y descriptiva").

## Tabla II — no-pérdida de información
Mediana (definida una vez en la nota), tamaños muestrales n, exclusión del outlier ≈80.5 s (cuerpo, línea 204), mapeo F1–F4→mecanismo (nota) y "CP" operacional: todos presentes y correctos.

## Coherencia numérica
RTO 7.91/36.75 s, razón 4.65×, MW U=0 p≈1.1×10⁻⁵, rango-biserial 1.00, HL 28.96 s, Spearman ρ≈0.62, RPO=0 (IDs 1–613 253 contiguos): intactos y consistentes (INV-11 satisfecho).

## Residuo remanente (no bloqueante, no fijable por escritura)
El techo hacia 90+ lo fija el alcance del piloto (un operador, una categoría de almacenamiento, failover intra-nodo, F4 no ejecutable), honestamente declarado como limitación (§V.A, §VII), no como defecto metodológico.

## Veredicto
87 → **89, Revisión Menor (esencialmente Aceptar):** los tres residuos R2 resueltos, Tabla II reformateada sin pérdida metodológica, coherencia numérica intacta.
