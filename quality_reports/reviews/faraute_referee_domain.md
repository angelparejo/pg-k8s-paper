# Informe de Árbitro de Dominio — Revista FARAUTE (UC/FACYT)

**Fecha:** 2026-08-12
**Manuscrito:** "Análisis multicapa de operadores de PostgreSQL y almacenamiento CSI en Kubernetes: un marco de análisis y un estudio empírico de CloudNativePG bajo fallos inyectados"
**Campo:** Sistemas Distribuidos / Infraestructura Cloud-Native
**Recomendación:** Revisión Menor (al borde de Revisión Mayor)
**Puntuación global:** 80/100

## Resumen
El artículo combina un marco descriptivo ligero —taxonomía + tupla S=(O,K,M,D) + invariantes— con un estudio empírico piloto de CloudNativePG bajo inyección de fallos en un clúster productivo. El hallazgo central —que lo que gobierna el *failover* no es el fallo sino su visibilidad ante Kubernetes, con F2 (*pod-failure*) que NO promueve réplica en contra de lo anticipado— es genuino, bien sustentado por el mecanismo (eventos del operador + identidad del pod/PVC) y honestamente enmarcado como refutación. La ejecución estadística para n=10 es cuidadosa y la declaración de limitaciones es ejemplar. Debilidades: (1) el "marco" hace poco trabajo analítico real —su valor está en el predicado de visibilidad, no en la tupla— y (2) la contribución empírica descansa sobre una topología degenerada (3 instancias co-localizadas en un nodo). Ambas abordables sin nuevos experimentos.

## Puntuaciones por dimensión
| Dimensión | Peso | Puntuación |
|-----------|------|-----------|
| Contribución y novedad | 30% | 76 |
| Posicionamiento en la literatura | 25% | 79 |
| Argumentos sustantivos | 20% | 83 |
| Validez externa y alcance | 15% | 81 |
| Ajuste a la revista | 10% | 88 |
| **Ponderado** | 100% | **80** |

## Comentarios Mayores
1. **Omisión de la referencia canónica: Jepsen / Kingsbury.** El *tx-verifier* es en esencia una versión ligera de la metodología Jepsen (verificación de consistencia/durabilidad bajo particiones). No citarla es una laguna que cualquier árbitro señalará. Añadir a Trabajos Relacionados (cuarta vertiente) y explicitar semejanzas/diferencias.
2. **El marco S=(O,K,M,D) hace poco trabajo analítico; el valor está en V(fallo,K).** La tupla es casi tautológica; las f(·) se declaran no derivadas. Reencuadrar Introducción/Conclusiones para que el predicado de visibilidad sea la contribución conceptual destacada y la tupla quede como andamiaje.
3. **Topología degenerada (3 instancias/1 nodo) socava el valor externo de las magnitudes RTO/RPO.** El hallazgo de visibilidad es robusto, pero las cifras titulares (7,91 s / 36,75 s / RPO=0) provienen de failover intra-nodo. Acotar en resumen y al inicio de Resultados que las magnitudes absolutas no se reclaman representativas de HA real; lo que se sostiene es el contraste F1/F2 y el mecanismo.
4. **El "comportamiento anticipado" que F2 refuta puede parecer hombre de paja.** Anclar la fuente de la expectativa (documentación CNPG / Tabla 1) y reformular el aporte como "confirmación empírica + mecanismo de visibilidad".
5. **El mecanismo del RPO=0 es inferencia no medida (LSN lag no registrado).** Registrar el lag en F1 o dejar más explícito que es hipótesis de mecanismo pendiente.

## Comentarios Menores
1. Referencia CSI débil (URL genérica kubernetes.io); apuntar a la especificación versionada.
2. **Iniciales de autoría erróneas:** Burckhardt es **Sebastian** (S., no M.); Taft (CockroachDB) es **Rebecca** (R., no A.). Revisar Han et al. La memoria del proyecto ya advierte problemas en ~40% de refs.
3. Literatura gris sin fecha (Portworx, simplyblock): etiquetar como industria y fechar acceso.
4. Cota "CP" de F3: precisar que el *primario aislado* deja de aceptar escrituras por inalcanzable (no "el sistema elige C sobre A" en sentido CAP).
5. Figura 3: cajas reconstruidas de cinco números; nota de que no representan densidad empírica completa (n=10).
6. Resumen omite F4 (correcto); coherencia.
7. Carga *pequeña* (no solo "modesta"): pgbench -s10 ~150 MB; central para el RPO=0.
8. Tendencia de calentamiento intra-F2 (Spearman ρ≈0,62): bien reportada; mantener visible.

## Literatura faltante
- **Kingsbury — Jepsen** (y/o Elle/Knossos). **Prioritaria.**
- Especificación CSI formal versionada.
- PostgreSQL: replicación en streaming y `synchronous_commit` (doc oficial).
- Opcional: Kleppmann (DDIA).

## Ruta a la aceptación
Revisión Menor que atienda Mayores 1–3 (Jepsen; reencuadre hacia visibilidad; acotar magnitudes) y los Menores de referencias. Mayores 4–5 deseables pero pueden quedar como limitación + agenda Fase 2. No se requieren experimentos nuevos para el tier primario en español.

**Disposición: Revisión Menor. Puntuación: 80/100.**
