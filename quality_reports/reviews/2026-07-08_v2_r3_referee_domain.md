# Árbitro de DOMINIO — v2-experimental (Ronda 3)

**Fecha:** 2026-07-08 · **Campo:** Sistemas Distribuidos / Bases de Datos Cloud-Native · **Recomendación: Revisión Menor (al borde de Aceptar)** · **Puntuación: 85/100** (antes 83)

## Resumen
La Ronda 3 no introduce cambios estructurales —no hacían falta—: refina la precisión terminológica y liquida los cuatro residuos menores de la R2. El cambio de mayor sustancia de dominio es la terminología fiel a Kubernetes: nombrar F1 como *eliminación* del pod (pod-kill borra el objeto Pod vía la API) y F2 como *fallo sostenido* (pod-failure). No es cosmética: cierra el círculo argumental de la tesis central (visibilidad = existencia del objeto Pod ante el plano de control, no salud del pod).

## Dimensiones (Base R2 → Ahora)
| Dimensión | Peso | Base R2 | Ahora |
|---|---|---|---|
| Contribución/novedad | 30% | 84 | 86 |
| Posicionamiento | 25% | 82 | 84 |
| Sustancia | 20% | 86 | 87 |
| Validez externa | 15% | 76 | 77 |
| Ajuste (revista) | 10% | 84 | 85 |
| **Ponderado** | 100% | **83** | **85** |

## Residuos R2 — estado
1. "predice" en §III.A → **RESUELTO** ("anticipa, a partir de su comportamiento documentado"; usos restantes en líneas 30/73 son cláusulas de renuncia).
2. [27] no analizado → **RESUELTO** (línea 47: objeto vs. delta de Chen et al.).
3. Matiz "CP" → **RESUELTO** (nota Tabla II + §VI.A: operacional, no CAP formal).
4. Build Fig. 1 (PDF vs .svg) → **PENDIENTE de producción** (no verificable desde Markdown).

## Residuos restantes (no bloqueantes, ninguno de dominio)
1. Confirmar en el PDF final que se embebe el vectorial (PDF/TikZ) y no el `.svg`.
2. "A petición" es adecuado para el tier primario; el tier secundario en inglés exigirá artefacto público (Zenodo con manifiestos + verificador + scripts, sin datos sensibles).
3. Nit opcional: el resumen enumera F1–F3 pero no F4 (correcto, pero un lector podría preguntarse por el "cuarto escenario").

## Veredicto
83 → **85**: la terminología fiel a Kubernetes afila la tesis central y los cuatro residuos menores de la R2 quedan cerrados. **Revisión Menor al borde de Aceptar** — sustantivamente listo para el tier primario en español.
