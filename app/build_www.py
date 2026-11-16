#!/usr/bin/env python3
"""Sinh app/www (nội dung đóng gói trong app) từ public/ của website kynanglamviec.com.

Chạy từ gốc kho:  python3 app/build_www.py
- Chép mọi trang và tài nguyên. Không sửa public/.
- Thay header website bằng khung app: thanh trên (logo, nút Aa), thanh tab dưới (Việt / Anh).
- Đổi link thư mục ".../" thành ".../index.html" để chạy trong WebView khi mất mạng.
- Link tuyệt đối tới kynanglamviec.com: đổi về trang trong app nếu trang có trong app.
- Tệp tải về (.csv) mở bằng trình duyệt của máy. Nút In và nút tải .ics ẩn trong app (CSS).
- Bỏ canonical, hreflang. Chèn script nhỏ trong <head> áp cỡ chữ, màu nền đã lưu.
- Thêm trang riêng của app: Của tôi (/cua-toi/, /en/mine/).
- Sinh www/app/index.js: danh mục khóa -> bài (theo thứ tự trên Bản đồ khóa) và danh sách bài để tìm kiếm.
Không thu dữ liệu, không gọi mạng.
"""
import html
import json
import posixpath
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "public"
OUT = ROOT / "www"
SITE = "https://kynanglamviec.com"
APP_NAME = "Kỹ Năng Làm Việc"
KEY = "klv.app.v1"  # khóa riêng của app; dữ liệu học của site vẫn dùng tiền tố "klv:"

SACH = ROOT / "sach"  # sinh bằng tools/gen_sach.py từ bộ nguồn sách
SKIP_FILES = {"_headers", "robots.txt", "sitemap.xml", "404.html"}

ICONS = {
    "home": '<path d="M3 11.5 12 4l9 7.5M5.5 10v9.5h13V10"/>',
    "path": '<circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><path d="M8 18h6a3.5 3.5 0 0 0 0-7h-4a3.5 3.5 0 0 1 0-7h6"/>',
    "sach": '<path d="M6 3.5h11.5a1 1 0 0 1 1 1V20a.5.5 0 0 1-.5.5H6.5A2 2 0 0 1 4.5 18.5v-13a2 2 0 0 1 1.5-2Z"/><path d="M4.5 18.5a2 2 0 0 1 2-2h12M9 3.5v7l2-1.4 2 1.4v-7"/>',
    "skill": '<rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/>',
    "book": '<path d="M4 5.5c2.5-1 5.5-1 8 .5 2.5-1.5 5.5-1.5 8-.5v13c-2.5-1-5.5-1-8 .5-2.5-1.5-5.5-1.5-8-.5zM12 6v13"/>',
    "mine": '<circle cx="12" cy="8.5" r="3.6"/><path d="M4.5 20c1-4 4-5.5 7.5-5.5s6.5 1.5 7.5 5.5"/>',
}
TABS = {
    "vi": [("home", "Trang chủ", "/index.html"), ("path", "Lộ trình", "/lo-trinh/index.html"),
           ("sach", "Sách", "/sach/index.html"), ("book", "Bài học", "/bai-hoc/index.html"),
           ("mine", "Của tôi", "/cua-toi/index.html")],
    "en": [("home", "Home", "/en/index.html"), ("path", "Paths", "/en/paths/index.html"),
           ("skill", "Skills", "/en/skills/index.html"), ("book", "Lessons", "/en/lessons/index.html"),
           ("mine", "My learning", "/en/mine/index.html")],
}
T = {
    "vi": dict(home="/index.html", aa="Cỡ chữ, màu nền, ngôn ngữ", size="Cỡ chữ", sizes=["Nhỏ", "Vừa", "Lớn", "Rất lớn"],
               theme="Màu nền", themes=["Theo máy", "Sáng", "Tối"], lang="Ngôn ngữ", nav="Điều hướng chính",
               note="Bản tiếng Anh có đủ 76 bài và 7 khóa. Trang chưa có bản tiếng Anh: {missing}. Bấm English ở những trang này sẽ về trang chủ tiếng Anh."),
    "en": dict(home="/en/index.html", aa="Text size, theme, language", size="Text size", sizes=["Small", "Medium", "Large", "Extra large"],
               theme="Theme", themes=["System", "Light", "Dark"], lang="Language", nav="Main navigation",
               note="English covers all 76 lessons and 7 courses. Vietnamese-only pages: {missing}."),
}
# Chạy trước khi vẽ trang: áp cỡ chữ và màu nền đã chọn, tránh nháy màn hình
PRE = ("<script>try{var s=JSON.parse(localStorage.getItem('" + KEY + "'))||{},d=document.documentElement;"
       "d.setAttribute('data-size',s.size||'m');if(s.theme==='dark'||(s.theme!=='light'&&matchMedia('(prefers-color-scheme: dark)').matches))"
       "d.setAttribute('data-dark','')}catch(e){}</script>")

