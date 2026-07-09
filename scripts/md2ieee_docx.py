#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md2ieee_docx.py -- Convierte un artículo en Markdown al formato del template
IEEE Conference (conference-template-letter.docx), con cumplimiento 100%.

Método (air-gapped, solo stdlib):
  - Se conserva byte a byte el "esqueleto" del template (styles.xml, theme,
    settings, numbering.xml, fontTable, footer1.xml, docProps, _rels,
    [Content_Types].xml, customXml, foot/endnotes).
  - Se REGENERA únicamente word/document.xml en namespace OOXML *Strict*
    (raíz http://purl.oclc.org/ooxml/wordprocessingml/main, w:conformance="strict"),
    heredando columnas/márgenes/footer del <w:sectPr> del template.
  - Se reempaqueta con zipfile.

Autonumeración del template (verificada en numbering.xml):
  Heading1 -> "I."   Heading2 -> "A."   references -> "[n]"
  figurecaption -> "Fig. n."   tablehead -> "TABLE I."   bulletlist -> viñeta
  => se ELIMINA la numeración manual del texto fuente.

Uso:
  python3 scripts/md2ieee_docx.py <in.md> <template.docx> <out.docx>
"""

import sys
import os
import re
import zipfile
import shutil
import tempfile
import struct
import zlib
import xml.dom.minidom as minidom

# --------------------------------------------------------------------------
# Namespaces raíz Strict del template (idénticos a los del template original).
# --------------------------------------------------------------------------
W = "http://purl.oclc.org/ooxml/wordprocessingml/main"

DOC_OPEN = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:document '
    'xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex" '
    'xmlns:cx1="http://schemas.microsoft.com/office/drawing/2015/9/8/chartex" '
    'xmlns:cx2="http://schemas.microsoft.com/office/drawing/2015/10/21/chartex" '
    'xmlns:cx3="http://schemas.microsoft.com/office/drawing/2016/5/9/chartex" '
    'xmlns:cx4="http://schemas.microsoft.com/office/drawing/2016/5/10/chartex" '
    'xmlns:cx5="http://schemas.microsoft.com/office/drawing/2016/5/11/chartex" '
    'xmlns:cx6="http://schemas.microsoft.com/office/drawing/2016/5/12/chartex" '
    'xmlns:cx7="http://schemas.microsoft.com/office/drawing/2016/5/13/chartex" '
    'xmlns:cx8="http://schemas.microsoft.com/office/drawing/2016/5/14/chartex" '
    'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
    'xmlns:aink="http://schemas.microsoft.com/office/drawing/2016/ink" '
    'xmlns:am3d="http://schemas.microsoft.com/office/drawing/2017/model3d" '
    'xmlns:o="urn:schemas-microsoft-com:office:office" '
    'xmlns:oel="http://schemas.microsoft.com/office/2019/extlst" '
    'xmlns:r="http://purl.oclc.org/ooxml/officeDocument/relationships" '
    'xmlns:m="http://purl.oclc.org/ooxml/officeDocument/math" '
    'xmlns:v="urn:schemas-microsoft-com:vml" '
    'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
    'xmlns:wp="http://purl.oclc.org/ooxml/drawingml/wordprocessingDrawing" '
    'xmlns:w10="urn:schemas-microsoft-com:office:word" '
    'xmlns:w="http://purl.oclc.org/ooxml/wordprocessingml/main" '
    'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
    'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" '
    'xmlns:w16cex="http://schemas.microsoft.com/office/word/2018/wordml/cex" '
    'xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid" '
    'xmlns:w16="http://schemas.microsoft.com/office/word/2018/wordml" '
    'xmlns:w16sdtdh="http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash" '
    'xmlns:w16se="http://schemas.microsoft.com/office/word/2015/wordml/symex" '
    'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
    'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
    'mc:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh wne wp14" '
    'w:conformance="strict">'
)
DOC_CLOSE = "</w:document>"

# --- Incrustación de figura -----------------------------------------------
# La línea "ISBN/XX/$XX.00 ©20XX IEEE" del footer de 1.ª página es una nota de
# copyright de ACTAS DE CONGRESO; no aplica a una revista arbitrada. Se blanquea.
STRIP_CONF_COPYRIGHT = True

FIG_SENTINEL = "%%FIGURE_DRAWING%%"                 # marcador reemplazado en build_docx
FIG_SVG_REL = "paper/figures/fig1_modelo_multicapa.svg"   # fuente vectorial
FIG_RID_PNG = "rId13"                               # respaldo raster
FIG_RID_SVG = "rId14"                               # SVG nativo (Word 2016+)
EMU_PER_PT = 12700
FIG_MAX_PT = 251                                    # ancho de columna (in-column)

# --- sectPr del template (verificados) -----------------------------------
# Sección de título: 1 columna, titlePg, footer en primera página.
SECTPR_TITLE = (
    '<w:sectPr>'
    '<w:footerReference w:type="first" r:id="rId8"/>'
    '<w:pgSz w:w="612pt" w:h="792pt" w:code="1"/>'
    '<w:pgMar w:top="54pt" w:right="44.65pt" w:bottom="72pt" w:left="44.65pt" '
    'w:header="36pt" w:footer="36pt" w:gutter="0pt"/>'
    '<w:cols w:space="36pt"/>'
    '<w:titlePg/>'
    '<w:docGrid w:linePitch="360"/>'
    '</w:sectPr>'
)
# Cuerpo a dos columnas (continuo).
SECTPR_2COL = (
    '<w:sectPr>'
    '<w:type w:val="continuous"/>'
    '<w:pgSz w:w="612pt" w:h="792pt" w:code="1"/>'
    '<w:pgMar w:top="54pt" w:right="45.35pt" w:bottom="72pt" w:left="45.35pt" '
    'w:header="36pt" w:footer="36pt" w:gutter="0pt"/>'
    '<w:cols w:num="2" w:space="18pt"/>'
    '<w:docGrid w:linePitch="360"/>'
    '</w:sectPr>'
)

# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------
def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def run(text, bold=False, italic=False):
    """Un <w:r> con escape XML y preservación de espacios."""
    if text == "":
        return ""
    rpr = ""
    if bold or italic:
        rpr = "<w:rPr>" + ("<w:b/>" if bold else "") + ("<w:i/>" if italic else "") + "</w:rPr>"
    sp = ' xml:space="preserve"' if (text != text.strip() or "  " in text) else ""
    return f"<w:r>{rpr}<w:t{sp}>{esc(text)}</w:t></w:r>"


def parse_inline(text):
    """Convierte **negrita**/*cursiva* en una lista de runs XML.

    Antes de procesar, une cada cita numérica [n] al texto previo con un espacio
    de no separación (U+00A0) para que la referencia no quede huérfana al saltar
    de línea (p. ej. "...recuperación [9]." nunca parte "[9]" a la línea siguiente).
    """
    text = re.sub(r"\s+(\[\d+\])", " \\1", text)
    runs = []
    i = 0
    n = len(text)
    buf = ""

    def flush(b=False, it=False):
        nonlocal buf
        if buf:
            runs.append(run(buf, b, it))
            buf = ""

    while i < n:
        # Salto de línea explícito dentro de la celda/párrafo (<br> o <br/>).
        if text.startswith("<br/>", i) or text.startswith("<br>", i):
            flush()
            runs.append("<w:r><w:br/></w:r>")
            i += 5 if text.startswith("<br/>", i) else 4
            continue
        # Código/identificador en línea `...` -> run en cursiva (sin backticks).
        # Se integra con el Times del cuerpo (convención académica en español),
        # en lugar de un segundo tipo de letra monoespaciado.
        if text[i] == "`":
            j = text.find("`", i + 1)
            if j != -1:
                flush()
                runs.append(run(text[i + 1:j], italic=True))
                i = j + 1
                continue
        if text.startswith("**", i):
            j = text.find("**", i + 2)
            if j != -1:
                flush()
                inner = text[i + 2:j]
                runs.append(run(inner, bold=True))
                i = j + 2
                continue
        if text[i] == "*" and not text.startswith("**", i):
            j = text.find("*", i + 1)
            if j != -1:
                flush()
                inner = text[i + 1:j]
                runs.append(run(inner, italic=True))
                i = j + 1
                continue
        buf += text[i]
        i += 1
    flush()
    return "".join(runs)


def split_author(text):
    """Descompone la línea de autor en las líneas del bloque IEEE.

    Separadores admitidos entre bloques: em/en dash o guion con espacios.
    El primer bloque "Nombre, Organización" se parte en dos líneas.
    El email (con @ y sin espacios) va en su propia línea.
    """
    segs = [s.strip() for s in re.split(r"\s+[—–-]\s+", text) if s.strip()]
    lines = []
    for s in segs:
        if "@" in s and " " not in s:            # email / ORCID
            lines.append(s)
        elif not lines and "," in s:             # "Nombre, Organización"
            name, org = s.split(",", 1)
            lines.append(name.strip())
            lines.append(org.strip())
        else:
            lines.append(s)
    return lines


def build_author(text):
    """Párrafo Author (centrado, 9 pt) con una línea por dato, como el template."""
    sz = '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
    runs = []
    for i, ln in enumerate(split_author(text)):
        br = "<w:br/>" if i > 0 else ""
        runs.append(f'<w:r>{sz}{br}<w:t xml:space="preserve">{esc(ln)}</w:t></w:r>')
    # Línea en blanco extra tras el email (separación con el Resumen).
    runs.append(f'<w:r>{sz}<w:br/></w:r>')
    return para("Author", "".join(runs))


def para(style, inner_runs, extra_ppr="", ind=None):
    """Construye un <w:p> con pStyle=style y runs ya serializados."""
    ppr = f'<w:pStyle w:val="{style}"/>'
    if ind:
        ppr += ind
    ppr += extra_ppr
    return f"<w:p><w:pPr>{ppr}</w:pPr>{inner_runs}</w:p>"


# --------------------------------------------------------------------------
# Parser de Markdown -> lista de bloques
# --------------------------------------------------------------------------
HEADING5_TITLES = {"referencias", "references", "agradecimientos",
                   "acknowledgment", "acknowledgments", "acknowledgement"}

RE_H1_NUM = re.compile(r"^[IVXLC]+\.\s+")          # "I. ", "II. "
RE_H2_NUM = re.compile(r"^[IVXLC]+\.[A-Z]\.?\s+")  # "III.A ", "III.A. "
RE_REF_NUM = re.compile(r"^\[\d+\]\s+")            # "[1] "
RE_TABLE_LBL = re.compile(r"^\*\*\s*(?:Tabla|Table|Cuadro)\s+[IVXLC0-9]+\.?\s*\*\*\s*")
RE_FIG_LBL = re.compile(r"^\*\*\s*(?:Fig\.?|Figura|Figure)\s*[0-9IVXLC]*\.?\s*\*\*\s*")
RE_HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
RE_IMG = re.compile(r"^!\[(.*?)\]\((.*?)\)\s*$")  # ![alt](ruta) -> figura, alt = pie


def parse_markdown(md):
    md = RE_HTML_COMMENT.sub("", md)
    lines = md.split("\n")
    blocks = []
    i = 0
    title_seen = False
    author_seen = False
    in_refs = False

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()

        if line == "":
            i += 1
            continue

        # Título
        if line.startswith("# ") and not line.startswith("## "):
            blocks.append(("title", line[2:].strip()))
            title_seen = True
            i += 1
            continue

        # Encabezados de sección
        if line.startswith("#### "):
            blocks.append(("h3", line[5:].strip()))
            i += 1
            continue
        if line.startswith("### "):
            txt = line[4:].strip()
            txt = RE_H2_NUM.sub("", txt)
            blocks.append(("h2", txt))
            i += 1
            continue
        if line.startswith("## "):
            txt = line[3:].strip()
            key = txt.lower().strip()
            if RE_H1_NUM.match(txt):
                # Sección numerada del cuerpo (I., II., ...): Heading1 autonumera.
                blocks.append(("h1", RE_H1_NUM.sub("", txt)))
                in_refs = False
            elif key in HEADING5_TITLES:
                # Rótulo normalizado del template para secciones conocidas.
                label = "References" if key in ("referencias", "references") else "Acknowledgment"
                blocks.append(("h5", label))
                in_refs = key in ("referencias", "references")
            else:
                # Encabezado sin numeral romano => material de cierre sin numerar
                # (p. ej. "Disponibilidad de datos y código"): Heading5.
                blocks.append(("h5", txt))
                in_refs = False
            i += 1
            continue

        # Autor: primera línea no vacía tras el título que no es abstract/keywords/heading
        if title_seen and not author_seen and not line.startswith("**") and not line.startswith("#"):
            blocks.append(("author", line))
            author_seen = True
            i += 1
            continue

        # Abstract
        low = line.lower()
        if low.startswith("**resumen**") or low.startswith("**abstract**"):
            body = re.sub(r"^\*\*\s*(?:Resumen|Abstract)\s*\*\*\s*[—\-–]?\s*", "", line,
                          flags=re.I)
            blocks.append(("abstract", body))
            i += 1
            continue

        # Keywords
        if low.startswith("**palabras clave**") or low.startswith("**palabras clave —**") \
                or low.startswith("**keywords**") or low.startswith("**índice de términos**") \
                or low.startswith("**palabras clave —"):
            body = re.sub(r"^\*\*\s*(?:Palabras\s+Clave|Keywords|Índice\s+de\s+términos)\s*\*\*\s*[—\-–]?\s*",
                          "", line, flags=re.I)
            blocks.append(("keywords", body))
            i += 1
            continue

        # Tabla en Markdown
        if line.startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl.append(lines[i].strip())
                i += 1
            blocks.append(("table", tbl))
            continue

        # Título de tabla (**Tabla I.** ...)
        if RE_TABLE_LBL.match(line):
            body = RE_TABLE_LBL.sub("", line)
            body = re.sub(r"\*\*$", "", body).strip()
            blocks.append(("tablehead", body))
            i += 1
            continue

        # Pie de figura (**Fig. 1.** ...)
        if RE_FIG_LBL.match(line):
            body = RE_FIG_LBL.sub("", line)
            body = re.sub(r"\*\*$", "", body).strip()
            blocks.append(("figure", body))
            i += 1
            continue

        # Imagen Markdown ![alt](ruta). Si le sigue un pie **Fig. N.** (la línea
        # ![]() es solo previsualización Markdown de la misma figura), se omite: el
        # pie ya la incrusta. Si no hay pie, el alt actúa como pie autonumerado.
        m_img = RE_IMG.match(line)
        if m_img:
            k2 = i + 1
            while k2 < len(lines) and lines[k2].strip() == "":
                k2 += 1
            if k2 < len(lines) and RE_FIG_LBL.match(lines[k2].strip()):
                i += 1
                continue
            blocks.append(("figure", m_img.group(1).strip()))
            i += 1
            continue

        # Viñetas
        if line.startswith("- ") or line.startswith("* "):
            blocks.append(("bullet", line[2:].strip()))
            i += 1
            continue

        # Referencia
        if in_refs and RE_REF_NUM.match(line):
            body = RE_REF_NUM.sub("", line)
            blocks.append(("reference", body))
            i += 1
            continue

        # Párrafo normal
        blocks.append(("body", line))
        i += 1

    return blocks


# --------------------------------------------------------------------------
# Construcción de la tabla (<w:tbl>)
# --------------------------------------------------------------------------
def build_table(rows, widths_pt=None, center_cols=None):
    """rows: lista de líneas '| a | b |'. La 2ª línea es el separador '|---|'.

    widths_pt   -- anchos de columna en puntos (lista); si None, reparto proporcional.
    center_cols -- índices de columnas cuyas celdas de DATOS van centradas
                   (sobrescribe el jc=both del estilo tablecopy para valores cortos).
    """
    def cells(r):
        parts = [c.strip() for c in r.strip().strip("|").split("|")]
        return parts

    data = [cells(r) for r in rows if not re.match(r"^\|[\s:|-]+\|?$", r.strip())]
    if not data:
        return ""
    ncol = max(len(r) for r in data)
    data = [r + [""] * (ncol - len(r)) for r in data]
    center_cols = center_cols or set()

    # Formato del template: tabla IN-COLUMN (cabe en UNA de las dos columnas).
    # Ancho de columna del cuerpo a 2 col = (612 - 45.35 - 45.35 - 18) / 2 = 251.65 pt.
    TOTAL_PT = 251
    if widths_pt and len(widths_pt) == ncol:
        widths = list(widths_pt)
    elif ncol >= 2:
        first = round(TOTAL_PT * 0.16)          # 1.ª columna más estrecha
        rest = (TOTAL_PT - first) // (ncol - 1)
        widths = [first] + [rest] * (ncol - 1)
        widths[-1] = TOTAL_PT - first - rest * (ncol - 2)  # ajuste para sumar exacto
    else:
        widths = [TOTAL_PT]
    wpt = [f"{w}pt" for w in widths]

    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in wpt)

    tblpr = (
        "<w:tblPr>"
        '<w:tblW w:w="0pt" w:type="auto"/>'
        '<w:jc w:val="center"/>'
        "<w:tblBorders>"
        '<w:top w:val="single" w:sz="2" w:space="0" w:color="auto"/>'
        '<w:start w:val="single" w:sz="2" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="single" w:sz="2" w:space="0" w:color="auto"/>'
        '<w:end w:val="single" w:sz="2" w:space="0" w:color="auto"/>'
        '<w:insideH w:val="single" w:sz="2" w:space="0" w:color="auto"/>'
        '<w:insideV w:val="single" w:sz="2" w:space="0" w:color="auto"/>'
        "</w:tblBorders>"
        '<w:tblLayout w:type="fixed"/>'
        # Márgenes de celda reducidos (2pt L/R) para aprovechar el ancho in-column.
        "<w:tblCellMar>"
        '<w:top w:w="0pt" w:type="dxa"/><w:start w:w="2pt" w:type="dxa"/>'
        '<w:bottom w:w="0pt" w:type="dxa"/><w:end w:w="2pt" w:type="dxa"/>'
        "</w:tblCellMar>"
        '<w:tblLook w:firstRow="0" w:lastRow="0" w:firstColumn="0" '
        'w:lastColumn="0" w:noHBand="0" w:noVBand="0"/>'
        "</w:tblPr>"
    )

    trs = []
    for ri, r in enumerate(data):
        is_head = (ri == 0)
        style = "tablecolhead" if is_head else "tablecopy"
        tcs = []
        for ci, cell in enumerate(r):
            tcpr = f'<w:tcPr><w:tcW w:w="{wpt[ci]}" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
            ppr = f'<w:pStyle w:val="{style}"/>'
            if (not is_head) and ci in center_cols:
                ppr += '<w:jc w:val="center"/>'   # centra valores cortos bajo su encabezado
            p = f'<w:p><w:pPr>{ppr}</w:pPr>{parse_inline(cell)}</w:p>'
            tcs.append(f"<w:tc>{tcpr}{p}</w:tc>")
        trpr = "<w:trPr><w:cantSplit/>" + ('<w:tblHeader/>' if is_head else "") + \
               '<w:jc w:val="center"/></w:trPr>'
        trs.append(f"<w:tr>{trpr}{''.join(tcs)}</w:tr>")

    return f"<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>{''.join(trs)}</w:tbl>"


# --------------------------------------------------------------------------
# Ensamblado del <w:body>
# --------------------------------------------------------------------------
REF_IND = '<w:ind w:start="17.70pt" w:hanging="17.70pt"/>'


def build_body(blocks):
    out = []            # cadenas XML de párrafos/tablas
    author_idx = None

    for k, (kind, payload) in enumerate(blocks):
        if kind == "title":
            out.append(para("papertitle", parse_inline(payload)))
        elif kind == "author":
            author_idx = len(out)
            out.append(build_author(payload))
        elif kind == "abstract":
            # rótulo "Resumen" en cursiva + em dash + cuerpo
            inner = run("Resumen", italic=True) + run("—") + parse_inline(payload)
            out.append(para("Abstract", inner))
        elif kind == "keywords":
            inner = run("Palabras Clave—") + parse_inline(payload)
            out.append(para("Keywords", inner))
        elif kind == "h1":
            out.append(para("Heading1", parse_inline(payload)))
        elif kind == "h2":
            out.append(para("Heading2", parse_inline(payload)))
        elif kind == "h3":
            out.append(para("Heading3", parse_inline(payload)))
        elif kind == "h5":
            out.append(para("Heading5", parse_inline(payload)))
        elif kind == "bullet":
            out.append(para("bulletlist", parse_inline(payload)))
        elif kind == "reference":
            out.append(para("references", parse_inline(payload), ind=REF_IND))
        elif kind == "figure":
            # párrafo centrado con la imagen (sentinel → drawing en build_docx)
            # seguido del pie autonumerado ("Fig. n.")
            out.append(f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr>{FIG_SENTINEL}</w:p>')
            out.append(para("figurecaption", parse_inline(payload)))
        elif kind == "tablehead":
            out.append(para("tablehead", parse_inline(payload)))
        elif kind == "table":
            # Todas las tablas IN-COLUMN: fluyen dentro de la columna, sin
            # saltos de sección (preserva el flujo de dos columnas del template).
            header = payload[0] if payload else ""
            if "¿Promueve?" in header:
                # Tabla II (v2): col. "Escenario" reducida a F1–F4 (el mecanismo
                # va en la nota), lo que libera ancho para encabezados completos.
                # Encabezados largos en 2 líneas (<br> en el .md); datos centrados.
                out.append(build_table(
                    payload,
                    widths_pt=[42, 50, 68, 20, 71],   # suma 251 pt (in-column)
                    center_cols={1, 2, 3, 4},
                ))
            else:
                out.append(build_table(payload))
        else:  # body
            out.append(para("BodyText", parse_inline(payload)))

    # Sección 0 (título+autor) a 1 columna: sectPr en el párrafo del autor.
    if author_idx is not None:
        out[author_idx] = _inject_sectpr(out[author_idx], SECTPR_TITLE)

    # sectPr final del documento: cuerpo a 2 columnas (continuo).
    return "<w:body>" + "".join(out) + SECTPR_2COL + "</w:body>"


def _inject_sectpr(paragraph_xml, sectpr):
    """Inserta un sectPr dentro del <w:pPr> de un <w:p> ya serializado."""
    assert paragraph_xml.startswith("<w:p>") and "<w:pPr>" in paragraph_xml
    return paragraph_xml.replace("</w:pPr>", sectpr + "</w:pPr>", 1)


# --------------------------------------------------------------------------
# Figura: PNG de respaldo (stdlib) + drawing XML con SVG nativo
# --------------------------------------------------------------------------
def _png_chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))


def make_png(width, height, rects):
    """PNG RGB (stdlib). `rects`: lista de (x, y, w, h, (r, g, b)) sobre fondo blanco."""
    row = bytearray([255, 255, 255] * width)
    buf = [bytearray(row) for _ in range(height)]
    for x, y, w, h, (r, g, b) in rects:
        for yy in range(max(0, y), min(height, y + h)):
            line = buf[yy]
            for xx in range(max(0, x), min(width, x + w)):
                line[xx * 3:xx * 3 + 3] = bytes((r, g, b))
    raw = bytearray()
    for line in buf:
        raw += b"\x00" + line
    comp = zlib.compress(bytes(raw), 9)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", ihdr)
            + _png_chunk(b"IDAT", comp) + _png_chunk(b"IEND", b""))


def _hex(c):
    return (int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16))


def build_figure_assets(svg_bytes):
    """Devuelve (drawing_xml, png_bytes). Escala in-column por el ancho de columna."""
    m = re.search(rb'viewBox="([\d.\s]+)"', svg_bytes)
    vw, vh = (620.0, 566.0)
    if m:
        nums = [float(x) for x in m.group(1).split()]
        if len(nums) == 4:
            vw, vh = nums[2], nums[3]
    cx = int(round(FIG_MAX_PT * EMU_PER_PT))
    cy = int(round(FIG_MAX_PT * (vh / vw) * EMU_PER_PT))

    # Respaldo raster (escala 0.5 del viewBox): cajas de colores del modelo, sin texto.
    sx = 0.5
    pw, ph = int(vw * sx), int(vh * sx)
    boxes = [(90, 26, "#dbeafe"), (90, 156, "#e2e8f0"),
             (90, 286, "#dcfce7"), (90, 416, "#fef3c7")]  # O, K, D, M
    rects = []
    for bx, by, col in boxes:
        rects.append((int(bx * sx), int(by * sx), int(440 * sx), int(80 * sx), _hex(col)))
    for ay in (106, 236, 366):  # flechas verticales
        rects.append((int(309 * sx), int(ay * sx), 2, int(48 * sx), (0x33, 0x41, 0x55)))
    png = make_png(pw, ph, rects)

    A = "http://purl.oclc.org/ooxml/drawingml/main"
    PIC = "http://purl.oclc.org/ooxml/drawingml/picture"
    ASVG = "http://schemas.microsoft.com/office/drawing/2016/SVG/main"
    drawing = (
        "<w:drawing>"
        '<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:docPr id="1" name="Figura 1 - Modelo multicapa"/>'
        f'<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="{A}" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        f'<a:graphic xmlns:a="{A}">'
        f'<a:graphicData uri="{PIC}">'
        f'<pic:pic xmlns:pic="{PIC}">'
        '<pic:nvPicPr><pic:cNvPr id="1" name="fig1_modelo_multicapa"/><pic:cNvPicPr/></pic:nvPicPr>'
        "<pic:blipFill>"
        f'<a:blip r:embed="{FIG_RID_PNG}">'
        '<a:extLst><a:ext uri="{96DAC541-7B7A-43D3-8B79-37D633B846F1}">'
        f'<asvg:svgBlip xmlns:asvg="{ASVG}" r:embed="{FIG_RID_SVG}"/>'
        "</a:ext></a:extLst>"
        "</a:blip>"
        "<a:stretch><a:fillRect/></a:stretch>"
        "</pic:blipFill>"
        "<pic:spPr>"
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        "</pic:spPr>"
        "</pic:pic></a:graphicData></a:graphic>"
        "</wp:inline></w:drawing>"
    )
    return drawing, png


# --------------------------------------------------------------------------
# Empaquetado
# --------------------------------------------------------------------------
def build_docx(md_path, template_path, out_path):
    with open(md_path, encoding="utf-8") as f:
        md = f.read()
    blocks = parse_markdown(md)
    body = build_body(blocks)
    document_xml = DOC_OPEN + body + DOC_CLOSE

    # --- Figura: incrustar SVG (+ PNG de respaldo) o degradar a marcador ---
    fig_embedded = False
    png_bytes = None
    svg_bytes = None
    if FIG_SENTINEL in document_xml:
        svg_path = os.path.join(os.path.dirname(os.path.abspath(md_path)), FIG_SVG_REL)
        if os.path.exists(svg_path):
            with open(svg_path, "rb") as f:
                svg_bytes = f.read()
            drawing, png_bytes = build_figure_assets(svg_bytes)
            document_xml = document_xml.replace(FIG_SENTINEL, "<w:r>" + drawing + "</w:r>")
            fig_embedded = True
        else:
            marker = run(f"[INSERTAR AQUÍ: {FIG_SVG_REL} — no encontrado]")
            document_xml = document_xml.replace(FIG_SENTINEL, marker)

    # Validación de buen formato XML
    minidom.parseString(document_xml.encode("utf-8"))

    tmp = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(template_path) as z:
            names = z.namelist()
            z.extractall(tmp)
        # Reescribe SOLO document.xml
        with open(os.path.join(tmp, "word", "document.xml"), "w", encoding="utf-8") as f:
            f.write(document_xml)

        # Blanquea la nota de copyright de actas de congreso (©20XX IEEE) del
        # footer de 1.ª página: no aplica a una revista arbitrada.
        footer_path = os.path.join(tmp, "word", "footer1.xml")
        if STRIP_CONF_COPYRIGHT and os.path.exists(footer_path):
            with open(footer_path, encoding="utf-8") as f:
                ftr = f.read()
            ftr2 = re.sub(r"(<w:t[^>]*>)[^<]*IEEE[^<]*(</w:t>)", r"\1\2", ftr)
            if ftr2 != ftr:
                with open(footer_path, "w", encoding="utf-8") as f:
                    f.write(ftr2)

        extra = []  # archivos añadidos (media) que no están en el template
        if fig_embedded:
            os.makedirs(os.path.join(tmp, "word", "media"), exist_ok=True)
            with open(os.path.join(tmp, "word", "media", "image1.png"), "wb") as f:
                f.write(png_bytes)
            with open(os.path.join(tmp, "word", "media", "image2.svg"), "wb") as f:
                f.write(svg_bytes)
            extra = ["word/media/image1.png", "word/media/image2.svg"]

            # Relaciones de imagen en document.xml.rels
            rels_path = os.path.join(tmp, "word", "_rels", "document.xml.rels")
            with open(rels_path, encoding="utf-8") as f:
                rels = f.read()
            add = (
                f'<Relationship Id="{FIG_RID_PNG}" '
                'Type="http://purl.oclc.org/ooxml/officeDocument/relationships/image" '
                'Target="media/image1.png"/>'
                f'<Relationship Id="{FIG_RID_SVG}" '
                'Type="http://purl.oclc.org/ooxml/officeDocument/relationships/image" '
                'Target="media/image2.svg"/>'
            )
            rels = rels.replace("</Relationships>", add + "</Relationships>")
            with open(rels_path, "w", encoding="utf-8") as f:
                f.write(rels)

            # Content types: Default para png y svg
            ct_path = os.path.join(tmp, "[Content_Types].xml")
            with open(ct_path, encoding="utf-8") as f:
                ct = f.read()
            ins = ""
            if 'Extension="png"' not in ct:
                ins += '<Default Extension="png" ContentType="image/png"/>'
            if 'Extension="svg"' not in ct:
                ins += '<Default Extension="svg" ContentType="image/svg+xml"/>'
            ct = ct.replace("<Default Extension=\"xml\"",
                            ins + "<Default Extension=\"xml\"", 1)
            with open(ct_path, "w", encoding="utf-8") as f:
                f.write(ct)

        # Reempaqueta conservando el orden original + media añadida
        if os.path.exists(out_path):
            os.remove(out_path)
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
            for name in names + extra:
                z.write(os.path.join(tmp, name), name)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    return blocks, document_xml, fig_embedded


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    md_path, template_path, out_path = sys.argv[1:4]
    blocks, doc, fig_embedded = build_docx(md_path, template_path, out_path)

    # Reporte por estilo
    from collections import Counter
    styles_used = re.findall(r'<w:pStyle w:val="([^"]*)"', doc)
    print(f"[OK] Generado: {out_path}")
    print(f"[OK] Bloques parseados: {len(blocks)}")
    print(f"[OK] document.xml: {len(doc)} bytes, XML bien formado")
    print("[OK] Conteo por estilo de párrafo:")
    for s, c in sorted(Counter(styles_used).items()):
        print(f"       {s:16} {c}")
    tbls = doc.count("<w:tbl>")
    print(f"[OK] Tablas <w:tbl>: {tbls}")
    print(f"[OK] Saltos de sección <w:sectPr>: {doc.count('<w:sectPr>')}")
    print(f"[OK] Figura incrustada (SVG + PNG respaldo): {'SÍ' if fig_embedded else 'no (marcador)'}")


if __name__ == "__main__":
    main()
