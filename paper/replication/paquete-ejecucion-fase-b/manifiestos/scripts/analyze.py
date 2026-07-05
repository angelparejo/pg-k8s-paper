#!/usr/bin/env python3
"""Estadistica no parametrica sobre results.csv, sin dependencias (air-gapped).

results.csv: experimento,operador,rep,t0,t1,rto
Salida: mediana/p95 por grupo, Mann-Whitney U (cnpg vs zalando por escenario),
Kruskal-Wallis y Spearman para los niveles de latencia F4.
"""
import sys, csv, math, re
from collections import defaultdict

def median(v):
    s = sorted(v); n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

def pct(v, p):
    s = sorted(v)
    k = (len(s) - 1) * p / 100
    f, c = int(k), min(int(k) + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)

def ranks(all_vals):
    s = sorted(range(len(all_vals)), key=lambda i: all_vals[i])
    r = [0.0] * len(all_vals); i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and all_vals[s[j + 1]] == all_vals[s[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[s[k]] = avg
        i = j + 1
    return r

def mann_whitney(a, b):
    vals = a + b
    r = ranks(vals)
    ra = sum(r[: len(a)])
    u1 = ra - len(a) * (len(a) + 1) / 2
    u2 = len(a) * len(b) - u1
    u = min(u1, u2)
    mu = len(a) * len(b) / 2
    sd = math.sqrt(len(a) * len(b) * (len(a) + len(b) + 1) / 12)
    z = (u - mu) / sd if sd else 0
    p = math.erfc(abs(z) / math.sqrt(2))          # aprox normal, bilateral
    return u, z, p

def kruskal(groups):
    vals = [x for g in groups for x in g]
    r = ranks(vals); n = len(vals); h = 0; i = 0
    for g in groups:
        rg = sum(r[i:i + len(g)]); i += len(g)
        h += rg * rg / len(g)
    return 12 / (n * (n + 1)) * h - 3 * (n + 1)   # comparar con chi2 (k-1 gl)

def spearman(x, y):
    rx, ry = ranks(x), ranks(y); n = len(x)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    return 1 - 6 * d2 / (n * (n * n - 1))

data = defaultdict(list)
for row in csv.reader(open(sys.argv[1] if len(sys.argv) > 1 else "results.csv")):
    if len(row) < 6:
        continue
    data[(row[0], row[1])].append(float(row[5]))

hdr_e, hdr_o = "experimento", "op"
print(f"{hdr_e:32s} {hdr_o:8s} n   mediana   p95")
for (exp, op), v in sorted(data.items()):
    print(f"{exp:32s} {op:8s} {len(v):<3d} {median(v):8.2f} {pct(v,95):8.2f}")

scen = defaultdict(dict)
for (exp, op), v in data.items():
    base = re.sub(r"-(cnpg|zalando)$", "", exp)   # emparejar por escenario
    scen[base][op] = v
print("\n-- Mann-Whitney (cnpg vs zalando) --")
for exp, ops in sorted(scen.items()):
    if "cnpg" in ops and "zalando" in ops:
        u, z, p = mann_whitney(ops["cnpg"], ops["zalando"])
        print(f"{exp:32s} U={u:.1f} z={z:+.2f} p~{p:.4f}")

for op in ("cnpg", "zalando"):
    lv, groups, flat_x, flat_y = [], [], [], []
    for (exp, o), v in sorted(data.items()):
        m = re.match(r"f4-iolatency-(\d+)ms", exp)
        if o == op and m:
            ms = int(m.group(1)); lv.append(ms); groups.append(v)
            flat_x += [ms] * len(v); flat_y += v
    if len(groups) > 1:
        print(f"\n-- F4 {op}: Kruskal-Wallis H={kruskal(groups):.2f} "
              f"(gl={len(groups)-1}) | Spearman rho={spearman(flat_x, flat_y):+.3f} --")
