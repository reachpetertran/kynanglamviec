"""English edition of kynanglamviec.com, generated under /en/.

The Vietnamese content is the original. The English edition is adapted with
international examples (Peter's decision, 14/11/2026) and is added in stages.

Sources:
  content/en/data/*.yaml      skills, levels, groups (same codes as data/*.yaml)
  content/en/lessons/*.md     English lessons; front matter `vi:` = Vietnamese slug
  content/en/quiz/*.yaml      self-check questions
  content/en/pages/*.md       printable templates; front matter `vi:` = course code

Called from build.py: ALT = build_en.alt_map() before building, build_en.run(build) at the end.
"""
import html, json, re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
EN = ROOT / "content/en"
SITE = "https://kynanglamviec.com"
NAME = "Work Skills"
e = lambda s: html.escape(str(s), quote=True)


def _y(p):
    return yaml.safe_load((EN / p).read_text(encoding="utf-8"))


def _front(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    return yaml.safe_load(m.group(1)), m.group(2)


LV = _y("data/levels.yaml")
LEVELS = {l["n"]: l for l in LV["levels"]}
RATING = LV["self_rating"]
SK = _y("data/skills.yaml")
CLUSTERS = {c["id"]: c["name"] for c in SK["clusters"]}
SKILLS = SK["skills"]
SKILL = {s["code"]: s for s in SKILLS}
GROUPS = _y("data/groups.yaml")["groups"]
MARK = {"-": ("—", "Not taught"), "o": ("○", "Introduced"), "c": ("●", "Core"), "a": ("◆", "Advanced")}


def _lessons():
    out = []
    for f in sorted((EN / "lessons").glob("*.md")):
        meta, body = _front(f)
        qf = EN / "quiz" / f"{meta['slug']}.yaml"
        meta["quiz"] = yaml.safe_load(qf.read_text(encoding="utf-8"))["questions"] if qf.exists() else []
        meta["body"] = body
        out.append(meta)
    return sorted(out, key=lambda l: l.get("order", 99))


LESSONS = _lessons()
LESSON = {l["slug"]: l for l in LESSONS}
PAGES_MD = {}
for f in sorted((EN / "pages").glob("*.md")):
    m, b = _front(f)
    PAGES_MD[m["vi"]] = (m, b)

COURSES = {
    "n1": {"title": "Exploring Jobs course (N1)", "home": "paths/n1/", "guide": "resources/n1/",
           "guide_label": "Guide and templates for adults", "strip_label": "Guide for adults",
           "thread": "One thread runs through the course: the <b>Job card</b>. Lesson 1 makes the cards, each later lesson adds to them or uses them, and the last lesson puts them all on display."},
    "n2": {"title": "Getting Ready for Work course (N2)", "home": "paths/n2/", "guide": "resources/n2/",
           "guide_label": "Course templates", "strip_label": "Templates",
           "thread": "One thread runs through the course: your <b>Job-ready file</b>, with 6 sheets. Each lesson completes one sheet. The last lesson peer-checks the whole file.",
           "after": '<p class="note"><b>Coming later:</b> a lesson on rights and safety in part-time work and internships. Labour rules differ by country, so it will cite the law where it applies.</p>'},
    "n3": {"title": "Your First 90 Days course (N3)", "home": "paths/n3/", "guide": "resources/n3/",
           "guide_label": "Course templates", "strip_label": "Templates",
           "thread": "One thread runs through the course: your <b>90-day notebook</b>, with 6 sheets you use every day at work. The last lesson turns them into a file for your review.",
           "after": '<p class="note"><b>More to learn:</b> the N3 lessons further down this page (90-day plan, progress reports, feedback, using AI safely, proposing improvements) add to the course. <b>Coming later:</b> a lesson on contracts, probation and workplace rules.</p>'},
    "n4": {"title": "Senior and Specialist course (N4)", "home": "paths/n4/", "guide": "resources/n4/",
           "guide_label": "Course templates", "strip_label": "Templates",
           "thread": "One thread runs through the course: your <b>specialist toolkit</b>, with 8 sheets you use on real work. The last lesson reviews the whole course and builds a 1–3 year career plan.",
           "after": '<p class="note"><b>Note:</b> Lesson 7 teaches how to read and apply regulations. It is not legal advice. Its legal examples come from Vietnam, with the date they were checked.</p>'},
    "n5": {"title": "Manager and Team Leader course (N5)", "home": "paths/n5/", "guide": "resources/n5/",
           "guide_label": "Course templates", "strip_label": "Templates",
           "thread": "One thread runs through the course: your <b>manager's handbook</b>, with 8 sheets you use with a real team. The last lesson reviews the whole course and builds a resource plan for next quarter.",
           "after": '<p class="note"><b>Note:</b> Lesson 5 teaches conversation skills. It does not replace your organisation\'s disciplinary process. Lesson 7 is not legal advice; its legal examples come from Vietnam, with the date they were checked. <b>Take first:</b> <a href="{{R}}en/lessons/k9-coach-a-colleague/">Mentor a colleague</a> from the N4 course.</p>'},
    "n6": {"title": "Senior Leadership course (N6)", "home": "paths/n6/", "guide": "resources/n6/",
           "guide_label": "Course templates", "strip_label": "Templates",
           "thread": "One thread runs through the course: your <b>executive handbook</b>, with 8 sheets you use with a real organisation. The last lesson reviews the whole course and builds a succession map.",
           "after": '<p class="note"><b>Note:</b> Lesson 7 is not legal advice; its legal examples come from Vietnam, with the date they were checked. Each tool states its level of evidence: research, recommended practice, or this site\'s proposal. <b>Take first:</b> the <a href="{{R}}en/paths/n5/">Manager and Team Leader course (N5)</a>.</p>'},
    "n7": {"title": "Founder and Start-up course (N7)", "home": "paths/n7/", "guide": "resources/n7/",
           "guide_label": "Course templates", "strip_label": "Templates",
           "thread": "One thread runs through the course: your <b>founder\'s handbook</b>, with 8 sheets you use with a real business. The evidence on Sheets 1–2 and the numbers on Sheet 4 are reused in your pitch on Sheet 7.",
           "after": '<p class="note"><b>Note:</b> Lessons 5, 6 and 8 are not legal advice, and Lesson 4 is not accounting or tax advice. Their legal examples come from Vietnam, with the date they were checked. Each lesson has a "Level of evidence" box. <b>Also useful:</b> <a href="{{R}}en/lessons/k9-delegate-and-follow-up/">Delegate and follow up</a> (N5) once your team starts to grow.</p>'},
}

NAV = [("paths/", "Paths"), ("skills/", "Skills"), ("lessons/", "Lessons"),
       ("self-assessment/", "Self-assessment"), ("resources/", "Resources"), ("about/", "About")]


def alt_map():
    """Vietnamese path -> English path, for pages that exist in both languages."""
    m = {"": "en/", "lo-trinh/": "en/paths/", "ky-nang/": "en/skills/", "bai-hoc/": "en/lessons/",
         "tu-danh-gia/": "en/self-assessment/", "nhat-ky/": "en/journal/", "tai-nguyen/": "en/resources/",
         "khung-tham-chieu/": "en/frameworks/", "gioi-thieu/": "en/about/"}
    for g in GROUPS:
        m[f"lo-trinh/{g['slug']}/"] = f"en/paths/{g['slug']}/"
    for s in SKILLS:
        m[f"ky-nang/{s['slug']}/"] = f"en/skills/{s['slug']}/"
    for l in LESSONS:
        m[f"bai-hoc/{l['vi']}/"] = f"en/lessons/{l['slug']}/"
    for code in PAGES_MD:
        m[f"tai-nguyen/{code}/"] = f"en/resources/{code}/"
    return m


ALT = alt_map()
REV = {v: k for k, v in ALT.items()}


# ------------------------------------------------------------------ page frame
def run(B):
    """B = the build module (OUT, PREVIEW, PAGES, md_to_html, TODAY)."""
    global _B
    _B = B
    build_home(); build_paths(); build_skills(); build_lessons(); build_self_assessment()
    build_misc()


def page(path, title, body, desc=""):
    B = _B
    depth = path.strip("/").count("/") + 1
    p = "../" * depth
    body = body.replace("{{R}}", p)
    nav = "".join(
        f'<a href="{p}en/{href}"{" aria-current=page" if path.startswith("en/" + href) else ""}>{label}</a>'
        for href, label in NAV)
    vi = REV.get(path, "")
    nav += f'<a class="lang" href="{p}{vi}" lang="vi" hreflang="vi">Tiếng Việt</a>'
    full = f"{title} · {NAME}" if path != "en/" else f"{NAME} – work skills along your career path"
    alts = (f'<link rel="alternate" hreflang="en" href="{SITE}/{path}">'
            + (f'<link rel="alternate" hreflang="vi" href="{SITE}/{vi}">' if path in REV else ""))
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc or 'Free work skills along your career path, from school to management. No login, no tracking.')}">
<link rel="canonical" href="{SITE}/{path}">
{alts}
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<meta property="og:image" content="https://kynanglamviec.com/assets/logo-1024.png">
<link rel="stylesheet" href="{p}assets/style.css">
<script src="{p}assets/js-on.js"></script>
<script src="{p}assets/app.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="{p}en/"><img class="logo" src="{p}assets/logo-icon.svg" alt="" width="40" height="40"><span>Work<br>Skills</span></a>
    <nav class="nav" aria-label="Main">{nav}</nav>
  </div>
