# Resumen de resultados — Piloto Fase B (solo CloudNativePG)

Clúster experimental `pglab-cnpg-exp` (CNPG 1.28.0, PG 16.13, 3 instancias, SC `huawei-ch-xfs`),
nodo del lab `tcolp293`, K8s 1.34.6, Calico 3.31.4, Chaos Mesh 2.8.3 confinado.
RTO = hueco entre COMMITs del `tx-verifier` (resolución ~100 ms). RPO = huecos en la
secuencia de la tabla `truth` (id secuencial, PK). Datos crudos en el servidor (gitignored);
series limpias en `data/cleaned/`.

## Ventana 1 (2026-07-07) — COMPLETA

### F1 — Terminación del pod primario (`pod-kill`, one-shot), n=10
- RTO: media **7.69 s**, mediana **7.91 s**, min **6.61**, max **8.17**, sd **0.54** (s).
- Failover real en las 10 reps (primario alternó exp-1↔exp-2).
- **RPO = 0.** Los 4 clústeres preexistentes intactos en todo el lote.
- Datos: `data/cleaned/f1_rto_cnpg.csv`.

### F3 — Partición de red del primario (NetworkPolicy Calico deny-all), 12 inyecciones
- Diseño: 1 exploratoria (149 s) + 1 sonda larga (300 s) + 10 fijas (60 s).
- **CNPG NO promovió en ninguna** (0/12). `currentPrimary` invariable; el pod primario
  aislado se mantuvo `Ready=True` toda la partición.
- Pérdida de disponibilidad de escritura = **duración de la partición** (p.ej. 60 s → 60.75 s;
  el ~0.75 s extra es la reconexión). Recuperación tras sanar **< 1 s** (mismo primario vuelve
  a ser alcanzable), frente a ~7.7 s de F1 (que requiere failover completo).
- **RPO = 0** (por construcción: sin promoción no hay divergencia posible).
- Datos: `data/cleaned/f3_partition_cnpg.csv`.

## Ventana 2 (2026-07-07) — F4 NO EJECUTADA (bloqueo estructural, reformulada como hallazgo)

### F4 — Sensibilidad a latencia de E/S (IOChaos FUSE): imposible sobre CNPG
La validación previa al lote (Opción A: 1 corrida a 100 ms antes de las 5×5 min) **detuvo el
experimento**: IOChaos **nunca inyecta** latencia. pgbench a "100 ms" da la misma latencia/tps
que el baseline 0 ms (lat media ~8.5 ms, ~450–480 tps en ambos), y el estado del recurso queda
en `AllInjected=False`.

**Causa raíz (confirmada por eventos del controller + logs del `chaos-daemon`):** el inyector
FUSE `toda` hace `ptrace attach` a postgres pero al montar el FUSE falla con
`toda startup ... Read-only file system (os error 30)` y hace panic, reintentando en bucle.
**CloudNativePG endurece sus pods con `readOnlyRootFilesystem: true`** (+ `runAsNonRoot`, drop de
capabilities); `toda` requiere un rootfs escribible para su andamiaje de montaje. El `PodIOChaos`
se construye correctamente (`volumeMountPath=/var/lib/postgresql/data`, `container=postgres`,
path/latency correctos) y el dry-run de selectores pasó: **no es un error de configuración sino
una incompatibilidad estructural** entre la inyección de E/S a nivel de contenedor (FUSE) y el
*hardening* del operador. Es un límite general de Chaos Mesh, no un defecto del kit.

**Hallazgo (publicable):** el endurecimiento de seguridad del operador (sistema de archivos raíz
de solo-lectura) **impide inyectar fallos de E/S a nivel de contenedor** con la herramienta de
caos estándar. Es una interacción hardening↔tooling directamente relevante para la tesis sobre
operadores y almacenamiento.

**Por qué V1 no lo detectó:** ni F1 (`pod-kill` vía API) ni F3 (NetworkPolicy Calico) usan el
`chaos-daemon`/`toda`; F4 fue el primer escenario en ejercer la inyección a nivel de contenedor.
La validación de una corrida antes del lote (parte del diseño Opción A) lo atrapó — justificación
empírica de ese gate.

**Decisión (2026-07-07):** F4 se **reformula** — el bloqueo se documenta como hallazgo y la
medición cuantitativa de sensibilidad de E/S pasa a trabajo futuro (mecanismo sin FUSE, p. ej.
throttle cgroup `io.max`, fuera del alcance de este piloto). No se altera el sistema bajo prueba.
Evidencia: `val-baseline.log`, `val-100ms.log` (en el servidor) + eventos `Read-only file system
(os error 30)`. El arnés F4 (`run-f4-latency.sh`, `parse-f4.py`, manifiestos IOChaos) queda en el
paquete de replicación por si se retoma con otro mecanismo.

## Ventana 3 (2026-07-07) — F2 (`pod-failure`): COMPLETA (n=10)

### F2 — Indisponibilidad del primario (`pod-failure`, 10 min) — sustituto de fallo de nodo
Contra lo hipotetizado, `pod-failure` **NO produce failover** — **0/10 promociones** (n=10 + 1 validación).
- **Sí inyecta** (`AllInjected=True`; sin bloqueo de air-gap, a diferencia de F4).
- `currentPrimary` **no cambia** (siguió `exp-2` en las 10 reps). En vez de promover una réplica,
  **CNPG recrea el pod primario en su sitio** (Terminating → Init → Running, mismo nombre/PVC) y lo
  devuelve a `Ready`, manteniéndolo primario. CNPG **derrota** el swap a imagen `pause` de Chaos Mesh
  recreando el pod con la imagen real; los `duration: 10m` resultan inefectivos.
