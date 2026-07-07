#!/usr/bin/env python3
"""RPO y RTO desde los logs del tx-verifier (sin dependencias externas).

Uso:
  kubectl -n pg-chaos-lab logs deploy/tx-verifier-cnpg --timestamps > verifier.log
  ./parse-verifier.py verifier.log [<host> <user> <password> <db>]   # 4 args -> tambien RPO

RTO (cliente) = huecos temporales entre COMMITs consecutivos. Cada inyeccion con
outage de escritura produce un gap; con reps espaciadas (cool-down >=120 s) los gaps
>= UMBRAL son las RTO por repeticion. Resolucion ~100 ms (el verificador commitea rapido).
RPO = IDs con COMMIT en el log que NO existen en la tabla truth (requiere los 4 args).
"""
import sys, subprocess, datetime

UMBRAL = 1.0  # s: gap minimo para contarlo como outage de una repeticion

def ts(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))

log = open(sys.argv[1]).read().splitlines()
commits = []
for line in log:
    parts = line.split()
    if "COMMIT" in parts:
        i = parts.index("COMMIT")
        commits.append((int(parts[i + 1]), ts(parts[i + 2])))
if not commits:
    sys.exit("sin COMMITs en el log")

gaps = [((b[1] - a[1]).total_seconds(), a[0], a[1]) for a, b in zip(commits, commits[1:])]
mx = max(g[0] for g in gaps)
print(f"COMMITs registrados : {len(commits)}")
print(f"RTO (mayor hueco)   : {mx:.2f} s")

big = sorted([g for g in gaps if g[0] >= UMBRAL], reverse=True)
print(f"Outages >= {UMBRAL:.0f} s (n={len(big)}) -- una por repeticion:")
for k, (sec, id0, t0) in enumerate(big, 1):
    print(f"  #{k:>2}  RTO={sec:7.2f} s   tras id {id0}   @ {t0.isoformat()}")

if len(sys.argv) >= 6:
    host, user, pw, db = sys.argv[2:6]
    ids = ",".join(str(c[0]) for c in commits if c[0] > 0)
    q = f"SELECT id FROM truth WHERE id IN ({ids})"
    out = subprocess.run(["psql", "-h", host, "-U", user, "-d", db, "-tAc", q],
                         env={"PGPASSWORD": pw, "PATH": "/usr/bin:/bin"},
                         capture_output=True, text=True).stdout.split()
    visible = {int(x) for x in out}
    lost = [c[0] for c in commits if c[0] > 0 and c[0] not in visible]
    print(f"RPO (tx perdidas)   : {len(lost)}  {lost[:20]}")
