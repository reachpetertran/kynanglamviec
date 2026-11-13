# Tiến độ dự án kynanglamviec.com

Đọc file này đầu mỗi phiên làm việc mới. Cập nhật cuối mỗi phiên.

## Trạng thái hiện tại (14/11/2026) – v0.1
- Bản xem trước (riêng tư, chỉ Peter xem): https://claude.ai/artifact/YQWK14o3VR6Xmw8nWMA2fK
- Mã nguồn: https://github.com/reachpetertran/kynanglamviec (public, nhánh `main`, đẩy ngày 14/11/2026). **Chưa nối Cloudflare Pages, site chưa chạy.**
- Phiên mới: gắn repo (add_repo, quyền push) rồi clone về để làm tiếp. Không cần file zip nữa.

## Đã xong
- Bộ sinh trang Python (`_build/build.py`), cùng cách làm với daynentang: build tại máy, commit `public/`, Cloudflare Pages chỉ phục vụ thư mục `public/`.
- Dữ liệu khung: `data/levels.yaml` (5 bậc, 4 mức tự đánh giá), `data/skills.yaml` (10 kỹ năng × 5 bậc × 2 câu "Tôi có thể…"), `data/groups.yaml` (N1–N5, ma trận, học phần).
- 28 trang: trang chủ, 5 lộ trình, 10 kỹ năng, bài học, tự đánh giá, nhật ký bằng chứng, tài nguyên in (STAR, danh sách việc 5 cột + CSV), khung tham chiếu, pháp lý (giữ chỗ), giới thiệu, 404, sitemap, _headers (CSP chặt).
- Tính năng localStorage: tự kiểm tra có giải thích, đánh dấu đã học + lịch ôn 1/3/7 ngày + tải .ics, phản tư lưu vào nhật ký, tự đánh giá có bậc gợi ý, in/lưu PDF.
- 2 bài mẫu (bản nháp, chờ duyệt):
  1. `k1-xac-nhan-chi-dan` – K1 Bậc 2, N2/N3.
  2. `k5-ghi-viec-va-bao-som` – K5 Bậc 2, N2/N3.

## Việc tiếp theo
1. Peter duyệt: mẫu bài, 100 câu "Tôi có thể…", giao diện.
2. Nối Cloudflare Pages với repo: build command để trống, output `public`, nhánh `main`. Sau đó gắn domain kynanglamviec.com (DNS ở GoDaddy). Đăng thật chỉ khi Peter đã duyệt nội dung.
3. Viết tiếp ~10 bài thử nghiệm N2–N3 (theo file Context mục 6). Bài pháp lý (K10) phải tra lại luật ngay trước khi viết.

## Quy trình thêm bài
1. Tạo `content/bai-hoc/<slug>.md` (front matter: title, slug, skill, level, group, order, minutes, objectives (đặt trong ngoặc kép), framework_map, prev, next, updated, status) với đúng 9 tiêu đề `## 1. Mục tiêu` … `## 9. Siêu dữ liệu`. Phần 6 và 9 để trống: build tự chèn câu hỏi và bảng siêu dữ liệu.
2. Tạo `content/cau-hoi/<slug>.yaml` (3–5 câu, mỗi lựa chọn có `why`).
3. Chạy `python3 _build/build.py` (và `--preview` để xem offline).

## Quyết định chờ Peter [TK]
- Giấy phép nội dung: đang để CC BY-NC-SA 4.0 (giống daynentang).
- Có giữ 2 câu/bậc hay tăng lên 3 câu/bậc.
