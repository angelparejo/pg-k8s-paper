#!/usr/bin/env python3
"""Fija el DOI de Zenodo en el paquete Faraute y recompila los PDF afectados.

Sustituye los marcadores de posición del DOI ('DOI por asignar' y
'10.5281/zenodo.XXXXXXX') por el *concept DOI* real reservado en Zenodo, en
todos los archivos que lo declaran, y deja el depósito listo para publicar.

Uso:
    python3 scripts/set_zenodo_doi.py 10.5281/zenodo.1234567
    python3 scripts/set_zenodo_doi.py 1234567              # se completa el prefijo
    python3 scripts/set_zenodo_doi.py --check              # solo informa el estado
    python3 scripts/set_zenodo_doi.py <doi> --dry-run      # muestra sin escribir
    python3 scripts/set_zenodo_doi.py <doi> --no-compile   # no recompila ni rearma el ZIP

Qué toca (y por qué son dos grupos distintos):
  * Campos DOI reales -> sustitución literal del marcador:
        paper/faraute/main.tex
        paper/faraute/carta_al_editor.md
        paper/faraute/main_referencia_extendida_18pp.tex
        paper/faraute/replication/supplement/suplemento.tex
        paper/faraute/replication/CITATION.cff
  * Texto instructivo que MENCIONA el marcador -> se reescribe la frase entera,
    porque una sustitución literal produciría un sinsentido del tipo
    "sustituir 'DOI: 10.5281/...' por el concept DOI":
        paper/faraute/replication/.zenodo.json   (campo "notes")
        paper/faraute/replication/README.md      (sección "Cómo obtener el DOI")

Después de escribir: recompila main.tex y suplemento.tex (2 pasadas de pdflatex
cada uno), rearma zenodo-deposito-fase1.zip y verifica que no queden marcadores.

Solo biblioteca estándar. Sin dependencias externas.
"""

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Rutas relativas a la raíz del proyecto (INV-16: sin rutas absolutas)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
FARAUTE = ROOT / "paper" / "faraute"
REPLICATION = FARAUTE / "replication"

PLACEHOLDER_TEXT = "DOI por asignar"
PLACEHOLDER_NUM = "10.5281/zenodo.XXXXXXX"

# Documentos de proceso: describen el procedimiento y citan el marcador; no son
# campos DOI, así que ni se sustituyen ni cuentan como pendientes.
DOCS_DE_PROCESO = {"CHECKLIST_ENVIO_FARAUTE.md", "PENDIENTE_MI_LADO.md"}

# Archivos con campos DOI reales: (ruta, [(patrón, plantilla de reemplazo)])
# La plantilla usa {doi} y {url}.
LITERAL_TARGETS = [
    (FARAUTE / "main.tex", [(PLACEHOLDER_TEXT, "DOI: {doi}")]),
    (FARAUTE / "carta_al_editor.md", [(PLACEHOLDER_TEXT, "DOI: {doi}")]),
    (FARAUTE / "main_referencia_extendida_18pp.tex", [(PLACEHOLDER_TEXT, "DOI: {doi}")]),
    (REPLICATION / "supplement" / "suplemento.tex", [(PLACEHOLDER_TEXT, "DOI: {doi}")]),
    (
        REPLICATION / "CITATION.cff",
        [
            # incluye el comentario de la misma línea, que deja de aplicar
            (
                'doi: "' + PLACEHOLDER_NUM + '"   # reservar en Zenodo y sustituir',
                'doi: "{doi}"',
            ),
            ('doi: "' + PLACEHOLDER_NUM + '"', 'doi: "{doi}"'),
        ],
    ),
]

# Texto instructivo: se reescribe la frase completa.
NOTES_OLD = (
    "Reservar el DOI en Zenodo antes de publicar y sustituir 'DOI por asignar' / "
    "'10.5281/zenodo.XXXXXXX' en CITATION.cff, el suplemento y el manuscrito por "
    "el concept DOI."
)
NOTES_NEW = "Concept DOI del depósito: {doi} (citado en el manuscrito y en el suplemento)."

README_OLD = """## Cómo obtener el DOI (Zenodo)
1. Crear un nuevo *upload* en Zenodo y arrastrar el contenido de esta carpeta (o su ZIP).
2. En el formulario, **"Reserve DOI"** para obtener el DOI antes de publicar.
3. Sustituir `DOI por asignar` / `10.5281/zenodo.XXXXXXX` en `CITATION.cff`, `.zenodo.json`,
   el suplemento y el manuscrito (sección Disponibilidad de datos) por el **concept DOI**.
4. Publicar. El *concept DOI* (todas las versiones) es el que se cita en el artículo.
"""

