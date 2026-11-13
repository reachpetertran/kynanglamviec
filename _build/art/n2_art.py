#!/usr/bin/env python3
"""Hình minh họa tự vẽ (SVG) cho khóa N2 "Chuẩn bị đi làm". Không dùng ảnh ngoài.
Chạy: python3 _build/art/n2_art.py  -> _build/static/assets/img/n2/*.svg
Mọi tên người, quán, công ty trong hình là giả định.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parents[1] / "static/assets/img/n2"
W, H = 640, 400
BRAND, BRAND2, ACC, ACCBG, INK, MUTED = "#14524f", "#1f7a74", "#d98a1c", "#fdf3e2", "#1d2a33", "#5b6b73"
RED, REDBG, GREEN, GREENBG, BLUE, BLUEBG = "#b03a2e", "#fbe9e7", "#1e7d4f", "#e6f4ec", "#2563a8", "#e8f0fa"
FONT = 'font-family="system-ui,-apple-system,Segoe UI,Roboto,Noto Sans,Arial,sans-serif"'
SCENES = {}


def scene(name, title):
    def deco(fn):
        SCENES[name] = (title, fn)
        return fn
    return deco


def svg(title, body, bg="#eef6f5"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)}</title><rect width="{W}" height="{H}" rx="18" fill="{bg}"/>{body}</svg>')


def text(x, y, s, size=14, fill=INK, anchor="middle", weight=400):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" {FONT}>{escape(s)}</text>')


def lines(x, y, rows, size=13, gap=17, **kw):
    return "".join(text(x, y + i * gap, r, size, **kw) for i, r in enumerate(rows))


def box(x, y, w, h, fill="#fff", stroke="#9fb9b6", rx=10, sw=1.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def bar(x, y, w, fill="#c9d6d4", h=7):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}"/>'


@scene("l1-ba-vong", "Ba vòng tròn giao nhau: điều mình thích làm, điều mình làm được có bằng chứng, điều kiện thật của mình. Phần giao ở giữa là hướng để thử.")
def _():
    b = text(320, 34, "Ba vòng để chọn hướng thử", 20, BRAND, weight=800)
    b += f'<circle cx="250" cy="170" r="105" fill="{ACC}" fill-opacity=".22" stroke="{ACC}" stroke-width="2"/>'
    b += f'<circle cx="390" cy="170" r="105" fill="{BRAND2}" fill-opacity=".2" stroke="{BRAND2}" stroke-width="2"/>'
    b += f'<circle cx="320" cy="280" r="105" fill="{BLUE}" fill-opacity=".16" stroke="{BLUE}" stroke-width="2"/>'
    b += lines(215, 112, ["Mình thích làm", "việc gì?"], 14, 18, fill=INK, weight=700)
    b += lines(212, 152, ["Làm lâu", "không thấy chán"], 12, 16, fill=MUTED)
    b += lines(425, 112, ["Mình làm được", "việc gì?"], 14, 18, fill=INK, weight=700)
    b += lines(428, 152, ["Có bằng chứng:", "sản phẩm, điểm số"], 12, 16, fill=MUTED)
    b += lines(320, 325, ["Điều kiện thật"], 14, 18, fill=INK, weight=700)
    b += lines(320, 345, ["Thời gian, đi lại, chi phí,", "nơi đang cần người"], 12, 16, fill=MUTED)
    b += f'<circle cx="320" cy="210" r="34" fill="#fff" stroke="{BRAND}" stroke-width="2.5"/>'
    b += lines(320, 206, ["Hướng", "để thử"], 13, 16, fill=BRAND, weight=800)
    return svg(SCENES["l1-ba-vong"][0], b)


@scene("l2-hai-tin", "Hai tin tuyển dụng giả định đặt cạnh nhau. Tin bên trái ghi rõ việc, ca, lương, địa chỉ. Tin bên phải có ba dấu hiệu cần dừng lại: lương rất cao mà không nói rõ việc, thu phí đồng phục, nộp bản gốc căn cước.")
def _():
    b = text(320, 32, "Hai tin tuyển dụng (giả định)", 19, BRAND, weight=800)
    # tin rõ
    b += box(24, 50, 286, 328, "#fff", GREEN, 12, 2)
    b += f'<rect x="24" y="50" width="286" height="34" rx="12" fill="{GREENBG}"/>'
    b += text(167, 73, "Tin A · Rõ ràng", 15, GREEN, weight=800)
    rowsA = [("Việc:", "phục vụ, dọn bàn, nhận order"), ("Ca:", "18:00–22:00, chọn 3 ca/tuần"),
             ("Lương:", "ghi rõ theo giờ, trả hằng tháng"), ("Yêu cầu:", "đủ 18 tuổi, biết đi xe máy"),
             ("Ưu tiên:", "đã từng phục vụ"), ("Địa chỉ:", "số nhà, tên đường, quận"),
             ("Liên hệ:", "quản lý quán, giờ hành chính")]
    for i, (k, v) in enumerate(rowsA):
        y = 112 + i * 34
        b += text(40, y, k, 13, INK, "start", 700) + text(112, y, v, 13, INK, "start")
    b += f'<rect x="104" y="{112+3*34-15}" width="198" height="22" rx="5" fill="none" stroke="{GREEN}" stroke-dasharray="4 3"/>'
    b += text(167, 366, "Bắt buộc và ưu tiên tách riêng", 12, GREEN, weight=700)
    # tin đáng ngờ
    b += box(330, 50, 286, 328, "#fff", RED, 12, 2)
    b += f'<rect x="330" y="50" width="286" height="34" rx="12" fill="{REDBG}"/>'
    b += text(473, 73, "Tin B · Cần dừng lại", 15, RED, weight=800)
    rowsB = [("Việc:", "\"việc nhẹ, làm tại nhà\""), ("Lương:", "\"thu nhập rất cao\""),
             ("Yêu cầu:", "không cần kinh nghiệm"), ("Thủ tục:", "nộp 500.000 đ đồng phục"),
             ("", "nộp bản gốc căn cước"), ("Liên hệ:", "chỉ nhắn tin, không địa chỉ")]
    for i, (k, v) in enumerate(rowsB):
        y = 112 + i * 38
        b += text(346, y, k, 13, INK, "start", 700) + text(416, y, v, 12.5, INK, "start")
    for i, y in enumerate((112, 150, 226, 264, 302)):
        b += f'<circle cx="604" cy="{y-5}" r="8" fill="{RED}"/>' + text(600, y - 1, "!", 13, "#fff", weight=800)
    b += text(473, 366, "Mập mờ · thu tiền · giữ giấy tờ gốc", 12, RED, weight=700)
    return svg(SCENES["l2-hai-tin"][0], b, "#f4f7f6")


@scene("l3-cv", "Khung CV một trang gồm 5 phần từ trên xuống: thông tin liên hệ, mục tiêu hai dòng, học vấn, hoạt động và kinh nghiệm viết theo công thức động từ cộng việc cộng kết quả, kỹ năng có bằng chứng.")
def _():
    b = box(150, 18, 340, 366, "#fff", "#9fb9b6", 6)
    parts = [("1", "Liên hệ", 34, 44), ("2", "Mục tiêu (2 dòng)", 86, 40), ("3", "Học vấn", 134, 44),
             ("4", "Hoạt động, kinh nghiệm", 186, 120), ("5", "Kỹ năng có bằng chứng", 314, 58)]
    for n, name, y, h in parts:
        hi = n == "4"
        b += f'<rect x="164" y="{y}" width="312" height="{h}" rx="6" fill="{ACCBG if hi else "#f2f7f6"}" stroke="{ACC if hi else "#d5e2e0"}"/>'
        b += f'<circle cx="180" cy="{y+14}" r="9" fill="{BRAND}"/>' + text(180, y + 18, n, 11, "#fff", weight=800)
        b += text(196, y + 18, name, 12.5, BRAND, "start", 700)
        rows = max(1, (h - 26) // 14)
        for r in range(rows):
            b += bar(196, y + 26 + r * 14, 250 - (r % 3) * 50)
    b += text(320, 216, "", 1)
    # chú thích công thức
    b += box(498, 196, 132, 96, "#fff", ACC, 10, 2)
    b += lines(564, 218, ["Mỗi dòng:", "Động từ", "+ việc", "+ kết quả, con số"], 12, 18, fill=INK, weight=700)
    b += f'<path d="M498,244 L478,244" stroke="{ACC}" stroke-width="2"/>'
    b += box(10, 36, 132, 70, "#fff", BRAND2, 10, 1.5)
    b += lines(76, 58, ["Email tên thật,", "số điện thoại,", "quận/huyện"], 12, 16, fill=INK)
    b += f'<path d="M142,56 L164,56" stroke="{BRAND2}" stroke-width="2"/>'
    b += box(10, 300, 132, 70, "#fff", RED, 10, 1.5)
    b += lines(76, 322, ["Không ghi số", "căn cước, địa chỉ", "nhà chi tiết"], 12, 16, fill=RED)
    return svg(SCENES["l3-cv"][0], b)


@scene("l4-truoc-trong-sau", "Dòng thời gian buổi phỏng vấn. Trước: tìm hiểu nơi tuyển, luyện giới thiệu 60 giây, chuẩn bị một ví dụ STAR, hai câu hỏi ngược, báo người nhà nơi đến. Trong: đến sớm 10 phút, nghe hết câu hỏi, hỏi lại khi chưa rõ. Sau: nhắn cảm ơn trong 24 giờ, ghi lại câu hỏi đã gặp.")
def _():
    b = text(320, 34, "Phỏng vấn: trước · trong · sau", 20, BRAND, weight=800)
    b += f'<path d="M40,80 L600,80" stroke="{BRAND2}" stroke-width="4"/>'
    cols = [("Trước", ACC, ["Tìm hiểu nơi tuyển", "Giới thiệu 60 giây", "1–2 ví dụ STAR", "2 câu hỏi ngược",
                            "Báo nhà nơi sẽ đến"]),
            ("Trong", BRAND2, ["Đến sớm 10 phút", "Nghe hết câu hỏi", "Chưa rõ thì hỏi lại", "Trả lời có ví dụ",
                              "Hỏi bước tiếp theo"]),
            ("Sau", BLUE, ["Cảm ơn trong 24 giờ", "Ghi câu hỏi đã gặp", "Ghi điều làm tốt",
                           "Ghi một điều sửa", "Đọc kỹ đề nghị việc"])]
    for i, (name, col, items) in enumerate(cols):
        x = 30 + i * 200
        b += f'<circle cx="{x+90}" cy="80" r="16" fill="{col}"/>'
        b += box(x, 108, 180, 260, "#fff", col, 12, 2)
        b += text(x + 90, 136, name, 17, col, weight=800)
        for j, it in enumerate(items):
            y = 172 + j * 40
            b += f'<rect x="{x+14}" y="{y-12}" width="14" height="14" rx="3" fill="none" stroke="{col}" stroke-width="2"/>'
            b += text(x + 36, y, it, 12.5, INK, "start")
    return svg(SCENES["l4-truoc-trong-sau"][0], b)


@scene("l5-tin-nhan", "Hai màn hình điện thoại. Bên trái tin nhắn mơ hồ: chị ơi, em có chút việc. Bên phải tin nhắn rõ: em chào chị, em là Linh ca tối thứ Sáu, em bị sốt nên xin nghỉ ca này, em đã hỏi bạn Tú làm thay, chị đồng ý giúp em nhé.")
def _():
    b = ""
    for i, (title, col, bg) in enumerate((("Mơ hồ", RED, REDBG), ("Rõ, đủ ý", GREEN, GREENBG))):
        x = 70 + i * 290
        b += box(x, 22, 210, 356, "#1d2a33", "#1d2a33", 26)
        b += box(x + 10, 46, 190, 306, "#f5f7f8", "#f5f7f8", 14)
        b += f'<rect x="{x+10}" y="46" width="190" height="34" rx="14" fill="{bg}"/>'
        b += text(x + 105, 68, title, 14, col, weight=800)
    # trái
    b += box(86, 100, 150, 44, "#fff", "#cfd8dc", 12)
    b += lines(161, 118, ["Chị ơi", "em có chút việc ạ"], 12.5, 17)
    b += box(160, 160, 120, 30, "#dff1ef", "#dff1ef", 12) + text(220, 180, "Việc gì em?", 12.5)
    b += box(86, 206, 120, 30, "#fff", "#cfd8dc", 12) + text(146, 226, "Tối nay ạ", 12.5)
    b += box(160, 252, 120, 30, "#dff1ef", "#dff1ef", 12) + text(220, 272, "Tối nay sao em?", 12.5)
    b += text(175, 330, "Phải hỏi lại 2 lần", 12.5, RED, weight=700)
    # phải
    b += box(376, 96, 176, 196, "#fff", "#cfd8dc", 12)
    b += lines(388, 116, ["Em chào chị, em là Linh,", "ca tối thứ Sáu.", "Em bị sốt nên xin nghỉ",
                          "ca 18:00–22:00 hôm nay.", "Em đã hỏi bạn Tú,", "bạn ấy làm thay được.",
                          "Chị đồng ý giúp em nhé.", "Em cảm ơn chị."], 12, 21, anchor="start")
    b += box(440, 302, 104, 30, "#dff1ef", "#dff1ef", 12) + text(492, 322, "Ok em, nghỉ đi", 12.5)
    b += text(465, 346, "Ai · việc gì · cần gì", 12, GREEN, weight=700)
    return svg(SCENES["l5-tin-nhan"][0], b, "#eef6f5")


@scene("l6-so-quy-trinh", "Một trang sổ quy trình viết tay: tên việc pha trà đào cam sả, các bước đánh số, ô lỗi hay gặp, và ba ô ôn lại sau 1 ngày, 3 ngày, 7 ngày, đã đánh dấu hai ô.")
def _():
    b = box(120, 20, 400, 360, "#fffdf6", "#d8cfae", 8)
    for i in range(14):
        b += f'<path d="M140,{78+i*22} L500,{78+i*22}" stroke="#e9e1c7"/>'
    b += f'<path d="M170,20 L170,380" stroke="#e7b3a9" stroke-width="1.5"/>'
    b += text(184, 54, "Quy trình: Pha trà đào cam sả (giả định)", 15, BRAND, "start", 800)
    steps = ["1. Rửa tay, lấy ly size M", "2. Cho 30 ml syrup đào", "3. Thêm trà đến vạch 2",
             "4. Cho đá đến vạch 3, lắc 10 lần", "5. Thêm đào miếng, cam, sả", "6. Đóng nắp, dán tem giờ"]
    for i, st in enumerate(steps):
        b += text(184, 96 + i * 22, st, 13.5, INK, "start")
    b += box(184, 236, 300, 64, REDBG, RED, 8)
    b += text(196, 256, "Lỗi hay gặp", 13, RED, "start", 800)
    b += lines(196, 276, ["Quên lắc → trà nhạt phía dưới", "Đá trước syrup → syrup không tan"], 12.5, 18, anchor="start")
    b += text(184, 330, "Ôn không nhìn sổ:", 13, BRAND, "start", 700)
    for i, (lab, done) in enumerate((("1 ngày", True), ("3 ngày", True), ("7 ngày", False))):
        x = 312 + i * 66
        b += f'<rect x="{x}" y="316" width="18" height="18" rx="3" fill="#fff" stroke="{BRAND}" stroke-width="2"/>'
        if done:
            b += f'<path d="M{x+3},{325} l5,5 l8,-10" fill="none" stroke="{GREEN}" stroke-width="3"/>'
        b += text(x + 24, 330, lab, 12, INK, "start")
    return svg(SCENES["l6-so-quy-trinh"][0], b)


@scene("l7-ho-so", "Bìa hồ sơ Hồ sơ sẵn sàng đi làm với 6 tờ chìa ra: bản đồ hướng đi, phiếu đọc tin, CV một trang, phiếu phỏng vấn, sổ tay tuần đầu, sổ quy trình. Bên cạnh là bảng kiểm chéo cùng một người bạn.")
def _():
    b = text(320, 32, "Hồ sơ sẵn sàng đi làm", 20, BRAND, weight=800)
    tabs = [("1", "Bản đồ hướng đi", ACC), ("2", "Phiếu đọc tin", RED), ("3", "CV một trang", BRAND2),
            ("4", "Phiếu phỏng vấn", BLUE), ("5", "Sổ tay tuần đầu", "#8e44ad"), ("6", "Sổ quy trình", GREEN)]
    for i, (n, name, col) in enumerate(tabs):
        y = 62 + i * 44
        b += f'<rect x="{60+i*6}" y="{y}" width="300" height="40" rx="6" fill="#fff" stroke="{col}" stroke-width="2"/>'
        b += f'<circle cx="{84+i*6}" cy="{y+20}" r="11" fill="{col}"/>' + text(84 + i * 6, y + 25, n, 12, "#fff", weight=800)
        b += text(104 + i * 6, y + 25, name, 14, INK, "start", 700)
    b += f'<rect x="40" y="330" width="360" height="44" rx="8" fill="{BRAND}"/>'
    b += text(220, 357, "Bìa hồ sơ", 15, "#fff", weight=700)
    b += box(420, 70, 200, 290, "#fff", BRAND2, 12, 2)
    b += text(520, 98, "Kiểm chéo với bạn", 15, BRAND, weight=800)
    checks = ["Đủ 6 tờ", "CV khớp 1 tin cụ thể", "Mỗi dòng CV kể được", "bằng một ví dụ",
              "Giới thiệu ≤ 60 giây", "Có 2 câu hỏi ngược", "Có lịch ôn 1–3–7"]
    y = 128
    for c in checks:
        sub = c in ("bằng một ví dụ",)
        if not sub:
            b += f'<rect x="436" y="{y-12}" width="14" height="14" rx="3" fill="none" stroke="{BRAND2}" stroke-width="2"/>'
        b += text(458, y, c, 12.5, INK, "start")
        y += 26 if not c.endswith("kể được") else 18
    return svg(SCENES["l7-ho-so"][0], b, "#fdf3e2")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (title, fn) in SCENES.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print(f"Đã vẽ {len(SCENES)} hình vào {OUT}")