HREF = re.compile(r'(href|src|action)="([^"]*)"')
ABS = re.compile(r"^https?://(www\.)?kynanglamviec\.com(/[^\"]*)?$")


def lang_of(rel: str) -> str:
    return "en" if rel.startswith("en/") else "vi"


def tab_of(rel: str) -> str:
    r = rel[3:] if rel.startswith("en/") else rel
    if r == "index.html":
        return "home"
    if rel.startswith("sach/"):
        return "sach"
    if rel.startswith("ky-nang/"):  # bản tiếng Việt không có tab Kỹ năng (nhường chỗ cho tab Sách)
        return "path"
    for key, pres in (("path", ("lo-trinh/", "paths/", "tai-nguyen/", "resources/")), ("skill", ("ky-nang/", "skills/")),
                      ("book", ("bai-hoc/", "lessons/")), ("mine", ("cua-toi/", "mine/", "tu-danh-gia/", "self-assessment/", "nhat-ky/", "journal/"))):
        if r.startswith(pres):
            return key
    return ""


def to_index(url: str) -> str:
    path, sep, tail = re.match(r"^([^?#]*)([?#]?)(.*)$", url).groups()
    if not path:
        return url  # chỉ có #neo hoặc ?tham số
    if path in (".", "./"):
        path = "index.html"
    elif path == "..":
        path = "../index.html"
    elif path.endswith("/"):
        path += "index.html"
    return f"{path}{sep}{tail}"


def abs_path(rel: str, url: str) -> str:
    """Đường dẫn tuyệt đối (bắt đầu bằng /) của link tương đối trên trang rel."""
    base = posixpath.dirname("/" + rel)
    path = url.split("#")[0].split("?")[0]
    p = posixpath.normpath(posixpath.join(base, path)) if not path.startswith("/") else posixpath.normpath(path)
    if path.endswith("/") or path in ("", ".", ".."):
        p = p.rstrip("/") + "/index.html"
    return p.replace("//", "/")


def buttons(vals, labels):
    return "".join(f'<button type="button" data-v="{v}">{l}</button>' for v, l in zip(vals, labels))


def chrome(rel: str, vi_url: str, en_url: str, missing: dict):
    lang = lang_of(rel)
    t, cur = T[lang], tab_of(rel)
    on = ' aria-current="true"'
    top = (
        f'<header class="app-top"><a class="app-brand" href="{t["home"]}">'
        f'<img src="/assets/logo-icon.svg" alt="" width="34" height="34"><span>{APP_NAME if lang == "vi" else "Work Skills"}</span></a>'
        f'<button type="button" class="app-aa" id="app-aa" aria-label="{t["aa"]}" aria-expanded="false">Aa</button></header>'
        '<div class="app-panel" id="app-panel" hidden>'
        f'<p><strong>{t["size"]}</strong></p><div class="app-row" id="app-size">{buttons("s m l xl".split(), t["sizes"])}</div>'
        f'<p><strong>{t["theme"]}</strong></p><div class="app-row" id="app-theme">{buttons("auto light dark".split(), t["themes"])}</div>'
        f'<p><strong>{t["lang"]}</strong></p><div class="app-row" id="app-lang">'
        f'<a href="{vi_url}" data-v="vi" lang="vi"{on if lang == "vi" else ""}>Tiếng Việt</a>'
        f'<a href="{en_url}" data-v="en" lang="en"{on if lang == "en" else ""}>English</a></div>'
        f'<p class="small muted">{html.escape(t["note"].format(missing=missing[lang]))}</p></div>'
    )
    page_on = ' aria-current="page"'
    items = "".join(
        f'<a href="{href}"{page_on if key == cur else ""}>'
        f'<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" fill="none" stroke="currentColor" '
        f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[key]}</svg><span>{label}</span></a>'
        for key, label, href in TABS[lang]
    )
    return top, f'<nav class="app-tabs" aria-label="{t["nav"]}">{items}</nav>'


