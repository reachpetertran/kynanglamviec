// Khung app Kỹ Năng Làm Việc. Mọi thứ lưu trên máy (localStorage). Không gọi mạng, không theo dõi.
// Dữ liệu học dùng chung với site (tiền tố "klv:": done, j, sa). Cài đặt và dữ liệu riêng của app: một khóa "klv.app.v1".
(function () {
  var KEY = 'klv.app.v1', NS = 'klv:', D = window.KLV || { courses: [], lessons: [], pages: [] };
  var EN = document.documentElement.lang === 'en', LG = EN ? 'en' : 'vi';
  var L = EN ? {
    save: 'Save this lesson', saved: 'Saved ✓', lessonOf: 'Lesson', of: 'of', cont: 'Continue reading',
    prog: 'lessons done', start: 'Start', goon: 'Continue', finished: 'Course finished. Remember to review on schedule.', now: 'Courses in progress',
    week: 'This week', days: 'days of learning', savedH: 'Saved lessons', none: 'Nothing here yet.',
    journal: 'Evidence journal', jn: 'entries', sa: 'Self-assessment', san: 'statements answered',
    wipe: 'Delete all my data on this phone', wipe2: 'Tap again to delete everything', noRes: 'No results.',
    search: 'Search lessons, courses and skills', ph: 'e.g. email, feedback, interview', course: 'Course', lesson: 'Lesson', page: 'Page',
    allC: 'All courses', dn: ['M', 'T', 'W', 'T', 'F', 'S', 'S']
  } : {
    save: 'Lưu bài này', saved: 'Đã lưu ✓', lessonOf: 'Bài', of: 'trên', cont: 'Đọc tiếp',
    prog: 'bài đã xong', start: 'Bắt đầu', goon: 'Học tiếp', finished: 'Bạn đã học xong khóa này. Nhớ ôn theo lịch.', now: 'Khóa đang học',
    week: 'Tuần này', days: 'ngày có học', savedH: 'Bài đã lưu', none: 'Chưa có gì ở đây.',
    journal: 'Nhật ký bằng chứng', jn: 'ghi chép', sa: 'Tự đánh giá', san: 'câu đã trả lời',
    wipe: 'Xóa mọi dữ liệu của tôi trên máy này', wipe2: 'Bấm lần nữa để xóa hết', noRes: 'Không tìm thấy.',
    search: 'Tìm bài, khóa hoặc kỹ năng', ph: 'Ví dụ: email, phản hồi, phỏng vấn', course: 'Khóa', lesson: 'Bài', page: 'Trang',
    allC: 'Tất cả khóa', dn: ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
  };

  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
  function get(k) { try { var v = localStorage.getItem(NS + k); return v === null ? null : JSON.parse(v); } catch (e) { return null; } }
  function siteKeys() { var o = []; try { for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (k && k.indexOf(NS) === 0) o.push(k); } } catch (e) {} return o; }
  var st = load();
  ['saved', 'days'].forEach(function (k) { st[k] = st[k] || {}; });
  function $(id) { return document.getElementById(id); }
  function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
  function href(p) { return p + 'index.html'; }
  function el(tag, cls, h) { var e = document.createElement(tag); if (cls) e.className = cls; if (h != null) e.innerHTML = h; return e; }
  function ymd(d) { d = d || new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function slugOf(p) { var m = p.match(/\/([^\/]+)\/$/); return m ? m[1] : ''; }
  function isDone(slug) { return !!get('done:' + slug); }

  // ---------- Link thư mục -> index.html (an toàn cho cả link do script của site sinh ra) ----------
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.target === '_blank' || a.origin !== location.origin) return;
    if (/\/$/.test(a.pathname)) { e.preventDefault(); location.href = a.pathname + 'index.html' + a.search + a.hash; }
  }, true);

  // ---------- Cỡ chữ, màu nền, ngôn ngữ ----------
  var root = document.documentElement, mq = window.matchMedia ? matchMedia('(prefers-color-scheme: dark)') : null;
  if (mq && mq.addEventListener) mq.addEventListener('change', function () { apply(); });
  function mark(id, v) {
    var box = $(id); if (!box) return;
    [].forEach.call(box.querySelectorAll('button'), function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-v') === v ? 'true' : 'false'); });
  }
  function apply() {
    root.setAttribute('data-size', st.size || 'm');
    var dark = st.theme === 'dark' || (st.theme !== 'light' && mq && mq.matches);
    if (dark) root.setAttribute('data-dark', ''); else root.removeAttribute('data-dark');
    mark('app-size', st.size || 'm'); mark('app-theme', st.theme || 'auto');
  }
  function bind(id, prop) {
    var box = $(id); if (!box) return;
    box.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; st[prop] = b.getAttribute('data-v'); save(); apply(); });
  }
  apply(); bind('app-size', 'size'); bind('app-theme', 'theme');
  var aa = $('app-aa'), panel = $('app-panel');
  if (aa && panel) {
    aa.addEventListener('click', function () { panel.hidden = !panel.hidden; aa.setAttribute('aria-expanded', String(!panel.hidden)); });
    document.addEventListener('click', function (e) { if (!panel.hidden && !panel.contains(e.target) && e.target !== aa) { panel.hidden = true; aa.setAttribute('aria-expanded', 'false'); } });
  }
  var lg = $('app-lang');
  if (lg) lg.addEventListener('click', function (e) { var a = e.target.closest('a'); if (a) { st.lang = a.getAttribute('data-v'); save(); } });

  var path = location.pathname.replace(/index\.html$/, '');
  // Mở app lần sau: vào đúng ngôn ngữ đã chọn
  var first = true; try { first = !sessionStorage.getItem('klv.go'); sessionStorage.setItem('klv.go', '1'); } catch (e) {}
  if (first && path === '/' && st.lang === 'en') { location.replace('/en/index.html'); return; }

  // ---------- Danh mục ----------
  var COURSES = D.courses.filter(function (c) { return c.g === LG; });
  var course = null, idx = -1;
  COURSES.forEach(function (c) {
    if (c.p === path) course = c;
    c.l.forEach(function (l, i) { if (l[0] === path) { course = c; idx = i; } });
  });
  function count(c) { var n = 0; c.l.forEach(function (l) { if (isDone(l[2])) n++; }); return n; }
  function nextOf(c) { for (var i = 0; i < c.l.length; i++) if (!isDone(c.l[i][2])) return c.l[i]; return null; }
  function bar(n, total) { return '<span class="app-bar" role="img" aria-label="' + n + '/' + total + '"><i style="width:' + (total ? Math.round(n / total * 100) : 0) + '%"></i></span>'; }
  function courseCard(c) {
    var n = count(c), nx = nextOf(c);
    return '<a class="app-course" href="' + href(nx ? nx[0] : c.p) + '"><strong>' + esc(c.t) + '</strong>' + bar(n, c.l.length) +
      '<small>' + n + '/' + c.l.length + ' ' + L.prog + (nx ? ' · ' + L.goon + ': ' + esc(nx[1]) : ' · ' + L.finished) + '</small></a>';
  }
  function active() { return COURSES.filter(function (c) { var n = count(c); return n > 0 && n < c.l.length; }); }

  var main = document.querySelector('main');
  var lesson = document.querySelector('article.lesson');
  var title = lesson ? lesson.getAttribute('data-title') : (document.querySelector('h1') || {}).textContent;

  // ---------- Bài học ----------
  if (lesson) {
    var slug = lesson.getAttribute('data-lesson');
    st.days[ymd()] = 1;
    st.last = { p: path, t: title, y: (st.last && st.last.p === path) ? st.last.y : 0 }; save();
    if (st.last.y > 200) requestAnimationFrame(function () { window.scrollTo(0, st.last.y); });
    var tick = null;
    window.addEventListener('scroll', function () {
      if (tick) return;
      tick = setTimeout(function () { tick = null; st.last.y = Math.round(window.scrollY); save(); }, 800);
    }, { passive: true });

    if (idx >= 0) {
      var crumb = el('a', 'app-crumb', '<small>' + esc(course.t) + ' · ' + L.lessonOf + ' ' + (idx + 1) + ' ' + L.of + ' ' + course.l.length + '</small>' + bar(count(course), course.l.length));
      crumb.href = href(course.p);
      lesson.insertBefore(crumb, lesson.firstChild);
    }
    var fin = lesson.querySelector('.finish');
    var sb = el('button', 'btn ghost app-save'); sb.type = 'button';
    var paint = function () { var s = !!st.saved[path]; sb.textContent = s ? L.saved : L.save; sb.setAttribute('aria-pressed', s); };
    sb.addEventListener('click', function () { if (st.saved[path]) delete st.saved[path]; else st.saved[path] = title; save(); paint(); });
    paint();
    if (fin) fin.appendChild(sb); else lesson.appendChild(sb);
    // Bấm "Đánh dấu đã học" của site: ghi ngày có học
    lesson.addEventListener('click', function (e) { if (e.target.closest('[data-action="done"]')) { st.days[ymd()] = 1; save(); } });
  }

  // ---------- Trang nhóm có khóa: thanh tiến độ và nút học tiếp ----------
  if (course && idx < 0 && main && course.l.length) {
    var n = count(course), nx = nextOf(course);
    var card = el('div', 'app-progress', '<strong>' + esc(course.t) + ': ' + n + '/' + course.l.length + ' ' + L.prog + '</strong>' + bar(n, course.l.length) +
      (nx ? '<a class="btn" href="' + href(nx[0]) + '">' + (n ? L.goon : L.start) + ': ' + esc(nx[1]) + '</a>' : '<p>' + L.finished + '</p>'));
    var lead = main.querySelector('.lead');
    if (lead) lead.parentNode.insertBefore(card, lead.nextSibling); else main.insertBefore(card, main.firstChild);
  }

  // ---------- Trang chủ: đọc tiếp, khóa đang học ----------
  if ((path === '/' || path === '/en/') && main) {
    var top = el('div', 'app-home');
    if (st.last && st.last.p.indexOf(EN ? '/en/' : '/bai-hoc/') === 0) top.innerHTML += '<a class="app-continue" href="' + href(st.last.p) + '"><small>' + L.cont + '</small><strong>' + esc(st.last.t) + '</strong></a>';
    active().slice(0, 3).forEach(function (c) { top.innerHTML += courseCard(c); });
    if (top.innerHTML) main.insertBefore(top, main.firstChild);
  }

  // ---------- Tab Bài học: tìm kiếm gõ không dấu ----------
  if (path === (EN ? '/en/lessons/' : '/bai-hoc/') && main) {
    var norm = function (s) { return String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd'); };
    var items = [];
    COURSES.forEach(function (c) { items.push([c.p, c.t, L.course, norm(c.t)]); });
    D.lessons.forEach(function (l) { if (l[4] === LG) items.push([l[0], l[1], l[2], norm(l[1] + ' ' + l[2])]); });
    D.pages.forEach(function (p) { if (p[2] === LG && !/\/(bai-hoc|lessons)\/$/.test(p[0])) items.push([p[0], p[1], L.page, norm(p[1])]); });
    var box = el('div', 'app-searchbox', '<label class="app-search"><span class="small muted">' + L.search + '</span>' +
      '<input type="search" id="app-q" placeholder="' + L.ph + '" autocomplete="off"></label><div id="app-results" class="app-list" aria-live="polite"></div>');
    var h1 = main.querySelector('h1'), after = main.querySelector('.lead') || h1;
    if (after) after.parentNode.insertBefore(box, after.nextSibling); else main.insertBefore(box, main.firstChild);
    var q = $('app-q'), res = $('app-results');
    q.addEventListener('input', function () {
      var words = norm(q.value).split(/\s+/).filter(Boolean);
      if (!words.length) { res.innerHTML = ''; return; }
      var hit = items.filter(function (it) { return words.every(function (w) { return it[3].indexOf(w) >= 0; }); }).slice(0, 40);
      res.innerHTML = hit.length ? hit.map(function (it) {
        var d = slugOf(it[0]) && isDone(slugOf(it[0])) ? ' <span class="app-tick">✓</span>' : '';
        return '<a href="' + href(it[0]) + '"><small>' + esc(it[2]) + '</small>' + esc(it[1]) + d + '</a>';
      }).join('') : '<p class="muted">' + L.noRes + '</p>';
    });
  }

  // ---------- Tab Của tôi ----------
  var mine = $('app-mine');
  if (mine) {
    // ngày có học = ngày mở bài + ngày bấm "đã học" (site lưu thời điểm)
    var days = {}; Object.keys(st.days).forEach(function (k) { days[k] = 1; });
    siteKeys().forEach(function (k) { if (k.indexOf(NS + 'done:') === 0) { var v = get(k.slice(NS.length)); if (typeof v === 'string') days[ymd(new Date(v))] = 1; } });
    var h = '', d = new Date(), dow = (d.getDay() + 6) % 7, got = 0, dots = '';
    for (var i = 0; i < 7; i++) {
      var x = new Date(d); x.setDate(d.getDate() - dow + i);
      var on = !!days[ymd(x)]; if (on) got++;
      dots += '<span class="' + (on ? 'on' : '') + (i === dow ? ' today' : '') + '"><i></i>' + L.dn[i] + '</span>';
    }
    h += '<h2>' + L.week + '</h2><div class="app-week" role="img" aria-label="' + got + ' ' + L.days + '">' + dots + '</div><p class="small muted">' + got + ' ' + L.days + '</p>';
    if (st.last) h += '<h2>' + L.cont + '</h2><a class="app-continue" href="' + href(st.last.p) + '"><strong>' + esc(st.last.t) + '</strong></a>';
    var all = COURSES.filter(function (c) { return count(c) > 0; });
    h += '<h2>' + L.now + '</h2>' + (all.length ? all.map(courseCard).join('') : '<p class="muted">' + L.none + '</p>');
    var sk = Object.keys(st.saved).filter(function (k) { return (k.indexOf('/en/') === 0) === EN; });
    h += '<h2>' + L.savedH + '</h2>' + (sk.length ? '<div class="app-list">' + sk.map(function (k) { return '<a href="' + href(k) + '">' + esc(st.saved[k]) + (isDone(slugOf(k)) ? ' <span class="app-tick">✓</span>' : '') + '</a>'; }).join('') + '</div>' : '<p class="muted">' + L.none + '</p>');
    var nj = siteKeys().filter(function (k) { return k.indexOf(NS + 'j:') === 0; }).length;
    var sa = get('sa') || {}, ns = Object.keys(sa).length;
    h += '<div class="app-list"><a href="' + (EN ? '/en/journal/index.html' : '/nhat-ky/index.html') + '"><small>' + nj + ' ' + L.jn + '</small>' + L.journal + '</a>' +
      '<a href="' + (EN ? '/en/self-assessment/index.html' : '/tu-danh-gia/index.html') + '"><small>' + ns + ' ' + L.san + '</small>' + L.sa + '</a></div>';
    h += '<p><button type="button" class="app-wipe" id="app-wipe">' + L.wipe + '</button></p>';
    mine.innerHTML = h;
    var wb = $('app-wipe'), armed = false;
    wb.addEventListener('click', function () {
      if (!armed) { armed = true; wb.textContent = L.wipe2; wb.classList.add('armed'); return; }
      siteKeys().forEach(function (k) { try { localStorage.removeItem(k); } catch (e) {} });
      try { localStorage.removeItem(KEY); sessionStorage.clear(); } catch (e) {}
      location.reload();
    });
  }

  // ---------- Dấu ✓ cạnh link tới bài đã xong (ngoài thẻ bài và bản đồ khóa, nơi site đã tự đánh dấu) ----------
  if (main) [].forEach.call(main.querySelectorAll('a[href]'), function (x) {
    if (x.closest('.app-home,.app-list,.app-crumb,.app-progress,.lesson-card,.coursemap,.course-strip,.pager,.app-course')) return;
    var p = x.pathname.replace(/index\.html$/, '');
    if (!/\/(bai-hoc|lessons)\/[^\/]+\/$/.test(p) || p === path) return;
    if (isDone(slugOf(p))) x.insertAdjacentHTML('beforeend', ' <span class="app-tick" aria-label="✓">✓</span>');
  });
})();
