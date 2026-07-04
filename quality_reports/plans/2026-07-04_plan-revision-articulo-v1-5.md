# Plan de Revisión — Artículo v1-5

**Estado:** DRAFT (pendiente de aprobación del usuario)
**Fecha:** 2026-07-04
**Fuente:** `quality_reports/reviews/2026-07-04_editorial_decision.md` (Revisión Mayor, sin objeciones FATALES)
**Alcance:** Este documento es un plan de ruteo. NO se ha editado el artículo todavía.

---

## 0. Hallazgo estructural antes de rutear

De los 16 ítems (8 MUST + 8 SHOULD), **solo 1 depende realmente de una decisión previa** (MUST-1, la ejecución de un piloto vs. el reencuadre del framing). Los otros 15 son correcciones mecánicas o de redacción aplicables ya, sin ejecutar nada en el clúster, y no cambian según qué rama se elija en MUST-1 — **siempre y cuando** se conserve la Sección IV.E con su nivel actual de detalle (ambos árbitros valoraron esa especificidad como una fortaleza; eliminarla del todo sería una tercera opción no recomendada). Esto significa que el trabajo puede empezar de inmediato en paralelo a que decidas MUST-1; la decisión solo bloquea el ajuste final de Resumen, Introducción (contribución 5), Discusión y Conclusiones.

---

## 1. Ruteo de los 8 MUST

| # | Objeción | Sección(es) del artículo | Tipo | Acción concreta |
|---|----------|---------------------------|------|------------------|
| M1 | Ausencia de validación empírica ejecutada | Resumen · I. Introducción (contribución 5) · IV.E (título/framing) · V. Discusión (limitaciones) · VI. Conclusiones (trabajo futuro) | **DEPENDE de la decisión piloto vs. reencuadre** | Ver Sección 3 — esta es la decisión que hay que tomar antes de tocar estos cinco puntos del texto. |
| M2 | Nombrar Chaos Mesh 2.7.x y mecanismos por escenario (PodChaos F1/F2, NetworkPolicy Calico F3, IOChaos F4) | IV.E (Diseño experimental propuesto) | **Mecánica — aplicable ya** | Insertar un párrafo o tabla que nombre la herramienta y el primitivo de Chaos Mesh usado por cada escenario, tomado directamente de `paper/replication/pg-chaos-lab.zip` (README.md, `40-experiments/`). No requiere ejecutar nada. |
| M3 | Aclarar que la latencia de E/S (F4) se inyecta vía FUSE dentro del pod y no toca la SAN real | IV.E | **Mecánica — aplicable ya** | Añadir una frase explícita: la inyección es a nivel de aplicación (FUSE), no altera el path de la SAN Huawei ni afecta a otros consumidores del arreglo — tomado literalmente del comentario en `40-experiments/f4-iolatency-*.yaml`. |
| M4 | Operacionalizar "carga sintética continua" (pgbench + parámetros) | IV.E | **Mecánica — aplicable ya** | Nombrar pgbench y los parámetros ya fijados en `30-workload/pgbench-*.yaml` (`-c 4 -j 2 -T 60` en bucle, escala `-s 10`). |
| M5 | Especificar versión de Zalando Postgres Operator / Patroni | IV.E | **Mecánica — aplicable ya** | Añadir "v1.13.x + Spilo 16" junto a la versión ya fijada de CloudNativePG 1.28.0, tomado de `pg-chaos-lab/README.md`. |
| M6 | Colisión de notación: C usado para almacenamiento (S=(O,K,C,D)) y para consistencia (C(S)) | III.B (Modelo del sistema) · III.C (Dimensiones de evaluación) | **Mecánica — aplicable ya** | Renombrar la dimensión de consistencia (p. ej. `Cn(S)` o `Cons(S)`) en III.C y verificar que no se reintroduzca la colisión en IV.C/V/VI. |
| M7 | K ausente de I(S)=f(O×C×D) pese a ser miembro de S y actor central en Tabla I | III.C (definición de I(S)) | **Mecánica — aplicable ya** | Decisión de redacción menor: o se reescribe I(S)=f(O×K×C×D) con una frase que explique el rol de K, o se justifica explícitamente por qué K queda fuera. No requiere experimentos, solo una elección de notación coherente con la Tabla I. |
| M8 | Incorporar literatura de chaos engineering / verificación de consistencia bajo partición | II. Trabajos Relacionados · Referencias | **Mecánica — aplicable ya** | Añadir Basiri et al. (2016), Kingsbury/Jepsen, Alquraan et al. (2018, OSDI) a Trabajos Relacionados (un párrafo nuevo) y a la lista de Referencias. |

---

## 2. Ruteo de los 8 SHOULD

