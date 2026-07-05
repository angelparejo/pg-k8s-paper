# SEGURIDAD — Garantías de aislamiento (para seguridad / DBA de producción)

Este documento está dirigido al responsable de seguridad y al DBA de producción. Explica **por qué** el piloto no puede afectar a los cuatro clústeres PostgreSQL preexistentes, pese a compartir el operador CloudNativePG.

## Situación

- El operador **CloudNativePG 1.28.0 ya está instalado** (namespace `cnpg-operator`) y gestiona **cuatro clústeres preexistentes**: `pg-prod` (producción), `gitlab/pg-gitlab` (infraestructura de GitLab), y `pg-cert` + `pg-dev` (no productivos). **Ninguno de los cuatro se toca.**
- El piloto añade un **quinto** clúster (`pglab-cnpg-exp`), nuevo, en un namespace nuevo (`pg-chaos-lab`), gestionado por **ese mismo operador compartido**.
- El operador es compartido; **los experimentos no**. Toda inyección de fallos apunta exclusivamente al clúster experimental.

## El riesgo y las cuatro barreras independientes

**Riesgo único a controlar:** que una inyección de fallos alcance por error los pods de los cuatro clústeres preexistentes. **El riesgo se agudiza** porque 3 de sus primarios (pg-cert-1, pg-dev-3, pg-gitlab-2) co-residen hoy en el nodo del laboratorio (`tcolp293`); por eso el dry-run de selectores (G1) es la barrera crítica.

La contención descansa en **cuatro capas independientes**. Tendrían que fallar las cuatro a la vez para que un experimento tocara producción:

1. **Chaos Mesh restringido al namespace.** Se instala con `clusterScoped: false`, `enableFilterNamespace: true` y `targetNamespace: pg-chaos-lab`. El controlador solo gestiona recursos de `pg-chaos-lab` y solo puede inyectar en namespaces que lleven el label de opt-in `chaos-mesh.org/inject=enabled`. Los namespaces productivos **no** llevan ese label. (Verificado en G2.1, G2.2, G3.)

2. **Daemon privilegiado confinado al nodo del lab.** El `chaos-daemon` (el componente que realmente mata/pausa/inyecta, y que corre privilegiado) se despliega con `nodeSelector: pg-chaos-lab/member=true`, es decir **solo en `tcolp293`**. **Advertencia honesta:** `tcolp293` es el worker nonprod designado, pero **no está vacío** — hoy co-aloja 3 primaries CNPG ajenos (pg-cert-1, pg-dev-3, pg-gitlab-2) además de ArgoCD/Harbor/Prometheus. Por tanto **la contención NO descansa en el aislamiento de nodo** (que no es total), sino en las barreras 1, 3 y 4: el `chaos-daemon` solo actúa cuando el **controlador** de Chaos Mesh se lo ordena, y el controlador solo gestiona recursos de `pg-chaos-lab`; ningún manifiesto de fallo selecciona a los vecinos (se demuestra pod por pod en el dry-run G1). Además, todos los escenarios son estrictamente pod-scoped (F1/F2 `pod-failure`, F4 IOChaos-FUSE): no hay fallos de nodo ni StressChaos que pudieran alcanzar por competencia de recursos a los primaries co-residentes. (Verificado en G4 —daemon solo en `tcolp293`— y G5 —inventario de co-residentes + confirmación de que ninguno es objetivo—.)

3. **Doble filtro en cada manifiesto.** Todos los experimentos de Chaos Mesh (PodChaos, IOChaos) están acotados por `namespaces: [pg-chaos-lab]` **y** por `cnpg.io/cluster: pglab-cnpg-exp`. La partición de red (F3) es una **NetworkPolicy**, que por diseño de Kubernetes solo puede afectar a pods de su propio namespace. (Verificado por el dry-run de selectores, G1.)

4. **Nombre de clúster único.** El clúster experimental se llama `pglab-cnpg-exp`, un nombre inequívoco que ninguno de los cuatro preexistentes comparte (se verifica en el paso 0.7). Así, el selector `cnpg.io/cluster: pglab-cnpg-exp` no puede resolver a un pod productivo ni siquiera hipotéticamente. (Verificado en G1.3.)

> El label `cnpg.io/instanceRole=primary` **sí** es común a los cinco clústeres (los 4 preexistentes + el experimental; todos tienen un primario). Por eso **ningún** manifiesto lo usa aislado: siempre va junto a `cnpg.io/cluster: pglab-cnpg-exp`. El checklist G1.4 lo demuestra explícitamente listando los 5 primarios y confirmando que ningún manifiesto seleccionaría por rol sin nombre de clúster.

## Qué NO hace el piloto

- **No instala ni actualiza operadores.** Usa el CNPG 1.28.0 existente tal cual. Si el operador no estuviera presente, el procedimiento se detiene (no lo instala).
- **No drena ni acordona nodos.** No se ejecuta `kubectl drain`/`cordon`. El "fallo de nodo" se **aproxima** con indisponibilidad sostenida del primario experimental (F2, `pod-failure` 10 min); no se provoca un fallo de nodo real.
- **No toca la SAN Huawei.** La inyección de latencia de E/S (F4) actúa a nivel de **FUSE dentro del pod** del primario experimental. No modifica el camino de E/S real hacia la cabina ni afecta a otros consumidores del arreglo.
- **No toca los cuatro clústeres preexistentes.** No los modifica, no los reprograma, no cambia su configuración. Al cerrar el piloto se **compara** el estado de producción contra la línea base capturada al inicio (paso 0.9 vs. Fase 6.3) y se exige que queden **idénticos**.
- **No silencia la monitorización de producción.** Como mucho se silencian alertas del namespace `pg-chaos-lab`. Las alertas de los clústeres preexistentes permanecen activas durante toda la ventana (G6).
- **No entra en el service mesh (Linkerd).** El namespace del lab (`pg-chaos-lab`) y los pods del clúster experimental se anotan con `linkerd.io/inject: disabled`, de modo que **no** se les inyecta el sidecar `linkerd-proxy`. Esto (a) **coincide con producción** —los namespaces `pg-*` de CNPG no están meshados—, por lo que no introduce salvedad de validez externa, y (b) evita contaminar la medición de RTO/latencia con un proxy en la ruta de datos.

## Contención de capacidad

El namespace `pg-chaos-lab` lleva una **ResourceQuota dura** (CPU, memoria, almacenamiento, nº de PVCs y pods) y un LimitRange. El laboratorio no puede consumir recursos más allá de ese tope, protegiendo la capacidad del clúster compartido (G7).

## Reversibilidad

Cualquier inyección se revierte al instante borrando el objeto que la causa (`kubectl delete podchaos/iochaos/networkpolicy`). El `ABORTO.md` detalla las señales de aborto y los comandos exactos de reversión por fase. La autoridad de aborto se define en `RESPONSABLES.md` y puede detener el piloto en cualquier momento.

## Coordinación con almacenamiento

Los volúmenes del laboratorio viven en la SAN Huawei real (vía CSI). Recomendaciones: si el OceanStor lo permite, asignar un pool/tier o QoS dedicado al lab. El borrado final del namespace elimina los PVCs del lab → **coordinar ese borrado con el equipo de almacenamiento**.
