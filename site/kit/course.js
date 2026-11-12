/* Course kit · course.js. No dependencies, no network, no URL-hash routing (plain anchors only).
   1. Theme button: cycles the page between the reader's system setting, light and dark.
   2. Slide frames: scales each 1920 x 1080 slide to its stage.
   3. Argument rail and the sticky ideas bar: mark the idea now on screen. */
(function () {
  'use strict';
  var root = document.documentElement, KEY = 'course-kit-theme';
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function apply(t) {
    if (t === 'light' || t === 'dark') root.setAttribute('data-theme', t); else root.removeAttribute('data-theme');
    [].forEach.call(document.querySelectorAll('.ck-theme'), function (b) {
      b.textContent = 'Theme: ' + (t === 'light' ? 'light' : t === 'dark' ? 'dark' : 'auto');
    });
  }
  apply(stored());
  function ready() {
    apply(stored());
    [].forEach.call(document.querySelectorAll('.ck-theme'), function (b) {
      b.addEventListener('click', function () {
        var cur = root.getAttribute('data-theme'), next = cur === 'light' ? 'dark' : cur === 'dark' ? null : 'light';
        try { if (next) localStorage.setItem(KEY, next); else localStorage.removeItem(KEY); } catch (e) {}
        apply(next);
      });
    });
    var stages = [].slice.call(document.querySelectorAll('.ck-stage'));
    function fit() { stages.forEach(function (s) { s.style.setProperty('--s', (s.clientWidth / 1920).toFixed(4)); }); }
    if (stages.length) { fit(); window.addEventListener('resize', fit); if (window.ResizeObserver) stages.forEach(function (s) { new ResizeObserver(fit).observe(s); }); }
    var links = [].slice.call(document.querySelectorAll('.ck-rail a[href^="#"], .ck-jump a[href^="#"]'));
    if (links.length && window.IntersectionObserver) {
      var byId = {}, seen = {}, last = null;
      links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { seen[e.target.id] = e.isIntersecting; });
        var on = null;
        links.forEach(function (a) { var id = a.getAttribute('href').slice(1); if (seen[id] && !on) on = id; });
        if (!on) on = last; last = on;
        links.forEach(function (a) {
          if (a.getAttribute('href').slice(1) === on) {
            a.setAttribute('aria-current', 'true');
            var bar = a.closest('.ck-jump ol'); if (bar && bar.scrollTo) bar.scrollTo({ left: Math.max(0, a.offsetLeft - bar.offsetLeft - 8), behavior: 'auto' });
          } else a.removeAttribute('aria-current');
        });
      }, { rootMargin: '-10% 0px -55% 0px' });
      Object.keys(byId).forEach(function (id) { var t = document.getElementById(id); if (t) io.observe(t); });
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready); else ready();
})();
