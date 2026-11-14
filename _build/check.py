#!/usr/bin/env python3
"""Kiểm tra bài học: câu tiếng Việt <= 25 chữ, phần 3 dưới 400 chữ, đủ 9 phần, ảnh tồn tại,
liên kết nội bộ tới bài có thật, câu hỏi 3-5 câu, mỗi lựa chọn có giải thích.
Chạy: python3 _build/check.py [slug...]"""
import re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
slugs = {p.stem for p in (ROOT / "content/bai-hoc").glob("*.md")}
want = sys.argv[1:]
bad = 0


def plain(t):
    t = re.sub(r"<img[^>]*>", " ", t)
    t = re.sub(r"<(figcaption|summary|b|span|li|div|p|a)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"[*_`>#|]", " ", t)
    return t


for f in sorted((ROOT / "content/bai-hoc").glob("*.md")):
    if want and f.stem not in want:
        continue
    raw = f.read_text(encoding="utf-8")
    meta, body = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S).groups()
    meta = yaml.safe_load(meta)
    errs = []
    heads = re.findall(r"^## (\d)\. ", body, re.M)
    if heads != [str(i) for i in range(1, 10)]:
        errs.append(f"tiêu đề 9 phần sai: {heads}")
    p3 = re.search(r"## 3\. .*?\n(.*?)\n## 4\. ", body, re.S).group(1)
    n3 = len(plain(p3).split())
    if n3 >= 400:
        errs.append(f"phần 3 có {n3} chữ (>=400)")
    for line in plain("\n".join(x for x in body.split("\n") if not x.lstrip().startswith("|"))).split("\n"):
        for sent in re.split(r"(?<=[.!?:;])[\"”]?\s+|\s[–—]\s", line):
            w = sent.split()
            if len(w) > 25:
                errs.append(f"câu {len(w)} chữ: {' '.join(w)[:90]}…")
    for img in re.findall(r'src="\.\./\.\./(assets/[^"]+)"', body):
        if not (ROOT / "_build/static" / img).exists():
            errs.append(f"thiếu ảnh {img}")
    for ln in re.findall(r"\(\.\./([a-z0-9-]+)/\)|bai-hoc/([a-z0-9-]+)/", body):
        s = ln[0] or ln[1]
        if s and s not in slugs:
            errs.append(f"liên kết tới bài không có: {s}")
    for k in ("prev", "next"):
        if meta.get(k) and meta[k] not in slugs:
            errs.append(f"{k} trỏ tới bài không có: {meta[k]}")
    qf = ROOT / "content/cau-hoi" / f"{f.stem}.yaml"
    if qf.exists():
        qs = yaml.safe_load(qf.read_text(encoding="utf-8"))["questions"]
        if not 3 <= len(qs) <= 5:
            errs.append(f"{len(qs)} câu hỏi")
        for q in qs:
            if sum(o["correct"] for o in q["options"]) != 1 or any(not o.get("why") for o in q["options"]):
                errs.append(f"câu {q['id']}: cần đúng 1 đáp án và mọi lựa chọn có why")
            for o in [q["prompt"]] + [o["why"] for o in q["options"]]:
                for sent in re.split(r"(?<=[.!?])\s+", o):
                    if len(sent.split()) > 25:
                        errs.append(f"câu hỏi {q['id']} có câu dài: {sent[:80]}…")
    else:
        errs.append("thiếu file câu hỏi")
    imgs = len(re.findall(r'<img ', body))
    dgs = len(re.findall(r'class="diagram"', body))
    status = "OK" if not errs else "LỖI"
    print(f"{status} {f.stem}: phần 3 = {n3} chữ, {imgs} hình, {dgs} sơ đồ")
    for x in errs:
        print("   -", x)
    bad += bool(errs)


# ---------------------------------------------------------------- bản tiếng Anh (content/en)
# Cùng quy tắc: câu <= 25 từ, phần 3 < 400 từ, đủ 9 phần, ảnh có thật, liên kết tới bài có thật.
def check_en():
    en = ROOT / "content/en"
    en_slugs = {p.stem for p in (en / "lessons").glob("*.md")}
    nbad = 0
    for f in sorted((en / "lessons").glob("*.md")):
        if want and f.stem not in want:
            continue
        meta, body = re.match(r"^---\n(.*?)\n---\n(.*)$", f.read_text(encoding="utf-8"), re.S).groups()
        meta = yaml.safe_load(meta)
        errs = []
        if meta.get("vi") not in slugs:
            errs.append(f"vi trỏ tới bài không có: {meta.get('vi')}")
        if re.findall(r"^## (\d)\. ", body, re.M) != [str(i) for i in range(1, 10)]:
            errs.append("tiêu đề 9 phần sai")
        p3 = re.search(r"## 3\. .*?\n(.*?)\n## 4\. ", body, re.S).group(1)
        n3 = len(plain(p3).split())
        if n3 >= 400:
            errs.append(f"phần 3 có {n3} từ (>=400)")
        for line in plain("\n".join(x for x in body.split("\n") if not x.lstrip().startswith("|"))).split("\n"):
            for sent in re.split(r"(?<=[.!?:;])[\"”]?\s+|\s[–—]\s", line):
                if len(sent.split()) > 25:
                    errs.append(f"câu {len(sent.split())} từ: {sent[:90]}…")
        for img in re.findall(r'src="\.\./\.\./\.\./(assets/[^"]+)"', body):
            if not (ROOT / "_build/static" / img).exists():
                errs.append(f"thiếu ảnh {img}")
        for s in re.findall(r"\]\(\.\./([a-z0-9-]+)/\)", body):
            if s not in en_slugs:
                errs.append(f"liên kết tới bài EN không có: {s}")
        for s in re.findall(r"\.\./\.\./\.\./bai-hoc/([a-z0-9-]+)/", body):
            if s not in slugs:
                errs.append(f"liên kết tới bài VI không có: {s}")
        for k in ("prev", "next"):
            if meta.get(k) and meta[k] not in en_slugs:
                errs.append(f"{k} trỏ tới bài không có: {meta[k]}")
        qf = en / "quiz" / f"{f.stem}.yaml"
        if qf.exists():
            qs = yaml.safe_load(qf.read_text(encoding="utf-8"))["questions"]
            if not 3 <= len(qs) <= 5:
                errs.append(f"{len(qs)} câu hỏi")
            for q in qs:
                if sum(o["correct"] for o in q["options"]) != 1 or any(not o.get("why") for o in q["options"]):
                    errs.append(f"câu {q['id']}: cần đúng 1 đáp án và mọi lựa chọn có why")
                for o in [q["prompt"]] + [o["why"] for o in q["options"]]:
                    for sent in re.split(r"(?<=[.!?])\s+", o):
                        if len(sent.split()) > 25:
                            errs.append(f"câu hỏi {q['id']} có câu dài: {sent[:80]}…")
        else:
            errs.append("thiếu file câu hỏi")
        print(f"{'OK' if not errs else 'LỖI'} en/{f.stem}: phần 3 = {n3} từ")
        for x in errs:
            print("   -", x)
        nbad += bool(errs)
    return nbad


bad += check_en()
sys.exit(1 if bad else 0)
