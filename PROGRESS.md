# Tiến độ dự án kynanglamviec.com

Đọc file này đầu mỗi phiên làm việc mới. Cập nhật cuối mỗi phiên.

## Trạng thái hiện tại (14/11/2026) – v0.3, ĐANG CHẠY THẬT
- Site: https://kynanglamviec.com và https://www.kynanglamviec.com (Cloudflare Pages, SSL bật). Bản dự phòng: https://kynanglamviec.pages.dev
- Mã nguồn: https://github.com/reachpetertran/kynanglamviec (public, nhánh `main`). Mỗi lần push lên `main`, Cloudflare tự đăng.
- Phiên mới: gắn repo (add_repo, quyền push), clone, sửa, `python3 _build/build.py`, commit cả `public/`, push.

## Hạ tầng (đã làm 14/11/2026)
- Cloudflare Pages project `kynanglamviec`: build command để trống, output `public`.
- Zone kynanglamviec.com trên Cloudflare, gói Free ($0). Nameserver tại GoDaddy đã đổi sang `christian.ns.cloudflare.com`, `clarissa.ns.cloudflare.com`.
- Đã xóa 3 bản ghi đỗ (parking) của GoDaddy (2 A, 1 CNAME www). Giữ `_domainconnect` và `_dmarc`.
- Giấy phép nội dung: CC BY-NC-SA 4.0 (Peter duyệt, giống daynentang).

## Quyết định của Peter (14/11/2026)
- Cho phép Claude đăng web thật, sửa DNS ở GoDaddy/Cloudflare. **Mọi thao tác tốn tiền: phải báo Peter, Claude không tự quyết.**
- Câu "Tôi có thể…": đủ rõ, đo được; mỗi bậc 3 câu (tổng 150 câu).
- Duyệt mẫu bài 9 phần; Claude được viết và đăng bài tiếp.

## Nội dung đã đăng (11 bài, N2–N3)
1. k1-xac-nhan-chi-dan – K1 B2
2. k5-ghi-viec-va-bao-som – K5 B2
3. k2-viet-email-cong-viec – K2 B2
4. k2-bao-cao-tien-do – K2 B3
5. k3-mo-ta-van-de-va-phuong-an – K3 B2
6. k7-xin-va-dung-phan-hoi – K7 B3
7. k8-chia-viec-du-an-nhom – K8 B2
8. k10-dung-ai-an-toan – K10 B3
9. k2-ke-vi-du-star – K2 B2
10. k7-ke-hoach-90-ngay – K7 B3
11. k4-de-xuat-cai-tien – K4 B3
Chuỗi prev/next theo thứ tự trên. Bài 11 có `next: null`.

## Khóa N1 "Khám phá nghề" (đăng 14/11/2026, 7 bài, chuỗi riêng, order 21–27)
12. k7-nghe-nghiep-quanh-em – K7 B1 (Bài 1)
13. k7-nghe-nao-cung-can-ky-nang – K7 B1 (Bài 2)
14. k7-ai-cung-co-the-lam-nghe-nay – K7 B1 (Bài 3, chống định kiến giới)
15. k8-cung-nhau-hoan-thanh-nhiem-vu – K8 B1 (Bài 4)
16. k5-nhan-viec-va-giu-hen – K5 B1 (Bài 5, THCS)
17. k7-phong-van-nguoi-lam-nghe – K7 B1 (Bài 6, THCS)
18. k7-ngay-hoi-nghe-nghiep – K7 B1 (Bài 7, ôn tập + kiểm chéo)
- Sợi chỉ xuyên khóa: Thẻ nghề 5 ô. Mỗi bài: 3 hình SVG tự vẽ + 2 sơ đồ HTML; câu hỏi cuối mỗi bài ôn bài trước.
- Hình: `_build/art/n1_art.py` sinh 21 SVG vào `_build/static/assets/img/n1/` (sửa hình thì sửa script rồi chạy lại).
- Front matter mới (tùy chọn): `course`, `short`, `hook`, `age`. Build sinh dải tiến độ khóa và bản đồ khóa ở /lo-trinh/n1/.
- Trang /tai-nguyen/n1/ từ `content/trang/n1-huong-dan.md`: lịch 7 tuần, ôn giãn cách, an toàn, 5 mẫu in.
- Bài N1 không có ô ghi phản tư (app.js bỏ qua khi data-group chứa N1).
- Kiểm tra: `python3 _build/check.py` (câu ≤25 chữ, phần 3 <400 chữ, đủ 9 phần, ảnh, liên kết, câu hỏi). Báo lỗi giả ở k5-ghi-viec-va-bao-som (dòng liệt kê dùng dấu ·).

## Việc tiếp theo
1. Bài pháp lý K10 "Quyền và an toàn khi đi làm thêm, thực tập" (N2): HOÃN. Luật sửa đổi BLLĐ đang được Quốc hội khóa XVI xem xét tại Kỳ họp thứ 2. Tra lại kết quả biểu quyết trước khi viết; dẫn 18/VBHN-VPQH (12/02/2026) nếu luật chưa có hiệu lực.
2. Bài còn thiếu theo học phần: "Phục vụ khách hàng nội bộ và bên ngoài" (N3), "Hiểu mình để chọn hướng" (N2), "Học nhanh việc mới" (N2), "Giao tiếp ở nơi làm việc đầu tiên" (N2), K6 cho N3.
3. N1 đã xong (chờ Peter duyệt nội dung). Tiếp theo: N4, N5.

## Quy trình thêm bài
1. Tạo `content/bai-hoc/<slug>.md` (front matter: title, slug, skill, level, group, order, minutes, objectives (đặt trong ngoặc kép), framework_map, prev, next, updated, status) với đúng 9 tiêu đề `## 1. Mục tiêu` … `## 9. Siêu dữ liệu`. Phần 6 và 9 để trống: build tự chèn câu hỏi và bảng siêu dữ liệu.
2. Tạo `content/cau-hoi/<slug>.yaml` (3–5 câu, mỗi lựa chọn có `why`).
3. Cập nhật `next` của bài trước.
4. Chạy `python3 _build/build.py` (và `--preview` để xem offline). Kiểm câu ≤25 chữ, phần giải thích <400 chữ.

## Đối chiếu khung (14/11/2026)
Tên gốc CSfW (10 lĩnh vực), SkillsFuture CCS (16), NACE (8), LifeComp (9), WEF FoJ 2025 đã đối chiếu và ghi trên trang /khung-tham-chieu/. `framework_map` trong `data/skills.yaml` đã cập nhật theo mã chính xác.
