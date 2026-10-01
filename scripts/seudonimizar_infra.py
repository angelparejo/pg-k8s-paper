#!/usr/bin/env python3
"""Seudonimiza los identificadores de la infraestructura productiva del repositorio.

Motivo: el paquete de reproducibilidad se deposita públicamente en Zenodo y el
repositorio tiene remoto en GitHub. El manuscrito ya usaba el seudónimo
`nodo-lab-01`, pero el paquete de ejecución y varios documentos de trabajo
conservaban los nombres reales de los nodos del clúster, el inventario de los
cuatro clústeres CNPG ajenos (con la ubicación de sus primarios) y el correo
corporativo del autor. Nada de eso hace falta para reproducir el experimento y
su publicación expone infraestructura de un tercero.

Este guion aplica un mapeo fijo y explícito, en orden (lo más específico
primero), sobre todos los archivos de texto del repositorio.

Uso:
    python3 scripts/seudonimizar_infra.py --check     # informa qué queda por seudonimizar
    python3 scripts/seudonimizar_infra.py --dry-run   # muestra los cambios sin escribirlos
    python3 scripts/seudonimizar_infra.py             # aplica y verifica

El mapeo se guarda en `.claude/state/mapeo-seudonimos-infra.md`, que está
ignorado por git: el autor conserva la correspondencia sin publicarla.

Solo biblioteca estándar. Sin dependencias externas.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUTA_MAPEO = ROOT / ".claude" / "state" / "mapeo-seudonimos-infra.md"

# ---------------------------------------------------------------------------
# El orden importa: lo mas especifico primero, para que un nombre corto no
# consuma a uno largo que lo contiene. cargar_mapeo() lo garantiza ordenando
# por longitud descendente.
# ---------------------------------------------------------------------------
# El mapeo NO vive aqui. Este archivo esta versionado en un repositorio publico,
# asi que llevar dentro los nombres reales anularia el proposito del guion: durante
# meses expuso justo lo que pretendia ocultar. Se lee de .claude/state/, ignorado
# por git. Si el archivo no existe, el guion se niega a trabajar en vez de adivinar.
def cargar_mapeo():
    """Lee los pares real -> seudonimo de la tabla Markdown privada."""
    if not RUTA_MAPEO.exists():
        sys.exit(
            "ERROR: no se encuentra el mapeo privado en %s\n"
            "       Es deliberado que no este en el repositorio: contiene los nombres\n"
            "       reales de la infraestructura. Recuperalo de tu copia local o de\n"
            "       una copia de seguridad antes de ejecutar este guion."
            % RUTA_MAPEO.relative_to(ROOT)
        )
    pares = []
    for linea in RUTA_MAPEO.read_text(encoding="utf-8").splitlines():
        celdas = [c.strip() for c in linea.split("|")]
        # filas de la tabla: | real | seudonimo | que es |
        if len(celdas) >= 4 and celdas[1] and celdas[2]:
            real, seudo = celdas[1], celdas[2]
            if real in ("Real", "---") or set(real) <= set("-: "):
                continue
            real = real.split(" (")[0].strip()
            pares.append((real, seudo))
    if not pares:
        sys.exit("ERROR: el mapeo de %s no contiene ninguna fila valida."
                 % RUTA_MAPEO.relative_to(ROOT))
    # Lo mas especifico primero, para que un nombre corto no consuma a uno largo.
    pares.sort(key=lambda par: -len(par[0]))
    return pares

# Detecta residuos tras aplicar el mapeo (algo que se nos haya escapado).
def residuos():
    """Patrones que delatan un nombre real sin seudonimizar.

    Se derivan del mapeo privado para no reproducir aqui los nombres.
    """
    return [re.compile(r"\b%s\b" % re.escape(real)) for real, _ in cargar_mapeo()]

EXT_BINARIAS = {
    ".pdf", ".zip", ".docx", ".doc", ".jpg", ".jpeg", ".png", ".gif", ".svg",
    ".gz", ".tgz", ".pyc", ".rds", ".RData", ".xlsx", ".pptx", ".ico",
    # activos web de terceros: 'gitlab' aparece ahí como nombre de icono
    ".css", ".js", ".map", ".woff", ".woff2", ".ttf", ".eot", ".html",
}

DIRS_EXCLUIDOS = {".git", "node_modules", "__pycache__", ".quarto",
                  "docs", "site_libs"}

# El propio guion contiene el mapeo: no se seudonimiza a sí mismo. Tampoco el
# archivo de mapeo privado, que existe justamente para guardar la equivalencia.
AUTOEXCLUIDOS = {"seudonimizar_infra.py"}

RUTA_MAPEO = ROOT / ".claude" / "state" / "mapeo-seudonimos-infra.md"


def archivos_de_texto():
    """Itera los archivos de texto candidatos del repositorio."""
    for ruta in sorted(ROOT.rglob("*")):
        if not ruta.is_file():
            continue
        if any(parte in DIRS_EXCLUIDOS for parte in ruta.parts):
            continue
        if ruta.suffix.lower() in EXT_BINARIAS:
            continue
        if ruta.name in AUTOEXCLUIDOS:
            continue
        if ruta == RUTA_MAPEO:
            continue
        yield ruta


def leer(ruta):
    """Devuelve el texto del archivo, o None si no es texto legible."""
    try:
        return ruta.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def escanear():
    """Devuelve {ruta relativa: {token: nº apariciones}} de lo que falta mapear."""
    hallazgos = {}
    for ruta in archivos_de_texto():
        texto = leer(ruta)
        if texto is None:
            continue
        cuentas = {}
        for patron in residuos():
            encontrados = patron.findall(texto)
            if encontrados:
                cuentas[patron.pattern] = len(encontrados)
        if cuentas:
            hallazgos[ruta.relative_to(ROOT)] = cuentas
    return hallazgos


def aplicar(dry_run):
    """Aplica el mapeo. Devuelve (archivos modificados, sustituciones totales)."""
    archivos = 0
    total = 0
    for ruta in archivos_de_texto():
        texto = leer(ruta)
        if texto is None:
            continue
        original = texto
        detalle = []
        for viejo, nuevo in cargar_mapeo():
            n = texto.count(viejo)
            if n:
                texto = texto.replace(viejo, nuevo)
                detalle.append("%s->%s x%d" % (viejo, nuevo, n))
                total += n
        if texto == original:
            continue
        if not dry_run:
            ruta.write_text(texto, encoding="utf-8")
        archivos += 1
        print("  %s %s" % ("~" if dry_run else "OK", ruta.relative_to(ROOT)))
        print("      %s" % "; ".join(detalle))
    return archivos, total


def guardar_mapeo():
    """Antes generaba el mapeo privado; ahora ese archivo es la fuente de verdad.

    Se conserva como no-op para no romper a quien la invoque. El mapeo se
    mantiene a mano en .claude/state/ y NUNCA se reconstruye desde aqui: hacerlo
    obligaria a llevar los nombres reales dentro de un archivo versionado, que es
    exactamente el fallo que este cambio corrige.
    """
    if RUTA_MAPEO.exists():
        print("  OK mapeo privado presente en %s" % RUTA_MAPEO.relative_to(ROOT))
    else:
        print("  ! falta el mapeo privado en %s" % RUTA_MAPEO.relative_to(ROOT))


def informar(hallazgos):
    if not hallazgos:
        print("Sin identificadores de infraestructura productiva pendientes.")
        return
    print("Identificadores pendientes de seudonimizar:")
    for ruta, cuentas in hallazgos.items():
        detalle = ", ".join("%s x%d" % (p, n) for p, n in cuentas.items())
        print("  %-70s %s" % (ruta, detalle))


def main():
    parser = argparse.ArgumentParser(
        description="Seudonimiza identificadores de infraestructura productiva."
    )
    parser.add_argument("--check", action="store_true",
                        help="solo informar lo que falta")
    parser.add_argument("--dry-run", action="store_true",
                        help="mostrar los cambios sin escribirlos")
    args = parser.parse_args()

    if args.check:
        informar(escanear())
        return 0

    print("1) Sustitucion")
    archivos, total = aplicar(args.dry_run)
    if archivos == 0:
        print("  = nada que sustituir")
    else:
        print("  %d archivo(s), %d sustitucion(es)" % (archivos, total))

    if args.dry_run:
        print("\n(dry-run: no se escribio nada)")
        return 0

    print("\n2) Mapeo privado")
    guardar_mapeo()

    print("\n3) Verificacion")
    hallazgos = escanear()
    if hallazgos:
        print("  ! QUEDAN residuos:")
        informar(hallazgos)
        return 1
    print("  OK sin residuos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
