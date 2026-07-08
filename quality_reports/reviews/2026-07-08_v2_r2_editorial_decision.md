# Decisión Editorial — v2-experimental (R&R Ronda 2)

**Fecha:** 2026-07-08 · **Tier:** primario iberoamericano en español
**Árbitros:** Dominio (STRUCTURAL) 72→**83** (Menor) · Métodos (SKEPTIC) 81→**87** (Menor, tendencia a Aceptar)

## Disposición: REVISIÓN MENOR (aceptación condicionada)

No se devuelve a los árbitros. Los 8 mayores originales (5 dominio + 3 métodos) están **resueltos**; los residuos son de redacción/declaración, verificables por el editor. Aplicados los MUST de abajo, el artículo queda **listo para el tier primario**. Ningún árbitro pide nueva experimentación.

## MUST (residuos menores — verificación editorial)
1. Quitar el verbo predictivo suelto en §III.A (coherencia con el reencuadre descriptivo).
2. Suavizar "base formal" en §VIII → "base conceptual/descriptiva".  *(1 y 2 son la misma tensión vista por ambos árbitros.)*
3. Etiquetar el lag≈0 como inferencia no instrumentada en §VI.A (o reportar LSN lag).
4. Añadir *data/code availability statement*.
5. Cerrar el análisis de [27] (qué mide vs el foco de este trabajo).
6. Aclarar el uso informal-operacional de "CP" (nota Tabla II / §VI.A).
7. Confirmar que el build LaTeX usa el PDF de la Fig. 1 y no el `.svg`.

## Estado tras aplicar (esta ronda)
Los 7 MUST se aplicaron: §III.A ("predice"→"anticipa a partir del comportamiento documentado"), §VIII ("base formal"→"base conceptual y descriptiva"), §VI.A (lag≈0 etiquetado "inferencia de mecanismo, no medición"), nueva sección "Disponibilidad de datos y código", §II ([27] analizada con su delta), nota Tabla II ("CP" en sentido operacional, no CAP formal), comentario de build para la Fig. 1 (PDF TikZ). → **listo para someter al tier primario.**

## Tier secundario (IEEE Access / FGCS / JSS): CERRADO
Requiere evidencia nueva reservada al segundo artículo del plan secuencial: fallo de nodo real (detach/attach CSI), comparación multi-operador (Zalando/Patroni, Crunchy) en entorno no productivo, y RPO de peor caso; más traducción al inglés + language editing. Las limitaciones actuales (co-localización, F4 no ejecutable, RPO=0 acotado) están correctamente declaradas y son aceptables *para el tier primario* porque el artículo no reclama más de lo que midió.

## Progreso global
Ronda adversarial previa → Ronda 1 peer review → R&R Ronda 2:
- Dominio: 54 → 72 → **83**.
- Métodos: 60 → 81 → **87**.
- writer-critic interno: 91 → **98**.
