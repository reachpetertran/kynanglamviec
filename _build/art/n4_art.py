#!/usr/bin/env python3
"""Hình minh họa tự vẽ (SVG) cho khóa N4 "Senior, chuyên gia". Không dùng ảnh ngoài.
Chạy: python3 _build/art/n4_art.py  -> _build/static/assets/img/n4/*.svg
Mọi tên người, nơi làm việc, số liệu trong hình là giả định, trừ Hình 7 (mốc thời gian
của Nghị định 283/2026/NĐ-CP, đối chiếu Điều 66, 67 văn bản gốc).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n2_art import (svg, text, lines, box, BRAND, BRAND2, ACC, ACCBG, INK, MUTED,  # noqa: E402
                    RED, REDBG, GREEN, GREENBG, BLUE, BLUEBG)

OUT = Path(__file__).resolve().parents[1] / "static/assets/img/n4"
SCENES = {}


def scene(name, title):
    def deco(fn):
        SCENES[name] = (title, fn)
        return fn
    return deco


def arrow(x1, y1, x2, y2, col=BRAND2, sw=2.5):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}"/>'
            f'<circle cx="{x2}" cy="{y2}" r="4.5" fill="{col}"/>')


def sign(x, y, s, col):
    return (f'<circle cx="{x}" cy="{y}" r="11" fill="#fff" stroke="{col}" stroke-width="2"/>'
            + text(x, y + 5, s, 15, col, weight=800))


@scene("l1-so-do-tac-dong", "Sơ đồ tác động, giả định, ở tổng đài chăm sóc khách hàng. Chỉ tiêu thời gian mỗi cuộc gọi dưới 3 phút làm nhân viên kết thúc cuộc gọi sớm. Vấn đề của khách chưa được giải quyết, khách gọi lại, số cuộc gọi tăng, thời gian chờ tăng. Quản lý siết chỉ tiêu hơn, vòng lặp quay lại.")
def _():
    b = text(320, 32, "Vòng lặp: sửa một ô, cả vòng xấu đi", 19, BRAND, weight=800)
    nodes = [(320, 80, "Siết chỉ tiêu", "< 3 phút/cuộc gọi", RED, REDBG),
             (520, 160, "Kết thúc", "cuộc gọi sớm", ACC, ACCBG),
             (470, 300, "Khách gọi lại", "38% cuộc gọi", ACC, ACCBG),
             (170, 300, "Thời gian chờ", "2 → 6 phút", RED, REDBG),
             (120, 160, "Quản lý lo", "chậm, siết thêm", BLUE, BLUEBG)]
    for x, y, t, s, col, bg in nodes:
        b += box(x - 80, y - 30, 160, 60, bg, col, 12, 2)
        b += text(x, y - 6, t, 14, col, weight=800) + text(x, y + 16, s, 12, INK)
    pairs = [((400, 95), (470, 130)), ((520, 190), (490, 270)), ((390, 305), (250, 305)),
             ((150, 270), (125, 190)), ((150, 130), (240, 92))]
    for (x1, y1), (x2, y2) in pairs:
        b += arrow(x1, y1, x2, y2)
    for (x, y) in [(455, 100), (520, 232), (320, 290), (122, 232), (190, 100)]:
        b += sign(x, y, "+", BRAND2)
    b += f'<circle cx="320" cy="200" r="42" fill="#fff" stroke="{BRAND}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    b += lines(320, 196, ["Vòng", "tự lớn dần"], 13, 17, fill=BRAND, weight=800)
    b += box(150, 350, 340, 36, GREENBG, GREEN, 10, 2)
    b += text(320, 374, "Điểm đòn bẩy: đo \"giải quyết ngay lần đầu\"", 13, GREEN, weight=800)
    return svg(SCENES["l1-so-do-tac-dong"][0], b)


@scene("l2-hai-loai-quyet-dinh", "Hai loại quyết định, giả định. Cửa quay lại được: thử mẫu báo cáo mới, đổi giờ họp. Quyết nhanh, thử nhỏ, đo lại. Cửa khó quay lại: ký hợp đồng nhà cung cấp 3 năm, thay hóa chất trên dây chuyền. Cần thêm dữ liệu, người duyệt và phương án dự phòng.")
def _():
    b = text(320, 32, "Quyết định có quay lại được không?", 19, BRAND, weight=800)
    for x, col, bg, t, ex, act in [
            (30, GREEN, GREENBG, "Cửa quay lại được", ["Thử mẫu báo cáo mới", "Đổi giờ họp nhóm", "Đoạn mã thay thế tạm"],
             ["Quyết nhanh", "Thử nhỏ", "Đo lại, đổi nếu cần"]),
            (330, RED, REDBG, "Cửa khó quay lại", ["Ký hợp đồng 3 năm", "Thay hóa chất dây chuyền", "Tuyển, cho nghỉ việc"],
             ["Thêm dữ liệu", "Người có quyền duyệt", "Phương án dự phòng"])]:
        b += box(x, 54, 280, 326, bg, col, 14, 2)
        b += f'<rect x="{x + 100}" y="74" width="80" height="110" rx="6" fill="#fff" stroke="{col}" stroke-width="2.5"/>'
        b += f'<circle cx="{x + 166}" cy="132" r="5" fill="{col}"/>'
        if col == GREEN:
            b += f'<path d="M{x + 60} 130 q -18 -30 0 -50" fill="none" stroke="{col}" stroke-width="2.5"/>'
            b += f'<path d="M{x + 220} 130 q 18 -30 0 -50" fill="none" stroke="{col}" stroke-width="2.5"/>'
        else:
            b += f'<line x1="{x + 70}" y1="190" x2="{x + 210}" y2="190" stroke="{col}" stroke-width="3"/>'
        b += text(x + 140, 216, t, 16, col, weight=800)
        b += lines(x + 140, 242, ex, 12.5, 18, fill=INK)
        for i, a in enumerate(act):
            y = 312 + i * 22
            b += f'<circle cx="{x + 60}" cy="{y - 4}" r="5" fill="{col}"/>' + text(x + 74, y, a, 13, INK, "start", 700)
    return svg(SCENES["l2-hai-loai-quyet-dinh"][0], b)


@scene("l3-ban-do-cac-ben", "Bản đồ các bên liên quan, giả định, cho đề xuất quét mã vạch ở kho. Trục dọc là ảnh hưởng tới quyết định, trục ngang là mức bị tác động. Giám đốc vận hành: ảnh hưởng cao, cần đề xuất một trang. Tổ trưởng kho: ảnh hưởng cao, bị tác động nhiều, gặp riêng trước. Kế toán: cần số liệu chi phí. Nhân viên kho ca đêm: bị tác động nhiều, cần hướng dẫn.")
def _():
    b = text(320, 30, "Bản đồ các bên: gặp ai trước, nói gì", 19, BRAND, weight=800)
    b += box(90, 48, 520, 300, "#fff", "#9fb9b6", 12, 1.5)
    b += f'<line x1="350" y1="48" x2="350" y2="348" stroke="#c9d6d4" stroke-width="1.5"/>'
    b += f'<line x1="90" y1="198" x2="610" y2="198" stroke="#c9d6d4" stroke-width="1.5"/>'
    b += lines(52, 110, ["Ảnh", "hưởng", "cao"], 12, 15, fill=BRAND, weight=700)
    b += lines(52, 262, ["Ảnh", "hưởng", "thấp"], 12, 15, fill=BRAND, weight=700)
    b += text(220, 372, "Bị tác động ít", 13, BRAND, weight=700) + text(480, 372, "Bị tác động nhiều", 13, BRAND, weight=700)
    people = [(110, 70, BLUE, BLUEBG, "Giám đốc vận hành", ["Quyết. Cần đề xuất", "một trang, có số liệu"]),
              (370, 70, RED, REDBG, "Tổ trưởng kho", ["Có thể cản. Lo xe chờ.", "Gặp riêng trước!"]),
              (110, 220, MUTED, "#f1f4f5", "Kế toán", ["Cần chi phí máy quét", "và tiền sai lệch/tháng"]),
              (370, 220, ACC, ACCBG, "Nhân viên kho ca đêm", ["Làm thay đổi hằng ngày.", "Cần hướng dẫn, thử sau"])]
    for x, y, col, bg, t, note in people:
        b += box(x, y, 220, 104, bg, col, 12, 2)
        b += f'<circle cx="{x + 26}" cy="{y + 28}" r="12" fill="{col}"/>'
        b += text(x + 46, y + 33, t, 14, col, "start", 800)
        b += lines(x + 110, y + 66, note, 12.5, 18, fill=INK)
    return svg(SCENES["l3-ban-do-cac-ben"][0], b)


@scene("l4-bon-buoc", "Bốn bước gỡ bất đồng, giả định, giữa kỹ sư thiết kế và kỹ sư sản xuất. Bước 1 sự kiện: 6 trên 200 chi tiết lệch dung sai. Bước 2 diễn giải: thiết kế cho rằng máy cũ, sản xuất cho rằng dung sai quá chặt. Bước 3 tiêu chí chung: lắp ráp được, không tăng chi phí. Bước 4 thử: đo 50 chi tiết trên máy khác.")
def _():
    b = text(320, 30, "Gỡ bất đồng: từ sự kiện đến thử nghiệm", 19, BRAND, weight=800)
    steps = [("1. Sự kiện chung", GREEN, GREENBG, ["6/200 chi tiết lệch dung sai", "Hai bên cùng công nhận"]),
             ("2. Diễn giải mỗi bên", ACC, ACCBG, ["Thảo (thiết kế): máy cũ", "Hưng (sản xuất): dung sai chặt"]),
             ("3. Tiêu chí chung", BLUE, BLUEBG, ["① Lắp ráp được", "② Không tăng chi phí"]),
             ("4. Thử nghiệm", BRAND, "#e3f0ee", ["50 chi tiết, máy khác", "Hai bên cùng đo, hạn thứ Năm"])]
    for i, (t, col, bg, rows) in enumerate(steps):
        y = 48 + i * 86
        x = 30 + i * 32
        b += box(x, y, 360, 74, bg, col, 12, 2)
        b += text(x + 16, y + 24, t, 15, col, "start", 800)
        b += text(x + 16, y + 46, rows[0], 13, INK, "start")
        b += text(x + 16, y + 65, rows[1], 12.5, MUTED, "start")
        if i < 3:
            b += arrow(x + 180, y + 74, x + 212, y + 86, col)
    b += box(500, 50, 120, 150, "#fff", ACC, 12, 2)
    b += lines(560, 76, ["Trước khi", "trả lời:"], 13, 17, fill=ACC, weight=800)
    b += lines(560, 122, ["Nhắc lại ý", "người kia.", "\"Tôi hiểu", "đúng chưa?\""], 12.5, 17, fill=INK)
    return svg(SCENES["l4-bon-buoc"][0], b)


@scene("l5-bon-nac", "Bốn nấc giao việc khi kèm cặp, giả định, cho việc lập báo giá. Nấc 1 làm mẫu: tuần 1. Nấc 2 làm cùng: tuần 2 đến 3. Nấc 3 quan sát: tuần 4 đến 6, xem trước khi gửi khách. Nấc 4 tự làm: từ tuần 7, báo lại sau khi gửi. Người kèm lùi lại khi người được kèm tiến lên.")
def _():
    b = text(320, 30, "Bốn nấc giao việc khi kèm cặp", 19, BRAND, weight=800)
    steps = [("1. Làm mẫu", "Mình làm, bạn xem", "Tuần 1", MUTED),
             ("2. Làm cùng", "Bạn làm, mình bên cạnh", "Tuần 2–3", BLUE),
             ("3. Quan sát", "Bạn làm, mình xem trước", "Tuần 4–6", ACC),
             ("4. Tự làm", "Bạn làm, báo lại sau", "Từ tuần 7", GREEN)]
    for i, (t, s, w, col) in enumerate(steps):
        x = 40 + i * 145
        h = 80 + i * 60
        y = 360 - h
        b += f'<rect x="{x}" y="{y}" width="135" height="{h}" rx="8" fill="#fff" stroke="{col}" stroke-width="2.5"/>'
        b += text(x + 67, y + 26, t, 15, col, weight=800)
        b += text(x + 67, y + 48, s, 11.5, INK)
        b += text(x + 67, y + 68, w, 12, MUTED, weight=700)
    b += text(40, 76, "Người được kèm: tiến lên từng nấc", 13, ACC, "start", 800)
    b += text(40, 98, "Người kèm: lùi lại từng bước", 13, BRAND, "start", 800)
    b += text(320, 388, "Việc mẫu: lập báo giá cho khách vừa (giả định)", 12, MUTED)
    return svg(SCENES["l5-bon-nac"][0], b)


@scene("l6-mot-trang", "Một trang dự án, giả định, cho dự án giao hàng nội thành trong một ngày. Sáu ô: mục tiêu, phạm vi làm và không làm, bốn mốc, vai trò, phụ thuộc vào phòng IT, ba rủi ro. Bên dưới là dải tiến độ các mốc: mốc 1 xong màu xanh, mốc 2 trễ màu cam.")
def _():
    b = text(320, 28, "Một trang dự án (giả định)", 19, BRAND, weight=800)
    cells = [(30, 44, BRAND, "Mục tiêu", ["80% đơn nội thành giao", "trong 1 ngày, trước 31/3"]),
             (230, 44, BLUE, "Phạm vi", ["Làm: đơn nội thành", "Không làm: đơn tỉnh"]),
             (430, 44, ACC, "Mốc", ["1 Quy trình hiện tại", "2 Kho xong trước 11h"]),
             (30, 160, BRAND2, "Vai trò", ["Mỗi việc 1 người", "chịu trách nhiệm"]),
             (230, 160, RED, "Phụ thuộc", ["Phòng IT đổi giờ chốt", "đơn, hạn tuần 3"]),
             (430, 160, MUTED, "Rủi ro", ["IT trễ · Xe thiếu", "· Kho quá tải"])]
    for x, y, col, t, rows in cells:
        b += box(x, y, 180, 100, "#fff", col, 10, 2)
        b += text(x + 14, y + 26, t, 15, col, "start", 800)
        b += lines(x + 14, y + 54, rows, 12.5, 18, fill=INK, anchor="start")
    b += text(30, 300, "Dải mốc", 14, BRAND, "start", 800)
    marks = [("Mốc 1", GREEN, "Xong"), ("Mốc 2", ACC, "Có rủi ro"), ("Mốc 3", "#c9d6d4", "Chưa đến"), ("Mốc 4", "#c9d6d4", "Chưa đến")]
    for i, (m, col, s) in enumerate(marks):
        x = 30 + i * 148
        b += f'<rect x="{x}" y="312" width="140" height="30" rx="6" fill="{col}"/>'
        b += text(x + 70, 332, m, 13, "#fff" if col != "#c9d6d4" else INK, weight=800)
        b += text(x + 70, 362, s, 12, MUTED)
    return svg(SCENES["l6-mot-trang"][0], b)


@scene("l7-dong-thoi-gian", "Dòng thời gian của Nghị định 283/2026/NĐ-CP. Ngày 15/7/2026: Chính phủ ký ban hành. Ngày 10/9/2026: có hiệu lực, Nghị định 12/2022/NĐ-CP hết hiệu lực. Hành vi đã xảy ra và kết thúc trước 10/9/2026 thì áp dụng văn bản có hiệu lực lúc đó. Hành vi vẫn đang diễn ra sau 10/9/2026 thì áp dụng Nghị định 283.")
def _():
    b = text(320, 30, "Ba mốc khi đọc một văn bản mới", 19, BRAND, weight=800)
    b += text(320, 52, "Ví dụ thật: Nghị định 283/2026/NĐ-CP (Điều 66, 67)", 13, MUTED)
    b += f'<line x1="40" y1="160" x2="600" y2="160" stroke="{BRAND}" stroke-width="4"/>'
    b += f'<rect x="40" y="148" width="300" height="24" rx="4" fill="{MUTED}" fill-opacity=".25"/>'
    b += f'<rect x="340" y="148" width="260" height="24" rx="4" fill="{BRAND2}" fill-opacity=".3"/>'
    b += text(190, 140, "Nghị định 12/2022 còn áp dụng", 12.5, INK, weight=700)
    b += text(470, 140, "Nghị định 283/2026 áp dụng", 12.5, BRAND, weight=700)
    for x, d, t, col in [(120, "15/7/2026", "Ký ban hành", BLUE), (340, "10/9/2026", "Có hiệu lực", GREEN)]:
        b += f'<circle cx="{x}" cy="160" r="10" fill="{col}"/>'
        b += text(x, 198, d, 15, col, weight=800) + text(x, 218, t, 13, INK)
    b += text(340, 236, "NĐ 12/2022 hết hiệu lực", 12, RED, weight=700)
    b += box(30, 260, 285, 120, "#fff", MUTED, 12, 2)
    b += text(46, 284, "Hành vi đã kết thúc trước 10/9", 13.5, INK, "start", 800)
    b += lines(46, 308, ["Áp dụng văn bản có hiệu lực", "tại thời điểm thực hiện hành vi", "(khoản 1 Điều 67)"], 12.5, 18, fill=INK, anchor="start")
    b += box(325, 260, 285, 120, "#fff", BRAND2, 12, 2)
    b += text(341, 284, "Hành vi còn diễn ra sau 10/9", 13.5, INK, "start", 800)
    b += lines(341, 308, ["Áp dụng Nghị định 283/2026", "(khoản 2 Điều 67)"], 12.5, 18, fill=INK, anchor="start")
    return svg(SCENES["l7-dong-thoi-gian"][0], b, "#f4f8f8")


@scene("l8-ba-huong", "Ba hướng làm mới nghề, giả định, cho một kỹ sư chất lượng 8 năm kinh nghiệm. Hướng sâu hơn: chuyên gia hệ thống quản lý chất lượng. Hướng rộng hơn: nhận dự án cải tiến liên phòng ban và kèm cặp kỹ sư mới. Hướng chuyển: sang đánh giá viên cho tổ chức chứng nhận. Ở giữa là các kỹ năng mang theo được.")
def _():
    b = text(320, 30, "Ba hướng làm mới nghề", 19, BRAND, weight=800)
    b += f'<circle cx="320" cy="215" r="80" fill="{BRAND}"/>'
    b += lines(320, 178, ["Kỹ năng", "mang theo được"], 13, 17, fill="#fff", weight=800)
    b += lines(320, 222, ["hệ thống · quyết định", "thuyết phục · kèm cặp", "dự án · đọc quy định"], 11, 15, fill="#e3f0ee")
    dirs = [(30, 60, GREEN, GREENBG, "Sâu hơn", ["Chuyên gia hệ thống", "quản lý chất lượng"], (240, 180)),
            (430, 60, BLUE, BLUEBG, "Rộng hơn", ["Dự án liên phòng ban,", "kèm kỹ sư mới"], (400, 180)),
            (230, 312, ACC, ACCBG, "Chuyển hướng", ["Đánh giá viên tổ chức", "chứng nhận (thử nhỏ trước)"], (320, 295))]
    for x, y, col, bg, t, rows, (ax, ay) in dirs:
        b += box(x, y, 180, 78, bg, col, 12, 2)
        b += text(x + 90, y + 26, t, 15, col, weight=800)
        b += lines(x + 90, y + 48, rows, 12, 16, fill=INK)
        cx, cy = x + 90, (y + 78 if y < 200 else y)
        b += f'<line x1="{ax}" y1="{ay}" x2="{cx}" y2="{cy}" stroke="{col}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    return svg(SCENES["l8-ba-huong"][0], b, "#fdf8ef")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (title, fn) in SCENES.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print(f"Đã vẽ {len(SCENES)} hình vào {OUT}")
