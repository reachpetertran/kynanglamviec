#!/usr/bin/env python3
"""Logo kynanglamviec.com, dựa trên khung huy hiệu của logo daynentang.com.
Giữ: dáng huy hiệu vòm, mặt trời, núi tuyết, rừng thông, dải băng chữ, thanh "EST. 2026".
Đổi: bảng màu theo site (xanh teal + vàng hổ phách); cảnh động vật -> lộ trình nghề nghiệp:
đường zíc-zắc 5 bậc lên đỉnh có cờ, người đi từ chân núi, tòa văn phòng bên trái.
Chữ được chuyển thành path (font Inter Display, OFL; Poppins thiếu chữ "Ệ") để hiển thị giống nhau mọi máy.
Chạy: python3 _build/art/logo_art.py  -> _build/static/assets/logo*.svg (+ PNG nếu có rsvg-convert)
"""
from pathlib import Path
import shutil
import subprocess

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = Path(__file__).resolve().parents[1] / "static/assets"
FONT_DIR = Path("/usr/share/fonts/opentype/inter")

SKY, SKY2 = "#0f3b39", "#174f4c"        # nền trời, dãy núi xa
BRAND, BRAND2 = "#14524f", "#1f7a74"
M_DARK, M_LIT = "#237a6a", "#4fae86"   # sườn núi tối / sáng
GROUND, PINE = "#123f3c", "#0f3533"
INK, CREAM = "#0a2523", "#fffdf8"
ACC, ACC_TOP, ACC_DK = "#d98a1c", "#f2b24a", "#b86f0f"


def text_path(s, font_file, size, cx, baseline, fill, max_w=None, tracking=0.0):
    """Trả về <path> của chuỗi s, căn giữa tại cx. tracking: khoảng cách thêm (đơn vị em)."""
    f = TTFont(FONT_DIR / font_file)
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    upm = f["head"].unitsPerEm
    names = [cmap[ord(ch)] for ch in s]
    adv = [hmtx[n][0] + tracking * upm for n in names]
    width = (sum(adv) - tracking * upm) * size / upm
    if max_w and width > max_w:
        size *= max_w / width
        width = max_w
    k = size / upm
    pen = SVGPathPen(gs)
    x = cx - width / 2
    for n, a in zip(names, adv):
        gs[n].draw(TransformPen(pen, (k, 0, 0, -k, x, baseline)))
        x += a * k
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>'


def pine(x, base, h, color=PINE):
    w = h * 0.42
    t = [f'<path d="M{x-w/2:.1f} {base-h*0.05:.1f} L{x:.1f} {base-h*0.62:.1f} L{x+w/2:.1f} {base-h*0.05:.1f}Z"/>',
         f'<path d="M{x-w*0.4:.1f} {base-h*0.38:.1f} L{x:.1f} {base-h*0.85:.1f} L{x+w*0.4:.1f} {base-h*0.38:.1f}Z"/>',
         f'<path d="M{x-w*0.29:.1f} {base-h*0.62:.1f} L{x:.1f} {base-h:.1f} L{x+w*0.29:.1f} {base-h*0.62:.1f}Z"/>',
         f'<rect x="{x-1.5:.1f}" y="{base-h*0.06:.1f}" width="3" height="{h*0.1:.1f}"/>']
    return f'<g fill="{color}">{"".join(t)}</g>'


