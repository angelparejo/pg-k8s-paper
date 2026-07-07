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

**F2 (pod-failure, Ventana 3) cerrará el gradiente:** al dejar el pod `NotReady` sin matarlo,
*debería* promover — validando que el no-failover de F3 se debe a que el pod sigue `Ready`.

## Nota de fiabilidad del harness
Un único id espurio negativo (`-1783400188329960503`, `ts=2026-07-07 04:56 UTC`) en `truth`,
anterior a todas las ventanas medidas (F1 arrancó 13:54 UTC). Es un *write de más* por un
`i` corrupto en el bash del verificador en un arranque previo, **no** una pérdida (no es RPO).
El rango medido (ids 1..211489) es contiguo sin huecos. Recomendación: inicializar `i` de forma
defensiva en el verificador para futuras ventanas.

## Pendiente
- **F4** (IOChaos 20/50/100 ms + base 0 ms) — Ventana 2, ~6.5–7 h.
- **F2** (`pod-failure` 10 min) — Ventana 3, ~2–2.5 h.
- **Fase 6** — `analyze.py` (Kruskal-Wallis niveles F4, Spearman), diff vs `estado-inicial.txt`, teardown + borrado de PVs (SC Retain).
- Decisión abierta: alcance de operadores (CNPG-solo vs 2).
