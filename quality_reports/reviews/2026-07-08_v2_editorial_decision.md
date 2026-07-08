# Decisión Editorial — v2-experimental (Fase 3)

**Calibrada a:** revista primaria iberoamericana en español (CLEI EJ / RISTI / Ingeniare / Computación y Sistemas). Calibración genérica; indexación/cuartil a verificar por el autor antes de someter.
**Artículo:** *Análisis Multicapa de Operadores de PostgreSQL y Almacenamiento CSI en Kubernetes: un Marco de Evaluación y su Validación Empírica en CloudNativePG bajo Fallos Inyectados*
**Autor:** Angel A. Parejo R. (Universidad de Carabobo) · **Fecha:** 2026-07-08
**Síntesis de:** dominio (STRUCTURAL, 72/100, Mayor) + métodos (SKEPTIC, 81/100, Menor). Decisión por juicio editorial, no promediada. *(Producida por el agente `editor`; reemplaza la síntesis manual previa del orquestador, con la que concuerda.)*

## Decisión: REVISIÓN MAYOR (ligera)

Tomo partido por la severidad del árbitro de dominio (Mayor) sobre la de métodos (Menor), pero es una **Mayor ligera**: el hallazgo empírico es sólido, ninguna corrección obligatoria requiere nueva experimentación de núcleo, y una revisión diligente convierte el artículo. Ningún punto es Reject.

## 1. Clasificación

**FATAL:** ninguna. Las tres limitaciones de entorno (un operador, un backend SAN/FC, fallo de nodo no testeable por co-localización en `tcolp293`) están declaradas y fueron aceptadas en escritorio. El hallazgo central (visibilidad ante Kubernetes gobierna el failover; kill ~7.91 s vs failure ~36.75 s, 4.6×) sobrevive intacto a ambos informes.

**ADDRESSABLE (reencuadre/divulgación/texto, sin evidencia nueva de núcleo):**
- **A1 — Sobreafirmación "modelo formal + validación"** (Dominio #1 ≈ Métodos #3, convergencia): S=(O,K,M,D) organiza pero no predice; se refinó post hoc; F2 **falsó** la predicción. Corrección de encuadre.
- **A2 — Exclusión NO divulgada del outlier ~80 s (1.ª inyección F2)** (Métodos #1): roza la independencia de Mann-Whitney; asimetría con las exploratorias sí divulgadas. **Integridad: debe entrar al manuscrito.**
- **A3 — RPO=0 en F1 bajo async: falta el mecanismo** (Métodos #2), no solo el caveat.
- **A4 — Lagunas de posicionamiento** (Dominio #2/#3/#4): chaos-CI del propio CNPG (LitmusChaos), arXiv 2025 de inyección en K8s, [9] Avizienis mal caracterizado, [17]≠Jepsen.
- **A5 — Comparativas §IV.A (Zalando/Patroni)** presentadas como medición.
- **A6 — Higiene:** p-valor exacto, bug ARG_MAX de `parse-verifier.py`, depósito del paquete.

**TASTE:** forzar que la tupla *derive* el gradiente (Dominio #1a) o afilar una invariante falsable (Métodos #3a) son *una de dos* vías; el fondo (no reclamar predicción que no se tiene) es obligatorio, la forma es del autor. Sonda de RPO peor-caso = fortalecimiento, no bloqueo. Matiz "CP" de F3.

## 2. Arbitraje Mayor vs Menor
Los árbitros convergen en el diagnóstico (el encuadre promete de más) por caminos independientes (STRUCTURAL y SKEPTIC) ⇒ defecto real. Me inclino por **Mayor** porque: (1) el reencuadre toca la afirmación central (el título dice "y su Validación"); (2) la exclusión no divulgada (A2) es bandera de integridad que exige re-revisión; (3) el posicionamiento (A4) requiere trabajo bibliográfico real. Pero **ningún MUST requiere corrida experimental de núcleo** ⇒ Mayor ligera, no pesada.

## 3. Acciones

**MUST address (bloqueantes):**
1. **Reencuadrar la contribución (A1):** elegir vía —(a) visibilidad V(fallo,K) como dimensión de primera clase que *derive* el gradiente, o (b) rebajar el formalismo a vocabulario descriptivo y hacer central el hallazgo empírico— y ser consistente en título/abstract/§III/§VI. No reclamar "validación del modelo"; presentar la **refutación de F2** como el elemento probatorio más fuerte.
2. **Divulgar el outlier ~80 s de F2 (A2):** valor exacto, justificación mecanística (caché fría/pull de imagen), tratamiento simétrico, y ausencia de tendencia vs índice de repetición.
3. **Explicar el mecanismo de RPO=0 en F1 bajo async (A3)** citando código/doc de CNPG, o declararlo como límite de constructo.
4. **Cerrar posicionamiento (A4):** delimitar qué añade F1 sobre el chaos-CI de CNPG; literatura 2025; corregir Avizienis [9] y [17].
5. **Marcar §IV.A (A5)** como inferencia de documentación, no medición.
6. **p-valor exacto** (≈1.1×10⁻⁵) o declararlo aproximación; **corregir ARG_MAX** antes del depósito.

**SHOULD:** depositar `paper/replication/`; justificar independencia entre corridas; declarar efecto de la granularidad 0.2 s por escenario; nota de matiz "CP".

**MAY push back:** no forzar poder predictivo si se elige el reencuadre descriptivo; diferir la sonda de RPO peor-caso al segundo artículo; consolidación estilística.

## 4. Tier alcanzable
- **Resueltos los MUST → tier primario iberoamericano: aceptación probable** (objetivo declarado).
- **Tier secundario (FGCS/JSS): NO con solo texto.** Techo por evidencia, no encuadre: un operador, fallo de nodo real ausente, y RPO=0 en F1 sin red inter-nodo (3 instancias co-localizadas). **IEEE Access** sería el candidato secundario plausible, pero solo con la sonda de RPO peor-caso y reencuadre fuerte. Coherente con el plan secuencial: este artículo al primario ahora; el comparativo (multi-operador + fallo de nodo real + RPO peor-caso) genera la evidencia para el secundario y cita a este.

## 5. Resuelto por Nivel 1 vs persistente
**Resuelto (54→72 dominio; 60→81 métodos):** limitaciones declaradas; F2 cota inferior; F4 reconvertido; RPO trivial vs genuino; Fig.1 PDF vectorial; replicación async declarada (C19); verificador+granularidad 0.2 s (C21); todas las cifras reconcilian con los CSV; potencia desactivada para F1-vs-F2 por separación completa.
**Persiste (MUST de esta ronda):** A1 sobreafirmación del formalismo; A2 outlier no divulgado; A3 mecanismo RPO async; A4 posicionamiento; A6 higiene.

**Síntesis en una línea:** hallazgo empírico genuino y publicable, aritmética impecable, límites honestos; pero la envoltura "marco formal validado" promete lo que la evidencia no da y hay una exclusión sin divulgar → **Revisión Mayor (ligera)**, convertible sin experimentación de núcleo, con destino natural en el tier primario iberoamericano.