| # | Objeción | Sección(es) del artículo | Tipo | Acción concreta |
|---|----------|---------------------------|------|------------------|
| S1 | Dar contenido operacional a f(·), o declarar que la notación es organizativa | III.C (Dimensiones de evaluación) | **Mecánica — aplicable ya** (esfuerzo variable) | Opción mínima (una frase: "estas funciones son organizativas, no operacionales, y no se resuelven en este trabajo") o opción completa (derivar una desigualdad/proposición, p. ej. una cota del RPO en función de la latencia de replicación). Ambas opciones son redacción/teoría, no requieren el clúster. |
| S2 | Justificar n=10 por combinación (potencia estadística) | IV.E | **Mecánica — aplicable ya** | Añadir cálculo de potencia o referencia a un estudio comparable que valide n=10 para Mann-Whitney/Kruskal-Wallis con este tamaño de efecto esperado. Es planificación estadística, no ejecución. |
| S3 | Discutir qué se pierde al aproximar "fallo de nodo" con indisponibilidad sostenida del primario | IV.E (donde ya se declara la aproximación) · V. Discusión (limitaciones) | **Mecánica — aplicable ya** | Añadir 2-3 frases sobre la latencia de detach/attach del driver CSI Huawei que no se captura con esta aproximación. |
| S4 | Citar documentación oficial de cada operador en la Tabla I, no solo [5]/[14] | IV.C (Tabla I) | **Mecánica — aplicable ya** | Añadir referencias a la documentación oficial de CloudNativePG, Patroni y Crunchy PGO como fuente de cada fila operador-específica. |
| S5 | Conectar al menos una fila de la Tabla I con la notación formal | III.B/III.C (notación) · IV.C (Tabla I) | **Mecánica — aplicable ya** | Anotar una fila de la Tabla I (p. ej. "Fallo del pod primario") con su instancia de I(S), mostrando cómo O, K y C interactúan en ese caso concreto. Depende de tener ya resueltos M6/M7 (mismo bloque de trabajo, hacerlos juntos). |
| S6 | Declarar sincronización de reloj (NTP) entre nodos y cliente de verificación | IV.E | **Mecánica — aplicable ya** | Una frase declarando el mecanismo de sincronización (o su ausencia, como limitación) dado que RTO se mide en el orden de segundos. |
| S7 | Aclarar por qué Crunchy está en la taxonomía pero no en el experimento | III.A (Taxonomía, referencia cruzada) · IV.E (alcance del diseño) | **Mecánica — aplicable ya** | Añadir una frase en III.A ("se incluye por completitud taxonómica; ver alcance experimental en IV.E") y en IV.E justificar por qué se seleccionaron los dos operadores más contrastantes en su mecanismo de coordinación. |
| S8 | Comparar el aporte frente a comparativas técnicas ya publicadas en la industria | II. Trabajos Relacionados (o nuevo párrafo en Introducción) | **Mecánica — aplicable ya** | Añadir un párrafo que reconozca las comparativas técnicas no académicas existentes (blogs EDB/Ongres/Portworx, charlas KubeCon) y explicite qué aporta este artículo que ellas no ofrecen. |

---

## 3. La decisión pendiente: piloto empírico vs. reencuadre del framing (M1)

Esta es la única decisión que bloquea el resto. Dos caminos:

### Camino (a) — Ejecutar un piloto empírico
Usar el kit `paper/replication/pg-chaos-lab.zip`, ya completamente implementado, para correr al menos una combinación operador × escenario (idealmente F1 en ambos operadores, el escenario de menor riesgo) y reportar RTO/RPO reales.

**Qué cambia en el texto si se elige este camino:**
- Resumen: pasar de "propone una agenda empírica" a mencionar el hallazgo piloto.
- I. Introducción (contribución 5): ajustar de "brechas que justifican una futura evaluación" a "validación piloto que confirma/refina el modelo."
- IV.E: cambiar tiempo verbal de propuesto ("se propone", "se contemplan") a ejecutado ("se ejecutó", "se aplicó"), y añadir una subsección de Resultados (nueva, antes de Discusión) con las cifras reales.
- V. Discusión: la limitación "no incluye validación empírica directa" deja de aplicar en su forma actual — reformular como "validación parcial; extensión completa queda como trabajo futuro."
- VI. Conclusiones: mismo ajuste que Discusión.
- **Costo:** requiere tiempo de laboratorio (ejecutar `run-experiment.sh` n≥10 veces por combinación, `parse-verifier.py`, `analyze.py`) antes de poder cerrar esta rama.

### Camino (b) — Reencuadrar el framing (recomendado si no hay tiempo de laboratorio ahora)
Mantener el artículo como marco conceptual + protocolo experimental completamente especificado (sin ejecutar nada), pero sin dar a entender que hay resultados inminentes.

