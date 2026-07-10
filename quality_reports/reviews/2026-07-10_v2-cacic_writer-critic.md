# Informe writer-critic — v2-CACIC (`paper/cacic/main.tex`)

**Fecha:** 2026-07-10 · **Severidad:** ALTA (Execution) · **Venue:** CACIC 2026 / Springer LNCS
**Tipo de paper:** empírico-descriptivo (medición de sistemas; sin pretensión causal formal).

## PUNTUACIÓN: 96 / 100 — SUPERA el umbral de 80. Apto para envío a CACIC (salvedades menores no bloqueantes).

---

## Verificación por categoría

1. **Integridad del argumento tras el recorte — PASA.** Hilo motivación→marco→método→resultado→
   discusión→conclusión intacto; paper autosuficiente sin leer el v1-6. §3 "Marco de Referencia"
   recupera lo necesario (S=(O,K,M,D), I(S), tres invariantes, taxonomía sintética). V(fallo,K) se
   introduce coherentemente. Sin referencias colgantes a la Tabla I eliminada ni a Patroni/Crunchy/
   Raft/k8s-nodes como objetos medidos.
2. **Claims–evidencia (INV-11/22) — PASA (cotejo exhaustivo).** Todas las cifras coinciden con
   `results_summary.md` y la fuente: RTO 7.91/36.75 s; RPO 0; n=10; 0/10, 0/12; U=0, p≈1.1×10⁻⁵,
   rango-biserial 1.00; Hodges–Lehmann 28.96 s; Clopper–Pearson ≤25.9%/≤22.1% (reverificados);
   Spearman ρ≈0.62 (crítico ≈0.65); 4.65×; IQR/rangos/IC; 613 253 ids contiguos; versiones. Sin
   confusión media/mediana.
3. **Anti-salami / cadena de citas — PASA, ejemplar.** La Introducción declara que el marco se
   establece en `[parejo2026]` y que este artículo "no reintroduce ese marco, sino que lo confronta
   con la evidencia". DOI placeholder esperado.
4. **Notación (INV-7) — PASA** (fricción menor C2).
5. **Tablas/figuras (INV-1/2/3) — PASA.** Tabla II con notas completas, booktabs, sin `\hline`;
   Fig. 1 con pie y fuente; PDF vectorial resuelve.
6. **Resumen ≤150 (INV-5) y keywords — PASA** (≈143–145 palabras; 8 keywords).
7. **Formato LNCS / CACIC — PASA.** `llncs.cls`, estructura LNCS, `thebibliography` estilo LNCS; 20
   refs, todas citadas y resueltas. Correcto NO aplicar `working-paper-format.md`.
8. **Escritura (español) — PASA** (retoques C1, C3).

Compilación: PDF de 10 pp presente (no re-ejecutada por el crítico).

## Hallazgos

| ID | Severidad | Cat. | Descripción | Deducción |
|----|-----------|------|-------------|-----------|
| C1 | Media | escritura | Frase run-on en §3 (concentra tres ideas; "que" sin antecedente claro). | −2 |
| C2 | Baja | notación | "se usa M y no C…": C(S) ya no se define tras el recorte; "C" semi-huérfano. | −1 |
| C3 | Baja | escritura | "resultado de mayor fuerza probatoria"/"de mayor peso" ×3 (roza muletilla). | −1 |
| A1 | Advisory | — | `\label{sec:modelo}` definido y nunca referenciado. | 0 |
| A2 | Advisory | compilación | Confirmar 10 pp y sin overfull tras retoques; sustituir DOI real al depositar. | 0 |

**Total: −4 → 96/100.**

## Recomendaciones (aplicadas por el escritor tras el informe)

1. C1: partir la frase de §3 en dos.
2. C2: "—se usa $M$ y no $C$ para no colisionar con la dimensión de Consistencia—".
3. C3: variar dos de las tres ocurrencias.
4. A1: eliminar `\label{sec:modelo}`.
5. A2: recompilar y sustituir DOI al depositar el v1-6.

## Veredicto

El recorte del ~49% preservó la integridad del argumento y la trazabilidad numérica íntegra; el paper
es autosuficiente, la cadena de citas con `[parejo2026]` es honesta y las convenciones LNCS son
correctas. Ninguna deducción es bloqueante. **96/100 — apto para envío a CACIC 2026** tras los retoques
de estilo C1–C3.
