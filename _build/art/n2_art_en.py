#!/usr/bin/env python3
"""English edition of the N2 illustrations (same layout as n2_art.py, English labels).
Run: python3 _build/art/n2_art_en.py  -> _build/static/assets/img/en/n2/*.svg
All names, shops and companies shown are hypothetical.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n2_art import (svg, text, lines, box, bar, BRAND, BRAND2, ACC, ACCBG, INK, MUTED,  # noqa: E402
                    RED, REDBG, GREEN, GREENBG, BLUE)

OUT = Path(__file__).resolve().parents[1] / "static/assets/img/en/n2"
SCENES = {}


def scene(name, title):
    def deco(fn):
        SCENES[name] = (title, fn)
        return fn
    return deco


@scene("l1-three-circles", "Three overlapping circles: what I like doing, what I can do with evidence, my real conditions. The overlap in the middle is a direction to test.")
def _():
    b = text(320, 34, "Three circles to choose a direction", 20, BRAND, weight=800)
    b += f'<circle cx="250" cy="170" r="105" fill="{ACC}" fill-opacity=".22" stroke="{ACC}" stroke-width="2"/>'
    b += f'<circle cx="390" cy="170" r="105" fill="{BRAND2}" fill-opacity=".2" stroke="{BRAND2}" stroke-width="2"/>'
    b += f'<circle cx="320" cy="280" r="105" fill="{BLUE}" fill-opacity=".16" stroke="{BLUE}" stroke-width="2"/>'
    b += lines(215, 112, ["What do I", "like doing?"], 14, 18, fill=INK, weight=700)
    b += lines(212, 152, ["Hours fly by,", "never boring"], 12, 16, fill=MUTED)
    b += lines(425, 112, ["What can", "I do?"], 14, 18, fill=INK, weight=700)
    b += lines(428, 152, ["With evidence:", "products, grades"], 12, 16, fill=MUTED)
    b += lines(320, 325, ["Real conditions"], 14, 18, fill=INK, weight=700)
    b += lines(320, 345, ["Time, travel, cost,", "who is hiring"], 12, 16, fill=MUTED)
    b += f'<circle cx="320" cy="210" r="34" fill="#fff" stroke="{BRAND}" stroke-width="2.5"/>'
    b += lines(320, 206, ["Direction", "to test"], 12, 16, fill=BRAND, weight=800)
    return svg(SCENES["l1-three-circles"][0], b)


@scene("l2-two-ads", "Two hypothetical job ads side by side. The left ad states the work, shift, pay and address. The right ad shows three signs to stop: very high pay with vague work, a uniform fee, handing over an original ID card.")
def _():
    b = text(320, 32, "Two job ads (hypothetical)", 19, BRAND, weight=800)
    b += box(24, 50, 286, 328, "#fff", GREEN, 12, 2)
    b += f'<rect x="24" y="50" width="286" height="34" rx="12" fill="{GREENBG}"/>'
    b += text(167, 73, "Ad A · Clear", 15, GREEN, weight=800)
    rowsA = [("Work:", "serve, clear tables, take orders"), ("Shift:", "18:00–22:00, pick 3 a week"),
             ("Pay:", "hourly rate stated, paid monthly"), ("Required:", "aged 18+, can ride a scooter"),
             ("Preferred:", "serving experience"), ("Address:", "number, street, district"),
             ("Contact:", "café manager, office hours")]
    for i, (k, v) in enumerate(rowsA):
        y = 112 + i * 34
        b += text(36, y, k, 12.5, INK, "start", 700) + text(110, y, v, 12.5, INK, "start")
    b += f'<rect x="102" y="{112+3*34-15}" width="200" height="22" rx="5" fill="none" stroke="{GREEN}" stroke-dasharray="4 3"/>'
    b += text(167, 366, "Required and preferred kept apart", 12, GREEN, weight=700)
    b += box(330, 50, 286, 328, "#fff", RED, 12, 2)
    b += f'<rect x="330" y="50" width="286" height="34" rx="12" fill="{REDBG}"/>'
    b += text(473, 73, "Ad B · Stop and check", 15, RED, weight=800)
    rowsB = [("Work:", "\"easy work from home\""), ("Pay:", "\"very high income\""),
             ("Required:", "no experience needed"), ("Process:", "pay a uniform fee"),
             ("", "hand over original ID"), ("Contact:", "messages only, no address")]
    for i, (k, v) in enumerate(rowsB):
        y = 112 + i * 38
        b += text(342, y, k, 12.5, INK, "start", 700) + text(414, y, v, 12.5, INK, "start")
    for y in (112, 150, 226, 264, 302):
        b += f'<circle cx="604" cy="{y-5}" r="8" fill="{RED}"/>' + text(600, y - 1, "!", 13, "#fff", weight=800)
    b += text(473, 366, "Vague · asks for money · keeps originals", 12, RED, weight=700)
    return svg(SCENES["l2-two-ads"][0], b, "#f4f7f6")


@scene("l3-cv", "A one-page CV frame with 5 parts from top to bottom: contact details, a two-line objective, education, activities and experience written as verb plus task plus result, skills with evidence.")
def _():
    b = box(150, 18, 340, 366, "#fff", "#9fb9b6", 6)
    parts = [("1", "Contact", 34, 44), ("2", "Objective (2 lines)", 86, 40), ("3", "Education", 134, 44),
             ("4", "Activities, experience", 186, 120), ("5", "Skills with evidence", 314, 58)]
    for n, name, y, h in parts:
        hi = n == "4"
        b += f'<rect x="164" y="{y}" width="312" height="{h}" rx="6" fill="{ACCBG if hi else "#f2f7f6"}" stroke="{ACC if hi else "#d5e2e0"}"/>'
        b += f'<circle cx="180" cy="{y+14}" r="9" fill="{BRAND}"/>' + text(180, y + 18, n, 11, "#fff", weight=800)
        b += text(196, y + 18, name, 12.5, BRAND, "start", 700)
        rows = max(1, (h - 26) // 14)
        for r in range(rows):
            b += bar(196, y + 26 + r * 14, 250 - (r % 3) * 50)
    b += box(498, 196, 132, 96, "#fff", ACC, 10, 2)
    b += lines(564, 218, ["Each line:", "Verb", "+ task", "+ result, number"], 12, 18, fill=INK, weight=700)
    b += f'<path d="M498,244 L478,244" stroke="{ACC}" stroke-width="2"/>'
    b += box(10, 36, 132, 70, "#fff", BRAND2, 10, 1.5)
    b += lines(76, 58, ["Real-name email,", "phone number,", "town or district"], 12, 16, fill=INK)
    b += f'<path d="M142,56 L164,56" stroke="{BRAND2}" stroke-width="2"/>'
    b += box(10, 300, 132, 70, "#fff", RED, 10, 1.5)
    b += lines(76, 322, ["No ID number,", "no full home", "address"], 12, 16, fill=RED)
    return svg(SCENES["l3-cv"][0], b)


@scene("l4-before-during-after", "Interview timeline. Before: research the employer, practise a 60-second introduction, prepare a STAR example, two questions to ask, tell family where you are going. During: arrive 10 minutes early, hear the whole question, ask if unclear. After: thank them within 24 hours, note the questions asked.")
def _():
    b = text(320, 34, "Interview: before · during · after", 20, BRAND, weight=800)
    b += f'<path d="M40,80 L600,80" stroke="{BRAND2}" stroke-width="4"/>'
    cols = [("Before", ACC, ["Research employer", "60-second intro", "1–2 STAR examples", "2 questions to ask",
                             "Tell family where"]),
            ("During", BRAND2, ["Arrive 10 min early", "Hear whole question", "Unclear? Ask", "Answer with examples",
                                "Ask about next steps"]),
            ("After", BLUE, ["Thanks within 24 h", "Note questions asked", "Note what went well",
                             "Note one thing to fix", "Read the offer"])]
    for i, (name, col, items) in enumerate(cols):
        x = 30 + i * 200
        b += f'<circle cx="{x+90}" cy="80" r="16" fill="{col}"/>'
        b += box(x, 108, 180, 260, "#fff", col, 12, 2)
        b += text(x + 90, 136, name, 17, col, weight=800)
        for j, it in enumerate(items):
            y = 172 + j * 40
            b += f'<rect x="{x+14}" y="{y-12}" width="14" height="14" rx="3" fill="none" stroke="{col}" stroke-width="2"/>'
            b += text(x + 36, y, it, 12.5, INK, "start")
    return svg(SCENES["l4-before-during-after"][0], b)


@scene("l5-messages", "Two phone screens. Left, a vague message: hi, something came up. Right, a clear message: hi, it's Lina from the Friday evening shift, I have a fever so I need to miss tonight's shift, Theo can cover, could you approve this.")
def _():
    b = ""
    for i, (title, col, bg) in enumerate((("Vague", RED, REDBG), ("Clear, complete", GREEN, GREENBG))):
        x = 70 + i * 290
        b += box(x, 22, 210, 356, "#1d2a33", "#1d2a33", 26)
        b += box(x + 10, 46, 190, 306, "#f5f7f8", "#f5f7f8", 14)
        b += f'<rect x="{x+10}" y="46" width="190" height="34" rx="14" fill="{bg}"/>'
        b += text(x + 105, 68, title, 14, col, weight=800)
    b += box(86, 100, 150, 44, "#fff", "#cfd8dc", 12)
    b += lines(161, 118, ["Hi,", "something came up"], 12.5, 17)
    b += box(160, 160, 120, 30, "#dff1ef", "#dff1ef", 12) + text(220, 180, "What is it?", 12.5)
    b += box(86, 206, 120, 30, "#fff", "#cfd8dc", 12) + text(146, 226, "Tonight", 12.5)
    b += box(160, 252, 120, 30, "#dff1ef", "#dff1ef", 12) + text(220, 272, "What about it?", 12.5)
    b += text(175, 330, "Had to ask twice", 12.5, RED, weight=700)
    b += box(376, 96, 176, 196, "#fff", "#cfd8dc", 12)
    b += lines(386, 116, ["Hi, it's Lina from", "the Friday evening shift.", "I have a fever, so I",
                          "need to miss tonight's", "18:00–22:00 shift.", "Theo can cover for me.",
                          "Could you approve this?", "Thank you."], 12, 21, anchor="start")
    b += box(436, 302, 112, 30, "#dff1ef", "#dff1ef", 12) + text(492, 322, "OK, rest well", 12.5)
    b += text(465, 346, "Who · what · need", 12, GREEN, weight=700)
    return svg(SCENES["l5-messages"][0], b, "#eef6f5")


@scene("l6-process-notebook", "A handwritten process notebook page: making peach, orange and lemongrass iced tea, numbered steps, a common mistakes box, and three review boxes for 1, 3 and 7 days, two of them ticked.")
def _():
    b = box(120, 20, 400, 360, "#fffdf6", "#d8cfae", 8)
    for i in range(14):
        b += f'<path d="M140,{78+i*22} L500,{78+i*22}" stroke="#e9e1c7"/>'
    b += f'<path d="M170,20 L170,380" stroke="#e7b3a9" stroke-width="1.5"/>'
    b += text(184, 54, "Process: Peach lemongrass tea (hypothetical)", 14, BRAND, "start", 800)
    steps = ["1. Wash hands, take a size M cup", "2. Add 30 ml peach syrup", "3. Add tea to line 2",
             "4. Ice to line 3, shake 10 times", "5. Add peach, orange, lemongrass", "6. Seal lid, add time sticker"]
    for i, st in enumerate(steps):
        b += text(184, 96 + i * 22, st, 13.5, INK, "start")
    b += box(184, 236, 300, 64, REDBG, RED, 8)
    b += text(196, 256, "Common mistakes", 13, RED, "start", 800)
    b += lines(196, 276, ["No shake → weak tea at the bottom", "Ice before syrup → syrup won't mix"], 12.5, 18, anchor="start")
    b += text(184, 330, "Recall, no notes:", 13, BRAND, "start", 700)
    for i, (lab, done) in enumerate((("1 day", True), ("3 days", True), ("7 days", False))):
        x = 312 + i * 66
        b += f'<rect x="{x}" y="316" width="18" height="18" rx="3" fill="#fff" stroke="{BRAND}" stroke-width="2"/>'
        if done:
            b += f'<path d="M{x+3},{325} l5,5 l8,-10" fill="none" stroke="{GREEN}" stroke-width="3"/>'
        b += text(x + 24, 330, lab, 12, INK, "start")
    return svg(SCENES["l6-process-notebook"][0], b)


@scene("l7-job-ready-file", "A Job-ready file cover with 6 sheets sticking out: direction map, job ad checklist, one-page CV, interview sheet, first-week notebook, process notebook. Beside it is a peer-check list to complete with a friend.")
def _():
    b = text(320, 32, "Job-ready file", 20, BRAND, weight=800)
    tabs = [("1", "Direction map", ACC), ("2", "Job ad checklist", RED), ("3", "One-page CV", BRAND2),
            ("4", "Interview sheet", BLUE), ("5", "First-week notebook", "#8e44ad"), ("6", "Process notebook", GREEN)]
    for i, (n, name, col) in enumerate(tabs):
        y = 62 + i * 44
        b += f'<rect x="{60+i*6}" y="{y}" width="300" height="40" rx="6" fill="#fff" stroke="{col}" stroke-width="2"/>'
        b += f'<circle cx="{84+i*6}" cy="{y+20}" r="11" fill="{col}"/>' + text(84 + i * 6, y + 25, n, 12, "#fff", weight=800)
        b += text(104 + i * 6, y + 25, name, 14, INK, "start", 700)
    b += f'<rect x="40" y="330" width="360" height="44" rx="8" fill="{BRAND}"/>'
    b += text(220, 357, "File cover", 15, "#fff", weight=700)
    b += box(420, 70, 200, 290, "#fff", BRAND2, 12, 2)
    b += text(520, 98, "Peer check", 15, BRAND, weight=800)
    checks = ["All 6 sheets", "CV matches 1 ad", "Each CV line works", "as an example",
              "Intro ≤ 60 seconds", "2 questions to ask", "1–3–7 review plan"]
    y = 128
    for c in checks:
        sub = c == "as an example"
        if not sub:
            b += f'<rect x="436" y="{y-12}" width="14" height="14" rx="3" fill="none" stroke="{BRAND2}" stroke-width="2"/>'
        b += text(458, y, c, 12.5, INK, "start")
        y += 26 if not c.endswith("works") else 18
    return svg(SCENES["l7-job-ready-file"][0], b, "#fdf3e2")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (title, fn) in SCENES.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print(f"Drew {len(SCENES)} figures into {OUT}")