</header>
<main id="main" class="wrap">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <p><b>kynanglamviec.com</b> – free, public, no login, no cookies, no trackers.
    Your progress is saved only on your own device.</p>
    <p>The site is written in Vietnamese first. The English edition is adapted with international examples.</p>
    <p>Sister sites: <a href="https://daynentang.com/en/">daynentang.com</a> (values, habits) ·
    <a href="https://tamhonkhoe.com/en/">tamhonkhoe.com</a> (inner life) ·
    trachnhiemxahoi.com (human rights, coming soon) ·
    <a href="https://tienganhcanban.com/">tienganhcanban.com</a> (learning English)</p>
    <p><a href="{p}en/frameworks/">Reference frameworks</a> · <a href="{p}en/journal/">Evidence journal</a> ·
    Original content: CC BY-NC-SA 4.0 · Updated {B.TODAY}</p>
  </div>
</footer>
</body>
</html>
"""
    if B.PREVIEW:
        doc = re.sub(r'href="(?!https?:|mailto:|#)([^"#]*/)(#[^"]*)?"', lambda m: f'href="{m.group(1)}index.html{m.group(2) or ""}"', doc)
    dest = B.OUT / path / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    B.PAGES.append(path)


# ------------------------------------------------------------------ shared pieces
R = "{{R}}en/"   # root of the English edition
RV = "{{R}}"     # root of the Vietnamese site


def skill_link(code):
    s = SKILL[code]
    return f'<a href="{R}skills/{s["slug"]}/">{s["code"]} · {e(s["name"])}</a>'


def lesson_card(l):
    s = SKILL[l["skill"]]
    return f"""<li class="card lesson-card" data-lesson="{e(l['slug'])}">
  <a href="{R}lessons/{e(l['slug'])}/"><b>{e(l['title'])}</b></a>
  <span class="meta">{s['code']} · Level {l['level']} {e(LEVELS[l['level']]['name'])} · {", ".join(l['group'])} · {l['minutes']} min</span>
  <span class="done-flag" hidden>✓ Done</span>
