#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Silabeador español y generador de excepciones \\hyphenation{} para LaTeX.

ESTADO (2026-08-17): herramienta de CONTINGENCIA, no se usa en el flujo normal.
El 16-08 se instaló `texlive-lang-spanish`, así que esta instalación de TeX ya
parte el castellano con los patrones reales y no hace falta ninguna tabla de
excepciones. Conviene conservar el guion porque el entorno es air-gapped y la
instalación costó (el DNS de la máquina está caído): si el proyecto se mueve a
un TeX sin patrones españoles, esto lo suple en un comando.

Advertencia si se vuelve a usar: la salida NO se carga sola. Hay que añadir
`\\input{silabeo-es}` en el preámbulo del documento. En agosto de 2026 se
descubrió que `paper/faraute/main.tex` nunca lo hizo, de modo que las 254 líneas
generadas fueron código muerto durante toda la vida del borrador.

Motivo original: la instalación de TeX de este entorno solo tenía patrones de silabeo
del inglés (`language.dat` = english / nohyphenation). `babel` con la opción
`spanish` fija los nombres ("Fig.", "Tabla") y \\lefthyphenmin/\\righthyphenmin,
pero no puede cargar patrones: los patrones solo se incorporan al construir el
formato. El resultado es que TeX parte el castellano con reglas inglesas
("mecan-ismos", "al-ma-ce-namien-to", "in-fraestruc-tura").

Como los patrones no son instalables aquí, se suministra a TeX una tabla de
excepciones exhaustiva: \\hyphenation{} tiene prioridad sobre los patrones y es
terminante para cada palabra listada. Al cubrir todo el vocabulario del
manuscrito, ningún reflujo del texto puede reintroducir un corte incorrecto.

Reglas implementadas (ortografía del español, RAE):
  - Dígrafos indivisibles: ch, ll, rr.
  - Grupos consonánticos indivisibles: consonante + l/r (bl, br, cl, cr, dr,
    fl, fr, gl, gr, kl, kr, pl, pr, tr). "tl" se separa (at-le-ta).
  - Entre núcleos vocálicos: V-CV, V-CCV / VC-CV, VC-CCV / VCC-CV, VCC-CCV.
  - Grupos vocálicos: diptongo (fuerte+débil, débil+fuerte, débil+débil) y
    triptongo no se parten; hiato (fuerte+fuerte, o débil tildada) sí.
  - Se respetan \\lefthyphenmin=2 y \\righthyphenmin=2.

Los tecnicismos no castellanos (Kubernetes, failover, workload...) se emiten
sin puntos de corte: en \\hyphenation{} eso los vuelve impartibles, que es
preferible a partirlos con reglas ajenas.

Uso:
    python3 scripts/silabeo_es.py <fuente.tex> [...] -o <salida.tex>
    python3 scripts/silabeo_es.py --demo palabra [palabra ...]

Solo biblioteca estándar (ver CLAUDE.md: scripting air-gapped).
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------- alfabeto ---

FUERTES = set("aeoáéó")
DEBILES_ATONAS = set("iuü")
DEBILES_TONICAS = set("íú")
VOCALES = FUERTES | DEBILES_ATONAS | DEBILES_TONICAS

DIGRAFOS = ("ch", "ll", "rr")
INSEPARABLES = {
    "bl", "br", "cl", "cr", "dr", "fl", "fr",
    "gl", "gr", "kl", "kr", "pl", "pr", "tr",
}

# Letras ajenas al castellano; su presencia marca la palabra como extranjera.
LETRAS_FORANEAS = set("kw")
# Terminaciones válidas de palabra en castellano.
FINALES_VALIDOS = set("aeiouáéíóúlrndszxyjc")

# Tecnicismos del dominio que deben viajar enteros aunque la heurística los
# tome por castellanos. Partir un nombre propio de software estorba al lector.
PROTEGIDAS = {
    "chaos", "mesh", "cluster", "clusters", "pod", "pods", "patroni", "spilo",
    "zalando", "prometheus", "grafana", "docker", "containerd", "etcd",
    "cloudnativepg", "postgresql", "postgres", "kubernetes", "kubelet",
    "kubectl", "namespace", "namespaces", "operator", "operators", "primary",
    "standby", "streaming", "commit", "commits", "quorum", "raft", "jepsen",
    "elle", "pgbench", "verifier", "provisioner", "sidecar", "runtime",
    "readonly", "rootfs", "fuse", "toda", "iochaos", "podchaos", "networkchaos",
}


def quitar_tildes(palabra):
    descompuesta = unicodedata.normalize("NFD", palabra)
    return "".join(c for c in descompuesta if unicodedata.category(c) != "Mn")


