# Informe writer-critic — Conversión Faraute
**Archivo:** `paper/faraute/main.tex` (19 pp, compila limpio) · **Fase:** Ejecución · **Severidad:** ALTA
## PUNTAJE: 70/100 — NO SUBMITTABLE (bajo el gate 80)

Calidad intrínseca alta: fidelidad numérica perfecta, 27/27 citas autor-año correctas, orden cronológico de multi-citas correcto, todas las refs cruzadas resuelven, cumplimiento Faraute correcto en puntos 1-7, 10-12. Bloquea el envío: límite de páginas + leyendas de tabla.

## Hallazgos
| # | Sev. | Hallazgo | Guía/INV | Ded. |
|---|------|----------|----------|------|
| 1 | **BLOQUEANTE** | 19 pp vs. máximo 12 (artículo científico). Requiere recorte sustancial. | Tipos (a) | −15 |
| 2 | **MAYOR** | Leyendas de AMBAS tablas ARRIBA; Faraute punto 8 exige "debajo". | Punto 8/INV-1 | −6 |
| 3 | MENOR | Resumen ≈151 palabras, marginalmente sobre 150. | Punto 5/INV-5 | −3 |
| 4 | MENOR | babel-spanish omitido → sin silabeo español, justificación degradada. | Puntos 1-3 | −2 |
| 5 | MENOR | Fig. 3 y 4 (datos) sin nota "Fuente:". Figs 1,2,5 son esquemas, no la requieren. | INV-2 | −2 |
| 6 | MENOR | Overfull hbox 39,95 pt en Ec. de visibilidad (línea 379). | Punto 11 | −1 |
| 7 | ADVIS. | Grises/300 dpi no verificable desde .tex; originales a color. | Punto 9 | −1 |
| 8 | ADVIS. | `Taft, A.` → autora principal CockroachDB es Rebecca Taft (R.). | INV-11 | 0 |
| 9 | ADVIS. | Refs de sección a mano ("Sección~5.2") en vez de \ref; frágil. | práctica | 0 |

## Fidelidad (eje B) — 100% coincidente e internamente consistente
Verificadas todas las cifras (RTO 7,91/36,75; 4,65×; n=10; 0/12; 613 253; MW U=0 p≈1,1e-5 z=−3,78; ρ≈0,62; HL 28,96; CP ≤25,9%/≤22,1%; cobertura 97,9%; IQR/rangos/IC F1 y F2; 80,5 s; 149/300 s; 60,75 s). Conversión correcta de punto→coma decimal española. Las 27 citas IEEE mapean correctamente a autor-año. Bibliografía alfabética con formato Faraute. Palabras clave en orden alfabético (mejora sobre la fuente).

Desviaciones aceptables: resumen omite frase final de Fase 2 (por límite 150; contenido preservado en Discusión/Conclusiones); eliminado material RITC (cabecera Congreso/PÓSTER, DOI ritc); Contribuciones/Fondos/Conflictos/Disponibilidad consolidados en Agradecimientos.

## Prioridades de corrección
1. **Recortar a ≤12 pp** (bloqueante). Candidatos: condensar §4 (muy expositiva) y §7 (reitera limitaciones); mover detalle metodológico fino a notas. → Escalar al usuario/Orchestrator qué sacrificar.
2. Mover leyendas de Tabla 1 y 2 DEBAJO.
3. Recortar 1 frase del resumen (<150).
4. Reintroducir babel/spanish (silabeo); corregir desborde Ec. visibilidad.
5. Confirmar grises 300 dpi; añadir "Fuente:" a Fig. 3 y 4; corregir inicial de Taft.
