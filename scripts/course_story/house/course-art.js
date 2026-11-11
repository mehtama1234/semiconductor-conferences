// Drawings for the course sites, made with the same helpers and classes as art.js (cream cards with a rust
// top edge, dotted rust lines, Tabler line icons). Everything drawn comes from window.CourseData, which the
// build writes from the course's own analysis files. Adds pictures to HelperJobsArt without changing it.
(function (root) {
  const icons = root.HelperJobsIcons, D = root.CourseData || {};
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const glyph = (name, x, y, size, cls = 'sp-glyph') => {
    const body = icons.icon(name).replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '');
    return `<g class="${cls}" transform="translate(${x} ${y}) scale(${size / 24})">${body}</g>`;
  };
  const card = (x, y, w, h, rot, inner, top = true) => `<g transform="translate(${x} ${y}) rotate(${rot})"><rect class="sp-card" width="${w}" height="${h}" rx="3"/>${top ? `<rect class="sp-top" width="${w}" height="5"/>` : ''}${inner}</g>`;
  const line = d => `<path class="sp-line" d="${d}"/>`;
  const svg = (label, body, w = 320, h = 220) => `<svg class="spot-art" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(label)}">${body}</svg>`;
  // Break a phrase into lines of at most `max` characters, so card text never runs past the card edge.
  const wrap = (text, max) => {
    const out = []; let cur = '';
    String(text || '').split(/\s+/).filter(Boolean).forEach(w => { if (cur && (cur + ' ' + w).length > max) { out.push(cur); cur = w; } else cur = cur ? cur + ' ' + w : w; });
    if (cur) out.push(cur);
    return out;
  };
  const lines = (arr, x, y, cls, gap) => arr.map((t, i) => `<text class="${cls}" x="${x}" y="${y + i * gap}">${esc(t)}</text>`).join('');

  // A step card: number, icon, title and up to three short lines.
  const stepCard = (i, s, x, y, w, h, rot) => {
    const [ic, title, a, b] = s;
    const tl = wrap(title, Math.floor((w - 28) / 9.6)).slice(0, 2);
    const body = wrap([a, b].filter(Boolean).join(' '), Math.floor((w - 28) / 5.9)).slice(0, 3);
    const ty = h - 22 - body.length * 15 - (tl.length - 1) * 20;
    return card(x, y, w, h, rot, `<circle class="sp-face-soft" cx="22" cy="28" r="12"/><text class="sp-num" x="22" y="32" text-anchor="middle">${i + 1}</text>${glyph(ic, w - 44, 14, 28)}${lines(tl, 14, ty, 'sp-title', 20)}${lines(body, 14, ty + (tl.length - 1) * 20 + 20, 'sp-small', 15)}`);
  };

  // Steps in a row (wide screens) or a column (phones), joined by dotted arrows; optional loop back.
  function steps(list, label, tall, loop) {
    const n = list.length;
    if (!tall) {
      const cw = Math.min(176, Math.floor((970 - 30 - (n - 1) * 30) / n)), gap = 30, ch = 156;
      let b = '';
      list.forEach((s, i) => { b += stepCard(i, s, 14 + i * (cw + gap), 26 + (i % 2) * 10, cw, ch, i % 2 ? 2 : -2); });
      for (let i = 0; i < n - 1; i++) { const x = 14 + (i + 1) * (cw + gap) - gap + 2; b += line(`M${x} 104 L${x + gap - 8} 104`) + `<path class="sp-arrow" d="M${x + gap - 12} 98l7 6-7 6"/>`; }
      const W = 28 + n * cw + (n - 1) * gap;
      if (loop) b += line(`M${W - 80} 198 C ${W - 80} 262, ${W - 200} 270, ${W / 2} 270 C 200 270, 94 262, 94 198`) + `<path class="sp-arrow" d="M88 206l6-9 6 9"/><text class="sp-return" x="${W / 2}" y="292" text-anchor="middle">${esc(loop)}</text>`;
      return svg(label, b, W, loop ? 300 : 210);
    }
    let b = '';
    list.forEach((s, i) => { b += stepCard(i, s, 14 + (i % 2) * 16, 12 + i * 132, 250, 108, i % 2 ? 1.5 : -1.5); });
    for (let i = 0; i < n - 1; i++) { const y = 122 + i * 132; b += line(`M140 ${y} L140 ${y + 18}`) + `<path class="sp-arrow" d="M134 ${y + 14}l6 7 6-7"/>`; }
    const H = 30 + n * 132;
    if (loop) b += line(`M282 ${H - 72} C 306 ${H - 110}, 306 110, 282 66`) + `<path class="sp-arrow" d="M290 74l-8-8 -1 11"/>`;
    return svg(label, b, 344, H);
  }

  // How the core ideas lean on each other: cards placed by the build, arrows from "learn first" to "then".
  function network(net) {
    if (!net || !net.nodes) return '';
    const pos = {}; net.nodes.forEach(nd => { pos[nd.id] = nd; });
    const W = net.w, H = net.h, cw = net.cw || 150, ch = 46;
    let b = '';
    (net.edges || []).forEach(([a, z]) => {
      const p = pos[a], q = pos[z]; if (!p || !q) return;
      const x1 = p.x + cw / 2, y1 = p.y + ch, x2 = q.x + cw / 2, y2 = q.y;
      const my = (y1 + y2) / 2;
      b += line(`M${x1} ${y1} C ${x1} ${my}, ${x2} ${my}, ${x2} ${y2 - 6}`) + `<path class="sp-arrow" d="M${x2 - 5} ${y2 - 11}l5 6 5-6"/>`;
    });
    net.nodes.forEach(nd => {
      const tl = wrap(nd.label, Math.floor((cw - 16) / 6.4)).slice(0, 2);
      const inner = `<rect class="sp-card" width="${cw}" height="${ch}" rx="3"/><rect class="sp-top" width="${cw}" height="4"/>` + tl.map((t, i) => `<text class="sp-small net-label" x="${cw / 2}" y="${(tl.length === 1 ? 29 : 21) + i * 14}" text-anchor="middle">${esc(t)}</text>`).join('');
      b += nd.href ? `<a href="${esc(nd.href)}"><g transform="translate(${nd.x} ${nd.y})">${inner}</g></a>` : `<g transform="translate(${nd.x} ${nd.y})">${inner}</g>`;
    });
    if (net.rows) net.rows.forEach(r => { b += `<text class="sp-return" x="4" y="${r.y + 28}">${esc(r.label)}</text>`; });
    return svg(net.caption || 'How the core ideas connect.', b, W, H);
  }

  // Three tilted cards with icons: a small header picture for any page.
  const trio = (label, ics) => svg(label, `
      ${card(14, 30, 92, 124, -3, `${glyph(ics[0], 28, 22, 36)}<rect class="sp-bar" x="14" y="74" width="62" height="7"/><rect class="sp-bar-soft" x="14" y="88" width="48" height="6"/>`)}
      ${card(114, 22, 92, 124, 2, `<circle class="sp-medal" cx="46" cy="40" r="24"/>${glyph(ics[1], 30, 24, 32, 'sp-glyph-light')}<rect class="sp-bar" x="14" y="80" width="56" height="7"/><rect class="sp-bar-soft" x="14" y="94" width="62" height="6"/>`)}
      ${card(214, 34, 92, 124, -2, `${glyph(ics[2], 28, 22, 36)}<rect class="sp-bar" x="14" y="74" width="60" height="7"/><rect class="sp-bar-soft" x="14" y="88" width="44" height="6"/>`)}
      ${line('M60 172 C 110 198, 210 198, 262 174')}`);

  function draw(name) {
    if (name === 'path') return steps(D.path || [], D.pathLabel || 'The course path.', false, '');
    if (name === 'pathTall') return steps(D.path || [], D.pathLabel || 'The course path.', true, '');
    if (name === 'network') return network(D.network);
    if (name.startsWith('flow:') || name.startsWith('flowTall:')) {
      const tall = name.startsWith('flowTall:'), f = (D.flows || {})[name.split(':')[1]];
      return f ? steps(f.steps, f.label, tall, f.loop || '') : '';
    }
    if (name.startsWith('trio:')) { const p = name.slice(5).split(','); return trio(p[3] || 'Three cards.', p); }
    if (name.startsWith('sketch:')) { const s = (D.sketches || {})[name.slice(7)]; return s ? svg(s.label, s.body, s.w, s.h) : ''; }
    return '';
  }
  const base = root.HelperJobsArt;
  root.HelperJobsArt = { draw: name => draw(name) || base.draw(name), names: base.names };
})(window);
