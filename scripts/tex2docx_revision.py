#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tex2docx_revision.py -- Genera una copia en DOCX del artículo para anotar.

No reproduce la maqueta de la revista: produce una **copia de revisión**,
pensada para que alguien lea y comente en Word. Por eso va a una columna, con
interlineado 1,5, márgenes amplios y **numeración de líneas continua**, de modo
que quien revise pueda decir "línea 143" sin ambigüedad.

Se parte del .tex, no del PDF: el texto sale limpio y con la estructura intacta
(secciones, tablas, ecuaciones, pies de figura), en vez de extraer cadenas de un
PDF ya maquetado.

Qué conserva:
  - Títulos en español e inglés, autoría, resúmenes y palabras clave.
  - Secciones y subsecciones numeradas.
  - Cursivas, negritas y monoespaciado del original.
  - Tablas como tablas reales de Word, con sus leyendas y notas.
  - Figuras incrustadas (JPEG) con su pie.
  - Ecuaciones numeradas, en una línea centrada y legible.
  - Referencias con sangría francesa.

Método air-gapped: se construye el OOXML a mano y se empaqueta con zipfile.
Sin pandoc, sin python-docx, sin dependencias externas.

Uso:
    python3 scripts/tex2docx_revision.py                     # rutas por defecto
    python3 scripts/tex2docx_revision.py <entrada.tex> <salida.docx>