def alt_urls(text: str, rel: str):
    """Trang tương ứng ở ngôn ngữ kia, theo nút ngôn ngữ ở header của site."""
    lang = lang_of(rel)
    m = re.search(r'<a class="lang" href="([^"]*)"', text)
    other = abs_path(rel, m.group(1)) if m else ("/index.html" if lang == "en" else "/en/index.html")
    if not (SRC / other.lstrip("/")).exists() and other.lstrip("/") not in EXTRA:
        other = "/index.html" if lang == "en" else "/en/index.html"
    here = "/" + rel
    return (here, other) if lang == "vi" else (other, here)


def fix_link(rel: str):
    def sub(m):
        attr, url = m.group(1), m.group(2)
        if not url or re.match(r"^(mailto:|tel:|sms:|#|data:|javascript:)", url):
            return m.group(0)
        a = ABS.match(url)
        if a:  # link tuyệt đối tới site: dùng trang trong app nếu có
            local = to_index(a.group(2) or "/")
            if (SRC / local.split("#")[0].lstrip("/")).exists() or local.lstrip("/").split("#")[0] in EXTRA:
                return f'{attr}="{local}"'
            return m.group(0)
        if re.match(r"^https?:", url):
            return m.group(0)
        if attr == "href" and url.split("#")[0].endswith(".csv"):  # WebView không tải tệp được: mở web
            return f'href="{SITE}{abs_path(rel, url)}" target="_blank" rel="noopener"'
        return f'{attr}="{to_index(url)}"'
    return sub


def transform(text: str, rel: str, missing: dict) -> str:
    vi_url, en_url = alt_urls(text, rel)
    top, bottom = chrome(rel, vi_url, en_url, missing)
    text = re.sub(r'<header class="top">.*?</header>', lambda m: top, text, count=1, flags=re.S)
    text = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\s*', "", text)
    text = re.sub(r'(<link rel="stylesheet" href="[^"]*assets/style\.css">)',
                  lambda m: m.group(1) + '\n<link rel="stylesheet" href="/app/app.css">\n' + PRE, text, count=1)
    text = text.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
                        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">')
    text = text.replace('"_suffix": ""', '"_suffix": "index.html"')  # link bài trong bảng kết quả tự đánh giá
    text = text.replace("</body>", f'{bottom}\n<script src="/app/index.js"></script>\n<script src="/app/app.js"></script>\n</body>')
    text = HREF.sub(fix_link(rel), text)
    return text


MINE = {
    "vi": ("Của tôi", "Mọi thứ ở đây chỉ nằm trên máy của bạn. App không gửi dữ liệu đi đâu."),
    "en": ("My learning", "Everything here stays on your phone. The app sends no data anywhere."),
}
EXTRA = {"cua-toi/index.html": "vi", "en/mine/index.html": "en"}  # trang riêng của app (sách thêm vào lúc chạy)


def shell_page(lang: str, title: str, main_html: str, other: str, up: int = 1) -> str:
    """Trang riêng của app: lấy khung (head, footer) từ trang chủ cùng ngôn ngữ, thay phần main. Trang nằm sâu hơn trang chủ một cấp."""
    home = (SRC / ("en/index.html" if lang == "en" else "index.html")).read_text(encoding="utf-8")
    home = re.sub(r'(href|src)="(?!https?:|/|#|mailto:)([^"]*)"', lambda m: f'{m.group(1)}="{"../" * up}{m.group(2)}"', home)
    home = re.sub(r"<main.*?</main>", lambda m: f'<main id="main" class="wrap">\n{main_html}\n</main>', home, count=1, flags=re.S)
    home = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} · {APP_NAME}</title>", home, count=1)
    return re.sub(r'<a class="lang" href="[^"]*"', f'<a class="lang" href="{other}"', home, count=1)


def mine_page(lang: str) -> str:
    h1, lead = MINE[lang]
    return shell_page(lang, h1, f'<h1>{h1}</h1>\n<p class="lead">{lead}</p>\n<div id="app-mine"></div>', "/en/mine/" if lang == "vi" else "/cua-toi/")


