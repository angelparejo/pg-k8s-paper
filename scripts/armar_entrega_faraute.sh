#!/usr/bin/env bash
# Arma el comprimido que se entrega a la Revista FARAUTE.
# Recompila artículo y suplemento, exporta las figuras al formato que exige la
# guía (punto 9: JPEG/TIFF, 300 dpi, escala de grises, nombradas "FigN") y
# empaqueta todo con un LEEME.
# Uso: scripts/armar_entrega_faraute.sh
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
F="$RAIZ/paper/faraute"
DEST="$F/entrega-latex"
ZIP="$F/entrega-latex.zip"

echo "== 1/4  Recompilando"
cd "$F"
for _ in 1 2 3; do xelatex -interaction=nonstopmode main.tex >/dev/null 2>&1 || true; done
cd "$F/replication/supplement"
for _ in 1 2 3; do xelatex -interaction=nonstopmode suplemento.tex >/dev/null 2>&1 || true; done
cd "$F"

err=$(grep -c '^!' main.log || true); ovf=$(grep -c 'Overfull \\hbox' main.log || true)
pgs=$(pdfinfo main.pdf | awk '/^Pages/{print $2}')
echo "   articulo: ${pgs} pp, ${err} errores, ${ovf} overfull"
[ "$err" -eq 0 ] || { echo "   ABORTA: el articulo no compila limpio" >&2; exit 1; }

echo "== 2/4  Exportando figuras a 300 dpi en escala de grises"
bash "$RAIZ/scripts/exportar_figuras_faraute.sh" >/dev/null

echo "== 3/4  Montando $DEST"
rm -rf "$DEST"; mkdir -p "$DEST/figuras"
cp main.tex                                   "$DEST/main.tex"
cp main.pdf                                   "$DEST/articulo_revisado_${pgs}pp.pdf"
cp replication/supplement/suplemento.pdf      "$DEST/suplemento.pdf"
cp carta_respuesta_arbitros.md                "$DEST/carta_respuesta_arbitros.md"
cp figuras_envio/*.jpg                        "$DEST/figuras/"

sup=$(pdfinfo replication/supplement/suplemento.pdf | awk '/^Pages/{print $2}')
nfig=$(ls -1 "$DEST/figuras" | wc -l)
cat > "$DEST/LEEME.txt" <<EOF
ARTICULO EN FORMATO LaTeX — VERSION REVISADA TRAS ARBITRAJE
Caracterizacion empirica de la conmutacion por error de CloudNativePG en
Kubernetes: RTO, RPO y los limites de la inyeccion de fallos

Herrera, M.; Parejo, A. — Universidad de Carabobo
Correspondencia: Parejo, A. — ORCID 0009-0001-9737-7116

CONTENIDO
  main.tex                        Fuente LaTeX completo y autocontenido: no usa
                                  \\input ni un .bib externo; la bibliografia va
                                  dentro del propio .tex, en formato Faraute.
                                  La unica figura se genera con pgfplots desde
                                  los datos, asi que no hay imagenes que enlazar.
  articulo_revisado_${pgs}pp.pdf        PDF compilado, ${pgs} paginas. Es la version que
                                  se envia a la revista.
  suplemento.pdf                  Material suplementario, ${sup} paginas.
  carta_respuesta_arbitros.md     Respuesta punto por punto a los dos informes.
  figuras/Fig1.jpg                Figura en JPEG, escala de grises, 300 dpi,
                                  segun el punto 9 de la guia para autores
                                  (copia digital aparte de la insertada en el PDF).

COMO COMPILAR
  xelatex main.tex   (tres pasadas; requiere el paquete pgfplots)
  El documento no necesita biber ni latexmk.

QUE CAMBIO EN ESTA VERSION
  El reencuadre central: de los cuatro escenarios de fallo disenados, solo uno
  reprodujo el fallo que nominalmente modela. En consecuencia se retiraron dos
  de las tres conclusiones empiricas de la version anterior y la contribucion
  pasa a ser la advertencia metodologica sobre la fidelidad del inyector.
  El detalle, observacion por observacion, esta en la carta de respuesta.

QUE HAY EN EL SUPLEMENTO
  El limite de 12 paginas obliga a enunciar algunos resultados sin su respaldo,
  y el articulo remite al suplemento varias veces. Contiene el reparto de
  responsabilidades por capa (Tabla S1), los metodos ampliados, la estadistica
  completa, las derivaciones del poder de deteccion del RPO y de la rejilla de
  medida del escenario F3, el tratamiento de las conexiones establecidas en la
  particion de red, y el diseno de la Fase 2.

DATOS Y REPLICACION
  Deposito publico en Zenodo, DOI 10.5281/zenodo.23004248: series de RTO e
  indisponibilidad por repeticion, recuento de la tabla de verdad del que se
  deriva el RPO, manifiestos, el verificador de transacciones y los scripts de
  analisis, que reproducen las cifras del articulo sin dependencias externas.
EOF

echo "== 4/4  Comprimiendo"
rm -f "$ZIP"
( cd "$F" && zip -r -q "$ZIP" "$(basename "$DEST")" )
rm -rf "$DEST"
echo
echo "Listo: $ZIP"
unzip -l "$ZIP" | tail -n +4 | head -20
