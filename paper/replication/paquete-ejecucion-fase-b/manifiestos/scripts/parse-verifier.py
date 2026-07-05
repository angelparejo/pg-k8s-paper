#!/usr/bin/env python3
"""RPO y RTO desde los logs del tx-verifier (sin dependencias externas).

Uso:
  kubectl -n pg-chaos-lab logs deploy/tx-verifier-cnpg --timestamps > verifier.log
  ./parse-verifier.py verifier.log <host> <user> <password> <db>   # opcional: verificacion de visibilidad

RTO(cliente) = mayor hueco temporal entre COMMITs consecutivos.
RPO          = IDs con COMMIT en el log que NO existen en la tabla truth
               (requiere los 4 argumentos de conexion; usa psql).
"""
import sys, subprocess, datetime

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

gaps = [(b[1] - a[1]).total_seconds() for a, b in zip(commits, commits[1:])]
mx = max(gaps)
print(f"COMMITs registrados : {len(commits)}")
print(f"RTO (mayor hueco)   : {mx:.2f} s (entre id {commits[gaps.index(mx)][0]} y el siguiente)")

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
