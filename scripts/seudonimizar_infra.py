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

# ---------------------------------------------------------------------------
# Mapeo. El ORDEN IMPORTA: 'pg-gitlab' antes que 'gitlab', y la frase sobre
# GitLab antes que el nombre suelto del namespace.
# ---------------------------------------------------------------------------
MAPEO = [
    # correo corporativo -> correo académico del autor
    ("aparejo@alitronslt.com", "angelparejo@gmail.com"),
    # clústeres CNPG preexistentes (ajenos al experimento)
    ("pg-gitlab", "pg-delta"),
    ("pg-prod", "pg-alfa"),
    ("pg-cert", "pg-beta"),
    ("pg-dev", "pg-gamma"),
    # el namespace de GitLab y la mención al servicio que aloja
    ("infraestructura de GitLab", "infraestructura de un servicio interno"),
    ("gitlab", "ns-delta"),
    # nodos del clúster. tcolp293 es el nodo del laboratorio: se alinea con el
    # seudónimo que ya usa el manuscrito.
    ("tcolp293", "nodo-lab-01"),
    ("tcolp295", "nodo-02"),
    ("tcolp296", "nodo-03"),
    ("tcolp300", "nodo-04"),
]

# Detecta residuos tras aplicar el mapeo (algo que se nos haya escapado).
RESIDUOS = [
    re.compile(r"tcolp\d+"),
    re.compile(r"\balitronslt\b"),
    re.compile(r"pg-(prod|cert|dev|gitlab)\b"),
]

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
        for patron in RESIDUOS:
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
        for viejo, nuevo in MAPEO:
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
    """Guarda la correspondencia en .claude/state/ (ignorado por git)."""
    RUTA_MAPEO.parent.mkdir(parents=True, exist_ok=True)
    lineas = [
        "# Mapeo de seudónimos de infraestructura (PRIVADO)",
        "",
        "Este archivo vive en `.claude/state/`, que está ignorado por git: la",
        "correspondencia queda en tu máquina y no se publica. Generado por",
        "`scripts/seudonimizar_infra.py`.",
        "",
        "| Real | Seudónimo | Qué es |",
        "|---|---|---|",
        "| tcolp293 | nodo-lab-01 | nodo del laboratorio (co-aloja 3 primarios ajenos) |",
        "| tcolp295 | nodo-02 | worker con el primario de producción |",
        "| tcolp296 | nodo-03 | worker con réplicas |",
        "| tcolp300 | nodo-04 | worker con réplicas |",
        "| pg-prod | pg-alfa | clúster CNPG de producción |",
        "| pg-cert | pg-beta | clúster CNPG de certificación |",
        "| pg-dev | pg-gamma | clúster CNPG de desarrollo |",
        "| pg-gitlab | pg-delta | clúster CNPG del servicio de repositorios |",
        "| gitlab (namespace) | ns-delta | namespace del servicio de repositorios |",
        "| aparejo@alitronslt.com | angelparejo@gmail.com | correo del autor |",
        "",
        "No se tocó `pglab-cnpg-exp` ni el namespace `pg-chaos-lab` (son del",
        "experimento, no de producción), ni los nombres de la StorageClass del",
        "proveedor de almacenamiento: el artículo declara el controlador CSI",
        "empleado porque es información metodológica necesaria.",
        "",
    ]
    RUTA_MAPEO.write_text("\n".join(lineas), encoding="utf-8")
    print("  OK mapeo privado en %s" % RUTA_MAPEO.relative_to(ROOT))


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
