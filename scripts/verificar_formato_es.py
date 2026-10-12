#!/usr/bin/env python3
"""Verifica el formato tipografico de un PDF en espanol.

Revisa el corte de palabras a final de linea contra las reglas de silabeo del
espanol, y algunas comprobaciones de maquetacion. Solo biblioteca estandar;
necesita pdftotext (poppler) en el PATH.

Uso: python3 scripts/verificar_formato_es.py archivo.pdf [...]
"""
import re
import subprocess
import sys
from pathlib import Path

VOCALES = set("aeiouáéíóúü")
# Digrafos que representan un solo fonema: no se pueden partir.
INSEPARABLES = ("ch", "ll", "rr", "gu", "qu")
# Grupos consonanticos que pasan enteros a la silaba siguiente.
# "kl"/"kr" no son grupos del espanol: incluirlos marcaba como error el corte
# correcto de compuestos ingleses como "work-loads".
GRUPOS = ("bl", "br", "cl", "cr", "dr", "fl", "fr", "gl", "gr",
          "pl", "pr", "tr")


def paginas(pdf):
    return int(subprocess.run(["pdfinfo", str(pdf)], capture_output=True,
                              text=True, check=True)
               .stdout.split("Pages:")[1].split()[0])


def texto_por_columnas(pdf, cols=((60, 245), (305, 245))):
    """Texto columna a columna, pagina a pagina, conservando los guiones.

    Hace falta -layout para que el guion de final de linea sobreviva (sin el,
    pdftotext une la palabra partida y el corte desaparece). Pero -layout en un
    documento a dos columnas las pone lado a lado, y entonces la "linea
    siguiente" no es la continuacion. Se extrae por tanto cada columna aparte,
    recortando con -x/-W segun la geometria de la clase faraute: letterpaper,
    margenes de 2,5 cm y columnas de unos 227 pt.
    """
    trozos = []
    for pg in range(1, paginas(pdf) + 1):
        for x, w in cols:
            r = subprocess.run(
                ["pdftotext", "-layout", "-f", str(pg), "-l", str(pg),
                 "-x", str(x), "-y", "0", "-W", str(w), "-H", "792",
                 str(pdf), "-"],
                capture_output=True, text=True)
            if r.returncode == 0:
                trozos.append(r.stdout)
    return "\n".join(trozos)


def cortes(txt):
    """Devuelve (izquierda, derecha, linea) de cada palabra partida."""
    out = []
    lineas = txt.split("\n")
    for i, ln in enumerate(lineas[:-1]):
        m = re.search(r"(\w[\w'´áéíóúñüÁÉÍÓÚÑÜ]*)-\s*$", ln)
        if not m:
            continue
        if re.search(r"(doi|http|\.org|/)", ln[-40:], re.I):
            continue                      # DOI, URL o ruta: no es silabeo
        sig = lineas[i + 1].lstrip()
        # Con la opcion [revision] la clase numera las lineas y el numero cae
        # en el margen, delante de la continuacion. Una palabra partida nunca
        # continua con una cifra, asi que se descarta ese prefijo.
        sig = re.sub(r"^\d+\s+", "", sig)
        m2 = re.match(r"([\w'´áéíóúñüÁÉÍÓÚÑÜ]+)", sig)
        if not m2:
            continue
        out.append((m.group(1), m2.group(1), i + 1))
    return out


def revisa(izq, der):
    """Devuelve la lista de problemas del corte izq-der."""
    p = []
    a, b = izq.lower(), der.lower()
    entera = a + b

    if len(a) < 2:
        p.append("deja %d letra sola al final de linea" % len(a))
    if len(b) < 2:
        p.append("arrastra %d letra sola a la linea siguiente" % len(b))

    # digrafo partido entre las dos mitades
    for d in INSEPARABLES:
        if a.endswith(d[0]) and b.startswith(d[1]):
            p.append("parte el digrafo «%s», que es inseparable" % d)

    # grupo consonantico partido
    for g in GRUPOS:
        if a.endswith(g[0]) and b.startswith(g[1]):
            p.append("parte el grupo «%s», que no se separa" % g)

    # corte entre vocales: posible diptongo roto
    if a and b and a[-1] in VOCALES and b[0] in VOCALES:
        fuertes = set("aeoáéó")
        if not (a[-1] in fuertes and b[0] in fuertes):
            p.append("parte un posible diptongo («%s|%s»)" % (a[-1], b[0]))

    # siglas, identificadores y cifras
    if izq.isupper() and len(izq) >= 2:
        p.append("parte una sigla o palabra en versales")
    # nombre propio en camelCase (CloudNativePG, PostgreSQL...): el corte
    # rompe la marca y queda feo aunque el silabeo sea legal
    completo = izq + der
    if re.search(r"[a-z][A-Z]", completo):
        p.append("parte un nombre en camelCase («%s»)" % completo)
    if any(c.isdigit() for c in entera):
        p.append("parte una expresion con cifras")
    if "_" in entera or entera.count(".") > 0:
        p.append("parte un identificador tecnico")
    return p


def analiza(pdf):
    txt = texto_por_columnas(pdf)
    cs = cortes(txt)
    print("=" * 66)
    print("%s" % Path(pdf).name)
    print("=" * 66)
    print("cortes de palabra a final de linea: %d" % len(cs))

    problemas = []
    for izq, der, ln in cs:
        ps = revisa(izq, der)
        if ps:
            problemas.append((izq, der, ln, ps))

    if not problemas:
        print("  Sin cortes incorrectos segun las reglas del espanol.")
    else:
        print("  %d corte(s) a revisar:" % len(problemas))
        for izq, der, ln, ps in problemas:
            print("    linea %-5d %s-|%s" % (ln, izq, der))
            for x in ps:
                print("               -> %s" % x)

    # maquetacion
    print("\nmaquetacion:")
    lineas = [l for l in txt.split("\n") if l.strip()]
    sueltas = sum(1 for l in lineas if len(l.strip()) < 3)
    print("  lineas con menos de 3 caracteres: %d" % sueltas)
    guiones = txt.count("—")
    print("  rayas (—): %d" % guiones)
    for mal in ("ů", "£", "�", "??"):
        n = txt.count(mal)
        if n:
            print("  ALERTA glifo «%s»: %d" % (mal, n))
    return len(problemas)


if __name__ == "__main__":
    archivos = sys.argv[1:]
    if not archivos:
        print(__doc__)
        sys.exit(2)
    total = 0
    for f in archivos:
        total += analiza(f)
        print()
    sys.exit(1 if total else 0)