- **RTO (ventana de indisponibilidad de escritura): mediana 36.75 s** (n=10; IQR ~[36.2, 37.1], rango
  35.5–38.3, sd ~0.83). El servicio `-rw` sigue apuntando al primario caído porque no hay promoción.
  **~4.6× el failover de F1 (7.91 s).** La validación previa (1.ª inyección, retirada a mano) dio ~80 s
  (outlier de primera-inyección; **excluida**, no está en `results.csv`).
- **RPO = 0.** Recuperación limpia (3/3); 4 preexistentes intactos tras cada rep.
- Datos: `data/cleaned/f2_podfailure_cnpg.csv`.

**RPO GLOBAL = 0 (todo el piloto):** `truth` contiguo **1..613253, 0 huecos** y 11/11 ids-frontera
(último COMMIT antes de cada outage) presentes → **ninguna escritura reconocida se perdió en F1, F3 ni
F2**. CNPG mantiene cero pérdida de datos bajo los tres tipos de fallo; lo que varía es el RTO
(7.91 s / 36.75 s / = duración de la partición).

**El gradiente F1/F2/F3 son TRES comportamientos distintos, no dos:**
- **F1 (pod-kill):** pod eliminado → promoción inmediata (RTO mediana **7.91 s**).
- **F2 (pod-failure):** pod recreado en sitio → **sin promoción**, RTO mediana **36.75 s** (esperar recreación).
- **F3 (partición):** pod sigue `Ready` → sin promoción, outage = duración de la partición.

Contraintuitivo: **matar el pod se recupera más rápido que "fallarlo"** — el kill dispara promoción,
el failure dispara esperar-y-recrear. El RTO de F2 es **cota inferior** del fallo de nodo real (no hay
detach/attach CSI). Instrumento: `run-experiment.sh` marca T0 (su detección de failover por cambio de
primario **no dispara** — cosmético); el RTO real sale del gap del verificador (`parse-verifier.py`).

## Hallazgo central (columna vertebral de la contribución sobre consistencia)

La variable causal del failover en CNPG **no es el fallo en sí, sino su visibilidad ante
Kubernetes**:
- **F1 (pod-kill):** el contenedor muere → pod `NotReady` → CNPG registra
  *"Current primary isn't healthy, initiating a failover"* → promueve en ~7.7 s.
- **F3 (partición Calico):** las sondas del kubelet **no** se bloquean (failsafe, tráfico de
  host) → el pod aislado sigue `Ready` → CNPG **no emite ningún evento** y **no promueve** →
  elige **consistencia sobre disponibilidad** (comportamiento CP), sin split-brain.

Evidencia directa del mecanismo: contraste de eventos de CNPG (F1 loguea el failover; F3
guarda silencio total durante 300 s de partición) + `pod.Ready=True` muestreado cada 20 s
durante la sonda larga. Respuesta al árbitro sobre "¿promueve alguna vez?": **no en ≥300 s**.

**Actualización tras la validación de F2 (Ventana 3):** la predicción de que `pod-failure`
promovería quedó **falsada** — CNPG recrea el primario en su sitio y **no promueve** (ver Ventana 3).
El mecanismo se refina: la promoción de F1 se explica por la **eliminación** del pod (el primario
deja de existir), no por el mero `NotReady`; cuando el pod se recrea con la misma identidad/PVC, CNPG
prefiere esperarlo antes que promover. El gradiente pasa a tres comportamientos (kill→promueve rápido;
failure→recrea en sitio, más lento; partición→CP sin promoción). **Confirmado con n=10: 0/10 promociones,
RTO mediana 36.75 s.**

## Nota de fiabilidad del harness
Un único id espurio negativo (`-1783400188329960503`, `ts=2026-07-07 04:56 UTC`) en `truth`,
anterior a todas las ventanas medidas (F1 arrancó 13:54 UTC). Es un *write de más* por un
`i` corrupto en el bash del verificador en un arranque previo, **no** una pérdida (no es RPO).
El rango medido (ids 1..211489) es contiguo sin huecos. Recomendación: inicializar `i` de forma
defensiva en el verificador para futuras ventanas.

**Bug de escala en `parse-verifier.py` (Fase 6):** con el log completo (117 223 COMMITs) el chequeo de
RPO falla con `OSError: Argument list too long: 'psql'` — construye un `WHERE id IN (…117k ids…)` que
excede `ARG_MAX`. El RTO (gaps) sí funciona. Workaround usado: consulta agregada de contigüidad en
`truth` server-side (`(max-min+1)-count(*)`) en vez del `IN (...)`. Arreglo pendiente en el script.

## Pendiente
- **F4** — REFORMULADA (ver Ventana 2): no se ejecuta con IOChaos; documentar el bloqueo como
  hallazgo en Métodos/Resultados del paper. Medición cuantitativa de E/S → trabajo futuro.
- **F2** (`pod-failure`) — lote n=10 EN EJECUCIÓN (Ventana 3). Confirmar el no-failover
  (recreación en sitio) y medir el RTO de recreación (~77 s en validación) desde el gap del verificador.
- **Fase 6** — `analyze.py results.csv` (medianas/p95 F1/F3; ya sin niveles F4), RPO final,
  diff vs `estado-inicial.txt`, teardown + borrado de PVs (SC Retain).
- **Escribir el hallazgo F4** en el paper (Métodos: por qué F4 no se ejecutó; Resultados/Discusión:
  la incompatibilidad hardening↔FUSE como resultado).
- Alcance de operadores: **RESUELTO** — producción no permite instalar Zalando → v2-experimental
  se reencuadra a estudio en profundidad de CNPG + marco analítico para N operadores
  (plan: `quality_reports/reframe_v2_cnpg_alcance.md`).
