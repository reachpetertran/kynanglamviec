#!/usr/bin/env python3
"""Hình minh họa tự vẽ (SVG) cho khóa N7 "Founder, khởi nghiệp". Không dùng ảnh ngoài.
Chạy: python3 _build/art/n7_art.py  -> _build/static/assets/img/n7/*.svg
Mọi tên người, nơi làm việc, số liệu trong hình là giả định.
Tiêu đề (aria-label) trùng với alt của ảnh trong bài học.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n2_art import (svg, text, box, BRAND, BRAND2, ACC, ACCBG, INK, MUTED,  # noqa: E402
                    RED, REDBG, GREEN, GREENBG, BLUE, BLUEBG)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_build/static/assets/img/n7"
SCENES = {}


def alt_of(name):
    for f in (ROOT / "content/bai-hoc").glob("*.md"):
        m = re.search(rf'img/n7/{name}\.svg" alt="([^"]+)"', f.read_text(encoding="utf-8"))
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


@scene("l1-cau-hoi-tot-xau")
def _():
    b = text(320, 32, "Hỏi về tương lai hay hỏi về quá khứ?", 19, BRAND, weight=800)
    cols = ((24, "Câu hỏi dẫn dắt", RED, REDBG, "→ cho lời khen",
             ["Chị có thích ứng dụng", "đặt lịch không?", "", "Chị có trả 50 nghìn", "một tháng không?"]),
            (336, "Câu hỏi về quá khứ", GREEN, GREENBG, "→ cho sự thật",
             ["Lần gần nhất chị đặt lịch", "là khi nào?", "Lúc đó chị làm thế nào?", "Chị tốn bao nhiêu", "thời gian?"]))
    for x, head, col, bg, foot, rows in cols:
        b += box(x, 56, 280, 286, bg, col, 14, 2)
        b += text(x + 140, 88, head, 16, col, weight=800)
        for i, r in enumerate(rows):
            if r:
                b += text(x + 140, 132 + i * 34, r, 14, INK, weight=600)
        b += text(x + 140, 322, foot, 15, col, weight=800)
    b += text(320, 376, "Ghi việc khách đã làm, đã trả, đã bỏ thời gian. Không ghi lời khen.", 13, INK, weight=700)
    return b


@scene("l2-nguong-quyet-dinh")
def _():
    b = text(320, 32, "Ba vùng quyết định, vẽ trước khi chạy thử", 19, BRAND, weight=800)
    b += text(320, 62, "Chỉ số: số đơn đặt trước có cọc trong 2 tuần", 14, MUTED, weight=700)
    x0, w = 40, 560
    scale = w / 40
    zones = ((0, 10, RED, REDBG, "Dừng / đổi lớn"), (10, 30, ACC, ACCBG, "Pivot một thành phần"),
             (30, 40, GREEN, GREENBG, "Tiếp tục"))
    for a, z, col, bg, lab in zones:
        b += box(x0 + a * scale, 110, (z - a) * scale, 70, bg, col, 8, 2)
        mid = 24.5 if a == 10 else (a + z) / 2
        b += text(x0 + mid * scale, 151, lab, 13, col, weight=800)
    for v in (0, 10, 20, 30, 40):
        b += text(x0 + v * scale, 204, str(v), 12.5, MUTED)
    xr = x0 + 18 * scale
    b += f'<line x1="{xr}" y1="96" x2="{xr}" y2="196" stroke="{INK}" stroke-width="3"/>'
    b += box(xr - 80, 232, 160, 52, "#fff", INK, 10, 2)
    b += text(xr, 256, "Kết quả thật", 12.5, MUTED) + text(xr, 276, "18 đơn", 16, INK, weight=800)
    b += box(40, 312, 560, 64, "#fff", "#9fb9b6", 12, 1.5)
    b += text(320, 338, "Viết trước: giả thuyết · cách thử · chỉ số · ngưỡng · thời hạn, chi phí tối đa", 13, INK, weight=700)
    b += text(320, 360, "Sau khi có kết quả, không sửa ngưỡng.", 13, RED, weight=700)
    return b


@scene("l3-ke-hoach-90-ngay")
def _():
    b = text(320, 32, "Kế hoạch 90 ngày của một tiệm bánh", 19, BRAND, weight=800)
    b += f'<line x1="60" y1="84" x2="580" y2="84" stroke="{BRAND2}" stroke-width="4"/>'
    ms = (("Ngày 30", "50 khách đặt trước", "Lò hỏng", "Thuê lò chung"),
          ("Ngày 60", "Bán ở 2 quán cà phê", "Quán từ chối", "Bán qua nhóm cư dân"),
          ("Ngày 90", "Hòa vốn tháng", "Giá bột tăng", "Đổi kích cỡ bánh"))
    for i, (d, kq, tro, du) in enumerate(ms):
        cx = 120 + i * 200
        b += f'<circle cx="{cx}" cy="84" r="14" fill="{BRAND2}"/>' + text(cx, 89, str(i + 1), 13, "#fff", weight=800)
        b += text(cx, 122, d, 14, INK, weight=800)
        b += box(cx - 92, 136, 184, 62, BLUEBG, BLUE, 10, 1.5)
        b += text(cx, 158, "Kết quả", 12, BLUE, weight=700) + text(cx, 182, kq, 13, INK, weight=700)
        b += box(cx - 92, 210, 184, 62, REDBG, RED, 10, 1.5)
        b += text(cx, 232, "Trở ngại dự đoán", 12, RED, weight=700) + text(cx, 256, tro, 13, INK, weight=700)
        b += box(cx - 92, 284, 184, 62, GREENBG, GREEN, 10, 1.5)
        b += text(cx, 306, "Nếu… thì…", 12, GREEN, weight=700) + text(cx, 330, du, 13, INK, weight=700)
    b += text(320, 380, "Quyết trước khi còn bình tĩnh. Khi sự cố đến, chỉ cần làm theo.", 13, INK, weight=700)
    return b


@scene("l4-dong-tien-13-tuan")
def _():
    b = text(320, 32, "Tiền cuối tuần trong 13 tuần (triệu đồng)", 19, BRAND, weight=800)
    vals = [40, 34, 29, 25, 20, 14, 8, -6, -12, 10, 18, 22, 27]
    x0, y0, bw, k = 64, 230, 38, 3.2
    b += f'<line x1="{x0 - 10}" y1="{y0}" x2="{x0 + 13 * 40 + 4}" y2="{y0}" stroke="{INK}" stroke-width="2"/>'
    b += text(x0 - 16, y0 + 5, "0", 12, MUTED, anchor="end")
    for i, v in enumerate(vals):
        x = x0 + i * 40
        h = abs(v) * k
        col = RED if v < 0 else BRAND2
        y = y0 - h if v >= 0 else y0
        b += f'<rect x="{x}" y="{y}" width="{bw - 6}" height="{h}" rx="4" fill="{col}"/>'
        b += text(x + (bw - 6) / 2, (y - 6) if v >= 0 else (y + h + 16), str(v), 11.5, col, weight=700)
        b += text(x + (bw - 6) / 2, 300, f"T{i + 1}", 11.5, MUTED)
    b += box(40, 318, 270, 62, REDBG, RED, 10, 1.5)
    b += text(175, 342, "Tuần 8–9 âm tiền:", 13, RED, weight=800)
    b += text(175, 364, "trả nguyên liệu lớn, khách sỉ chưa trả", 12, INK)
    b += box(330, 318, 270, 62, GREENBG, GREEN, 10, 1.5)
    b += text(465, 342, "Thấy từ tuần 2:", 13, GREEN, weight=800)
    b += text(465, 364, "thu sớm · chi muộn · cắt chi · tìm thêm tiền", 12, INK)
    return b


@scene("l5-loai-hinh")
def _():
    b = text(320, 30, "So sánh ba loại hình theo bốn câu hỏi", 19, BRAND, weight=800)
    heads = ("Hộ kinh doanh", "Công ty TNHH", "Công ty cổ phần")
    rows = (("Trách nhiệm", ("Toàn bộ tài sản", "Trong vốn góp", "Trong vốn góp")),
            ("Số chủ", ("Chủ hộ", "1 hoặc nhiều", "Từ 3 cổ đông")),
            ("Gọi vốn", ("Khó nhất", "Hạn chế", "Dễ nhất")),
            ("Giấy tờ", ("Ít nhất", "Vừa", "Nhiều nhất")))
    x0, cw = 156, 156
    for i, h in enumerate(heads):
        b += box(x0 + i * cw + 4, 48, cw - 8, 40, BLUEBG, BLUE, 8, 1.5)
        b += text(x0 + i * cw + cw / 2, 73, h, 13.5, BLUE, weight=800)
    for j, (q, cells) in enumerate(rows):
        y = 100 + j * 64
        b += box(20, y, 128, 54, ACCBG, ACC, 8, 1.5) + text(84, y + 32, q, 13.5, INK, weight=800)
        for i, c in enumerate(cells):
            hot = (j == 0 and i == 0)
            b += box(x0 + i * cw + 4, y, cw - 8, 54, REDBG if hot else "#fff", RED if hot else "#c9d6d4", 8, 1.5)
            b += text(x0 + i * cw + cw / 2, y + 32, c, 13, RED if hot else INK, weight=700 if hot else 400)
    b += text(320, 384, "Tóm tắt để so sánh. Kiểm lại với văn bản gốc trước khi quyết.", 12.5, MUTED, weight=700)
    return b


@scene("l6-tuyen-nguoi-dau-tien")
def _():
    b = text(320, 32, "Bốn bước tuyển và giữ người đầu tiên", 19, BRAND, weight=800)
    steps = (("1", "3 kết quả", "trong 90 ngày", BLUE, BLUEBG), ("2", "Bài làm thử", "45 phút", ACC, ACCBG),
             ("3", "Hợp đồng, thử việc,", "bảo hiểm", RED, REDBG), ("4", "Gặp 1-1", "mỗi tuần 15 phút", GREEN, GREENBG))
    for i, (n, a, c, col, bg) in enumerate(steps):
        x = 24 + i * 152
        b += box(x, 90, 136, 170, bg, col, 14, 2)
        b += f'<circle cx="{x + 68}" cy="126" r="18" fill="{col}"/>' + text(x + 68, 132, n, 16, "#fff", weight=800)
        b += text(x + 68, 186, a, 12.5, INK, weight=800) + text(x + 68, 210, c, 12.5, INK)
        if i < 3:
            b += arrow(x + 138, 175, x + 150, 175)
    b += box(24, 296, 592, 64, "#fff", "#9fb9b6", 12, 1.5)
    b += text(320, 322, "Mô tả bằng kết quả, không bằng chức danh.", 14, INK, weight=800)
    b += text(320, 345, "Tên gọi \"cộng tác viên\" không đổi bản chất hợp đồng.", 13, MUTED, weight=700)
    return b


@scene("l7-pitch-5-phan")
def _():
    b = text(320, 32, "Pitch 3 phút: 5 phần", 19, BRAND, weight=800)
    parts = (("Vấn đề", 30, BLUE), ("Bằng chứng", 45, GREEN), ("Giải pháp", 45, BRAND2), ("Con số", 30, ACC), ("Đề nghị", 30, RED))
    x, k = 30, 580 / 180
    for name, s, col in parts:
        w = s * k
        b += f'<rect x="{x}" y="64" width="{w - 4}" height="64" rx="8" fill="{col}"/>'
        b += text(x + w / 2 - 2, 92, name, 13.5, "#fff", weight=800) + text(x + w / 2 - 2, 114, f"{s} giây", 12, "#fff")
        x += w
    b += box(30, 168, 280, 170, GREENBG, GREEN, 12, 2)
    b += text(170, 198, "Số đã có", 16, GREEN, weight=800)
    b += text(170, 240, "18 đơn cọc", 18, INK, weight=800) + text(170, 266, "trong 3 tuần", 14, INK)
    b += text(170, 312, "Nói: \"Đây là số thật\"", 13, GREEN, weight=700)
    b += box(330, 168, 280, 170, ACCBG, ACC, 12, 2)
    b += text(470, 198, "Số dự báo", 16, ACC, weight=800)
    b += text(470, 240, "200 đơn mỗi tháng", 18, INK, weight=800) + text(470, 266, "sau 6 tháng", 14, INK)
    b += text(470, 312, "Nói: \"Đây là dự báo\"", 13, ACC, weight=700)
    b += text(320, 374, "Kiểm: người nghe nhắc lại đúng đề nghị của bạn.", 13.5, INK, weight=700)
    return b


@scene("l8-bang-cong-cu-so")
def _():
    b = text(320, 30, "Bảng công cụ số của một tiệm bánh", 19, BRAND, weight=800)
    heads = ("Công cụ", "Dữ liệu", "Dữ liệu cá nhân?")
    cws = (200, 250, 142)
    x = 24
    for h, w in zip(heads, cws):
        b += box(x + 2, 50, w - 4, 36, BLUEBG, BLUE, 8, 1.5) + text(x + w / 2, 73, h, 13.5, BLUE, weight=800)
        x += w
    rows = (("Trang bán hàng", "Tên, số điện thoại khách", True), ("Ví điện tử", "Dữ liệu thanh toán", True),
            ("Phần mềm hóa đơn", "Mã số thuế khách sỉ", True), ("Nhóm chat nhân viên", "Lịch ca", True),
            ("Thư mục ảnh sản phẩm", "Ảnh bánh", False))
    for j, (a, d, pd) in enumerate(rows):
        y = 96 + j * 54
        x = 24
        bg, st = (ACCBG, ACC) if pd else ("#fff", "#c9d6d4")
        for c, w in zip((a, d, "Có" if pd else "Không"), cws):
            b += box(x + 2, y, w - 4, 46, bg, st, 8, 1.2) + text(x + w / 2, y + 28, c, 13, INK, weight=700 if c == a else 400)
            x += w
    b += text(320, 384, "Dòng tô vàng: kiểm quyền truy cập, sao lưu, thu quyền khi nhân viên nghỉ.", 12.5, INK, weight=700)
    return b


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in SCENES.items():
        bg = "#fdf8ef" if name in ("l1-cau-hoi-tot-xau", "l8-bang-cong-cu-so") else "#eef6f5"
        (OUT / f"{name}.svg").write_text(svg(alt_of(name), fn(), bg), encoding="utf-8")
    print(f"Đã vẽ {len(SCENES)} hình vào {OUT}")
