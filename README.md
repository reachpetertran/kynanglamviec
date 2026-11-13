# kynanglamviec.com

Mã nguồn website **Kỹ Năng Làm Việc** – kỹ năng làm việc theo lộ trình nghề nghiệp, từ học sinh đến quản lý.

- Trang tĩnh (HTML/CSS/JS), không đăng nhập, không cookie, không công cụ theo dõi, không tải mã hay phông chữ bên ngoài.
- Tiến độ, tự đánh giá, nhật ký: chỉ lưu localStorage trên máy người học.
- Nội dung tự viết: CC BY-NC-SA 4.0.

## Cấu trúc
```
data/            levels.yaml, skills.yaml, groups.yaml  (khung chương trình)
content/bai-hoc/ mỗi bài một file Markdown + YAML front matter (9 phần)
content/cau-hoi/ câu hỏi tự kiểm tra, mỗi bài một file YAML
_build/          build.py + static/ (CSS, JS, _headers, robots.txt)
public/          kết quả build – Cloudflare Pages phục vụ thư mục này
```

## Build
```
pip install markdown pyyaml
python3 _build/build.py            # -> public/
python3 _build/build.py --preview  # -> preview/ (mở file trực tiếp, không cần máy chủ)
```

## Cloudflare Pages
Build command: để trống · Output directory: `public` · Nhánh: `main`.

Sau này: sách bằng Pandoc từ `content/bai-hoc/*.md`; app dạng PWA từ cùng `public/`.

Xem `PROGRESS.md` cho tiến độ.
