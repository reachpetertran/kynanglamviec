#!/usr/bin/env python3
"""Bộ sinh trang tĩnh cho kynanglamviec.com.

Nguồn nội dung duy nhất:
  data/*.yaml              khung: bậc, kỹ năng, nhóm
  content/bai-hoc/*.md     bài học (YAML front matter + 9 phần)
  content/cau-hoi/*.yaml   câu hỏi tự kiểm tra của từng bài

Chạy:
  python3 _build/build.py              -> public/   (để đăng lên Cloudflare Pages)
  python3 _build/build.py --preview    -> preview/  (liên kết trỏ thẳng index.html, xem offline)
"""
import html, re, shutil, sys, datetime
from pathlib import Path
import markdown, yaml

ROOT = Path(__file__).resolve().parent.parent
PREVIEW = "--preview" in sys.argv
OUT = ROOT / ("preview" if PREVIEW else "public")
SITE = "https://kynanglamviec.com"
SITE_NAME = "Kỹ Năng Làm Việc"
TODAY = datetime.date.today().isoformat()

e = lambda s: html.escape(str(s), quote=True)


def load_yaml(p):
    return yaml.safe_load((ROOT / p).read_text(encoding="utf-8"))


LV = load_yaml("data/levels.yaml")
LEVELS = {l["n"]: l for l in LV["levels"]}
RATING = LV["self_rating"]
SK = load_yaml("data/skills.yaml")
CLUSTERS = {c["id"]: c["name"] for c in SK["clusters"]}
SKILLS = SK["skills"]
SKILL = {s["code"]: s for s in SKILLS}
GROUPS = load_yaml("data/groups.yaml")["groups"]
GROUP = {g["code"]: g for g in GROUPS}
MARK = {"-": ("—", "Không dạy"), "o": ("○", "Giới thiệu"), "c": ("●", "Trọng tâm"), "a": ("◆", "Nâng cao")}


def md_to_html(text):
    return markdown.markdown(text, extensions=["tables", "md_in_html", "attr_list", "sane_lists"])


def load_lessons():
    out = []
    for f in sorted((ROOT / "content/bai-hoc").glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        meta, body = yaml.safe_load(m.group(1)), m.group(2)
        qf = ROOT / "content/cau-hoi" / f"{meta['slug']}.yaml"
        meta["quiz"] = yaml.safe_load(qf.read_text(encoding="utf-8"))["questions"] if qf.exists() else []
        meta["body"] = body
        out.append(meta)
    return sorted(out, key=lambda l: l.get("order", 99))


LESSONS = load_lessons()
LESSON = {l["slug"]: l for l in LESSONS}

# ---------------------------------------------------------------- khung trang
NAV = [("lo-trinh/", "Lộ trình"), ("ky-nang/", "Kỹ năng"), ("bai-hoc/", "Bài học"),
       ("tu-danh-gia/", "Tự đánh giá"), ("tai-nguyen/", "Tài nguyên"), ("gioi-thieu/", "Giới thiệu")]


def page(path, title, body, desc="", wide=False):
    """path: 'ky-nang/k1/' hoặc '' cho trang chủ, hoặc '404.html'."""
    depth = 0 if path in ("", "404.html") else path.strip("/").count("/") + 1
    p = "../" * depth if not path == "404.html" else "/"
    if PREVIEW and path == "404.html":
        p = ""
    body = body.replace("{{R}}", p)
    nav = "".join(
        f'<a href="{p}{href}"{" aria-current=page" if path.startswith(href) else ""}>{label}</a>'
        for href, label in NAV)
    full_title = f"{title} · {SITE_NAME}" if path else f"{SITE_NAME} – kỹ năng làm việc theo lộ trình nghề nghiệp"
    canon = f"{SITE}/{path}" if path != "404.html" else SITE + "/"
    doc = f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc or 'Học miễn phí kỹ năng làm việc theo lộ trình nghề nghiệp, từ học sinh đến quản lý. Không đăng nhập, không theo dõi.')}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{p}assets/style.css">
<script src="{p}assets/js-on.js"></script>
<script src="{p}assets/app.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Bỏ qua, đến nội dung</a>
<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="{p or './'}"><span class="logo" aria-hidden="true">K</span><span>Kỹ Năng<br>Làm Việc</span></a>
    <nav class="nav" aria-label="Chính">{nav}</nav>
  </div>
</header>
<main id="main" class="wrap{' wide' if wide else ''}">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <p><b>kynanglamviec.com</b> – miễn phí, công khai, không đăng nhập, không cookie, không công cụ theo dõi.
    Tiến độ học chỉ lưu trên máy của bạn.</p>
    <p>Trang cùng hệ: <a href="https://daynentang.com/">daynentang.com</a> (giá trị, thói quen) ·
    <a href="https://tamhonkhoe.com/">tamhonkhoe.com</a> (tinh thần) ·
    <a href="https://trachnhiemxahoi.com/">trachnhiemxahoi.com</a> (quyền con người) ·
    <a href="https://tienganhcanban.com/">tienganhcanban.com</a> (tiếng Anh)</p>
    <p><a href="{p}khung-tham-chieu/">Khung tham chiếu</a> · <a href="{p}phap-ly/">Pháp lý khi đi làm</a> ·
    <a href="{p}nhat-ky/">Nhật ký bằng chứng</a> · Nội dung tự viết: CC BY-NC-SA 4.0 · Cập nhật {TODAY}</p>
  </div>
