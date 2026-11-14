#!/usr/bin/env python3
"""Hình minh họa tự vẽ (SVG) cho khóa N6 "Lãnh đạo cấp cao". Không dùng ảnh ngoài.
Chạy: python3 _build/art/n6_art.py  -> _build/static/assets/img/n6/*.svg
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
OUT = ROOT / "_build/static/assets/img/n6"
SCENES = {}


def alt_of(name):
    for f in (ROOT / "content/bai-hoc").glob("*.md"):
        m = re.search(rf'img/n6/{name}\.svg" alt="([^"]+)"', f.read_text(encoding="utf-8"))
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


@scene("l1-lich-dieu-hanh")
def _():
    b = text(320, 30, "Lịch tuần của giám đốc: trước và sau", 19, BRAND, weight=800)
    days = ["T2", "T3", "T4", "T5", "T6"]
    before = [["D", "D", "D"], ["D", "D", "T"], ["D", "D", "D"], ["D", "D", "D"], ["D", "D", "D"]]
    after = [["T", "D", "D"], ["D", "T", "D"], ["D", "D", "T"], ["T", "D", "D"], ["D", "T", "T"]]
    for ox, title, grid in ((24, "Trước", before), (336, "Sau", after)):
        b += text(ox + 140, 64, title, 16, INK, weight=800)
        for i, d in enumerate(days):
            x = ox + i * 56
            b += text(x + 26, 88, d, 12, MUTED, weight=700)
            for j, c in enumerate(grid[i]):
                y = 96 + j * 62
                col, bg = (GREEN, GREENBG) if c == "T" else (RED, REDBG)
                b += box(x + 2, y, 48, 54, bg, col, 8, 1.5)
                b += text(x + 26, y + 33, c, 16, col, weight=800)
    b += box(24, 300, 592, 84, "#fff", "#9fb9b6", 12, 1.5)
    b += box(40, 318, 22, 22, REDBG, RED, 5, 1.5) + text(70, 334, "D: cấp dưới làm được (duyệt đơn nhỏ, khiếu nại lẻ, sửa báo cáo)", 12.5, INK, anchor="start")
    b += box(40, 350, 22, 22, GREENBG, GREEN, 5, 1.5) + text(70, 366, "T: việc cấp tổ chức (rà soát chiến lược, người kế cận, đi tuyến đầu, rủi ro)", 12.5, INK, anchor="start")
    return b


@scene("l2-hai-goc-nhin")
def _():
    b = text(320, 30, "Ước tính thời gian mở 20 cửa hàng", 19, BRAND, weight=800)
    b += box(24, 52, 280, 120, ACCBG, ACC, 12, 2)
    b += text(164, 80, "Góc nhìn bên trong", 15, ACC, weight=800)
    b += text(164, 112, "Kế hoạch ghi", 13, MUTED) + text(164, 148, "6 tháng", 26, INK, weight=800)
    b += box(336, 52, 280, 120, BLUEBG, BLUE, 12, 2)
    b += text(476, 80, "Góc nhìn bên ngoài", 15, BLUE, weight=800)
    b += text(476, 112, "6 lần mở rộng trước", 13, MUTED) + text(476, 148, "8 – 11 tháng", 24, INK, weight=800)
    # trục tháng
    x0, w = 60, 520 / 12
    b += f'<line x1="{x0}" y1="300" x2="{x0 + 12 * w}" y2="300" stroke="{MUTED}" stroke-width="2"/>'
    for m in range(0, 13, 2):
        b += text(x0 + m * w, 320, str(m), 11.5, MUTED)
    b += text(320, 340, "tháng", 11.5, MUTED)
    for v, y in ((8, 270), (9, 255), (9, 240), (10, 270), (11, 255), (8, 240)):
        b += f'<circle cx="{x0 + v * w}" cy="{y}" r="8" fill="{BLUE}" opacity="0.8"/>'
    b += f'<line x1="{x0 + 6 * w}" y1="210" x2="{x0 + 6 * w}" y2="300" stroke="{ACC}" stroke-width="3" stroke-dasharray="6 4"/>'
    b += text(x0 + 6 * w, 202, "kế hoạch", 12, ACC, weight=700)
    b += f'<line x1="{x0 + 9 * w}" y1="210" x2="{x0 + 9 * w}" y2="300" stroke="{GREEN}" stroke-width="3"/>'
    b += text(x0 + 9 * w, 202, "mức ở giữa ≈ 9", 12, GREEN, weight=700)
    b += box(24, 352, 592, 36, GREENBG, GREEN, 10, 1.5)
    b += text(320, 376, "Bắt đầu từ 9 tháng, rồi chỉnh theo điểm khác biệt có lý do", 13.5, INK, weight=700)
    return b


@scene("l3-chuoi-chien-luoc")
def _():
    b = text(320, 30, "Một ưu tiên, ba khối, hai chỗ phụ thuộc", 19, BRAND, weight=800)
    b += box(110, 50, 420, 60, BLUEBG, BLUE, 12, 2)
    b += text(320, 74, "Ưu tiên", 13, BLUE, weight=800)
    b += text(320, 96, "Giao hàng nội thành dưới 24 giờ trước tháng 6", 14, INK, weight=600)
    blocks = [(24, "Kho", "Soạn hàng xong trong 4 giờ"), (232, "Vận tải", "95% chuyến đúng giờ"),
              (440, "Công nghệ", "Đơn tự chuyển web → kho")]
    for x, n, r in blocks:
        b += arrow(320, 110, x + 88, 168, BRAND2, 2)
        b += box(x, 172, 176, 82, GREENBG, GREEN, 12, 2)
        b += text(x + 88, 200, n, 15, GREEN, weight=800) + text(x + 88, 228, r, 12, INK)
    # phụ thuộc
    b += f'<path d="M 528 256 C 480 330, 160 330, 112 256" fill="none" stroke="{RED}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    b += f'<circle cx="112" cy="256" r="5" fill="{RED}"/>'
    b += f'<circle cx="320" cy="311" r="12" fill="{RED}"/>' + text(320, 316, "1", 13, "#fff", weight=800)
    b += f'<path d="M 112 256 C 140 286, 290 286, 320 256" fill="none" stroke="{ACC}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    b += f'<circle cx="320" cy="256" r="5" fill="{ACC}"/>'
    b += f'<circle cx="216" cy="278" r="12" fill="{ACC}"/>' + text(216, 283, "2", 13, "#fff", weight=800)
    b += box(24, 330, 592, 62, ACCBG, ACC, 10, 1.5)
    b += text(320, 350, "Chỗ phụ thuộc: (1) Kho cần Công nghệ · (2) Vận tải cần Kho", 13, INK, weight=600)
    b += text(320, 368, "Mỗi chỗ phụ thuộc có một người điều phối có tên", 13.5, INK, weight=800)
    b += text(320, 385, "Rà soát tháng: tiếp tục · đổi cách làm · dừng", 12, MUTED)
    return b


@scene("l4-thong-diep-qua-cap")
def _():
    b = text(320, 30, "Thông điệp đi qua bốn cấp", 19, BRAND, weight=800)
    rows = [(BLUE, BLUEBG, "Ban điều hành", "Ưu tiên giữ khách cũ, chưa mở chi nhánh mới"),
            (GREEN, GREENBG, "Giám đốc khối", "Năm nay tập trung khách cũ"),
            (ACC, ACCBG, "Trưởng phòng", "Năm nay công ty khó khăn"),
            (RED, REDBG, "Tổ trưởng", "Sắp cắt giảm người")]
    for i, (col, bg, who, msg) in enumerate(rows):
        y = 52 + i * 78
        w = 560 - i * 60
        x = 320 - w / 2
        b += box(x, y, w, 60, bg, col, 12, 2)
        b += text(320, y + 24, who, 13, col, weight=800)
        b += text(320, y + 46, "“" + msg + "”", 14, INK, weight=600)
        if i < 3:
            b += arrow(320, y + 60, 320, y + 76, MUTED, 2)
    b += text(320, 382, "Mỗi cấp bỏ bớt một phần. Đến tuyến đầu, nghĩa đã khác.", 13.5, RED, weight=700)
    return b


@scene("l5-bang-quyen")
def _():
    b = text(320, 30, "Bảng quyền quyết định (rút gọn)", 19, BRAND, weight=800)
    cols = ["Đề xuất", "Được hỏi", "Quyết", "Được báo"]
    rows = [("Giảm giá khách lớn ≤ 5%", ["NV KD", "KT giá", "GĐ KD", "GĐ SX"]),
            ("Tuyển trưởng phòng", ["GĐ khối", "Nhân sự", "TGĐ", "Khối liên quan"]),
            ("Mua máy dưới ngưỡng", ["Xưởng", "Kỹ thuật", "GĐ NM", "Kế toán"]),
            ("Đổi nhà cung cấp chính", ["Mua hàng", "SX, QA", "GĐ SX", "Kế toán"]),
            ("Ra mẫu sản phẩm mới", ["Thiết kế", "KD, SX", "GĐ KD", "Kho"])]
    x0, cw = 196, 104
    b += box(24, 48, 592, 36, BLUEBG, BLUE, 8, 1.5)
    b += text(110, 71, "Quyết định", 13, BLUE, weight=800)
    for i, c in enumerate(cols):
        b += text(x0 + i * cw + cw / 2, 71, c, 13, BLUE, weight=800)
    for j, (name, cells) in enumerate(rows):
        y = 90 + j * 52
        b += box(24, y, 592, 46, "#fff", "#c9d6d4", 8, 1)
        b += text(32, y + 28, name, 12.5, INK, anchor="start", weight=600)
        for i, c in enumerate(cells):
            cx = x0 + i * cw
            if i == 2:
                b += box(cx + 6, y + 6, cw - 12, 34, GREENBG, GREEN, 8, 2)
                b += text(cx + cw / 2, y + 28, c, 12.5, GREEN, weight=800)
            else:
                b += text(cx + cw / 2, y + 28, c, 12, INK)
    b += text(320, 372, "Mỗi hàng chỉ có một ô Quyết", 14, GREEN, weight=800)
    b += text(320, 390, "Viết tắt: NV nhân viên, KD kinh doanh, KT kế toán, SX sản xuất, NM nhà máy", 11, MUTED)
    return b


@scene("l6-tin-xau-di-len")
def _():
    b = text(320, 30, "Đường đi của tin xấu", 19, BRAND, weight=800)
    levels = ["Ban điều hành", "Giám đốc khối", "Trưởng phòng", "Tổ trưởng", "Tuyến đầu"]
    for side, ox, title in ((0, 24, "Không có kênh"), (1, 336, "Có Kênh tin xấu")):
        col, bg = (RED, REDBG) if side == 0 else (GREEN, GREENBG)
        b += text(ox + 140, 60, title, 15, col, weight=800)
        for i, lv in enumerate(levels):
            y = 72 + i * 52
            b += box(ox + 40, y, 200, 38, "#fff" if i else bg, col, 10, 1.5)
            b += text(ox + 140, y + 24, lv, 13, INK, weight=600)
        if side == 0:
            for i in range(4, 0, -1):
                y = 72 + i * 52
                b += arrow(ox + 140, y, ox + 140, y - 12, RED, 2)
            b += text(ox + 140, 342, "Mỗi cấp lọc bớt tin", 12.5, RED, weight=700)
            b += text(ox + 140, 362, "→ lên đến nơi: “mọi thứ ổn”", 12.5, RED, weight=700)
        else:
            for i in range(4, 0, -1):
                y = 72 + i * 52
                b += arrow(ox + 140, y, ox + 140, y - 12, GREEN, 2)
            b += f'<path d="M {ox + 250} {72 + 4 * 52 + 19} C {ox + 300} 240, {ox + 300} 130, {ox + 250} 91" fill="none" stroke="{ACC}" stroke-width="2.5" stroke-dasharray="6 4"/>'
            b += f'<circle cx="{ox + 250}" cy="91" r="5" fill="{ACC}"/>'
            b += text(ox + 140, 342, "An toàn, khách lớn, pháp lý, tài chính", 12, GREEN, weight=700)
            b += text(ox + 140, 362, "lên trong 48 giờ · có đường vượt cấp", 12, GREEN, weight=700)
    return b


@scene("l7-ban-do-rui-ro")
def _():
    b = text(320, 28, "Bản đồ rủi ro: khả năng × tác động", 19, BRAND, weight=800)
    x0, y0, s = 120, 50, 58
    for i in range(5):
        for j in range(5):
            score = (i + 1) * (5 - j)
            col = REDBG if score >= 10 else (ACCBG if score >= 5 else GREENBG)
            b += box(x0 + i * s, y0 + j * s, s - 4, s - 4, col, "#fff", 6, 1)
    for i in range(5):
        b += text(x0 + i * s + 27, y0 + 5 * s + 16, str(i + 1), 12, MUTED)
        b += text(x0 - 14, y0 + i * s + 33, str(5 - i), 12, MUTED)
    b += text(x0 + 2.5 * s, y0 + 5 * s + 36, "Khả năng xảy ra →", 12.5, INK, weight=700)
    b += f'<text x="70" y="{y0 + 2.5 * s}" font-size="12.5" fill="{INK}" font-weight="700" text-anchor="middle" transform="rotate(-90 70 {y0 + 2.5 * s})">Tác động →</text>'
    pts = [(3, 5, "1"), (2, 5, "2"), (4, 4, "3"), (3, 4, "4")]
    for p, im, n in pts:
        cx, cy = x0 + (p - 1) * s + 27, y0 + (5 - im) * s + 27
        b += f'<circle cx="{cx}" cy="{cy}" r="13" fill="{RED}"/>' + text(cx, cy + 5, n, 13, "#fff", weight=800)
    legend = ["1 Mất khách lớn nhất", "2 Sự cố an toàn lao động", "3 Lộ dữ liệu khách hàng", "4 Người chủ chốt nghỉ đột ngột"]
    b += box(430, 70, 190, 150, "#fff", "#c9d6d4", 10, 1.5)
    for k, t in enumerate(legend):
        b += text(442, 100 + k * 32, t, 11.5, INK, anchor="start")
    b += box(430, 236, 190, 96, REDBG, RED, 10, 1.5)
    b += text(525, 262, "Vùng đỏ:", 13, RED, weight=800)
    b += text(525, 284, "ban điều hành", 12.5, INK)
    b += text(525, 304, "theo dõi mỗi quý", 12.5, INK)
    return b


@scene("l8-ban-do-ke-nhiem")
def _():
    b = text(320, 30, "Bản đồ kế nhiệm: 4 vị trí then chốt", 19, BRAND, weight=800)
    heads = ["Sẵn sàng ngay", "Sau 1–2 năm", "Sau 3 năm+"]
    x0, cw = 196, 140
    for i, h in enumerate(heads):
        b += box(x0 + i * cw + 4, 50, cw - 8, 34, BLUEBG, BLUE, 8, 1.5)
        b += text(x0 + i * cw + cw / 2, 72, h, 13, BLUE, weight=800)
    rows = [("Giám đốc tài chính", 0), ("Giám đốc nhà máy", 1), ("Giám đốc kinh doanh", 2), ("Trưởng phòng công nghệ", None)]
    for j, (pos, lv) in enumerate(rows):
        y = 96 + j * 66
        miss = lv is None
        b += box(24, y, 164, 56, REDBG if miss else "#fff", RED if miss else "#9fb9b6", 10, 2 if miss else 1.5)
        b += text(106, y + 33, pos, 12.5, INK, weight=700)
        for i in range(3):
            b += box(x0 + i * cw + 4, y, cw - 8, 56, "#fff", "#c9d6d4", 10, 1)
        if miss:
            b += text(x0 + 1.5 * cw, y + 33, "Chưa có ai → ghi vào Sổ rủi ro", 13, RED, weight=800)
        else:
            cx = x0 + lv * cw + cw / 2
            b += f'<circle cx="{cx}" cy="{y + 28}" r="16" fill="{GREEN}"/>'
            b += text(cx, y + 33, "1", 13, "#fff", weight=800)
    b += box(24, 364, 592, 30, ACCBG, ACC, 8, 1.5)
    b += text(320, 384, "Mỗi người kế cận: việc thử thách · người kèm · mốc xem lại 6 tháng", 12.5, INK, weight=700)
    return b


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in SCENES.items():
        bg = "#fdf8ef" if name in ("l1-lich-dieu-hanh", "l8-ban-do-ke-nhiem") else "#eef6f5"
        (OUT / f"{name}.svg").write_text(svg(alt_of(name), fn(), bg), encoding="utf-8")
    print(f"Đã vẽ {len(SCENES)} hình vào {OUT}")
