#!/usr/bin/env python3
"""Hình minh họa tự vẽ (SVG) cho 12 bài lấp ô trống K × bậc (ngoài khóa). Không dùng ảnh ngoài.
Chạy: python3 _build/art/bs_art.py  -> _build/static/assets/img/bs/*.svg
Mọi tên người, nơi làm việc, số liệu trong hình là giả định.
Tiêu đề (aria-label) lấy từ alt của ảnh trong bài học.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n2_art import (svg, text, lines, box, BRAND, BRAND2, ACC, ACCBG, INK, MUTED,  # noqa: E402
                    RED, REDBG, GREEN, GREENBG, BLUE, BLUEBG)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_build/static/assets/img/bs"
SCENES = {}
WARM = ("k10-tin-nhan-gia-sep", "k4-cham-y-tuong", "k9-ba-vai")


def alt_of(name):
    for f in (ROOT / "content/bai-hoc").glob("*.md"):
        m = re.search(rf'img/bs/{name}\.svg" alt="([^"]+)"', f.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    raise SystemExit(f"Không tìm thấy alt cho {name}")


def scene(name):
    def deco(fn):
        SCENES[name] = fn
        return fn
    return deco


def arrow(x1, y1, x2, y2, col=BRAND2, sw=2.5):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}"/>'
            f'<circle cx="{x2}" cy="{y2}" r="4.5" fill="{col}"/>')


def person(x, y, shirt=BRAND2, s=1.0):
    """Người đơn giản: đầu tròn, thân bo góc. (x, y) là đỉnh đầu."""
    r = 16 * s
    return (f'<circle cx="{x}" cy="{y + r}" r="{r}" fill="#f1c9a5" stroke="{INK}" stroke-width="1.2"/>'
            f'<rect x="{x - 24 * s}" y="{y + 2 * r + 4}" width="{48 * s}" height="{58 * s}" rx="{14 * s}" fill="{shirt}"/>')


def bubble(x, y, w, h, rows, col=BRAND, size=12.5):
    b = box(x, y, w, h, "#fff", col, 12, 1.8)
    b += f'<path d="M{x + 26},{y + h} l10,14 l8,-14 z" fill="#fff" stroke="{col}" stroke-width="1.8"/>'
    b += f'<rect x="{x + 24}" y="{y + h - 3}" width="24" height="6" fill="#fff"/>'
    return b + lines(x + w / 2, y + 22, rows, size, 17, fill=INK, weight=600)


def tick(x, y, col=GREEN):
    return (f'<circle cx="{x}" cy="{y}" r="15" fill="{col}"/>'
            f'<path d="M{x - 7},{y} l5,6 l10,-12" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>')


def cross(x, y, col=RED):
    return (f'<circle cx="{x}" cy="{y}" r="15" fill="{col}"/>'
            f'<path d="M{x - 6},{y - 6} l12,12 M{x + 6},{y - 6} l-12,12" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>')


# 1. K1 B1
@scene("k1-nghe-het")
def _():
    b = text(320, 30, "Nghe hết, rồi nhắc lại theo thứ tự", 19, BRAND, weight=800)
    for i, (head, col) in enumerate((("1. Anh chủ dặn", BRAND), ("2. Dừng tay, nghe hết", ACC), ("3. Nhắc lại", GREEN))):
        x = 16 + i * 208
        b += box(x, 48, 196, 330, "#fff", col, 14, 2)
        b += text(x + 98, 74, head, 14.5, col, weight=800)
        b += f'<line x1="{x + 10}" y1="330" x2="{x + 186}" y2="330" stroke="#c9d6d4" stroke-width="2"/>'
    # khung 1
    b += bubble(28, 88, 172, 92, ["Hết khách thì", "tắt lò, đậy khay", "pa-tê, rồi lau quầy."])
    b += person(80, 200, BRAND) + person(150, 214, BRAND2, .85)
    # khung 2
    b += person(330, 196, BRAND2)
    b += f'<rect x="236" y="300" width="70" height="22" rx="10" fill="{ACC}"/>' + text(271, 316, "ổ bánh", 11, "#fff", weight=700)
    b += lines(330, 110, ["Đặt đồ xuống,", "quay sang", "người nói"], 13, 19, fill=INK, weight=700)
    b += f'<path d="M300,170 q30,-22 60,0" fill="none" stroke="{ACC}" stroke-width="2.5"/>'
    # khung 3
    b += bubble(440, 88, 172, 92, ["Dạ, em tắt lò,", "đậy khay pa-tê,", "rồi lau quầy."], GREEN)
    b += person(500, 200, BRAND2)
    for k in range(3):
        b += f'<circle cx="{560 + k * 18}" cy="{246}" r="8" fill="{GREEN}"/>' + text(560 + k * 18, 250, str(k + 1), 10, "#fff", weight=800)
    b += text(526, 356, "Đúng thứ tự", 13, GREEN, weight=800)
    b += text(110, 356, "Có điều kiện: hết khách", 12, MUTED, weight=700)
    b += text(318, 356, "Không chen lời", 13, ACC, weight=800)
    return b


# 2. K3 B1
@scene("k3-khi-bi-vuong")
def _():
    b = text(320, 30, "Khi bị vướng: hỏi ngay hay tự thử?", 19, BRAND, weight=800)
    b += box(200, 48, 240, 44, BRAND, BRAND, 22) + text(320, 76, "Mình đang bị vướng", 15, "#fff", weight=800)
    b += arrow(320, 92, 320, 118)
    b += f'<polygon points="300,122 440,170 300,218 160,170" fill="{ACCBG}" stroke="{ACC}" stroke-width="2"/>'
    b += lines(300, 162, ["An toàn, tiền của khách,", "máy móc lạ?"], 13, 18, fill=INK, weight=700)
    b += text(448, 162, "Có", 13, RED, "start", 800) + arrow(440, 170, 482, 170, RED)
    b += box(486, 136, 140, 68, REDBG, RED, 12, 2) + lines(556, 164, ["HỎI NGAY", "người phụ trách"], 13, 18, fill=RED, weight=800)
    b += text(310, 238, "Không", 13, GREEN, "start", 800) + arrow(300, 218, 300, 250, GREEN)
    b += box(170, 252, 260, 44, "#fff", GREEN, 12, 2) + text(300, 279, "Tự thử vài phút với hướng dẫn có sẵn", 12.5, INK, weight=700)
    b += arrow(250, 296, 150, 326, GREEN) + arrow(390, 296, 490, 326, ACC)
    b += box(30, 328, 230, 54, GREENBG, GREEN, 12, 2) + lines(145, 350, ["Được: làm tiếp,", "ghi lại cách làm"], 13, 17, fill=GREEN, weight=800)
    b += box(372, 328, 254, 54, ACCBG, ACC, 12, 2) + lines(499, 350, ["Chưa được: nói chỗ vướng 1 câu,", "nhờ đúng người, đúng lúc"], 12.5, 17, fill=INK, weight=800)
    return b


# 3. K6 B1
def gift(x, y, ok):
    col = GREEN if ok else RED
    b = f'<rect x="{x}" y="{y}" width="150" height="110" rx="8" fill="{GREENBG if ok else REDBG}" stroke="{col}" stroke-width="2"/>'
    if not ok:
        for k in range(4):
            b += f'<path d="M{x + 12 + k * 34},{y + 10} q8,30 -4,60 q-8,20 6,36" fill="none" stroke="{col}" stroke-opacity=".55" stroke-width="2"/>'
    b += f'<rect x="{x + 66}" y="{y}" width="18" height="110" fill="{ACC}"/><rect x="{x}" y="{y + 46}" width="150" height="18" fill="{ACC}"/>'
    return b


@scene("k6-doi-mot-diem")
def _():
    b = text(320, 30, "Thử lại, đổi đúng một điểm", 19, BRAND, weight=800)
    b += box(24, 52, 276, 300, "#fff", RED, 14, 2) + text(162, 80, "Lần 1", 16, RED, weight=800)
    b += box(340, 52, 276, 300, "#fff", GREEN, 14, 2) + text(478, 80, "Lần 2", 16, GREEN, weight=800)
    b += gift(87, 120, False) + cross(258, 110)
    b += gift(403, 120, True) + tick(574, 110)
    b += lines(162, 268, ["Giấy vừa khít mép hộp", "→ giấy bị nhăn, hở góc"], 13, 20, fill=INK, weight=600)
    b += f'<line x1="395" y1="250" x2="561" y2="250" stroke="{BRAND2}" stroke-width="2" stroke-dasharray="4 3"/>'
    b += text(478, 244, "+3 cm mỗi mép", 12, BRAND2, weight=800)
    b += lines(478, 278, ["Chỉ đổi khổ giấy", "→ gói phẳng"], 13, 20, fill=INK, weight=600)
    b += arrow(300, 200, 336, 200, ACC, 3)
    b += text(320, 382, "Đổi nhiều thứ cùng lúc thì không biết điều gì đã giúp.", 13, INK, weight=700)
    return b


# 4. K4 B1
@scene("k4-chia-o-ban-do")
def _():
    b = text(320, 30, "Phát tờ rơi: hai cách làm (giả định)", 19, BRAND, weight=800)
    cols = (BRAND2, ACC, BLUE, RED)

    def grid(x0):
        g = f'<rect x="{x0}" y="70" width="270" height="250" rx="10" fill="#fff" stroke="#9fb9b6" stroke-width="1.5"/>'
        for k in range(1, 5):
            g += f'<line x1="{x0 + k * 54}" y1="70" x2="{x0 + k * 54}" y2="320" stroke="#e1eae8" stroke-width="6"/>'
            g += f'<line x1="{x0}" y1="{70 + k * 50}" x2="{x0 + 270}" y2="{70 + k * 50}" stroke="#e1eae8" stroke-width="6"/>'
        return g
    b += grid(26) + text(161, 60, "Mỗi người tự đi", 14, RED, weight=800)
    paths = ("M40,90 L120,90 L120,190 L230,190", "M60,300 L60,140 L180,140 L180,90",
             "M280,300 L170,300 L170,190 L90,190", "M250,90 L250,250 L120,250")
    for p, c in zip(paths, cols):
        b += f'<path d="{p}" fill="none" stroke="{c}" stroke-width="4" stroke-opacity=".8" stroke-linecap="round"/>'
    for cx, cy in ((120, 190), (170, 190), (180, 140)):
        b += f'<circle cx="{cx}" cy="{cy}" r="11" fill="none" stroke="{RED}" stroke-width="2.5"/>'
    b += text(161, 344, "Phát trùng ở giữa, sót ở góc", 13, RED, weight=700)
    x0 = 344
    b += grid(x0) + text(479, 60, "Chia 4 ô, mỗi người một ô", 14, GREEN, weight=800)
    for k, c in enumerate(cols):
        ox, oy = x0 + (k % 2) * 135, 70 + (k // 2) * 125
        b += f'<rect x="{ox + 4}" y="{oy + 4}" width="127" height="117" rx="8" fill="{c}" fill-opacity=".16" stroke="{c}" stroke-width="2"/>'
        b += text(ox + 67, oy + 68, f"Bạn {k + 1}", 14, c, weight=800)
    b += text(479, 344, "Không trùng, không sót", 13, GREEN, weight=700)
    b += text(320, 382, "Câu hỏi bắt đầu: “Còn cách nào khác không?”", 13.5, INK, weight=800)
    return b


# 5. K9 B1
@scene("k9-ba-vai")
def _():
    b = text(320, 32, "Ba vai nhỏ trong nhóm", 20, BRAND, weight=800)
    data = (("Người giữ giờ", BRAND2, ["Báo khi còn 5 phút", "Nhắc chuyển việc", "Giữ buổi họp đúng giờ"]),
            ("Người ghi chép", ACC, ["Ai làm gì", "Hạn khi nào", "Gửi lại nhóm sau buổi"]),
            ("Người nhắc việc", BLUE, ["Một ngày trước hạn", "Hỏi tiến độ từng phần", "Hỏi có cần hỗ trợ"]))
    for i, (name, col, rows) in enumerate(data):
        x = 22 + i * 204
        b += box(x, 54, 188, 312, "#fff", col, 16, 2.5)
        cx, cy = x + 94, 130
        b += f'<circle cx="{cx}" cy="{cy}" r="44" fill="{col}" fill-opacity=".15"/>'
        if i == 0:
            b += f'<circle cx="{cx}" cy="{cy}" r="28" fill="#fff" stroke="{col}" stroke-width="4"/>'
            b += f'<path d="M{cx},{cy} L{cx},{cy - 18} M{cx},{cy} L{cx + 13},{cy + 6}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        elif i == 1:
            b += f'<rect x="{cx - 24}" y="{cy - 30}" width="48" height="60" rx="5" fill="#fff" stroke="{col}" stroke-width="3.5"/>'
            for k in range(4):
                b += f'<line x1="{cx - 14}" y1="{cy - 16 + k * 11}" x2="{cx + 14}" y2="{cy - 16 + k * 11}" stroke="{MUTED}" stroke-width="2.5"/>'
        else:
            b += f'<path d="M{cx - 22},{cy + 16} q4,-4 4,-20 q0,-22 18,-22 q18,0 18,22 q0,16 4,20 z" fill="#fff" stroke="{col}" stroke-width="3.5"/>'
            b += f'<circle cx="{cx}" cy="{cy + 24}" r="5" fill="{col}"/>'
        b += text(cx, 206, name, 15.5, col, weight=800)
        for k, r in enumerate(rows):
            b += f'<circle cx="{x + 22}" cy="{246 + k * 36}" r="4" fill="{col}"/>' + text(x + 34, 251 + k * 36, r, 13, INK, "start", 600)
    b += text(320, 388, "Nhận vai thì nói rõ: “Hôm nay mình giữ giờ nhé.”", 13, INK, weight=700)
    return b


# 6. K10 B1
def door(x, y, label, col):
    return (f'<rect x="{x}" y="{y}" width="58" height="84" rx="6" fill="#fff" stroke="{col}" stroke-width="2.2"/>'
            f'<circle cx="{x + 46}" cy="{y + 44}" r="3.5" fill="{col}"/>' + text(x + 29, y + 102, label, 11, INK, weight=700))


def key(x, y, col):
    return (f'<circle cx="{x}" cy="{y}" r="9" fill="none" stroke="{col}" stroke-width="3.5"/>'
            f'<path d="M{x + 9},{y} h26 m-8,0 v8 m-8,-8 v6" stroke="{col}" stroke-width="3.5" fill="none" stroke-linecap="round"/>')


@scene("k10-mot-chia-khoa")
def _():
    b = text(320, 30, "Một chìa cho mọi cửa, hay mỗi cửa một chìa?", 18.5, BRAND, weight=800)
    labels = ("Email", "Ngân hàng", "Mạng XH", "Bán hàng")
    b += box(16, 48, 296, 312, REDBG, RED, 14, 2) + text(164, 76, "Dùng chung một mật khẩu", 14.5, RED, weight=800)
    for k, lb in enumerate(labels):
        b += door(30 + k * 70, 196, lb, RED)
        b += f'<path d="M164,148 L{59 + k * 70},194" stroke="{RED}" stroke-width="1.6" stroke-dasharray="4 3"/>'
    b += key(146, 128, RED)
    b += lines(164, 330, ["Lộ một chỗ → kẻ xấu thử", "ở mọi tài khoản → mất cả bốn"], 12.5, 17, fill=RED, weight=700)
    b += box(328, 48, 296, 312, GREENBG, GREEN, 14, 2) + text(476, 76, "Mỗi nơi một mật khẩu + 2 lớp", 14.5, GREEN, weight=800)
    kc = (BRAND2, ACC, BLUE, GREEN)
    for k, lb in enumerate(labels):
        b += door(342 + k * 70, 196, lb, GREEN)
        b += key(356 + k * 70, 166, kc[k])
    b += f'<rect x="456" y="96" width="40" height="58" rx="7" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    b += text(476, 122, "Mã", 10.5, INK, weight=700) + text(476, 140, "xác thực", 9, INK, weight=600)
    b += lines(476, 330, ["Lộ một chìa → ba cửa còn lại", "vẫn an toàn"], 12.5, 17, fill=GREEN, weight=700)
    b += text(320, 388, "Không đưa mật khẩu hay mã OTP cho bất kỳ ai.", 13, INK, weight=800)
    return b


# 7. K10 B2
@scene("k10-tin-nhan-gia-sep")
def _():
    b = text(320, 30, "Ba dấu hiệu trong một tin nhắn (giả định)", 18.5, BRAND, weight=800)
    b += f'<rect x="40" y="46" width="250" height="342" rx="26" fill="{INK}"/>'
    b += f'<rect x="52" y="62" width="226" height="310" rx="14" fill="#fff"/>'
    b += f'<circle cx="80" cy="88" r="15" fill="{BRAND2}"/>' + text(102, 86, "Giám đốc (tài khoản mới)", 11.5, INK, "start", 800)
    b += text(102, 101, "vừa xong", 10, MUTED, "start")
    msg = [("Phúc chuyển gấp 45 triệu", 1), ("cho đối tác theo số TK này.", 1),
           ("Anh đang họp, không nghe", 3), ("máy được.", 3), ("Xong trước 11 giờ nhé.", 2)]
    b += f'<rect x="64" y="118" width="202" height="122" rx="12" fill="#eef2f1"/>'
    for k, (r, _n) in enumerate(msg):
        b += text(76, 140 + k * 22, r, 12.5, INK, "start", 600)
    marks = ((1, 151, "Đòi chuyển tiền"), (2, 228, "Gấp gáp"), (3, 195, "Chặn gọi xác nhận"))
    for n, y, lb in marks:
        b += f'<line x1="266" y1="{y - 4}" x2="318" y2="{y - 4}" stroke="{RED}" stroke-width="2"/>'
        b += f'<circle cx="330" cy="{y - 4}" r="12" fill="{RED}"/>' + text(330, y + 1, str(n), 12, "#fff", weight=800)
        b += text(350, y + 1, lb, 13.5, RED, "start", 800)
    b += box(338, 262, 286, 118, "#fff", GREEN, 14, 2)
    b += text(481, 286, "Phúc làm 3 bước", 14, GREEN, weight=800)
    for k, s in enumerate(("1. Dừng: không chuyển, không trả lời", "2. Gọi số giám đốc đã lưu sẵn", "3. Báo kế toán trưởng, cảnh báo nhóm")):
        b += text(354, 314 + k * 24, s, 12.5, INK, "start", 600)
    b += f'<rect x="64" y="252" width="202" height="30" rx="15" fill="#fff" stroke="#c9d6d4"/>' + text(165, 272, "Nhập tin nhắn…", 11, MUTED)
    return b


# 8. K6 B2
@scene("k6-cu-va-moi")
def _():
    b = text(320, 30, "Cách cũ và cách mới: tìm điểm khác", 19, BRAND, weight=800)
    old = ("Nhận hàng", "Kiểm số lượng", "Ghi sổ tay", "Xếp lên kệ")
    new = ("Nhận hàng", "Kiểm số lượng", "Quét mã bằng điện thoại", "Xếp lên kệ")
    b += text(160, 66, "Cách cũ", 15, MUTED, weight=800) + text(480, 66, "Cách mới", 15, BRAND, weight=800)
    for k in range(4):
        y = 82 + k * 70
        ch = k == 2
        b += box(40, y, 240, 50, "#fff", "#b7c7c5", 10, 1.6) + text(160, y + 31, old[k], 14, MUTED, weight=600)
        b += box(360, y, 240, 50, ACCBG if ch else "#fff", ACC if ch else BRAND2, 10, 2.4 if ch else 1.6)
        b += text(480, y + 31, new[k], 14, INK, weight=800 if ch else 600)
        b += f'<circle cx="24" cy="{y + 25}" r="11" fill="{BRAND}"/>' + text(24, y + 30, str(k + 1), 11, "#fff", weight=800)
        if ch:
            b += arrow(282, y + 25, 356, y + 25, ACC, 3) + text(320, y + 15, "đổi", 12, ACC, weight=800)
        else:
            b += f'<line x1="284" y1="{y + 25}" x2="356" y2="{y + 25}" stroke="#c9d6d4" stroke-width="2" stroke-dasharray="5 4"/>'
            b += text(320, y + 18, "giữ", 11, MUTED, weight=700)
    b += text(320, 380, "Ba bước giữ nguyên. Chỉ cần tập trung học bước số 3.", 13.5, INK, weight=800)
    return b


# 9. K4 B2
@scene("k4-phieu-thu")
def _():
    b = text(320, 30, "Phiếu thử nhỏ của Lan (giả định)", 19, BRAND, weight=800)
    cells = (("Cách cũ", "Dụng cụ để trong ngăn kéo", MUTED), ("Cách mới", "Treo băng dính, kéo lên giá", ACC),
             ("Đo gì", "Số phút cho 10 đơn", BLUE), ("Thử bao lâu", "3 ca", BRAND2))
    for k, (h, v, c) in enumerate(cells):
        x, y = 22 + (k % 2) * 186, 52 + (k // 2) * 160
        b += box(x, y, 176, 148, "#fff", c, 12, 2)
        b += f'<rect x="{x}" y="{y}" width="176" height="34" rx="12" fill="{c}" fill-opacity=".16"/>'
        b += text(x + 88, y + 23, h, 14, c, weight=800)
        words = v.split(" ")
        mid = (len(words) + 1) // 2
        rows = [v] if len(words) <= 2 else [" ".join(words[:mid]), " ".join(words[mid:])]
        b += lines(x + 88, y + 74 + (10 if len(rows) == 1 else 0), rows, 13.5, 20, fill=INK, weight=600)
    # biểu đồ
    b += box(398, 52, 222, 308, "#fff", "#9fb9b6", 12, 1.5)
    b += text(509, 78, "Phút cho 10 đơn", 13.5, INK, weight=800)
    base = 320
    for k, (lb, v, c) in enumerate((("Trước", 25, MUTED), ("Sau", 20, GREEN))):
        h = v * 8.4
        x = 438 + k * 92
        b += f'<rect x="{x}" y="{base - h}" width="56" height="{h}" rx="6" fill="{c}"/>'
        b += text(x + 28, base - h - 8, f"~{v}", 15, c, weight=800) + text(x + 28, base + 22, lb, 13, INK, weight=700)
    b += f'<line x1="420" y1="{base}" x2="600" y2="{base}" stroke="{INK}" stroke-width="1.5"/>'
    b += text(320, 388, "Đổi một điểm · đo trước và sau · thử đủ nhiều lần", 13, INK, weight=800)
    return b


# 10. K9 B2
@scene("k9-dong-thoi-gian")
def _():
    b = text(320, 30, "Điều phối một buổi chiều xếp kho (giả định)", 18.5, BRAND, weight=800)
    b += f'<line x1="60" y1="84" x2="590" y2="84" stroke="{BRAND}" stroke-width="4"/>'
    for x, t, lb in ((80, "13:00", "Đề xuất, chia việc"), (330, "15:00", "Hỏi tiến độ"), (570, "17:00", "Chốt, cảm ơn")):
        b += f'<circle cx="{x}" cy="84" r="11" fill="{ACC}" stroke="#fff" stroke-width="3"/>'
        b += text(x, 62, t, 14, BRAND, weight=800) + text(x, 112, lb, 12.5, INK, weight=700)
    lanes = (("Cặp 1: phân loại", 1.0, BRAND2), ("Cặp 2: gấp", 0.55, ACC), ("Cặp 3: xếp kệ, dán nhãn", 0.9, BLUE))
    for k, (lb, done, c) in enumerate(lanes):
        y = 150 + k * 62
        b += text(60, y - 8, lb, 13, INK, "start", 700)
        b += f'<rect x="60" y="{y}" width="530" height="22" rx="11" fill="#e1eae8"/>'
        b += f'<rect x="60" y="{y}" width="{270 * done}" height="22" rx="11" fill="{c}"/>'
    b += f'<line x1="330" y1="128" x2="330" y2="300" stroke="{RED}" stroke-width="2" stroke-dasharray="5 4"/>'
    b += box(346, 180, 240, 28, REDBG, RED, 8, 1.6) + text(466, 199, "Chậm → xong phần mình rồi sang phụ", 12, RED, weight=700)
    b += box(40, 318, 560, 64, "#fff", GREEN, 12, 2)
    b += lines(320, 342, ["Đề xuất 3 câu: việc cần làm · cách làm · “Mọi người thấy ổn không?”",
                          "Hỏi tiến độ cụ thể, không trách"], 13, 20, fill=INK, weight=700)
    return b


# 11. K4 B4
@scene("k4-hai-hop")
def _():
    b = text(320, 30, "Mượn nguyên lý từ ba lĩnh vực khác", 19, BRAND, weight=800)
    srcs = ("Siêu thị", "bổ sung hàng lên kệ"), ("Quầy pha chế", "hai hộp nguyên liệu"), ("Bệnh viện", "tủ thuốc trực khoa")
    for k, (h, s) in enumerate(srcs):
        x = 24 + k * 206
        b += box(x, 50, 180, 70, "#fff", BLUE, 12, 2) + text(x + 90, 78, h, 14.5, BLUE, weight=800) + text(x + 90, 100, s, 12.5, INK, weight=600)
        b += arrow(x + 90, 120, 320, 160, BLUE, 2)
    b += box(150, 164, 340, 116, ACCBG, ACC, 14, 2.5)
    b += text(320, 188, "Nguyên lý: dùng hai hộp", 15, INK, weight=800)
    for k, (lb, full) in enumerate((("Hộp 1: hết", False), ("Hộp 2: đang dùng", True))):
        x = 196 + k * 150
        b += f'<rect x="{x}" y="204" width="98" height="46" rx="6" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        if full:
            for j in range(6):
                b += f'<circle cx="{x + 14 + j * 14}" cy="232" r="6" fill="{BRAND2}"/>'
        else:
            b += f'<rect x="{x + 22}" y="216" width="54" height="22" rx="4" fill="{RED}"/>' + text(x + 49, 232, "lấy thêm", 11, "#fff", weight=800)
        b += text(x + 49, 268, lb, 12, INK, weight=700)
    b += arrow(320, 280, 320, 306, ACC, 3)
    b += box(120, 308, 400, 72, GREENBG, GREEN, 14, 2)
    b += lines(320, 334, ["Áp vào chuyền may: hộp chỉ, nút, nhãn", "Hộp hết là tín hiệu, chuyền không phải dừng"], 13, 20, fill=INK, weight=700)
    return b


# 12. K4 B5
@scene("k4-cham-y-tuong")
def _():
    b = text(320, 30, "Chấm ý tưởng theo 4 tiêu chí (giả định)", 18.5, BRAND, weight=800)
    heads = (["Tác động"], ["Chi phí", "thử thấp"], ["Mức", "bằng chứng"], ["Quay lại", "được"])
    rows = ((["A. Đổi toàn bộ", "phần mềm kho"], (3, 1, 1, 1), ["Chưa đầu tư:", "cần bằng chứng"], RED, REDBG),
            (["B. Xếp lại", "khu đóng gói"], (2, 3, 2, 3), ["Cho thử", "trước"], GREEN, GREENBG),
            (["C. Tin nhắn", "báo giờ giao"], (2, 3, 1, 3), ["Thử nhỏ", "ở 1 tuyến"], GREEN, GREENBG))
    x0, cw = 172, 80
    for j, h in enumerate(heads):
        x = x0 + j * cw
        b += box(x + 2, 50, cw - 4, 48, BRAND, BRAND, 8)
        b += lines(x + cw / 2, 70 if len(h) == 2 else 79, h, 12, 15, fill="#fff", weight=700)
    b += box(x0 + 4 * cw + 6, 50, 640 - (x0 + 4 * cw) - 22, 48, BRAND, BRAND, 8)
    b += text(x0 + 4 * cw + 6 + (640 - (x0 + 4 * cw) - 22) / 2, 79, "Quyết định", 12.5, "#fff", weight=700)
    for i, (name, sc, verdict, c, bg) in enumerate(rows):
        y = 108 + i * 84
        b += box(16, y, 152, 74, "#fff", "#9fb9b6", 10, 1.5) + lines(92, y + 32, name, 13, 18, fill=INK, weight=700)
        for j, s in enumerate(sc):
            x = x0 + j * cw
            b += box(x + 2, y, cw - 4, 74, "#fff", "#d5e2e0", 8, 1.2)
            for d in range(3):
                b += f'<circle cx="{x + cw / 2 - 20 + d * 20}" cy="{y + 37}" r="7.5" fill="{ACC if d < s else "#e1eae8"}"/>'
        vx = x0 + 4 * cw + 6
        vw = 640 - vx - 16
        b += box(vx, y, vw, 74, bg, c, 10, 2) + lines(vx + vw / 2, y + 32, verdict, 13, 18, fill=c, weight=800)
    b += text(320, 382, "Ý khó quay lại cần bằng chứng mạnh hơn trước khi đầu tư lớn.", 13, INK, weight=800)
    return b


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in SCENES.items():
        bg = "#fdf8ef" if name in WARM else "#eef6f5"
        (OUT / f"{name}.svg").write_text(svg(alt_of(name), fn(), bg), encoding="utf-8")
    print(f"Đã vẽ {len(SCENES)} hình vào {OUT}")