</footer>
</body>
</html>
"""
    if PREVIEW:  # liên kết thư mục -> index.html để mở được ngoài máy chủ
        doc = re.sub(r'href="(?!https?:|mailto:|#)([^"]*/)"', r'href="\1index.html"', doc)
        doc = doc.replace('href="./"', 'href="index.html"')
    dest = OUT / (path if path.endswith(".html") else path + "index.html")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    PAGES.append(path)


PAGES = []

# ---------------------------------------------------------------- mảnh dùng chung


def skill_link(code, R="{{R}}"):
    s = SKILL[code]
    return f'<a href="{R}ky-nang/{s["slug"]}/">{s["code"]} · {e(s["name"])}</a>'


def lesson_card(l):
    s = SKILL[l["skill"]]
    groups = ", ".join(l["group"])
    draft = '<span class="tag draft">Bản nháp</span>' if l.get("status") == "draft" else ""
    return f"""<li class="card lesson-card" data-lesson="{e(l['slug'])}">
  <a href="{{{{R}}}}bai-hoc/{e(l['slug'])}/"><b>{e(l['title'])}</b></a>
  <span class="meta">{s['code']} · Bậc {l['level']} {e(LEVELS[l['level']]['name'])} · {groups} · {l['minutes']} phút</span>
  {draft}<span class="done-flag" hidden>✓ Đã học</span>
</li>"""


def lessons_list(ls, empty="Bài học đang được biên soạn."):
    if not ls:
        return f'<p class="muted">{empty}</p>'
    return '<ul class="cards">' + "".join(lesson_card(l) for l in ls) + "</ul>"


def mark(sym, note=""):
    s, label = MARK[sym]
    t = f' <span class="muted">{e(note)}</span>' if note else ""
    return f'<span class="mk mk-{sym}" title="{label}">{s}</span> {label}{t}'


# ---------------------------------------------------------------- trang chủ
def build_home():
    groups = "".join(f"""<a class="card group-card" href="{{{{R}}}}lo-trinh/{g['slug']}/">
  <span class="gcode">{g['code']}</span><b>{e(g['name'])}</b><span>{e(g['short'])}</span>
  <span class="meta">{e(g['levels'])}</span></a>""" for g in GROUPS)
    by_cluster = ""
    for cid, cname in CLUSTERS.items():
        items = "".join(f'<li>{skill_link(s["code"])}</li>' for s in SKILLS if s["cluster"] == cid)
        by_cluster += f'<div class="cluster"><h3>{cid}. {e(cname)}</h3><ul>{items}</ul></div>'
    body = f"""
<section class="hero">
  <h1>Kỹ năng làm việc, học theo lộ trình nghề nghiệp</h1>
  <p class="lead">Từ học sinh khám phá nghề đến người quản lý dẫn dắt đội. Miễn phí, không cần đăng nhập.
  Mỗi bài 10–20 phút, có tình huống tại nơi làm việc Việt Nam và câu hỏi tự kiểm tra.</p>
  <p><a class="btn" href="{{{{R}}}}tu-danh-gia/">Tự đánh giá kỹ năng</a>
     <a class="btn ghost" href="{{{{R}}}}bai-hoc/">Xem bài học</a></p>
</section>

<h2>Bạn đang ở đâu trên đường nghề nghiệp?</h2>
<p>Chọn nhóm gần với bạn nhất. Đây chỉ là lộ trình gợi ý: mọi bài đều mở, bạn tự chọn bậc cho từng kỹ năng.</p>
<div class="grid5">{groups}</div>

<h2>10 kỹ năng, 5 cụm</h2>
<p>Mỗi kỹ năng có 5 bậc: {" → ".join(f"{n}. {e(l['name'])}" for n, l in LEVELS.items())}.</p>
<div class="clusters">{by_cluster}</div>

<h2>Học thế nào cho nhớ lâu?</h2>
<div class="cols2">
  <div class="card"><b>Tự kiểm tra</b><p>Mỗi bài có câu hỏi tình huống. Cố nhớ lại câu trả lời giúp nhớ lâu hơn đọc lại.</p></div>
  <div class="card"><b>Ôn giãn cách</b><p>Học xong, ôn lại sau 1, 3 và 7 ngày. Site tạo sẵn file nhắc lịch cho bạn.</p></div>
</div>
<p class="muted small">Căn cứ: Dunlosky và cộng sự (2013), tổng quan về các kỹ thuật học tập,
<a href="https://journals.sagepub.com/doi/abs/10.1177/1529100612453266">Psychological Science in the Public Interest</a>.
Đọc lại và tô đậm không nằm trong nhóm kỹ thuật hiệu quả cao.</p>

<h2>Bài học mới</h2>
{lessons_list(LESSONS[:6])}
"""
    page("", SITE_NAME, body)


# ---------------------------------------------------------------- lộ trình
def build_groups():
    cards = "".join(f"""<a class="card group-card" href="{g['slug']}/">
  <span class="gcode">{g['code']}</span><b>{e(g['name'])}</b><span>{e(g['short'])}</span>
  <span class="meta">{e(g['levels'])}</span></a>""" for g in GROUPS)
    page("lo-trinh/", "Lộ trình", f"""<h1>Lộ trình theo nhóm người học</h1>
<p class="lead">Bảy lộ trình gợi ý. Không có nội dung nào bị khóa. Một người có thể ở bậc khác nhau tùy kỹ năng.</p>
<div class="grid5">{cards}</div>""")

    for g in GROUPS:
        rows = "".join(
            f"<tr><td>{skill_link(code)}</td><td>{mark(*g['matrix'][code])}</td></tr>" for code in SKILL)
        ls = [l for l in LESSONS if g["code"] in l["group"]]
        modules = "".join(f"<li>{e(m)}</li>" for m in g["modules"])
        note = f'<p class="note">{e(g["note"])}</p>' if g.get("note") else ""
        extra = ""
        if g["code"] in ("N2", "N3", "N4", "N5", "N6", "N7"):
            extra = course_map(g["slug"])
        if g["code"] == "N1":
            extra = course_map("n1") + """<div class="note"><b>Dành cho phụ huynh và giáo viên.</b> Các bài N1 được viết để người lớn
dẫn trẻ học. Không có trắc nghiệm chọn nghề. Site không thu dữ liệu của trẻ.
Bài nhật ký và tự đánh giá không dành cho trẻ tự dùng.</div>"""
        body = f"""<p class="crumb"><a href="{{{{R}}}}lo-trinh/">Lộ trình</a> › {g['code']}</p>
