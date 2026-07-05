# ABORTO — Señales de parada y reversión inmediata

**Principio:** ante cualquier duda razonable sobre impacto en producción, **abortar primero, investigar después**. Revertir es barato e inmediato; un incidente en producción no. La **autoridad de aborto** (ver `RESPONSABLES.md`) puede detener el piloto en cualquier momento sin justificación previa.

---

## 1. Señales que OBLIGAN a abortar

Verificar tras **cada** inyección (y de forma continua durante F2/F4, que son largas). Si se cumple **cualquiera**:

- **Alertas activas fuera de `pg-chaos-lab`** — cualquier alerta de los cuatro clústeres preexistentes o de infraestructura compartida.
- **Degradación del plano de control** — latencia p99 del API server o `etcd_disk_wal_fsync` peor que la línea base; timeouts de `kubectl`.
- **Cualquier anomalía en los cuatro clústeres preexistentes** — un clúster preexistente que cambie de nº de instancias, pierda el primario, haga failover, entre en `CrashLoopBackOff`, o cuyo pod se reprograme coincidiendo en el tiempo con una inyección. **Atención especial** a pg-cert, pg-dev y pg-gitlab, cuyos primarios co-residen con el lab en `tcolp293`.
- **Presión de E/S anómala en nodos que NO son del laboratorio.**
- **Un `chaos-daemon` aparece en un nodo que no es del lab**, o un experimento selecciona un pod fuera de `pg-chaos-lab`.
- **La verificación de igualdad (Fase 6.3) o la reanudación (R2) detecta un cambio en recursos preexistentes.**

---

## 2. Reversión inmediata (en orden, según la fase en curso)

**Detener toda inyección de Chaos Mesh (F1 / F2 / F4) — efecto inmediato:**
```bash
kubectl -n pg-chaos-lab delete podchaos,iochaos --all
```

**Revertir la partición de red (F3):**
```bash
kubectl -n pg-chaos-lab delete networkpolicy -l experiment=f3
# (equivalente: kubectl delete -f manifiestos/40-experiments/f3-partition-cnpg.yaml)
```

**Congelar el laboratorio (detener la carga sin desmontar):**
```bash
kubectl -n pg-chaos-lab scale deploy pgbench-cnpg tx-verifier-cnpg --replicas=0
```

**Desmontaje de emergencia del laboratorio completo (si se decide abandonar el piloto):**
```bash
kubectl -n pg-chaos-lab delete podchaos,iochaos,networkpolicy --all
kubectl delete -f manifiestos/30-workload/
kubectl -n pg-chaos-lab delete cluster pglab-cnpg-exp
kubectl delete -f chaos-mesh-rendered.yaml           # retira Chaos Mesh
# El borrado del namespace elimina PVCs -> coordinar con almacenamiento:
# kubectl delete namespace pg-chaos-lab
# La SC huawei-ch-xfs es reclaimPolicy=Retain: los PV NO se borran solos.
# Borrar los PV liberados del lab (coordinar con almacenamiento):
# kubectl get pv | grep pg-chaos-lab ; kubectl delete pv <nombres>
```

---

## 3. Después de abortar

1. **Confirmar que la inyección cesó:**
   ```bash
   kubectl -n pg-chaos-lab get podchaos,iochaos,networkpolicy   # -> sin recursos
   ```
2. **Verificar producción contra la línea base** (mismo bloque de la Fase 6.3):
   ```bash
   kubectl get clusters.postgresql.cnpg.io -A                    # los 4 preexistentes, saludables
   kubectl get deploy -A -l app.kubernetes.io/name=cloudnative-pg
   ```
   Comparar con `estado-inicial.txt`. Si algún recurso preexistente cambió → **escalar como incidente** al DBA/seguridad (ver `RESPONSABLES.md`), no cerrar el piloto.
3. **Documentar** en `RESPONSABLES.md` (hoja de registro): qué señal disparó el aborto, hora, fase/ventana, estado de producción tras revertir, y decisión (reintentar en otra ventana / abandonar).
4. **No reanudar** hasta que la causa esté entendida y el checklist GO/NO-GO vuelva a estar completo en PASA.

---

## 4. Contactos de aborto

Rellenar en `RESPONSABLES.md`. Tener a mano durante toda la ventana:
- Autoridad de aborto (decide detener): __________
- DBA de producción de guardia: __________
- Responsable de almacenamiento (SAN): __________
- Responsable de plataforma/K8s: __________
