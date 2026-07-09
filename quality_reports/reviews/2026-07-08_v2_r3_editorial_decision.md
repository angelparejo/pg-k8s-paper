# Decisión Editorial — v2-experimental (Ronda 3, re-evaluación)

**Fecha:** 2026-07-08 · **Tier:** primario iberoamericano en español
**Motivo:** re-evaluación tras los cambios de formato/terminología de la sesión DOCX IEEE (commit 623aad8).

## Puntuaciones (Base R2 → Ronda 3)
| Evaluador | Peso | Base R2 | Ronda 3 | Δ |
|---|---|---|---|---|
| Árbitro de dominio | 12,5% | 83 | **85** | +2 |
| Árbitro de métodos | 12,5% | 87 | **89** | +2 |
| writer-critic | 10% | 98 | **98** | 0 |
| Promedio de árbitros (calidad del paper) | 25% | 85,0 | **87,0** | +2 |

**Agregado ponderado sobre componentes evaluados** (theorist excluido por ser paper descriptivo; strategist/coder/librarian/explorer/verifier no re-evaluados este ciclo → excluidos y renormalizados): **≈ 88,7 → ≈ 90,2**.

## Disposición: REVISIÓN MENOR (aceptación condicionada) — listo para tier primario
Los cambios de la sesión (terminología K8s, promoción explícita, disponibilidad de datos, Tabla II) resolvieron los residuos de la R2 y mejoraron dominio (+2) y métodos (+2). Ningún evaluador pide nueva experimentación. El techo hacia 95 lo fija el alcance del piloto (un operador, una categoría de almacenamiento, failover intra-nodo, F4 no ejecutable), honestamente declarado como limitación.

## MUST (residuo accionable único)
1. **Corregir la etiqueta "(regla de tres)" en §VI (línea 208)** → es la cota exacta de Clopper–Pearson (los valores ≤25.9%/≤22.1% ya son correctos). Cambio de una palabra.

## SHOULD (opcionales)
- Marcar "framework" (§ línea 43) como los demás tecnicismos, o glosarlo.
- Considerar una media frase en el resumen anticipando F4, o dejarlo.
- Para el tier secundario (inglés): depósito público con DOI (Zenodo) del paquete de ejecución sin datos sensibles.

## Compuertas de calidad
- Todos los componentes evaluados ≥ 80 ✓
- Agregado ≈ 90 → supera Commit (80) y PR (90); NO alcanza Submission (95, interno).
- Verdicto editorial de aptitud: **listo para someter al tier primario** (Revisión Menor), independientemente de la compuerta interna de 95.

## Progreso global (v2-experimental)
- Dominio: 54 → 72 → 83 → **85**
- Métodos: 60 → 81 → 87 → **89**
- writer-critic: 91 → 98 → **98**
