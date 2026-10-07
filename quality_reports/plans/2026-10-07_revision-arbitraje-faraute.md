# Revisión mayor FARAUTE — puntos 2 y 3 aplicados

**Estado:** COMPLETADO (compila: 12 pp, 0 errores, 0 overfull, 0 refs sin resolver)
**Base congelada:** tag `enviado-faraute-2026-09-29`, `articulo_ENVIADO_2026-09-29.pdf`
**Fichero:** `paper/faraute/main.tex`

## Decisiones del autor
1. Marco formal: **eliminar** las Ecs. 2–5; se conserva S=(O,K,M,D) como vocabulario en prosa.
2. F2: **reencuadrar sin repetir** (testbed desmontado); re-ejecución comprometida para la Fase 2.
3. Título: **acotarlo a lo medido**.

## Punto 2 — correcciones objetivas
| Id | Cambio |
|----|--------|
| T1 | El kubelet no reinicia el pod: CNPG gestiona pods directamente, sin StatefulSet |
| T2 | `node-monitor-grace-period` ≈50 s por defecto en k8s v1.34 (CNPG documenta 40–55 s); temporizador attach/detach (~6 min) y taint `node.kubernetes.io/out-of-service` |
| T3 | Patroni en Kubernetes usa Endpoints/ConfigMaps nativos como DCS, no un etcd propio; la diferencia real es *quién decide* la promoción |
| T4 | Fuera el argumento de «cota inferior»: CNPG es *shared-nothing*, el detach/attach no está en el camino crítico del failover |
| E1 | F2: 11 inyecciones, 10 retenidas, declarado explícitamente |
| E2 | Medianas con y sin el arranque en frío: 36,8 s (n=10) y 36,9 s (n=11) |
| E3 | Precisión ajustada a la resolución del instrumento (±0,2 s): 7,9 s y 36,8 s |
| E4 | ρ=0,62 es moderada-fuerte; no significativa por falta de potencia, no por ser pequeña |

**Bibliografía.** Stonebraker & Kemnitz (1991) retirado como referencia del WAL (POSTGRES era
*no-overwrite*) y sustituido por ARIES (Mohan et al., 1992, TODS 17(1):94–162). Altas verificadas
contra fuente primaria: Abadi (2012) PACELC, *Computer* 45(2):37–42; Sun et al. (2022) Sieve,
OSDI 22:143–159; Gu et al. (2023) Acto, SOSP '23:96–112; Sivko (2026), Coroot, 29-07-2026.
Bajas por huérfanas: Engelbert, Portworx, Ongaro. Bajas por tangenciales: Van Renesse, Taft,
Burckhardt, Khan. **0 referencias huérfanas al cierre.**

## Punto 3 — reescritura
- **Título** (es/en) acotado a lo medido; **resumen** (150 pal.) y **abstract** (136) rehechos.
- **§3 y §4 fusionadas** en «Marco de análisis»; fuera las Ecs. 2–5 y las subsecciones 4.1, 4.2 y 4.4.
- **F2 reencuadrado**: *pod-failure* altera la especificación del pod; con
  `primaryUpdateStrategy: unsupervised` CNPG reconcilia la deriva reiniciando in situ. Los 36,8 s
  miden una reconciliación forzada, no un RTO. Retirada la afirmación de que el operador «decide esperar».
- **F3 reencuadrado**: no hubo decisión CP sino **ausencia de detección** (failsafe de Calico).
  Contrastado con Sivko (2026): bajo aislamiento completo CNPG promueve a los 38 s, el primario
  aislado sigue escribiendo 177 s y se pierden 291 escrituras confirmadas (562 reasignadas).
- **Hallazgo central** reescrito: de cuatro escenarios, solo F1 produjo el fallo que modela.
  La contribución pasa a ser metodológica: validar el inyector precede a cualquier cifra de resiliencia.
- **V(fallo,K)** degradado a **hipótesis**, con su contraejemplo (fallo de nodo) declarado.
- **§6 y §7** reescritas; limitaciones reordenadas con la fidelidad de la inyección en primer lugar.
- Fuera las cotas Clopper–Pearson de F2/F3 (ya no sostienen conclusión) y la Fig. 5.
- Afirmaciones ancladas por ruta al depósito Zenodo (DOI 10.5281/zenodo.23004248).