README_NEW = """## DOI del depósito (Zenodo)
Este depósito se cita con su **concept DOI** (todas las versiones):

> {doi} — {url}

El mismo DOI aparece en `CITATION.cff`, `.zenodo.json`, el suplemento y el manuscrito
(sección de disponibilidad de datos). Si se publica una versión nueva del depósito, el
concept DOI no cambia: no hay que reeditar el artículo.
"""

INSTRUCTIONAL_TARGETS = [
    (REPLICATION / ".zenodo.json", [(NOTES_OLD, NOTES_NEW)]),
    (REPLICATION / "README.md", [(README_OLD, README_NEW)]),
]

# PDF a regenerar tras la sustitución: (directorio, archivo .tex sin extensión)
COMPILE_TARGETS = [
    (FARAUTE, "main"),
    (FARAUTE, "main_referencia_extendida_18pp"),
    (REPLICATION / "supplement", "suplemento"),
]

ZIP_PATH = FARAUTE / "zenodo-deposito-fase1.zip"


def normalizar_doi(entrada):
    """Acepta '10.5281/zenodo.N', 'zenodo.N', 'N' o una URL; devuelve el DOI canónico."""
    valor = entrada.strip()
    valor = re.sub(r"^https?://(dx\.)?doi\.org/", "", valor, flags=re.IGNORECASE)
    valor = re.sub(r"^doi:\s*", "", valor, flags=re.IGNORECASE)
    if re.fullmatch(r"\d{4,}", valor):
        valor = "10.5281/zenodo." + valor
    elif re.fullmatch(r"zenodo\.\d{4,}", valor, flags=re.IGNORECASE):
        valor = "10.5281/" + valor.lower()
    if not re.fullmatch(r"10\.5281/zenodo\.\d{4,}", valor):
        raise ValueError(
            "DOI no reconocido: %r. Se espera 10.5281/zenodo.<numero> "
            "(o solo el numero)." % entrada
        )
    return valor


def buscar_marcadores():
    """Devuelve {ruta relativa: [(nº de línea, línea)]} con marcadores pendientes.

    Se ignoran los documentos de proceso (checklists), que nombran el marcador
    al describir el procedimiento y no son campos DOI del depósito.
    """
    hallazgos = {}
    for ruta in sorted(FARAUTE.rglob("*")):
        if not ruta.is_file() or ruta.suffix.lower() in {".pdf", ".zip", ".jpg", ".png"}:
            continue
        if ruta.name in DOCS_DE_PROCESO:
            continue
        try:
            texto = ruta.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        lineas = [
            (n, linea.strip())
            for n, linea in enumerate(texto.splitlines(), 1)
            if PLACEHOLDER_TEXT in linea or PLACEHOLDER_NUM in linea
        ]
        if lineas:
            hallazgos[ruta.relative_to(ROOT)] = lineas
    return hallazgos


def aplicar(doi, dry_run):
    """Sustituye en todos los destinos. Devuelve el nº de archivos modificados."""
    url = "https://doi.org/" + doi
    modificados = 0
    for ruta, reglas in LITERAL_TARGETS + INSTRUCTIONAL_TARGETS:
        if not ruta.exists():
            print("  ! ausente, se omite: %s" % ruta.relative_to(ROOT))
            continue
        original = ruta.read_text(encoding="utf-8")
        texto = original
        aplicadas = 0
        for patron, plantilla in reglas:
            if patron not in texto:
                continue
            reemplazo = plantilla.format(doi=doi, url=url)
            aplicadas += texto.count(patron)
            texto = texto.replace(patron, reemplazo)
        if texto == original:
            print("  = sin cambios: %s" % ruta.relative_to(ROOT))
            continue
        if not dry_run:
            ruta.write_text(texto, encoding="utf-8")
        print("  %s %s (%d sustitucion/es)"
              % ("~" if dry_run else "OK", ruta.relative_to(ROOT), aplicadas))
        modificados += 1
    return modificados