</li>"""


def lessons_list(ls, empty="English lessons are being written."):
    if not ls:
        return f'<p class="muted">{empty}</p>'
    return '<ul class="cards">' + "".join(lesson_card(l) for l in ls) + "</ul>"


def mark(sym, note=""):
    s, label = MARK[sym]
    t = f' <span class="muted">{e(note)}</span>' if note else ""
    return f'<span class="mk mk-{sym}" title="{label}">{s}</span> {label}{t}'


def course_lessons(c):
    return [l for l in LESSONS if l.get("course") == c]


def course_map(c):
    cl = course_lessons(c)
    if c not in COURSES or not cl:
        return ""
    C = COURSES[c]
    steps = "".join(
        f'<li data-lesson="{e(l["slug"])}"><a href="{R}lessons/{e(l["slug"])}/"><b>Lesson {i}. {e(l.get("short", l["title"]))}</b>'
        f'<span>{e(l.get("hook", ""))}</span><span class="meta">{l["skill"]} · Level {l["level"]} · {l["minutes"]} min'
        f'{" · " + e(l["age"]) if l.get("age") else ""}</span></a></li>' for i, l in enumerate(cl, 1))
    return f"""<h2>Map of the {e(C["title"])}</h2>
<p>The course has {len(cl)} lessons, taken in order. {C["thread"]}</p>
<ol class="coursemap">{steps}</ol>
{C.get("after", "")}
<p><a class="btn" href="{R}lessons/{cl[0]['slug']}/">Start Lesson 1</a>
<a class="btn ghost" href="{R}{C["guide"]}">{e(C["guide_label"])}</a></p>
"""


def course_strip(l):
    c = l.get("course")
    if c not in COURSES:
        return ""
    items = ""
    for i, x in enumerate(course_lessons(c), 1):
        cur = ' aria-current="step"' if x["slug"] == l["slug"] else ""
        items += (f'<li data-lesson="{e(x["slug"])}"{cur}><a href="{R}lessons/{e(x["slug"])}/">'
                  f'<span class="cs-n">{i}</span><span class="cs-t">{e(x.get("short", x["title"]))}</span></a></li>')
    C = COURSES[c]
    return (f'<nav class="course-strip" aria-label="Lessons in this course"><p class="small"><b>{e(C["title"])}</b> · '
            f'<a href="{R}{C["home"]}">Course map</a> · <a href="{R}{C["guide"]}">{C["strip_label"]}</a></p><ol>{items}</ol></nav>')


EDITION_NOTE = ('<p class="note small"><b>English edition.</b> Vietnamese is the original language of this site. '
                'English pages are adapted with international examples, not translated word for word. '
                'Every lesson is available in both languages. Vietnamese lessons: <a href="{{R}}bai-hoc/" lang="vi">Bài học</a>.</p>')


# ------------------------------------------------------------------ home
def build_home():
    groups = "".join(f"""<a class="card group-card" href="{R}paths/{g['slug']}/">
  <span class="gcode">{g['code']}</span><b>{e(g['name'])}</b><span>{e(g['short'])}</span>
  <span class="meta">{e(g['levels'])}</span></a>""" for g in GROUPS)
    by_cluster = ""
    for cid, cname in CLUSTERS.items():
        items = "".join(f'<li>{skill_link(s["code"])}</li>' for s in SKILLS if s["cluster"] == cid)
        by_cluster += f'<div class="cluster"><h3>{cid}. {e(cname)}</h3><ul>{items}</ul></div>'
    body = f"""