**Qué cambia en el texto si se elige este camino:**
- Título: revisar si "Análisis Sistemático" sigue siendo honesto, o si conviene un matiz (p. ej. "Marco Sistemático de Evaluación..." en vez de "Análisis Sistemático de Operadores...") — decisión de estilo, no obligatoria si el resto del texto ya dis­tingue claramente entre lo analizado (taxonomía, Tabla I) y lo propuesto (IV.E).
- Resumen: la redacción actual ("propone una agenda empírica para una validación posterior") ya es compatible con este camino — probablemente no requiere cambios.
- V. Discusión / VI. Conclusiones: la declaración actual de limitación ya es honesta; solo reforzar que el protocolo está completamente especificado y listo para ejecutarse (dato a favor: el kit `pg-chaos-lab` ya existe), sin prometer fecha de ejecución.
- **Costo:** ninguno en tiempo de laboratorio; es trabajo de redacción únicamente.
- **Importante:** este camino NO significa eliminar la Sección IV.E — ambos árbitros valoraron su nivel de detalle como una fortaleza real. Reencuadrar ≠ recortar el protocolo.

### Recomendación operativa (no vinculante)
Dado que M2–M8 y los 8 SHOULD no dependen de esta decisión, se pueden completar todos ahora. La decisión de M1 se puede tomar al final, cuando el resto del artículo ya esté corregido — en ese punto el único trabajo restante será: (a) correr el piloto y añadir resultados, o (b) dar los últimos retoques de framing en Resumen/Título/Discusión/Conclusiones. Esto evita bloquear 15 de 16 ítems por una decisión que no es urgente resolver primero.

---

## 4. Corrección de afiliación (DE ESTILO, fuera de MUST/SHOULD)

| Ítem | Sección | Tipo | Acción concreta |
|------|---------|------|------------------|
| Afiliación del autor | Encabezado / metadatos del artículo | **Mecánica — aplicable ya** | El artículo dice "Angel A. Parejo R. — Caracas, Venezuela". Corregir a "Angel A. Parejo R. — Valencia, Estado Carabobo, Venezuela" (y añadir afiliación institucional "Universidad de Carabobo" si el formato de la revista objetivo lo requiere), consistente con `CLAUDE.md` y `README-PROYECTO.md`. |

---

## 5. Orden de ejecución sugerido

1. **Fase mecánica (ahora, sin decisión pendiente):** M2, M3, M4, M5, M6, M7, M8, S1–S8, corrección de afiliación. Se pueden agrupar por sección para minimizar pasadas sobre el documento:
   - Una pasada por III.B/III.C (M6, M7, S1, S5-parcial)
   - Una pasada por IV.C — Tabla I (S4, S5-parcial)
   - Una pasada por IV.E (M2, M3, M4, M5, S2, S3, S6, S7-parcial)
   - Una pasada por II. Trabajos Relacionados + Referencias (M8, S8)
   - Una pasada por III.A (S7-parcial, referencia cruzada)
   - Corrección de metadatos (afiliación)
2. **Decisión M1** (piloto vs. reencuadre) — a tomar cuando el resto esté listo.
3. **Fase final dependiente de M1:** ajustar Resumen, Introducción (contribución 5), Discusión, Conclusiones, y (si camino (a)) ejecutar el piloto y redactar la sección de Resultados.

---

## Siguiente paso

Este plan queda a la espera de tu aprobación. Ningún archivo del artículo ha sido modificado. Cuando apruebes, procedo con la Fase mecánica (punto 1) primero, dejando M1 para el final tal como se recomienda arriba — o en el orden que prefieras.

---

## Estado (actualizado 2026-07-04, fin de la fase mecánica)

**Trabajo realizado sobre `articulo_angelparejov1-6.md`** (copia de trabajo; `articulo_angelparejov1-5.docx` permanece intacto):