def person(x, base, s=1.0, bag=None, color=INK):
    """Người đi bộ, nhìn nghiêng sang phải. bag: 'backpack' | 'briefcase' | None."""
    g = [f'<circle cx="0" cy="-35" r="5.2"/>',
         f'<path d="M-4.5 -28 Q0 -30.5 4.5 -28 L5.5 -13 L-5 -13Z"/>',                     # thân
         f'<path d="M-2.5 -14 L-8 -1 M2.5 -14 L6.5 -1" stroke="{color}" stroke-width="4.2" stroke-linecap="round" fill="none"/>',
         f'<path d="M-3.5 -26 L-8.5 -17 M3.5 -26 L8.5 -18" stroke="{color}" stroke-width="3.2" stroke-linecap="round" fill="none"/>']
    if bag == "backpack":
        g.append('<rect x="-10.5" y="-28" width="6.5" height="12" rx="2.5"/>')
    if bag == "briefcase":
        g.append('<rect x="6.5" y="-19" width="9" height="7" rx="1.5"/><path d="M9 -19 v-2 h4 v2" stroke="%s" stroke-width="1.3" fill="none"/>' % color)
    return f'<g transform="translate({x} {base}) scale({s})" fill="{color}">{"".join(g)}</g>'


def building(x, w, top, base, win_cols, color=INK):
    out = [f'<rect x="{x}" y="{top}" width="{w}" height="{base-top}" fill="{color}"/>']
    cw = w / win_cols
    y = top + 6
    row = 0
    while y < base - 10:
        for c in range(win_cols):
            lit = (row * 3 + c * 5 + int(x)) % 4 != 0
            out.append(f'<rect x="{x + c*cw + cw*0.28:.1f}" y="{y:.1f}" width="{cw*0.44:.1f}" height="4" '
                       f'fill="{ACC_TOP if lit else SKY2}"/>')
        y += 9
        row += 1
    return "".join(out)


DEFS = (f'<defs><clipPath id="kc"><path d="M48 392 V186 A152 152 0 0 1 352 186 V392 Z"/></clipPath>'
        f'<linearGradient id="ksun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACC_TOP}"/>'
        f'<stop offset="1" stop-color="{ACC}"/></linearGradient></defs>')

# đường lên đỉnh: 5 bậc (5 điểm mốc), zíc-zắc trên sườn núi
TRAIL = [(186, 312), (246, 286), (176, 258), (226, 232), (192, 207), (204, 186)]
STEPS = [(246, 286), (176, 258), (226, 232), (192, 207), (204, 186)]


def scene():
    s = [f'<rect width="400" height="440" fill="{SKY}"/>',
         f'<circle cx="200" cy="176" r="92" fill="url(#ksun)"/>',
         # dãy núi xa
         f'<path d="M30 300 L110 205 L150 245 L200 150 L250 230 L290 195 L370 300Z" fill="{SKY2}"/>',
         # núi chính
         f'<path d="M70 312 L200 168 L330 312Z" fill="{M_DARK}"/>',
         f'<path d="M200 168 L330 312 L232 312 L214 250 L222 214Z" fill="{M_LIT}"/>',
         f'<path d="M200 168 L178 193 L190 190 L200 200 L210 189 L222 194Z" fill="{CREAM}"/>',
         # cờ trên đỉnh
         f'<path d="M200 170 V128" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>',
         f'<path d="M201.5 129 L228 136 L201.5 144Z" fill="{ACC_TOP}" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>',
         # chim
         f'<path d="M120 120 q7 -7 14 0 q7 -7 14 0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>',
         f'<path d="M262 104 q5 -5 10 0 q5 -5 10 0" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>']
    # đường mòn + 5 mốc
    d = "M" + " L".join(f"{x} {y}" for x, y in TRAIL)
    s.append(f'<path d="{d}" fill="none" stroke="{CREAM}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 9"/>')
    for i, (x, y) in enumerate(STEPS):
        r = 4 + i * 0.6
        s.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{ACC_TOP}" stroke="{INK}" stroke-width="1.8"/>')
    # rừng thông bên phải
    for x, h in [(300, 46), (322, 62), (344, 52), (364, 66), (382, 48)]:
        s.append(pine(x, 312, h))
    # tòa văn phòng bên trái
    s.append(building(52, 26, 244, 314, 2))
    s.append(building(80, 20, 266, 314, 2))
    s.append(building(102, 30, 226, 314, 3))
    s.append(f'<rect x="114" y="214" width="6" height="12" fill="{INK}"/>')
    s.append(building(134, 18, 276, 314, 2))
    # mặt đất
    s.append(f'<path d="M0 304 Q200 290 400 304 L400 440 L0 440Z" fill="{GROUND}"/>')
    # người: học sinh đeo cặp -> người đi làm xách cặp
    s.append(person(166, 314, 0.9, "backpack"))
    s.append(person(268, 312, 0.85, "briefcase"))
    s.append(person(290, 312, 0.78))
    return "".join(s)