<section class="hero hero-logo">
  <img class="hero-badge" src="{{{{R}}}}assets/logo.svg" alt="Kỹ Năng Làm Việc logo: a 5-step path up a mountain" width="180" height="193">
  <h1>Work skills, learned along your career path</h1>
  <p class="lead">From pupils exploring jobs to managers leading teams. Free, no login needed.
  Each lesson takes 10–20 minutes, with a workplace scenario and self-check questions.</p>
  <p><a class="btn" href="{R}self-assessment/">Assess your skills</a>
     <a class="btn ghost" href="{R}lessons/">See lessons</a></p>
</section>
{EDITION_NOTE}
<h2>Where are you on your career path?</h2>
<p>Choose the group closest to you. These are suggested paths only: every lesson is open, and you choose your level for each skill.</p>
<div class="grid5">{groups}</div>

<h2>10 skills, 5 clusters</h2>
<p>Each skill has 5 levels: {" → ".join(f"{n}. {e(l['name'])}" for n, l in LEVELS.items())}.</p>
<div class="clusters">{by_cluster}</div>

<h2>How to remember what you learn</h2>
<div class="cols2">
  <div class="card"><b>Self-testing</b><p>Every lesson has scenario questions. Trying to recall the answer helps you remember longer than rereading.</p></div>
  <div class="card"><b>Spaced review</b><p>After a lesson, review it after 1, 3 and 7 days. The site creates a calendar reminder file for you.</p></div>
</div>
<p class="muted small">Source: Dunlosky and colleagues (2013), a review of learning techniques,
<a href="https://journals.sagepub.com/doi/abs/10.1177/1529100612453266">Psychological Science in the Public Interest</a>.
Rereading and highlighting are not among the high-utility techniques.</p>

<h2>English lessons</h2>
{lessons_list(LESSONS[:6])}
"""
    page("en/", NAME, body)


# ------------------------------------------------------------------ paths
def build_paths():
    cards = "".join(f"""<a class="card group-card" href="{g['slug']}/">
  <span class="gcode">{g['code']}</span><b>{e(g['name'])}</b><span>{e(g['short'])}</span>
  <span class="meta">{e(g['levels'])}</span></a>""" for g in GROUPS)
    page("en/paths/", "Paths", f"""<h1>Paths by learner group</h1>
<p class="lead">Seven suggested paths. Nothing is locked. One person can be at different levels in different skills.</p>
<div class="grid5">{cards}</div>""")
    for g in GROUPS:
        rows = "".join(f"<tr><td>{skill_link(c)}</td><td>{mark(*g['matrix'][c])}</td></tr>" for c in SKILL)
        modules = "".join(f"<li>{e(m)}</li>" for m in g["modules"])
        note = f'<p class="note">{e(g["note"])}</p>' if g.get("note") else ""
        ls = [l for l in LESSONS if g["code"] in l["group"]]
        if g["slug"] in COURSES and course_lessons(g["slug"]):
            extra = course_map(g["slug"])
            rest = [l for l in ls if l.get("course") != g["slug"]]
            more = ("<h2>More lessons for this group</h2>" + lessons_list(rest)) if rest else ""
        else:
            extra = (f'<p class="note">The English course for this group is not ready yet. '
                     f'The full Vietnamese course is here: <a href="{RV}lo-trinh/{g["slug"]}/" lang="vi">{g["code"]} (Tiếng Việt)</a>.</p>')
            more = ("<h2>English lessons for this group</h2>" + lessons_list(ls)) if ls else ""
        if g["code"] == "N1":
            extra += ('<div class="note"><b>For parents and teachers.</b> N1 lessons are written for an adult to lead with the child. '
                      'There is no career-choice quiz. The site collects no data about children. '
                      'The journal and self-assessment are not for children to use alone.</div>')
        body = f"""<p class="crumb"><a href="{R}paths/">Paths</a> › {g['code']}</p>
