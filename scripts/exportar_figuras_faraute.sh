#!/usr/bin/env bash
# Exporta las figuras del articulo al formato que exige la guia de FARAUTE:
# JPEG, 300 dpi, escala de grises, nombradas "FigN".
#   Guia, punto 9: "Estas deben estar en blanco y negro o escala de grises en
#   formato JPEG o TIFF a una resolucion de 300 dpi, y el archivo debe ser
#   nombrado como 'Fig' seguido del numero que corresponda en el articulo."
# Uso: scripts/exportar_figuras_faraute.sh [directorio_salida]
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEX="$RAIZ/paper/faraute/main.tex"
SALIDA="${1:-$RAIZ/paper/faraute/figuras_envio}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$SALIDA"

# El preambulo del articulo, hasta \begin{document}, para que la figura se
# componga con los mismos tipos y paquetes que en el manuscrito.
sed -n '1,/\\begin{document}/p' "$TEX" | sed '$d' > "$TMP/preambulo.tex"

n=0
# Cada entorno figure del articulo se recompila por separado, sin leyenda:
# la leyenda va en el manuscrito, no en el fichero de imagen.
python3 - "$TEX" "$TMP" <<'PY'
import re, sys, pathlib
tex = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
tmp = pathlib.Path(sys.argv[2])
figs = re.findall(r"\\begin\{figure\*?\}.*?\\end\{figure\*?\}", tex, flags=re.S)
for i, f in enumerate(figs, 1):
    cuerpo = re.sub(r"\\caption\{.*?\}\s*(?=\\label|\\end)", "", f, flags=re.S)
    cuerpo = re.sub(r"\\label\{[^}]*\}", "", cuerpo)
    cuerpo = cuerpo.replace("\\begin{figure}[tb]", "").replace("\\begin{figure}", "")
    cuerpo = cuerpo.replace("\\end{figure}", "").replace("\\centering", "")
    (tmp / f"fig{i}_cuerpo.tex").write_text(cuerpo.strip(), encoding="utf-8")
print(len(figs))
PY

for cuerpo in "$TMP"/fig*_cuerpo.tex; do
  n=$((n+1))
  { cat "$TMP/preambulo.tex"
    echo '\usepackage[active,tightpage]{preview}'
    echo '\PreviewEnvironment{tikzpicture}'
    echo '\renewcommand{\PreviewBorder}{6pt}'
    echo '\begin{document}'
    cat "$cuerpo"
    echo '\end{document}'
  } > "$TMP/Fig$n.tex"
  (cd "$TMP" && xelatex -interaction=nonstopmode "Fig$n.tex" >/dev/null 2>&1) || true
  if [ -f "$TMP/Fig$n.pdf" ]; then
    pdftoppm -r 300 -gray -jpeg -jpegopt quality=95 -singlefile \
             "$TMP/Fig$n.pdf" "$SALIDA/Fig$n"
    echo "  Fig$n.jpg  $(identify -format '%wx%h %[resolution.x]dpi' "$SALIDA/Fig$n.jpg" 2>/dev/null || echo "$(file -b "$SALIDA/Fig$n.jpg" | cut -d, -f2-3)")"
  else
    echo "  Fig$n: no se pudo componer" >&2
  fi
done
echo "Figuras en: $SALIDA"