<h1><span class="gcode">{g['code']}</span> {e(g['name'])}</h1>
<p class="lead">{e(g['intro'])}</p>
<p><b>Dành cho:</b> {e(g['audience'])}<br><b>Bậc trọng tâm:</b> {e(g['levels'])}</p>
{note}{extra}
<h2>Học phần gợi ý</h2>
<ol class="modules">{modules}</ol>
{group_lessons(g, ls)}
<h2>Kỹ năng trọng tâm của nhóm</h2>
<table class="matrix"><thead><tr><th>Kỹ năng</th><th>Mức độ</th></tr></thead><tbody>{rows}</tbody></table>
<p class="muted small">— không dạy · ○ giới thiệu · ● trọng tâm · ◆ nâng cao</p>
"""
        page(f"lo-trinh/{g['slug']}/", f"{g['code']} {g['name']}", body, desc=g["intro"][:150])


def group_lessons(g, ls):
    c = g["slug"]
    if c in COURSES and course_lessons(c):
        rest = [l for l in ls if l.get("course") != c]
        if not rest:
            return ""
        return ("<h2>Bài học thêm cho nhóm</h2><p>Các bài này ngoài khóa, học theo nhu cầu.</p>"
                + lessons_list(rest))
    return "<h2>Bài học đã có</h2>" + lessons_list(ls)


def course_map(c):
    cl = course_lessons(c)
    if not cl:
        return ""
    C = COURSES[c]
    steps = "".join(
        f'<li data-lesson="{e(l["slug"])}"><a href="{{{{R}}}}bai-hoc/{e(l["slug"])}/"><b>Bài {i}. {e(l.get("short", l["title"]))}</b>'
        f'<span>{e(l.get("hook", ""))}</span><span class="meta">{SKILL[l["skill"]]["code"]} · Bậc {l["level"]} · {l["minutes"]} phút'
        f'{" · " + e(l["age"]) if l.get("age") else ""}</span></a></li>' for i, l in enumerate(cl, 1))
    return f"""<h2>Bản đồ {e(C["title"])}</h2>
<p>Khóa có {len(cl)} bài, học theo thứ tự. {C["thread"]}</p>
<ol class="coursemap">{steps}</ol>
{C.get("after", "")}
<p><a class="btn" href="{{{{R}}}}bai-hoc/{cl[0]['slug']}/">Bắt đầu Bài 1</a>
<a class="btn ghost" href="{{{{R}}}}{C["guide"]}">{e(C["guide_label"])}</a></p>
"""


# ---------------------------------------------------------------- kỹ năng
def build_skills():
    rows = ""
    for cid, cname in CLUSTERS.items():
        for s in [s for s in SKILLS if s["cluster"] == cid]:
            rows += f"""<tr><td>{cid}. {e(cname)}</td><td><a href="{s['slug']}/"><b>{s['code']}</b> {e(s['name'])}</a></td>
<td>{e(s['summary'])}</td></tr>"""
    page("ky-nang/", "10 kỹ năng", f"""<h1>10 kỹ năng làm việc</h1>
<p class="lead">Mỗi kỹ năng có 5 bậc, mô tả bằng câu "Tôi có thể…". Dùng chúng để tự đánh giá và chọn bài.</p>
<table class="matrix"><thead><tr><th>Cụm</th><th>Kỹ năng</th><th>Nội dung</th></tr></thead><tbody>{rows}</tbody></table>""")

    for s in SKILLS:
        lv = ""
        for n, stmts in s["levels"].items():
            li = "".join(f"<li>{e(x)}</li>" for x in stmts)
            lv += f"""<div class="level"><h3><span class="lvn">Bậc {n}</span> {e(LEVELS[n]['name'])}</h3>
<p class="muted small">{e(LEVELS[n]['desc'])}</p><ul>{li}</ul>
{lessons_list([l for l in LESSONS if l['skill'] == s['code'] and l['level'] == n], empty='Chưa có bài ở bậc này.')}</div>"""
        focus = "".join(
            f"<tr><td><a href=\"{{{{R}}}}lo-trinh/{g['slug']}/\">{g['code']}</a> {e(g['name'])}</td><td>{mark(*g['matrix'][s['code']])}</td></tr>"
            for g in GROUPS)
        cl = s.get("crosslink")
        cross = f'<p class="note">{e(cl["note"])} <a href="{cl["url"]}">Đến {cl["site"]}</a></p>' if cl else ""
        fm = "".join(f"<li>{e(x)}</li>" for x in s["framework_map"])
        body = f"""<p class="crumb"><a href="{{{{R}}}}ky-nang/">Kỹ năng</a> › {s['code']}</p>
<h1><span class="gcode">{s['code']}</span> {e(s['name'])}</h1>
<p class="lead">{e(s['summary'])}</p>
<p class="muted">Cụm {s['cluster']}. {e(CLUSTERS[s['cluster']])} · Năng lực chung GDPT 2018: {e(s['gdpt'])}</p>
{cross}
<h2>5 bậc của kỹ năng</h2>
{lv}
<p><a class="btn" href="{{{{R}}}}tu-danh-gia/#{s['code']}">Tự đánh giá {s['code']}</a></p>
<h2>Mức độ theo nhóm người học</h2>
<table class="matrix"><tbody>{focus}</tbody></table>
<h2>Khung quốc tế đối chiếu</h2>
<ul class="small">{fm}</ul>
<p class="muted small">Tên khung chỉ để dẫn chiếu. Nội dung và câu "Tôi có thể…" do site tự viết.
Xem <a href="{{{{R}}}}khung-tham-chieu/">Khung tham chiếu</a>.</p>
"""
        page(f"ky-nang/{s['slug']}/", f"{s['code']} {s['name']}", body, desc=s["summary"])


# ---------------------------------------------------------------- bài học
def quiz_html(l):
    if not l["quiz"]:
        return '<p class="muted">Câu hỏi đang được biên soạn.</p>'
    out = f'<div class="quiz" data-lesson="{e(l["slug"])}">'
    for i, q in enumerate(l["quiz"], 1):
        opts = ""
        for j, o in enumerate(q["options"]):
            ok = "1" if o["correct"] else "0"
            label = "Đúng" if o["correct"] else "Chưa đúng"
            opts += f"""<li><button type="button" class="opt" data-correct="{ok}">{chr(65 + j)}. {e(o['text'])}</button>
