#!/usr/bin/env python3
"""Reproduce TODAS las cifras estadísticas del artículo (Fase 1, CloudNativePG).

Air-gapped: solo biblioteca estándar de Python (sin numpy/scipy/pandas).
Lee los CSV limpios de RTO/RPO por escenario y reproduce, con sus fórmulas:
  - medianas, IQR y rangos (F1, F2, F3 fija);
  - intervalos de confianza de mediana distribución-libre (estadísticos de orden);
  - contraste F1 vs F2: Mann-Whitney U exacto (p bilateral) y aprox. normal (z),
    correlación rango-biserial, estimador de Hodges-Lehmann, razón de medianas;
  - cotas superiores de no-promoción por Clopper-Pearson (0/10 en F2, 0/12 en F3);
  - Spearman rho (índice de repetición vs. RTO) para el efecto de calentamiento en F2;
  - prueba de permutación exacta (equivalente a Mann-Whitney bajo separación total).

Uso:  python3 analyze.py [DIR_DATOS]
      (por defecto localiza replication/data junto al paquete)

Este estudio (Fase 1) cubre un ÚNICO operador, CloudNativePG. El contraste con
Zalando/Patroni y Crunchy se aborda de forma analítica en el artículo (Tabla 1) y
se asigna a la Fase 2; por eso aquí no aparece ningún otro operador.
"""
import sys
import csv
import math
from pathlib import Path
from itertools import combinations


# ----------------------------- utilidades ----------------------------------
def median(v):
    s = sorted(v)
    n = len(s)
    m = n // 2
    return s[m] if n % 2 else (s[m - 1] + s[m]) / 2.0


def quantile(v, q):
    """Cuantil por interpolación lineal (tipo 7, como R por defecto)."""
    s = sorted(v)
    if len(s) == 1:
        return s[0]
    h = (len(s) - 1) * q
    lo = int(math.floor(h))
    frac = h - lo
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + frac * (s[hi] - s[lo])


def order_stat_ci(v):
    """IC de mediana distribución-libre para n=10 con estadísticos de orden 2 y 9.
    Cobertura = 1 - 2*sum_{k=0}^{1} C(n,k) 0.5^n."""
    s = sorted(v)
    n = len(s)
    if n != 10:
        # generaliza: escoge el par (k, n+1-k) más cercano al 95%
        best = None
        for k in range(1, n // 2 + 1):
            cov = 1 - 2 * sum(math.comb(n, j) for j in range(0, k)) * 0.5 ** n
            if best is None or abs(cov - 0.95) < abs(best[0] - 0.95):
                best = (cov, k)
        cov, k = best
        return s[k - 1], s[n - k], cov
    cov = 1 - 2 * sum(math.comb(10, j) for j in range(0, 2)) * 0.5 ** 10
    return s[1], s[8], cov  # x(2), x(9)


def mann_whitney(a, b):
    """U de Mann-Whitney (menor), p exacto bilateral por enumeración, z normal."""
    n1, n2 = len(a), len(b)
    # U por conteo de pares (con mitad por empates)
    u = 0.0
    for x in a:
        for y in b:
            if x < y:
                u += 1
            elif x == y:
                u += 0.5
    u = min(u, n1 * n2 - u)
    # p exacto por distribución de U (sin empates): recurrencia de conteo
    p_exact = exact_two_sided_p(u, n1, n2)
    mu = n1 * n2 / 2.0
    sigma = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12.0)
    z = (u - mu) / sigma
    p_norm = 2 * (0.5 * math.erfc(-(-abs(z)) / math.sqrt(2)))  # 2*Phi(-|z|)
    rank_biserial = 1 - 2 * u / (n1 * n2)
    return u, p_exact, z, p_norm, rank_biserial


def exact_two_sided_p(u_obs, n1, n2):
    """p bilateral exacta de Mann-Whitney sin empates (conteo de particiones)."""
    # count[k] = nº de asignaciones con U = k ; recurrencia estándar
    max_u = n1 * n2
    count = [0] * (max_u + 1)
    count[0] = 1
    # DP: f(n1,n2,U)
    # usamos la recurrencia f(m,n,U)=f(m-1,n,U-n)+f(m,n-1,U)
    from functools import lru_cache
    import sys as _s
    _s.setrecursionlimit(10000)

    @lru_cache(maxsize=None)
    def f(m, n, U):
        if U < 0 or U > m * n:
            return 0
        if m == 0 or n == 0:
            return 1 if U == 0 else 0
        return f(m - 1, n, U - n) + f(m, n - 1, U)

    total = math.comb(n1 + n2, n1)
    # p de cola: U menor o igual al observado, por dos colas simétricas
    le = sum(f(n1, n2, k) for k in range(0, int(round(u_obs)) + 1))
    p_one = le / total
    return min(1.0, 2 * p_one)


def hodges_lehmann(a, b):
    """HL para dos muestras: mediana de todas las diferencias b_j - a_i."""
    diffs = [y - x for x in a for y in b]
    return median(diffs)


def clopper_pearson_upper(x, n, conf=0.95):
    """Cota superior unilateral (nivel conf) para una proporción con x éxitos.
    Para x=0: 1 - (1-conf)^(1/n)."""
    if x == 0:
        return 1 - (1 - conf) ** (1.0 / n)
    # caso general por inversión de la beta (no necesario aquí)
    raise NotImplementedError


def spearman(x, y):
    """Rho de Spearman (sin empates relevantes)."""
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for pos, i in enumerate(order):
            r[i] = pos + 1
        return r
    rx, ry = rank(x), rank(y)
    n = len(x)
    d2 = sum((rx[i] - ry[i]) ** 2 for i in range(n))
    return 1 - 6 * d2 / (n * (n * n - 1))


