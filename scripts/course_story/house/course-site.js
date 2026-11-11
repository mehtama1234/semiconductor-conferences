// Fills in icons, drawings and charts on every course page from window.CourseData (written at build time).
(function () {
  const D = window.CourseData || {}, C = window.PortfolioCharts;
  document.querySelectorAll('[data-icon]').forEach(el => { el.innerHTML = window.HelperJobsIcons.icon(el.dataset.icon); });
  document.querySelectorAll('[data-art]').forEach(el => { el.innerHTML = window.HelperJobsArt.draw(el.dataset.art); });
  const formats = { n: v => Number(v).toLocaleString('en-US'), pct: v => `${v}%`, h: v => `${v} h`, min: v => `${v} min` };
  document.querySelectorAll('[data-chart]').forEach(el => {
    const spec = (D.charts || {})[el.dataset.chart];
    if (!spec || !C[spec.type]) return;
    el.innerHTML = C[spec.type](Object.assign({}, spec, { format: formats[spec.format] || formats.n }));
  });
})();
