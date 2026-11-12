/* Course site on the board kit: step-through drawings, switches between cases, and the ideas jump bar. No dependencies. */
(function () {
  'use strict';
  function each(sel, fn, root) { [].forEach.call((root || document).querySelectorAll(sel), fn); }
  function ready() {
    each('.ck-stepper', function (box) {
      var frames = [].slice.call(box.querySelectorAll('.ck-frame')), i = 0;
      var out = box.querySelector('output'), label = box.getAttribute('data-label') || 'Step';
      var btns = [].slice.call(box.querySelectorAll('.ck-sbtn')), tabs = [].slice.call(box.querySelectorAll('.ck-lens button'));
      box.classList.add('js');
      function show(k) {
        i = Math.max(0, Math.min(frames.length - 1, k));
        frames.forEach(function (f, j) { f.hidden = j !== i; });
        if (out) out.textContent = label + ' ' + (i + 1) + ' of ' + frames.length;
        btns.forEach(function (b) { var d = +b.getAttribute('data-go'); b.disabled = (d < 0 && i === 0); if (d > 0) b.textContent = i === frames.length - 1 ? 'Start again' : 'Next step'; });
        tabs.forEach(function (t, j) { t.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
      }
      btns.forEach(function (b) { b.addEventListener('click', function () { var d = +b.getAttribute('data-go'); show(d > 0 && i === frames.length - 1 ? 0 : i + d); }); });
      tabs.forEach(function (t, j) { t.addEventListener('click', function () { show(j); }); });
      show(0);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready); else ready();
})();
