#!/usr/bin/env python3
"""Hình minh họa tự vẽ (SVG) cho khóa N3 "90 ngày đầu". Không dùng ảnh ngoài.
Chạy: python3 _build/art/n3_art.py  -> _build/static/assets/img/n3/*.svg
Mọi tên người, nơi làm việc trong hình là giả định.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n2_art import (svg, text, lines, box, BRAND, BRAND2, ACC, ACCBG, INK, MUTED,  # noqa: E402
                    RED, REDBG, GREEN, GREENBG, BLUE, BLUEBG)

OUT = Path(__file__).resolve().parents[1] / "static/assets/img/n3"
SCENES = {}


def scene(name, title):
    def deco(fn):
        SCENES[name] = (title, fn)
        return fn
    return deco


def chip(x, y, s, fill, col, w=None, size=12):
    w = w or (len(s) * 7 + 18)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="{fill}" stroke="{col}"/>'
            + text(x + w / 2, y + 16, s, size, col, weight=700))


def arrow(x1, y1, x2, y2, col=BRAND2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2.5"/>'
            f'<circle cx="{x2}" cy="{y2}" r="4.5" fill="{col}"/>')


@scene("l1-ma-tran", "Ma trận bốn ô sắp ưu tiên, giả định. Trục ngang là hạn gần hay xa, trục dọc là ảnh hưởng lớn hay nhỏ. Ô ảnh hưởng lớn, hạn gần: làm trước. Ảnh hưởng lớn, hạn xa: xếp lịch. Ảnh hưởng nhỏ, hạn gần: làm nhanh hoặc hỏi. Ảnh hưởng nhỏ, hạn xa: để sau.")
def _():
    b = text(320, 32, "Sắp ưu tiên: ảnh hưởng × hạn", 19, BRAND, weight=800)
    cells = [(110, 56, RED, REDBG, "1. Làm trước", ["Ảnh hưởng lớn", "Hạn gần"], ["Báo cáo số liệu", "cho khách, hạn 15:00"]),
             (370, 56, BLUE, BLUEBG, "2. Xếp lịch", ["Ảnh hưởng lớn", "Hạn xa"], ["Học phần mềm mới,", "đặt 2 khung giờ"]),
             (110, 212, ACC, ACCBG, "3. Làm nhanh / hỏi", ["Ảnh hưởng nhỏ", "Hạn gần"], ["In tài liệu họp,", "làm trong 10 phút"]),
             (370, 212, MUTED, "#f1f4f5", "4. Để sau", ["Ảnh hưởng nhỏ", "Hạn xa"], ["Sắp lại thư mục", "chung"])]
    for x, y, col, bg, t, sub, ex in cells:
        b += box(x, y, 240, 140, bg, col, 12, 2)
        b += text(x + 120, y + 28, t, 16, col, weight=800)
        b += lines(x + 120, y + 52, sub, 12, 16, fill=MUTED)
        b += lines(x + 120, y + 100, ex, 13, 17, fill=INK)
    b += lines(60, 140, ["Ảnh", "hưởng", "lớn"], 12, 15, fill=BRAND, weight=700)
    b += lines(60, 296, ["Ảnh", "hưởng", "nhỏ"], 12, 15, fill=BRAND, weight=700)
    b += text(230, 378, "Hạn gần", 13, BRAND, weight=700) + text(490, 378, "Hạn xa", 13, BRAND, weight=700)
    return svg(SCENES["l1-ma-tran"][0], b)


@scene("l2-trang-hop", "Trang ghi họp chia ba ô, giả định. Ô Quyết định: chọn mẫu bao bì B. Ô Việc: ai làm gì, hạn khi nào, ba dòng. Ô Câu hỏi còn mở: chờ báo giá in. Bên dưới là tin nhắn tóm tắt gửi nhóm trong 24 giờ để mọi người xác nhận.")
def _():
    b = text(320, 32, "Trang ghi họp: 3 ô", 19, BRAND, weight=800)
    b += box(30, 50, 180, 210, GREENBG, GREEN, 12, 2)
    b += text(120, 76, "Quyết định", 15, GREEN, weight=800)
    b += lines(120, 110, ["Chọn mẫu", "bao bì B", "", "Ra mắt", "tuần 2/12"], 13, 18, fill=INK)
    b += box(230, 50, 230, 210, "#fff", BRAND2, 12, 2)
    b += text(345, 76, "Việc: ai · gì · hạn", 15, BRAND, weight=800)
    rows = [("Lan", "sửa file in", "T4"), ("Tú", "xin 2 báo giá", "T5"), ("Mình", "lịch ra mắt", "T6")]
    for i, (a, g, h) in enumerate(rows):
        y = 112 + i * 44
        b += text(248, y, a, 13, INK, "start", 700) + text(296, y, g, 13, INK, "start") + text(444, y, h, 13, RED, "end", 700)
    b += box(480, 50, 130, 210, ACCBG, ACC, 12, 2)
    b += text(545, 76, "Còn mở", 15, ACC, weight=800)
    b += lines(545, 110, ["Chờ báo giá", "in: ai chốt?"], 13, 18, fill=INK)
    b += box(30, 278, 580, 104, "#fff", BLUE, 12, 2)
    b += text(46, 302, "Tin nhắn tóm tắt (gửi trong 24 giờ)", 14, BLUE, "start", 800)
    b += lines(46, 326, ["Em tóm tắt họp sáng nay: chốt mẫu B, ra mắt tuần 2/12.",
                         "Việc: Lan sửa file (T4), Tú xin báo giá (T5), em làm lịch (T6).",
                         "Anh chị xem có sai hay thiếu gì giúp em nhé."], 12.5, 18, fill=INK, anchor="start")
    return svg(SCENES["l2-trang-hop"][0], b)


@scene("l3-bon-buoc-khach", "Bốn bước xử lý yêu cầu của khách hàng, giả định: nghe hết, xác nhận nhu cầu, đưa phương án và hạn, theo dõi đến khi xong. Bên trái là khách bên ngoài ở cửa hàng điện máy. Bên phải là khách nội bộ, đồng nghiệp phòng kế toán.")
def _():
    b = text(320, 32, "Bốn bước với mọi khách hàng", 19, BRAND, weight=800)
    steps = [("1", "Nghe hết", "Không ngắt lời"), ("2", "Xác nhận", "Tóm tắt nhu cầu"),
             ("3", "Phương án + hạn", "Trong quyền của mình"), ("4", "Theo dõi", "Báo khi xong")]
    for i, (n, t, s) in enumerate(steps):
        x = 30 + i * 152
        b += box(x, 56, 136, 92, "#fff", BRAND2, 12, 2)
        b += f'<circle cx="{x+22}" cy="80" r="13" fill="{BRAND}"/>' + text(x + 22, 85, n, 13, "#fff", weight=800)
        b += text(x + 80, 86, t if len(t) < 12 else "Phương án", 14, INK, weight=800)
        if len(t) >= 12:
            b += text(x + 80, 104, "+ hạn", 14, INK, weight=800)
        b += text(x + 68, 132, s, 11.5, MUTED)
        if i < 3:
            b += arrow(x + 136, 102, x + 150, 102)
    b += box(30, 170, 284, 206, BLUEBG, BLUE, 12, 2)
    b += text(172, 196, "Khách bên ngoài", 15, BLUE, weight=800)
    b += lines(46, 224, ["Khách: \"Máy giặt mới giao", "kêu to, tôi muốn đổi.\"",
                         "Mình: \"Dạ, máy kêu từ lần giặt đầu,", "anh muốn đổi máy, đúng không ạ?\"",
                         "Hẹn kỹ thuật kiểm tra 10:00 mai,", "chiều mai em gọi báo kết quả."], 12, 22, fill=INK, anchor="start")
    b += box(326, 170, 284, 206, GREENBG, GREEN, 12, 2)
    b += text(468, 196, "Khách nội bộ", 15, GREEN, weight=800)
    b += lines(342, 224, ["Kế toán: \"Gửi chị bảng doanh số.\"",
                          "Mình: \"Chị cần tháng nào, theo", "cửa hàng hay theo nhân viên ạ?\"",
                          "\"Tháng 10, theo cửa hàng.\"",
                          "\"Dạ, em gửi file Excel", "trước 16:00 hôm nay ạ.\""], 12, 22, fill=INK, anchor="start")
    return svg(SCENES["l3-bon-buoc-khach"][0], b)


@scene("l4-vi-sao", "Chuỗi năm câu hỏi vì sao, giả định, ở xưởng may. Hiện tượng: lô áo bị trả vì sai cỡ nhãn. Vì sao 1: nhãn cỡ M gắn vào áo cỡ L. Vì sao 2: hai hộp nhãn để cạnh nhau, giống màu. Vì sao 3: kệ nhãn không chia ô theo cỡ. Nguyên nhân gốc: chưa có quy định sắp kệ. Sửa tạm: kiểm lại lô. Sửa gốc: chia ô kệ, dán màu theo cỡ.")
def _():
    b = text(320, 32, "Hỏi \"Vì sao?\" đến nguyên nhân gốc", 19, BRAND, weight=800)
    b += box(30, 50, 580, 40, REDBG, RED, 10, 2)
    b += text(320, 76, "Hiện tượng: lô 300 áo bị trả vì sai nhãn cỡ (giả định)", 14, RED, weight=800)
    whys = ["Vì sao? Nhãn cỡ M bị gắn vào áo cỡ L.",
            "Vì sao? Hai hộp nhãn M và L để cạnh nhau, cùng màu.",
            "Vì sao? Kệ nhãn không chia ô theo cỡ.",
            "Vì sao? Chưa có quy định sắp kệ nhãn."]
    for i, w in enumerate(whys):
        y = 104 + i * 46
        b += box(50 + i * 18, y, 470, 36, "#fff", BRAND2, 8, 1.5)
        b += text(66 + i * 18, y + 23, w, 13, INK, "start")
    b += box(30, 296, 280, 84, ACCBG, ACC, 12, 2)
    b += text(170, 320, "Sửa tạm (ngay hôm nay)", 14, ACC, weight=800)
    b += lines(170, 344, ["Kiểm lại cả lô, thay nhãn sai"], 12.5, 17, fill=INK)
    b += box(330, 296, 280, 84, GREENBG, GREEN, 12, 2)
    b += text(470, 320, "Sửa gốc (để không lặp lại)", 14, GREEN, weight=800)
    b += lines(470, 344, ["Chia ô kệ theo cỡ,", "dán màu khác nhau cho mỗi cỡ"], 12.5, 17, fill=INK)
    return svg(SCENES["l4-vi-sao"][0], b)


@scene("l5-rut-kinh-nghiem", "Bốn bước khi việc không như kế hoạch: báo ngay, khắc phục, rút kinh nghiệm bằng bốn câu hỏi, chia sẻ cách làm mới. Bốn câu hỏi: định làm gì, thực tế ra sao, vì sao khác, lần sau làm gì.")
def _():
    b = text(320, 32, "Khi việc không như kế hoạch", 19, BRAND, weight=800)
    steps = [("Báo ngay", RED, REDBG), ("Khắc phục", ACC, ACCBG), ("Rút kinh nghiệm", BLUE, BLUEBG), ("Chia sẻ", GREEN, GREENBG)]
    for i, (t, col, bg) in enumerate(steps):
        x = 30 + i * 152
        b += box(x, 54, 136, 52, bg, col, 26, 2)
        b += text(x + 68, 86, t, 14, col, weight=800)
        if i < 3:
            b += arrow(x + 136, 80, x + 150, 80)
    b += box(90, 132, 460, 246, "#fff", BLUE, 14, 2)
    b += text(320, 160, "Rút kinh nghiệm: 4 câu hỏi", 16, BLUE, weight=800)
    qs = [("1", "Mình định làm gì?", "Gửi 200 thiệp mời trước thứ Sáu"),
          ("2", "Thực tế ra sao?", "Gửi 180 thiệp, sót 20 khách hàng cũ"),
          ("3", "Vì sao khác?", "Lấy danh sách cũ, chưa có khách mới"),
          ("4", "Lần sau làm gì?", "Hỏi bản danh sách mới nhất trước khi gửi")]
    for i, (n, q, a) in enumerate(qs):
        y = 196 + i * 46
        b += f'<circle cx="122" cy="{y-5}" r="12" fill="{BLUE}"/>' + text(122, y, n, 12, "#fff", weight=800)
        b += text(144, y - 6, q, 13.5, INK, "start", 800)
        b += text(144, y + 12, a + " (giả định)", 12, MUTED, "start")
    return svg(SCENES["l5-rut-kinh-nghiem"][0], b, "#eef3fa")


@scene("l6-ban-do-phoi-hop", "Bản đồ phối hợp của một nhân viên mới ở phòng kinh doanh, giả định. Ở giữa là Mình. Xung quanh là bốn đầu mối: kho, kế toán, chăm sóc khách hàng, trưởng nhóm. Mỗi đầu mối ghi mình cần gì từ họ và họ cần gì từ mình.")
def _():
    b = text(320, 32, "Bản đồ phối hợp", 19, BRAND, weight=800)
    b += f'<circle cx="320" cy="214" r="46" fill="{BRAND}"/>' + lines(320, 210, ["Mình", "(kinh doanh)"], 13, 17, fill="#fff", weight=800)
    nodes = [(40, 56, "Kho", "Cần: số tồn kho trước 9:00", "Họ cần: đơn đủ mã hàng"),
             (380, 56, "Kế toán", "Cần: xác nhận đã nhận tiền", "Họ cần: hóa đơn đúng hạn"),
             (40, 284, "Chăm sóc khách hàng", "Cần: ghi chú khách khó", "Họ cần: hẹn giao chính xác"),
             (380, 284, "Trưởng nhóm", "Cần: ưu tiên khi trùng việc", "Họ cần: báo sớm khi chậm")]
    for x, y, t, need, give in nodes:
        b += box(x, y, 220, 92, "#fff", BRAND2, 12, 2)
        b += text(x + 110, y + 24, t, 14, BRAND, weight=800)
        b += text(x + 14, y + 50, need, 12, INK, "start")
        b += text(x + 14, y + 74, give, 12, ACC, "start", 700)
        cx, cy = x + 110, (y + 92 if y < 200 else y)
        b += f'<line x1="{cx}" y1="{cy}" x2="320" y2="214" stroke="{BRAND2}" stroke-width="1.5" stroke-dasharray="5 4"/>'
    b += f'<circle cx="320" cy="214" r="46" fill="{BRAND}"/>' + lines(320, 210, ["Mình", "(kinh doanh)"], 13, 17, fill="#fff", weight=800)
    return svg(SCENES["l6-ban-do-phoi-hop"][0], b)


@scene("l7-ho-so-danh-gia", "Hồ sơ cho buổi đánh giá 90 ngày, giả định. Bên trái là sáu tờ của Sổ tay 90 ngày. Mũi tên dẫn sang bên phải: ba ví dụ STAR có số liệu, bảng tự đánh giá Tôi có thể, hai câu hỏi cho cấp trên, ba mục tiêu cho 90 ngày tới.")
def _():
    b = text(320, 32, "Từ Sổ tay 90 ngày đến buổi đánh giá", 19, BRAND, weight=800)
    tờ = ["1 Bảng việc tuần", "2 Trang ghi họp", "3 Phiếu yêu cầu", "4 Phiếu sự cố", "5 Phiếu rút kinh nghiệm", "6 Bản đồ phối hợp"]
    for i, t in enumerate(tờ):
        y = 56 + i * 52
        b += box(30 + i * 4, y, 230, 42, "#fff", BRAND2, 8, 1.5)
        b += text(46 + i * 4, y + 26, "Tờ " + t, 13, INK, "start", 700)
    b += arrow(280, 214, 330, 214, ACC)
    b += box(340, 56, 270, 320, ACCBG, ACC, 14, 2)
    b += text(475, 84, "Mang vào buổi đánh giá", 15, ACC, weight=800)
    items = ["3 ví dụ STAR có số liệu", "Bảng tự đánh giá \"Tôi có thể…\"", "1 điểm mạnh, 1 điểm cần tiến bộ",
             "2 câu hỏi cho cấp trên", "3 mục tiêu cho 90 ngày tới"]
    for i, t in enumerate(items):
        y = 124 + i * 50
        b += f'<rect x="358" y="{y-14}" width="16" height="16" rx="3" fill="#fff" stroke="{ACC}" stroke-width="2"/>'
        b += text(384, y, t, 13, INK, "start")
    return svg(SCENES["l7-ho-so-danh-gia"][0], b, "#fdf3e2")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (title, fn) in SCENES.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print(f"Đã vẽ {len(SCENES)} hình vào {OUT}")
