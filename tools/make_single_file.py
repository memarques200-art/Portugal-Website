"""Build a single self-contained HTML file (images embedded) from index.html.

Usage:  python3 tools/make_single_file.py  ->  writes portugal-single-file.html
"""
import base64, mimetypes, pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text(encoding="utf-8")

def embed(m):
    path = root / m.group(2)
    mime = mimetypes.guess_type(path.name)[0]
    data = base64.b64encode(path.read_bytes()).decode()
    return f'{m.group(1)}"data:{mime};base64,{data}"'

html = re.sub(r'((?:src|href)=)"(images/[^"]+)"', embed, html)
out = root / "portugal-single-file.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB)")