<p class="why why-{ok}"><b>{label}.</b> {e(o['why'])}</p></li>"""
        out += f'<div class="q"><p class="q-prompt"><b>Câu {i}.</b> {e(q["prompt"])}</p><ul class="opts">{opts}</ul></div>'
    return out + '<p class="quiz-score" aria-live="polite"></p></div>'


def meta_table(l):
    s = SKILL[l["skill"]]
    fm = "; ".join(l["framework_map"])
    return f"""<table class="meta-table small"><tbody>
<tr><th>skill</th><td>{s['code']} · {e(s['name'])}</td></tr>
<tr><th>level</th><td>Bậc {l['level']} · {e(LEVELS[l['level']]['name'])}</td></tr>
<tr><th>group</th><td>{", ".join(l['group'])}</td></tr>
<tr><th>framework_map</th><td>{e(fm)} (chỉ dẫn chiếu)</td></tr>
<tr><th>updated</th><td>{l['updated']}</td></tr></tbody></table>"""


COURSES = {
    "n1": {"title": "Khóa Khám phá nghề (N1)", "home": "lo-trinh/n1/", "guide": "tai-nguyen/n1/",
           "guide_label": "Hướng dẫn và mẫu in cho người lớn", "strip_label": "Hướng dẫn cho người lớn",
           "thread": "Một sợi chỉ nối cả khóa: <b>Thẻ nghề</b>. Bài 1 làm thẻ, mỗi bài sau điền thêm hoặc dùng thẻ, bài cuối trưng bày tất cả."},
    "n2": {"title": "Khóa Chuẩn bị đi làm (N2)", "home": "lo-trinh/n2/", "guide": "tai-nguyen/n2/",
           "guide_label": "Mẫu in của khóa", "strip_label": "Mẫu in",
           "thread": "Một sợi chỉ nối cả khóa: <b>Hồ sơ sẵn sàng đi làm</b>, gồm 6 tờ. Mỗi bài làm xong một tờ. Bài cuối kiểm tra chéo cả hồ sơ.",
           "after": '<p class="note"><b>Sắp có:</b> bài "Quyền và an toàn khi đi làm thêm, thực tập". Bài sẽ viết sau khi Quốc hội biểu quyết luật sửa đổi Bộ luật Lao động, để dẫn đúng văn bản đang có hiệu lực.</p>'},
    "n3": {"title": "Khóa 90 ngày đầu (N3)", "home": "lo-trinh/n3/", "guide": "tai-nguyen/n3/",
           "guide_label": "Mẫu in của khóa", "strip_label": "Mẫu in",
           "thread": "Một sợi chỉ nối cả khóa: <b>Sổ tay 90 ngày</b>, gồm 6 tờ dùng hằng ngày ở chỗ làm. Bài cuối gom các tờ thành hồ sơ cho buổi đánh giá.",
           "after": '<p class="note"><b>Học thêm:</b> các bài N3 ở mục bên dưới (kế hoạch 90 ngày, báo cáo tiến độ, xin phản hồi, dùng AI an toàn, đề xuất cải tiến) bổ sung cho khóa. <b>Sắp có:</b> bài "Hợp đồng, thử việc và nội quy", viết sau khi Quốc hội biểu quyết luật sửa đổi Bộ luật Lao động.</p>'},
    "n4": {"title": "Khóa Senior, chuyên gia (N4)", "home": "lo-trinh/n4/", "guide": "tai-nguyen/n4/",
           "guide_label": "Mẫu in của khóa", "strip_label": "Mẫu in",
           "thread": "Một sợi chỉ nối cả khóa: <b>Sổ công cụ chuyên gia</b>, gồm 8 tờ dùng với việc thật. Bài cuối ôn trộn cả khóa và lập kế hoạch nghề 1–3 năm.",
           "after": '<p class="note"><b>Lưu ý:</b> Bài 7 dạy cách đọc và áp dụng văn bản quy định, không phải tư vấn pháp lý. Nguồn pháp luật trong bài ghi rõ ngày tra.</p>'},
    "n5": {"title": "Khóa Quản lý, trưởng nhóm (N5)", "home": "lo-trinh/n5/", "guide": "tai-nguyen/n5/",
           "guide_label": "Mẫu in của khóa", "strip_label": "Mẫu in",
           "thread": "Một sợi chỉ nối cả khóa: <b>Sổ tay quản lý</b>, gồm 8 tờ dùng với đội thật. Bài cuối ôn trộn cả khóa và lập bảng phân bổ cho quý tới.",
           "after": '<p class="note"><b>Lưu ý:</b> Bài 5 dạy kỹ năng nói chuyện, không thay quy trình kỷ luật của đơn vị. Bài 7 không tư vấn pháp lý; nguồn luật ghi rõ ngày tra. <b>Nên học trước:</b> bài <a href="{{R}}bai-hoc/k9-kem-cap-dong-nghiep/">Kèm cặp đồng nghiệp</a> của khóa N4.</p>'},
    "n6": {"title": "Khóa Lãnh đạo cấp cao (N6)", "home": "lo-trinh/n6/", "guide": "tai-nguyen/n6/",
           "guide_label": "Mẫu in của khóa", "strip_label": "Mẫu in",
           "thread": "Một sợi chỉ nối cả khóa: <b>Sổ tay điều hành</b>, gồm 8 tờ dùng với tổ chức thật. Bài cuối ôn trộn cả khóa và lập bản đồ kế nhiệm.",
           "after": '<p class="note"><b>Lưu ý:</b> Bài 7 không tư vấn pháp lý; nguồn luật ghi rõ ngày tra. Các công cụ trong khóa ghi rõ mức bằng chứng: nghiên cứu, phương pháp được khuyến nghị, hay đề xuất của site. <b>Nên học trước:</b> khóa <a href="{{R}}lo-trinh/n5/">Quản lý, trưởng nhóm (N5)</a>.</p>'},
    "n7": {"title": "Khóa Founder, khởi nghiệp (N7)", "home": "lo-trinh/n7/", "guide": "tai-nguyen/n7/",
           "guide_label": "Mẫu in của khóa", "strip_label": "Mẫu in",
           "thread": "Một sợi chỉ nối cả khóa: <b>Sổ tay founder</b>, gồm 8 tờ dùng với việc kinh doanh thật. Bằng chứng ở Tờ 1–2 và con số ở Tờ 4 được dùng lại trong pitch ở Tờ 7.",
           "after": '<p class="note"><b>Lưu ý:</b> Bài 5, 6 và 8 không tư vấn pháp lý; Bài 4 không phải kế toán hay tư vấn thuế. Nguồn luật ghi rõ ngày tra. Mỗi bài có hộp "Mức bằng chứng". <b>Học thêm:</b> <a href="{{R}}bai-hoc/k9-giao-viec-va-theo-doi/">Giao việc và theo dõi</a> (N5) khi đội bắt đầu lớn.</p>'},
}


def course_lessons(c):
    return sorted([l for l in LESSONS if l.get("course") == c], key=lambda l: l.get("order", 99))


def course_strip(l):
    c = l.get("course")
    if not c:
        return ""
    items = ""
    for i, x in enumerate(course_lessons(c), 1):
        cur = ' aria-current="step"' if x["slug"] == l["slug"] else ""
        items += (f'<li data-lesson="{e(x["slug"])}"{cur}><a href="{{{{R}}}}bai-hoc/{e(x["slug"])}/">'
                  f'<span class="cs-n">{i}</span><span class="cs-t">{e(x.get("short", x["title"]))}</span></a></li>')
    return (f'<nav class="course-strip" aria-label="Các bài trong khóa"><p class="small"><b>{e(COURSES[c]["title"])}</b> · '
            f'<a href="{{{{R}}}}{COURSES[c]["home"]}">Bản đồ khóa</a> · <a href="{{{{R}}}}{COURSES[c]["guide"]}">{COURSES[c]["strip_label"]}</a></p><ol>{items}</ol></nav>')


def build_lessons():
    page("bai-hoc/", "Bài học", f"""<h1>Bài học</h1>
