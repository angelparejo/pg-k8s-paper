# Decisión Editorial — v2-experimental (Fase 3)

**Fecha:** 2026-07-08 · **Tier:** primario iberoamericano en español
**Síntesis de:** árbitro de dominio (STRUCTURAL, 72/100, Mayor) + árbitro de métodos (SKEPTIC, 81/100, Menor).
> Nota: síntesis producida por el orquestador (el agente editor se interrumpió por límite de sesión); ejerce juicio editorial, no promedia puntuaciones.

## Decisión: REVISIÓN MAYOR (con ruta clara y barata a la aceptación)

Los dos árbitros convergen en el diagnóstico de fondo aunque difieren en severidad (Mayor vs Menor). El artículo tiene un hallazgo genuino y verificado (visibilidad ante Kubernetes; asimetría kill-vs-fail ~4.6×; RPO global nulo) y una honestidad de límites ejemplar. **Ninguna objeción es FATAL** y **ninguna MUST requiere nueva experimentación** — todas se resuelven con reencuadre, divulgación y texto. Fijo Mayor (no Menor) porque las correcciones tocan el **reclamo central** (dos árbitros piden rebajar/afilar el "modelo formal validado") y porque hay una **exclusión no divulgada** que es cuestión de integridad; pero la distancia a la aceptación es corta.

## Clasificación de preocupaciones

**FATAL:** ninguna.

**MUST address (ADDRESSABLE, sin experimentos nuevos):**
1. **Reencuadrar el estatus del formalismo** (ambos árbitros). Dejar de reclamar "validación del modelo": presentar S=(O,K,M,D) como **vocabulario/marco descriptivo** y elevar a contribución central el **hallazgo de visibilidad ante Kubernetes** + la **refutación de F2**. Opción fuerte: introducir la visibilidad V(fallo, K) como dimensión de primera clase que *derive* el gradiente F1/F2/F3. Ajustar resumen, contribuciones (§I), §III.C, §VI.C y conclusiones. *(Es el cambio de mayor alcance; puramente editorial.)*
2. **Divulgar en el manuscrito la exclusión del outlier ~80 s de la primera inyección de F2** (métodos, integridad), simétrica con las demás exclusiones ya declaradas, con justificación mecanística (calentamiento/caché) y una nota de ausencia de tendencia con el índice de repetición.
3. **Explicar el mecanismo de RPO=0 en F1 bajo replicación asíncrona** (¿espera de catch-up vs promoción de la réplica más avanzada con lag≈0?), citando código/doc de CNPG; mantener el caveat de carga modesta.
4. **Cerrar lagunas de posicionamiento** (dominio): citar el chaos-testing del propio CloudNativePG (LitmusChaos CI) y delimitar el delta de F1; añadir literatura 2024–2025 de inyección de fallos en Kubernetes; **corregir la caracterización de [9] Avizienis** y posicionar la taxonomía propia frente a ella.
5. **Marcar las afirmaciones comparativas de §IV.A** (Zalando/Patroni) como "esperado según documentación, no medido".

**SHOULD address:**
- Aclarar si, con las 3 instancias co-localizadas, la replicación async cruzó red real o fue intra-nodo (afecta la interpretación de RPO=0 en F1 como prueba de durabilidad de red) — dominio Q5.
- Reportar la Mann–Whitney **exacta** (≈1.1×10⁻⁵) o declarar que es aproximación normal; afirmar que la separación completa hace irrelevante n para F1-vs-F2.
- Depositar el paquete de replicación (manifiestos + scripts + CSV) y corregir el bug ARG_MAX de `parse-verifier.py`.
- Nota de matiz sobre "CP" (CAP); precisar [17] (Jepsen/Alvaro-Tymon); consolidar la repetición de "clúster productivo".
- Fig. 1 en PDF vectorial para LaTeX. **(Ya resuelto: TikZ→PDF.)**

**MAY push back (defendible mantener para este artículo):**
- Sonda de RPO en peor caso (alta concurrencia) y **fallo de nodo real** con detach/attach del CSI: son legítimamente **trabajo futuro** dentro del plan de publicación secuencial (este artículo = CNPG en profundidad; el siguiente = comparativo + fallo de nodo). Comprometerlo explícitamente en Conclusiones basta; no se puede ejecutar en el clúster productivo actual.

## Divergencia entre árbitros — resolución
El SKEPTIC (métodos, 81) considera Menor porque las cifras son sólidas y verificadas; el STRUCTURAL (dominio, 72) considera Mayor por el estatus del formalismo y el posicionamiento. **Tomo partido por el dominio en la severidad**: el reclamo de "modelo formal validado" recorre título, resumen y varias secciones, y su reencuadre no es cosmético; además la laguna del chaos-testing propio de CNPG es una objeción de novedad que un especialista levantará de inmediato. Pero adopto el diagnóstico del SKEPTIC de que **todo es subsanable con texto**: por eso es Mayor "barata", no Mayor estructural.

## Evaluación de tier
- **Tier primario iberoamericano:** con las MUST resueltas, **aceptación probable**. La combinación de hallazgo no obvio + honestidad + estadística correcta encaja bien.
- **Tier secundario (IEEE Access / FGCS / JSS):** **no alcanzable solo con texto.** Gatean el alcance de un operador + un backend + fallo de nodo no medido. IEEE Access sería el techo realista y solo tras ejecutar (en entorno no productivo) el fallo de nodo real y/o un segundo operador. FGCS/JSS quedan para el artículo comparativo. Mantener el plan secuencial.

## Comparación con la ronda adversarial previa (severidad máxima)
| | Dominio | Métodos |
|---|---|---|
| Ronda previa (pre-revisión) | 54 (Reject→Major) | 60 (Major, limítrofe Reject) |
| Esta ronda (post-Nivel 1) | **72 (Mayor)** | **81 (Menor)** |
**Resueltas por el Nivel 1:** replicación asíncrona declarada; verificador y granularidad 0.2 s documentados; sobre-precisión mitigada; F4 reconvertido en lección de instrumentación (sin generalidad); RPO trivial (F2/F3) vs genuino (F1) distinguido; co-localización intra-nodo declarada; estadística añadida (Mann–Whitney, HL, IC de mediana e IC binomial); §V Metodología propia; Raft [25] y engagement con [15]; título y resumen reencuadrados.
**Persisten (esta ronda):** estatus del formalismo (reencuadre); exclusión no divulgada del outlier F2; mecanismo de RPO=0 async; lagunas de literatura (chaos-CI de CNPG, 2025, Avizienis); comparativas de §IV.A como documentación; y, como trabajo futuro, fallo de nodo real + RPO peor caso.