def badge(with_text=True):
    vb_h = 428 if with_text else 412
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 {vb_h}" role="img" aria-label="Kỹ Năng Làm Việc">',
             '<title>Kỹ Năng Làm Việc – kynanglamviec.com</title>', DEFS,
             f'<path d="M36 400 V186 A164 164 0 0 1 364 186 V400 Z" fill="{SKY}"/>',
             f'<g clip-path="url(#kc)">{scene()}</g>',
             f'<path d="M48 392 V186 A152 152 0 0 1 352 186 V392 Z" fill="none" stroke="{CREAM}" stroke-width="4"/>']
    if with_text:
        parts.append(f'<path d="M14 322 H386 L374 352 L386 382 H14 L26 352Z" fill="{CREAM}" stroke="{SKY}" stroke-width="6"/>')
        parts.append(text_path("KỸ NĂNG LÀM VIỆC", "InterDisplay-Bold.otf", 27, 200, 362, SKY, max_w=300, tracking=0.06))
        parts.append(f'<rect x="27" y="392" width="346" height="30" fill="{SKY}"/>')
        parts.append(text_path("EST. 2026 · KYNANGLAMVIEC.COM", "InterDisplay-SemiBold.otf", 14, 200, 412, ACC_TOP, max_w=272, tracking=0.12))
    parts.append("</svg>")
    return "".join(parts)


def icon():
    """Biểu tượng vuông 64x64 cho favicon, đầu trang."""
    trail = "M28 52 L41 46 L26 40 L37 34 L30 28 L32 22"
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            f'<defs><clipPath id="ki"><rect width="64" height="64" rx="13"/></clipPath>'
            f'<linearGradient id="kis" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACC_TOP}"/>'
            f'<stop offset="1" stop-color="{ACC}"/></linearGradient></defs>'
            f'<g clip-path="url(#ki)"><rect width="64" height="64" fill="{SKY}"/>'
            f'<circle cx="32" cy="27" r="17" fill="url(#kis)"/>'
            f'<path d="M4 54 L32 20 L60 54Z" fill="{M_DARK}"/><path d="M32 20 L60 54 L40 54 L37 38Z" fill="{M_LIT}"/>'
            f'<path d="M32 20 L27 26 L32 28 L37 26Z" fill="{CREAM}"/>'
            f'<path d="M32 21 V9" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>'
            f'<path d="M32.8 9.3 L41 11.6 L32.8 14Z" fill="{ACC_TOP}" stroke="{INK}" stroke-width=".8" stroke-linejoin="round"/>'
            f'<path d="{trail}" fill="none" stroke="{CREAM}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<rect y="52" width="64" height="12" fill="{GROUND}"/></g></svg>')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {"logo.svg": badge(True), "logo-khong-chu.svg": badge(False), "logo-icon.svg": icon()}
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
    (OUT / "favicon.svg").write_text(files["logo-icon.svg"], encoding="utf-8")
    if shutil.which("rsvg-convert"):
        for src, dst, w in [("logo.svg", "logo-512.png", 512), ("logo.svg", "logo-1024.png", 1024),
                            ("logo-icon.svg", "apple-touch-icon.png", 180), ("logo-icon.svg", "logo-icon-512.png", 512)]:
            subprocess.run(["rsvg-convert", "-w", str(w), "-o", str(OUT / dst), str(OUT / src)], check=True)
    print("OK:", ", ".join(sorted(p.name for p in OUT.glob("logo*")) + ["favicon.svg", "apple-touch-icon.png"]))


if __name__ == "__main__":
    main()