def load_sach():
    f = SACH / "sach.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def sach_pages(book):
    """Trang mục lục /sach/ và 20 trang chương /sach/chuong-NN/ (chỉ tiếng Việt)."""
    pages, chs = {}, book["chapters"]
    rows, cur = [], None
    for c in chs:
        if c["part"] != cur:
            cur = c["part"]
            pt = book["parts"][str(cur)]
            rows.append(f'<h2 class="sach-part" style="--pa:{pt["color"]}">{html.escape(pt["name"])}</h2>'
                        + "".join(f'<p class="sach-intro">{html.escape(x)}</p>' for x in pt["intro"]))
        rows.append(f'<a class="card sach-card" href="/sach/chuong-{c["n"]:02d}/"><img src="/sach/tranh/c{c["n"]:02d}.webp" alt="" width="72" height="107" loading="lazy">'
                    f'<span><span class="tag">Chương {c["n"]} · {html.escape(c["where"])} · {html.escape(c["skill"].split(" · ")[0])}</span>'
                    f'<strong>{html.escape(c["title"])}</strong></span></a>')
    src = "".join(f"<p>{x}</p>" for x in book["sources"])
    index = f"""<figure class="sach-cover"><img src="/sach/tranh/bia.webp" alt="" width="900" height="1334"></figure>
<p class="eyebrow">Sách cho cả nhà · {html.escape(book["author"])} kể</p>
<h1>{html.escape(book["title"])}</h1>
<p class="lead">{html.escape(book["sub"])}. Hai mươi chương, mỗi chương dẫn tới một bài học trong app.</p>
<p class="small muted">Truyện hư cấu. Nơi chốn và vấn đề là thật; tổ chức và nhân vật phụ do tác giả đặt ra. Chữ và tranh có AI hỗ trợ; tranh không phải chân dung người thật.</p>
{chr(10).join(rows)}
<details class="sach-src"><summary>Nguồn dữ kiện trong Góc người lớn</summary>{src}</details>
"""
    pages["sach/index.html"] = shell_page("vi", book["title"], index, "/en/")
    for i, c in enumerate(chs):
        n = c["n"]
        body = (SACH / f"c{n:02d}.html").read_text(encoding="utf-8")
        if c.get("opener"):
            body = f'<div class="sach-opener">{c["opener"]}</div>\n' + body
        nav = ""
        if i > 0:
            nav += f'<a class="prev" href="/sach/chuong-{chs[i-1]["n"]:02d}/">← Chương {chs[i-1]["n"]}</a>'
        if i < len(chs) - 1:
            nav += f'<a class="next" href="/sach/chuong-{chs[i+1]["n"]:02d}/">Chương {chs[i+1]["n"]}: {html.escape(chs[i+1]["title"])} →</a>'
        else:
            nav += '<a class="next" href="/sach/">Về mục lục sách</a>'
        main = (f'<article class="sach-chapter" data-slug="sach-c{n:02d}" data-title="Chương {n}. {html.escape(c["title"])}" '
                f'style="--pa:{book["parts"][str(c["part"])]["color"]}">\n{body}<nav class="pager sach-pager">{nav}</nav>\n</article>')
        pages[f"sach/chuong-{n:02d}/index.html"] = shell_page("vi", f'Chương {n}. {c["title"]}', main, "/en/", up=2)
    return pages


