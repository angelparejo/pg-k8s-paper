# Informe de Árbitro de MÉTODOS — v2-experimental (Fase 2)

**Fecha:** 2026-07-07 · **Disposición:** SKEPTIC · **Tier:** primario iberoamericano
**Recomendación:** Revisión Menor · **Puntuación: 81/100**

## Resumen
Mide RTO/RPO de CloudNativePG bajo tres modos de fallo; hallazgo contraintuitivo bien fundamentado (F1 ~7.9 s vs F2 ~36.75 s, ~4.6×). **Verifiqué todas las cifras inferenciales contra `data/cleaned/*.csv` y reconcilian exactamente:** F1 mediana 7.905≈7.91 (media 7.693≈7.69), F2 36.745≈36.75, separación completa (min F2 35.51 > max F1 8.17 → U=0 y rank-biserial 1.00 son EXACTOS), razón 4.65×, IC distribución-libre = x(2)/x(9), cotas regla de tres correctas. Entré con prior escéptico (RPO=0 triple, n=10 sin potencia); el artículo desactiva casi toda la objeción con reconocimiento honesto de alcance — salvo una exclusión de outlier no divulgada en el manuscrito.

## Puntuaciones por dimensión
| Dimensión | Peso | Punt. |
|---|---|---|
| Validez de constructo | 30% | 86 |
| Construcción y replicabilidad | 25% | 80 |
| Validación | 25% | 78 |
| Calidad del análisis | 15% | 88 |
| Preparación para replicación | 5% | 74 |
| **Ponderado** | 100% | **81** |

## Chequeos de sanidad
- Cifras reconcilian con los CSV (verificado). Separación completa ⇒ U=0/rank-biserial=1.00 exactos; **n=10 sobra para F1-vs-F2** (la objeción de potencia queda desactivada para ese contraste).
- Gradiente kill/failure/partición mecanísticamente coherente y respaldado por eventos del operador.
- "Demasiado limpio" (RPO=0 triple): parcialmente resuelto por el propio artículo (F2/F3 trivial; solo F1 prueba durabilidad, bajo async, con caveat de carga).

## Comentarios mayores
1. **Exclusión NO divulgada del outlier ~80 s de la primera inyección de F2.** El manuscrito divulga las exploratorias de F3 y el id espurio, pero **no** el ~80 s excluido; la asimetría es llamativa y es evidencia de un **efecto de calentamiento/orden** que roza la independencia de Mann-Whitney. *Cambiaría mi opinión:* divulgar el ~80 s con justificación mecanística (caché fría, pull de imagen) tratándolo simétricamente; reportar ausencia de tendencia con el índice de repetición (o aleatorizar el orden).
2. **RPO=0 en F1 bajo async: falta el mecanismo, no solo el caveat.** Bajo async un `pod-kill` *debería* poder perder WAL no propagado; 10/10 sin pérdida exige explicación (¿CNPG espera catch-up o promueve la réplica más avanzada con lag≈0 por carga ligera?). *Cambiaría mi opinión:* explicar el mecanismo citando código/doc; idealmente sonda de RPO peor-caso (más clientes, WAL sostenido). Declararlo como límite de constructo si (b) no es viable.
3. **"Modelo formal" = vocabulario no falsable; "validación" promete de más.** F1/F3 "confirman" predicciones casi tautológicas; el único elemento con fuerza probatoria real es la **refutación de F2**. *Cambiaría mi opinión:* afilar ≥1 invariante a predicción cuantitativa falsable, o reencuadrar la parte empírica como caracterización/descubrimiento con la refutación de F2 como núcleo.

## Comentarios menores
1. p-valor por aproximación normal (z=−3.78, p≈1.6×10⁻⁴); el exacto bilateral da ≈1.1×10⁻⁵. Declarar que es aproximación o reportar el exacto.
2. Bug ARG_MAX de `parse-verifier.py` (RPO por `IN(…117k ids…)`); workaround de contigüidad válido, pero corregir antes del depósito.
3. Justificar exchangeabilidad/independencia entre corridas (secuenciales, ~2.5 min).
4. F3 "RTO = duración de partición": bien manejado (excedente ~0.75 s = reconexión; sin sobre-precisión).
5. Paquete de replicación no depositado (`paper/replication/` "not started").

## Preguntas para el autor
1. ¿CNPG espera catch-up antes de promover o promueve la réplica más avanzada? (determina si RPO=0 es propiedad del mecanismo o artefacto de lag≈0).
2. ¿Valor exacto y justificación de la primera inyección de F2 excluida? (debe ir al manuscrito).
3. ¿Se aleatorizó el orden de las inyecciones o fueron secuenciales?

**Nota de progreso (60→81):** la revisión resolvió de forma genuina lo que un árbitro de métodos marcaría (async declarada C19, verificador+granularidad 0.2 s C21, F4 reconvertido, RPO trivial vs genuino). Los tres mayores restantes son subsanables con divulgación y texto — no requieren nueva experimentación (salvo la sonda de RPO peor-caso, que es fortalecimiento, no bloqueo).