## Defectos corregidos de paso
- Referencias cruzadas desplazadas tras la fusión de secciones → 16 `\label` y 19 `\ref`, sin números fijos.
- Flotantes diferidos al final (`\dbltopfraction` 0.7 impedía colocar la Tabla 1): parámetros ampliados.
  Era la causa real de las 14 páginas, no el exceso de texto.
- Pie de la Fig. 1 (línea temporal): advierte que las dos magnitudes no son RTO comparables.

## Pendiente
- Sincronizar: `main_referencia_extendida_18pp.tex`, suplemento, `CITATION.cff`, carta al editor, Zenodo.
- Redactar la carta de respuesta a los árbitros punto por punto.

---

# Segunda pasada — cierre de los huecos de escritorio (2026-10-07)

**Búsqueda previa:** se rastrearon el árbol de trabajo, las 11 ramas locales, las 5 remotas y
los 1.460 blobs de todo el historial de git. **Los eventos del operador no existen en ninguna
parte**; `data/raw/` está vacío por diseño. El entorno productivo no es recuperable.

## Artículo (`main.tex`)

| Obs. | Cambio |
|------|--------|
| O9 | F2 pasa a enunciarse como **inferencia**, no observación. Se declara que la imagen de pausa no figura en `images/image-list.txt` (entorno air-gapped) y que la conclusión es **robusta a las dos ramas** —si cargó o si quedó en `ImagePullBackOff`—, porque en ambas el operador reconcilia una deriva de especificación sin evaluar promoción. Explica además el arranque en frío de ~80,5 s. Se declaran los valores por defecto vigentes (`failoverDelay` 0 s, `primaryUpdateMethod` restart) |
| T3 | La política sí denegaba la salida al *API server*, luego `probes.liveness.isolationCheck` (CNPG ≥1.27) era aplicable; si se activó no puede determinarse |
| O3 | Drees (2026) matizado: su CI sí integra comprobaciones tipo Jepsen y métricas de *failover* |
| O7 | Taxonomía con criterios explícitos y excluyentes: operadores por **quién decide la promoción** (central vs. distribuida); almacenamiento por **dónde reside el dominio de fallo del volumen**. Resuelta la incoherencia de Crunchy y el solape Ceph/SAN |
| O6 | Eliminada la dimensión de rendimiento, que no se medía |
| O11 | Cliente documentado: `psql`/libpq, conexión nueva por inserción, sin *pooler*, `PGCONNECT_TIMEOUT` 2 s, reintento a 0,2 s. Se declara que la descomposición del RTO exigiría los eventos perdidos |
| O13 | Autorización del equipo de operaciones, operador compartido con otros 4 clústeres, primarios ajenos en el nodo, CPU/ES no registradas. Antiafinidad **preferente** |
| O14, E5 | Fig. 1 nueva (pgfplots): las 20 ejecuciones individuales por orden, con medianas |
| E4 | **Confundido temporal declarado**: F1 13:54–14:21 UTC, F2 22:22–23:03, en bloques. El sesgo esperable va en contra del resultado |
| O16 | Tabla 2: columna «Indisp. (mediana)», columna `n`, y nota de que solo F1 es un RTO |
| Formal | Fuera la Fig. 1 anterior (texto ilegible); bibliografía en bandera, que elimina las URL con espacios |

## Depósito Zenodo (v1.1-fase1)

- **`data/f2_podfailure_cnpg_excluida.csv`** (nuevo): la inyección descartada, auditable sin
  alterar el conjunto analizado. Declarado que el valor es aproximado y la marca de tiempo no se conservó.
- **`analyze.py`**: reporta la mediana con y sin la exclusión (36,75 / 36,92 s). Verificado.
- **`README.md`, `DATA_DICTIONARY.md`, suplemento, 18 pp, `main.tex`**: corregida la promesa de
  facilitar los eventos del operador — no se conservaron y no pueden facilitarse.
