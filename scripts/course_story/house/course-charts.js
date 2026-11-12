// Extra chart shapes for the course sites, in the same look as charts.js (sand for comparison, rust for the
// thing being shown, espresso for a third tone; every bar carries its own number). Adds to PortfolioCharts.
(function (root) {
  const C = root.PortfolioCharts;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const table = (caption, head, rows) => `<div class="sr-only"><table><caption>${esc(caption)}</caption><tr>${head.map(h => `<th>${esc(h)}</th>`).join('')}</tr>${rows.map(r => `<tr>${r.map(c => `<td>${esc(c)}</td>`).join('')}</tr>`).join('')}</table></div>`;
  const frame = (w, h, body, labelText) => `<svg class="chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(labelText)}">${body}</svg>`;
  function hBars({ items, caption, format = v => String(v), labelW = 200, unit = '' }) {
    const w = 640, rowH = 40, top = 10, right = 70, h = top + items.length * rowH + 10;
    const lo = Math.min(0, ...items.map(i => i.value)), hi = Math.max(0, ...items.map(i => i.value));
    const span = hi - lo || 1, plotL = labelW, plotW = w - labelW - right - (lo < 0 ? 60 : 0);
    const x = v => plotL + (lo < 0 ? 60 : 0) + ((v - lo) / span) * plotW;
    let body = `<line class="axis" x1="${x(0)}" x2="${x(0)}" y1="${top - 4}" y2="${h - 6}"/>`;
    items.forEach((it, i) => {
      const cy = top + i * rowH + rowH / 2, x0 = Math.min(x(0), x(it.value)), bw = Math.max(2, Math.abs(x(it.value) - x(0)));
      const neg = it.value < 0, tx = neg ? x0 - 8 : x0 + bw + 8;
      body += `<text class="cat-l" x="0" y="${cy + 5}">${esc(it.label)}</text><rect class="bar ${it.tone || 's1'}" x="${x0}" y="${cy - 12}" width="${bw}" height="24" rx="3"/><text class="val strong" x="${tx}" y="${cy + 5}" text-anchor="${neg ? 'end' : 'start'}">${esc(format(it.value))}${esc(unit)}</text>`;
    });
    return frame(w, h, body, caption) + table(caption, ['', 'Value'], items.map(it => [it.label, format(it.value) + unit]));
  }
  function heatGrid({ rows, cols, values, caption, labelW = 170 }) {
    const w = 640, cellH = 38, top = 30, h = top + rows.length * cellH + 8, cw = (w - labelW) / cols.length;
    const max = Math.max(1, ...values.flat());
    let body = cols.map((c, ci) => `<text class="tick" x="${labelW + ci * cw + cw / 2}" y="18" text-anchor="middle">${esc(c)}</text>`).join('');
    rows.forEach((r, ri) => {
      const y = top + ri * cellH;
      body += `<text class="cat-l" x="0" y="${y + cellH / 2 + 5}">${esc(r)}</text>`;
      values[ri].forEach((v, ci) => {
        const op = v ? 0.15 + 0.85 * (v / max) : 0;
        body += `<rect class="cell" x="${labelW + ci * cw + 3}" y="${y + 3}" width="${cw - 6}" height="${cellH - 6}" rx="4"/>${v ? `<rect class="bar s1" x="${labelW + ci * cw + 3}" y="${y + 3}" width="${cw - 6}" height="${cellH - 6}" rx="4" fill-opacity="${op.toFixed(2)}"/>` : ''}<text class="val${v / max > 0.5 ? ' light' : ' strong'}" x="${labelW + ci * cw + cw / 2}" y="${y + cellH / 2 + 5}" text-anchor="middle">${v || ''}</text>`;
      });
    });
    return frame(w, h, body, caption) + table(caption, ['', ...cols], rows.map((r, ri) => [r, ...values[ri].map(String)]));
  }
  Object.assign(C, { hBars, heatGrid });
})(window);