<p class="lead">Mỗi bài 10–20 phút, theo 9 phần: mục tiêu, khởi động, giải thích, ví dụ, thực hành,
tự kiểm tra, phản tư, áp dụng thật, siêu dữ liệu.</p>
{lessons_list(LESSONS)}""")

    for l in LESSONS:
        s = SKILL[l["skill"]]
        h = md_to_html(l["body"])
        # gắn id p1..p9 cho 9 phần
        h = re.sub(r"<h2>(\d)\. ", lambda m: f'<h2 id="p{m.group(1)}">{m.group(1)}. ', h)
        h = h.replace('<h2 id="p6">6. Tự kiểm tra</h2>',
                      '<h2 id="p6">6. Tự kiểm tra</h2>\n<p>Chọn đáp án. Mỗi lựa chọn đều có giải thích.</p>\n' + quiz_html(l))
        h = h.replace('<h2 id="p9">9. Siêu dữ liệu</h2>', '<h2 id="p9">9. Siêu dữ liệu</h2>\n' + meta_table(l))
        nav = ""
        if l.get("prev") in LESSON:
            nav += f'<a href="{{{{R}}}}bai-hoc/{l["prev"]}/">← {e(LESSON[l["prev"]]["title"])}</a>'
        if l.get("next") in LESSON:
            nav += f'<a class="next" href="{{{{R}}}}bai-hoc/{l["next"]}/">{e(LESSON[l["next"]]["title"])} →</a>'
        draft = '<p class="note">Bài đang ở dạng <b>bản nháp</b>, chờ duyệt nội dung.</p>' if l.get("status") == "draft" else ""
        strip = course_strip(l)
        age = f" · {e(l['age'])}" if l.get("age") else ""
        body = f"""<article class="lesson" data-lesson="{e(l['slug'])}" data-title="{e(l['title'])}" data-group="{e(' '.join(l['group']))}">
<p class="crumb"><a href="{{{{R}}}}ky-nang/{s['slug']}/">{s['code']} · {e(s['name'])}</a> › Bậc {l['level']} {e(LEVELS[l['level']]['name'])}</p>
<h1>{e(l['title'])}</h1>
<p class="meta">{l['minutes']} phút · Nhóm {", ".join(l['group'])}{age} · Cập nhật {l['updated']}</p>
{strip}{draft}
{h}
<section class="finish card">
  <h2>Hoàn thành bài</h2>
  <p>Đánh dấu đã học để site gợi ý lịch ôn sau 1, 3 và 7 ngày. Dữ liệu chỉ lưu trên máy của bạn.</p>
  <button type="button" class="btn" data-action="done">Đánh dấu đã học</button>
  <div class="review" hidden>
    <p><b>Lịch ôn gợi ý:</b> <span class="review-dates"></span></p>
    <p><button type="button" class="btn ghost" data-action="ics">Tải file nhắc lịch (.ics)</button>
    <button type="button" class="btn ghost" data-action="undo">Bỏ đánh dấu</button></p>
  </div>
</section>
<nav class="pager">{nav}</nav>
</article>"""
        page(f"bai-hoc/{l['slug']}/", l["title"], body, desc=" ".join(l["objectives"])[:155])


# ---------------------------------------------------------------- tự đánh giá
def build_self_assessment():
    blocks = ""
    for s in SKILLS:
        rows = ""
        for n, stmts in s["levels"].items():
            for i, x in enumerate(stmts):
                key = f"{s['code']}-{n}-{i}"
                radios = "".join(
                    f'<label><input type="radio" name="{key}" value="{v}"><span>{e(r)}</span></label>'
                    for v, r in enumerate(RATING))
                rows += f"""<fieldset class="sa-item" data-key="{key}" data-level="{n}">
<legend><span class="lvn">B{n}</span> {e(x)}</legend><div class="sa-opts">{radios}</div></fieldset>"""
        blocks += f"""<details class="sa-skill" id="{s['code']}" data-skill="{s['code']}">