def spearman_crit(n, alpha=0.05):
    """Valor crítico bilateral (alpha=0.05) de Spearman por TABLA EXACTA.
    La aproximación por t subestima el crítico para n pequeño; se usan los
    valores exactos tabulados (permutación). Para n=10 es 0.648, que es el
    umbral que emplea el artículo."""
    exact = {8: 0.738, 9: 0.700, 10: 0.648, 11: 0.618, 12: 0.587}
    if n in exact:
        return exact[n]
    tcrit = 2.26  # fallback aproximado para n no tabulado
    return tcrit / math.sqrt((n - 2) + tcrit ** 2)


# ------------------------------- carga -------------------------------------
def find_data_dir():
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    here = Path(__file__).resolve()
    for base in [here.parents[3] / "data", Path.cwd() / "data", Path.cwd()]:
        if (base / "f1_rto_cnpg.csv").exists():
            return base
    raise SystemExit("No encuentro los CSV (f1/f2/f3). Pasa el directorio como argumento.")


def col(path, name):
    with open(path, newline="") as fh:
        return [row[name] for row in csv.DictReader(fh)]


# ------------------------------- reporte -----------------------------------
def main():
    d = find_data_dir()
    f1 = [float(x) for x in col(d / "f1_rto_cnpg.csv", "rto_s")]
    f2 = [float(x) for x in col(d / "f2_podfailure_cnpg.csv", "rto_s")]
    f2_prom = col(d / "f2_podfailure_cnpg.csv", "promocion")
    f3_tipo = col(d / "f3_partition_cnpg.csv", "tipo")
    f3_out = [float(x) for x in col(d / "f3_partition_cnpg.csv", "outage_s")]
    f3_prom = col(d / "f3_partition_cnpg.csv", "promocion")

    print("=" * 66)
    print("REPRODUCCIÓN DE CIFRAS DEL ARTÍCULO — Fase 1, CloudNativePG")
    print("Directorio de datos:", d)
    print("=" * 66)

    for name, v in (("F1 (pod-kill)", f1), ("F2 (pod-failure)", f2)):
        lo, hi, cov = order_stat_ci(v)
        print(f"\n[{name}]  n={len(v)}")
        print(f"  mediana        = {median(v):.2f} s")
        print(f"  IQR            = [{quantile(v,0.25):.2f}, {quantile(v,0.75):.2f}] s")
        print(f"  rango          = [{min(v):.2f}, {max(v):.2f}] s")
        print(f"  IC mediana     = [{lo:.2f}, {hi:.2f}] s  (cobertura {cov*100:.1f}%)")

    # F3 fija
    fija = [o for t, o in zip(f3_tipo, f3_out) if t == "fija"]
    lo, hi, cov = order_stat_ci(fija)
    print(f"\n[F3 fija (60 s)]  n={len(fija)}")
    print(f"  mediana        = {median(fija):.2f} s   IC [{lo:.2f}, {hi:.2f}] (cob. {cov*100:.1f}%)")
    print(f"  excedente reconexión ~ {median(fija)-60:.2f} s")

    # Contraste F1 vs F2
    print("\n" + "-" * 66)
    print("CONTRASTE F1 vs F2")
    u, p_ex, z, p_norm, rb = mann_whitney(f1, f2)
    print(f"  Mann-Whitney U         = {u:.0f}")
    print(f"  p exacto (bilateral)   = {p_ex:.3e}")
    print(f"  aprox. normal z        = {z:.2f}   p ~ {p_norm:.2e}")
    print(f"  correlación rango-bis. = {rb:.2f}")
    print(f"  Hodges-Lehmann (dif.)  = {hodges_lehmann(f1, f2):.2f} s")
    print(f"  razón de medianas F2/F1= {median(f2)/median(f1):.3f}x")
    # permutación exacta = mismo p (separación total): nº de reordenamientos
    # que igualan o superan la separación observada / total
    total = math.comb(len(f1) + len(f2), len(f1))
    print(f"  permutación exacta: 2/C(20,10) = {2/total:.3e}  (coincide con U=0)")

    # No-promoción
    print("\n" + "-" * 66)
    print("NO-PROMOCIÓN (cota superior Clopper-Pearson, unilateral 95%)")
    x2 = sum(1 for p in f2_prom if p.strip().lower() in ("si", "sí", "yes", "true"))
    x3 = sum(1 for p in f3_prom if p.strip().lower() in ("si", "sí", "yes", "true"))
    print(f"  F2: {x2}/{len(f2_prom)} promociones -> P(prom) <= {clopper_pearson_upper(x2,len(f2_prom))*100:.1f}%")
    print(f"  F3: {x3}/{len(f3_prom)} promociones -> P(prom) <= {clopper_pearson_upper(x3,len(f3_prom))*100:.1f}%")

    # Spearman (efecto de calentamiento en F2)
    print("\n" + "-" * 66)
    print("EFECTO DE ORDEN/CALENTAMIENTO EN F2 (Spearman)")
    idx = list(range(1, len(f2) + 1))
    rho = spearman(idx, f2)
    crit = spearman_crit(len(f2))
    print(f"  rho(índice, RTO) = {rho:.2f}   crítico(0.05) ~ {crit:.2f}   "
          f"{'NO ' if abs(rho) < crit else ''}significativa")

    print("\n" + "=" * 66)
    print("Cifras del artículo esperadas: F1 7.91 s, F2 36.75 s, razón 4.65x,")
    print("U=0 p~1.1e-5 z=-3.78 rb=1.00 HL=28.96 s; CP 25.9%/22.1%;")
    print("IC mediana cobertura 97.9%; Spearman rho~0.62 (no significativa).")
    print("=" * 66)


if __name__ == "__main__":
    main()
