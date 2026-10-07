#!/usr/bin/env python3
"""Detector de marcadores estilisticos asociados a texto generado por IA.

Analiza el cuerpo de un .tex en espanol y reporta los rasgos que los
detectores automaticos y los lectores humanos usan como senal: uniformidad
de longitud de frase, densidad de conectores formulaicos, tricolones,
construcciones "no solo X sino Y", guiones largos, y pobreza lexica.

No instala nada: solo biblioteca estandar.
"""
import re
import sys
import statistics
from collections import Counter
from pathlib import Path

# -------------------------------------------------------------------- limpieza
def cuerpo_tex(ruta):
    s = ruta.read_text(encoding="utf-8")
    ini = s.index("\\section{Introducci")
    fin = s.index("\\section*{Bibliograf")
    s = s[ini:fin]
    s = re.sub(r"\\begin\{(figure|table|tikzpicture|axis|tabularx)\*?\}.*?"
               r"\\end\{\1\*?\}", " ", s, flags=re.S)
    s = re.sub(r"%.*", " ", s)
    s = re.sub(r"\\(textit|textbf|emph|texttt|ref|cref|label|cite)\*?\{([^{}]*)\}", r"\2", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", s)
    s = re.sub(r"[{}$~\\]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def frases(t):
    partes = re.split(r"(?<=[.:;])\s+(?=[A-ZÁÉÍÓÚÑ¿«])", t)
    return [p.strip() for p in partes if len(p.split()) >= 4]

# ------------------------------------------------------------------ marcadores
CONECTORES = ["en primer lugar", "en segundo lugar", "por otro lado", "por otra parte",
              "es importante destacar", "cabe destacar", "cabe senalar", "cabe señalar",
              "en conclusion", "en conclusión", "en resumen", "en definitiva",
              "adicionalmente", "asimismo", "de igual manera", "de este modo",
              "en este sentido", "no obstante", "sin embargo", "por lo tanto",
              "por consiguiente", "en el ambito", "en el ámbito", "juega un papel",
              "desempena un papel", "desempeña un papel", "es fundamental",
              "resulta crucial", "vale la pena", "profundizar en", "abordar el desafio",
              "panorama", "robusto", "aprovechar", "destacar que"]

def analiza(ruta):
    t = cuerpo_tex(ruta)
    fs = frases(t)
    largos = [len(f.split()) for f in fs]
    pal = re.findall(r"[a-záéíóúñü]+", t.lower())

    print("=" * 62)
    print("MARCADORES DE ESTILO — %s" % ruta.name)
    print("=" * 62)
    print("palabras: %d | frases: %d" % (len(pal), len(fs)))

    media = statistics.mean(largos)
    desv = statistics.pstdev(largos)
    cv = desv / media
    print("\n[1] Longitud de frase")
    print("    media %.1f | desviacion %.1f | CV %.2f | rango %d-%d"
          % (media, desv, cv, min(largos), max(largos)))
    print("    %s  (CV<0.35 = sospechosamente uniforme; humano tipico 0.45-0.75)"
          % ("ALERTA" if cv < 0.35 else "OK"))

    print("\n[2] Conectores formulaicos")
    hits = Counter()
    bajo = t.lower()
    for c in CONECTORES:
        n = bajo.count(c)
        if n:
            hits[c] = n
    tasa = sum(hits.values()) / max(len(fs), 1)
    for c, n in hits.most_common(10):
        print("    %-26s %d" % (c, n))
    print("    total %d | %.3f por frase  %s"
          % (sum(hits.values()), tasa, "ALERTA" if tasa > 0.30 else "OK"))

    print("\n[3] Construcciones caracteristicas")
    pats = {
        "no solo ... sino": r"no s[oó]lo\b[^.]{0,90}\bsino\b",
        "tricolon (a, b y c)": r"\b\w+, \w+ y \w+\b",
        "guion largo (par)": r"—",
        "«no es X, es Y»": r"\bno es\b[^.]{0,50}\bsino\b",
        "«más que X, Y»": r"\bm[áa]s que\b[^.]{0,40},",
    }
    for nom, p in pats.items():
        n = len(re.findall(p, t, flags=re.I))
        print("    %-22s %3d  (%.3f/frase)" % (nom, n, n / max(len(fs), 1)))

    print("\n[4] Riqueza lexica")
    uni = len(set(pal))
    ttr = uni / len(pal)
    print("    tipos %d | TTR %.3f  %s" % (uni, ttr, "ALERTA" if ttr < 0.22 else "OK"))
    comunes = [w for w, n in Counter(pal).most_common(40)
               if len(w) > 6 and n >= 10]
    if comunes:
        print("    repetidas (>6 letras, >=10 veces): " + ", ".join(comunes[:12]))

    print("\n[5] Frases mas largas (revisar legibilidad)")
    for f in sorted(fs, key=lambda x: -len(x.split()))[:3]:
        print("    [%d pal] %s..." % (len(f.split()), f[:110]))


if __name__ == "__main__":
    destinos = sys.argv[1:] or ["paper/faraute/main.tex"]
    for d in destinos:
        analiza(Path(d))
        print()