<h1><span class="gcode">{g['code']}</span> {e(g['name'])}</h1>
<p class="lead">{e(g['intro'])}</p>
<p><b>For:</b> {e(g['audience'])}<br><b>Focus levels:</b> {e(g['levels'])}</p>
{note}{extra}
<h2>Suggested modules</h2>
<ol class="modules">{modules}</ol>
{more}
<h2>Focus skills for this group</h2>
<table class="matrix"><thead><tr><th>Skill</th><th>Depth</th></tr></thead><tbody>{rows}</tbody></table>
<p class="muted small">— not taught · ○ introduced · ● core · ◆ advanced</p>
"""
        page(f"en/paths/{g['slug']}/", f"{g['code']} {g['name']}", body, desc=g["intro"][:150])


# ------------------------------------------------------------------ skills
def build_skills():
    rows = ""
    for cid, cname in CLUSTERS.items():
        for s in [s for s in SKILLS if s["cluster"] == cid]:
            rows += (f'<tr><td>{cid}. {e(cname)}</td><td><a href="{s["slug"]}/"><b>{s["code"]}</b> {e(s["name"])}</a></td>'
                     f'<td>{e(s["summary"])}</td></tr>')
    page("en/skills/", "10 skills", f"""<h1>10 work skills</h1>
<p class="lead">Each skill has 5 levels, described with "I can…" statements. Use them to assess yourself and choose lessons.</p>
<table class="matrix"><thead><tr><th>Cluster</th><th>Skill</th><th>What it covers</th></tr></thead><tbody>{rows}</tbody></table>""")
    for s in SKILLS:
        lv = ""
        for n, stmts in s["levels"].items():
            li = "".join(f"<li>{e(x)}</li>" for x in stmts)
            ls = [l for l in LESSONS if l["skill"] == s["code"] and l["level"] == n]
            empty = (f'No English lesson at this level yet. '
                     f'<a href="{RV}ky-nang/{s["slug"]}/" lang="vi">Vietnamese lessons for {s["code"]}</a>.')
            lv += f"""<div class="level"><h3><span class="lvn">Level {n}</span> {e(LEVELS[n]['name'])}</h3>
<p class="muted small">{e(LEVELS[n]['desc'])}</p><ul>{li}</ul>
{lessons_list(ls, empty=empty)}</div>"""
        focus = "".join(
            f'<tr><td><a href="{R}paths/{g["slug"]}/">{g["code"]}</a> {e(g["name"])}</td><td>{mark(*g["matrix"][s["code"]])}</td></tr>'
            for g in GROUPS)
        cl = s.get("crosslink")
        cross = (f'<p class="note">{e(cl["note"])}' + (f' <a href="{cl["url"]}">Go to {cl["site"]}</a>' if cl.get("url") else "") + '</p>') if cl else ""
        fm = "".join(f"<li>{e(x)}</li>" for x in s["framework_map"])
        body = f"""<p class="crumb"><a href="{R}skills/">Skills</a> › {s['code']}</p>
<h1><span class="gcode">{s['code']}</span> {e(s['name'])}</h1>
<p class="lead">{e(s['summary'])}</p>
<p class="muted">Cluster {s['cluster']}. {e(CLUSTERS[s['cluster']])} · Vietnam's 2018 school curriculum, core competency: {e(s['gdpt'])}</p>
{cross}
<h2>The 5 levels of this skill</h2>
{lv}
<p><a class="btn" href="{R}self-assessment/#{s['code']}">Assess yourself on {s['code']}</a></p>
<h2>Depth by learner group</h2>
<table class="matrix"><tbody>{focus}</tbody></table>
<h2>International frameworks referenced</h2>
<ul class="small">{fm}</ul>
<p class="muted small">Framework names are for reference only. The content and "I can…" statements are written by this site.
See <a href="{R}frameworks/">Reference frameworks</a>.</p>
"""
        page(f"en/skills/{s['slug']}/", f"{s['code']} {s['name']}", body, desc=s["summary"])


# ------------------------------------------------------------------ lessons
def quiz_html(l):
    if not l["quiz"]:
        return '<p class="muted">Questions are being written.</p>'
    out = f'<div class="quiz" data-lesson="{e(l["slug"])}">'
    for i, q in enumerate(l["quiz"], 1):
        opts = ""
        for j, o in enumerate(q["options"]):
            ok = "1" if o["correct"] else "0"
            label = "Correct" if o["correct"] else "Not quite"
            opts += f"""<li><button type="button" class="opt" data-correct="{ok}">{chr(65 + j)}. {e(o['text'])}</button>
<p class="why why-{ok}"><b>{label}.</b> {e(o['why'])}</p></li>"""
        out += f'<div class="q"><p class="q-prompt"><b>Question {i}.</b> {e(q["prompt"])}</p><ul class="opts">{opts}</ul></div>'
    return out + '<p class="quiz-score" aria-live="polite"></p></div>'


def meta_table(l):
    s = SKILL[l["skill"]]
    return f"""<table class="meta-table small"><tbody>
