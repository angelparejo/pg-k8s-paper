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
# Interludio a 1 columna (continuo) para tablas/figuras que ocupan todo el ancho.
SECTPR_1COL_SPAN = (
    '<w:sectPr>'
    '<w:type w:val="continuous"/>'
    '<w:pgSz w:w="612pt" w:h="792pt" w:code="1"/>'
    '<w:pgMar w:top="54pt" w:right="45.35pt" w:bottom="72pt" w:left="45.35pt" '
    'w:header="36pt" w:footer="36pt" w:gutter="0pt"/>'
    '<w:cols w:space="36pt"/>'
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
    """Convierte **negrita**/*cursiva* en una lista de runs XML."""
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
def build_table(rows):
    """rows: lista de líneas '| a | b |'. La 2ª línea es el separador '|---|'."""
    def cells(r):
        parts = [c.strip() for c in r.strip().strip("|").split("|")]
        return parts

    data = [cells(r) for r in rows if not re.match(r"^\|[\s:|-]+\|?$", r.strip())]
    if not data:
        return ""
    ncol = max(len(r) for r in data)
    data = [r + [""] * (ncol - len(r)) for r in data]

    # Ancho total ~ ancho de página menos márgenes (612pt - 2*45.35pt) en dxa.
    total = 10420
    # Primera columna algo más estrecha; el resto reparte.
    if ncol >= 2:
        first = int(total * 0.16)
        rest = (total - first) // (ncol - 1)
        widths = [first] + [rest] * (ncol - 1)
        widths[-1] = total - first - rest * (ncol - 2) if ncol > 2 else total - first
    else:
        widths = [total]

    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)

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
            tcpr = f'<w:tcPr><w:tcW w:w="{widths[ci]}" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
            p = f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{parse_inline(cell)}</w:p>'
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
    table_spans = []    # (idx_pre, idx_table_end) para cada tabla ancha
    pending_pre = None  # índice del párrafo previo a un título tablehead

    for k, (kind, payload) in enumerate(blocks):
        if kind == "title":
            out.append(para("papertitle", parse_inline(payload)))
        elif kind == "author":
            author_idx = len(out)
            out.append(para("Author", parse_inline(payload)))
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
            # marcador de imagen (paso manual) + pie autonumerado
            marker = run("[INSERTAR AQUÍ: paper/figures/fig1_modelo_multicapa.pdf]")
            out.append(para("BodyText", marker))
            out.append(para("figurecaption", parse_inline(payload)))
        elif kind == "tablehead":
            # el párrafo emitido justo antes cierra la corrida a 2 columnas
            pending_pre = len(out) - 1
            out.append(para("tablehead", parse_inline(payload)))
        elif kind == "table":
            out.append(build_table(payload))
            # si no hubo tablehead inmediatamente antes, el "pre" es el párrafo previo
            pre = pending_pre if pending_pre is not None else len(out) - 2
            table_spans.append((pre, len(out) - 1))
            pending_pre = None
        else:  # body
            out.append(para("BodyText", parse_inline(payload)))

    # --- Inyección de saltos de sección ---
    # Sección 0 (título+autor) a 1 columna: sectPr en el párrafo del autor.
    if author_idx is not None:
        out[author_idx] = _inject_sectpr(out[author_idx], SECTPR_TITLE)

    # Cada tabla ancha => interludio a 1 columna. Se procesa de la última a la
    # primera para que las inserciones no invaliden los índices anteriores.
    closer = f"<w:p><w:pPr>{SECTPR_1COL_SPAN}</w:pPr></w:p>"
    for pre, tend in sorted(table_spans, reverse=True):
        out.insert(tend + 1, closer)  # cierra el interludio a 1 columna tras la tabla
        if 0 <= pre < len(out) and out[pre].startswith("<w:p>") and "<w:pPr>" in out[pre]:
            out[pre] = _inject_sectpr(out[pre], SECTPR_2COL)  # cierra la corrida a 2 columnas
        else:
            # no hay párrafo apto antes de la tabla: inserta un cierre explícito
            out.insert(pre + 1, f"<w:p><w:pPr>{SECTPR_2COL}</w:pPr></w:p>")

    # sectPr final del documento: cuerpo a 2 columnas (continuo)
    return "<w:body>" + "".join(out) + SECTPR_2COL + "</w:body>"


def _inject_sectpr(paragraph_xml, sectpr):
    """Inserta un sectPr dentro del <w:pPr> de un <w:p> ya serializado."""
    assert paragraph_xml.startswith("<w:p>") and "<w:pPr>" in paragraph_xml
    return paragraph_xml.replace("</w:pPr>", sectpr + "</w:pPr>", 1)


# --------------------------------------------------------------------------
# Empaquetado
# --------------------------------------------------------------------------
def build_docx(md_path, template_path, out_path):
    with open(md_path, encoding="utf-8") as f:
        md = f.read()
    blocks = parse_markdown(md)
    body = build_body(blocks)
    document_xml = DOC_OPEN + body + DOC_CLOSE

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
        # Reempaqueta conservando el orden original
        if os.path.exists(out_path):
            os.remove(out_path)
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
            for name in names:
                z.write(os.path.join(tmp, name), name)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    return blocks, document_xml


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    md_path, template_path, out_path = sys.argv[1:4]
    blocks, doc = build_docx(md_path, template_path, out_path)

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


if __name__ == "__main__":
    main()