<summary><b>{s['code']}</b> {e(s['name'])} <span class="sa-result"></span></summary>
{rows}<p class="small"><a href="{{{{R}}}}ky-nang/{s['slug']}/">Xem kỹ năng {s['code']} và bài học</a></p></details>"""
    page("tu-danh-gia/", "Tự đánh giá", f"""<h1>Tự đánh giá kỹ năng</h1>
<p class="lead">Với mỗi câu "Tôi có thể…", chọn mức đúng với bạn nhất. Không có đúng sai.</p>
<p class="note">Câu trả lời chỉ lưu trong trình duyệt trên máy này (localStorage). Site không gửi dữ liệu đi đâu.
Không dành cho trẻ em tự dùng.</p>
<p class="small muted">Cách tính bậc gợi ý: bậc cao nhất mà mọi câu từ Bậc 1 đến bậc đó đều ở mức
"Thường xuyên" trở lên. Đây chỉ là gợi ý để chọn bài, không phải chứng nhận.</p>
<div class="sa">{blocks}</div>
<h2>Tóm tắt</h2>
<table class="matrix sa-summary"><thead><tr><th>Kỹ năng</th><th>Bậc gợi ý</th><th>Bài nên học</th></tr></thead><tbody></tbody></table>
<p class="noprint"><button type="button" class="btn" data-action="print">In hoặc lưu PDF</button>
<button type="button" class="btn ghost" data-action="sa-clear">Xóa câu trả lời</button></p>
<script type="application/json" id="sa-data">{SA_JSON()}</script>
""")


def SA_JSON():
    import json
    data = {s["code"]: {"slug": s["slug"], "name": s["name"],
                        "lessons": [{"slug": l["slug"], "title": l["title"], "level": l["level"]}
                                    for l in LESSONS if l["skill"] == s["code"]]} for s in SKILLS}
    data["_suffix"] = "index.html" if PREVIEW else ""
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


# ---------------------------------------------------------------- trang phụ
def build_misc():
    page("nhat-ky/", "Nhật ký bằng chứng", """<h1>Nhật ký bằng chứng</h1>
<p class="lead">Những gì bạn viết ở phần Phản tư của các bài học được gom ở đây.
Dùng chúng làm ví dụ thật khi viết CV, phỏng vấn hoặc đánh giá cuối năm.</p>
<p class="note">Nhật ký chỉ lưu trên trình duyệt này. Nếu xóa dữ liệu trình duyệt, nhật ký sẽ mất.
Hãy in hoặc lưu PDF định kỳ.</p>
<div class="journal-list"><p class="muted">Chưa có ghi chép nào.</p></div>
<p class="noprint"><button type="button" class="btn" data-action="print">In hoặc lưu PDF</button>
<button type="button" class="btn ghost" data-action="journal-clear">Xóa toàn bộ nhật ký</button></p>""")

    page("tai-nguyen/", "Tài nguyên", """<h1>Tài nguyên in được</h1>
<p class="lead">Mẫu để in hoặc chép vào sổ. Dùng kèm bài học.</p>
<h2 id="star">Mẫu nhật ký bằng chứng (STAR)</h2>
<p>STAR là cách kể một ví dụ công việc theo 4 phần. Rất hữu ích khi phỏng vấn.</p>
<table class="matrix print-form"><tbody>
<tr><th>S – Situation (Tình huống)</th><td>Ở đâu, khi nào, bối cảnh gì?</td></tr>
<tr><th>T – Task (Nhiệm vụ)</th><td>Bạn cần làm gì? Kết quả mong đợi là gì?</td></tr>
<tr><th>A – Action (Hành động)</th><td>Bạn đã làm cụ thể những gì?</td></tr>
<tr><th>R – Result (Kết quả)</th><td>Kết quả ra sao? Có số liệu không? Bạn học được gì?</td></tr>
</tbody></table>
<h2 id="danh-sach-viec">Mẫu danh sách việc 5 cột</h2>
<p>Dùng với bài <a href="{{R}}bai-hoc/k5-ghi-viec-va-bao-som/">Ghi lại việc được giao và báo sớm</a>.</p>
<table class="matrix print-form"><thead><tr><th>Việc</th><th>Kết quả</th><th>Hạn</th><th>Người giao</th><th>Trạng thái</th></tr></thead>
<tbody><tr><td>&nbsp;</td><td></td><td></td><td></td><td></td></tr><tr><td>&nbsp;</td><td></td><td></td><td></td><td></td></tr>
<tr><td>&nbsp;</td><td></td><td></td><td></td><td></td></tr><tr><td>&nbsp;</td><td></td><td></td><td></td><td></td></tr></tbody></table>
<p class="small muted">Trạng thái: Chưa làm · Đang làm · Có nguy cơ trễ · Xong</p>
<p class="noprint"><a class="btn ghost" href="{{R}}assets/danh-sach-viec.csv" download>Tải bản bảng tính (.csv)</a>
<button type="button" class="btn" data-action="print">In trang này</button></p>
<h2>Hướng dẫn cho phụ huynh và giáo viên (N1)</h2>
<p>Cách dẫn khóa Khám phá nghề, lịch ôn và 4 mẫu in: Thẻ nghề, Bảng nhiệm vụ nhóm, Phiếu phỏng vấn, Phiếu ôn tập.</p>
<p><a class="btn" href="{{R}}tai-nguyen/n1/">Mở hướng dẫn N1</a></p>
<h2>Mẫu in khóa Chuẩn bị đi làm (N2)</h2>
<p>Bảy mẫu cho Hồ sơ sẵn sàng đi làm: bản đồ hướng đi, phiếu đọc tin tuyển dụng, khung CV, phiếu phỏng vấn, sổ tay tuần đầu, trang quy trình, bảng kiểm.</p>
<p><a class="btn" href="{{R}}tai-nguyen/n2/">Mở mẫu in N2</a></p>
<h2>Mẫu in khóa 90 ngày đầu (N3)</h2>
<p>Bảy mẫu cho Sổ tay 90 ngày: bảng việc tuần, trang ghi họp, phiếu yêu cầu khách hàng, phiếu sự cố, phiếu rút kinh nghiệm, bản đồ phối hợp, hồ sơ buổi đánh giá.</p>
<p><a class="btn" href="{{R}}tai-nguyen/n3/">Mở mẫu in N3</a></p>
<h2>Mẫu in khóa Senior, chuyên gia (N4)</h2>
<p>Tám mẫu cho Sổ công cụ chuyên gia: sơ đồ tác động, phiếu quyết định, bản đồ các bên và đề xuất một trang, phiếu gỡ bất đồng, kế hoạch kèm cặp, một trang dự án, phiếu theo dõi quy định, kế hoạch nghề 1–3 năm.</p>
<p><a class="btn" href="{{R}}tai-nguyen/n4/">Mở mẫu in N4</a></p>
<h2>Mẫu in khóa Quản lý, trưởng nhóm (N5)</h2>
<p>Tám mẫu cho Sổ tay quản lý: bản chuyển vai, mục tiêu đội một trang, phiếu giao việc, trang 1-1, phiếu chuẩn bị đối thoại khó, thỏa thuận làm việc của đội, kế hoạch thay đổi và quy tắc dùng AI, bảng phân bổ quý.</p>
<p><a class="btn" href="{{R}}tai-nguyen/n5/">Mở mẫu in N5</a></p>
<h2>Mẫu in khóa Lãnh đạo cấp cao (N6)</h2>
<p>Tám mẫu cho Sổ tay điều hành: lịch điều hành, biên bản pre-mortem, bảng chiến lược thành việc, bản định hướng và kế hoạch truyền đạt, bảng quyền quyết định, kênh tin xấu, sổ rủi ro và danh mục AI, bản đồ kế nhiệm.</p>
<p><a class="btn" href="{{R}}tai-nguyen/n6/">Mở mẫu in N6</a></p>
<h2>Mẫu in khóa Founder, khởi nghiệp (N7)</h2>
<p>Tám mẫu cho Sổ tay founder: phiếu giả thuyết và phỏng vấn, phiếu thử nghiệm, kế hoạch 90 ngày, bảng dòng tiền 13 tuần, bảng kiểm pháp lý khởi sự, phiếu tuyển người đầu tiên, kịch bản pitch, bảng công cụ số và quy tắc AI.</p>
<p><a class="btn" href="{{R}}tai-nguyen/n7/">Mở mẫu in N7</a></p>""")
    for code, fn in (("n1", "n1-huong-dan.md"), ("n2", "n2-mau-in.md"), ("n3", "n3-mau-in.md"), ("n4", "n4-mau-in.md"), ("n5", "n5-mau-in.md"), ("n6", "n6-mau-in.md"), ("n7", "n7-mau-in.md")):
        gp = ROOT / "content/trang" / fn
        if not gp.exists():
            continue
        raw = gp.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        gm = yaml.safe_load(m.group(1))
        page(f"tai-nguyen/{code}/", gm["title"], f'<p class="crumb"><a href="{{{{R}}}}tai-nguyen/">Tài nguyên</a> › {code.upper()}</p>'
             + md_to_html(m.group(2)), desc=gm.get("desc", ""))

    page("phap-ly/", "Pháp lý khi đi làm", """<h1>Pháp lý khi đi làm</h1>
