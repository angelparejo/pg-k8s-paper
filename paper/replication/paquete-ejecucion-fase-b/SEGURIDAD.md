# SEGURIDAD — Garantías de aislamiento (para seguridad / DBA de producción)

Este documento está dirigido al responsable de seguridad y al DBA de producción. Explica **por qué** el piloto no puede afectar a los tres clústeres PostgreSQL productivos, pese a compartir el operador CloudNativePG.

## Situación

- El operador **CloudNativePG 1.28.0 ya está instalado** y gestiona **tres clústeres productivos** en sus namespaces.
- El piloto añade un **cuarto** clúster (`pglab-cnpg-exp`), nuevo, en un namespace nuevo (`pg-chaos-lab`), gestionado por **ese mismo operador compartido**.
- El operador es compartido; **los experimentos no**. Toda inyección de fallos apunta exclusivamente al clúster experimental.

## El riesgo y las cuatro barreras independientes

**Riesgo único a controlar:** que una inyección de fallos alcance por error los pods de los tres clústeres productivos.

La contención descansa en **cuatro capas independientes**. Tendrían que fallar las cuatro a la vez para que un experimento tocara producción:

1. **Chaos Mesh restringido al namespace.** Se instala con `clusterScoped: false`, `enableFilterNamespace: true` y `targetNamespace: pg-chaos-lab`. El controlador solo gestiona recursos de `pg-chaos-lab` y solo puede inyectar en namespaces que lleven el label de opt-in `chaos-mesh.org/inject=enabled`. Los namespaces productivos **no** llevan ese label. (Verificado en G2.1, G2.2, G3.)

2. **Daemon privilegiado confinado a los nodos del lab.** El `chaos-daemon` (el componente que realmente mata/pausa/inyecta, y que corre privilegiado) se despliega con `nodeSelector: pg-chaos-lab/member=true`. No existe en los nodos que alojan producción. (Verificado en G4; además G5 confirma que ningún pod productivo corre en los nodos del lab.)

3. **Doble filtro en cada manifiesto.** Todos los experimentos de Chaos Mesh (PodChaos, IOChaos) están acotados por `namespaces: [pg-chaos-lab]` **y** por `cnpg.io/cluster: pglab-cnpg-exp`. La partición de red (F3) es una **NetworkPolicy**, que por diseño de Kubernetes solo puede afectar a pods de su propio namespace. (Verificado por el dry-run de selectores, G1.)

4. **Nombre de clúster único.** El clúster experimental se llama `pglab-cnpg-exp`, un nombre inequívoco que ninguno de los tres productivos comparte (se verifica en el paso 0.7). Así, el selector `cnpg.io/cluster: pglab-cnpg-exp` no puede resolver a un pod productivo ni siquiera hipotéticamente. (Verificado en G1.3.)

> El label `cnpg.io/instanceRole=primary` **sí** es común a los cuatro clústeres (todos tienen un primario). Por eso **ningún** manifiesto lo usa aislado: siempre va junto a `cnpg.io/cluster: pglab-cnpg-exp`. El checklist G1.4 lo demuestra explícitamente listando los 4 primarios y confirmando que ningún manifiesto seleccionaría por rol sin nombre de clúster.

## Qué NO hace el piloto

- **No instala ni actualiza operadores.** Usa el CNPG 1.28.0 existente tal cual. Si el operador no estuviera presente, el procedimiento se detiene (no lo instala).
- **No drena ni acordona nodos.** No se ejecuta `kubectl drain`/`cordon`. El "fallo de nodo" se **aproxima** con indisponibilidad sostenida del primario experimental (F2, `pod-failure` 10 min); no se provoca un fallo de nodo real.
- **No toca la SAN Huawei.** La inyección de latencia de E/S (F4) actúa a nivel de **FUSE dentro del pod** del primario experimental. No modifica el camino de E/S real hacia la cabina ni afecta a otros consumidores del arreglo.
- **No toca los tres clústeres productivos.** No los modifica, no los reprograma, no cambia su configuración. Al cerrar el piloto se **compara** el estado de producción contra la línea base capturada al inicio (paso 0.9 vs. Fase 6.3) y se exige que queden **idénticos**.
- **No silencia la monitorización de producción.** Como mucho se silencian alertas del namespace `pg-chaos-lab`. Las alertas de los clústeres productivos permanecen activas durante toda la ventana (G6).

## Contención de capacidad

El namespace `pg-chaos-lab` lleva una **ResourceQuota dura** (CPU, memoria, almacenamiento, nº de PVCs y pods) y un LimitRange. El laboratorio no puede consumir recursos más allá de ese tope, protegiendo la capacidad del clúster compartido (G7).

## Reversibilidad

Cualquier inyección se revierte al instante borrando el objeto que la causa (`kubectl delete podchaos/iochaos/networkpolicy`). El `ABORTO.md` detalla las señales de aborto y los comandos exactos de reversión por fase. La autoridad de aborto se define en `RESPONSABLES.md` y puede detener el piloto en cualquier momento.

## Coordinación con almacenamiento

Los volúmenes del laboratorio viven en la SAN Huawei real (vía CSI). Recomendaciones: si el OceanStor lo permite, asignar un pool/tier o QoS dedicado al lab. El borrado final del namespace elimina los PVCs del lab → **coordinar ese borrado con el equipo de almacenamiento**.
