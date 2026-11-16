#!/usr/bin/env python3
"""Sinh phần Sách cho app từ bộ nguồn sách "Cuốn sổ bìa xanh" (cuon-so-bia-xanh-chu-va-ma.zip).

Chạy khi sách đổi (cần playwright + chromium, segno, pillow):
    python3 app/tools/gen_sach.py /đường/dẫn/cuon-so-bia-xanh
Ghi vào app/sach/: cNN.html (đoạn HTML từng chương), cNN.webp (tranh), bia.webp, sach.json.
build_www.py đọc app/sach/ để dựng /sach/ trong app. Chữ lấy đúng từ text/chuong-NN.md qua hàm chapter() của build_sach.py,
bỏ phần "Ghi chú cho biên tập". QR trong Góc người lớn đổi thành nút mở bài học ngay trong app.
"""
import ast
import html as H
import io
import json
import pathlib
import re
import sys

from PIL import Image

SRC = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(SRC))
import art_sach as A  # noqa: E402
import build_sach as B  # noqa: E402

APP = pathlib.Path(__file__).resolve().parent.parent
OUT = APP / "sach"
OUT.mkdir(exist_ok=True)
WIDTH = 900  # px, tranh trong app


def render_art():
    from playwright.sync_api import sync_playwright
    items = [(f"c{k:02d}", f) for k, f in A.SCENES.items()] + [("bia", A.scene_cover)]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_context(viewport={"width": A.W, "height": A.Hh}, device_scale_factor=WIDTH / A.W).new_page()
        for name, f in items:
            pg.set_content(f'<html><body style="margin:0">{f()}</body></html>')
            png = pg.screenshot(clip={"x": 0, "y": 0, "width": A.W, "height": A.Hh})
            Image.open(io.BytesIO(png)).convert("RGB").save(OUT / f"{name}.webp", "WEBP", quality=80, method=6)
            print(name, end=" ", flush=True)
        b.close()
    print()


def lesson_button(blocks, slug, title):
    """Khối QR của bản in -> nút mở bài trong app (đọc được khi mất mạng)."""
    btn = (f'<p class="sach-more"><a class="btn" href="/bai-hoc/{slug}/">Mở bài học: {H.escape(title)}</a>'
           f'<span class="small muted">Bài trên kynanglamviec.com, có sẵn trong app.</span></p>')
    blocks = [b.replace("quét mã QR để làm bài", "bấm nút dưới đây để làm bài") for b in blocks]
    out = [btn if b.startswith('<div class="more">') else b for b in blocks]
    return out if btn in out else out + [btn]


def chapter_html(c, slug):
    n = c["n"]
    part = B.PARTS[c["part"]]
    s = [f'<p class="eyebrow">Chương {n} · {H.escape(part["name"].split(" · ")[1])}</p>',
         f'<h1>{H.escape(c["title"])}</h1>',
         f'<p class="sach-label">{H.escape(c["label"])}</p>',
         f'<figure class="sach-plate"><img src="/sach/tranh/c{n:02d}.webp" alt="Tranh minh họa chương {n}" width="900" height="{round(900 * A.Hh / A.W)}">'
         '<figcaption>Tranh minh họa do AI tạo, không phải chân dung người thật.</figcaption></figure>',
         '<dl class="sach-facts">'
         f'<dt>Ở đâu</dt><dd>{H.escape(B.WHERE[n])}</dd><dt>Nhân vật chính</dt><dd>{H.escape(B.WHO[n])}</dd>'
         f'<dt>Kỹ năng</dt><dd>{H.escape(c["skill"])}</dd><dt>Người đọc</dt><dd>Cả nhà cùng đọc · khoảng 12 phút</dd></dl>',
         '<div class="sach-text">' + "".join(c["story"]) + "</div>",
         f'<section class="sach-notebook">{A.spot_notebook(n)}<p class="eyebrow">Trang sổ chung số {n}</p>'
         f'<h2>{H.escape(c["so_title"])}</h2><ul>' + "".join(f"<li>{B.inline(x)}</li>" for x in c["nb"]) + "</ul></section>",
         '<section class="sach-adult"><h2>Góc người lớn</h2>'
         f'<p class="sach-skill">{B.inline(c["skill_line"])}</p>' + "".join(lesson_button(c["adult"], slug, c["lesson"])) + "</section>",
         '<section class="sach-talk"><h2>Cả nhà cùng trò chuyện</h2>' + "".join(c["talk"]) + "</section>",
         f'<section class="sach-do"><h2>{H.escape(c["do_head"])}</h2>' + "".join(c["do"]) + "</section>"]
    return "\n".join(s) + "\n"


def sources():
    """Danh sách Nguồn ở cuối sách (lấy từ build_sach.py)."""
    m = re.search(r"nguon = (\[.*?\n        \])", (SRC / "build_sach.py").read_text(encoding="utf-8"), flags=re.S)
    return ast.literal_eval(m.group(1)) if m else []


def main():
    meta = []
    for n in range(1, 21):
        raw = (SRC / "text" / f"chuong-{n:02d}.md").read_text(encoding="utf-8")
        slug = B.fm(raw.split("---", 2)[1], "lesson_slug")
        c = B.chapter(n)
        (OUT / f"c{n:02d}.html").write_text(chapter_html(c, slug), encoding="utf-8")
        opener = ""
        if n == 12:  # Trang mở nửa sau
            sec = B.section(raw.split("---", 2)[2], "Trang mở nửa sau")
            opener = "".join(B.story_items(sec))
        meta.append(dict(n=n, title=c["title"], part=c["part"], lesson=slug, lesson_title=c["lesson"],
                         skill=c["skill"], where=B.SHORT[n], who=B.WHO[n], opener=opener))
    parts = {k: dict(name=v["name"], color=v["color"], light=v["light"], intro=v["intro"]) for k, v in B.PARTS.items()}
    data = dict(title=B.TITLE, sub=B.SUB, author=B.AUTHOR, parts=parts, chapters=meta, sources=sources())
    (OUT / "sach.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    if "--no-art" not in sys.argv:
        render_art()
    print(f"{len(meta)} chương -> {OUT}")


if __name__ == "__main__":
    main()
