#!/usr/bin/env python3
"""Parseo de F4 (latencia de E/S) - sin dependencias externas (air-gapped).

Lee los logs crudos de pgbench (--progress=1) producidos por run-f4-latency.sh,
descarta el calentamiento inicial, construye la serie por segundo, calcula
tps y percentiles de latencia por nivel, escribe f4-latency-series.csv y anexa
una fila-resumen por corrida (latencia media) a results.csv para que analyze.py
haga Kruskal-Wallis + Spearman sobre la curva dosis-respuesta.

Uso: ./parse-f4.py <dir_logs> [results.csv] [--warmup S]   (warmup por defecto 30 s)
Lineas esperadas: "progress: <t> s, <tps> tps, lat <lat> ms stddev <sd>"
"""
import sys, os, re, glob, csv

WARMUP = 30
if "--warmup" in sys.argv:
    WARMUP = int(sys.argv[sys.argv.index("--warmup") + 1])
pos = [a for a in sys.argv[1:] if not a.startswith("--") and not a.isdigit()]
logdir = pos[0] if pos else "data-f4"
resultscsv = pos[1] if len(pos) > 1 else "results.csv"

prog = re.compile(r"progress:\s+([\d.]+)\s+s,\s+([\d.]+)\s+tps,\s+lat\s+([\d.]+)\s+ms")
fname = re.compile(r"f4-(\d+)ms-rep(\d+)\.log$")

def median(v):
    s = sorted(v); n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
def pct(v, p):
    s = sorted(v); k = (len(s) - 1) * p / 100
    f = int(k); c = min(f + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)

series, tpsser, rows = {}, {}, []
seriescsv = os.path.join(logdir, "..", "f4-latency-series.csv")
with open(seriescsv, "w", newline="") as sf:
    sw = csv.writer(sf); sw.writerow(["nivel_ms", "rep", "segundo", "tps", "lat_ms"])
    for path in sorted(glob.glob(os.path.join(logdir, "f4-*ms-rep*.log"))):
        m = fname.search(path)
        if not m:
            continue
        lvl, rep = int(m.group(1)), int(m.group(2))
        lats, tp = [], []
        for line in open(path):
            mm = prog.search(line)
            if not mm:
                continue
            t = float(mm.group(1))
            if t < WARMUP:
                continue
            tps, lat = float(mm.group(2)), float(mm.group(3))
            tp.append(tps); lats.append(lat)
            sw.writerow([lvl, rep, t, tps, lat])
        if not lats:
            print(f"[warn] sin datos post-warmup en {path}"); continue
        series.setdefault(lvl, []).extend(lats)
        tpsser.setdefault(lvl, []).extend(tp)
        rows.append((f"f4-iolatency-{lvl}ms", "cnpg", rep, "", "", f"{sum(lats)/len(lats):.3f}"))

with open(resultscsv, "a", newline="") as f:
    w = csv.writer(f)
    for row in rows:
        w.writerow(row)

print(f"# F4: {len(rows)} corridas parseadas | warmup descartado={WARMUP}s")
print(f"# serie por segundo -> {os.path.normpath(seriescsv)}")
print(f"# filas-resumen (latencia media/corrida) anexadas a {resultscsv} -> correr analyze.py")
print()
print(f"{'nivel_ms':>8} {'n_seg':>6} {'tps_med':>9} {'lat_p50':>9} {'lat_p95':>9} {'lat_p99':>9}")
for lvl in sorted(series):
    v, t = series[lvl], tpsser[lvl]
    print(f"{lvl:>8} {len(v):>6} {median(t):>9.1f} {median(v):>9.2f} {pct(v,95):>9.2f} {pct(v,99):>9.2f}")