def es_extranjera(palabra):
    """Heurística conservadora: ante la duda, no partir."""
    if palabra in PROTEGIDAS:
        return True
    if LETRAS_FORANEAS & set(palabra):
        return True
    if any(d in palabra for d in ("sh", "th", "ck", "ss", "tt", "ff", "mm", "pp")):
        return True
    if palabra[-1] not in FINALES_VALIDOS:
        return True
    # Terminaciones inglesas frecuentes en la jerga del dominio.
    if re.search(r"(ing|ment|over|load|ware|less|ful)$", palabra):
        return True
    return False


# ---------------------------------------------------------------- segmentar ---


def _unidades(palabra):
    """Descompone en unidades: dígrafos y letras sueltas."""
    unidades, i = [], 0
    while i < len(palabra):
        if palabra[i:i + 2] in DIGRAFOS:
            unidades.append(palabra[i:i + 2])
            i += 2
        else:
            unidades.append(palabra[i])
            i += 1
    return unidades


def _es_vocal(unidad):
    return len(unidad) == 1 and unidad in VOCALES


def _parte_grupo_vocalico(grupo):
    """Puntos de corte internos de un grupo de vocales contiguas (hiatos).

    Devuelve los índices (relativos al grupo) tras los cuales se corta.
    """
    cortes = []
    i = 0
    while i < len(grupo) - 1:
        a, b = grupo[i], grupo[i + 1]
        # Triptongo: débil átona + fuerte + débil átona (estudiáis, buey).
        if (i + 2 < len(grupo)
                and a in DEBILES_ATONAS
                and b in FUERTES
                and grupo[i + 2] in DEBILES_ATONAS):
            i += 3
            continue
        if a in DEBILES_TONICAS or b in DEBILES_TONICAS:
            hiato = True                      # país, río, búho
        elif a in FUERTES and b in FUERTES:
            hiato = True                      # ca-os, le-er, a-é-re-o
        else:
            hiato = False                     # diptongo
        if hiato:
            cortes.append(i + 1)
            i += 1
        else:
            i += 2
    return cortes


def silabas(palabra):
    """Divide una palabra castellana en sílabas."""
    unidades = _unidades(palabra)

    # 'y' es consonante salvo al final de palabra tras vocal (rey, hay, muy).
    def vocal_en(k):
        u = unidades[k]
        if u == "y":
            return k == len(unidades) - 1 and k > 0 and _es_vocal(unidades[k - 1])
        return _es_vocal(u)

    # Agrupar en bloques alternos de vocales y consonantes.
    bloques = []
    for k, u in enumerate(unidades):
        tipo = "V" if vocal_en(k) else "C"
        if bloques and bloques[-1][0] == tipo:
            bloques[-1][1].append(u)
        else:
            bloques.append([tipo, [u]])

    # Puntos de corte, expresados como índice de unidad donde empieza sílaba.
    cortes = set()
    pos = [0]
    for tipo, us in bloques:
        pos.append(pos[-1] + len(us))

    for b, (tipo, us) in enumerate(bloques):
        inicio = pos[b]
        if tipo == "V":
            grupo = [u for u in us]
            for c in _parte_grupo_vocalico(grupo):
                cortes.add(inicio + c)
        else:
            # Solo las consonantes ENTRE dos núcleos vocálicos se reparten.
            hay_vocal_antes = b > 0 and bloques[b - 1][0] == "V"
            hay_vocal_despues = b + 1 < len(bloques) and bloques[b + 1][0] == "V"
            if not (hay_vocal_antes and hay_vocal_despues):
                continue
            n = len(us)
            if n == 1:
                corte = 0                                  # V-CV
            elif n == 2:
                par = "".join(us)
                corte = 0 if (par in INSEPARABLES or par in DIGRAFOS) else 1
            elif n == 3:
                ultimas = "".join(us[1:])
                corte = 1 if (ultimas in INSEPARABLES or ultimas in DIGRAFOS) else 2
            else:
                corte = 2                                  # VCC-CCV
            cortes.add(inicio + corte)

    # Reconstruir sílabas a partir de los índices de unidad.
    trozos, actual = [], []
    for k, u in enumerate(unidades):
        if k in cortes and actual:
            trozos.append("".join(actual))
            actual = []
        actual.append(u)
    if actual:
        trozos.append("".join(actual))
    return trozos


def punteada(palabra, lefthyphenmin=2, righthyphenmin=2):
    """Palabra con guiones en los cortes que TeX puede usar realmente."""
    trozos = silabas(palabra)
    if len(trozos) < 2:
        return palabra
    salida, acumulado = trozos[0], len(trozos[0])
    for trozo in trozos[1:]:
        restante = len(palabra) - acumulado
        if acumulado >= lefthyphenmin and restante >= righthyphenmin:
            salida += "-"
        salida += trozo
        acumulado += len(trozo)
    return salida


# ------------------------------------------------------------ extracción ----

