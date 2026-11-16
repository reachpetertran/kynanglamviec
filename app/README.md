# App Kỹ Năng Làm Việc (Android, Capacitor 8)

Bọc site tĩnh `public/` thành app. Nội dung đóng gói sẵn, đọc được khi mất mạng, không cần máy chủ.
Miễn phí, không quảng cáo, không tài khoản, không tracking, không nút quyên góp.

## Cấu trúc
- `build_www.py`: sinh `www/` từ `../public/`. Không sửa `public/`. `www/` và `node_modules/` không commit.
- `shell/app.css`, `shell/app.js`: khung app (thanh trên, 5 tab: Trang chủ, Lộ trình, Sách, Bài học, Của tôi; nút Aa, tiến độ, lưu bài, tìm kiếm, tuần này, xóa dữ liệu).
- `capacitor.config.json`: appId `com.kynanglamviec.app` (KHÔNG đổi sau lần tải lên Play Store đầu tiên), webDir `www`, androidScheme `https`.
- `android/`: tạo bằng `npx cap add android`. targetSdk 36, minSdk 24.
- `assets/`: nguồn icon và màn hình chờ (SVG lấy từ `public/assets/logo-icon.svg`, bỏ dải đất ở lớp trước). Sinh lại: `npx @capacitor/assets generate --android`.
- Build: `.github/workflows/app-android.yml`. Đẩy nhánh `app` thì GitHub Actions build APK bản thử, lưu thành artifact `ky-nang-lam-viec-ban-thu`.

## Sách "Cuốn sổ bìa xanh" (thêm 16/11/2026)
- `sach/`: 20 chương (đoạn HTML), 21 tranh WebP 900 px (20 chương + bìa, 5,3 MB), `sach.json`. Sinh bằng
  `python3 app/tools/gen_sach.py /đường/dẫn/cuon-so-bia-xanh` từ `cuon-so-bia-xanh-chu-va-ma.zip` (chữ lấy từ `text/chuong-NN.md` qua `build_sach.py`, tranh vẽ lại bằng `art_sach.py`). Thêm `--no-art` nếu chỉ sửa chữ.
- Bản trong app: bản gia đình, tên thật Vĩ và Sơn (Peter chọn 16/11/2026). Bỏ phần "Ghi chú cho biên tập". QR đổi thành nút mở bài học ngay trong app.
- `/sach/` (mục lục theo 3 phần, nguồn), `/sach/chuong-NN/`. Tab "Sách" thay tab "Kỹ năng" ở bản tiếng Việt (trang Kỹ năng vẫn mở từ Trang chủ, Lộ trình). Bản tiếng Anh chưa có sách.
- Sách tính như một khóa: tiến độ "x/20 chương đã đọc", Đọc tiếp, tìm kiếm. Đã đọc lưu `klv:done:sach-cNN`. Bài học có chương minh họa hiện thẻ "Truyện minh họa trong sách".

## Dữ liệu trên máy
- Dữ liệu học dùng chung với site, tiền tố `klv:` (bài đã học `klv:done:<slug>`, nhật ký `klv:j:…`, tự đánh giá `klv:sa`).
- Dữ liệu riêng của app: một khóa `klv.app.v1` (cỡ chữ, màu nền, ngôn ngữ, bài đã lưu, ngày có học, vị trí đọc).
- Nút "Xóa mọi dữ liệu của tôi trên máy này" (tab Của tôi) xóa cả hai, bấm hai lần.
- Ghi chú riêng từng bài = phần Phản tư có sẵn của site (vào Nhật ký bằng chứng). Bài N1 không có ô ghi (không thu dữ liệu của trẻ).

## Khác với website
- Link thư mục đổi thành `…/index.html`. Link tuyệt đối tới kynanglamviec.com đổi về trang trong app.
- Ẩn nút In và nút tải `.ics` (WebView không in, không tải tệp). Link `.csv` mở trên trình duyệt của máy.
- Link ra ngoài (daynentang, tamhonkhoe, nguồn nghiên cứu…) mở bằng trình duyệt của máy.
- Bỏ canonical, hreflang. Nút ngôn ngữ trong bảng Aa dẫn đúng trang tương ứng; không có thì về trang chủ ngôn ngữ kia.

## Build trên máy (nếu cần)
```
python3 app/build_www.py
cd app && npm ci && npx cap sync android
cd android && ./gradlew assembleDebug
```
