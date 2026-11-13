#!/usr/bin/env python3
"""Hình minh họa tự vẽ (SVG) cho khóa N1. Không dùng ảnh ngoài.
Chạy: python3 _build/art/n1_art.py  -> _build/static/assets/img/n1/*.svg
Nguyên tắc: nhiều nghề, nam nữ làm đủ loại nghề, không dùng tên/logo thật.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parents[1] / "static/assets/img/n1"
W, H = 640, 400
BRAND, BRAND2, ACC, ACCBG, INK = "#14524f", "#1f7a74", "#d98a1c", "#fdf3e2", "#1d2a33"
SKIN = ["#f6d1a8", "#e8b383", "#c98d5c", "#9c6340", "#f1c9a0"]
HAIR = ["#2b1d14", "#1a1410", "#4a3020", "#3b2a20", "#a8a8a8"]
FONT = 'font-family="system-ui,-apple-system,Segoe UI,Roboto,Noto Sans,Arial,sans-serif"'


def svg(title, body, bg="#eef6f5"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)}</title><rect width="{W}" height="{H}" rx="18" fill="{bg}"/>{body}</svg>')


def text(x, y, s, size=14, fill=INK, anchor="middle", weight=400):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" {FONT}>{escape(s)}</text>')


def lines(x, y, rows, size=13, gap=17, **kw):
    return "".join(text(x, y + i * gap, r, size, **kw) for i, r in enumerate(rows))


def bubble(x, y, w, h, rows, tx, ty, size=13, fill="#fff", stroke="#9fb9b6"):
    """Bóng nói: hộp (x,y,w,h), đuôi trỏ về (tx,ty)."""
    cx = x + w / 2
    bx = min(max(tx, x + 18), x + w - 18)
    by = y + h if ty > y + h else y
    tail = f'<path d="M{bx-9},{by} L{tx},{ty} L{bx+9},{by}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    box = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    cover = f'<path d="M{bx-8},{by} L{bx+8},{by}" stroke="{fill}" stroke-width="3"/>'
    n = len(rows)
    ty0 = y + h / 2 - (n - 1) * (size + 4) / 2 + size * 0.35
    return tail + box + cover + lines(cx, ty0, rows, size, size + 4)


def label(x, y, s, fill=BRAND, color="#fff", size=13):
    w = len(s) * size * 0.56 + 18
    return (f'<rect x="{x - w/2}" y="{y - size}" width="{w}" height="{size + 10}" rx="{(size+10)/2}" fill="{fill}"/>'
            + text(x, y + 1, s, size, color, weight=600))


# ------------------------------------------------------------------ người
def hair_svg(style, c):
    if style == "short":
        return f'<path d="M-23,-172 Q-24,-198 0,-198 Q24,-198 23,-172 Q16,-186 0,-186 Q-14,-186 -23,-172Z" fill="{c}"/>'
    if style == "long":
        return (f'<path d="M-25,-175 Q-28,-200 0,-200 Q28,-200 25,-175 L27,-135 Q16,-128 14,-140 L14,-176 Q0,-186 -14,-176 L-14,-140 Q-16,-128 -27,-135Z" fill="{c}"/>')
    if style == "bun":
        return (f'<circle cx="0" cy="-201" r="11" fill="{c}"/>'
                f'<path d="M-23,-170 Q-24,-197 0,-197 Q24,-197 23,-170 Q14,-185 0,-185 Q-14,-185 -23,-170Z" fill="{c}"/>')
    if style == "pony":
        return (f'<path d="M20,-185 Q40,-180 34,-150 Q30,-160 22,-170Z" fill="{c}"/>'
                f'<path d="M-23,-170 Q-24,-197 0,-197 Q24,-197 23,-170 Q14,-185 0,-185 Q-14,-185 -23,-170Z" fill="{c}"/>')
    if style == "curly":
        return "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}"/>' for x, y in
                       [(-18, -184), (-8, -194), (6, -195), (17, -186), (-22, -172), (22, -172)])
    if style == "bald":
        return f'<path d="M-23,-168 Q-24,-176 -20,-178 L-20,-166Z M23,-168 Q24,-176 20,-178 L20,-166Z" fill="{c}"/>'
    return ""


def hat_svg(hat):
    if hat == "chef":
        return ('<rect x="-18" y="-206" width="36" height="16" fill="#fff" stroke="#cfd8d6"/>'
                '<circle cx="-12" cy="-210" r="11" fill="#fff" stroke="#cfd8d6"/><circle cx="0" cy="-216" r="13" fill="#fff" stroke="#cfd8d6"/>'
                '<circle cx="12" cy="-210" r="11" fill="#fff" stroke="#cfd8d6"/><rect x="-17" y="-206" width="34" height="8" fill="#fff"/>')
    if hat == "helmet":
        return (f'<path d="M-27,-180 Q-26,-210 0,-210 Q26,-210 27,-180Z" fill="{ACC}"/>'
                '<rect x="-31" y="-182" width="62" height="6" rx="3" fill="#b8700f"/>')
    if hat == "cap":
        return (f'<path d="M-23,-178 Q-22,-202 0,-202 Q22,-202 23,-178Z" fill="{BRAND}"/>'
                f'<rect x="10" y="-182" width="26" height="6" rx="3" fill="{BRAND}"/>')
    if hat == "pilot":
        return ('<path d="M-25,-180 Q-24,-204 0,-205 Q24,-204 25,-180Z" fill="#203a5a"/>'
                '<rect x="-27" y="-184" width="54" height="7" rx="3" fill="#111"/><circle cx="0" cy="-195" r="4" fill="#f2c94c"/>')
    if hat == "non":  # nón lá
        return '<path d="M-44,-180 L0,-222 L44,-180Z" fill="#e9d9a6" stroke="#b9a46a"/>'
    return ""


ARMS = {  # (vai trái -> tay trái), (vai phải -> tay phải), tọa độ bàn tay
    "down": ((-30, -88), (30, -88)),
    "hold": ((-12, -112), (12, -112)),
    "wave": ((-30, -88), (44, -205)),
    "point": ((-30, -88), (62, -140)),
    "give": ((-30, -88), (52, -118)),
    "write": ((-6, -108), (14, -102)),
    "both_up": ((-44, -205), (44, -205)),
    "side": ((-34, -100), (40, -110)),
}


def person(x, y, s=1.0, skin=0, hair="short", hc=0, shirt=BRAND2, pants="#34495e", pose="down",
           hat=None, coat=None, apron=None, prop="", flip=False, skirt=False):
    sk = SKIN[skin]
    hcol = HAIR[hc]
    (lx, ly), (rx, ry) = ARMS[pose]
    g = []
    # chân
    if skirt:
        g.append(f'<path d="M-24,-84 L-30,-36 L30,-36 L24,-84Z" fill="{pants}"/>')
        g.append(f'<rect x="-17" y="-38" width="10" height="32" fill="{sk}"/><rect x="7" y="-38" width="10" height="32" fill="{sk}"/>')
    else:
        g.append(f'<rect x="-20" y="-86" width="17" height="80" rx="6" fill="{pants}"/><rect x="3" y="-86" width="17" height="80" rx="6" fill="{pants}"/>')
    g.append('<ellipse cx="-12" cy="-4" rx="13" ry="6" fill="#2d2d2d"/><ellipse cx="12" cy="-4" rx="13" ry="6" fill="#2d2d2d"/>')
    # thân
    g.append(f'<rect x="-26" y="-148" width="52" height="68" rx="13" fill="{shirt}"/>')
    if coat:
        g.append(f'<path d="M-26,-135 Q-26,-148 -13,-148 L-4,-148 L-4,-80 L-26,-80Z M26,-135 Q26,-148 13,-148 L4,-148 L4,-80 L26,-80Z" fill="{coat}"/>')
    if apron:
        g.append(f'<path d="M-17,-128 L17,-128 L20,-82 L-20,-82Z" fill="{apron}"/>')
    # tay
    g.append(f'<path d="M-22,-140 L{lx},{ly}" stroke="{coat or shirt}" stroke-width="12" stroke-linecap="round"/>')
    g.append(f'<path d="M22,-140 L{rx},{ry}" stroke="{coat or shirt}" stroke-width="12" stroke-linecap="round"/>')
    g.append(f'<circle cx="{lx}" cy="{ly}" r="7" fill="{sk}"/><circle cx="{rx}" cy="{ry}" r="7" fill="{sk}"/>')
    # đầu
    g.append(f'<rect x="-7" y="-156" width="14" height="12" fill="{sk}"/>')
    if hair == "long":
        g.append(hair_svg("long", hcol))
    g.append(f'<circle cx="0" cy="-172" r="23" fill="{sk}"/>')
    if hair != "long":
        g.append(hair_svg(hair, hcol))
    else:
        g.append(f'<path d="M-23,-172 Q-24,-199 0,-199 Q24,-199 23,-172 Q14,-188 0,-188 Q-14,-188 -23,-172Z" fill="{hcol}"/>')
    g.append('<circle cx="-8" cy="-171" r="2.6" fill="#222"/><circle cx="8" cy="-171" r="2.6" fill="#222"/>')
    g.append('<path d="M-7,-161 Q0,-155 7,-161" stroke="#7a3b2e" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    g.append(f'<circle cx="-14" cy="-163" r="3.5" fill="#f29b8a" opacity=".45"/><circle cx="14" cy="-163" r="3.5" fill="#f29b8a" opacity=".45"/>')
    if hat:
        g.append(hat_svg(hat))
    if prop:
        g.append(PROPS[prop](rx, ry, lx, ly))
    t = f"translate({x},{y}) scale({-s if flip else s},{s})"
    return f'<g transform="{t}">{"".join(g)}</g>'


# đồ vật cầm tay (tọa độ cục bộ của người)
PROPS = {
    "wrench": lambda rx, ry, lx, ly: f'<path d="M{rx},{ry} l18,-26" stroke="#7f8c8d" stroke-width="6" stroke-linecap="round"/><circle cx="{rx+20}" cy="{ry-29}" r="7" fill="none" stroke="#7f8c8d" stroke-width="5"/>',
    "book": lambda rx, ry, lx, ly: f'<rect x="-22" y="-126" width="44" height="30" rx="3" fill="#c0392b"/><rect x="-1" y="-126" width="2" height="30" fill="#fff"/>',
    "notebook": lambda rx, ry, lx, ly: f'<rect x="-20" y="-128" width="34" height="40" rx="3" fill="#fff" stroke="#999"/><path d="M-14,-118 h22 M-14,-110 h22 M-14,-102 h16" stroke="#9ab" stroke-width="2"/><path d="M{rx},{ry} l10,-18" stroke="{ACC}" stroke-width="4" stroke-linecap="round"/>',
    "clipboard": lambda rx, ry, lx, ly: f'<rect x="-20" y="-132" width="38" height="48" rx="4" fill="#b07a45"/><rect x="-16" y="-126" width="30" height="38" fill="#fff"/><path d="M-12,-118 h22 M-12,-110 h22 M-12,-102 h14" stroke="#9ab" stroke-width="2"/>',
    "pan": lambda rx, ry, lx, ly: f'<ellipse cx="{rx+26}" cy="{ry-2}" rx="22" ry="7" fill="#333"/><path d="M{rx},{ry} L{rx+8},{ry-1}" stroke="#333" stroke-width="5"/>',
    "tray": lambda rx, ry, lx, ly: f'<rect x="{rx-4}" y="{ry-10}" width="46" height="5" rx="2" fill="#8d6e63"/><path d="M{rx+4},{ry-10} q8,-14 16,0 M{rx+20},{ry-10} q8,-14 16,0" fill="#e0a85b" stroke="#b07a35"/>',
    "phone": lambda rx, ry, lx, ly: f'<rect x="{rx-7}" y="{ry-24}" width="15" height="26" rx="3" fill="#263238"/><rect x="{rx-5}" y="{ry-21}" width="11" height="17" fill="#80deea"/>',
    "wheel": lambda rx, ry, lx, ly: f'<circle cx="0" cy="-112" r="26" fill="none" stroke="#333" stroke-width="6"/><path d="M-26,-112 h52 M0,-112 v26" stroke="#333" stroke-width="4"/>',
    "blueprint": lambda rx, ry, lx, ly: f'<rect x="-30" y="-128" width="60" height="34" rx="2" fill="#2f6fa8"/><path d="M-24,-120 h20 v14 h-20z M2,-120 h22 M2,-112 h18" stroke="#cfe3f5" stroke-width="1.5" fill="none"/>',
    "box": lambda rx, ry, lx, ly: f'<rect x="-24" y="-132" width="48" height="38" rx="3" fill="#c69c6d" stroke="#8d6e4a"/><path d="M-24,-120 h48" stroke="#8d6e4a"/>',
    "brick": lambda rx, ry, lx, ly: f'<rect x="{rx-4}" y="{ry-12}" width="30" height="14" rx="2" fill="#c0563b" stroke="#8e3b27"/>',
    "seedling": lambda rx, ry, lx, ly: f'<path d="M{lx},{ly} q-4,-20 -14,-26 M{lx},{ly} q2,-22 10,-28 M{lx},{ly} q-1,-18 -2,-30" stroke="#3c9a3c" stroke-width="3" fill="none"/>',
    "pliers": lambda rx, ry, lx, ly: f'<path d="M{rx},{ry} l14,-20 M{rx+6},{ry+2} l14,-20" stroke="#d35400" stroke-width="5" stroke-linecap="round"/><path d="M{rx+14},{ry-20} l6,-10 M{rx+20},{ry-18} l2,-12" stroke="#7f8c8d" stroke-width="4"/>',
    "blocks": lambda rx, ry, lx, ly: f'<rect x="{rx-6}" y="{ry-18}" width="16" height="16" fill="#e74c3c"/><rect x="{rx+12}" y="{ry-18}" width="16" height="16" fill="#3498db"/><rect x="{rx+3}" y="{ry-34}" width="16" height="16" fill="#f1c40f"/>',
    "brush": lambda rx, ry, lx, ly: f'<path d="M{rx},{ry} l12,-22" stroke="#8d6e63" stroke-width="5" stroke-linecap="round"/><path d="M{rx+12},{ry-22} l5,-9" stroke="#e74c3c" stroke-width="7" stroke-linecap="round"/>',
    "card": lambda rx, ry, lx, ly: f'<rect x="-28" y="-138" width="56" height="44" rx="4" fill="#fff" stroke="{BRAND}" stroke-width="2"/><rect x="-28" y="-138" width="56" height="10" rx="4" fill="{BRAND}"/><circle cx="-14" cy="-114" r="7" fill="{ACC}"/><path d="M-2,-118 h22 M-2,-110 h18 M-20,-102 h40" stroke="#9ab" stroke-width="2"/>',
    "mic": lambda rx, ry, lx, ly: f'<path d="M{rx},{ry} l4,-14" stroke="#333" stroke-width="4"/><circle cx="{rx+5}" cy="{ry-18}" r="6" fill="#555"/>',
    "bread": lambda rx, ry, lx, ly: f'<path d="M{rx-2},{ry-4} q20,-14 40,0 q-20,8 -40,0z" fill="#e0a85b" stroke="#b07a35"/>',
    "": lambda *a: "",
}


# ------------------------------------------------------------------ cảnh nền
def ground(y=330, c="#d7e8d0"):
    return f'<rect x="0" y="{y}" width="{W}" height="{H-y}" fill="{c}"/>'


def shop(x, y, w, h, sign, color, awning=ACC):
    stripes = "".join(f'<rect x="{x + i*w/6}" y="{y}" width="{w/12}" height="22" fill="#fff" opacity=".7"/>' for i in range(6))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>'
            f'<rect x="{x-6}" y="{y}" width="{w+12}" height="22" fill="{awning}"/>{stripes}'
            f'<rect x="{x+12}" y="{y-34}" width="{w-24}" height="28" rx="6" fill="#fff" stroke="{BRAND}" stroke-width="2"/>'
            + text(x + w / 2, y - 14, sign, 14, BRAND, weight=700) +
            f'<rect x="{x+w*0.15}" y="{y+40}" width="{w*0.7}" height="{h-60}" rx="4" fill="#cfe7f0" opacity=".8"/>')


def panel(x, y, w, h, title, fill="#fff"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#cfdcda" stroke-width="2"/>'
            + label(x + w / 2, y + 26, title))


def table(x, y, w, c="#b98a5a"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="12" rx="4" fill="{c}"/><rect x="{x+10}" y="{y+12}" width="8" height="40" fill="{c}"/><rect x="{x+w-18}" y="{y+12}" width="8" height="40" fill="{c}"/>'


# ------------------------------------------------------------------ 21 hình
SCENES = {}


def scene(name, title):
    def deco(fn):
        SCENES[name] = (title, fn)
        return fn
    return deco


@scene("l1-pho-nghe", "Một con phố có nhiều nghề: bán bánh mì, dược sĩ, thợ sửa xe, người giao hàng")
def _():
    b = ground(318)
    b += f'<rect x="0" y="318" width="{W}" height="14" fill="#c9c3b4"/>'
    b += shop(20, 110, 170, 208, "Bánh mì", "#f6e3c8")
    b += shop(235, 110, 170, 208, "Nhà thuốc", "#e3f0ea", awning=BRAND2)
    b += shop(450, 110, 170, 208, "Sửa xe", "#e8e4f2", awning="#7b6bb5")
    b += table(50, 262, 110, "#a0522d")
    b += person(105, 318, .62, skin=1, hair="bun", shirt="#e67e22", apron="#fff", pose="hold", prop="bread")
    b += person(320, 318, .62, skin=0, hair="short", hc=1, shirt="#5d6d7e", coat="#fff", pose="hold", prop="box")
    b += person(530, 318, .62, skin=2, hair="pony", shirt="#2c3e50", pants="#2c3e50", pose="side", prop="wrench")
    b += person(196, 372, .5, skin=3, hair="cap", shirt=ACC, pose="hold", prop="box")
    b += person(430, 378, .58, skin=1, hair="long", shirt="#8e44ad", pose="down")
    b += person(470, 378, .4, skin=1, hair="short", shirt="#27ae60", pose="point", flip=True)
    b += bubble(520, 335, 112, 44, ["Mẹ ơi, cô ấy", "làm nghề gì?"], 488, 330, 12)
    return svg(SCENES["l1-pho-nghe"][0], b, "#e8f3fb")


@scene("l1-mot-ngay", "Một ngày của em: sáng gặp tài xế xe buýt, trưa gặp đầu bếp, chiều gặp thầy giáo")
def _():
    b = ""
    for i, (t, bg) in enumerate([("Buổi sáng", "#fff7e6"), ("Buổi trưa", "#f0f7ee"), ("Buổi chiều", "#eef2fb")]):
        b += panel(18 + i * 208, 20, 196, 360, t, bg)
    b += f'<rect x="56" y="186" width="56" height="48" fill="#cfe7f0"/>'
    b += person(86, 292, .55, skin=2, hair="long", shirt=BRAND, pose="hold", prop="wheel")
    b += f'<path fill-rule="evenodd" d="M34,170 h160 a12,12 0 0 1 12,12 v118 h-184 v-118 a12,12 0 0 1 12,-12z M56,186 h56 v48 h-56z" fill="#f2c94c"/>'
    b += f'<rect x="124" y="186" width="60" height="40" rx="4" fill="#cfe7f0"/><rect x="22" y="262" width="184" height="10" fill="#e0b43a"/>'
    b += '<circle cx="66" cy="300" r="14" fill="#333"/><circle cx="166" cy="300" r="14" fill="#333"/>' 
    b += lines(116, 330, ["Tài xế xe buýt", "đưa em đến trường"], 14)
    b += table(250, 250, 128, "#95a5a6")
    b += person(314, 300, .7, skin=0, hair="short", shirt="#fff", pants="#555", hat="chef", pose="hold", prop="pan", apron="#dfe6e9")
    b += lines(314, 330, ["Đầu bếp nấu", "bữa trưa ở trường"], 14)
    b += f'<rect x="440" y="70" width="150" height="90" rx="6" fill="#2e4d3f"/>' + text(515, 112, "2 + 3 = 5", 18, "#fff")
    b += person(515, 300, .7, skin=1, hair="short", hc=2, shirt="#3d6fb6", pose="point", prop="")
    b += lines(515, 330, ["Thầy giáo dạy", "em làm toán"], 14)
    return svg(SCENES["l1-mot-ngay"][0], b, "#fbfaf7")


@scene("l1-the-nghe", "Mẫu Thẻ nghề với 5 ô: tên nghề, làm gì, ở đâu, dùng gì, cần kỹ năng gì")
def _():
    b = f'<rect x="60" y="24" width="520" height="352" rx="18" fill="#fff" stroke="{BRAND}" stroke-width="3"/>'
    b += f'<rect x="60" y="24" width="520" height="52" rx="18" fill="{BRAND}"/><rect x="60" y="56" width="520" height="20" fill="{BRAND}"/>'
    b += text(320, 58, "THẺ NGHỀ", 24, "#fff", weight=800)
    b += f'<rect x="84" y="96" width="170" height="250" rx="12" fill="#fdf3e2"/>'
    b += person(169, 330, .9, skin=1, hair="pony", shirt="#2c3e50", pants="#2c3e50", hat="helmet", pose="side", prop="pliers")
    rows = [("1. Tên nghề", "Thợ điện"), ("2. Làm gì?", "Lắp và sửa đường điện"), ("3. Ở đâu?", "Nhà dân, công trình"),
            ("4. Dùng gì?", "Kìm, bút thử điện, thang"), ("5. Cần kỹ năng gì?", "(Em điền ở Bài 2)")]
    for i, (k, v) in enumerate(rows):
        y = 112 + i * 50
        b += f'<rect x="276" y="{y}" width="282" height="40" rx="8" fill="{"#fdf3e2" if i == 4 else "#eef6f5"}"/>'
        b += text(288, y + 17, k, 13, BRAND, "start", 700) + text(288, y + 34, v, 14, INK if i < 4 else "#8a5200", "start")
    return svg(SCENES["l1-the-nghe"][0], b, "#eef6f5")


@scene("l2-bep", "Nhân viên phục vụ nghe khách gọi món, nhắc lại, rồi báo cho đầu bếp")
def _():
    b = f'<rect x="0" y="300" width="{W}" height="100" fill="#e9dcc9"/>'
    b += f'<rect x="380" y="60" width="240" height="240" fill="#e7eef0"/><rect x="380" y="200" width="240" height="18" fill="#95a5a6"/>'
    b += table(40, 250, 140, "#a0522d")
    b += person(70, 300, .62, skin=0, hair="bald", hc=3, shirt="#7f8c8d", pose="down")
    b += person(250, 330, .7, skin=3, hair="bun", shirt=BRAND2, apron="#fff", pose="write", prop="notebook", flip=True)
    b += person(520, 330, .7, skin=1, hair="short", shirt="#fff", pants="#555", hat="chef", pose="hold", prop="pan", apron="#dfe6e9", flip=True)
    b += bubble(20, 40, 190, 54, ["Cho bác một phở bò,", "không hành nhé."], 78, 166, 13)
    b += bubble(150, 110, 170, 54, ["Dạ, một phở bò,", "không hành ạ."], 246, 186, 13)
    b += bubble(380, 20, 220, 36, ["Bàn 2: phở bò, không hành!"], 330, 220, 13)
    b += label(480, 380, "Nghe đúng → nhắc lại → báo lại", BRAND)
    return svg(SCENES["l2-bep"][0], b, "#fbf5ec")


@scene("l2-dieu-duong", "Nam điều dưỡng giải thích cho bệnh nhân lớn tuổi cách uống thuốc")
def _():
    b = f'<rect x="0" y="300" width="{W}" height="100" fill="#dfe9ef"/>'
    b += f'<rect x="24" y="250" width="150" height="30" rx="8" fill="#fff" stroke="#b0c4ce"/><rect x="24" y="200" width="14" height="120" fill="#9aa"/><rect x="160" y="280" width="12" height="40" fill="#9aa"/><rect x="40" y="238" width="44" height="14" rx="6" fill="#e3edf2"/>'
    b += person(220, 340, .7, skin=0, hair="bun", hc=4, shirt="#b3cde0", pants="#6b7f8a", pose="down")
    b += person(410, 340, .78, skin=2, hair="short", shirt="#7ec4cf", pants="#7ec4cf", pose="hold", prop="clipboard", flip=True)
    b += bubble(300, 30, 250, 56, ["Bác uống 1 viên sau bữa sáng.", "Bác nhắc lại giúp cháu nhé?"], 410, 150, 13)
    b += bubble(40, 70, 170, 40, ["Sau bữa sáng, 1 viên."], 210, 190, 13)
    b += f'<rect x="520" y="200" width="70" height="100" rx="8" fill="#fff" stroke="#b0c4ce"/>' + text(555, 260, "+", 40, "#e74c3c", weight=800)
    b += label(320, 380, "Nói rõ và hỏi lại để người nghe hiểu đúng", BRAND)
    return svg(SCENES["l2-dieu-duong"][0], b, "#f2f7fa")


@scene("l2-nong-dan", "Nữ nông dân trên ruộng lúa dùng điện thoại xem dự báo thời tiết trước khi làm")
def _():
    b = f'<circle cx="560" cy="70" r="34" fill="#f7c948"/>'
    b += f'<rect x="0" y="230" width="{W}" height="170" fill="#9ccf7a"/>'
    for r in range(5):
        for c in range(14):
            x, y = 20 + c * 46 + (r % 2) * 12, 250 + r * 30
            b += f'<path d="M{x},{y+14} q-3,-12 -8,-16 M{x},{y+14} q2,-12 7,-17 M{x},{y+14} v-18" stroke="#3c8a3c" stroke-width="2.5" fill="none"/>'
    b += person(250, 360, .85, skin=2, hair="long", shirt="#5d8aa8", pants="#34495e", hat="non", pose="side", prop="phone")
    b += f'<rect x="380" y="96" width="200" height="120" rx="14" fill="#fff" stroke="#9fb9b6" stroke-width="1.5"/>'
    b += text(480, 124, "Dự báo hôm nay", 14, BRAND, weight=700)
    b += '<circle cx="430" cy="166" r="18" fill="#f7c948"/><path d="M450,176 q8,-22 30,-12 q20,-6 22,14z" fill="#d6e4ee"/>'
    b += text(530, 162, "Chiều", 13) + text(530, 180, "có mưa", 13)
    b += f'<path d="M380,170 L300,226" stroke="#9fb9b6" stroke-width="1.5" stroke-dasharray="4 4"/>'
    b += label(320, 386, "Nghề nào cũng dùng công nghệ", BRAND)
    return svg(SCENES["l2-nong-dan"][0], b, "#e3f2fb")


@scene("l3-cap-nghe", "Bốn người làm nghề: nữ kỹ sư xây dựng, nam điều dưỡng, nữ phi công, nam giáo viên mầm non")
def _():
    b = ""
    data = [("Kỹ sư xây dựng", dict(skin=1, hair="long", shirt="#e67e22", hat="helmet", pose="hold", prop="blueprint")),
            ("Điều dưỡng", dict(skin=0, hair="short", shirt="#7ec4cf", pants="#7ec4cf", pose="hold", prop="clipboard")),
            ("Phi công", dict(skin=2, hair="bun", shirt="#fff", coat="#203a5a", pants="#203a5a", hat="pilot", pose="wave")),
            ("Giáo viên mầm non", dict(skin=3, hair="curly", shirt="#27ae60", pose="give", prop="blocks"))]
    LBL = {"Kỹ sư xây dựng": ["Kỹ sư", "xây dựng"], "Điều dưỡng": ["Điều dưỡng"], "Phi công": ["Phi công"],
           "Giáo viên mầm non": ["Giáo viên", "mầm non"]}
    for i, (t, kw) in enumerate(data):
        x = 16 + i * 156
        b += f'<rect x="{x}" y="20" width="144" height="360" rx="14" fill="#fff" stroke="#cfdcda" stroke-width="2"/>'
        b += f'<circle cx="{x+72}" cy="190" r="62" fill="{ACCBG}"/>'
        b += person(x + 72, 300, .72, **kw)
        b += lines(x + 72, 334, LBL[t], 14, 18, weight=600)
    return svg(SCENES["l3-cap-nghe"][0], b, "#eef6f5")


@scene("l3-ve-nguoi-lam-nghe", "Hoạt động: em vẽ một người làm nghề, rồi cả nhà cùng xem tranh")
def _():
    b = f'<rect x="0" y="250" width="{W}" height="150" fill="#d9b48a"/>'
    b += f'<rect x="130" y="50" width="380" height="270" rx="6" fill="#fff" stroke="#ccc" stroke-width="2" transform="rotate(-3 320 185)"/>'
    b += text(320, 90, "Hãy vẽ một kỹ sư", 20, BRAND, weight=700)
    b += f'<rect x="200" y="110" width="240" height="180" rx="8" fill="none" stroke="#bbb" stroke-dasharray="8 6" stroke-width="2"/>'
    b += '<path d="M290,250 q30,-90 60,0" stroke="#e67e22" stroke-width="4" fill="none"/><circle cx="320" cy="160" r="20" fill="none" stroke="#e67e22" stroke-width="4"/><path d="M300,140 q20,-22 40,0" stroke="#d98a1c" stroke-width="7" fill="none"/>'
    for i, c in enumerate(["#e74c3c", "#3498db", "#27ae60", "#f1c40f", "#8e44ad"]):
        b += f'<rect x="{60+i*14}" y="300" width="9" height="70" rx="4" fill="{c}" transform="rotate({-10+i*5} {64+i*14} 335)"/>'
    b += f'<path d="M470,330 q40,-30 70,-20 q16,10 0,22 q-30,10 -70,8z" fill="{SKIN[1]}"/><path d="M455,346 l40,-60" stroke="#e74c3c" stroke-width="8" stroke-linecap="round"/>'
    b += bubble(470, 140, 150, 60, ["Kỹ sư của em", "là ai, làm gì?"], 440, 200, 13)
    return svg(SCENES["l3-ve-nguoi-lam-nghe"][0], b, "#f6efe4")


@scene("l3-doi-cau-hoi", "Đổi câu hỏi: thay vì hỏi nghề này dành cho con trai hay con gái, hãy hỏi nghề này cần kỹ năng gì")
def _():
    b = bubble(40, 60, 250, 90, ["Nghề này chỉ dành", "cho con trai?"], 120, 230, 18, "#fdecea", "#e6a29b")
    b += '<path d="M60,82 L270,130" stroke="#b3261e" stroke-width="5" stroke-linecap="round"/>'
    b += bubble(350, 60, 250, 90, ["Nghề này cần", "kỹ năng gì?"], 520, 230, 18, "#e8f5e9", "#8cc79a")
    b += f'<path d="M296,105 h44" stroke="{BRAND}" stroke-width="6" marker-end="url(#a)"/>'
    b = ('<defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10z" fill="{BRAND}"/></marker></defs>') + b
    b += person(130, 380, .62, skin=1, hair="short", shirt="#27ae60", pose="down")
    b += person(510, 380, .62, skin=2, hair="pony", shirt="#8e44ad", pose="wave")
    b += lines(320, 230, ["Câu hỏi mới mở ra", "nhiều nghề hơn cho", "mọi bạn nhỏ"], 16, 22, fill=BRAND, weight=600)
    return svg(SCENES["l3-doi-cau-hoi"][0], b, "#fbfaf7")


@scene("l4-nhom-poster", "Bốn bạn cùng làm một tấm áp phích, mỗi bạn một vai: vẽ, viết chữ, giữ giờ, kiểm tra")
def _():
    b = f'<rect x="120" y="230" width="400" height="18" rx="6" fill="#b98a5a"/>'
    b += f'<rect x="200" y="160" width="240" height="76" rx="4" fill="#fff" stroke="#ccc"/>' + text(320, 196, "NGHỀ QUANH EM", 18, BRAND, weight=800)
    b += '<circle cx="240" cy="222" r="8" fill="#e74c3c"/><circle cx="270" cy="222" r="8" fill="#3498db"/><circle cx="400" cy="222" r="8" fill="#27ae60"/>'
    kids = [(80, "Vẽ", dict(skin=1, hair="pony", shirt="#e74c3c", pose="side", prop="brush")),
            (230, "Viết chữ", dict(skin=0, hair="short", shirt="#3498db", pose="write", prop="notebook")),
            (410, "Giữ giờ", dict(skin=2, hair="curly", shirt="#27ae60", pose="hold", prop="phone")),
            (560, "Kiểm tra", dict(skin=3, hair="bun", shirt="#8e44ad", pose="point", prop="", flip=True))]
    for x, r, kw in kids:
        b += person(x, 372, .55, **kw)
        b += label(x, 392, r, ACC)
    b += bubble(470, 30, 150, 44, ["Còn 10 phút nữa!"], 420, 250, 13)
    b += bubble(30, 30, 160, 44, ["Mình vẽ phần hình."], 80, 250, 13)
    return svg(SCENES["l4-nhom-poster"][0], b, "#fff7e6")


@scene("l4-doi-xay-dung", "Đội thợ xây chuyền gạch cho nhau: mỗi người một phần, cùng một mục tiêu")
def _():
    b = ground(330, "#d8cfc0")
    for r in range(6):
        for c in range(5 - (r % 2)):
            b += f'<rect x="{470 + c*30 + (r%2)*15}" y="{300 - r*16}" width="28" height="14" fill="#c0563b" stroke="#8e3b27"/>'
    b += f'<rect x="30" y="290" width="80" height="40" fill="#c0563b" stroke="#8e3b27"/>'
    b += person(120, 340, .62, skin=2, hair="short", shirt="#e67e22", hat="helmet", pose="give", prop="brick")
    b += person(250, 340, .62, skin=1, hair="pony", shirt="#2980b9", hat="helmet", pose="give", prop="brick")
    b += person(380, 340, .62, skin=3, hair="short", hc=1, shirt="#16a085", hat="helmet", pose="give", prop="brick")
    b += f'<path d="M150,250 h300" stroke="{BRAND}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#b)"/>'
    b = ('<defs><marker id="b" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10z" fill="{BRAND}"/></marker></defs>') + b
    b += label(320, 60, "Mỗi người một phần, cùng một mục tiêu", BRAND, size=16)
    b += bubble(380, 100, 140, 40, ["Nhận lấy nhé!"], 400, 196, 13)
    return svg(SCENES["l4-doi-xay-dung"][0], b, "#e8f3fb")


@scene("l4-bang-nhiem-vu", "Bảng nhiệm vụ nhóm có ba cột: Ai, Làm gì, Xong khi nào")
def _():
    b = f'<rect x="50" y="30" width="540" height="330" rx="12" fill="#fff" stroke="#9aa" stroke-width="6"/>'
    b += text(320, 72, "BẢNG NHIỆM VỤ NHÓM", 22, BRAND, weight=800)
    cols = [(70, "Ai"), (200, "Làm gì"), (420, "Xong khi nào")]
    b += f'<rect x="70" y="90" width="500" height="36" rx="6" fill="{BRAND}"/>'
    for x, t in cols:
        b += text(x + 14, 114, t, 16, "#fff", "start", 700)
    rows = [("Lan", "Vẽ 3 hình nghề", "Thứ Ba", "#ffe08a"), ("Huy", "Viết tên các nghề", "Thứ Ba", "#bfe3ff"),
            ("Mai", "Dán hình lên giấy", "Thứ Tư", "#c8f0c4"), ("Cả nhóm", "Xem lại cùng nhau", "Thứ Tư", "#f5d0f0")]
    for i, (a, w, d, c) in enumerate(rows):
        y = 136 + i * 52
        b += f'<rect x="70" y="{y}" width="500" height="44" rx="6" fill="{c}" opacity=".55"/>'
        b += text(84, y + 28, a, 16, INK, "start", 700) + text(214, y + 28, w, 16, INK, "start") + text(434, y + 28, d, 16, INK, "start")
        b += f'<rect x="540" y="{y+12}" width="20" height="20" rx="4" fill="#fff" stroke="{BRAND}" stroke-width="2"/>'
        if i < 2:
            b += f'<path d="M544,{y+22} l5,6 l9,-12" stroke="{BRAND}" stroke-width="3" fill="none"/>'
    b += f'<rect x="270" y="360" width="100" height="14" rx="4" fill="#9aa"/>'
    return svg(SCENES["l4-bang-nhiem-vu"][0], b, "#eef6f5")


@scene("l5-nhac-lai", "Cô giáo giao việc, bạn học sinh nhắc lại việc và hạn để chắc mình hiểu đúng")
def _():
    b = f'<rect x="20" y="40" width="250" height="150" rx="6" fill="#2e4d3f"/>' + lines(145, 100, ["Bài tả con vật", "Nộp: thứ Sáu"], 18, 30, fill="#fff")
    b += ground(330, "#e9dcc9")
    b += person(170, 345, .78, skin=1, hair="long", shirt="#c0392b", pose="give", prop="")
    b += person(470, 360, .58, skin=2, hair="short", shirt="#2980b9", pose="hold", prop="notebook", flip=True)
    b += bubble(290, 40, 300, 56, ["Em viết bài tả con vật,", "nộp vào thứ Sáu nhé."], 210, 170, 14)
    b += bubble(330, 130, 290, 56, ["Dạ, em viết bài tả con vật,", "nộp thứ Sáu ạ."], 470, 230, 14, "#e8f5e9", "#8cc79a")
    b += label(320, 386, "Nghe hết → nhắc lại → ghi hạn", BRAND)
    return svg(SCENES["l5-nhac-lai"][0], b, "#fbfaf7")


@scene("l5-lich-hen", "Lịch tuần có hạn nộp thứ Sáu và một mốc kiểm tra giữa chừng vào thứ Tư")
def _():
    days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
    b = f'<rect x="30" y="40" width="580" height="250" rx="14" fill="#fff" stroke="#cfdcda" stroke-width="2"/>'
    b += f'<rect x="30" y="40" width="580" height="46" rx="14" fill="{BRAND}"/><rect x="30" y="70" width="580" height="16" fill="{BRAND}"/>'
    b += text(320, 70, "Tuần này của em", 18, "#fff", weight=700)
    for i, d in enumerate(days):
        x = 44 + i * 80
        b += text(x + 34, 112, d, 15, BRAND, weight=700)
        b += f'<rect x="{x}" y="122" width="70" height="150" rx="8" fill="#f6f4ef"/>'
    b += f'<rect x="48" y="140" width="62" height="56" rx="4" fill="#bfe3ff" transform="rotate(-3 79 168)"/>' + lines(79, 162, ["Nhận", "việc"], 13)
    b += f'<rect x="208" y="140" width="62" height="70" rx="4" fill="#ffe08a" transform="rotate(2 239 175)"/>' + lines(239, 160, ["Xem", "giữa", "chừng"], 13)
    b += f'<rect x="368" y="140" width="62" height="56" rx="4" fill="#ffb3a7" transform="rotate(-2 399 168)"/>' + lines(399, 162, ["Nộp", "bài"], 13, weight=700)
    b += f'<circle cx="399" cy="230" r="20" fill="none" stroke="#b3261e" stroke-width="3"/>' + text(399, 236, "!", 18, "#b3261e", weight=800)
    b += f'<circle cx="120" cy="340" r="36" fill="#fff" stroke="{BRAND}" stroke-width="4"/><path d="M120,340 v-22 M120,340 h16" stroke="{BRAND}" stroke-width="4" stroke-linecap="round"/>'
    b += lines(370, 330, ["Ghi hạn vào lịch.", "Đặt một ngày xem giữa chừng."], 16, 24, weight=600)
    return svg(SCENES["l5-lich-hen"][0], b, "#eef6f5")


@scene("l5-bao-som", "Bạn học sinh báo sớm với cô rằng phần việc có thể chậm và nói cần gì để kịp")
def _():
    b = ground(330, "#e9dcc9")
    b += person(160, 345, .58, skin=0, hair="pony", shirt="#16a085", pose="hold", prop="card")
    b += person(460, 345, .78, skin=2, hair="bun", hc=1, shirt="#34495e", coat="#7f8c8d", pose="side", prop="", flip=True)
    b += bubble(20, 40, 300, 76, ["Thưa cô, phần của em có thể", "chậm một ngày. Em cần thêm", "giấy màu ạ."], 160, 210, 14)
    b += bubble(340, 60, 280, 56, ["Cảm ơn em báo sớm. Cô có", "giấy màu, em lấy nhé."], 450, 170, 14, "#e8f5e9", "#8cc79a")
    b += label(320, 386, "Báo sớm khi chưa trễ, nói rõ cần gì", BRAND)
    return svg(SCENES["l5-bao-som"][0], b, "#fff7e6")


@scene("l6-phong-van", "Bạn nhỏ cầm sổ phỏng vấn cô thợ làm bánh, có mẹ ngồi cạnh")
def _():
    b = f'<rect x="0" y="0" width="{W}" height="260" rx="18" fill="#f6e3c8"/>' + ground(300, "#e9dcc9")
    b += f'<rect x="420" y="120" width="200" height="16" fill="#a0522d"/>'
    for i in range(4):
        b += f'<path d="M{432+i*44},118 q18,-22 36,0z" fill="#e0a85b" stroke="#b07a35"/>'
    b += person(490, 340, .74, skin=1, hair="bun", shirt="#fff", apron="#e67e22", pose="side", prop="bread", flip=True)
    b += person(250, 360, .52, skin=2, hair="short", shirt="#27ae60", pose="write", prop="notebook")
    b += person(110, 350, .7, skin=0, hair="long", shirt="#8e44ad", pose="down")
    b += bubble(150, 40, 230, 56, ["Cô thích điều gì nhất", "trong công việc ạ?"], 250, 196, 14)
    b += bubble(420, 20, 200, 56, ["Cô thích thấy khách", "ăn ngon miệng."], 480, 150, 14, "#e8f5e9", "#8cc79a")
    b += label(110, 386, "Người lớn đi cùng", ACC)
    return svg(SCENES["l6-phong-van"][0], b, "#fbfaf7")


@scene("l6-phieu-phong-van", "Phiếu phỏng vấn người làm nghề với năm câu hỏi")
def _():
    b = f'<rect x="150" y="20" width="340" height="364" rx="16" fill="#b07a45"/><rect x="170" y="44" width="300" height="326" rx="6" fill="#fff"/>'
    b += f'<rect x="270" y="10" width="100" height="30" rx="8" fill="#7f8c8d"/>'
    b += text(320, 76, "PHIẾU PHỎNG VẤN", 18, BRAND, weight=800)
    qs = ["1. Cô/chú làm nghề gì?", "2. Một ngày làm những việc gì?", "3. Dùng những đồ dùng gì?",
          "4. Cần những kỹ năng gì?", "5. Điều gì khó, điều gì vui?"]
    for i, q in enumerate(qs):
        y = 108 + i * 52
        b += text(184, y, q, 14, INK, "start", 600)
        b += f'<path d="M184,{y+16} h272 M184,{y+30} h272" stroke="#cfd8dc" stroke-width="1.5"/>'
    b += person(70, 380, .55, skin=3, hair="curly", shirt="#e67e22", pose="point", prop="")
    b += person(570, 380, .55, skin=1, hair="pony", shirt="#3498db", pose="hold", prop="notebook", flip=True)
    return svg(SCENES["l6-phieu-phong-van"][0], b, "#eef6f5")


@scene("l6-ke-ve-nghe", "Bạn nhỏ kể cho cả lớp về nghề mình đã phỏng vấn, dùng Thẻ nghề")
def _():
    b = f'<rect x="300" y="30" width="300" height="200" rx="8" fill="#fff" stroke="{BRAND}" stroke-width="3"/>'
    b += f'<rect x="300" y="30" width="300" height="34" rx="8" fill="{BRAND}"/>' + text(450, 54, "THẺ NGHỀ: Thợ làm bánh", 15, "#fff", weight=700)
    for i, t in enumerate(["Làm gì: nướng bánh mỗi sáng", "Ở đâu: tiệm bánh", "Dùng gì: lò, cân, khuôn", "Kỹ năng: đo chính xác, giữ giờ"]):
        b += text(316, 92 + i * 34, t, 14, INK, "start")
    b += person(220, 330, .7, skin=2, hair="short", shirt="#27ae60", pose="point", prop="")
    b += ground(330, "#e9dcc9")
    for i, (sk, h, c) in enumerate([(0, "pony", "#e74c3c"), (3, "short", "#3498db"), (1, "bun", "#f1c40f"), (2, "curly", "#8e44ad")]):
        b += person(360 + i * 70, 398, .4, skin=sk, hair=h, shirt=c, pose="down")
    b += bubble(20, 60, 200, 56, ["Cô làm bánh dậy lúc", "4 giờ sáng đó các bạn!"], 200, 180, 13)
    return svg(SCENES["l6-ke-ve-nghe"][0], b, "#fff7e6")


@scene("l7-tuong-the-nghe", "Tường trưng bày Thẻ nghề của cả nhà trong Ngày hội nghề nghiệp")
def _():
    b = f'<path d="M20,60 Q320,110 620,60" stroke="#8d6e63" stroke-width="3" fill="none"/>'
    names = [("Thợ điện", "#e67e22"), ("Điều dưỡng", "#7ec4cf"), ("Nông dân", "#5d8aa8"),
             ("Thợ làm bánh", "#e0a85b"), ("Tài xế", BRAND2), ("Kỹ sư", "#8e44ad")]
    for i, (n, c) in enumerate(names):
        x = 34 + i * 100
        y = 72 + int(28 * (1 - ((x + 40 - 320) / 300) ** 2))
        b += f'<rect x="{x+34}" y="{y-10}" width="12" height="20" rx="2" fill="#c69c6d"/>'
        b += f'<rect x="{x}" y="{y}" width="84" height="110" rx="6" fill="#fff" stroke="{c}" stroke-width="3" transform="rotate({(-1)**i*3} {x+42} {y+55})"/>'
        b += f'<circle cx="{x+42}" cy="{y+40}" r="20" fill="{c}" opacity=".85"/>' + text(x + 42, y + 86, n, 12, INK, weight=600)
    b += ground(330, "#e9dcc9")
    b += person(140, 380, .55, skin=1, hair="long", shirt="#c0392b", pose="point")
    b += person(260, 380, .4, skin=1, hair="short", shirt="#27ae60", pose="wave")
    b += person(470, 380, .62, skin=2, hair="short", hc=2, shirt="#34495e", pose="down")
    b += person(540, 380, .4, skin=2, hair="pony", shirt="#f1c40f", pose="both_up")
    b += label(320, 250, "Ngày hội nghề nghiệp của nhà mình", BRAND, size=16)
    return svg(SCENES["l7-tuong-the-nghe"][0], b, "#fbfaf7")


@scene("l7-dong-vai", "Trẻ đóng vai tiệm bánh: một bạn làm bánh, một bạn bán hàng, một bạn là khách")
def _():
    b = shop(170, 130, 300, 190, "Tiệm bánh nhà em", "#f6e3c8")
    b += ground(320, "#e9dcc9") + table(230, 270, 180, "#a0522d")
    b += person(250, 320, .55, skin=0, hair="short", shirt="#fff", hat="chef", apron="#dfe6e9", pose="hold", prop="tray")
    b += person(390, 320, .55, skin=3, hair="pony", shirt="#e67e22", pose="give", prop="bread", flip=True)
    b += person(560, 380, .55, skin=1, hair="curly", shirt="#3498db", pose="side", prop="", flip=True)
    b += bubble(470, 40, 160, 56, ["Cho con 2 bánh", "mì nhé!"], 556, 250, 13)
    b += bubble(250, 14, 170, 56, ["Dạ, 2 bánh mì.", "Đợi con chút ạ."], 392, 205, 13, "#e8f5e9", "#8cc79a")
    b += label(320, 386, "Đóng vai: nghe, nhắc lại, phối hợp", BRAND)
    return svg(SCENES["l7-dong-vai"][0], b, "#fff7e6")


@scene("l7-huy-hieu", "Sáu huy hiệu của khóa: Nhà thám hiểm nghề, Thám tử kỹ năng, Người phá định kiến, Đồng đội tốt, Người giữ hẹn, Phóng viên nhí")
def _():
    badges = [("1", "Nhà thám hiểm", "nghề", "#e67e22"), ("2", "Thám tử", "kỹ năng", "#2980b9"),
              ("3", "Người phá", "định kiến", "#8e44ad"), ("4", "Đồng đội", "tốt", "#27ae60"),
              ("5", "Người", "giữ hẹn", "#c0392b"), ("6", "Phóng viên", "nhí", BRAND2)]
    b = text(320, 44, "Huy hiệu khóa Khám phá nghề", 20, BRAND, weight=800)
    for i, (n, a, c2, col) in enumerate(badges):
        cx, cy = 120 + (i % 3) * 200, 140 + (i // 3) * 160
        b += f'<path d="M{cx-22},{cy+40} l-10,48 l22,-12 l10,16 l10,-50z M{cx+22},{cy+40} l10,48 l-22,-12 l-10,16 l-10,-50z" fill="{col}" opacity=".7"/>'
        b += f'<circle cx="{cx}" cy="{cy}" r="56" fill="{col}"/><circle cx="{cx}" cy="{cy}" r="46" fill="#fff"/>'
        b += text(cx, cy - 14, n, 22, col, weight=800) + text(cx, cy + 6, a, 12, INK, weight=700) + text(cx, cy + 22, c2, 12, INK, weight=700)
    return svg(SCENES["l7-huy-hieu"][0], b, "#fdf3e2")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (title, fn) in SCENES.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print(f"Đã vẽ {len(SCENES)} hình vào {OUT}")
