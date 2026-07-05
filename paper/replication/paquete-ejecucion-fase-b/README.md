# Paquete de ejecución — Piloto Fase B (solo CloudNativePG)

Paquete autocontenido para que un equipo ejecutor (que puede no conocer el contexto de la investigación) realice, de forma segura, un piloto de inyección de fallos sobre **un único clúster PostgreSQL nuevo y aislado** en un clúster Kubernetes **productivo**.

## En una frase

Se crea un **cuarto** clúster CloudNativePG (`pglab-cnpg-exp`), nuevo y aislado en el namespace `pg-chaos-lab`, gestionado por el operador CNPG **ya instalado y compartido** con tres clústeres productivos. Se le inyectan fallos controlados (terminación de pod, indisponibilidad sostenida, partición de red, latencia de E/S) y se miden RTO y RPO. **Los tres clústeres productivos no se tocan.**

## Qué hace / qué NO hace

| ✅ Hace | ❌ No hace |
|---|---|
| Crea `pglab-cnpg-exp` en `pg-chaos-lab` | Instalar o actualizar operadores (usa el CNPG existente) |
| Inyecta fallos **solo** a ese clúster (doble filtro namespace + nombre) | Drenar/acordonar nodos |
| Mide RTO/RPO con carga real (pgbench + verificador) | Tocar la SAN Huawei (IOChaos es FUSE dentro del pod) |
| Deja evidencia y compara producción antes/después | Tocar los 3 clústeres CNPG productivos |

## Orden de lectura (obligatorio)

1. **`SEGURIDAD.md`** — garantías de aislamiento (leerlo primero, sobre todo seguridad/DBA).
2. **`RESPONSABLES.md`** — rellenar roles y autoridad de aborto antes de agendar.
3. **`PROCEDIMIENTO.md`** — maestro paso a paso (incluye **Planificación de Ventanas**: el piloto se fracciona en 3 ventanas de mantenimiento).
4. **`CHECKLIST-GONOGO.md`** — compuerta crítica; se ejecuta en Fase 4 y al reanudar cada ventana.
5. **`ABORTO.md`** — señales de aborto y reversión exacta por fase (tenerlo abierto durante la ejecución).

## Contenido

```
PROCEDIMIENTO.md        Maestro paso a paso (Fase 0–6) + Planificación de Ventanas
SEGURIDAD.md            Garantías de aislamiento para seguridad/DBA de producción
CHECKLIST-GONOGO.md     Compuerta PASA/NO PASA antes de inyectar
ABORTO.md               Señales de aborto + reversión por fase
RESPONSABLES.md         Roles, hoja de registro de la ventana e inventario productivo
manifiestos/            Kit adaptado a Camino B (solo CNPG, clúster pglab-cnpg-exp)
  00-namespace/         Aislamiento: namespace, cuota, límites, RBAC scoped
  10-chaos-mesh/        Chaos Mesh 2.7.x acotado + instalación offline (air-gapped)
  20-cluster/           Definición del clúster experimental CNPG
  30-workload/          Carga pgbench + verificador de transacciones (RTO/RPO)
  40-experiments/       Manifiestos de fallo F1–F4 (todos acotados a pglab-cnpg-exp)
  scripts/              Orquestación, parsing, estadística y dry-run de selectores GO/NO-GO (sin dependencias)
  images/               Lista de imágenes + import por ctr
```

## Notas

- **Air-gapped:** todas las imágenes se importan con `ctr` en cada nodo del lab (ver `manifiestos/images/` y `manifiestos/10-chaos-mesh/INSTALL-offline.md`).
- **Fraccionamiento:** el piloto completo son ~12–14 h; se ejecuta en 3 ventanas (V1: setup + F1 + F3 · V2: F4 · V3: F2). El laboratorio se deja desplegado entre ventanas — ver "Planificación de Ventanas" en `PROCEDIMIENTO.md`.
- **Nombre único:** el clúster experimental se llama `pglab-cnpg-exp`. Si algún clúster productivo ya usara ese nombre (se verifica en el paso 0.7), cambiarlo en todos los manifiestos antes de empezar.
- El script `manifiestos/scripts/analyze.py` conserva la lógica de comparación CNPG-vs-Zalando del kit original; en Camino B (solo CNPG) esa comparación queda **inerte** y no afecta a los resultados.