"""

import os
import re
import struct
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEX_POR_DEFECTO = ROOT / "paper" / "faraute" / "main.tex"
SALIDA_POR_DEFECTO = ROOT / "articulo_faraute_12pp_para_revision.docx"

EMU_POR_PULGADA = 914400
ANCHO_UTIL_EMU = int(6.0 * EMU_POR_PULGADA)   # Carta 8,5" menos 1,25" por lado

# ---------------------------------------------------------------------------
# Sustituciones de texto en línea
# ---------------------------------------------------------------------------
SIMBOLOS = [
    (r"\\approx", "≈"), (r"\\times", "×"), (r"\\le\b", "≤"), (r"\\ge\b", "≥"),
    (r"\\rho", "ρ"), (r"\\alpha", "α"), (r"\\mu", "μ"), (r"\\sigma", "σ"),
    (r"\\in\b", "∈"), (r"\\cdot", "·"), (r"\\ldots", "…"), (r"\\dots", "…"),
    (r"\\rightarrow", "→"), (r"\\to\b", "→"), (r"\\pm", "±"),
    (r"\\%", "%"), (r"\\&", "&"), (r"\\_", "_"), (r"\\\$", "$"),
    (r"\\#", "#"), (r"\\,", "\u2009"), (r"\\;", " "), (r"\\ ", " "),
]

SUPERINDICES = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵",
                "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "-": "⁻"}


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def superindice(m):
    return "".join(SUPERINDICES.get(c, c) for c in m.group(1))


def limpiar_math(s):
    """Convierte matemáticas sencillas de LaTeX en texto legible."""
    s = re.sub(r"\\text\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\mathrm\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\^\{([^{}]*)\}", superindice, s)
    s = re.sub(r"\^(-?\d)", lambda m: superindice(m), s)
    s = re.sub(r"_\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"_(\w)", r"\1", s)
    for patron, simbolo in SIMBOLOS:
        s = re.sub(patron, simbolo, s)
    s = s.replace("{,}", ",").replace("{", "").replace("}", "")
    return s


def limpiar(s):
    """Normaliza el texto plano de LaTeX (sin marcas de formato)."""
    s = re.sub(r"\\url\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\phantomsection|\\begingroup|\\endgroup", "", s)
    s = re.sub(r"\$([^$]*)\$", lambda m: limpiar_math(m.group(1)), s)
    for patron, simbolo in SIMBOLOS:
        s = re.sub(patron, simbolo, s)
    s = s.replace("---", "—").replace("--", "–")
    s = s.replace("``", "“").replace("''", "”")
    s = s.replace("~", "\u00a0")
    s = re.sub(r"\\par\b", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# ---------------------------------------------------------------------------
# Piezas de OOXML
# ---------------------------------------------------------------------------
def run(texto, *, cursiva=False, negrita=False, mono=False, tam=None):
    if not texto:
        return ""
    props = ""
    if negrita:
        props += "<w:b/>"
    if cursiva:
        props += "<w:i/>"
    if mono:
        props += '<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/>'
    if tam:
        props += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (tam * 2, tam * 2)
    rpr = "<w:rPr>%s</w:rPr>" % props if props else ""
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, esc(texto))


def runs_desde_tex(s):
    """Traduce \\textit, \\emph, \\textbf y \\texttt a runs con formato."""
    piezas = []
    patron = re.compile(r"\\(textit|emph|textbf|texttt|textsc)\{([^{}]*)\}")
    pos = 0
    for m in patron.finditer(s):
        if m.start() > pos:
            piezas.append((s[pos:m.start()], {}))
        estilo = {"textit": {"cursiva": True}, "emph": {"cursiva": True},
                  "textbf": {"negrita": True}, "texttt": {"mono": True},
                  "textsc": {}}[m.group(1)]
        piezas.append((m.group(2), estilo))
        pos = m.end()
    if pos < len(s):
        piezas.append((s[pos:], {}))
    return "".join(run(limpiar(t), **e) for t, e in piezas if limpiar(t))


def parrafo(contenido_runs, *, estilo=None, alineacion=None, sangria=None,
            espacio_antes=0, espacio_despues=120, interlineado=360):
    ppr = ""
    if estilo:
        ppr += '<w:pStyle w:val="%s"/>' % estilo
    ppr += ('<w:spacing w:before="%d" w:after="%d" w:line="%d" '
            'w:lineRule="auto"/>' % (espacio_antes, espacio_despues, interlineado))
    if sangria:
        ppr += '<w:ind w:left="%d" w:hanging="%d"/>' % sangria
    if alineacion:
        ppr += '<w:jc w:val="%s"/>' % alineacion
    return "<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (ppr, contenido_runs)


def celda(runs_xml, ancho_dxa, *, negrita_fondo=False):
    sombra = '<w:shd w:val="clear" w:fill="EEEEEE"/>' if negrita_fondo else ""
    return (
        '<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s'
        '<w:tcMar><w:top w:w="60" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/>'
        '<w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tcMar>'
        "</w:tcPr>%s</w:tc>" % (ancho_dxa, sombra, runs_xml)
    )


def tabla(filas, anchos_dxa):
    bordes = ('<w:tblBorders>'
              + "".join('<w:%s w:val="single" w:sz="4" w:color="999999"/>' % b
                        for b in ("top", "left", "bottom", "right",
                                  "insideH", "insideV"))
              + "</w:tblBorders>")
    xml = ('<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>%s'
           '<w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>%s</w:tblGrid>'
           % (bordes, "".join('<w:gridCol w:w="%d"/>' % a for a in anchos_dxa)))
    for idx, fila in enumerate(filas):
        celdas = ""
        for j, texto in enumerate(fila):
            ancho = anchos_dxa[j] if j < len(anchos_dxa) else anchos_dxa[-1]
            contenido = parrafo(runs_desde_tex(texto) or run(""),
                                espacio_despues=0, interlineado=240)
            celdas += celda(contenido, ancho, negrita_fondo=(idx == 0))
        xml += "<w:tr>%s</w:tr>" % celdas
    return xml + "</w:tbl>"


def dimensiones_jpeg(ruta):
    """Lee ancho y alto de un JPEG sin librerías externas."""
    with open(ruta, "rb") as f:
        datos = f.read()
    i = 2
    while i < len(datos) - 9:
        if datos[i] != 0xFF:
            i += 1
            continue
        marcador = datos[i + 1]
        if marcador in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                        0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            alto, ancho = struct.unpack(">HH", datos[i + 5:i + 9])
            return ancho, alto
        if marcador in (0xD8, 0xD9) or 0xD0 <= marcador <= 0xD7:
            i += 2
            continue
        longitud = struct.unpack(">H", datos[i + 2:i + 4])[0]
        i += 2 + longitud
    return 800, 600


def figura(rel_id, ancho_px, alto_px, nombre, indice):
    """`indice` da un identificador estable: hash() varía entre ejecuciones."""
    ancho_emu = ANCHO_UTIL_EMU
    alto_emu = int(ANCHO_UTIL_EMU * alto_px / max(ancho_px, 1))
    doc_pr = 1000 + indice
    return (
        '<w:p><w:pPr><w:jc w:val="center"/>'
        '<w:spacing w:before="180" w:after="60"/></w:pPr><w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0">'
        '<wp:extent cx="%d" cy="%d"/><wp:docPr id="%d" name="%s"/>'
        "<a:graphic><a:graphicData "
        'uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        "<pic:pic><pic:nvPicPr>"
        '<pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/>'
        "</a:stretch></pic:blipFill><pic:spPr><a:xfrm>"
        '<a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        "</pic:pic></a:graphicData></a:graphic></wp:inline>"
        "</w:drawing></w:r></w:p>"
        % (ancho_emu, alto_emu, doc_pr, nombre,
           doc_pr, nombre, rel_id, ancho_emu, alto_emu)
    )


# ---------------------------------------------------------------------------
# Análisis del .tex
# ---------------------------------------------------------------------------
def extraer_entorno(texto, entorno):
    """Devuelve la lista de bloques de un entorno dado."""
    patron = re.compile(r"\\begin\{%s\}(.*?)\\end\{%s\}" % (entorno, entorno),
                        re.S)
    return patron.findall(texto)


def _saltar_grupo(s, i):
    """Devuelve el índice tras el grupo {...} que empieza en s[i], con anidamiento."""
    if i >= len(s) or s[i] != "{":
        return i
    nivel = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            nivel += 1
        elif s[j] == "}":
            nivel -= 1
            if nivel == 0:
                return j + 1
    return len(s)


def filas_de_tabularx(bloque):
    """Convierte un tabularx en lista de filas de celdas.

    `\\begin{tabularx}` lleva DOS grupos —ancho y especificación de columnas— y
    el segundo trae llaves anidadas (`>{\\raggedright\\arraybackslash}X`). Hay
    que saltarlos contando llaves; una expresión regular no perezosa se queda
    en la primera `}` y deja la especificación dentro del texto.
    """
    m = re.search(r"\\begin\{tabularx\}", bloque)
    # extraer_entorno() ya recorta el \begin, así que el bloque puede empezar
    # directamente en el primer grupo.
    inicio = m.end() if m else 0
    resto = bloque[inicio:].lstrip()
    desplazamiento = len(bloque) - len(bloque[inicio:]) + \
        (len(bloque[inicio:]) - len(resto))
    if resto.startswith("{"):
        i = _saltar_grupo(bloque, desplazamiento)   # {\textwidth} o {\linewidth}
        i = _saltar_grupo(bloque, i)                # {@{}>{...}X ...@{}}
        cuerpo = bloque[i:]
    else:
        cuerpo = bloque[inicio:]
    cuerpo = cuerpo.replace("\\end{tabularx}", "")
    for regla in ("\\toprule", "\\midrule", "\\bottomrule"):
        cuerpo = cuerpo.replace(regla, "")
    filas = []
    for cruda in cuerpo.split("\\\\"):
        cruda = cruda.strip()
        if not cruda:
            continue
        filas.append([c.strip() for c in cruda.split("&")])
    return filas


def construir(tex_path, salida_path):
    tex = tex_path.read_text(encoding="utf-8")
    base = tex_path.parent

    # --- mapa de etiquetas -> número, por orden de aparición ---
    etiquetas = {}
    for tipo, patron in (("tabla", r"\\label\{(tab:[^}]+)\}"),
                         ("figura", r"\\label\{(fig:[^}]+)\}"),
                         ("ec", r"\\label\{(eq:[^}]+)\}")):
        for n, m in enumerate(re.finditer(patron, tex), 1):
            etiquetas[m.group(1)] = str(n)

    def resolver_refs(s):
        s = re.sub(r"\\ref\{([^}]+)\}", lambda m: etiquetas.get(m.group(1), "?"), s)
        s = re.sub(r"\\Ec\{([^}]+)\}",
                   lambda m: "Ec. (%s)" % etiquetas.get(m.group(1), "?"), s)
        return s

    cuerpo = []
    imagenes = []          # (nombre_archivo, rel_id)

    def img_rel(ruta_rel):
        nombre = Path(ruta_rel).name
        for n, rid in imagenes:
            if n == nombre:
                return rid
        rid = "rId%d" % (100 + len(imagenes))
        imagenes.append((nombre, rid))
        return rid

    # ---------------- portada ----------------
    m = re.search(r"\\bfseries\s*\n([A-ZÁÉÍÓÚÑ][^\\]*?)\\par", tex)
    titulo_es = limpiar(m.group(1)) if m else "(sin título)"
    m = re.search(r"\\fontsize\{12\}\{15\}\\selectfont\\bfseries\s*\n(.*?)\\par",
                  tex, re.S)
    titulo_en = limpiar(m.group(1)) if m else ""

    cuerpo.append(parrafo(run("COPIA DE REVISIÓN — no es la maqueta de la revista",
                              negrita=True, tam=10),
                          alineacion="center", espacio_despues=40))
    cuerpo.append(parrafo(
        run("Versión de 12 páginas enviada a la Revista FARAUTE. Las líneas van "
            "numeradas al margen para que puedas referirte a ellas en tus "
            "observaciones.", tam=9),
        alineacion="center", espacio_despues=300))

    cuerpo.append(parrafo(run(titulo_es, negrita=True, tam=14),
                          alineacion="center", espacio_despues=160))
    if titulo_en:
        cuerpo.append(parrafo(run(titulo_en, negrita=True, tam=12),
                              alineacion="center", espacio_despues=200))

    for patron, tam in ((r"\{\\normalsize (Angel[^\\]*?)\\par\}", 12),
                        (r"\{\\small \\textsuperscript\{1\}([^\\]*?)\\par\}", 10),
                        (r"\{\\small (angelparejo@[^\\]*?)\\par\}", 10)):
        m = re.search(patron, tex)
        if m:
            cuerpo.append(parrafo(run(limpiar(m.group(1)), tam=tam),
                                  alineacion="center", espacio_despues=60))

    # ---------------- resúmenes ----------------
    for etiqueta, patron in (
            ("Resumen", r"\\textbf\{Resumen\.\}\\;\s*\\small\\justifying\s*\n(.*?)\n\\par"),
            ("Palabras clave", r"\\textbf\{\\small Palabras clave:\}\\;\s*\{\\small ([^}]*)\}"),
            ("Abstract", r"\\textbf\{Abstract\.\}\\;\s*\\small\\justifying\s*\n(.*?)\n\\par"),
            ("Keywords", r"\\textbf\{\\small Keywords:\}\\;\s*\{\\small ([^}]*)\}")):
        m = re.search(patron, tex, re.S)
        if m:
            cuerpo.append(parrafo(
                run(etiqueta + ". ", negrita=True) + runs_desde_tex(resolver_refs(m.group(1))),
                alineacion="both", espacio_antes=120))

    # ---------------- cuerpo ----------------
    ini = tex.index("\\section{Introducción}")
    fin = tex.index("\\section*{Agradecimientos}")
    texto_cuerpo = tex[ini:fin]

    n_sec = 0
    n_sub = 0
    n_fig = 0
    n_tab = 0
    n_ec = 0

    # trocear respetando entornos completos
    piezas = re.split(
        r"(\\section\{[^}]*\}|\\subsection\{[^}]*\}"
        r"|\\begin\{table\*?\}.*?\\end\{table\*?\}"
        r"|\\begin\{figure\}.*?\\end\{figure\}"
        r"|\\begin\{equation\}.*?\\end\{equation\}"
        r"|\\begin\{itemize\}.*?\\end\{itemize\})",
        texto_cuerpo, flags=re.S)

    for pieza in piezas:
        p = pieza.strip()
        if not p:
            continue

        m = re.match(r"\\section\{([^}]*)\}$", p)
        if m:
            n_sec += 1
            n_sub = 0
            cuerpo.append(parrafo(
                run("%d. %s" % (n_sec, limpiar(m.group(1))), negrita=True, tam=13),
                espacio_antes=300, espacio_despues=120))
            continue

        m = re.match(r"\\subsection\{([^}]*)\}$", p)
        if m:
            n_sub += 1
            cuerpo.append(parrafo(
                run("%d.%d. %s" % (n_sec, n_sub, limpiar(m.group(1))),
                    negrita=True, tam=12),
                espacio_antes=200, espacio_despues=100))
            continue

        if p.startswith("\\begin{table"):
            n_tab += 1
            bloques = extraer_entorno(p, "tabularx")
            if bloques:
                filas = filas_de_tabularx(bloques[0])
                n_col = max(len(f) for f in filas)
                total = 9000
                anchos = ([1700] + [(total - 1700) // (n_col - 1)] * (n_col - 1)
                          if n_col > 1 else [total])
                cuerpo.append(tabla(filas, anchos))
            m = re.search(r"\\caption\{(.*?)\}\s*\n", p, re.S)
            if m:
                cuerpo.append(parrafo(
                    run("Tabla %d. " % n_tab, negrita=True, tam=10)
                    + runs_desde_tex(resolver_refs(m.group(1))),
                    espacio_antes=60))
            m = re.search(r"\\fignota\{(.*?)\}\s*\n?\\end\{table", p, re.S)
            if m:
                cuerpo.append(parrafo(
                    run("Nota: ", negrita=True, tam=9)
                    + runs_desde_tex(resolver_refs(m.group(1))),
                    espacio_despues=180))
            continue

        if p.startswith("\\begin{figure}"):
            n_fig += 1
            m = re.search(r"\\includegraphics\[[^\]]*\]\{([^}]+)\}", p)
            if m:
                ruta = base / m.group(1)
                if ruta.exists():
                    ancho, alto = dimensiones_jpeg(ruta)
                    cuerpo.append(figura(img_rel(m.group(1)), ancho, alto,
                                         Path(m.group(1)).name, n_fig))
            m = re.search(r"\\caption\{(.*?)\}\s*\n", p, re.S)
            if m:
                cuerpo.append(parrafo(
                    run("Fig. %d. " % n_fig, negrita=True, tam=10)
                    + runs_desde_tex(resolver_refs(m.group(1))),
                    espacio_despues=180))
            continue

        if p.startswith("\\begin{equation}"):
            n_ec += 1
            contenido = re.sub(r"\\begin\{equation\}|\\end\{equation\}", "", p)
            contenido = re.sub(r"\\label\{[^}]*\}", "", contenido)
            contenido = re.sub(r"\\begin\{aligned\}|\\end\{aligned\}", "", contenido)
            contenido = contenido.replace("\\\\", " ").replace("&", "")
            cuerpo.append(parrafo(
                run(limpiar_math(limpiar(contenido)), cursiva=True)
                + run("     (%d)" % n_ec),
                alineacion="center", espacio_antes=100, espacio_despues=100))
            continue

        if p.startswith("\\begin{itemize}"):
            for punto in re.findall(r"\\item\s+(.*?)(?=\\item|\\end\{itemize\})",
                                    p, re.S):
                cuerpo.append(parrafo(
                    run("•  ") + runs_desde_tex(resolver_refs(punto.strip())),
                    alineacion="both", sangria=(560, 280), espacio_despues=60))
            continue

        for bloque in re.split(r"\n\s*\n", p):
            bloque = bloque.strip()
            if not bloque or bloque.startswith("%"):
                continue
            cuerpo.append(parrafo(runs_desde_tex(resolver_refs(bloque)),
                                  alineacion="both"))

    # ---------------- agradecimientos y referencias ----------------
    m = re.search(r"\\section\*\{Agradecimientos\}(.*?)\\phantomsection", tex, re.S)
    if m:
        cuerpo.append(parrafo(run("Agradecimientos", negrita=True, tam=13),
                              espacio_antes=300, espacio_despues=120))
        cuerpo.append(parrafo(runs_desde_tex(resolver_refs(m.group(1).strip())),
                              alineacion="both"))

    cuerpo.append(parrafo(run("Referencias", negrita=True, tam=13),
                          espacio_antes=300, espacio_despues=120))
    bloque_refs = tex[tex.index("\\section*{Referencias}"):]
    for ref in re.findall(r"\n([A-ZÁÉÍÓÚÑa-z][^\n]*?)\\par", bloque_refs):
        cuerpo.append(parrafo(runs_desde_tex(ref), alineacion="both",
                              sangria=(560, 560), espacio_despues=80,
                              interlineado=280))

    escribir_docx(salida_path, "".join(cuerpo), imagenes, base)
    return len(cuerpo), len(imagenes)


# ---------------------------------------------------------------------------
# Empaquetado
# ---------------------------------------------------------------------------
def escribir_docx(salida, cuerpo_xml, imagenes, base_figuras):
    ns = (
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"'
    )
    # Carta, márgenes 1,25", numeración de líneas continua
    sectpr = (
        "<w:sectPr>"
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" '
        'w:header="720" w:footer="720" w:gutter="0"/>'
        '<w:lnNumType w:countBy="1" w:restart="continuous" w:distance="360"/>'
        "</w:sectPr>"
    )
    documento = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                 "<w:document %s><w:body>%s%s</w:body></w:document>"
                 % (ns, cuerpo_xml, sectpr))

    estilos = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:docDefaults><w:rPrDefault><w:rPr>"
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
        'w:eastAsia="Times New Roman" w:cs="Times New Roman"/>'
        '<w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="es-ES"/>'
        "</w:rPr></w:rPrDefault><w:pPrDefault><w:pPr>"
        '<w:spacing w:after="120" w:line="360" w:lineRule="auto"/>'
        "</w:pPr></w:pPrDefault></w:docDefaults>"
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
        '<w:name w:val="Normal"/></w:style>'
        "</w:styles>"
    )

    rels_doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" '
                'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
                'Target="styles.xml"/>')
    for nombre, rid in imagenes:
        rels_doc += ('<Relationship Id="%s" '
                     'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                     'Target="media/%s"/>' % (rid, nombre))
    rels_doc += "</Relationships>"

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="jpeg" ContentType="image/jpeg"/>'
        '<Default Extension="jpg" ContentType="image/jpeg"/>'
        '<Override PartName="/word/document.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        "</Types>"
    )

    rels_raiz = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" '
                 'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
                 'Target="word/document.xml"/></Relationships>')

    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels_raiz)
        z.writestr("word/document.xml", documento)
        z.writestr("word/styles.xml", estilos)
        z.writestr("word/_rels/document.xml.rels", rels_doc)
        for nombre, _ in imagenes:
            ruta = base_figuras / "figures" / nombre
            if ruta.exists():
                z.write(ruta, "word/media/%s" % nombre)


def main():
    tex = Path(sys.argv[1]) if len(sys.argv) > 1 else TEX_POR_DEFECTO
    salida = Path(sys.argv[2]) if len(sys.argv) > 2 else SALIDA_POR_DEFECTO
    if not tex.exists():
        print("No existe %s" % tex, file=sys.stderr)
        return 2
    n_par, n_img = construir(tex, salida)
    print("OK %s" % salida.relative_to(ROOT))
    print("   %d bloques, %d figuras incrustadas, %d KB"
          % (n_par, n_img, salida.stat().st_size // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
