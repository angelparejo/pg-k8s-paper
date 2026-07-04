# Análisis Sistemático de Operadores de PostgreSQL y Almacenamiento basado en CSI en Kubernetes: Arquitectura, Manejo de Fallos e Implicaciones en la Consistencia

*(Título de trabajo, v1-5)*

Estudio en curso sobre cómo la interacción entre la capa de operador de Kubernetes, el driver de almacenamiento CSI y PostgreSQL afecta la **consistencia** y la **recuperación ante fallos**, medida mediante RTO (Recovery Time Objective) y RPO (Recovery Point Objective) bajo inyección controlada de fallos.

**Autor:** Angel A. Parejo R. — Valencia, Estado Carabobo, Venezuela — angelparejo@gmail.com
**Institución:** Universidad de Carabobo, Valencia, Estado Carabobo, Venezuela

Este es un proyecto de investigación concreto construido sobre el andamiaje [clo-author](https://github.com/hugosantanna/clo-author), adaptado de economía empírica a investigación en sistemas distribuidos. Ver `CLAUDE.md` para la configuración de trabajo y `.claude/references/domain-profile.md` para el perfil metodológico completo. `README.md` documenta el andamiaje en sí y se deja intencionalmente en inglés/genérico.

---

## Pregunta de investigación

¿Cómo difieren el comportamiento de failover y las garantías de consistencia de datos entre operadores de PostgreSQL en Kubernetes, al inyectar fallos controlados de almacenamiento y red en un testbed?

---

## Idioma y plan de publicación

- El artículo se redacta **en español** (secciones, prosa, `/write` y el pase de humanizer).
- **Tier primario (objetivo inmediato):** revistas iberoamericanas indexadas en Scopus/SciELO — CLEI Electronic Journal, RISTI, Ingeniare (Revista Chilena de Ingeniería), Computación y Sistemas (CIC-IPN, México). Envío en español. **Indexación Scopus/SciELO y cuartil de las cuatro revistas: pendientes de verificar** en el portal de cada revista antes de someter.
- **Tier secundario (futuro):** Future Generation Computer Systems (FGCS), Journal of Systems and Software (JSS), IEEE Access. Requiere, en este orden: (1) validación empírica completa de los experimentos, (2) traducción íntegra al inglés + pase de language editing. No se somete a este tier hasta cumplir ambas condiciones.

---

## Testbed

| Componente | Versión |
|-----------|---------|
| Kubernetes | 1.34.6 |
| CloudNativePG | 1.28.0 |
| PostgreSQL | 16.13 |
| Driver CSI | Huawei CSI 4.10.1 (Fibre Channel / SAN) |
| CNI | Calico 3.31.4 |
| Inyección de fallos | Chaos Mesh |
| Operadores comparados | CloudNativePG vs. Zalando/Patroni |

---

## Metodología (resumen)

- Inyección de fallos controlada (Chaos Mesh) bajo cargas de benchmark repetidas (pgbench/sysbench)
- Métricas primarias: **RTO** y **RPO**
- Análisis estadístico: **no paramétrico** (Mann-Whitney U, Kruskal-Wallis, Spearman) — distribuciones no normales, n pequeño
- Sin pretensión de inferencia causal; es una evaluación comparativa/descriptiva controlada de sistemas

### Limitaciones conocidas

- El almacenamiento es SAN/Fibre-Channel homogéneo; no hay contraste empírico frente a almacenamiento local o distribuido en red
- El fallo de nodo se aproxima mediante inyección sostenida de pod-failure, no mediante desalojo real de nodo ni ciclo detach/attach del CSI

---

## Restricción del entorno

El testbed está **air-gapped**. Todos los scripts de análisis (`scripts/`) usan bash y la librería estándar de Python — sin `pip install`, sin R, sin paquetes externos.

---

## Estado

Borrador en curso. Ver `CLAUDE.md` → Current Project State para el estado vivo del pipeline.
