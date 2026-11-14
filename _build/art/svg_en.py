#!/usr/bin/env python3
"""English edition of the N4–N7 illustrations, made from the Vietnamese SVGs.

The Vietnamese art scripts (n4_art.py … n7_art.py) stay the single source of layout.
This script copies each generated SVG, swaps every <text> label using
_build/art/en/<course>.yaml, and takes the title / aria-label from the alt text
of the English lesson that uses the picture.

Run after the Vietnamese art scripts:
  python3 _build/art/svg_en.py [n4 n5 n6 n7]
Output: _build/static/assets/img/en/<course>/*.svg
It stops with an error if a label has no translation, and warns when an English
label is much wider than the Vietnamese one (check the picture by eye).
"""
import html, re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
IMG = ROOT / "_build/static/assets/img"
LESSONS = ROOT / "content/en/lessons"


def alts():
    out = {}
    for f in LESSONS.glob("*.md"):
        for src, alt in re.findall(r'<img src="[./]*assets/img/en/([^"]+)" alt="([^"]*)"', f.read_text(encoding="utf-8")):
            out[src] = html.unescape(alt)
    return out


def run(code):
    cfg = yaml.safe_load((ROOT / f"_build/art/en/{code}.yaml").read_text(encoding="utf-8"))
    tr, files = cfg["text"], cfg["files"]
    alt = alts()
    out = IMG / "en" / code
    out.mkdir(parents=True, exist_ok=True)
    missing, wide = [], []

    for vi_name, en_name in files.items():
        svg = (IMG / code / vi_name).read_text(encoding="utf-8")

        def swap(m):
            attrs, s = m.group(1), html.unescape(m.group(2))
            if not re.search(r"[^\W\d_]", s):          # numbers and symbols only
                return m.group(0)
            if s not in tr:
                missing.append(f"{vi_name}: {s}")
                return m.group(0)
            en = str(tr[s])
            if len(en) > len(s) * 1.15 + 3:
                wide.append(f"{en_name}: '{en}' ({len(en)}) vs '{s}' ({len(s)})")
            return f"<text{attrs}>{html.escape(en, quote=False)}</text>"

        svg = re.sub(r"<text([^>]*)>(.*?)</text>", swap, svg)
        title = alt.get(f"{code}/{en_name}")
        if not title:
            missing.append(f"{en_name}: no English lesson uses this picture (alt text)")
        else:
            t = html.escape(title, quote=True)
            svg = re.sub(r'aria-label="[^"]*"', f'aria-label="{t}"', svg, count=1)
            svg = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title, quote=False)}</title>", svg, count=1, flags=re.S)
        (out / en_name).write_text(svg, encoding="utf-8")

    for w in wide:
        print("  wide?", w)
    if missing:
        print("MISSING:\n  " + "\n  ".join(missing))
        sys.exit(1)
    print(f"{code}: {len(files)} SVG -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    for c in sys.argv[1:] or ["n4", "n5", "n6", "n7"]:
        run(c)
