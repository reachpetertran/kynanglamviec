#!/usr/bin/env python3
"""English edition of the N3 illustrations (same layout as n3_art.py, English labels).
Run: python3 _build/art/n3_art_en.py  -> _build/static/assets/img/en/n3/*.svg
All names and workplaces shown are hypothetical.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n2_art import (svg, text, lines, box, BRAND, BRAND2, ACC, ACCBG, INK, MUTED,  # noqa: E402
                    RED, REDBG, GREEN, GREENBG, BLUE, BLUEBG)

OUT = Path(__file__).resolve().parents[1] / "static/assets/img/en/n3"
SCENES = {}


def scene(name, title):
    def deco(fn):
        SCENES[name] = (title, fn)
        return fn
    return deco


def chip(x, y, s, fill, col, w=None, size=12):
    w = w or (len(s) * 7 + 18)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="{fill}" stroke="{col}"/>'
            + text(x + w / 2, y + 16, s, size, col, weight=700))


def arrow(x1, y1, x2, y2, col=BRAND2):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2.5"/>'
            f'<circle cx="{x2}" cy="{y2}" r="4.5" fill="{col}"/>')


@scene("l1-matrix", "A hypothetical four-box priority matrix. The horizontal axis is whether the deadline is near or far; the vertical axis is whether the impact is high or low. High impact, near deadline: do first. High impact, far deadline: schedule. Low impact, near deadline: do quickly or ask. Low impact, far deadline: later.")
def _():
    b = text(320, 32, "Prioritising: impact × deadline", 19, BRAND, weight=800)
    cells = [(110, 56, RED, REDBG, "1. Do first", ["High impact", "Near deadline"], ["Data report for a", "client, due 15:00"]),
             (370, 56, BLUE, BLUEBG, "2. Schedule", ["High impact", "Far deadline"], ["Learn the new software,", "book 2 time slots"]),
             (110, 212, ACC, ACCBG, "3. Quick or ask", ["Low impact", "Near deadline"], ["Print meeting papers,", "10 minutes"]),
             (370, 212, MUTED, "#f1f4f5", "4. Later", ["Low impact", "Far deadline"], ["Tidy the shared", "folder"])]
    for x, y, col, bg, t, sub, ex in cells:
        b += box(x, y, 240, 140, bg, col, 12, 2)
        b += text(x + 120, y + 28, t, 16, col, weight=800)
        b += lines(x + 120, y + 52, sub, 12, 16, fill=MUTED)
        b += lines(x + 120, y + 100, ex, 13, 17, fill=INK)
    b += lines(60, 140, ["High", "impact"], 12, 15, fill=BRAND, weight=700)
    b += lines(60, 296, ["Low", "impact"], 12, 15, fill=BRAND, weight=700)
    b += text(230, 378, "Near deadline", 13, BRAND, weight=700) + text(490, 378, "Far deadline", 13, BRAND, weight=700)
    return svg(SCENES["l1-matrix"][0], b)


@scene("l2-meeting-page", "A hypothetical meeting notes page with three boxes. Decisions: packaging design B chosen. Actions: who does what, by when, three lines. Open questions: waiting for print quotes. Below is a summary message sent to the team within 24 hours for everyone to confirm.")
def _():
    b = text(320, 32, "Meeting notes page: 3 boxes", 19, BRAND, weight=800)
    b += box(30, 50, 180, 210, GREENBG, GREEN, 12, 2)
    b += text(120, 76, "Decisions", 15, GREEN, weight=800)
    b += lines(120, 110, ["Packaging", "design B", "", "Launch in", "week of 2 Dec"], 13, 18, fill=INK)
    b += box(230, 50, 230, 210, "#fff", BRAND2, 12, 2)
    b += text(345, 76, "Actions: who · what · when", 14, BRAND, weight=800)
    rows = [("Lena", "fix print file", "Wed"), ("Tom", "get 2 quotes", "Thu"), ("Me", "launch plan", "Fri")]
    for i, (a, g, h) in enumerate(rows):
        y = 112 + i * 44
        b += text(248, y, a, 13, INK, "start", 700) + text(296, y, g, 13, INK, "start") + text(444, y, h, 13, RED, "end", 700)
    b += box(480, 50, 130, 210, ACCBG, ACC, 12, 2)
    b += text(545, 76, "Open", 15, ACC, weight=800)
    b += lines(545, 110, ["Print quotes:", "who decides?"], 13, 18, fill=INK)
    b += box(30, 278, 580, 104, "#fff", BLUE, 12, 2)
    b += text(46, 302, "Summary message (sent within 24 hours)", 14, BLUE, "start", 800)
    b += lines(46, 326, ["Summary of this morning: design B agreed, launch week of 2 Dec.",
                         "Actions: Lena fixes the file (Wed), Tom gets quotes (Thu), I do the plan (Fri).",
                         "Please tell me if anything is wrong or missing."], 12.5, 18, fill=INK, anchor="start")
    return svg(SCENES["l2-meeting-page"][0], b)


@scene("l3-four-steps-customer", "Four steps for handling a customer request, hypothetical: listen fully, confirm the need, give an option and a time, follow up until done. On the left, an external customer at an appliance store. On the right, an internal customer, a colleague from accounts.")
def _():
    b = text(320, 32, "Four steps for every customer", 19, BRAND, weight=800)
    steps = [("1", "Listen fully", "Do not interrupt"), ("2", "Confirm", "Sum up the need"),
             ("3", "Option + time", "Within your authority"), ("4", "Follow up", "Report when done")]
    for i, (n, t, s) in enumerate(steps):
        x = 30 + i * 152
        b += box(x, 56, 136, 92, "#fff", BRAND2, 12, 2)
        b += f'<circle cx="{x+22}" cy="80" r="13" fill="{BRAND}"/>' + text(x + 22, 85, n, 13, "#fff", weight=800)
        b += text(x + 82, 86, t, 12.5, INK, weight=800)
        b += text(x + 68, 132, s, 11.5, MUTED)
        if i < 3:
            b += arrow(x + 136, 102, x + 150, 102)
    b += box(30, 170, 284, 206, BLUEBG, BLUE, 12, 2)
    b += text(172, 196, "External customer", 15, BLUE, weight=800)
    b += lines(46, 224, ["Customer: \"My new washing machine", "is really loud. I want a new one.\"",
                         "Me: \"So it has been loud since the first", "wash, and you want it replaced?\"",
                         "Technician visits at 10:00 tomorrow;", "I will call you in the afternoon."], 12, 22, fill=INK, anchor="start")
    b += box(326, 170, 284, 206, GREENBG, GREEN, 12, 2)
    b += text(468, 196, "Internal customer", 15, GREEN, weight=800)
    b += lines(342, 224, ["Accounts: \"Send me the sales table.\"",
                          "Me: \"Which month? By store", "or by salesperson?\"",
                          "\"October, by store.\"",
                          "\"OK, I will send the spreadsheet", "before 16:00 today.\""], 12, 22, fill=INK, anchor="start")
    return svg(SCENES["l3-four-steps-customer"][0], b)


@scene("l4-five-whys", "A hypothetical chain of why questions in a garment workshop. Symptom: a batch of shirts was returned for wrong size labels. Why 1: size M labels were sewn onto size L shirts. Why 2: the two label boxes sat side by side, same colour. Why 3: the label shelf had no separate slots by size. Root cause: no rule for arranging the shelf. Quick fix: recheck the batch. Root fix: slots by size, a colour for each size.")
def _():
    b = text(320, 32, "Ask \"Why?\" until you reach the root cause", 19, BRAND, weight=800)
    b += box(30, 50, 580, 40, REDBG, RED, 10, 2)
    b += text(320, 76, "Symptom: a batch of 300 shirts returned for wrong size labels", 14, RED, weight=800)
    whys = ["Why? Size M labels were sewn onto size L shirts.",
            "Why? The M and L label boxes sit side by side, same colour.",
            "Why? The label shelf has no separate slots by size.",
            "Why? There is no rule for arranging the label shelf."]
    for i, w in enumerate(whys):
        y = 104 + i * 46
        b += box(50 + i * 18, y, 470, 36, "#fff", BRAND2, 8, 1.5)
        b += text(66 + i * 18, y + 23, w, 13, INK, "start")
    b += box(30, 296, 280, 84, ACCBG, ACC, 12, 2)
    b += text(170, 320, "Quick fix (today)", 14, ACC, weight=800)
    b += lines(170, 344, ["Recheck the whole batch,", "replace wrong labels"], 12.5, 17, fill=INK)
    b += box(330, 296, 280, 84, GREENBG, GREEN, 12, 2)
    b += text(470, 320, "Root fix (so it does not recur)", 14, GREEN, weight=800)
    b += lines(470, 344, ["Shelf slots by size,", "a different colour for each size"], 12.5, 17, fill=INK)
    return svg(SCENES["l4-five-whys"][0], b)


@scene("l5-lessons-learned", "Four steps when work does not go to plan: report at once, fix it, review with four questions, share the new way of working. The four questions: what did I plan, what actually happened, why was it different, what will I do next time.")
def _():
    b = text(320, 32, "When work does not go to plan", 19, BRAND, weight=800)
    steps = [("Report now", RED, REDBG), ("Fix it", ACC, ACCBG), ("Review", BLUE, BLUEBG), ("Share", GREEN, GREENBG)]
    for i, (t, col, bg) in enumerate(steps):
        x = 30 + i * 152
        b += box(x, 54, 136, 52, bg, col, 26, 2)
        b += text(x + 68, 86, t, 14, col, weight=800)
        if i < 3:
            b += arrow(x + 136, 80, x + 150, 80)
    b += box(90, 132, 460, 246, "#fff", BLUE, 14, 2)
    b += text(320, 160, "Review: 4 questions", 16, BLUE, weight=800)
    qs = [("1", "What did I plan?", "Send 200 invitations by Friday"),
          ("2", "What actually happened?", "Sent 180; 20 new customers missed"),
          ("3", "Why was it different?", "Used last year's list, without new customers"),
          ("4", "What will I do next time?", "Ask for the latest list before sending")]
    for i, (n, q, a) in enumerate(qs):
        y = 196 + i * 46
        b += f'<circle cx="122" cy="{y-5}" r="12" fill="{BLUE}"/>' + text(122, y, n, 12, "#fff", weight=800)
        b += text(144, y - 6, q, 13.5, INK, "start", 800)
        b += text(144, y + 12, a + " (hypothetical)", 12, MUTED, "start")
    return svg(SCENES["l5-lessons-learned"][0], b, "#eef3fa")


@scene("l6-coordination-map", "A hypothetical coordination map for a new salesperson. In the middle is Me. Around it are four contacts: warehouse, accounts, customer service, team leader. Each contact shows what I need from them and what they need from me.")
def _():
    b = text(320, 32, "Coordination map", 19, BRAND, weight=800)
    nodes = [(40, 56, "Warehouse", "Need: stock levels by 9:00", "They need: orders with item codes"),
             (380, 56, "Accounts", "Need: payment confirmation", "They need: invoices on time"),
             (40, 284, "Customer service", "Need: notes on hard cases", "They need: exact delivery times"),
             (380, 284, "Team leader", "Need: priorities when tasks clash", "They need: early warning of delays")]
    for x, y, t, need, give in nodes:
        b += box(x, y, 220, 92, "#fff", BRAND2, 12, 2)
        b += text(x + 110, y + 24, t, 14, BRAND, weight=800)
        b += text(x + 14, y + 50, need, 11.5, INK, "start")
        b += text(x + 12, y + 74, give, 11, ACC, "start", 700)
        cx, cy = x + 110, (y + 92 if y < 200 else y)
        b += f'<line x1="{cx}" y1="{cy}" x2="320" y2="214" stroke="{BRAND2}" stroke-width="1.5" stroke-dasharray="5 4"/>'
    b += f'<circle cx="320" cy="214" r="46" fill="{BRAND}"/>' + lines(320, 210, ["Me", "(sales)"], 13, 17, fill="#fff", weight=800)
    return svg(SCENES["l6-coordination-map"][0], b)


@scene("l7-review-file", "A hypothetical file for a 90-day review. On the left are the six sheets of the 90-day notebook. An arrow leads to the right: three STAR examples with numbers, the I can self-assessment, two questions for your manager, three goals for the next 90 days.")
def _():
    b = text(320, 32, "From the 90-day notebook to your review", 19, BRAND, weight=800)
    sheets = ["1 Weekly task board", "2 Meeting notes page", "3 Customer request log", "4 Incident sheet", "5 Lessons-learned sheet", "6 Coordination map"]
    for i, t in enumerate(sheets):
        y = 56 + i * 52
        b += box(30 + i * 4, y, 230, 42, "#fff", BRAND2, 8, 1.5)
        b += text(46 + i * 4, y + 26, "Sheet " + t, 12.5, INK, "start", 700)
    b += arrow(280, 214, 330, 214, ACC)
    b += box(340, 56, 270, 320, ACCBG, ACC, 14, 2)
    b += text(475, 84, "Bring to your review", 15, ACC, weight=800)
    items = ["3 STAR examples with numbers", "\"I can…\" self-assessment", "1 strength, 1 area to improve",
             "2 questions for your manager", "3 goals for the next 90 days"]
    for i, t in enumerate(items):
        y = 124 + i * 50
        b += f'<rect x="358" y="{y-14}" width="16" height="16" rx="3" fill="#fff" stroke="{ACC}" stroke-width="2"/>'
        b += text(384, y, t, 13, INK, "start")
    return svg(SCENES["l7-review-file"][0], b, "#fdf3e2")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (title, fn) in SCENES.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print(f"Drew {len(SCENES)} images into {OUT}")