<tr><th>skill</th><td>{s['code']} · {e(s['name'])}</td></tr>
<tr><th>level</th><td>Level {l['level']} · {e(LEVELS[l['level']]['name'])}</td></tr>
<tr><th>group</th><td>{", ".join(l['group'])}</td></tr>
<tr><th>framework_map</th><td>{e("; ".join(l['framework_map']))} (reference only)</td></tr>
<tr><th>original</th><td><a href="{RV}bai-hoc/{l['vi']}/" lang="vi">Vietnamese version</a></td></tr>
<tr><th>updated</th><td>{l['updated']}</td></tr></tbody></table>"""


def build_lessons():
    B = _B
    page("en/lessons/", "Lessons", f"""<h1>Lessons</h1>
<p class="lead">Each lesson takes 10–20 minutes and has 9 parts: objectives, warm-up, explanation, example, practice,
self-check, reflection, real-world application, metadata.</p>
{EDITION_NOTE}
{lessons_list(LESSONS)}""")
    for l in LESSONS:
        s = SKILL[l["skill"]]
        h = B.md_to_html(l["body"])
        h = re.sub(r"<h2>(\d)\. ", lambda m: f'<h2 id="p{m.group(1)}">{m.group(1)}. ', h)
        h = h.replace('<h2 id="p6">6. Self-check</h2>',
                      '<h2 id="p6">6. Self-check</h2>\n<p>Choose an answer. Every option has an explanation.</p>\n' + quiz_html(l))
        h = h.replace('<h2 id="p9">9. Metadata</h2>', '<h2 id="p9">9. Metadata</h2>\n' + meta_table(l))
        nav = ""
        if l.get("prev") in LESSON:
            nav += f'<a href="{R}lessons/{l["prev"]}/">← {e(LESSON[l["prev"]]["title"])}</a>'
        if l.get("next") in LESSON:
            nav += f'<a class="next" href="{R}lessons/{l["next"]}/">{e(LESSON[l["next"]]["title"])} →</a>'
        age = f" · {e(l['age'])}" if l.get("age") else ""
        body = f"""<article class="lesson" data-lesson="{e(l['slug'])}" data-title="{e(l['title'])}" data-group="{e(' '.join(l['group']))}">
<p class="crumb"><a href="{R}skills/{s['slug']}/">{s['code']} · {e(s['name'])}</a> › Level {l['level']} {e(LEVELS[l['level']]['name'])}</p>
<h1>{e(l['title'])}</h1>
<p class="meta">{l['minutes']} min · Group {", ".join(l['group'])}{age} · Updated {l['updated']} ·
<a href="{RV}bai-hoc/{l['vi']}/" lang="vi">Bản tiếng Việt</a></p>
{course_strip(l)}
{h}
<section class="finish card">
  <h2>Finish the lesson</h2>
  <p>Mark it as done and the site suggests reviews after 1, 3 and 7 days. The data stays on your device only.</p>
  <button type="button" class="btn" data-action="done">Mark as done</button>
  <div class="review" hidden>
    <p><b>Suggested reviews:</b> <span class="review-dates"></span></p>
    <p><button type="button" class="btn ghost" data-action="ics">Download calendar reminders (.ics)</button>
    <button type="button" class="btn ghost" data-action="undo">Unmark</button></p>
  </div>
</section>
<nav class="pager">{nav}</nav>
</article>"""
        page(f"en/lessons/{l['slug']}/", l["title"], body, desc=" ".join(l["objectives"])[:155])


# ------------------------------------------------------------------ self-assessment
def build_self_assessment():
    blocks = ""
    for s in SKILLS:
        rows = ""
        for n, stmts in s["levels"].items():
            for i, x in enumerate(stmts):
                key = f"{s['code']}-{n}-{i}"
                radios = "".join(f'<label><input type="radio" name="{key}" value="{v}"><span>{e(r)}</span></label>'
                                 for v, r in enumerate(RATING))
                rows += f"""<fieldset class="sa-item" data-key="{key}" data-level="{n}">
<legend><span class="lvn">L{n}</span> {e(x)}</legend><div class="sa-opts">{radios}</div></fieldset>"""
        blocks += f"""<details class="sa-skill" id="{s['code']}" data-skill="{s['code']}">
<summary><b>{s['code']}</b> {e(s['name'])} <span class="sa-result"></span></summary>
{rows}<p class="small"><a href="{R}skills/{s['slug']}/">See skill {s['code']} and its lessons</a></p></details>"""
    data = {s["code"]: {"slug": s["slug"], "name": s["name"],
                        "lessons": [{"slug": l["slug"], "title": l["title"], "level": l["level"]}
                                    for l in LESSONS if l["skill"] == s["code"]]} for s in SKILLS}
    data["_suffix"] = "index.html" if _B.PREVIEW else ""
    data["_base"] = "../lessons/"
    js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page("en/self-assessment/", "Self-assessment", f"""<h1>Assess your skills</h1>
