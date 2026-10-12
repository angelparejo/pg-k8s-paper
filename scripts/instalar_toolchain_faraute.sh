#!/usr/bin/env bash
# Instala y verifica la cadena de herramientas que exige la plantilla
# "plantilla-autor-v2" de la Revista FARAUTE.
#
# La plantilla se compila con pdfLaTeX + Biber y usa biblatex con estilo APA,
# que no vienen en la instalacion de TeX Live de este equipo.
#
# Uso:
#   scripts/instalar_toolchain_faraute.sh --check     solo informa que falta
#   scripts/instalar_toolchain_faraute.sh --dry-run   muestra el apt-get sin ejecutarlo
#   scripts/instalar_toolchain_faraute.sh             instala y verifica
#   scripts/instalar_toolchain_faraute.sh --verify    solo compila la plantilla de ejemplo
#
# Requiere sudo para instalar. Las comprobaciones no lo requieren.
set -uo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLANTILLA="$RAIZ/paper/faraute/plantilla-autor-v2"
MODO="${1:-instalar}"

# ---------------------------------------------------------------- requisitos
# Formato: "comprobacion|que buscar|paquete apt|para que sirve"
REQS=(
  "bin|biber|biber|motor de bibliografia que exige la plantilla"
  "bin|latexmk|latexmk|compila las pasadas (pdflatex, biber, pdflatex x2) de una vez"
  "tex|biblatex.sty|texlive-bibtex-extra|bibliografia con biblatex"
  "tex|apa.bbx|texlive-bibtex-extra|estilo APA 7 que usa la revista"
  "tex|algorithm.sty|texlive-science|entorno algorithm de la clase"
  "tex|algpseudocode.sty|texlive-science|pseudocodigo de la clase"
  "tex|newtxtext.sty|texlive-fonts-extra|tipografia del diseno (hay alternativa, pero cambia el aspecto)"
)

falta() {  # imprime los paquetes apt que faltan, uno por linea
  local tipo nombre paquete _
  for r in "${REQS[@]}"; do
    IFS='|' read -r tipo nombre paquete _ <<<"$r"
    case "$tipo" in
      bin) command -v "$nombre" >/dev/null 2>&1 || echo "$paquete" ;;
      tex) kpsewhich "$nombre" >/dev/null 2>&1 || echo "$paquete" ;;
    esac
  done | sort -u
}

informe() {
  local tipo nombre paquete motivo estado n=0
  echo "Estado de la cadena de herramientas para la plantilla FARAUTE"
  echo
  printf "  %-20s %-24s %s\n" "COMPONENTE" "PAQUETE APT" "ESTADO"
  for r in "${REQS[@]}"; do
    IFS='|' read -r tipo nombre paquete motivo <<<"$r"
    case "$tipo" in
      bin) command -v "$nombre" >/dev/null 2>&1 && estado="instalado" || { estado="FALTA"; n=$((n+1)); } ;;
      tex) kpsewhich "$nombre" >/dev/null 2>&1 && estado="instalado" || { estado="FALTA"; n=$((n+1)); } ;;
    esac
    printf "  %-20s %-24s %s\n" "$nombre" "$paquete" "$estado"
    [ "$estado" = "FALTA" ] && printf "  %-20s %-24s   -> %s\n" "" "" "$motivo"
  done
  echo
  return $n
}

verificar() {
  echo "Verificacion: compilando la plantilla de ejemplo de principio a fin"
  [ -d "$PLANTILLA" ] || { echo "  No encuentro $PLANTILLA" >&2; return 1; }
  local tmp; tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' RETURN
  cp -r "$PLANTILLA"/. "$tmp/" || return 1
  (
    cd "$tmp" || exit 1
    pdflatex -interaction=nonstopmode articulo.tex >/dev/null 2>&1
    biber articulo                                  >/dev/null 2>&1
    pdflatex -interaction=nonstopmode articulo.tex >/dev/null 2>&1
    pdflatex -interaction=nonstopmode articulo.tex >/dev/null 2>&1
  )
  if [ ! -f "$tmp/articulo.pdf" ]; then
    echo "  FALLO: no se genero el PDF."
    echo "  Primeros errores:"
    grep -m5 -E "^!|not found" "$tmp/articulo.log" 2>/dev/null | sed 's/^/    /'
    return 1
  fi
  local pgs err avisos refs img reales
  pgs=$(pdfinfo "$tmp/articulo.pdf" 2>/dev/null | awk '/^Pages/{print $2}')
  err=$(grep -c '^!' "$tmp/articulo.log" 2>/dev/null)
  avisos=$(grep -c 'Class faraute Warning' "$tmp/articulo.log" 2>/dev/null)
  refs=$(grep -ci 'undefined' "$tmp/articulo.log" 2>/dev/null)
  # La plantilla de ejemplo cita una imagen que no viene en la carpeta (no trae
  # figuras/). Ese error es del material de ejemplo, no de la cadena de
  # herramientas, y no debe confundirse con un fallo de instalacion.
  img=$(grep -c "LaTeX Error: File \`valores-singulares' not found" "$tmp/articulo.log" 2>/dev/null)
  reales=$(( err - img ))
  echo "  PDF generado: ${pgs} paginas"
  echo "  avisos de la clase faraute: ${avisos} | referencias sin resolver: ${refs}"
  [ "$refs" -eq 0 ] && echo "  La bibliografia con biber resolvio correctamente."
  if [ "$img" -gt 0 ]; then
    echo "  Nota: la plantilla de ejemplo cita la imagen 'valores-singulares', que no"
    echo "        viene en la carpeta (no hay figuras/). Es del ejemplo, no de la"
    echo "        instalacion, y desaparece al poner sus propias figuras."
  fi
  if [ "$reales" -le 0 ]; then
    echo "  OK: la cadena de herramientas funciona en este equipo."
    return 0
  fi
  echo "  REVISAR: ${reales} error(es) ajenos a la imagen de ejemplo:"
  grep '^!' "$tmp/articulo.log" | grep -v 'valores-singulares' | head -5 | sed 's/^/    /'
  return 1
}

# ------------------------------------------------------------------- acciones
case "$MODO" in
  --check)
    informe; exit $?
    ;;
  --verify)
    verificar; exit $?
    ;;
  --dry-run)
    informe || true
    paquetes="$(falta | tr '\n' ' ')"
    if [ -z "${paquetes// }" ]; then echo "No falta nada que instalar."; exit 0; fi
    echo "Orden que se ejecutaria:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install -y $paquetes"
    exit 0
    ;;
  instalar) ;;
  *)
    echo "Opcion desconocida: $MODO  (use --check, --dry-run, --verify o sin argumentos)" >&2
    exit 2
    ;;
esac

informe || true
paquetes="$(falta | tr '\n' ' ')"
if [ -z "${paquetes// }" ]; then
  echo "No falta nada. Paso directo a la verificacion."
  echo
  verificar
  exit $?
fi

echo "Se van a instalar: $paquetes"
echo "Descarga aproximada: varios cientos de MB (texlive-fonts-extra y texlive-science son grandes)."
echo
if ! sudo -n true 2>/dev/null; then
  echo "Hace falta sudo. Se pedira la contrasena."
fi
sudo apt-get update || { echo "Fallo apt-get update" >&2; exit 1; }
# shellcheck disable=SC2086
sudo apt-get install -y $paquetes || { echo "Fallo la instalacion" >&2; exit 1; }

echo
echo "Reconstruyendo la base de datos de ficheros de TeX..."
sudo mktexlsr >/dev/null 2>&1 || true

echo
informe || true
echo
verificar
