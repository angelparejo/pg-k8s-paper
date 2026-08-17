# Informe de Árbitro — MÉTODOS (ciego) — Revista FARAUTE (UC/FACYT)
**Fecha:** 2026-08-12 · **Tipo:** Medición/descriptivo (experimento de sistemas) · **Severidad:** MÁXIMA
**Recomendación:** Revisión MAYOR (limítrofe con Menor) · **Puntaje:** 79/100

## Resumen
Verifiqué a mano TODOS los estadísticos reportados y **son correctos** (Mann–Whitney, Clopper–Pearson, IC distribución-libre, Spearman, Hodges–Lehmann). Los problemas no son de cálculo sino de **inferencia bajo no-independencia**, **precisión incompatible con la granularidad del instrumento**, un **hueco en la semántica del verificador ante reintentos** y **reproducibilidad "a petición"**. Todo resoluble con reanálisis y divulgación de los datos existentes — sin nuevos experimentos.

## Puntajes por dimensión
| Dimensión | Peso | Puntaje |
|-----------|------|---------|
| Validez de constructo (RTO/RPO, tx-verifier) | 30% | 82 |
| Construcción y replicabilidad | 25% | 78 |
| Validación | 25% | 76 |
| Calidad del análisis | 15% | 85 |
| Preparación para replicación | 5% | 65 |
| **Ponderado** | 100% | **79** |

## Verificaciones numéricas (reproducidas, TODAS correctas)
MW U=0 → p exacto bilateral 1,083e-5 ✓ · z=−3,78, p≈1,6e-4 ✓ · rango-biserial 1,00 ✓ · Clopper–Pearson **unilateral** 95%: 25,89% (0/10), 22,09% (0/12) ✓ (NB: etiquetar como unilateral; bilateral daría 30,8%/26,5%) · IC mediana [x₂,x₉] cobertura 97,85% ✓ · Spearman crítico n=10 ≈0,648 > 0,62 → no significativa ✓ · IC/IQR/rango F1 y F2 internamente consistentes ✓ · HL 28,96 s plausible ✓ · razón 4,646≈4,65× ✓.

## Comentarios MAYORES
1. **No-independencia / pseudorreplicación.** 10 repeticiones en serie, mismo nodo/instancias; deriva ρ≈0,62 en F2. MW exacto supone intercambiabilidad → sobreestima precisión. Reencuadrar hacia la **separación completa** + mecanismo, y/o **prueba de permutación por bloques** respetando el orden temporal.
2. **p saturado (piso teórico).** Con separación completa y n=10, el p bilateral mínimo alcanzable ES 1,08e-5; se reporta ese piso. Reconocerlo y trasladar el peso al tamaño de efecto (rango-biserial 1,00; HL 28,96 s) y al mecanismo.
3. **Semántica del verificador ante COMMIT confirmado-pero-no-reconocido.** Si el primario confirmó pero se perdió el ACK, el reintento del mismo BIGINT chocaría con clave duplicada. Falta explicar el manejo (idempotencia/ON CONFLICT/detección de fila) y cuántos casos frontera hubo. Toca directamente el "RPO=0".
4. **Sobre-precisión:** se reportan 0,01 s con granularidad de instrumento ≈0,2 s. Reportar cifras significativas coherentes con ±0,2 s o distinguir resolución de timestamp vs. sondeo.
5. **Exclusiones:** confirmar simetría — ¿se excluyó también la 1.ª inyección de F1? Reportar medianas con y sin exclusión (incluir 80,5 s solo AMPLÍA la brecha → blinda la exclusión).
6. **Reproducibilidad "a petición" insuficiente para FARAUTE.** Datos limpios (10+10+10), manifiestos, tx-verifier y scripts podrían depositarse públicamente (Zenodo/DOI) sin exponer producción. Subiría replicación de 65 a ~90.

## Comentarios MENORES
1. Abstract/Conclusiones: el "RPO nulo" del resumen no lleva las salvedades (asíncrono, carga ligera, co-localización, lag no medido) — añadir calificador breve.
2. F3 IC ultra-estrecho [60,74;60,77] refleja ventana exógena; lo informativo es el excedente de reconexión (~0,75 s). Reencuadrar.
3. Fig. 3: con n=10, preferible dot/strip plot con los 10 puntos crudos frente a boxplot reconstruido.
4. F3: fijar qué n alimenta cada estadístico (0/12 no-promoción vs. RTO sobre 10 fijos).
5. F2 cota inferior: recordarlo también en la nota de la Tabla 2 junto a 36,75 s.

## Preguntas al autor
1. ¿Se excluyó también la 1.ª inyección de F1? Medianas con todos los puntos.
2. Reintento de BIGINT ya confirmado antes del fallo: ¿colisión/ON CONFLICT/detección? ¿cuántos casos frontera por evento?
3. Resolución real del timestamp de COMMIT; ¿estadísticos sobre valores cuantizados a 0,2 s o timestamps finos?
4. ¿Orden de las 10 corridas aleatorizado o secuencial? ¿F1/F2 intercalados o en bloques (confusión orden×escenario)?
5. ¿Los IC de mediana usan exactamente los estadísticos de orden 2.º y 9.º?

**Veredicto: Revisión MAYOR (limítrofe). 79/100.** Ninguna objeción exige nuevos experimentos.