<p class="lead">For each "I can…" statement, choose the option that fits you best. There are no right or wrong answers.</p>
<p class="note">Your answers are saved only in this browser on this device (localStorage). The site sends no data anywhere.
Not for children to use alone.</p>
<p class="small muted">How the suggested level is worked out: the highest level where every statement from Level 1 up to that level
is at "Usually" or above. This only helps you choose lessons. It is not a certificate.
Answers are shared with the Vietnamese version of this page.</p>
<div class="sa">{blocks}</div>
<h2>Summary</h2>
<table class="matrix sa-summary"><thead><tr><th>Skill</th><th>Suggested level</th><th>Lessons to take</th></tr></thead><tbody></tbody></table>
<p class="noprint"><button type="button" class="btn" data-action="print">Print or save as PDF</button>
<button type="button" class="btn ghost" data-action="sa-clear">Clear answers</button></p>
<script type="application/json" id="sa-data">{js}</script>
""")


# ------------------------------------------------------------------ other pages
def build_misc():
    B = _B
    page("en/journal/", "Evidence journal", """<h1>Evidence journal</h1>
<p class="lead">What you write in the Reflection part of each lesson is collected here.
Use it as real examples when you write a CV, interview or prepare for a yearly review.</p>
<p class="note">The journal is saved only in this browser. If you clear your browser data, it will be lost.
Print it or save it as a PDF regularly.</p>
<div class="journal-list"><p class="muted">No entries yet.</p></div>
<p class="noprint"><button type="button" class="btn" data-action="print">Print or save as PDF</button>
<button type="button" class="btn ghost" data-action="journal-clear">Delete the whole journal</button></p>""")

    guides = ""
    for code, (m, _) in PAGES_MD.items():
        guides += f'<h2>{e(m["title"])}</h2><p>{e(m.get("desc", ""))}</p><p><a class="btn" href="{R}resources/{code}/">Open {code.upper()} templates</a></p>'
    page("en/resources/", "Resources", f"""<h1>Printable resources</h1>
<p class="lead">Templates to print or copy into a notebook. Use them with the lessons.</p>
<h2 id="star">Evidence journal template (STAR)</h2>
<p>STAR is a way to tell a work example in 4 parts. It is very useful in interviews.</p>
<table class="matrix print-form"><tbody>
<tr><th>S – Situation</th><td>Where, when, what was the context?</td></tr>
<tr><th>T – Task</th><td>What did you need to do? What result was expected?</td></tr>
<tr><th>A – Action</th><td>What exactly did you do?</td></tr>
<tr><th>R – Result</th><td>What happened? Any numbers? What did you learn?</td></tr>
</tbody></table>
<h2 id="task-list">Five-column task list template</h2>
<table class="matrix print-form"><thead><tr><th>Task</th><th>Result</th><th>Deadline</th><th>Given by</th><th>Status</th></tr></thead>
<tbody><tr><td>&nbsp;</td><td></td><td></td><td></td><td></td></tr><tr><td>&nbsp;</td><td></td><td></td><td></td><td></td></tr>
<tr><td>&nbsp;</td><td></td><td></td><td></td><td></td></tr><tr><td>&nbsp;</td><td></td><td></td><td></td><td></td></tr></tbody></table>
<p class="small muted">Status: Not started · In progress · At risk of delay · Done</p>
<p class="noprint"><a class="btn ghost" href="{{{{R}}}}assets/task-list.csv" download>Download as a spreadsheet (.csv)</a>
<button type="button" class="btn" data-action="print">Print this page</button></p>
{guides}
""")

    for code, (m, b) in PAGES_MD.items():
        page(f"en/resources/{code}/", m["title"],
             f'<p class="crumb"><a href="{R}resources/">Resources</a> › {code.upper()}</p>' + B.md_to_html(b), desc=m.get("desc", ""))

    fw_rows = "".join(
        f"<tr><td>{s['cluster']}. {e(CLUSTERS[s['cluster']])}</td><td>{s['code']} {e(s['name'])}</td>"
        f"<td>{e('; '.join(s['framework_map']))}</td><td>{e(s['gdpt'])}</td></tr>" for s in SKILLS)
    page("en/frameworks/", "Reference frameworks", f"""<h1>Reference frameworks</h1>
