/* kynanglamviec.com – mọi dữ liệu chỉ lưu localStorage trên máy người học. Không gửi đi đâu. */
(function () {
  "use strict";
  var NS = "klv:";
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(NS + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(NS + k, JSON.stringify(v)); return true; } catch (e) { return false; } },
    del: function (k) { try { localStorage.removeItem(NS + k); } catch (e) {} },
    keys: function () { var o = []; try { for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (k.indexOf(NS) === 0) o.push(k.slice(NS.length)); } } catch (e) {} return o; }
  };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var fmt = function (d) { return d.toLocaleDateString("vi-VN", { weekday: "short", day: "2-digit", month: "2-digit" }); };
  var addDays = function (d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };

  /* ---------- in trang ---------- */
  $$('[data-action="print"]').forEach(function (b) {
    b.addEventListener("click", function () { $$("details").forEach(function (d) { d.open = true; }); window.print(); });
  });

  /* ---------- đánh dấu bài đã học trên danh sách ---------- */
  $$(".lesson-card").forEach(function (c) {
    if (store.get("done:" + c.dataset.lesson)) { var f = $(".done-flag", c); if (f) f.hidden = false; }
  });

  /* ---------- tự kiểm tra ---------- */
  $$(".quiz").forEach(function (quiz) {
    var qs = $$(".q", quiz), right = 0, answered = 0;
    qs.forEach(function (q) {
      $$(".opt", q).forEach(function (btn) {
        btn.addEventListener("click", function () {
          if (q.classList.contains("answered")) return;
          q.classList.add("answered"); answered++;
          var ok = btn.dataset.correct === "1"; if (ok) right++;
          btn.classList.add(ok ? "right" : "wrong");
          $$(".opt", q).forEach(function (b) { b.disabled = true; if (b.dataset.correct === "1") b.classList.add("right"); });
          if (answered === qs.length) {
            $(".quiz-score", quiz).textContent = "Bạn trả lời đúng " + right + "/" + qs.length + " câu. " +
              (right === qs.length ? "Rất tốt! Nhớ ôn lại theo lịch." : "Đọc kỹ giải thích, rồi làm lại sau 1 ngày.");
          }
        });
      });
    });
  });

  /* ---------- bài học: phản tư + hoàn thành ---------- */
  var lesson = $("article.lesson");
  if (lesson) {
    var slug = lesson.dataset.lesson, title = lesson.dataset.title;
    // Phản tư: thêm ô ghi sau từng câu hỏi trong phần 7
    var h7 = $("#p7"), list = h7 && h7.nextElementSibling;
    if (list && list.tagName === "OL") {
      $$("li", list).forEach(function (li, i) {
        var key = "j:" + slug + ":" + i;
        var ta = document.createElement("textarea");
        ta.className = "reflect"; ta.setAttribute("aria-label", "Ghi câu trả lời " + (i + 1));
        ta.placeholder = "Ghi vào nhật ký bằng chứng (chỉ lưu trên máy này)…";
        var saved = store.get(key); if (saved) ta.value = saved.a;
        var msg = document.createElement("span"); msg.className = "saved";
        var t;
        ta.addEventListener("input", function () {
          clearTimeout(t);
          t = setTimeout(function () {
            if (ta.value.trim()) store.set(key, { slug: slug, title: title, q: li.firstChild.textContent.trim(), a: ta.value, d: new Date().toISOString() });
            else store.del(key);
            msg.textContent = "Đã lưu";
          }, 500);
        });
        li.appendChild(ta); li.appendChild(msg);
      });
    }
    // Hoàn thành + lịch ôn 1, 3, 7 ngày
    var box = $(".finish", lesson), review = $(".review", box), btnDone = $('[data-action="done"]', box);
    var show = function () {
      var d = store.get("done:" + slug);
      if (!d) { review.hidden = true; btnDone.hidden = false; return; }
      var base = new Date(d);
      $(".review-dates", box).textContent = [1, 3, 7].map(function (n) { return fmt(addDays(base, n)); }).join(" · ");
      review.hidden = false; btnDone.hidden = true;
    };
    btnDone.addEventListener("click", function () { store.set("done:" + slug, new Date().toISOString()); show(); });
    $('[data-action="undo"]', box).addEventListener("click", function () { store.del("done:" + slug); show(); });
    $('[data-action="ics"]', box).addEventListener("click", function () {
      var base = new Date(store.get("done:" + slug) || Date.now());
      var ymd = function (x) { return x.getFullYear() + String(x.getMonth() + 1).padStart(2, "0") + String(x.getDate()).padStart(2, "0"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+/, "");
      var url = location.href.split("#")[0];
      var ev = [1, 3, 7].map(function (n) {
        var s = addDays(base, n), en = addDays(base, n + 1);
        return ["BEGIN:VEVENT", "UID:" + slug + "-" + n + "-" + ymd(base) + "@kynanglamviec.com", "DTSTAMP:" + stamp,
          "DTSTART;VALUE=DATE:" + ymd(s), "DTEND;VALUE=DATE:" + ymd(en),
          "SUMMARY:Ôn bài (ngày " + n + "): " + title.replace(/[,;]/g, " "),
          "DESCRIPTION:Làm lại phần Tự kiểm tra trước khi xem giải thích. " + url, "URL:" + url, "END:VEVENT"].join("\r\n");
      });
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//kynanglamviec.com//VI", "CALSCALE:GREGORIAN"].concat(ev, ["END:VCALENDAR"]).join("\r\n");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics], { type: "text/calendar;charset=utf-8" }));
      a.download = "on-bai-" + slug + ".ics"; document.body.appendChild(a); a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    });
    show();
  }

  /* ---------- tự đánh giá ---------- */
  var sa = $(".sa");
  if (sa) {
    var data = JSON.parse($("#sa-data").textContent);
    var answers = store.get("sa", {});
    var levelOf = function (code) {
      var lvl = 0;
      for (var n = 1; n <= 5; n++) {
        var items = $$('.sa-item[data-key^="' + code + "-" + n + '-"]');
        var allOk = items.every(function (it) { var v = answers[it.dataset.key]; return v !== undefined && v >= 2; });
        if (allOk) lvl = n; else break;
      }
      return lvl;
    };
    var answeredCount = function (code) { return Object.keys(answers).filter(function (k) { return k.indexOf(code + "-") === 0; }).length; };
    var render = function () {
      var rows = "";
      $$(".sa-skill").forEach(function (d) {
        var code = d.dataset.skill, n = answeredCount(code), lv = levelOf(code);
        $(".sa-result", d).textContent = n ? "· Bậc gợi ý: " + (lv ? lv : "dưới Bậc 1") + " (" + n + "/15 câu)" : "";
        if (!n) return;
        var next = Math.min(lv + 1, 5);
        var ls = data[code].lessons.filter(function (l) { return l.level === next || l.level === lv; });
        var links = ls.length ? ls.map(function (l) { return '<a href="../bai-hoc/' + l.slug + '/' + (data._suffix || "") + '">' + esc(l.title) + "</a>"; }).join("<br>")
          : '<span class="muted">Chưa có bài ở Bậc ' + next + ".</span>";
        rows += "<tr><td><b>" + code + "</b> " + esc(data[code].name) + "</td><td>" + (lv ? "Bậc " + lv : "Dưới Bậc 1") + "</td><td>" + links + "</td></tr>";
      });
      $(".sa-summary tbody").innerHTML = rows || '<tr><td colspan="3" class="muted">Chưa có câu trả lời.</td></tr>';
    };
    $$(".sa-item").forEach(function (it) {
      var k = it.dataset.key;
      if (answers[k] !== undefined) { var r = $('input[value="' + answers[k] + '"]', it); if (r) r.checked = true; }
      it.addEventListener("change", function (ev) { answers[k] = +ev.target.value; store.set("sa", answers); render(); });
    });
    if (location.hash) { var t = document.getElementById(location.hash.slice(1)); if (t && t.tagName === "DETAILS") t.open = true; }
    $('[data-action="sa-clear"]').addEventListener("click", function () {
      if (window.confirm("Xóa toàn bộ câu trả lời tự đánh giá?")) { answers = {}; store.del("sa"); $$(".sa-item input").forEach(function (i) { i.checked = false; }); render(); }
    });
    render();
  }

  /* ---------- nhật ký bằng chứng ---------- */
  var jl = $(".journal-list");
  if (jl) {
    var drawJ = function () {
      var es = store.keys().filter(function (k) { return k.indexOf("j:") === 0; }).map(function (k) { return store.get(k); })
        .filter(Boolean).sort(function (a, b) { return a.d < b.d ? 1 : -1; });
      jl.innerHTML = es.length ? es.map(function (x) {
        return '<div class="card journal-entry"><span class="meta">' + esc(new Date(x.d).toLocaleDateString("vi-VN")) + " · " + esc(x.title) +
          "</span><p><b>" + esc(x.q) + "</b></p><p>" + esc(x.a).replace(/\n/g, "<br>") + "</p></div>";
      }).join("") : '<p class="muted">Chưa có ghi chép nào. Hãy viết ở phần Phản tư của một bài học.</p>';
    };
    $('[data-action="journal-clear"]').addEventListener("click", function () {
      if (!window.confirm("Xóa toàn bộ nhật ký trên máy này?")) return;
      store.keys().filter(function (k) { return k.indexOf("j:") === 0; }).forEach(store.del); drawJ();
    });
    drawJ();
  }
})();
