# Síntesis de validaciones y recomendaciones — Conversión Faraute
**Fecha:** 2026-08-12 · **Manuscrito:** `paper/faraute/main.tex` (19 pp, compila limpio)

## Puntajes de las validaciones
| Validación | Agente | Puntaje | Veredicto |
|-----------|--------|---------|-----------|
| V1a Formato+fidelidad | writer-critic | **70/100** | No submittable (bloqueante: 19>12 pp) |
| V1b Build/integridad | verifier | **PASS** | Compila; 300 dpi OK; figuras a color |
| V2a Dominio | domain-referee | **80/100** | Revisión Menor |
| V2b Métodos | methods-referee | **79/100** | Revisión Mayor (limítrofe) |

**Estado:** la conversión es fiel y de alta calidad (cifras 100% correctas y verificadas dos veces; 27/27 citas autor-año correctas; bibliografía Faraute alfabética; compila sin warnings). **No es submittable tal cual** por un bloqueante duro (extensión) y un conjunto acotado de arreglos. Ninguna objeción de los árbitros exige nuevos experimentos.

---

## GRUPO A — Formato Faraute (mecánico, bajo riesgo, sin tocar ciencia)
| # | Acción | Origen |
|---|--------|--------|
| A1 | Mover las leyendas de **Tabla 1 y Tabla 2 DEBAJO** del cuerpo (Faraute punto 8). | writer-critic (MAYOR) |
| A2 | Recortar el resumen a **<150 palabras** (hoy ~151). | writer-critic, INV-5 |
| A3 | Corregir **overfull hbox** de la Ec. de visibilidad (línea 379): partir el conjunto en dos líneas. | writer-critic, verifier |
| A4 | Reintroducir silabeo español (babel spanish vía `provide=*`, o `\usepackage{polyglossia}`, o cargar hyphenation). | writer-critic |
| A5 | Añadir nota **"Fuente: mediciones del piloto."** a Fig. 3 y Fig. 4. | writer-critic, INV-2 |
| A6 | Limpiar archivos auxiliares del directorio (`diag.*`, `pass*.txt`, etc.). | verifier |

## GRUPO B — Extensión ≤12 pp (BLOQUEANTE — requiere decisión de alcance)
El cuerpo tiene ~9.300 palabras → ~19 pp a 12pt/2-col (densidad real ~570 palabras/pág). Para ≤12 pp hay que reducir ~35-40%. Opciones:
- **B1 Recorte editorial:** condensar §4 (Análisis comparativo, muy expositiva y solapada con Tabla 1) y §7 (Discusión, reitera limitaciones de §5-§6); mover detalle metodológico fino (§5.2 cadencia del verificador, exclusiones) a notas al pie.
- **B2 Material complementario:** núcleo ≤12 pp + apéndice online (detalle estadístico, exclusiones, F4).
- **B3 No recortar** (mantener 19 pp) — incumple Faraute; solo válido si se reconsidera tipo/revista.

## GRUPO C — Revisiones científicas de los árbitros (contenido/prosa)
| # | Acción | Origen | Prioridad |
|---|--------|--------|-----------|
| C1 | **Citar y posicionar frente a Jepsen/Kingsbury** (el tx-verifier es verificación de consistencia bajo partición) en Trabajos Relacionados. | domain (MAYOR 1) | Alta |
| C2 | **Reencuadrar la contribución** hacia el predicado de visibilidad V(fallo,K); degradar S=(O,K,M,D) a andamiaje descriptivo. | domain (MAYOR 2) | Alta |
| C3 | **Acotar en resumen/conclusiones** que las magnitudes RTO/RPO provienen de topología co-localizada intra-nodo; lo que se sostiene es el contraste F1/F2 y el mecanismo. | domain (M3), methods (menor 1) | Alta |
| C4 | Reencuadrar el **p-valor saturado**: reconocer que 1,1e-5 es el piso teórico para n=10; peso probatorio en tamaño de efecto (rango-biserial 1,00; HL 28,96 s) y mecanismo. | methods (MAYOR 2) | Media |
| C5 | **Prueba de permutación por bloques** (respeta orden temporal) como robustez ante la deriva ρ≈0,62; se mantendrá por separación completa. | methods (MAYOR 1) | Media |
| C6 | Explicar la **semántica del verificador ante ACK perdido** (reintento de BIGINT ya confirmado: ¿ON CONFLICT/idempotencia?) y nº de casos frontera — condiciona RPO=0. | methods (MAYOR 3) | Alta |
| C7 | Declarar **precisión coherente con ±0,2 s** (o distinguir resolución de timestamp vs. sondeo). | methods (MAYOR 4) | Media |
| C8 | Declarar **simetría de exclusiones** (¿1.ª inyección de F1 también?) y análisis de sensibilidad con/sin. | methods (MAYOR 5) | Media |
| C9 | Anclar la fuente del "comportamiento anticipado" que F2 refuta (evitar hombre de paja). | domain (M4) | Media |
| C10 | Etiquetar Clopper–Pearson como **unilateral 95%**; precisar cota "CP" de F3; nota de F2 cota inferior en Tabla 2. | methods (varios) | Baja |

## GRUPO D — Referencias (factual — verificar antes de editar)
| # | Acción | Origen |
|---|--------|--------|
| D1 | **Burckhardt → Sebastian (S.)**, no M. | domain (menor 2) |
| D2 | **Taft (CockroachDB) → Rebecca (R.)**, no A. | domain, writer-critic |
| D3 | Reforzar cita **CSI** (spec versionada) en vez de URL genérica. | domain |
| D4 | Añadir doc oficial de PostgreSQL (`synchronous_commit`/streaming) para anclar RPO. | domain |
| D5 | Verificación web de las 27 referencias (la memoria del proyecto advierte ~40% con problemas). | memoria proyecto |

## GRUPO E — Figuras y datos (decisión)
| # | Acción | Origen |
|---|--------|--------|
| E1 | Convertir las 5 figuras a **escala de grises** (300 dpi ya OK) — Faraute punto 9. Riesgo: Fig. 3/4 usan color para distinguir F1/F2. | verifier, writer-critic |
| E2 | Depósito público (Zenodo/DOI) de datos limpios + tx-verifier + scripts + manifiestos; reservar "a petición" solo para crudos de producción. | methods (MAYOR 6) |

---

## Recomendación de secuencia
1. **Autorizar GRUPO A** (formato seguro) → reintento de writer-critic (esperado ≥80 salvo el bloqueante de páginas).
2. **Decidir GRUPO B** (estrategia de extensión) — es la palanca que desbloquea el envío.
3. **Autorizar GRUPO C** selectivo (C1, C2, C3, C6 son los de mayor impacto para los árbitros).
4. **GRUPO D/E** antes del envío final.

**Compuerta:** nada se aplica sin autorización del autor (según lo solicitado).