# Comandos cuyo argumento es una etiqueta o ruta, no prosa.
CMD_NO_TEXTO = (
    "label", "ref", "cref", "Cref", "eqref", "cite", "citep", "citet",
    "input", "include", "includegraphics", "bibliography", "usepackage",
    "documentclass", "url", "href", "texttt", "verb", "hyphenation",
    "newcommand", "renewcommand", "definecolor", "pagestyle", "graphicspath",
)


def texto_plano(fuente):
    """Aproxima el texto visible de un .tex: fuera comentarios, matemáticas,
    verbatim y argumentos que no son prosa."""
    t = re.sub(r"(?<!\\)%.*", "", fuente)
    t = re.sub(r"\\begin\{(verbatim|lstlisting|tikzpicture)\}.*?\\end\{\1\}",
               " ", t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$", " ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", " ", t)
    t = re.sub(r"\\\[.*?\\\]", " ", t, flags=re.S)
    t = re.sub(r"\\begin\{(equation|align|gather|multline)\*?\}.*?"
               r"\\end\{\1\*?\}", " ", t, flags=re.S)
    for cmd in CMD_NO_TEXTO:
        t = re.sub(r"\\" + cmd + r"\*?(\[[^\]]*\])?(\{[^{}]*\})?", " ", t)
    t = re.sub(r"\\[a-zA-Z@]+\*?", " ", t)
    t = re.sub(r"[{}\\~^_&#]", " ", t)
    return t


PALABRA = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")


def palabras_de(texto, minimo=5):
    """Palabras candidatas a ser partidas por TeX, en minúsculas."""
    encontradas = set()
    for bruta in PALABRA.findall(texto):
        w = bruta.lower()
        if len(w) < minimo:
            continue          # TeX no parte por debajo de left+right hyphenmin
        if bruta.isupper():
            continue          # siglas
        encontradas.add(w)
    return encontradas


# ------------------------------------------------------------------- salida --


def bloque_hyphenation(palabras, ancho=72):
    """Genera el cuerpo del \\hyphenation{...} ordenado alfabéticamente."""
    entradas = []
    for w in sorted(palabras):
        entradas.append(w if es_extranjera(w) else punteada(w))
    lineas, actual = [], "  "
    for e in entradas:
        if len(actual) + len(e) + 1 > ancho:
            lineas.append(actual.rstrip())
            actual = "  "
        actual += e + " "
    if actual.strip():
        lineas.append(actual.rstrip())
    return entradas, lineas


CABECERA = """\
%% ===========================================================================
%%  silabeo-es.tex — excepciones de división silábica en español
%%  GENERADO POR scripts/silabeo_es.py — no editar a mano; regenerar con:
%%      python3 scripts/silabeo_es.py paper/faraute/main.tex \\
%%              -o paper/faraute/silabeo-es.tex
%%
%%  Esta instalación de TeX solo trae patrones de silabeo del inglés
%%  (language.dat = english/nohyphenation) y los patrones no se pueden cargar
%%  en tiempo de ejecución. Sin esta tabla, TeX parte el castellano con reglas
%%  inglesas: "mecan-ismos", "al-ma-ce-namien-to", "in-fraestruc-tura".
%%
%%  \\hyphenation{{}} tiene prioridad sobre los patrones y es terminante para
%%  cada palabra listada, así que cubrir todo el vocabulario del manuscrito
%%  impide que un reflujo del texto reintroduzca un corte incorrecto.
%%  Los tecnicismos no castellanos se listan sin guiones: quedan impartibles.
%%
%%  Palabras: {n}
%% ===========================================================================
\\hyphenation{{
{cuerpo}
}}
"""


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fuentes", nargs="*", type=Path, help="archivos .tex de entrada")
    p.add_argument("-o", "--salida", type=Path, help="archivo .tex a generar")
    p.add_argument("--demo", nargs="+", help="silabea las palabras dadas y termina")
    p.add_argument("--listar", action="store_true",
                   help="imprime una palabra por línea en vez del bloque LaTeX")
    args = p.parse_args(argv)

    if args.demo:
        for w in args.demo:
            marca = "  [extranjera: impartible]" if es_extranjera(w.lower()) else ""
            print(f"{w:<28} {'-'.join(silabas(w.lower()))}{marca}")
        return 0

    if not args.fuentes:
        p.error("indica al menos un .tex de entrada (o usa --demo)")

    palabras = set()
    for ruta in args.fuentes:
        palabras |= palabras_de(texto_plano(ruta.read_text(encoding="utf-8")))

    entradas, lineas = bloque_hyphenation(palabras)

    if args.listar:
        print("\n".join(entradas))
        return 0

    contenido = CABECERA.format(n=len(entradas), cuerpo="\n".join(lineas))
    if args.salida:
        args.salida.write_text(contenido, encoding="utf-8")
        print(f"{args.salida}: {len(entradas)} palabras "
              f"({sum(1 for e in entradas if '-' not in e)} impartibles)")
    else:
        sys.stdout.write(contenido)
    return 0


if __name__ == "__main__":
    sys.exit(main())
