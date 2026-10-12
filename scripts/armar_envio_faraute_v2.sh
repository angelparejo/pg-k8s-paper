#!/usr/bin/env bash
# Monta el paquete de reenvio a la Revista FARAUTE con la plantilla v2.
#
# Compila la version extensa en sus dos modalidades (normal y [revision]),
# audita que la de arbitraje no filtre la identidad de los autores, y
# empaqueta el PDF anonimo, las dos cartas, las fuentes y el suplemento.
#
# Uso: scripts/armar_envio_faraute_v2.sh
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
V2="$RAIZ/paper/faraute/v2"
SUP="$RAIZ/paper/faraute/replication/supplement"
DEST="$V2/envio-faraute"
ZIP="$V2/envio-faraute.zip"

compila() {   # $1 = nombre base del .tex
  ( cd "$V2" && pdflatex -interaction=nonstopmode "$1.tex" >/dev/null 2>&1
                biber "$1"                                 >/dev/null 2>&1
                pdflatex -interaction=nonstopmode "$1.tex" >/dev/null 2>&1
                pdflatex -interaction=nonstopmode "$1.tex" >/dev/null 2>&1 ) || true
  local err ovf pgs avisos
  err=$(grep -c '^!' "$V2/$1.log" || true)
  ovf=$(grep -c 'Overfull \\hbox' "$V2/$1.log" || true)
  avisos=$(grep -c 'Class faraute Warning' "$V2/$1.log" || true)
  pgs=$(pdfinfo "$V2/$1.pdf" 2>/dev/null | awk '/^Pages/{print $2}')
  printf "   %-30s %2s pp | %s err | %s overfull | %s avisos\n" "$1" "${pgs:-?}" "$err" "$ovf" "$avisos"
  [ "$err" -eq 0 ] || { echo "   ABORTA: $1 no compila limpio" >&2; exit 1; }
  [ "$avisos" -eq 0 ] || { echo "   ABORTA: $1 deja avisos de la clase faraute" >&2; exit 1; }
}

echo "== 1/4  Compilando"
compila articulo-extensa
compila articulo-extensa-arbitraje

echo "== 2/4  Auditando el anonimato del PDF de arbitraje"
TXT="$(pdftotext "$V2/articulo-extensa-arbitraje.pdf" - 2>/dev/null)"
fugas=0
for patron in Parejo Herrera Mirella angelparejo uc.edu.ve Carabobo ORCID 0009-0001 10.5281 FaCyT; do
  n=$(printf '%s' "$TXT" | grep -oic "$patron" || true)
  if [ "$n" -gt 0 ]; then echo "   FUGA: '$patron' aparece $n vez/veces"; fugas=$((fugas+n)); fi
done
if [ "$fugas" -gt 0 ]; then
  echo "   ABORTA: el PDF de arbitraje no es anonimo." >&2; exit 1
fi
echo "   Sin fugas de identidad."

echo "== 3/4  Montando $DEST"
rm -rf "$DEST"; mkdir -p "$DEST/fuentes"
cp "$V2/articulo-extensa-arbitraje.pdf"          "$DEST/articulo-arbitraje.pdf"
cp "$V2/carta_de_envio.md"                       "$DEST/"
cp "$RAIZ/paper/faraute/carta_respuesta_arbitros.md" "$DEST/"
cp "$SUP/suplemento.pdf"                         "$DEST/suplemento.pdf"
# Fuentes con los nombres que pide la plantilla
cp "$V2/datos.tex"            "$DEST/fuentes/datos.tex"
cp "$V2/contenido-extensa.tex" "$DEST/fuentes/contenido.tex"
cp "$V2/referencias.bib"      "$DEST/fuentes/referencias.bib"
sed 's/{contenido-extensa}/{contenido}/' "$V2/articulo-extensa.tex" > "$DEST/fuentes/articulo.tex"

pgs=$(pdfinfo "$V2/articulo-extensa-arbitraje.pdf" | awk '/^Pages/{print $2}')
sup=$(pdfinfo "$SUP/suplemento.pdf" | awk '/^Pages/{print $2}')
cat > "$DEST/LEEME.txt" <<EOF
REENVIO TRAS REVISION MAYOR — Revista FARAUTE de Ciencias y Tecnologia

Caracterizacion empirica de la conmutacion por error de CloudNativePG en
Kubernetes: RTO, RPO y los limites de la inyeccion de fallos

CONTENIDO
  carta_de_envio.md             Tipo de contribucion, originalidad, formato y
                                declaracion de uso de IA.
  carta_respuesta_arbitros.md   Respuesta punto por punto a los dos informes.
  articulo-arbitraje.pdf        Manuscrito ANONIMO con lineas numeradas,
                                ${pgs} paginas. Compilado con la opcion
                                [revision] de la clase, segun el apartado
                                "Que enviar" de las instrucciones.
  suplemento.pdf                Material suplementario, ${sup} paginas.
  fuentes/                      articulo.tex, datos.tex, contenido.tex y
                                referencias.bib.

COMO COMPILAR LAS FUENTES
  latexmk -pdf articulo.tex
  o bien: pdflatex -> biber -> pdflatex -> pdflatex
  Requiere la clase faraute.cls, que no se incluye por ser de la revista.
  La unica figura se genera con pgfplots y TikZ desde los datos: no hay
  imagenes externas que enlazar.

NOTA SOBRE EL ANONIMATO
  El PDF adjunto omite el DOI del deposito de datos y el nombre de la
  institucion de la fase siguiente, porque ambos revelarian la identidad de
  los autores. El DOI consta en la carta de envio, a disposicion del editor.
  Al retirar la opcion [revision] de articulo.tex reaparecen.
EOF

echo "== 4/4  Comprimiendo"
rm -f "$ZIP"
( cd "$V2" && zip -r -q "$ZIP" "$(basename "$DEST")" )
rm -rf "$DEST"
echo
echo "Listo: $ZIP"
unzip -l "$ZIP" | tail -n +4 | head -12
