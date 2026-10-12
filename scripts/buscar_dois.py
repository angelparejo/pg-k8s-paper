#!/usr/bin/env python3
"""Consulta Crossref para obtener el DOI de una lista de referencias.

Comprueba que el titulo devuelto se parece al buscado antes de aceptar el DOI,
para no asignar uno equivocado. Solo biblioteca estandar.

Uso: python3 scripts/buscar_dois.py
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from difflib import SequenceMatcher

API = "https://api.crossref.org/works"
CORREO = "angelparejo@gmail.com"   # Crossref pide un contacto en el User-Agent

# clave -> (titulo, primer autor, anio)
REFS = {
    "abadi2012":       ("Consistency tradeoffs in modern distributed database system design", "Abadi", 2012),
    "alquraan2018":    ("An analysis of network-partitioning failures in cloud systems", "Alquraan", 2018),
    "alvaro2018":      ("Abstracting the geniuses away from failure testing", "Alvaro", 2018),
    "avizienis2004":   ("Basic concepts and taxonomy of dependable and secure computing", "Avizienis", 2004),
    "bailis2013":      ("Eventual consistency today: limitations, extensions, and beyond", "Bailis", 2013),
    "basiri2016":      ("Chaos engineering", "Basiri", 2016),
    "burns2016":       ("Borg, Omega, and Kubernetes", "Burns", 2016),
    "chen2026":        ("An empirical evaluation of Kubernetes resilience in cloud-edge deployments using failure injection", "Chen", 2026),
    "gilbert2002":     ("Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services", "Gilbert", 2002),
    "gu2023":          ("Acto: Automatic End-to-End Testing for Operation Correctness of Cloud System Management", "Gu", 2023),
    "han2024":         ("PALF: Replicated Write-Ahead Logging for Distributed Databases", "Han", 2024),
    "kingsbury2021":   ("Elle: inferring isolation anomalies from experimental observations", "Kingsbury", 2021),
    "mega2023":        ("Orchestrating information governance workloads as stateful services using Kubernetes operator framework", "Mega", 2023),
    "mohan1992":       ("ARIES: a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging", "Mohan", 1992),
    "natella2016":     ("Assessing Dependability with Software Fault Injection: A Survey", "Natella", 2016),
    "schwarzkopf2013": ("Omega: flexible, scalable schedulers for large compute clusters", "Schwarzkopf", 2013),
    "sun2022":         ("Automatic Reliability Testing For Cluster Management Controllers", "Sun", 2022),
}

def normaliza(t):
    return re.sub(r"[^a-z0-9 ]", " ", t.lower()).split()

def parecido(a, b):
    return SequenceMatcher(None, " ".join(normaliza(a)), " ".join(normaliza(b))).ratio()

def consulta(titulo, autor, anio):
    q = urllib.parse.urlencode({
        "query.bibliographic": titulo,
        "query.author": autor,
        "rows": 5,
    })
    req = urllib.request.Request(
        f"{API}?{q}",
        headers={"User-Agent": f"faraute-bib/1.0 (mailto:{CORREO})"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        datos = json.load(r)
    mejor = None
    for it in datos.get("message", {}).get("items", []):
        t = (it.get("title") or [""])[0]
        p = parecido(titulo, t)
        a = None
        for campo in ("published-print", "published-online", "issued"):
            if it.get(campo, {}).get("date-parts", [[None]])[0][0]:
                a = it[campo]["date-parts"][0][0]
                break
        if mejor is None or p > mejor[0]:
            mejor = (p, it.get("DOI"), t, a, it.get("container-title", [""])[0] if it.get("container-title") else "")
    return mejor

def main():
    print("%-17s %-6s %-34s %s" % ("CLAVE", "COINC.", "DOI", "TITULO DEVUELTO"))
    print("-" * 110)
    hallados = {}
    for clave, (titulo, autor, anio) in REFS.items():
        try:
            m = consulta(titulo, autor, anio)
        except Exception as e:                      # red caida, 429, etc.
            print("%-17s  ERROR  %s" % (clave, e))
            continue
        if not m:
            print("%-17s  ----   sin resultados" % clave)
            continue
        p, doi, t, a, rev = m
        aviso = ""
        if p < 0.75:
            aviso = "  <-- COINCIDENCIA BAJA, revisar a mano"
        elif a and abs(a - anio) > 1:
            aviso = "  <-- ANIO DISTINTO (%s), revisar" % a
        else:
            hallados[clave] = doi
        print("%-17s %5.2f  %-34s %s%s" % (clave, p, doi or "-", t[:46], aviso))
        time.sleep(0.4)                              # cortesia con la API
    print("-" * 110)
    print("DOI aceptados automaticamente: %d de %d" % (len(hallados), len(REFS)))
    print(json.dumps(hallados, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    sys.exit(main())
