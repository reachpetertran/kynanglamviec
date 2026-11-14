#!/usr/bin/env python3
"""Hình minh họa tự vẽ (SVG) cho khóa N5 "Quản lý, trưởng nhóm". Không dùng ảnh ngoài.
Chạy: python3 _build/art/n5_art.py  -> _build/static/assets/img/n5/*.svg
Mọi tên người, nơi làm việc, số liệu trong hình là giả định.
Tiêu đề (aria-label) trùng với alt của ảnh trong bài học.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n2_art import (svg, text, lines, box, BRAND, BRAND2, ACC, ACCBG, INK, MUTED,  # noqa: E402
                    RED, REDBG, GREEN, GREENBG, BLUE, BLUEBG)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_build/static/assets/img/n5"
SCENES = {}


def alt_of(name):
    """Lấy alt từ bài học để hình và bài luôn khớp."""
    for f in (ROOT / "content/bai-hoc").glob("*.md"):
        m = re.search(rf'img/n5/{name}\.svg" alt="([^"]+)"', f.read_text(encoding="utf-8"))
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


def dot(x, y, col, r=5):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>'


@scene("l1-ba-cot")
def _():
    b = text(320, 32, "Bản chuyển vai của tổ trưởng mới", 19, BRAND, weight=800)
    cols = [(24, RED, REDBG, "Buông", "giao lại cho tổ",
             ["Tự may mẫu khó", "Tự sửa hàng lỗi", "Tự đi lấy phụ liệu"]),
            (226, ACC, ACCBG, "Giữ", "ít, có hạn",
             ["Duyệt mẫu đầu chuyền", "(đến hết tháng 2)"]),
            (428, GREEN, GREENBG, "Mới", "việc của quản lý",
             ["Họp đầu ca 10 phút", "Giao việc theo bảng", "1-1 mỗi tuần 3 người", "Kèm 2 thợ công đoạn khó"])]
    for x, col, bg, t, sub, rows in cols:
        b += box(x, 54, 188, 300, bg, col, 14, 2)
        b += text(x + 94, 88, t, 20, col, weight=800) + text(x + 94, 110, sub, 12, MUTED)
        for i, r in enumerate(rows):
            y = 150 + i * 44
            b += box(x + 12, y - 22, 164, 34, "#fff", col, 8, 1.5)
            b += text(x + 94, y, r, 12.5, INK, weight=600 if not r.startswith("(") else 400)
    b += arrow(214, 370, 426, 370, BRAND, 3)
    b += text(320, 392, "Buông việc cũ → có thời gian cho việc mới", 13, BRAND, weight=700)
    return b


@scene("l2-chuoi-muc-tieu")
def _():
    b = text(320, 32, "Chuỗi mục tiêu: từ công ty đến từng người", 19, BRAND, weight=800)
    b += box(120, 52, 400, 64, BLUEBG, BLUE, 12, 2)
    b += text(320, 78, "Công ty", 14, BLUE, weight=800)
    b += text(320, 100, "Giảm khiếu nại của khách 30% trong năm", 13.5, INK)
    b += arrow(320, 116, 320, 146)
    b += box(80, 150, 480, 84, GREENBG, GREEN, 12, 2)
    b += text(320, 176, "Đội chăm sóc khách hàng · đến hết quý 2", 14, GREEN, weight=800)
    b += text(320, 200, "Trả lời lần đầu trong 2 giờ", 13.5, INK)
    b += text(320, 220, "Giải quyết ngay lần đầu 80%", 13.5, INK)
    people = [(40, "Mai", ["Kênh email"]), (240, "Tùng", ["Kênh điện thoại"]), (440, "Hà", ["Viết lại 10", "câu trả lời mẫu"])]
    for x, n, rows in people:
        b += arrow(320, 234, x + 80, 266, BRAND2, 2)
        b += box(x, 270, 160, 84, ACCBG, ACC, 12, 2)
        b += f'<circle cx="{x + 28}" cy="298" r="14" fill="#fff" stroke="{ACC}" stroke-width="2"/>'
        b += text(x + 28, 303, n[0], 13, ACC, weight=800)
        b += text(x + 96, 302, n, 15, INK, weight=800)
        b += lines(x + 80, 328, rows, 12.5, 16, fill=INK)
    b += text(320, 384, "Không làm đến hết quý 2: video hướng dẫn", 13, RED, weight=700)
    return b


@scene("l3-muc-tu-quyet")
def _():
    b = text(320, 32, "Bốn mức tự quyết khi giao việc", 19, BRAND, weight=800)
    steps = [("1", "Làm theo hướng dẫn", "hỏi khi có gì khác", RED, REDBG),
             ("2", "Đề xuất, chờ duyệt", "rồi mới làm", ACC, ACCBG),
             ("3", "Tự làm, báo sau", "báo khi xong", BLUE, BLUEBG),
             ("4", "Tự quyết hoàn toàn", "báo ở họp định kỳ", GREEN, GREENBG)]
    for i, (n, t, s, col, bg) in enumerate(steps):
        x = 30 + i * 148
        y = 230 - i * 45
        h = 350 - y
        b += box(x, y, 136, h, bg, col, 12, 2)
        b += f'<circle cx="{x + 68}" cy="{y + 30}" r="17" fill="{col}"/>' + text(x + 68, y + 36, n, 16, "#fff", weight=800)
        b += lines(x + 68, y + 70, [t], 13, 16, fill=INK, weight=800)
        b += lines(x + 68, y + 90, [s], 12, 16, fill=MUTED)
    b += arrow(40, 366, 600, 366, BRAND, 2.5)
    b += text(320, 390, "Quản lý can thiệp ít dần →", 12.5, BRAND, weight=700)
    b += lines(98, 80, ["Rủi ro cao,", "người còn mới"], 12.5, 16, fill=RED, weight=700)
    b += lines(542, 60, ["Việc quen,", "rủi ro thấp"], 12.5, 16, fill=GREEN, weight=700)
    return b


@scene("l4-bon-buoc")
def _():
    b = text(320, 32, "Buổi 1-1: bốn bước câu hỏi", 19, BRAND, weight=800)
    steps = [("Mục tiêu", ["Hôm nay em muốn", "ra về với điều gì?"], BLUE, BLUEBG),
             ("Thực tế", ["Đang thế nào?", "Em đã thử gì?"], ACC, ACCBG),
             ("Lựa chọn", ["Còn cách nào", "khác nữa?"], BRAND2, "#e3f0ee"),
             ("Bước tiếp", ["Em làm gì trước?", "Khi nào?"], GREEN, GREENBG)]
    for i, (t, q, col, bg) in enumerate(steps):
        x = 24 + i * 152
        b += box(x, 60, 136, 180, bg, col, 14, 2)
        b += f'<circle cx="{x + 68}" cy="94" r="18" fill="{col}"/>' + text(x + 68, 100, str(i + 1), 16, "#fff", weight=800)
        b += text(x + 68, 140, t, 15, col, weight=800)
        b += f'<path d="M{x + 14} 160 h108 a8 8 0 0 1 8 8 v40 a8 8 0 0 1 -8 8 h-70 l-10 10 v-10 h-28 a8 8 0 0 1 -8 -8 v-40 a8 8 0 0 1 8 -8z" fill="#fff" stroke="{col}" stroke-width="1.5"/>'
        b += lines(x + 68, 182, q, 11.5, 16, fill=INK)
        if i < 3:
            b += arrow(x + 136, 150, x + 152, 150, BRAND, 2)
    b += text(320, 276, "Ai nói nhiều hơn?", 14, BRAND, weight=800)
    b += text(110, 312, "Quản lý", 13, INK, "start", 700)
    b += f'<rect x="200" y="300" width="120" height="16" rx="5" fill="{ACC}"/>'
    b += text(330, 313, "hỏi, tóm lại, chờ", 12, MUTED, "start")
    b += text(110, 348, "Nhân viên", 13, INK, "start", 700)
    b += f'<rect x="200" y="336" width="300" height="16" rx="5" fill="{GREEN}"/>'
    b += text(510, 349, "kể, nghĩ, chọn", 12, MUTED, "start")
    b += text(320, 386, "Minh họa ý tưởng, không phải số đo", 11.5, MUTED)
    return b


@scene("l5-hai-loai")
def _():
    b = text(320, 30, "Hai loại đối thoại khó", 19, BRAND, weight=800)
    sides = [(24, BLUE, BLUEBG, "Với một người", "về kết quả công việc",
              ["Sự kiện", "Tác động", "Hỏi và nghe", "Thỏa thuận", "Ngày xem lại"]),
             (330, ACC, ACCBG, "Giữa hai người", "hòa giải xung đột",
              ["Gặp riêng A", "Gặp riêng B", "Gặp chung", "Tiêu chí chung", "Thỏa thuận cách làm"])]
    for x, col, bg, t, s, rows in sides:
        b += box(x, 48, 286, 250, bg, col, 14, 2)
        b += text(x + 143, 76, t, 16, col, weight=800) + text(x + 143, 96, s, 12, MUTED)
        for i, r in enumerate(rows):
            y = 126 + i * 34
            b += f'<circle cx="{x + 40}" cy="{y - 4}" r="11" fill="{col}"/>' + text(x + 40, y + 1, str(i + 1), 12, "#fff", weight=800)
            b += text(x + 62, y + 1, r, 13.5, INK, "start", 600)
    b += box(24, 312, 592, 72, REDBG, RED, 12, 2)
    b += text(320, 340, "Vùng không hòa giải", 15, RED, weight=800)
    b += text(320, 364, "Quấy rối, bạo lực, gian lận, nguy hiểm an toàn → báo theo quy trình", 13, INK)
    return b


@scene("l6-luot-noi")
def _():
    b = text(320, 30, "Ai được nghe trong cuộc họp?", 19, BRAND, weight=800)
    panels = [(24, RED, REDBG, "Trước thỏa thuận", [92, 70, 60, 10, 8, 6, 4],
               "Vài người nói gần hết giờ"),
              (330, GREEN, GREENBG, "Sau thỏa thuận", [34, 30, 32, 28, 30, 26, 24],
               "Viết trước, người ít nói nói trước")]
    names = ["QL", "A", "B", "C", "D", "E", "Từ xa"]
    for x, col, bg, t, vals, note in panels:
        b += box(x, 48, 286, 300, bg, col, 14, 2)
        b += text(x + 143, 76, t, 15, col, weight=800)
        for i, (n, v) in enumerate(zip(names, vals)):
            y = 104 + i * 32
            b += text(x + 64, y + 12, n, 12, INK, "end", 700)
            b += f'<rect x="{x + 74}" y="{y}" width="{v * 2}" height="16" rx="5" fill="{col}" fill-opacity=".85"/>'
        b += text(x + 143, 336, note, 12.5, INK, weight=600)
    b += text(320, 380, "Độ dài thanh: thời gian nói, minh họa giả định", 12, MUTED)
    return b


@scene("l7-thu-nho")
def _():
    b = text(320, 30, "Thử nhỏ, đo, rồi mới mở rộng", 19, BRAND, weight=800)
    stages = [(24, 150, BLUE, BLUEBG, "Giai đoạn 1", "Tuần 1–2", ["2 người tình nguyện", "soạn nháp thông báo"]),
              (230, 110, ACC, ACCBG, "Giai đoạn 2", "Tuần 3–6", ["Cả phòng dùng", "quy tắc 5 dòng", "chia sẻ lỗi mỗi tuần"]),
              (436, 70, GREEN, GREENBG, "Giai đoạn 3", "Từ tuần 7", ["Đo thời gian, số lỗi", "mở rộng hay dừng"])]
    for x, y, col, bg, t, w, rows in stages:
        b += box(x, y, 180, 300 - y, bg, col, 14, 2)
        b += text(x + 90, y + 28, t, 15, col, weight=800) + text(x + 90, y + 48, w, 12.5, MUTED, weight=700)
        b += lines(x + 90, y + 78, rows, 12.5, 18, fill=INK)
    b += arrow(204, 220, 228, 200) + arrow(410, 180, 434, 160)
    b += box(24, 318, 592, 62, REDBG, RED, 12, 2)
    b += text(320, 344, "Mọi giai đoạn: không đưa dữ liệu cá nhân", 14, RED, weight=800)
    b += text(320, 366, "của người lao động vào AI", 14, RED, weight=800)
    return b


@scene("l8-can-suc")
def _():
    b = text(320, 30, "Cân công sức của đội trong một quý", 19, BRAND, weight=800)
    # cán cân
    b += f'<polygon points="320,300 300,340 340,340" fill="{BRAND}"/>'
    b += f'<line x1="120" y1="250" x2="520" y2="200" stroke="{BRAND}" stroke-width="5" stroke-linecap="round"/>'
    b += f'<circle cx="320" cy="225" r="7" fill="{BRAND}"/>'
    b += f'<line x1="320" y1="225" x2="320" y2="300" stroke="{BRAND}" stroke-width="4"/>'
    # đĩa trái: việc cần làm
    b += box(40, 150, 170, 100, REDBG, RED, 12, 2)
    b += text(125, 178, "7 việc cần", 15, RED, weight=800)
    b += text(125, 206, "340", 26, INK, weight=800)
    b += text(125, 230, "ngày công", 12.5, MUTED)
    # đĩa phải: sức thật
    b += box(430, 100, 170, 100, GREENBG, GREEN, 12, 2)
    b += text(515, 128, "Sức thật", 15, GREEN, weight=800)
    b += text(515, 156, "250", 26, INK, weight=800)
    b += text(515, 180, "sau khi trừ phép, họp…", 11.5, MUTED)
    b += box(40, 348, 560, 40, ACCBG, ACC, 10, 2)
    b += text(320, 373, "Dừng 1 việc · Hoãn 1 việc sang quý sau · Thu nhỏ 1 việc", 13.5, INK, weight=700)
    b += text(320, 70, "Thiếu khoảng 90 ngày công → phải bớt việc", 14, RED, weight=700)
    return b


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in SCENES.items():
        bg = "#fdf8ef" if name in ("l1-ba-cot", "l8-can-suc") else "#eef6f5"
        (OUT / f"{name}.svg").write_text(svg(alt_of(name), fn(), bg), encoding="utf-8")
    print(f"Đã vẽ {len(SCENES)} hình vào {OUT}")
