# Árbitro de MÉTODOS — v2-experimental (R&R Ronda 2)

**Fecha:** 2026-07-08 · **Disposición:** SKEPTIC · **Recomendación:** Revisión Menor (tendencia a Aceptar) · **Puntuación: 87/100** (antes 81)

## Resumen
La revisión resuelve genuinamente los 3 mayores por divulgación y reencuadre honestos, sin maquillar. Reverificado por recálculo sobre los CSV: Spearman F2 ρ=0.624≈0.62 (Σd²=62), MW exacta p=2/C(20,10)=1.08×10⁻⁵≈1.1×10⁻⁵, medianas 7.905/36.745, razón 4.65×. Bug ARG_MAX corregido en `parse-verifier.py` (contigüidad server-side). Residuos: el lag≈0 es inferencia no instrumentada, y falta un *availability statement*.

## Dimensiones
| Dimensión | Antes | Ahora |
|---|---|---|
| Validez de constructo | 86 | 89 |
| Construcción/replicabilidad | 80 | 86 |
| Validación | 78 | 85 |
| Calidad del análisis | 88 | 92 |
| Preparación para replicación | 74 | 85 |
| **Ponderado** | **81** | **87** |

## Estado de los 3 mayores
1. Outlier ~80 s no divulgado + efecto de orden → **RESUELTA** (§VI.A divulga ≈80.5 s excluido simétricamente; Spearman ρ≈0.62 no significativa reportada como limitación, "no como ausencia de tendencia"; separación F1–F2 ≈29 s ≫ variación intra-F2).
2. RPO=0 async sin mecanismo → **RESUELTA** (lag≈0 bajo carga modesta, no garantía de diseño; + matiz de co-localización: sin enlace inter-nodo ⇒ no prueba durabilidad de red).
3. "Modelo formal/validación" → **RESUELTA** (reencuadre "caracterización, no validación"; F1 confirmación casi trivial, F2 refutación como núcleo).

Menores: p exacto **RESUELTO**; ARG_MAX **RESUELTO**; independencia **PARCIAL** (el efecto de orden divulgado ES la no-independencia, reconocida como limitación); paquete **PARCIAL** (existe; falta statement).

## Residuos (ninguno bloqueante)
1. El lag≈0 es inferencia, no medición → etiquetarlo o reportar LSN lag.
2. Falta *data/code availability statement* en el manuscrito.
3. "base formal" en §VIII en tensión con el reencuadre descriptivo.

## Veredicto
81 → **87**, **Revisión Menor con tendencia a Aceptar**; residuos de una sola pasada de escritura, sin nueva experimentación.