- **`CITATION.cff` / `.zenodo.json`**: versión 1.1-fase1, título nuevo del artículo.
- **`zenodo-deposito-fase1.zip`** reconstruido: 44 ficheros, sin auxiliares.
- **Pendiente:** publicar la nueva versión en Zenodo (el concept DOI 10.5281/zenodo.23004248 no cambia).

## Estado de compilación
12/13 págs según la decisión sobre la Tabla 1 · 0 errores · 0 overfull · 0 refs sin resolver · 0 huérfanas · resumen 150 pal.

## Sigue pendiente (necesita el banco de pruebas)
- Repetir F2 con `SIGKILL` (A1 obligatorio 1, A2 requisito 1) — **imposible**: entorno no recuperable.
- Descomponer el RTO de F1 en línea de tiempo (A1 obligatorio 8, segunda mitad) — **imposible**: eventos no conservados.
- Carta de respuesta punto por punto a O1–O17, T1–T6, E1–E5.

## Cierre de la segunda pasada
- **Tabla 1 → Tabla S1 del suplemento** (decisión del autor), con puntero explícito desde §3.3.
  Las correcciones T1/T2/T4 se mantienen **en el artículo**, en prosa: CNPG gestiona los pods sin
  `StatefulSet`; `node-monitor-grace-period` ≈50 s por defecto en k8s v1.34 (CNPG: 40–55 s); el
  desalojo elimina el pod, luego la promoción sí se produce; Patroni usa objetos nativos como DCS.
- **T6**: F1 se inyectó sin `gracePeriod`, luego rigió el valor por defecto (terminación abrupta).
- **Artículo final: 12 págs · 0 errores · 0 overfull · 0 refs sin resolver · 0 huérfanas · resumen 150 pal.**
- **Suplemento: 5 págs · 0 errores · 0 overfull.** Depósito: 56 entradas.

---

# Tercera pasada — resolución de la tutora (2026-10-07)

Leída `ObserrvacionesArbitrosResolucionAP.docx` (69 párrafos). Es un documento de triaje:
apartados **A–G** a aplicar ya, **6 puntos diferidos** al Trabajo de Especialización (FaCyT-UC),
y un borrador de carta de respuesta.

**Resultado de la auditoría: A–G ya estaban aplicados** por las dos pasadas anteriores. Lo que
faltaba era suyo y se ha añadido:

| Añadido | Origen |
|---|---|
| Fase 2 reescrita para cubrir **los seis diferidos**, atada explícitamente al Trabajo de Especialización FaCyT-UC: F2 con `container-kill`/`SIGKILL`; F3 con aislamiento total por iptables/eBPF para ejercitar `isolationCheck`; fallo de nodo con antiafinidad **obligatoria**; F4 por `io.max` de cgroups v2; LSN bajo carga intensiva; comparación empírica de operadores y almacenamiento | Tutora §2 |
| Compromiso explícito de instrumentar el LSN donde se discute el RPO | Tutora §2.6 / O12 |
| Terminología unificada en el cuerpo: `\textit{failover}` | A1 formal 4 |
| **Bibliografía reordenada**: Abadi estaba tras Alvaro. 26 entradas, 0 duplicadas, 0 huérfanas | — |
| Referencias a la Tabla S1 abreviadas tras la primera mención | — |

**Carta de respuesta redactada:** `paper/faraute/carta_respuesta_arbitros.md` (3.063 palabras).
Cubre los 9 obligatorios y los 7 recomendados de A1, los 4 requisitos de A2, y los 6 diferidos con
justificación y plan, siguiendo el esquema de la tutora. Referencias de sección verificadas contra
el PDF final.

## Estado final
**Artículo: 12 págs · 0 errores · 0 overfull · 0 Missing character · 0 refs sin resolver · 0 huérfanas · resumen 150 pal. · abstract 134**
**Suplemento: 5 págs · 0 errores.** Depósito v1.1-fase1: 56 entradas.

## Pendiente (no depende de mí)
1. Publicar la versión nueva en Zenodo con el zip reconstruido (el concept DOI no cambia).
2. ORCID de la coautora y, si procede, correo institucional del autor de correspondencia (A1 formal 6).
3. Confirmar el título: la tutora propuso otro como ejemplo (ver abajo).
4. Nada commiteado.

