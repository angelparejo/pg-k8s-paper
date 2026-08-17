# Paquete de replicación — Estudio empírico Fase 1 (CloudNativePG bajo fallos inyectados)

Acompaña al artículo *"Análisis multicapa de operadores de PostgreSQL y almacenamiento CSI
en Kubernetes: un marco de análisis y un estudio empírico de CloudNativePG bajo fallos
inyectados"* (Revista FARAUTE de Ciencias y Tecnología, UC/FACYT).

**Autor:** Angel A. Parejo R. — Universidad de Carabobo (ORCID 0009-0001-9737-7116)
**Licencias:** datos/documentación CC-BY-4.0 · código MIT (ver `LICENSE.md`)
**DOI:** *por asignar en Zenodo* (ver "Cómo obtener el DOI" abajo)

> **Nota sobre nombres.** El experimento se ejecutó sobre un clúster Kubernetes productivo
> de un tercero. Los nombres de nodos y de los clústeres PostgreSQL ajenos al experimento
> son **seudónimos consistentes** (`nodo-lab-01`, `nodo-02`…`nodo-04`; `pg-alfa`, `pg-beta`,
> `pg-gamma`, `pg-delta`), iguales en el artículo y en todo este paquete. La topología, la
> co-residencia y los recuentos son los reales: lo único sustituido son los identificadores.
> El clúster experimental (`pglab-cnpg-exp`) y su namespace (`pg-chaos-lab`) sí llevan su
> nombre verdadero, porque los crea y destruye el propio piloto.

## Contenido
```
data/                        Datos limpios de RTO/RPO por escenario (F1, F2, F3)
DATA_DICTIONARY.md           Diccionario de columnas de los CSV
supplement/
  suplemento.pdf / .tex      Material suplementario: métodos y resultados extendidos
execution-package/           Paquete de ejecución (protocolo + manifiestos + scripts)
  manifiestos/00..40         Kubernetes / Chaos Mesh (namespace, cluster, workload, experimentos)
  manifiestos/30-workload/tx-verifier-cnpg.yaml   Cliente verificador de transacciones
  manifiestos/scripts/analyze.py                  Reproduce TODAS las cifras del artículo
  PROCEDIMIENTO.md, CHECKLIST-GONOGO.md, SEGURIDAD.md
CITATION.cff                 Metadatos de citación
LICENSE.md                   Licencias (CC-BY-4.0 datos/docs; MIT código)
.zenodo.json                 Metadatos para el depósito
```

## Reproducir las cifras del artículo (1 comando, sin dependencias)
```bash
python3 execution-package/manifiestos/scripts/analyze.py
```
Reproduce, desde `data/*.csv` y solo con biblioteca estándar de Python: medianas, IQR, rangos,
intervalos de confianza de mediana (estadísticos de orden, cobertura 97,9 %), Mann–Whitney
(U exacto, p bilateral, z), correlación rango-biserial, Hodges–Lehmann, razón de medianas,
Clopper–Pearson (0/10 y 0/12), permutación exacta y Spearman. Salida esperada: F1 7,91 s,
F2 36,75 s, razón 4,65×, U=0 p≈1,1×10⁻⁵, HL 28,96 s, cotas 25,9 %/22,1 %.

## Reproducir el experimento completo
Requiere un clúster Kubernetes con CloudNativePG y Chaos Mesh. Ver `execution-package/PROCEDIMIENTO.md`
(namespace → cluster → workload → verifier → experimentos → parseo → análisis). Los escenarios:
F1 PodChaos `pod-kill`; F2 PodChaos `pod-failure`; F3 partición vía NetworkPolicy de Calico;
F4 IOChaos (no ejecutable sobre CNPG por incompatibilidad FUSE / `readOnlyRootFilesystem` —
ver el suplemento). Entorno: Kubernetes 1.34.6, PostgreSQL 16.13, CNPG 1.28.0, Chaos Mesh 2.8.3,
Calico 3.31.4, CSI Huawei 4.10.1 (SAN/FC).

## Cómo obtener el DOI (Zenodo)
1. Crear un nuevo *upload* en Zenodo y arrastrar el contenido de esta carpeta (o su ZIP).
2. En el formulario, **"Reserve DOI"** para obtener el DOI antes de publicar.
3. Sustituir `DOI por asignar` / `10.5281/zenodo.XXXXXXX` en `CITATION.cff`, `.zenodo.json`,
   el suplemento y el manuscrito (sección Disponibilidad de datos) por el **concept DOI**.
4. Publicar. El *concept DOI* (todas las versiones) es el que se cita en el artículo.

## Nota de acceso
El experimento se ejecutó sobre un clúster productivo bajo acceso restringido; por ello no se
publican los registros crudos del verificador ni los eventos del operador (se facilitan a
petición). Los datos limpios, el verificador, los manifiestos y el suplemento bastan para
auditar los resultados y replicar el diseño en un clúster equivalente.