<p class="lead">Kiến thức thực tế về hợp đồng, thử việc, học nghề, an toàn và bảo mật ở nơi làm việc.</p>
<p class="note">Các bài pháp lý đang được biên soạn và đối chiếu với văn bản gốc.
Mỗi bài sẽ ghi rõ số hiệu văn bản, ngày hiệu lực và ngày cập nhật lần cuối.
Thông tin trên site không thay thế tư vấn pháp lý.</p>""")

    fw_rows = "".join(
        f"<tr><td>{s['cluster']}. {e(CLUSTERS[s['cluster']])}</td><td>{s['code']} {e(s['name'])}</td>"
        f"<td>{e('; '.join(s['framework_map']))}</td><td>{e(s['gdpt'])}</td></tr>" for s in SKILLS)
    page("khung-tham-chieu/", "Khung tham chiếu", f"""<h1>Khung tham chiếu</h1>
<p class="lead">Khung 10 kỹ năng của site được xây dựa trên các khung quốc tế đã công bố, điều chỉnh cho bối cảnh Việt Nam
và đối chiếu với năng lực chung của Chương trình GDPT 2018.</p>
<p class="note">Tên các khung chỉ dùng để dẫn chiếu. Toàn bộ mô tả, câu "Tôi có thể…" và bài học do site tự viết.
Site không dịch hay chuyển thể nội dung của bất kỳ khung nào.</p>
<h2>Bảng đối chiếu</h2>
<table class="matrix small"><thead><tr><th>Cụm</th><th>Kỹ năng</th><th>Khung đối chiếu chính</th><th>GDPT 2018</th></tr></thead>
<tbody>{fw_rows}</tbody></table>
<h2>Thang bậc</h2>
<p>Site dùng 5 bậc: {" → ".join(f"{n}. {e(l['name'])}" for n, l in LEVELS.items())}.
Để đối chiếu: khung CSfW của Chính phủ Úc dùng 5 giai đoạn từ Novice đến Expert; SkillsFuture Critical Core Skills
của Singapore dùng 3 mức Basic, Intermediate, Advanced.</p>
<h2>Nguồn</h2>
<ul class="small">
<li><a href="https://www.weforum.org/publications/the-future-of-jobs-report-2025">World Economic Forum – Future of Jobs Report 2025</a></li>
<li><a href="https://www.dewr.gov.au/skills-information-training-providers/core-skills-work-developmental-framework">Core Skills for Work Developmental Framework (CSfW), Chính phủ Úc</a></li>
<li><a href="https://www.skillsfuture.gov.sg/initiatives/early-career/criticalcoreskills">SkillsFuture – Critical Core Skills, Singapore</a></li>
<li><a href="https://www.naceweb.org/career-readiness/competencies/career-readiness-defined">NACE – Career Readiness Competencies</a></li>
<li><a href="https://joint-research-centre.ec.europa.eu/jrc-news-and-updates/european-commission-updates-its-digital-competence-framework-digcomp-2025-11-27_en">DigComp 3.0, Trung tâm Nghiên cứu Chung (JRC), Ủy ban châu Âu</a></li>
<li><a href="https://publications.jrc.ec.europa.eu/repository/handle/JRC120911">LifeComp, JRC</a></li>
<li><a href="https://www.unicef.org/media/64751/file/Global-framework-on-transferable-skills-2019.pdf">UNICEF – Global Framework on Transferable Skills (2019)</a></li>
<li><a href="https://www.ilo.org/media/455766/download">ILO – core work skills</a></li>
<li><a href="https://www.onetcenter.org/reports/Higher_Order_Styles.html">O*NET – Work Styles</a></li>
<li><a href="https://www.skillsbuilder.uk/universal-framework">Skills Builder Universal Framework</a> (chỉ tham khảo; giấy phép CC BY-NC-ND 4.0)</li>
<li>Chương trình GDPT 2018, Thông tư 32/2018/TT-BGDĐT.</li>
</ul>
<h2>Tên gốc đã đối chiếu</h2>
<p class="small">Danh sách tên gọi gốc để đối chiếu mã trong bảng trên. Chỉ ghi tên, không chép mô tả.</p>
<ul class="small">
<li><b>CSfW</b> (3 cụm, 10 lĩnh vực): 1a Manage career and work life · 1b Work with roles, rights and protocols ·
2a Communicate for work · 2b Connect and work with others · 2c Recognise and utilise diverse perspectives ·
3a Plan and organise · 3b Make decisions · 3c Identify and solve problems · 3d Create and innovate · 3e Work in a digital world.</li>
<li><b>SkillsFuture CCS</b> (16 năng lực, 3 cụm): Thinking Critically – Creative Thinking, Decision Making, Problem Solving,
Sense Making, Transdisciplinary Thinking · Interacting with Others – Building Inclusivity, Collaboration, Communication,
Customer Orientation, Developing People, Influence · Staying Relevant – Adaptability, Digital Fluency, Global Perspective,
Learning Agility, Self Management.</li>
<li><b>NACE</b> (8 năng lực): Career and Self-Development · Communication · Critical Thinking · Equity and Inclusion ·
Leadership · Professionalism · Teamwork · Technology.</li>
<li><b>LifeComp</b> (9 năng lực): P1 Self-regulation · P2 Flexibility · P3 Wellbeing · S1 Empathy · S2 Communication ·
S3 Collaboration · L1 Growth mindset · L2 Critical thinking · L3 Managing learning.</li>
<li><b>WEF Future of Jobs 2025</b>: tên kỹ năng theo bảng phân loại của báo cáo, ví dụ Analytical thinking;
Resilience, flexibility and agility; Leadership and social influence; Empathy and active listening.</li>
</ul>
<p class="muted small">Đối chiếu lần cuối ngày 14/11/2026.</p>""")

    page("gioi-thieu/", "Giới thiệu", """<h1>Giới thiệu</h1>