<p class="lead">The site's 10-skill framework is built on published international frameworks, adapted to Vietnam
and mapped to the core competencies of Vietnam's 2018 General Education Curriculum.</p>
<p class="note">Framework names are used for reference only. All descriptions, "I can…" statements and lessons are written by this site.
The site does not translate or adapt the content of any framework.</p>
<h2>Mapping table</h2>
<table class="matrix small"><thead><tr><th>Cluster</th><th>Skill</th><th>Main frameworks referenced</th><th>2018 curriculum</th></tr></thead>
<tbody>{fw_rows}</tbody></table>
<h2>Levels</h2>
<p>The site uses 5 levels: {" → ".join(f"{n}. {e(l['name'])}" for n, l in LEVELS.items())}.
For comparison: Australia's Core Skills for Work framework uses 5 stages from Novice to Expert; Singapore's SkillsFuture
Critical Core Skills uses 3 levels: Basic, Intermediate, Advanced.</p>
<h2>Sources</h2>
<ul class="small">
<li><a href="https://www.weforum.org/publications/the-future-of-jobs-report-2025">World Economic Forum – Future of Jobs Report 2025</a></li>
<li><a href="https://www.dewr.gov.au/skills-information-training-providers/core-skills-work-developmental-framework">Core Skills for Work Developmental Framework (CSfW), Australian Government</a></li>
<li><a href="https://www.skillsfuture.gov.sg/initiatives/early-career/criticalcoreskills">SkillsFuture – Critical Core Skills, Singapore</a></li>
<li><a href="https://www.naceweb.org/career-readiness/competencies/career-readiness-defined">NACE – Career Readiness Competencies</a></li>
<li><a href="https://joint-research-centre.ec.europa.eu/jrc-news-and-updates/european-commission-updates-its-digital-competence-framework-digcomp-2025-11-27_en">DigComp 3.0, Joint Research Centre (JRC), European Commission</a></li>
<li><a href="https://publications.jrc.ec.europa.eu/repository/handle/JRC120911">LifeComp, JRC</a></li>
<li><a href="https://www.unicef.org/media/64751/file/Global-framework-on-transferable-skills-2019.pdf">UNICEF – Global Framework on Transferable Skills (2019)</a></li>
<li><a href="https://www.ilo.org/media/455766/download">ILO – core work skills</a></li>
<li><a href="https://www.onetcenter.org/reports/Higher_Order_Styles.html">O*NET – Work Styles</a></li>
<li><a href="https://www.skillsbuilder.uk/universal-framework">Skills Builder Universal Framework</a> (reference only; licensed CC BY-NC-ND 4.0)</li>
<li>Vietnam's 2018 General Education Curriculum, Circular 32/2018/TT-BGDĐT.</li>
</ul>
<p class="muted small">The list of original framework names is on the <a href="{RV}khung-tham-chieu/" lang="vi">Vietnamese version of this page</a>. Last checked 14/11/2026.</p>""")

    page("en/about/", "About", f"""<h1>About</h1>
<p class="lead">kynanglamviec.com teaches work skills along a career path, from school pupils to managers.
Free, public, no login needed.</p>
<h2>How the site is built</h2>
<ul>
<li>10 skills, 5 clusters, 5 levels, based on <a href="{R}frameworks/">international frameworks</a> and adapted to Vietnam.</li>
<li>Every lesson follows 9 parts, with a hypothetical workplace scenario.</li>
<li>Learning uses self-testing and spaced review, two techniques with strong evidence
(<a href="https://journals.sagepub.com/doi/abs/10.1177/1529100612453266">Dunlosky and colleagues, 2013</a>).</li>
<li>No real company or customer names are used. Every scenario is hypothetical.</li>
</ul>
<h2>The English edition</h2>
<p>The site is written in Vietnamese first. English pages are adapted for international readers: names, places and
examples are changed, and Vietnamese law appears only as an example with its source. The meaning and method stay the same.
The English edition now covers the whole site: seven courses (N1 to N7, 53 lessons), 11 core lessons for N2–N3 and 12 standalone lessons, so every skill has a lesson at every level.</p>
<h2>Privacy</h2>
<p>No login, no cookies, no trackers, no external scripts or fonts.
Progress, self-assessment and journal entries are stored only in your browser (localStorage). The site has no server that stores user data.</p>
<h2>Sister sites</h2>
<ul>
<li><a href="https://daynentang.com/en/">daynentang.com</a> – values, ethics, habits, character.</li>
<li><a href="https://tamhonkhoe.com/en/">tamhonkhoe.com</a> – inner life, meditation, Stoicism.</li>
<li>trachnhiemxahoi.com – social compliance, human rights (in Vietnamese, coming soon).</li>
<li><a href="https://tienganhcanban.com/">tienganhcanban.com</a> – learning English.</li>
</ul>
<h2>Licence</h2>
<p>Original content is licensed CC BY-NC-SA 4.0: you may share and adapt it for non-commercial purposes,
with attribution and under the same licence.</p>""")
