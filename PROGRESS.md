# Tiến độ dự án kynanglamviec.com

Đọc file này đầu mỗi phiên làm việc mới. Cập nhật cuối mỗi phiên.

## Trạng thái hiện tại (14/11/2026) – v1.0, ĐANG CHẠY THẬT (7 khóa N1–N7, 76 bài, đủ 50 ô K1–K10 × Bậc 1–5, có logo; bản tiếng Anh /en/ 57 bài: khóa N2–N7 + 11 bài chuỗi chính)
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

## Khóa N5 "Quản lý, trưởng nhóm" (đăng 14/11/2026, 8 bài, chuỗi riêng, order 61–68)
41. k7-tu-chuyen-vien-thanh-quan-ly – K7 B5 (Bài 1, Tờ 1 Bản chuyển vai: buông/giữ/mới; 3 câu phản hồi nhiều chiều)
42. k2-noi-ro-muc-tieu-doi – K2 B5 (Bài 2, Tờ 2 Mục tiêu đội một trang; kiểm hiểu bằng nhờ nói lại)
43. k9-giao-viec-va-theo-doi – K9 B5 (Bài 3, Tờ 3 Phiếu giao việc 6 ô; 4 mức tự quyết; phản hồi kịp thời/định kỳ)
44. k1-lang-nghe-de-coaching – K1 B5 (Bài 4, Tờ 4 Trang 1-1; 4 bước kiểu GROW, câu hỏi tự viết)
45. k8-doi-thoai-kho – K8 B4 (Bài 5, Tờ 5; 6 bước chuẩn bị; hòa giải gặp riêng rồi gặp chung; vùng không hòa giải)
46. k8-xay-doi-hoa-nhap – K8 B5 (Bài 6, Tờ 6 Thỏa thuận làm việc; việc không tên; link chéo trachnhiemxahoi)
47. k6-dan-dat-thay-doi-va-ai – K6 B5 (Bài 7, Tờ 7 Kế hoạch thay đổi + Quy tắc AI 5 dòng; dẫn Luật BVDLCN 91/2025/QH15 hiệu lực 01/01/2026, Luật Trí tuệ nhân tạo 134/2025/QH15 hiệu lực 01/3/2026 – chỉ nêu tên, ngày, không diễn giải điều khoản)
48. k5-phan-bo-nguon-luc-va-on-tap – K5 B5 (Bài 8, ôn trộn 7 câu + Tờ 8 Bảng phân bổ quý, Danh sách không làm)
- Sợi chỉ: Sổ tay quản lý (8 tờ). Mẫu in `content/trang/n5-mau-in.md` → /tai-nguyen/n5/ (#to-1 … #to-8).
- Hình: `_build/art/n5_art.py` sinh 8 SVG vào `_build/static/assets/img/n5/`; aria-label lấy tự động từ alt trong bài.
- build.py: COURSES["n5"]; trang nhóm N5 hiện Bản đồ khóa.

## Nhóm mới N6, N7 (thêm 14/11/2026 theo yêu cầu của Peter)
- data/groups.yaml có 7 nhóm. N6 "Quản lý cấp cao, lãnh đạo" (Bậc 4–5). N7 "Founder, khởi nghiệp" (Bậc 2–4 tùy kỹ năng), trang /lo-trinh/n7/ có ghi chú "Khóa N7 đang được soạn".
- Khung chi tiết (ma trận, học phần, mục tiêu, nguồn, mục [TK]): project doc `claude/khung-n6-n7.md`.
- Nguồn: báo cáo nghiên cứu 14/11/2026 (UK Success Profiles – OGL v3.0; APS ILS; US OPM ECQs 2025; EntreComp; Camuffo 2020; Campos 2017; Flyvbjerg 2006; Klein 2007; Edmondson 1999).

## Khóa N6 "Lãnh đạo cấp cao" (đăng 14/11/2026, 8 bài, chuỗi riêng, order 71–78)
49. k9-tu-quan-ly-doi-den-lanh-dao-to-chuc – K9 B5 (Bài 1, Tờ 1 Lịch điều hành; nhãn D/T)
50. k3-quyet-dinh-chien-luoc-theo-nhom – K3 B5 (Bài 2, Tờ 2 Biên bản pre-mortem; góc nhìn bên ngoài; nối N4 k3-quyet-dinh-khi-thieu-thong-tin)
51. k5-chien-luoc-thanh-thuc-thi – K5 B5 (Bài 3, Tờ 3; ≤3 ưu tiên, chỗ phụ thuộc, tiêu chí tiếp tục/đổi/dừng)
52. k2-truyen-dat-qua-nhieu-cap – K2 B5 (Bài 4, Tờ 4 Bản định hướng 5 phần + kế hoạch truyền đạt)
53. k8-thiet-ke-quyen-quyet-dinh – K8 B5 (Bài 5, Tờ 5 Bảng quyền quyết định; 4 vai, 1 người quyết, 3 dấu hiệu nghẽn)
54. k1-nghe-tin-hieu-yeu – K1 B5 (Bài 6, Tờ 6 Kênh tin xấu; Edmondson 1999; link chéo trachnhiemxahoi)
55. k10-rui-ro-tuan-thu-va-quan-tri-ai – K10 B5 (Bài 7, Tờ 7 Sổ rủi ro + Danh mục AI; dẫn LDN 59/2020/QH14 sửa bởi 03/2022/QH15, 76/2025/QH15, Điều 165; Luật TTNT 134/2025/QH15; Luật BVDLCN 91/2025/QH15)
56. k9-lanh-dao-ke-can-va-on-tap – K9 B5 (Bài 8, ôn trộn 7 câu + Tờ 8 Bản đồ kế nhiệm)
- Mỗi bài có hộp "Mức bằng chứng" (nghiên cứu / khung năng lực / đề xuất của site).
- Sợi chỉ: Sổ tay điều hành (8 tờ). Mẫu in `content/trang/n6-mau-in.md` → /tai-nguyen/n6/ (#to-1 … #to-8).
- Hình: `_build/art/n6_art.py` sinh 8 SVG vào `_build/static/assets/img/n6/`.
- build.py: COURSES["n6"]; trang nhóm N6 hiện Bản đồ khóa; /lo-trinh/ ghi "Bảy lộ trình".
- [TK] Điều 165 LDN: chưa đối chiếu văn bản hợp nhất sau Luật 76/2025/QH15. Trang /khung-tham-chieu/ chưa có dòng UK Success Profiles, APS ILS, OPM ECQs, EntreComp.

## Khóa N7 "Founder, khởi nghiệp" (Peter duyệt khung 14/11/2026; đăng cùng ngày, 8 bài, chuỗi riêng, order 81–88)
57. k1-kham-pha-khach-hang – K1 B4 (Bài 1, Tờ 1 Phiếu giả thuyết + kịch bản phỏng vấn; 3 giả thuyết, hỏi về quá khứ)
58. k3-thu-nghiem-va-quyet-dinh-pivot – K3 B4 (Bài 2, Tờ 2 Phiếu thử nghiệm; ngưỡng viết trước, 3 vùng; Camuffo 2020 MS 66(2): 116 startup Ý, kết quả tốt hơn, pivot nhiều hơn, không bỏ cuộc nhiều hơn)
59. k6-chu-dong-va-phuc-hoi – K6 B4 (Bài 3, Tờ 3 Kế hoạch 90 ngày + phiếu rút kinh nghiệm 4 dòng; Campos 2017 Science: Togo ~1.500 DN, +30% vs +11% không YNTK; link chéo tamhonkhoe)
60. k5-nhung-con-so-song-con – K5 B3 (Bài 4, Tờ 4 Dòng tiền 13 tuần, biên gộp, hòa vốn, số tháng còn trụ; link chéo daynentang)
61. k10-phap-ly-khoi-su – K10 B3 (Bài 5, Tờ 5; 4 câu hỏi chọn loại hình; LDN 59/2020 sửa 03/2022, 76/2025 (CSHHL); NQ 198/2025/QH15 k4, k6 Điều 10; NĐ 20/2026/NĐ-CP ngày 15/01/2026)
62. k9-tuyen-va-giu-nhan-vien-dau-tien – K9 B3 (Bài 6, Tờ 6; 18/VBHN-VPQH Điều 13 k1, 14, 25–26, 118–119; Luật BHXH 41/2024/QH15 điểm a k1 Điều 2)
63. k2-pitch-ba-phut – K2 B3 (Bài 7, Tờ 7 Pitch 5 phần; tách số thật / dự báo; kiểm bằng nhờ nhắc lại đề nghị)
64. k10-van-hanh-so-du-lieu-va-on-tap – K10 B3 (Bài 8, ôn trộn 7 câu + Tờ 8 Bảng công cụ số, thông báo dữ liệu, 3 quy tắc AI; Luật BVDLCN 91/2025/QH15 Điều 38 k2–3; NĐ 356/2025/NĐ-CP)
- Sợi chỉ: Sổ tay founder (8 tờ). Mẫu in `content/trang/n7-mau-in.md` → /tai-nguyen/n7/ (#to-1 … #to-8).
- Hình: `_build/art/n7_art.py` sinh 8 SVG vào `_build/static/assets/img/n7/`.
- build.py: COURSES["n7"]; trang nhóm N7 hiện Bản đồ khóa; bỏ ghi chú "đang được soạn" trong data/groups.yaml.
- Mỗi bài có hộp "Mức bằng chứng" hoặc hộp "Cập nhật lần cuối" (bài 5, 6, 8).
- [TK] Camuffo 2024 SMJ 45(6): chưa đối chiếu bài gốc. NQ 198 / NĐ 20/2026: số điều khoản lấy từ nguồn thứ cấp (thuvienphapluat, luatvietnam). Điều 38 Luật BVDLCN: ngoại lệ lấy từ bản tóm tắt của hãng luật. Luật DN: trách nhiệm theo loại hình (Điều 46, 74, 111, 188) chưa dẫn số điều trong bài. Luật sửa BLLĐ và sửa Luật BHXH đang thảo luận tại kỳ họp.

## Nguồn pháp luật (14/11/2026)
- Thử dùng tài khoản Pro thuvienphapluat.vn qua Chrome: site chặn vì "tốc độ Robot" và đòi mã bảo vệ sau vài lượt tra. Đã dừng, KHÔNG tải PDF. Không tự động hóa site này.
- Số hiệu đã xác định trên thuvienphapluat (chưa đối chiếu ngày hiệu lực): Luật ATVSLĐ 84/2015/QH13; Luật BVDLCN 91/2025/QH15; Luật Trí tuệ nhân tạo 134/2025/QH15; NĐ 145/2020/NĐ-CP; NĐ 337/2025/NĐ-CP (HĐLĐ điện tử); Luật BHXH 41/2024/QH15; Luật Việc làm 74/2025/QH15; Luật Trẻ em 102/2016/QH13; Luật Giáo dục 43/2019/QH14.
- Luật sửa đổi BLLĐ 2026: chưa có trên thuvienphapluat ngày 14/11/2026; Quốc hội thảo luận 09/11/2026.

## Logo (đăng 14/11/2026)
- Dựa trên khung huy hiệu logo daynentang (Peter gửi file zip): giữ dáng vòm, mặt trời, núi tuyết, rừng thông, dải băng chữ, thanh "EST. 2026".
- Đổi màu theo site (teal #14524f/#0f3b39 + vàng #d98a1c); cảnh động vật thay bằng đường zíc-zắc 5 bậc lên đỉnh có cờ, tòa văn phòng, người đeo cặp và người xách cặp.
- Mã sinh: `_build/art/logo_art.py` -> `_build/static/assets/` logo.svg, logo-khong-chu.svg, logo-icon.svg, favicon.svg, logo-512/1024.png, logo-icon-512.png, apple-touch-icon.png. Chữ đã chuyển thành path (Inter Display, OFL; Poppins thiếu chữ "Ệ").
- Gắn: biểu tượng ở đầu trang mọi trang, favicon, apple-touch-icon, og:image (logo-1024.png), huy hiệu ở trang chủ.
- Lỗi check.py có từ trước: bài k5-ghi-viec-va-bao-som có 1 dòng bảng bị đếm là câu 26 chữ (chưa sửa).

## Bài lấp ô trống K × bậc (đăng 14/11/2026, 12 bài, ngoài khóa, order 12–23)
Rà ma trận 10 kỹ năng × 5 bậc: 12 ô chưa có bài. Nay ô nào cũng có ít nhất 1 bài (trang /ky-nang/ không còn "Chưa có bài ở bậc này").
Chuỗi A (prev/next, Bậc 1–2, nhóm N2 hoặc N2+N3):
65. k1-nghe-het-va-nhac-lai – K1 B1 (N2; dẫn sang k1-xac-nhan-chi-dan B2)
66. k3-noi-ro-cho-vuong-va-nho-giup – K3 B1 (N2; 3 bước khi bị vướng; việc an toàn/tiền/máy lạ thì hỏi ngay)
67. k6-khi-ke-hoach-thay-doi-nho – K6 B1 (N2; 2 câu hỏi khi kế hoạch đổi; đổi một điểm rồi thử lại; link chéo tamhonkhoe)
68. k4-hoi-con-cach-nao-khac – K4 B1 (N2; bỏ bớt / gộp, đổi thứ tự / mượn cách; ý tưởng 2 câu)
69. k9-nhan-vai-nho-trong-nhom – K9 B1 (N2; 3 vai nhỏ; chỉ bạn mới 4 bước)
70. k10-mat-khau-va-thong-tin-ca-nhan – K10 B1 (N2; mật khẩu, 2FA, OTP; 3 loại thông tin cá nhân giữ kín)
71. k10-nhan-ra-lua-dao-qua-email-tin-nhan – K10 B2 (N2, N3; 5 dấu hiệu; dừng – kiểm qua kênh khác – báo; hộp "Cập nhật lần cuối")
72. k6-lam-quen-cong-cu-va-quy-trinh-moi – K6 B2 (N2, N3; 4 bước làm quen cách mới; nhận góp ý 3 bước; link k7-hoc-nhanh-viec-moi)
73. k4-thu-cach-lam-moi-nho – K4 B2 (N2, N3; phiếu thử nhỏ 4 ô; góp ý 3 dòng)
74. k9-dieu-phoi-viec-nho-cua-nhom – K9 B2 (N2, N3; đề xuất 3 câu; điều phối 4 bước; next: null)
Chuỗi K4 nâng cao (nối tiếp chuỗi chính: k4-de-xuat-cai-tien.next = k4-muon-y-tuong-tu-linh-vuc-khac):
75. k4-muon-y-tuong-tu-linh-vuc-khac – K4 B4 (N4; mượn nguyên lý 3 bước; vòng cải tiến 5 bước, có chuẩn hóa; hộp "Mức bằng chứng")
76. k4-nuoi-van-hoa-thu-nghiem – K4 B5 (N5, N6; quỹ thử nghiệm 4 điều; chấm ý tưởng 4 tiêu chí; rút kinh nghiệm không đổ lỗi; Edmondson 1999, Camuffo 2020)
- Không gắn N1 cho bài Bậc 1 (N1 chỉ học 4 chủ đề đã chốt).
- Hình (thêm 14/11/2026): `_build/art/bs_art.py` sinh 12 SVG vào `_build/static/assets/img/bs/`, mỗi bài 1 hình + ít nhất 1 sơ đồ HTML (k1-nghe-het thêm sơ đồ "Ba trường hợp khi nhận chỉ dẫn"). aria-label lấy từ alt trong bài. Hình k4-cham-y-tuong nằm trong "Lời giải mẫu" để không lộ đáp án.
- K10 B2: chỉ dạy nhận diện lừa đảo. Phần "đọc hợp đồng, thỏa thuận thực tập" vẫn HOÃN cùng bài pháp lý N2.
- Kênh báo lừa đảo: bài K10 B2 dẫn tinnhiemmang.vn (Trung tâm An ninh mạng Quốc gia vận hành; có tra cứu website và tin cảnh báo lừa đảo; kiểm tra 14/11/2026) để tra cứu, KHÔNG phải kênh nhận báo cáo. Email tinnhiemmang@ais.gov.vn Peter gửi: chưa xác minh được là kênh nhận báo cáo lừa đảo, không thấy trên trang chủ tinnhiemmang.vn, chưa đưa vào bài. [TK] Nếu Peter có văn bản chính thức nêu kênh nhận phản ánh, bổ sung sau.

## Bản tiếng Anh /en/ (đợt 1, đăng 14/11/2026)
- Peter chọn (14/11/2026): làm thử rồi làm hết; URL `/en/` + slug tiếng Anh; **quốc tế hóa ví dụ** (tên, nơi chốn đổi sang bối cảnh chung; luật VN chỉ nêu làm ví dụ, ghi nguồn). Bản tiếng Việt là bản gốc.
- Đã có: /en/ (trang chủ), /en/paths/ + 7 nhóm, /en/skills/ + 10 kỹ năng (150 câu "I can…"), /en/lessons/ (7 bài khóa N2), /en/self-assessment/, /en/journal/, /en/resources/ + /en/resources/n2/ (7 mẫu in, neo #sheet-1 … #sheet-7), /en/frameworks/, /en/about/.
- Nguồn: `content/en/data/` (skills, levels, groups – cùng mã), `content/en/lessons/*.md` (front matter `vi:` = slug bài gốc), `content/en/quiz/`, `content/en/pages/n2-templates.md` (`vi: n2`).
- Bài N2 tiếng Anh: k7-know-yourself-choose-a-direction, k7-read-a-job-ad, k2-write-your-first-cv, k2-prepare-your-first-interview, k2-communicate-in-your-first-week, k7-learn-a-new-task-fast, k7-review-your-job-ready-file.
- Mã: `_build/build_en.py` (gọi từ build.py; `alt_map()` nối trang VI↔EN). Header VI có nút "English" (trỏ tới trang tương ứng, không có thì /en/); EN có nút "Tiếng Việt". Có `hreflang`. app.js đổi chữ theo `<html lang>`; tự đánh giá dùng chung câu trả lời hai ngôn ngữ.
- Hình: `_build/art/n2_art_en.py` → `_build/static/assets/img/en/n2/` (7 SVG). `assets/task-list.csv` tiếng Anh.
- `check.py` kiểm cả bài EN (câu ≤25 từ, phần 3 <400 từ, ảnh, liên kết, `vi:` trỏ đúng bài gốc).
- Trang nhóm chưa có khóa EN thì ghi chú và dẫn sang khóa tiếng Việt. Bài EN dẫn bài VI chưa dịch kèm "(in Vietnamese)".
- (14/11/2026) trachnhiemxahoi.com chưa thực hiện: đã gỡ liên kết, xem mục riêng bên dưới.
- Peter duyệt văn phong đợt 1 (14/11/2026) và giao làm đợt 2.

## Bản tiếng Anh /en/ – đợt 2 (đăng 14/11/2026): khóa N3 + 11 bài chuỗi chính
- Khóa N3 "Your First 90 Days course" (order 41–47, `course: n3`): k5-prioritise-competing-tasks, k1-close-actions-after-a-meeting, k3-handle-customer-requests, k3-find-the-root-cause, k6-when-work-goes-off-plan, k8-work-with-other-teams, k7-prepare-your-90-day-review. Sợi chỉ: 90-day notebook (Sheet 1–7).
- Mẫu in: `content/en/pages/n3-templates.md` → /en/resources/n3/ (neo #sheet-1 … #sheet-7). build_en.py: thêm COURSES["n3"].
- Hình: `_build/art/n3_art_en.py` (dùng helper của n2_art) → `_build/static/assets/img/en/n3/` (7 SVG: l1-matrix … l7-review-file).
- 11 bài chuỗi chính (order 1–11, prev/next nối nhau, bài 11 next: null): k1-confirm-instructions, k5-track-tasks-and-flag-delays-early, k2-write-a-work-email, k2-write-a-progress-report, k3-describe-a-problem-with-two-options, k7-ask-for-and-use-feedback, k8-split-work-in-a-group-project, k10-use-ai-safely, k2-tell-a-star-example, k7-plan-your-first-90-days, k4-propose-a-small-improvement. Không có hình (giống bản VI), giữ sơ đồ `flow`.
- Bài N3 Bài 7 EN: hộp "Sources (example: Vietnam)" dẫn BLLĐ hợp nhất 18/VBHN-VPQH Điều 25, k1 Điều 27; tra 14/11/2026: luật sửa đổi BLLĐ vẫn đang được Quốc hội xem xét (thảo luận 09/11/2026), chưa thấy tin biểu quyết.
- Quốc tế hóa: tên người đổi sang tên quốc tế; bỏ Zalo, Tết, VND, tên thành phố; điểm "8,5" đổi thành "a high mark"; "18 triệu đồng" đổi thành "worth 7,500 in total" (không đơn vị tiền).
- Đã sửa 3 bài N2 EN: liên kết "(in Vietnamese)" sang bài EN mới (k1-confirm-instructions, k2-tell-a-star-example, k8-split-work-in-a-group-project, k10-use-ai-safely).
- Lưu ý YAML câu hỏi EN: giá trị có ": " phải đặt trong ngoặc kép.
- Đang có 25 bài EN. Việc tiếp: đợt 3 = N4–N7 (32 bài); 12 bài lẻ; N1 cuối (bài cho phụ huynh, cần cân nhắc bối cảnh).

## Bản tiếng Anh /en/ – đợt 3 (đăng 14/11/2026): khóa N4, N5, N6, N7 (32 bài)
- Peter yêu cầu 14/11/2026. Mỗi khóa: 8 bài + câu hỏi (`content/en/lessons`, `content/en/quiz`), mẫu in `content/en/pages/n4…n7-templates.md` → /en/resources/n4…n7/ (neo #sheet-1 … #sheet-8), 8 hình. build_en.py: thêm COURSES n4–n7.
- Slug EN: N4 k3-see-the-whole-system, k3-decide-with-incomplete-information, k2-persuade-without-authority, k8-resolve-professional-disagreements, k9-coach-a-colleague, k5-run-a-lean-project, k10-turn-rules-into-practice, k7-renew-your-career. N5 k7-from-specialist-to-manager, k2-make-team-goals-clear, k9-delegate-and-follow-up, k1-listen-to-coach, k8-hold-difficult-conversations, k8-build-an-inclusive-team, k6-lead-change-and-ai-adoption, k5-allocate-resources-and-review. N6 k9-from-team-manager-to-organisation-leader, k3-make-strategic-decisions-as-a-group, k5-turn-strategy-into-execution, k2-communicate-across-levels, k8-design-decision-rights, k1-hear-weak-signals, k10-risk-compliance-and-ai-governance, k9-develop-successors-and-review. N7 k1-discover-your-customers, k3-run-experiments-and-decide-to-pivot, k6-take-initiative-and-bounce-back, k5-the-numbers-that-keep-you-alive, k10-legal-basics-for-starting-up, k9-hire-and-keep-your-first-employees, k2-pitch-in-three-minutes, k10-digital-operations-data-and-review.
- Hình EN mới cách làm: `_build/art/svg_en.py` lấy SVG tiếng Việt (n4…n7_art.py), thay chữ theo `_build/art/en/<khóa>.yaml`, lấy aria-label/title từ alt của bài EN. Thiếu bản dịch thì dừng báo lỗi; nhãn dài hơn nhiều thì cảnh báo "wide?" để xem bằng mắt (rsvg-convert). Sửa hình VI thì chạy lại script VI rồi `python3 _build/art/svg_en.py`.
- framework_map, level, skill, group, order của bài EN chép đúng từ bài VI (đã đối chiếu bằng script).
- Quốc tế hóa: tên người quốc tế; bỏ tên tỉnh, thành; tiền dùng đơn vị chung không ghi VND (bài N7-4, N7-7); luật VN để trong hộp "Last updated … (example: Vietnam)" hoặc ghi "(Vietnam)" ở tình huống (N4-7, N5-7, N6-7, N7-5, N7-6, N7-8).
- Đang có 57 bài EN. Còn lại: 12 bài lẻ (lấp ô K × bậc) và khóa N1 (cho phụ huynh, cần cân nhắc bối cảnh).

## trachnhiemxahoi.com chưa có (Peter báo 14/11/2026)
- Đã gỡ mọi liên kết tới trachnhiemxahoi.com (footer VI/EN, trang giới thiệu, ghi chú K10 trong data/skills.yaml và content/en/data/skills.yaml, 4 bài VI: k1-nghe-tin-hieu-yeu, k10-bien-quy-dinh-thanh-viec-lam, k7-ai-cung-co-the-lam-nghe-nay, k8-xay-doi-hoa-nhap). Giữ tên site dạng chữ thường, ghi "sắp ra mắt" / "coming soon".
- build.py, build_en.py: ô crosslink trên trang kỹ năng chỉ hiện nút liên kết khi có `url`. Khi trachnhiemxahoi.com chạy, thêm lại `url` và liên kết.

## Việc tiếp theo
1. Bài pháp lý K10 "Quyền và an toàn khi đi làm thêm, thực tập" (N2): HOÃN. Luật sửa đổi BLLĐ đang được Quốc hội khóa XVI xem xét tại Kỳ họp thứ 2. Tra lại kết quả biểu quyết trước khi viết; dẫn 18/VBHN-VPQH (12/02/2026) nếu luật chưa có hiệu lực.
2. (Đã xong 14/11: "Phục vụ khách hàng" và K6 cho N3, trong khóa N3.)
3. Đủ 5 khóa N1–N5 đã đăng (14/11/2026). N4, N5 chờ Peter duyệt nội dung.
4. Khóa N7 đã đăng 14/11/2026. Chờ Peter duyệt nội dung N4–N7. Đối chiếu NQ 198/2025, NĐ 20/2026 trên văn bản gốc; khi luật sửa BLLĐ/BHXH được thông qua, cập nhật N7 Bài 6.
5. (Xong 14/11: đủ 50 ô K × bậc.) Gợi ý tiếp: trang tự đánh giá theo khóa; bài pháp lý hoãn (xem mục 1) khi luật sửa đổi BLLĐ được thông qua.

## Quy trình thêm bài
1. Tạo `content/bai-hoc/<slug>.md` (front matter: title, slug, skill, level, group, order, minutes, objectives (đặt trong ngoặc kép), framework_map, prev, next, updated, status) với đúng 9 tiêu đề `## 1. Mục tiêu` … `## 9. Siêu dữ liệu`. Phần 6 và 9 để trống: build tự chèn câu hỏi và bảng siêu dữ liệu.
2. Tạo `content/cau-hoi/<slug>.yaml` (3–5 câu, mỗi lựa chọn có `why`).
3. Cập nhật `next` của bài trước.
4. Chạy `python3 _build/build.py` (và `--preview` để xem offline). Kiểm câu ≤25 chữ, phần giải thích <400 chữ.

## Đối chiếu khung (14/11/2026)
Tên gốc CSfW (10 lĩnh vực), SkillsFuture CCS (16), NACE (8), LifeComp (9), WEF FoJ 2025 đã đối chiếu và ghi trên trang /khung-tham-chieu/. `framework_map` trong `data/skills.yaml` đã cập nhật theo mã chính xác.