<p class="lead">kynanglamviec.com dạy kỹ năng làm việc theo lộ trình nghề nghiệp, từ học sinh đến quản lý.
Miễn phí, công khai, không cần đăng nhập.</p>
<h2>Cách site được xây</h2>
<ul>
<li>10 kỹ năng, 5 cụm, 5 bậc, dựa trên các <a href="{{R}}khung-tham-chieu/">khung quốc tế</a> và điều chỉnh cho Việt Nam.</li>
<li>Mỗi bài học theo 9 phần, có tình huống giả định tại nơi làm việc Việt Nam.</li>
<li>Học bằng tự kiểm tra và ôn giãn cách, hai kỹ thuật có bằng chứng tốt
(<a href="https://journals.sagepub.com/doi/abs/10.1177/1529100612453266">Dunlosky và cộng sự, 2013</a>).</li>
<li>Không dùng tên công ty hay khách hàng thật. Mọi tình huống đều là giả định.</li>
</ul>
<h2>Quyền riêng tư</h2>
<p>Không đăng nhập, không cookie, không công cụ theo dõi, không tải mã hay phông chữ bên ngoài.
Tiến độ, tự đánh giá và nhật ký chỉ lưu trong trình duyệt của bạn (localStorage). Site không có máy chủ lưu dữ liệu người dùng.</p>
<h2>Trang cùng hệ</h2>
<ul>
<li><a href="https://daynentang.com/">daynentang.com</a> – giá trị, đạo đức, thói quen, phẩm chất.</li>
<li><a href="https://tamhonkhoe.com/">tamhonkhoe.com</a> – tinh thần, thiền, Stoicism.</li>
<li><a href="https://trachnhiemxahoi.com/">trachnhiemxahoi.com</a> – social compliance, quyền con người.</li>
<li><a href="https://tienganhcanban.com/">tienganhcanban.com</a> – tiếng Anh.</li>
</ul>
<h2>Giấy phép</h2>
<p>Nội dung tự viết theo giấy phép CC BY-NC-SA 4.0: được chia sẻ, chỉnh sửa cho mục đích phi thương mại,
ghi nguồn và giữ cùng giấy phép.</p>""")

    page("404.html", "Không tìm thấy trang", """<h1>Không tìm thấy trang</h1>
<p>Trang này không tồn tại hoặc đã đổi địa chỉ. <a href="{{R}}">Về trang chủ</a>.</p>""")


def build_static():
    src = ROOT / "_build" / "static"
    shutil.copytree(src, OUT, dirs_exist_ok=True)
    if PREVIEW:
        for f in ("_headers", "robots.txt"):
            (OUT / f).unlink(missing_ok=True)
    else:
        urls = "".join(f"<url><loc>{SITE}/{p}</loc><lastmod>{TODAY}</lastmod></url>"
                       for p in PAGES if p != "404.html")
        (OUT / "sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
            encoding="utf-8")


if __name__ == "__main__":
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    build_home(); build_groups(); build_skills(); build_lessons()
    build_self_assessment(); build_misc(); build_static()
    print(f"Đã sinh {len(PAGES)} trang vào {OUT.relative_to(ROOT)}/")