| # | Ítem | Estado |
|---|------|--------|
| M2 | Nombrar Chaos Mesh 2.7.x + mecanismos por escenario | ✅ Resuelto |
| M3 | Aclarar FUSE/SAN en F4 | ✅ Resuelto |
| M4 | Operacionalizar pgbench + parámetros | ✅ Resuelto |
| M5 | Versión Zalando/Patroni (v1.13.x + Spilo 16) | ✅ Resuelto |
| M6 | Colisión de notación C (renombrado a M, "medio de almacenamiento") | ✅ Resuelto |
| M7 | K incluido en I(S)=f(O×K×M×D), con justificación conceptual | ✅ Resuelto |
| M8 | Literatura de chaos engineering / Jepsen / partición de red | ✅ Resuelto ([16]-[18] en el texto y en `Bibliography_base.bib`) |
| **M1** | **Validación empírica ejecutada vs. reencuadre del framing** | **⏳ PENDIENTE — única decisión de fondo que queda** |
| S1 | Contenido operacional de f(·) / declaración de que son organizativas | ✅ Resuelto (declaración honesta) |
| S2 | Justificar n=10 | ✅ Resuelto (honesto: sin cálculo de potencia formal) |
| S3 | Qué se pierde en la aproximación de fallo de nodo | ✅ Resuelto (conectado con Tabla I) |
| S4 | Citar documentación oficial por operador en Tabla I | ✅ Resuelto ([19]-[21]) |
| S5 | Conectar una fila de la Tabla I con la notación formal | ✅ Resuelto (fila "Fallo del pod primario") |
| S6 | Sincronización de reloj (NTP) | ✅ Resuelto |
| S7 | Alcance: por qué Crunchy está en la taxonomía pero no en el experimento | ✅ Resuelto (III.A + IV.E) |
| S8 | Comparación con literatura técnica de industria | ✅ Resuelto ([22]-[23]) |
| — | Corrección de afiliación (Caracas → Valencia, Estado Carabobo — Universidad de Carabobo) | ✅ Resuelto |

**Total: 7/7 MUST mecánicos + 8/8 SHOULD + afiliación = 16/16 ítems mecánicos resueltos. Solo falta M1.**

**Pendiente menor (cosmético, no bloqueante):** las referencias [19]-[21] (documentación web) llevan `[Accessed: pendiente]` en vez de una fecha real en formato IEEE — corregir en la fase de conversión a LaTeX/formato final, cuando también se resuelva la tarea pendiente de volcar las referencias [1]-[15] al `.bib` (ya anotada en `Bibliography_base.bib`).

---

## Decisión M1 (2026-07-04): Ruta B — reencuadre, publicación secuencial

**Decisión:** el acceso al clúster productivo es incierto, por lo que se descarta ejecutar un piloto ahora. Se opta por Ruta B (reencuadre honesto del framing) para poder someter la versión conceptual al tier primario sin más demora, dejando la validación empírica para un segundo artículo.

**Estrategia de publicación secuencial:**

1. **`articulo_angelparejov1-6.md` (versión conceptual, reencuadrada)** — se somete ahora al tier primario en español (CLEI Electronic Journal / RISTI / Ingeniare / Computación y Sistemas). Contribución: taxonomía, modelo formal S=(O,K,M,D), invariantes, y protocolo experimental completamente especificado y reproducible (Sección IV.E). Sin resultados empíricos — declarado explícitamente en título, resumen, introducción, discusión y conclusiones.
2. **Segundo artículo futuro (con piloto empírico)** — cuando el acceso al clúster productivo lo permita. Tomará esta versión conceptual como base, ejecutará el protocolo de IV.E (ya implementado en `paper/replication/pg-chaos-lab.zip`), y añadirá una sección de Resultados con RTO/RPO reales.
3. **Regla de citación obligatoria:** el segundo artículo DEBE citar explícitamente al primero (este) como el trabajo que establece el marco, el modelo y el protocolo que se está validando — para evitar cualquier lectura de publicación duplicada o "salami slicing". La contribución de cada uno debe quedar delimitada sin solapamiento: el primero es marco + protocolo; el segundo es validación empírica + resultados + refinamiento del modelo a partir de la evidencia.

**Nota:** esta estrategia queda documentada aquí (plan del proyecto), no en el texto del artículo — el artículo no menciona un "segundo artículo futuro" para evitar autocitas a trabajo inexistente.

---

## Cierre del plan (2026-07-04): v1-6-conceptual completa

**Título final aplicado:** "Hacia un Análisis Multicapa de Operadores de PostgreSQL y Almacenamiento CSI en Kubernetes: Taxonomía, Modelo Formal y Protocolo Experimental Reproducible"

Reencuadre de framing (Ruta B) aplicado y verificado sin residuos de lenguaje de resultados:
- Título, Resumen (152 palabras), Introducción (contribución final + declaración de alcance conceptual/metodológico), Discusión (3 ajustes de palabra: "resultados"→"análisis"), IV.D (1 ajuste), Conclusiones (protocolo como contribución principal + trabajo futuro reformulado como "ejecución", no "diseño").
- Secciones técnicas (III, IV.A-E cuerpo, Tabla I, notación) sin tocar salvo los ajustes de palabra explícitamente autorizados.

**PLAN CERRADO.** `articulo_angelparejov1-6.md` es la versión conceptual completa, lista para conversión a LaTeX y envío al tier primario. `articulo_angelparejov1-5.docx` permanece intacto como versión histórica.