def compilar():
    """Recompila los PDF (2 pasadas). Devuelve True si todos salieron bien."""
    if shutil.which("pdflatex") is None:
        print("  ! pdflatex no esta en el PATH: recompila a mano los PDF.")
        return False
    ok = True
    for directorio, nombre in COMPILE_TARGETS:
        tex = directorio / (nombre + ".tex")
        if not tex.exists():
            print("  ! ausente, se omite: %s" % tex.relative_to(ROOT))
            continue
        for pasada in (1, 2):
            resultado = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", nombre + ".tex"],
                cwd=str(directorio),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        log = directorio / (nombre + ".log")
        paginas = "?"
        if log.exists():
            texto_log = log.read_text(encoding="latin-1", errors="replace")
            hallado = re.search(r"Output written on .*?\((\d+) pages", texto_log)
            if hallado:
                paginas = hallado.group(1)
        if resultado.returncode == 0:
            print("  OK %s -> %s pp" % (tex.relative_to(ROOT), paginas))
        else:
            print("  ! fallo la compilacion de %s (ver %s)"
                  % (tex.relative_to(ROOT), log.relative_to(ROOT)))
            ok = False
    return ok


def rearmar_zip():
    """Reconstruye el ZIP del depósito desde replication/."""
    if not REPLICATION.is_dir():
        print("  ! no existe %s" % REPLICATION.relative_to(ROOT))
        return False
    excluidos = {".aux", ".log", ".out", ".toc", ".synctex.gz"}
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for ruta in sorted(REPLICATION.rglob("*")):
            if not ruta.is_file() or ruta.suffix.lower() in excluidos:
                continue
            zf.write(ruta, ruta.relative_to(REPLICATION.parent))
    tam = ZIP_PATH.stat().st_size // 1024
    print("  OK %s (%d KB)" % (ZIP_PATH.relative_to(ROOT), tam))
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Fija el DOI de Zenodo en el paquete Faraute y recompila."
    )
    parser.add_argument("doi", nargs="?", help="concept DOI (o solo el numero)")
    parser.add_argument("--check", action="store_true",
                        help="solo informar marcadores pendientes")
    parser.add_argument("--dry-run", action="store_true",
                        help="mostrar los cambios sin escribirlos")
    parser.add_argument("--no-compile", action="store_true",
                        help="no recompilar PDF ni rearmar el ZIP")
    args = parser.parse_args()

    if args.check or args.doi is None:
        pendientes = buscar_marcadores()
        if not pendientes:
            print("Sin marcadores de DOI pendientes en paper/faraute/.")
            return 0
        print("Marcadores de DOI pendientes:")
        for ruta, lineas in pendientes.items():
            for numero, linea in lineas:
                print("  %s:%d" % (ruta, numero))
                print("      %s" % (linea[:110] + ("..." if len(linea) > 110 else "")))
        if args.doi is None and not args.check:
            print("\nPasa el DOI para sustituirlos: "
                  "python3 scripts/set_zenodo_doi.py 10.5281/zenodo.1234567")
        return 0

    try:
        doi = normalizar_doi(args.doi)
    except ValueError as error:
        print("Error: %s" % error, file=sys.stderr)
        return 2

    print("DOI a fijar: %s" % doi)
    print("\n1) Sustitucion en archivos")
    modificados = aplicar(doi, args.dry_run)
    if args.dry_run:
        print("\n(dry-run: no se escribio nada)")
        return 0
    if modificados == 0:
        print("\nNada que sustituir: los marcadores ya estaban resueltos.")

    if not args.no_compile:
        print("\n2) Recompilacion de PDF")
        compilar()
        # main_final_12pp.pdf es la copia entregable de main.pdf
        entregable = FARAUTE / "main_final_12pp.pdf"
        principal = FARAUTE / "main.pdf"
        if principal.exists():
            shutil.copyfile(principal, entregable)
            print("  OK %s sincronizado con main.pdf" % entregable.relative_to(ROOT))
        print("\n3) Rearmado del ZIP del deposito")
        rearmar_zip()

    print("\n4) Verificacion")
    pendientes = buscar_marcadores()
    if pendientes:
        print("  ! QUEDAN marcadores:")
        for ruta, lineas in pendientes.items():
            for numero, _ in lineas:
                print("      %s:%d" % (ruta, numero))
        return 1
    print("  OK sin marcadores de DOI pendientes.")
    print("\nListo. Revisa main_final_12pp.pdf y publica el deposito en Zenodo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
