# Tiến độ dự án kynanglamviec.com

Đọc file này đầu mỗi phiên làm việc mới. Cập nhật cuối mỗi phiên.

## Trạng thái hiện tại (14/11/2026) – v0.5, ĐANG CHẠY THẬT
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

## Khóa N2 "Chuẩn bị đi làm" (đăng 14/11/2026, 7 bài, chuỗi riêng, order 31–37)
19. k7-hieu-minh-chon-huong – K7 B2 (Bài 1, Tờ 1 Bản đồ hướng đi)
20. k7-doc-tin-tuyen-dung – K7 B2 (Bài 2, Tờ 2; dẫn BLLĐ hợp nhất 18/VBHN-VPQH Điều 16, 17, 143)
21. k2-viet-cv-dau-tien – K2 B2 (Bài 3, Tờ 3 CV một trang)
22. k2-chuan-bi-phong-van – K2 B2 (Bài 4, Tờ 4; STAR dẫn sang k2-ke-vi-du-star)
23. k2-giao-tiep-tuan-dau – K2 B1 (Bài 5, Tờ 5 Sổ tay tuần đầu)
24. k7-hoc-nhanh-viec-moi – K7 B2 (Bài 6, Tờ 6 Sổ quy trình; Dunlosky 2013)
25. k7-on-tap-ho-so-san-sang – K7 B2 (Bài 7, ôn tập trộn + kiểm chéo + kế hoạch 30 ngày)
- Sợi chỉ xuyên khóa: Hồ sơ sẵn sàng đi làm (6 tờ + bảng kiểm). Mẫu in: `content/trang/n2-mau-in.md` → /tai-nguyen/n2/ (neo #to-1 … #to-7).
- Hình: `_build/art/n2_art.py` sinh 7 SVG vào `_build/static/assets/img/n2/`.
- Build: `COURSES` trong build.py giờ hỗ trợ nhiều khóa (title, home, guide, thread, after). Trang nhóm có khóa thì hiện "Bản đồ khóa" + "Bài học thêm cho nhóm".
- 7 bài N2 cũ (chuỗi chính) hiện ở mục "Bài học thêm cho nhóm" trên /lo-trinh/n2/.
- Chỗ trống: bài pháp lý "Quyền và an toàn khi đi làm thêm, thực tập" — thêm vào khóa N2 (Bài 3 hoặc cuối) sau khi luật sửa đổi BLLĐ được biểu quyết. Bản đồ khóa đang có hộp "Sắp có".

## Khóa N3 "90 ngày đầu" (đăng 14/11/2026, 7 bài, chuỗi riêng, order 41–47)
26. k5-sap-uu-tien-nhieu-viec – K5 B3 (Bài 1, Tờ 1 Bảng việc tuần; ma trận ảnh hưởng × hạn)
27. k1-nghe-va-chot-viec-sau-hop – K1 B3 (Bài 2, Tờ 2 Trang ghi họp)
28. k3-xu-ly-yeu-cau-khach-hang – K3 B3 (Bài 3, Tờ 3; học phần "Phục vụ khách hàng nội bộ và bên ngoài")
29. k3-tim-nguyen-nhan-goc – K3 B3 (Bài 4, Tờ 4 Phiếu sự cố; sửa tạm / sửa gốc)
30. k6-khi-viec-khong-nhu-ke-hoach – K6 B3 (Bài 5, Tờ 5; link chéo tamhonkhoe)
31. k8-phoi-hop-dong-nghiep – K8 B3 (Bài 6, Tờ 6 Bản đồ phối hợp)
32. k7-chuan-bi-danh-gia-90-ngay – K7 B3 (Bài 7, ôn tập trộn + Tờ 7; dẫn BLLĐ hợp nhất 18/VBHN-VPQH Điều 25, k1 Điều 27)
- Sợi chỉ: Sổ tay 90 ngày (6 tờ + Tờ 7). Mẫu in `content/trang/n3-mau-in.md` → /tai-nguyen/n3/ (#to-1 … #to-7).
- Hình: `_build/art/n3_art.py` (import helper từ n2_art.py) sinh 7 SVG vào `_build/static/assets/img/n3/`.
- build.py: thêm COURSES["n3"]; trang nhóm N2 và N3 cùng hiện Bản đồ khóa. 11 bài chuỗi chính cũ có N3 hiện ở "Bài học thêm".
- Chỗ trống: bài "Hợp đồng, thử việc và nội quy" (K10, N3) – HOÃN tới khi luật sửa đổi BLLĐ được biểu quyết.

## Khóa N4 "Senior, chuyên gia" (soạn 14/11/2026, 8 bài, chuỗi riêng, order 51–58)
33. k3-nhin-van-de-theo-he-thong – K3 B4 (Bài 1, Tờ 1 Sơ đồ tác động; vòng lặp, độ trễ, điểm đòn bẩy)
34. k3-quyet-dinh-khi-thieu-thong-tin – K3 B4 (Bài 2, Tờ 2 Phiếu quyết định)
35. k2-thuyet-phuc-khong-can-chuc-danh – K2 B4 (Bài 3, Tờ 3 Bản đồ các bên + đề xuất một trang; lập trường/lợi ích)
36. k8-go-bat-dong-chuyen-mon – K8 B4 (Bài 4, Tờ 4; nghe phản biện K1)
37. k9-kem-cap-dong-nghiep – K9 B4 (Bài 5, Tờ 5; 4 nấc giao việc)
38. k5-du-an-gon-nhe – K5 B4 (Bài 6, Tờ 6 Một trang dự án; gồm "thử nhỏ" của K4)
39. k10-bien-quy-dinh-thanh-viec-lam – K10 B4 (Bài 7, Tờ 7; dẫn NĐ 283/2026/NĐ-CP Điều 66–67, NĐ 293/2025/NĐ-CP Điều 3–5, Luật BHVBQPPL 64/2025/QH15 sửa đổi 87/2025/QH15 theo 54/VBHN-VPQH Điều 4, 53, 57, 58, 65 – đối chiếu file gốc trong thư mục luật của Peter)
40. k7-lam-moi-nghe-nghiep – K7 B4 (Bài 8, ôn tập trộn 7 câu + Tờ 8 Kế hoạch nghề 1–3 năm)
- Sợi chỉ: Sổ công cụ chuyên gia (8 tờ). Mẫu in `content/trang/n4-mau-in.md` → /tai-nguyen/n4/ (#to-1 … #to-8).
- Hình: `_build/art/n4_art.py` sinh 8 SVG vào `_build/static/assets/img/n4/`.
- build.py: COURSES["n4"]; trang /lo-trinh/n4/ hiện Bản đồ khóa.
- Nguồn luật: thư mục "Danh mục văn bản pháp luật" trên máy Peter (Luật Lao động - BHXH, ATVSLĐ, PCCC, Môi trường). Bản .md là OCR, mức tiền dễ sai: không chép số tiền, dẫn điều khoản.

## Nguồn pháp luật (14/11/2026)
- Thử dùng tài khoản Pro thuvienphapluat.vn qua Chrome: site chặn vì "tốc độ Robot" và đòi mã bảo vệ sau vài lượt tra. Đã dừng, KHÔNG tải PDF. Không tự động hóa site này.
- Số hiệu đã xác định trên thuvienphapluat (chưa đối chiếu ngày hiệu lực): Luật ATVSLĐ 84/2015/QH13; Luật BVDLCN 91/2025/QH15; Luật Trí tuệ nhân tạo 134/2025/QH15; NĐ 145/2020/NĐ-CP; NĐ 337/2025/NĐ-CP (HĐLĐ điện tử); Luật BHXH 41/2024/QH15; Luật Việc làm 74/2025/QH15; Luật Trẻ em 102/2016/QH13; Luật Giáo dục 43/2019/QH14.
- Luật sửa đổi BLLĐ 2026: chưa có trên thuvienphapluat ngày 14/11/2026; Quốc hội thảo luận 09/11/2026.

## Việc tiếp theo
1. Bài pháp lý K10 "Quyền và an toàn khi đi làm thêm, thực tập" (N2): HOÃN. Luật sửa đổi BLLĐ đang được Quốc hội khóa XVI xem xét tại Kỳ họp thứ 2. Tra lại kết quả biểu quyết trước khi viết; dẫn 18/VBHN-VPQH (12/02/2026) nếu luật chưa có hiệu lực.
2. (Đã xong 14/11: "Phục vụ khách hàng" và K6 cho N3, trong khóa N3.)
3. N1, N2, N3 đã đăng. N4 đã soạn 14/11 (chờ Peter duyệt). Tiếp theo: khóa N5.

## Quy trình thêm bài
1. Tạo `content/bai-hoc/<slug>.md` (front matter: title, slug, skill, level, group, order, minutes, objectives (đặt trong ngoặc kép), framework_map, prev, next, updated, status) với đúng 9 tiêu đề `## 1. Mục tiêu` … `## 9. Siêu dữ liệu`. Phần 6 và 9 để trống: build tự chèn câu hỏi và bảng siêu dữ liệu.
2. Tạo `content/cau-hoi/<slug>.yaml` (3–5 câu, mỗi lựa chọn có `why`).
3. Cập nhật `next` của bài trước.
4. Chạy `python3 _build/build.py` (và `--preview` để xem offline). Kiểm câu ≤25 chữ, phần giải thích <400 chữ.

## Đối chiếu khung (14/11/2026)
Tên gốc CSfW (10 lĩnh vực), SkillsFuture CCS (16), NACE (8), LifeComp (9), WEF FoJ 2025 đã đối chiếu và ghi trên trang /khung-tham-chieu/. `framework_map` trong `data/skills.yaml` đã cập nhật theo mã chính xác.
