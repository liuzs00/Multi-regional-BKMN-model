"""
Render a markdown document to PDF.  Usage: py -3 tools/md_to_pdf.py <in.md> [out.pdf]

Landscape A4, because the outline carries a wide ASCII citation graph and a
three-column table whose middle column runs long; portrait clips both.
"""
import os
import sys

import markdown
from xhtml2pdf import pisa

CSS = """
@page { size: A4 landscape; margin: 1.6cm 1.8cm; }
body   { font-family: Helvetica, Arial, sans-serif; font-size: 8.5pt;
         line-height: 1.35; color: #16202b; }
h1     { font-size: 17pt; margin: 0 0 4pt 0; }
h2     { font-size: 11.5pt; margin: 14pt 0 4pt 0; color: #0e7c86;
         border-bottom: 0.6pt solid #cfd6dd; padding-bottom: 2pt; }
p      { margin: 0 0 6pt 0; }
code, pre { font-family: Courier, monospace; font-size: 6.4pt; color: #16202b; }
pre    { background: #f4f6f8; padding: 6pt; line-height: 1.15; }
table  { width: 100%; border-collapse: collapse; margin: 4pt 0 9pt 0; }
th     { background: #eef2f5; font-size: 8pt; text-align: left;
         padding: 3pt 5pt; border-bottom: 0.8pt solid #9aa6b5; }
td     { padding: 3pt 5pt; border-bottom: 0.4pt solid #e4e8ec;
         vertical-align: top; }
hr     { border: 0; border-top: 0.4pt solid #cfd6dd; margin: 10pt 0; }
strong { color: #16202b; }
"""


# The core PDF fonts carry no box-drawing or maths glyphs, so anything outside
# Latin-1 renders as a filled square.  Transliterate rather than embed a font:
# the markdown source keeps the characters that make it readable in an editor.
GLYPHS = {
    "─": "-", "│": "|", "┌": "+", "┐": "+",
    "└": "+", "┘": "+", "├": "+", "┤": "+",
    "┬": "+", "┴": "+", "┼": "+",
    "▼": "v", "▲": "^", "→": "->", "←": "<-",
    "≈": "~", "≫": ">>", "≪": "<<", "≠": "!=",
    "−": "-", "≤": "<=", "≥": ">=",
}


def transliterate(s):
    for a, b in GLYPHS.items():
        s = s.replace(a, b)
    return s


def convert(src, dest=None):
    dest = dest or os.path.splitext(src)[0] + ".pdf"
    with open(src, encoding="utf-8") as f:
        html = markdown.markdown(transliterate(f.read()),
                                 extensions=["tables", "fenced_code"])
    doc = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head>" \
          f"<body>{html}</body></html>"
    with open(dest, "wb") as out:
        status = pisa.CreatePDF(doc, dest=out, encoding="utf-8")
    if status.err:
        raise SystemExit(f"failed: {status.err} error(s)")
    print(f"{dest}  ({os.path.getsize(dest)/1024:.0f} kB)")
    return dest


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    convert(*sys.argv[1:3])