---

# Cuarta pasada — revisión profunda con los agentes del proyecto (2026-10-07)

Despachados **writer-critic (62/100)**, **árbitro de dominio (70/100)** y **árbitro de métodos
(64/100)**. Los tres: revisión mayor. Cada hallazgo se verificó antes de aplicarlo; **dos
resultaron erróneos** y no se aplicaron: la acusación de que el evento del operador se copió del
informe de A1 (está en la versión enviada *antes* del arbitraje y registrado en
`results_summary.md`), y el cambio de formato de los nombres de autor, que contradice la
instrucción escrita del jurado.

## Correcciones de fondo

| Hallazgo | Verificación | Acción |
|---|---|---|
| Mediana de F2 mal redondeada | 36,745 → **36,7**, no 36,8 (doble redondeo) | Corregido en 7 apariciones; `analyze.py` imprime ahora valor exacto y reportable |
| Mecanismo de F3 equivocado | Documentación de Calico: la política solo afecta a conexiones **nuevas**; las establecidas sobreviven (existe `FlushConntrackOnPolicyUpdate`) | Reescrito: tráfico de *host* + excepción por *conntrack*. F3 no fue partición parcial |
| Cronología del fallo de nodo | `default-not-ready-toleration-seconds` = 300 s; el pod queda en `Terminating`, no se elimina | Corregida; contradecía al propio suplemento |
| Hipótesis de visibilidad | Refutada por el desalojo (pod no desaparece y CNPG promueve) y por Sivko (promoción con pod intacto) | **Retirada** del artículo y de la carta |
| «Commit fantasma» | El verificador manda el error a `/dev/null`: era un comentario, no código | Afirmación retirada |
| Ventana de F2 | `run-experiment.sh` la retira a los ~120 s, no 10 min | Declarado |
| Rejilla de medida de F3 | Depende del escenario (DROP vs REJECT): 2 s, no 0,2 s | Sin falsa precisión: «≈61 s» |
| Sivko 177 s vs 99 s | **Ambas correctas**, miden cosas distintas | Las dos, con su mecanismo |
| Suplemento desincronizado | Conservaba título viejo, «débil», «cota inferior» y permutación circular | Sincronizado |
| Citas ausentes | Chaos Mesh y Calico sin entrada bibliográfica | Añadidas + Natella et al. (2016) y kube-controller-manager |

## Guía de estilo de la revista
Verificado el cumplimiento literal de `guia_autor_Faraute.pdf`. Añadido `indentfirst` (medido en el
número publicado: todos los párrafos van sangrados). Figuras exportadas a JPEG 300 dpi en escala de
grises (`scripts/exportar_figuras_faraute.sh`). Orden de citas múltiples verificado: cronológico y
luego alfabético en las 12.

## Validación de uso de IA
`scripts/check_ia_estilo.py` (stdlib). Todo limpio salvo los guiones largos: 73 → 45. «de modo que»
24 → 8. **A1 contó la declaración de IA entre las fortalezas del artículo.**

## Materiales inexistentes — verificado y cerrado
`results.csv` y `verifier-cnpg.log` **nunca estuvieron en el repositorio**: 243 revisiones, 808
rutas en todo el historial, ramas locales y remotas, árbol de trabajo con ignorados, sin otro clon
en la máquina. Corregida en los cinco artefactos la promesa de facilitarlos a petición.

## Ajuste a 12 páginas sin pérdida
Tipografía (columnas, interlineado de tabla, figura), taxonomía condensada (lo pedía A1-O7/O8),
prosa de secciones sin respuestas obligatorias, y traslado al suplemento de las derivaciones del
RPO, la rejilla de F3, el detalle de *conntrack* y el plan de Fase 2.

## Estado final
**Artículo 12 pp · suplemento 6 pp · 0 errores · 0 overfull · 0 refs sin resolver ni huérfanas ·
resumen 148 palabras · 30 referencias.** Depósito v1.1-fase1, 57 ficheros.