def strip(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def course_index():
    """Khóa = Bản đồ khóa trên trang nhóm. Thứ tự bài theo thứ tự link trên bản đồ."""
    out = []
    for base, prefix, lang in (("lo-trinh", "/lo-trinh/", "vi"), ("en/paths", "/en/paths/", "en")):
        for d in sorted((SRC / base).iterdir()):
            f = d / "index.html"
            if not f.exists():
                continue
            text = f.read_text(encoding="utf-8")
            m = re.search(r"<h2>([^<]*)</h2>\s*(?:<p>.*?</p>\s*)?<ol class=\"coursemap\">(.*?)</ol>", text, flags=re.S)
            if not m:
                continue
            title = re.sub(r"^(Bản đồ |Course map: |Map of the )", "", strip(m.group(1)))
            lessons = []
            for slug, href, short in re.findall(r'<li data-lesson="([^"]+)"><a href="([^"]+)"><b>(.*?)</b>', m.group(2)):
                p = abs_path(f"{base}/{d.name}/index.html", href).replace("index.html", "")
                lessons.append([p, strip(short), slug])
            out.append(dict(p=f"{prefix}{d.name}/", t=title, g=lang, code=d.name.upper(), l=lessons))
    return out


def lesson_list():
    """Mọi bài (cho tìm kiếm): đường dẫn, tiêu đề, dòng meta, slug, ngôn ngữ."""
    out = []
    for base, prefix, lang in (("bai-hoc", "/bai-hoc/", "vi"), ("en/lessons", "/en/lessons/", "en")):
        for d in sorted((SRC / base).iterdir()):
            f = d / "index.html"
            if not f.exists():
                continue
            text = f.read_text(encoding="utf-8")
            a = re.search(r'<article class="lesson" data-lesson="([^"]+)" data-title="([^"]*)"', text)
            if not a:
                continue
            meta = re.search(r'<p class="crumb">(.*?)</p>', text, flags=re.S)
            out.append([f"{prefix}{d.name}/", html.unescape(a.group(2)), strip(meta.group(1)) if meta else "", a.group(1), lang])
    return out


def other_pages(lang: str):
    """Trang chính khác (kỹ năng, nhóm, tài nguyên...) cho tìm kiếm."""
    out = []
    base = SRC / "en" if lang == "en" else SRC
    for f in sorted(base.rglob("index.html")):
        rel = f.relative_to(SRC).as_posix()
        if lang == "vi" and rel.startswith("en/"):
            continue
        if re.match(r"^(en/)?(bai-hoc|lessons)/[^/]+/", rel):
            continue
        m = re.search(r"<h1[^>]*>(.*?)</h1>", f.read_text(encoding="utf-8"), flags=re.S)
        if m:
            out.append(["/" + rel.replace("index.html", ""), strip(m.group(1)), lang])
    return out


def vi_only():
    """Trang tiếng Việt không có bản tiếng Anh (nút English trỏ về trang chủ EN)."""
    names = []
    for f in sorted(SRC.rglob("index.html")):
        rel = f.relative_to(SRC).as_posix()
        if rel.startswith("en/") or rel == "index.html":
            continue
        m = re.search(r'<a class="lang" href="([^"]*)"', f.read_text(encoding="utf-8"))
        if m and abs_path(rel, m.group(1)) == "/en/index.html":
            h = re.search(r"<h1[^>]*>(.*?)</h1>", f.read_text(encoding="utf-8"), flags=re.S)
            names.append(strip(h.group(1)) if h else rel)
    return names


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    missing_vi = vi_only()
    missing = {"vi": ", ".join(missing_vi) or "không có", "en": ", ".join(missing_vi) or "none"}
    n = 0
    for f in sorted(SRC.rglob("*")):
        rel = f.relative_to(SRC)
        if f.is_dir() or rel.name in SKIP_FILES:
            continue
        dst = OUT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if f.suffix == ".html":
            dst.write_text(transform(f.read_text(encoding="utf-8"), rel.as_posix(), missing), encoding="utf-8")
            n += 1
        else:
            shutil.copy2(f, dst)
    book = load_sach()
    extra = {rel: mine_page(lang) for rel, lang in EXTRA.items()}
    if book:
        sp = sach_pages(book)
        EXTRA.update({rel: "vi" for rel in sp})
        extra.update(sp)
        (OUT / "sach" / "tranh").mkdir(parents=True, exist_ok=True)
        for img in SACH.glob("*.webp"):
            shutil.copy2(img, OUT / "sach" / "tranh" / img.name)
    for rel, text in extra.items():
        dst = OUT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(transform(text, rel, missing), encoding="utf-8")
        n += 1

    courses = course_index()
    lessons = lesson_list()
    if book:  # sách = một "khóa" tiếng Việt: dùng chung tiến độ, đọc tiếp, tìm kiếm
        chs = [[f'/sach/chuong-{c["n"]:02d}/', f'Chương {c["n"]}. {c["title"]}', f'sach-c{c["n"]:02d}', c["lesson"]] for c in book["chapters"]]
        courses.append(dict(p="/sach/", t=book["title"], g="vi", code="SACH", book=1, l=[x[:3] for x in chs]))
        lessons += [[x[0], x[1], f'{book["title"]} · ' + x[1].split(".")[0], x[2], "vi"] for x in chs]
    data = dict(courses=courses, lessons=lessons, pages=other_pages("vi") + other_pages("en"),
                book={x[3]: [x[0], x[1]] for x in chs} if book else {})
    (OUT / "app").mkdir(exist_ok=True)
    (OUT / "app" / "index.js").write_text("window.KLV=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8")
    for name in ("app.css", "app.js"):
        shutil.copy2(ROOT / "shell" / name, OUT / "app" / name)

    size = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    in_course = sum(len(c["l"]) for c in courses)
    print(f"{n} trang, {len(courses)} khóa ({in_course} bài trong khóa), {len(lessons)} bài, {size / 1e6:.1f} MB -> {OUT}")
    print("Trang chỉ có tiếng Việt:", missing["vi"])


if __name__ == "__main__":
    main()
