/* Course kit · charts.js
   Small SVG builders in the boards' style. No dependencies, no network.
   Use:  <figure data-chart><script type="application/json">{"type":"line", ...}</script></figure>
   or:   KitCharts.mount(element, spec)
   Every chart is drawn at the real pixel width of its box (and redrawn when the box changes),
   so text is never scaled below its set size. Colours come from the tokens through CSS classes.
   Series differ by line style as well as colour: 1 solid ink, 2 dashed rust, 3 dotted taupe. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  function S(tag, a, parent, text) {
    var e = document.createElementNS(NS, tag);
    for (var k in a) if (a[k] != null) e.setAttribute(k, a[k]);
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function H(tag, a, parent, text) {
    var e = document.createElement(tag);
    for (var k in a) if (a[k] != null) e.setAttribute(k, a[k]);
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function lin(d0, d1, r0, r1) { return function (x) { return r0 + (x - d0) * (r1 - r0) / (d1 - d0 || 1); }; }
  function fmt(v, d) {
    if (typeof v !== 'number') return String(v);
    if (d == null) d = Math.abs(v) >= 100 ? 0 : Math.abs(v) >= 10 ? 1 : 2;
    var s = v.toFixed(d);
    if (s.indexOf('.') >= 0) s = s.replace(/0+$/, '').replace(/\.$/, '');
    if (s === '-0') s = '0';
    return s.replace('-', '−');
  }
  function niceTicks(min, max, n) {
    var span = max - min, raw = span / (n || 5), p = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p;
    var step = (m < 1.5 ? 1 : m < 3 ? 2 : m < 7 ? 5 : 10) * p, out = [];
    for (var v = Math.ceil(min / step - 1e-9) * step; v <= max + step * 1e-6; v += step) out.push(Math.abs(v) < step * 1e-6 ? 0 : +v.toFixed(10));
    return out;
  }
  function wrap(text, maxChars) {
    var words = String(text).split(/\s+/), lines = [], cur = '';
    words.forEach(function (w) {
      if (cur && (cur + ' ' + w).length > maxChars) { lines.push(cur); cur = w; } else cur = cur ? cur + ' ' + w : w;
    });
    if (cur) lines.push(cur);
    return lines;
  }
  function textLines(g, lines, x, y, lh, a) {
    var t = S('text', Object.assign({ x: x, y: y }, a), g);
    lines.forEach(function (l, i) { S('tspan', { x: x, dy: i ? lh : 0 }, t, l); });
    return t;
  }
  var STY = [['s-ink', ''], ['s-rust', 'dashed'], ['s-soft', 'dotted']];
  function styleOf(s, i) {
    var col = s.color ? 's-' + s.color : STY[i % 3][0];
    var dash = s.style ? (s.style === 'solid' ? '' : s.style) : STY[i % 3][1];
    return 's ' + col + (dash ? ' ' + dash : '') + (s.thin ? ' thin' : '');
  }
  function pathOf(pts, X, Y, step) {
    var d = '';
    pts.forEach(function (p, i) {
      if (!i) d += 'M' + X(p[0]).toFixed(1) + ' ' + Y(p[1]).toFixed(1);
      else if (step) d += 'H' + X(p[0]).toFixed(1) + 'V' + Y(p[1]).toFixed(1);
      else d += 'L' + X(p[0]).toFixed(1) + ' ' + Y(p[1]).toFixed(1);
    });
    return d;
  }
  function arrowHead(g, x, y, ang, cls, size) {
    size = size || 9;
    var a1 = ang + Math.PI - 0.42, a2 = ang + Math.PI + 0.42;
    S('path', { d: 'M' + x.toFixed(1) + ' ' + y.toFixed(1) + 'L' + (x + size * Math.cos(a1)).toFixed(1) + ' ' + (y + size * Math.sin(a1)).toFixed(1) + 'L' + (x + size * Math.cos(a2)).toFixed(1) + ' ' + (y + size * Math.sin(a2)).toFixed(1) + 'Z', class: 'f-' + ((cls.match(/\bs-(\w+)/) || [0, 'ink'])[1]) }, g);
  }
  function arrowLine(g, pts, cls) {
    var d = pts.map(function (p, i) { return (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join('');
    S('path', { d: d, class: cls }, g);
    var n = pts.length, a = pts[n - 2], b = pts[n - 1];
    arrowHead(g, b[0], b[1], Math.atan2(b[1] - a[1], b[0] - a[0]), cls);
  }
  function polyVal(c, x) { var y = 0; for (var i = c.length - 1; i >= 0; i--) y = y * x + c[i]; return y; }
  function sample(s, xmin, xmax) {
    if (s.points) return s.points;
    var pts = [], n = 80;
    for (var i = 0; i <= n; i++) { var x = xmin + (xmax - xmin) * i / n; pts.push([x, polyVal(s.poly, x)]); }
    return pts;
  }
  function valueAt(s, pts, x) {
    if (s.poly) return polyVal(s.poly, x);
    if (x <= pts[0][0]) return pts[0][1];
    for (var i = 1; i < pts.length; i++) if (x <= pts[i][0] + 1e-9) {
      if (s.step) return x >= pts[i][0] - 1e-9 ? pts[i][1] : pts[i - 1][1];
      var t = (x - pts[i - 1][0]) / (pts[i][0] - pts[i - 1][0] || 1);
      return pts[i - 1][1] + t * (pts[i][1] - pts[i - 1][1]);
    }
    return pts[pts.length - 1][1];
  }
  /* axes for an x/y plot; returns scales */
  function frame(svg, W, Hh, spec, opt) {
    opt = opt || {};
    var x = spec.x || {}, y = spec.y || {};
    var m = { l: 46, r: opt.right || 16, t: y.label ? 30 : 14, b: x.label ? 46 : 28 };
    if (opt.equal) {
      var uw = (W - m.l - m.r) / (x.max - x.min);
      Hh = Math.round(uw * (y.max - y.min) + m.t + m.b);
      var capH = maxPlotH(W);
      if (Hh > capH) { var uw2 = (capH - m.t - m.b) / (y.max - y.min), ex = (W - m.l - m.r) - uw2 * (x.max - x.min); m.l += ex / 2; m.r += ex / 2; Hh = capH; }
    }
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + Hh);
    var X = lin(x.min, x.max, m.l, W - m.r), Y = lin(y.min, y.max, Hh - m.b, m.t);
    var g = S('g', {}, svg);
    var maxN = Math.max(2, Math.floor((W - m.l - m.r) / 64));
    var xt = x.ticks || niceTicks(x.min, x.max, Math.min(x.n || 6, maxN)), yt = y.ticks || niceTicks(y.min, y.max, y.n || 5);
    yt.forEach(function (v) {
      S('path', { d: 'M' + m.l + ' ' + Y(v).toFixed(1) + 'H' + (W - m.r), class: v === 0 && y.min < 0 ? 'ax' : 'gr' }, g);
      S('text', { x: m.l - 8, y: Y(v) + 5, 'text-anchor': 'end' }, g, fmt(v) + (y.unit || ''));
    });
    var y0 = y.min < 0 && y.max > 0 && opt.zeroAxis !== false ? Y(0) : Hh - m.b;
    S('path', { d: 'M' + m.l + ' ' + (Hh - m.b) + 'H' + (W - m.r), class: 'ax' }, g);
    xt.forEach(function (v) {
      S('path', { d: 'M' + X(v).toFixed(1) + ' ' + (Hh - m.b) + 'v5', class: 'ax' }, g);
      S('text', { x: X(v), y: Hh - m.b + 20, 'text-anchor': 'middle' }, g, (x.tickLabels && x.tickLabels[v] != null ? x.tickLabels[v] : fmt(v)) + (x.unit || ''));
    });
    if (x.min < 0 && x.max > 0 && opt.zeroAxis !== false) S('path', { d: 'M' + X(0).toFixed(1) + ' ' + m.t + 'V' + (Hh - m.b), class: 'ax' }, g);
    if (x.label) S('text', { x: (m.l + W - m.r) / 2, y: Hh - 6, 'text-anchor': 'middle', class: 'ti' }, g, x.label);
    if (y.label) S('text', { x: 4, y: 14, class: 'ti' }, g, y.label);
    return { X: X, Y: Y, m: m, H: Hh, y0: y0 };
  }
  /* Height limit for plots that keep equal axes: about one phone screen on a phone, 560 elsewhere. */
  function maxPlotH(W) { return W < 520 ? Math.round(Math.min(W * 1.05, 400)) : 560; }

  /* Label collision avoidance. Free labels carry the class "halo". After a chart is in the page each one is tested
     against the labels placed before it, the marked points and the drawn lines (sampled every 7 px). If it sits on
     any of them it is moved to the nearest clear spot among: above, below, further above, further below, flipped to
     the other side, and it is kept inside the plot. Authors' dx and dy still apply: they set the first position tried. */
  function declutter(svg) {
    var labs = [].slice.call(svg.querySelectorAll('text.halo'));
    if (!labs.length || !svg.getBBox) return 0;
    var vb = svg.viewBox.baseVal, obs = [], placed = [], moved = 0;
    [].forEach.call(svg.querySelectorAll('circle'), function (c) { var b = c.getBBox(); if (b.width < 40) obs.push([b.x + b.width / 2, b.y + b.height / 2, b.width / 2 + 2]); });
    [].forEach.call(svg.querySelectorAll('path.s, polyline.s, line.s'), function (p) {
      var L; try { L = p.getTotalLength(); } catch (e) { return; }
      if (!L || L > 6000) return;
      for (var d = 0; d <= L; d += 7) { var q = p.getPointAtLength(d); obs.push([q.x, q.y, 2]); }
    });
    function hits(b) {
      var n = 0, i, o;
      for (i = 0; i < placed.length; i++) { o = placed[i]; if (b.x < o.x + o.width + 3 && b.x + b.width + 3 > o.x && b.y < o.y + o.height + 1 && b.y + b.height + 1 > o.y) n += 40; }
      for (i = 0; i < obs.length; i++) { o = obs[i]; if (o[0] > b.x - o[2] && o[0] < b.x + b.width + o[2] && o[1] > b.y - o[2] + 2 && o[1] < b.y + b.height + o[2] - 2) n++; }
      if (b.x < 0) n += 30 + -b.x; if (b.x + b.width > vb.width) n += 30 + b.x + b.width - vb.width;
      if (b.y < 0) n += 30; if (b.y + b.height > vb.height) n += 30;
      return n;
    }
    labs.forEach(function (t) {
      var b0; try { b0 = t.getBBox(); } catch (e) { return; }
      if (!b0.width) return;
      var h = b0.height, w = b0.width, best = [0, 0, hits(b0)];
      if (best[2] > 0) {
        var c = [[0, -h * 0.7], [0, h * 0.8], [0, -h * 1.5], [0, h * 1.6], [-(w + 22), 0], [w + 22, 0], [-(w / 2 + 11), -h], [w / 2 + 11, -h], [-(w / 2 + 11), h], [w / 2 + 11, h], [0, -h * 2.4], [0, h * 2.5]];
        for (var i = 0; i < c.length && best[2] > 0; i++) {
          var s = hits({ x: b0.x + c[i][0], y: b0.y + c[i][1], width: w, height: h }) + i * 0.2;
          if (s < best[2]) best = [c[i][0], c[i][1], s];
        }
        if (best[0] || best[1]) {
          moved++;
          t.setAttribute('x', (+t.getAttribute('x') + best[0]).toFixed(1)); t.setAttribute('y', (+t.getAttribute('y') + best[1]).toFixed(1));
          [].forEach.call(t.querySelectorAll('tspan[x]'), function (ts) { ts.setAttribute('x', (+ts.getAttribute('x') + best[0]).toFixed(1)); });
          t.setAttribute('data-moved', '1');
        }
      }
      placed.push({ x: b0.x + best[0], y: b0.y + best[1], width: w, height: h });
    });
    return moved;
  }
  function label(g, x, y, text, cls, anchor) {
    return S('text', { x: x, y: y, class: (cls || 'ti') + ' halo', 'text-anchor': anchor || 'start' }, g, text);
  }

  var B = {};

  /* ---- line / fn / steps: an x-y plot with an optional slider cursor or marked point ---- */
  function xy(spec, W, st, mode) {
    var svg = S('svg', { class: 'cx' });
    var Hh = Math.round(Math.max(210, Math.min(W * (spec.ratio || 0.6), 420)));
    var needRight = (spec.series || []).some(function (s) { return s.endLabel; }) ? Math.min(110, W * 0.22) : 16;
    if (spec.y && spec.y.label) Hh += 16;
    var f = frame(svg, W, Hh, spec, { right: needRight }), X = f.X, Y = f.Y;
    (spec.bands || []).forEach(function (b) {
      S('rect', { x: X(b.x0), y: f.m.t, width: X(b.x1) - X(b.x0), height: f.H - f.m.b - f.m.t, class: 'f-soft' }, svg);
      if (b.label) S('text', { x: (X(b.x0) + X(b.x1)) / 2, y: f.H - f.m.b - 10, 'text-anchor': 'middle', class: 'tr' }, svg, b.label);
    });
    var reads = [], legend = [], v = st.v;
    var series = (spec.series || []).map(function (s, i) {
      var pts = sample(s, spec.x.min, spec.x.max);
      S('path', { d: pathOf(pts, X, Y, s.step), class: styleOf(s, i) }, svg);
      if (s.dots) pts.forEach(function (p) { S('circle', { cx: X(p[0]), cy: Y(p[1]), r: 3.5, class: 'f-' + (s.color || (i % 3 === 1 ? 'rust' : 'ink')) }, svg); });
      if (s.endLabel) { var e = pts[pts.length - 1]; S('text', { x: X(e[0]) + 8, y: Y(e[1]) + 5, class: 'ti halo' }, svg, s.endLabel); }
      if (s.name) legend.push({ name: s.name, cls: styleOf(s, i) });
      return { s: s, pts: pts, i: i };
    });
    (spec.hlines || []).forEach(function (hl) {
      S('path', { d: 'M' + f.m.l + ' ' + Y(hl.y).toFixed(1) + 'H' + (W - f.m.r), class: 's thin dashed s-' + (hl.color || 'soft') }, svg);
      if (hl.label) label(svg, W - f.m.r - 4, Y(hl.y) - 6, hl.label, hl.cls || '', 'end');
    });
    (spec.points || []).forEach(function (p) {
      S('circle', { cx: X(p.x), cy: Y(p.y), r: p.r || 5.5, class: p.hollow ? 'f-paper s thin s-ink' : 'f-' + (p.color || 'ink') }, svg);
      if (p.label) {
        var an = p.anchor || (X(p.x) > W * 0.7 ? 'end' : 'start');
        var ls = wrap(p.label, p.wrap || 22), t = textLines(svg, ls, X(p.x) + (an === 'end' ? -10 : 10) + (p.dx || 0), Y(p.y) + (p.dy != null ? p.dy : -10), 16, { class: (p.cls || 'ti') + ' halo', 'text-anchor': an });
      }
    });
    if (v != null && spec.slider) {
      if (mode === 'fn') {
        var k = spec.marker && spec.marker.curve || 0, cs = series[k], yv = valueAt(cs.s, cs.pts, v);
        if (spec.marker && spec.marker.tangent && cs.s.poly) {
          var der = cs.s.poly.map(function (c, i) { return c * i; }).slice(1), sl = polyVal(der, v);
          var half = (spec.x.max - spec.x.min) * 0.16, xa = v - half, xb = v + half;
          var clip = function (xx) { return Math.max(spec.x.min, Math.min(spec.x.max, xx)); };
          xa = clip(xa); xb = clip(xb);
          S('path', { d: 'M' + X(xa).toFixed(1) + ' ' + Y(yv + sl * (xa - v)).toFixed(1) + 'L' + X(xb).toFixed(1) + ' ' + Y(yv + sl * (xb - v)).toFixed(1), class: 's s-rust thin' }, svg);
          reads.push({ label: spec.marker.slopeLabel || 'slope here', value: fmt(sl, 2), on: Math.abs(sl) < 1e-9 });
        }
        if (spec.marker && spec.marker.drop !== false) S('path', { d: 'M' + X(v).toFixed(1) + ' ' + Y(yv).toFixed(1) + 'V' + (f.H - f.m.b), class: 'cur' }, svg);
        S('circle', { cx: X(v), cy: Y(yv), r: 7, class: 'f-rust halo' }, svg);
        reads.unshift({ label: (spec.marker && spec.marker.valueLabel) || cs.s.name || 'value', value: fmt(yv, spec.slider.valueDecimals), unit: spec.y.unit });
        ((spec.marker && spec.marker.extras) || []).forEach(function (e) { reads.push({ label: e.label, value: fmt(polyVal(e.poly, v), e.decimals), unit: e.unit }); });
      } else {
        S('path', { d: 'M' + X(v).toFixed(1) + ' ' + f.m.t + 'V' + (f.H - f.m.b), class: 'cur' }, svg);
        series.forEach(function (c) {
          if (c.s.read === false) return;
          var yv = valueAt(c.s, c.pts, v);
          S('circle', { cx: X(v), cy: Y(yv), r: 6, class: 'halo f-' + (c.s.color || (c.i % 3 === 1 ? 'rust' : c.i % 3 === 2 ? 'mute' : 'ink')) }, svg);
          reads.push({ label: c.s.name, value: fmt(yv, c.s.decimals), unit: c.s.unit });
        });
      }
    }
    return { svg: svg, reads: reads, legend: legend.length > 1 ? legend : [] };
  }
  B.line = function (spec, W, st) { return xy(spec, W, st, 'line'); };
  B.fn = function (spec, W, st) { return xy(spec, W, st, 'fn'); };
  B.steps = function (spec, W, st) {
    spec.series.forEach(function (s) { if (s.step == null) s.step = true; });
    return xy(spec, W, st, 'line');
  };

  /* ---- bars: horizontal, labels wrapped, value at the bar end ---- */
  B.bars = function (spec, W) {
    var svg = S('svg', { class: 'cx' });
    var items = spec.items, labW = Math.min(Math.round(W * 0.38), 210), valW = 86, rowH = 0, y = 8;
    var max = spec.max || Math.max.apply(null, items.map(function (d) { return d.value; }));
    var X = lin(0, max, labW + 10, W - valW);
    items.forEach(function (d) {
      var ls = wrap(d.label, Math.max(8, Math.floor(labW / 6.3))), h = Math.max(30, ls.length * 17 + 8);
      textLines(svg, ls, labW, y + h / 2 - (ls.length - 1) * 8.5 + 5, 17, { 'text-anchor': 'end', class: 'ti' });
      var bw = Math.max(d.value > 0 ? 2 : 0, X(d.value) - X(0));
      S('rect', { x: X(0), y: y + (h - 24) / 2, width: W - valW - X(0), height: 24, class: 'f-sand' }, svg);
      S('rect', { x: X(0), y: y + (h - 24) / 2, width: bw, height: 24, class: d.em ? 'f-rust' : 'f-mute' }, svg);
      S('text', { x: X(d.value) + 8, y: y + h / 2 + 5, class: 'tb' }, svg, d.display != null ? d.display : fmt(d.value) + (spec.unit || ''));
      y += h + 8;
    });
    S('path', { d: 'M' + X(0) + ' 4V' + (y - 4), class: 'ax' }, svg);
    if (spec.axisLabel) { S('text', { x: X(0), y: y + 14, class: '' }, svg, spec.axisLabel); y += 20; }
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + y);
    return { svg: svg };
  };

  /* ---- dots: a dot-matrix table. cell: 1 filled, 0 empty, "on" rust, "part" half, "miss" dashed ---- */
  B.dots = function (spec, W) {
    var svg = S('svg', { class: 'cx' });
    var labW = Math.min(Math.round(W * 0.42), 250), cols = spec.cols, cw = (W - labW - 8) / cols.length;
    var headLines = cols.map(function (c) { return wrap(c, Math.max(6, Math.floor(cw / 7))); });
    var hh = Math.max.apply(null, headLines.map(function (l) { return l.length; })) * 16 + 12, y = hh;
    cols.forEach(function (c, i) { textLines(svg, headLines[i], labW + cw * (i + 0.5), 14, 16, { 'text-anchor': 'middle', class: 'tb' }); });
    var r = Math.min(11, cw / 2 - 6);
    spec.rows.forEach(function (row) {
      var ls = wrap(row.label, Math.max(8, Math.floor(labW / 6.3))), h = Math.max(34, ls.length * 17 + 10);
      S('path', { d: 'M0 ' + y + 'H' + W, class: 'gr' }, svg);
      textLines(svg, ls, 0, y + h / 2 - (ls.length - 1) * 8.5 + 5, 17, { class: row.em ? 'tb' : 'ti' });
      row.cells.forEach(function (c, i) {
        var cx = labW + cw * (i + 0.5), cy = y + h / 2;
        if (c === 'part') { S('circle', { cx: cx, cy: cy, r: r, class: 'f-paper s thin s-ink' }, svg); S('path', { d: 'M' + cx + ' ' + (cy - r) + 'A' + r + ' ' + r + ' 0 0 0 ' + cx + ' ' + (cy + r) + 'Z', class: 'f-ink' }, svg); }
        else if (c === 'miss') S('circle', { cx: cx, cy: cy, r: r, class: 'f-none s thin s-hold dashed' }, svg);
        else if (c === 'on') S('circle', { cx: cx, cy: cy, r: r, class: 'f-rust' }, svg);
        else if (c) S('circle', { cx: cx, cy: cy, r: r, class: 'f-ink' }, svg);
        else S('circle', { cx: cx, cy: cy, r: r, class: 'f-none s thin s-line' }, svg);
        if (typeof c === 'string' && c !== 'on' && c !== 'part' && c !== 'miss') { /* text cell */ }
      });
      y += h;
    });
    S('path', { d: 'M0 ' + y + 'H' + W, class: 'gr' }, svg);
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + (y + 2));
    return { svg: svg, legendHtml: spec.legend };
  };

  /* ---- ring: sectors round a wheel, rings from the rim inwards, one dot per item ---- */
  B.ring = function (spec, W) {
    var svg = S('svg', { class: 'cx' }), n = spec.sectors.length, rings = spec.rings.length;
    var Hh = Math.min(W, 520), cx = W / 2, cy = Hh / 2, R = Math.min(W, Hh) / 2 - 58, r0 = R * 0.2;
    var rr = function (k) { return R - (R - r0) * (k + 0.5) / rings; };
    for (var k = 0; k <= rings; k++) S('circle', { cx: cx, cy: cy, r: R - (R - r0) * k / rings, class: k === 0 ? 'f-paper ax' : 'f-none gr' }, svg);
    spec.sectors.forEach(function (sec, i) {
      var a0 = -Math.PI / 2 + 2 * Math.PI * i / n, a1 = a0 + 2 * Math.PI / n, am = (a0 + a1) / 2;
      S('path', { d: 'M' + (cx + r0 * Math.cos(a0)).toFixed(1) + ' ' + (cy + r0 * Math.sin(a0)).toFixed(1) + 'L' + (cx + R * Math.cos(a0)).toFixed(1) + ' ' + (cy + R * Math.sin(a0)).toFixed(1), class: 'ax' }, svg);
      var ls = wrap(sec.label, 14), lx = cx + (R + 12) * Math.cos(am), ly = cy + (R + 12) * Math.sin(am);
      textLines(svg, ls, lx, ly - (ls.length - 1) * 8 + 4 + (Math.sin(am) > 0.5 ? 8 : Math.sin(am) < -0.5 ? -4 : 0), 16, { 'text-anchor': Math.cos(am) > 0.3 ? 'start' : Math.cos(am) < -0.3 ? 'end' : 'middle', class: sec.em ? 'tb' : 'ti' });
      var byRing = {};
      sec.items.forEach(function (it) { (byRing[it.ring] = byRing[it.ring] || []).push(it); });
      Object.keys(byRing).forEach(function (rk) {
        byRing[rk].forEach(function (it, j, arr) {
          var a = a0 + (a1 - a0) * (j + 1) / (arr.length + 1), r = rr(+rk);
          S('circle', { cx: cx + r * Math.cos(a), cy: cy + r * Math.sin(a), r: 6.5, class: it.em ? 'f-rust' : it.open ? 'f-paper s thin s-ink' : 'f-ink' }, svg).appendChild(S('title', {}, null, it.label + ' · ' + spec.rings[+rk]));
        });
      });
    });
    spec.rings.forEach(function (name, k) { S('text', { x: cx + 4, y: cy - rr(k) + 5, class: 'halo tu' }, svg, name); });
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + Hh);
    return { svg: svg };
  };

  /* ---- payoff: a 2 x 2 game grid with move arrows ---- */
  B.payoff = function (spec, W) {
    var svg = S('svg', { class: 'cx' }), w = Math.min(W, 520), ox = (W - w) / 2 + 92, oy = 64, cw = (w - 104) / 2, ch = Math.min(cw * 0.72, 120);
    S('text', { x: ox + cw, y: 16, 'text-anchor': 'middle', class: 'tu' }, svg, spec.colPlayer);
    S('text', { x: ox - 84, y: oy - 14, class: 'tu' }, svg, spec.rowPlayer);
    spec.cols.forEach(function (c, j) { S('text', { x: ox + cw * (j + 0.5), y: oy - 14, 'text-anchor': 'middle', class: 'tn' }, svg, c); });
    spec.rows.forEach(function (r, i) {
      S('text', { x: ox - 14, y: oy + ch * (i + 0.5) + 6, 'text-anchor': 'end', class: 'tn' }, svg, r);
      spec.cols.forEach(function (c, j) {
        var hi = spec.highlight && spec.highlight[0] === i && spec.highlight[1] === j, cell = spec.cells[i][j];
        S('rect', { x: ox + cw * j, y: oy + ch * i, width: cw, height: ch, class: (hi ? 'f-soft' : 'f-paper') + ' s thin s-ink' }, svg);
        S('text', { x: ox + cw * j + 14, y: oy + ch * (i + 1) - 14, class: 'tn' }, svg, fmt(cell[0]));
        S('text', { x: ox + cw * (j + 1) - 14, y: oy + ch * i + 26, 'text-anchor': 'end', class: 'tn tr' }, svg, fmt(cell[1]));
      });
    });
    (spec.arrows || []).forEach(function (a) {
      var p = function (rc, t) { return [ox + cw * (rc[1] + 0.5), oy + ch * (rc[0] + 0.5)]; };
      var A = p(a.from), Bp = p(a.to), dx = Bp[0] - A[0], dy = Bp[1] - A[1], L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L, pad = 30;
      arrowLine(svg, [[A[0] + ux * pad, A[1] + uy * pad], [Bp[0] - ux * pad, Bp[1] - uy * pad]], a.who === 'col' ? 's s-rust dashed' : 's s-ink');
    });
    var Hh = oy + ch * 2 + 12;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + Hh);
    return { svg: svg, legend: [{ name: spec.rowPlayer + ' (bottom left number, solid arrow)', cls: 's s-ink' }, { name: spec.colPlayer + ' (top right number, dashed arrow)', cls: 's s-rust dashed' }] };
  };

  /* ---- timeline: rows of segments on a shared time axis ---- */
  B.timeline = function (spec, W) {
    var svg = S('svg', { class: 'cx' }), labW = W < 460 ? 0 : Math.min(150, W * 0.26), X = lin(spec.min || 0, spec.max, labW + 8, W - 14), y = 6;
    spec.rows.forEach(function (row) {
      var ls = wrap(row.label, labW ? Math.floor(labW / 7) : 60);
      if (!labW) { textLines(svg, ls, 0, y + 14, 17, { class: 'tb' }); y += ls.length * 17 + 6; }
      else textLines(svg, ls, 0, y + 30 - (ls.length - 1) * 8.5, 17, { class: 'tb' });
      S('path', { d: 'M' + X(spec.min || 0) + ' ' + (y + 25) + 'H' + X(spec.max), class: 'gr' }, svg);
      row.segments.forEach(function (sg) {
        var x0 = X(sg.from), x1 = X(sg.to);
        if (sg.kind === 'plan') S('path', { d: 'M' + x0 + ' ' + (y + 25) + 'H' + x1, class: 's s-soft dashed' }, svg);
        else S('rect', { x: x0, y: y + 14, width: Math.max(2, x1 - x0), height: 22, class: sg.kind === 'on' ? 'f-rust' : 'f-ink' }, svg);
        if (sg.look) { S('circle', { cx: x0, cy: y + 25, r: 6, class: 'f-paper s thin s-ink' }, svg); S('circle', { cx: x0, cy: y + 25, r: 2, class: 'f-ink' }, svg); }
      });
      if (row.note) { var nl = wrap(row.note, Math.floor((W - labW - 20) / 6.6)); textLines(svg, nl, labW + 8, y + 56, 17, {}); y += (nl.length - 1) * 17; }
      y += 78;
    });
    var ty = y - 8;
    S('path', { d: 'M' + X(spec.min || 0) + ' ' + ty + 'H' + X(spec.max), class: 'ax' }, svg);
    (spec.ticks || []).forEach(function (t) {
      S('path', { d: 'M' + X(t.at) + ' ' + ty + 'v5', class: 'ax' }, svg);
      S('text', { x: X(t.at), y: ty + 20, 'text-anchor': t.at === (spec.min || 0) ? 'start' : t.at === spec.max ? 'end' : 'middle' }, svg, t.label);
    });
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + (ty + 28));
    return { svg: svg, legendHtml: spec.legend };
  };

  /* ---- shapes in data coordinates (used by plane and field) ---- */
  function drawShapes(svg, shapes, X, Y, W) {
    (shapes || []).forEach(function (sh) {
      var cls = (sh.fill ? 'f-' + sh.fill : 'f-none') + ' s s-' + (sh.color || 'ink') + (sh.style ? ' ' + sh.style : '') + (sh.thin ? ' thin' : '');
      var sx = Math.abs(X(1) - X(0)), sy = Math.abs(Y(1) - Y(0)), e;
      if (sh.k === 'circle') e = S('ellipse', { cx: X(sh.c[0]), cy: Y(sh.c[1]), rx: sh.r * sx, ry: sh.r * sy, class: cls }, svg);
      else if (sh.k === 'ellipse') e = S('ellipse', { cx: X(sh.c[0]), cy: Y(sh.c[1]), rx: sh.rx * sx, ry: sh.ry * sy, class: cls }, svg);
      else if (sh.k === 'line') e = S('path', { d: 'M' + X(sh.a[0]).toFixed(1) + ' ' + Y(sh.a[1]).toFixed(1) + 'L' + X(sh.b[0]).toFixed(1) + ' ' + Y(sh.b[1]).toFixed(1), class: cls }, svg);
      else if (sh.k === 'path') {
        e = S('path', { d: pathOf(sh.pts, X, Y, sh.step), class: cls }, svg);
        if (sh.arrow) { var n = sh.pts.length, a = sh.pts[n - 2], b = sh.pts[n - 1]; arrowHead(svg, X(b[0]), Y(b[1]), Math.atan2(Y(b[1]) - Y(a[1]), X(b[0]) - X(a[0])), cls); }
        if (sh.dots) sh.pts.forEach(function (p, i) { S('circle', { cx: X(p[0]), cy: Y(p[1]), r: i === sh.pts.length - 1 ? 5.5 : 4, class: 'f-' + (sh.color || 'ink') }, svg); });
      }
      else if (sh.k === 'poly') e = S('path', { d: pathOf(sh.pts, X, Y) + 'Z', class: cls + (sh.noline ? ' f-only' : '') , 'stroke-width': sh.noline ? 0 : null }, svg);
      else if (sh.k === 'arrow') {
        arrowLine(svg, [[X(sh.a[0]), Y(sh.a[1])], [X(sh.b[0]), Y(sh.b[1])]], cls);
        if (sh.label) label(svg, X(sh.b[0]) + (sh.dx != null ? sh.dx : 8), Y(sh.b[1]) + (sh.dy != null ? sh.dy : -6), sh.label, sh.cls || (sh.color === 'rust' ? 'tr' : 'ti'), sh.anchor);
      }
      else if (sh.k === 'pt') {
        S('circle', { cx: X(sh.at[0]), cy: Y(sh.at[1]), r: sh.r || 6, class: sh.hollow ? 'f-paper s thin s-' + (sh.color || 'ink') : 'f-' + (sh.color || 'ink') + ' halo' }, svg);
        if (sh.label) {
          var an = sh.anchor || (X(sh.at[0]) > W * 0.68 ? 'end' : 'start'), ls = wrap(sh.label, sh.wrap || 24);
          textLines(svg, ls, X(sh.at[0]) + (an === 'end' ? -11 : an === 'middle' ? 0 : 11) + (sh.dx || 0), Y(sh.at[1]) + (sh.dy != null ? sh.dy : -10), 16, { class: (sh.cls || 'ti') + ' halo', 'text-anchor': an });
        }
      }
      else if (sh.k === 'text') {
        textLines(svg, wrap(sh.text, sh.wrap || 28), X(sh.at[0]) + (sh.dx || 0), Y(sh.at[1]) + (sh.dy || 0), 16, { class: (sh.cls || 'ti') + ' halo', 'text-anchor': sh.anchor || 'start' });
      }
      if (e && sh.title) S('title', {}, e, sh.title);
    });
  }

  /* ---- plane: geometry in data coordinates, with optional slider frames ---- */
  B.plane = function (spec, W, st) {
    var svg = S('svg', { class: 'cx' });
    var Hh = Math.round(Math.max(220, Math.min(W * (spec.ratio || 0.7), 460)));
    var opt = spec.lens ? spec.lens.options[st.lens || 0] : null, sp = opt && opt.y ? Object.assign({}, spec, { y: opt.y }) : spec, f;
    if (sp.axes === false) {
      var m = 10, uw = (W - 2 * m) / (sp.x.max - sp.x.min);
      var mx = m;
      if (sp.equal !== false) {
        Hh = Math.round(uw * (sp.y.max - sp.y.min) + 2 * m);
        var capH = maxPlotH(W);
        if (Hh > capH) { uw = (capH - 2 * m) / (sp.y.max - sp.y.min); mx = (W - uw * (sp.x.max - sp.x.min)) / 2; Hh = capH; }
      }
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + Hh);
      f = { X: lin(sp.x.min, sp.x.max, mx, W - mx), Y: lin(sp.y.min, sp.y.max, Hh - m, m) };
    } else f = frame(svg, W, Hh, sp, { equal: sp.equal === true });
    drawShapes(svg, sp.shapes, f.X, f.Y, W);
    if (opt && opt.shapes) drawShapes(svg, opt.shapes, f.X, f.Y, W);
    var out = { svg: svg, reads: (opt && opt.reads) || sp.reads || [], note: opt && opt.note };
    var frames = sp.framesByLens ? sp.framesByLens[st.lens || 0] : sp.frames;
    if (frames) {
      var fr = frames[Math.max(0, Math.min(frames.length - 1, Math.round(((st.v != null ? st.v : sp.slider.value) - sp.slider.min) / (sp.slider.step || 1))))];
      drawShapes(svg, fr.shapes, f.X, f.Y, W);
      if (fr.reads) out.reads = fr.reads;
      if (fr.note != null) out.note = fr.note;
    }
    out.legendHtml = (opt && opt.legend) || sp.legend;
    return out;
  };

  /* ---- field: a vector field x' = A x + c (c = b·u when a slider sets u), with paths ---- */
  B.field = function (spec, W, st) {
    var svg = S('svg', { class: 'cx' });
    var Hh = Math.round(Math.max(240, Math.min(W * (spec.ratio || 0.72), 440)));
    var f = frame(svg, W, Hh, spec, {}), X = f.X, Y = f.Y, A = spec.A, u = st.v != null ? st.v : 1;
    var c = spec.b ? [spec.b[0] * u, spec.b[1] * u] : (spec.c || [0, 0]);
    var F = function (x, y) { return [A[0][0] * x + A[0][1] * y + c[0], A[1][0] * x + A[1][1] * y + c[1]]; };
    var nx = Math.max(6, Math.floor((W - 70) / 44)), ny = Math.max(5, Math.floor((f.H - 60) / 40)), maxL = 0, vs = [];
    for (var i = 0; i < nx; i++) for (var j = 0; j < ny; j++) {
      var x = spec.x.min + (spec.x.max - spec.x.min) * (i + 0.5) / nx, y = spec.y.min + (spec.y.max - spec.y.min) * (j + 0.5) / ny, v = F(x, y);
      var px = v[0] * Math.abs(X(1) - X(0)), py = -v[1] * Math.abs(Y(1) - Y(0)), L = Math.hypot(px, py);
      maxL = Math.max(maxL, L); vs.push([X(x), Y(y), px, py, L]);
    }
    vs.forEach(function (q) {
      if (q[4] < 1e-9) { S('circle', { cx: q[0], cy: q[1], r: 2, class: 'f-mute' }, svg); return; }
      var len = 8 + 14 * Math.sqrt(q[4] / maxL), ux = q[2] / q[4], uy = q[3] / q[4];
      S('path', { d: 'M' + (q[0] - ux * len / 2).toFixed(1) + ' ' + (q[1] - uy * len / 2).toFixed(1) + 'L' + (q[0] + ux * len / 2).toFixed(1) + ' ' + (q[1] + uy * len / 2).toFixed(1), class: 's s-soft thin' }, svg);
      arrowHead(svg, q[0] + ux * len / 2, q[1] + uy * len / 2, Math.atan2(uy, ux), 's s-soft', 6);
    });
    var reads = [];
    (spec.paths || []).forEach(function (p, k) {
      var pts = p.points;
      if (!pts) {
        pts = [p.from.slice()]; var s = p.from.slice(), dt = p.dt || 0.01, n = Math.round(p.T / dt);
        for (var q = 0; q < n; q++) { var d = F(s[0], s[1]); s = [s[0] + dt * d[0], s[1] + dt * d[1]]; pts.push(s); }
      }
      pts = pts.filter(function (z) { return z[0] >= spec.x.min && z[0] <= spec.x.max && z[1] >= spec.y.min && z[1] <= spec.y.max; });
      if (pts.length < 2) return;
      drawShapes(svg, [{ k: 'path', pts: pts, color: p.color || (k ? 'ink' : 'rust'), arrow: true, style: p.style }, { k: 'pt', at: pts[0], label: p.label, hollow: true }], X, Y, W);
      if (p.read) { var e = pts[pts.length - 1]; reads.push({ label: p.read[0], value: fmt(e[0], 2) }, { label: p.read[1], value: fmt(e[1], 2) }); }
    });
    drawShapes(svg, spec.shapes, X, Y, W);
    return { svg: svg, reads: reads };
  };

  /* ---- tree: game trees, recursion, a map of methods ---- */
  B.tree = function (spec, W) {
    var svg = S('svg', { class: 'cx' }), rows = [], y = 6, indent = W < 520 ? 22 : 34;
    (function walk(n, d, last) {
      var boxW = Math.min(W - d * indent - 2, spec.boxWidth || 300), ls = wrap(n.label, Math.floor((boxW - 24) / 7.4));
      var nl = n.note ? wrap(n.note, Math.floor((W - d * indent - 40) / 6.4)) : [];
      var h = ls.length * 19 + 14;
      var r = { n: n, d: d, y: y, h: h, x: d * indent, w: boxW, ls: ls, nl: nl, kids: [] };
      rows.push(r); y += h + (nl.length ? nl.length * 17 + 6 : 0) + 10;
      (n.children || []).forEach(function (c, i, arr) { r.kids.push(walk(c, d + 1, i === arr.length - 1)); });
      return r;
    })(spec.root, 0, true);
    rows.forEach(function (r) {
      r.kids.forEach(function (k) {
        S('path', { d: 'M' + (r.x + 12) + ' ' + (r.y + r.h) + 'V' + (k.y + k.h / 2) + 'H' + k.x, class: 's thin ' + (k.n.dashed ? 's-rust thread' : 's-ink') }, svg);
      });
    });
    rows.forEach(function (r) {
      var n = r.n, fill = n.em ? 'f-rust' : n.dark ? 'f-esp' : n.leaf === false || (n.children && n.children.length) ? 'f-paper' : 'f-sand';
      S('rect', { x: r.x + 0.75, y: r.y, width: r.w - 1.5, height: r.h, class: fill + ' s thin ' + (n.dashed ? 's-rust dashed' : n.em ? 's-rust' : 's-ink') }, svg);
      textLines(svg, r.ls, r.x + 12, r.y + 21, 19, { class: 'tn' + (n.em ? ' tor' : n.dark ? ' tp' : '') });
      if (r.nl.length) textLines(svg, r.nl, r.x + (r.kids.length ? 26 : 12), r.y + r.h + 17, 17, {});
    });
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + (y + 2));
    return { svg: svg };
  };

  /* ---- grid: a state grid for dynamic programming; frames step through sweeps ---- */
  B.grid = function (spec, W, st) {
    var svg = S('svg', { class: 'cx' });
    var cells = spec.cells, fr = null;
    if (spec.frames) { fr = spec.frames[Math.max(0, Math.min(spec.frames.length - 1, Math.round(((st.v != null ? st.v : spec.slider.value) - spec.slider.min) / (spec.slider.step || 1))))]; cells = fr.cells || cells; }
    var R = cells.length, C = cells[0].length, lab = spec.rowLabels ? 34 : 2, cw = Math.min(84, (W - lab - 2) / C), ox = lab + (W - lab - cw * C) / 2, oy = spec.colLabels ? 24 : 2;
    var AR = { r: [1, 0], l: [-1, 0], u: [0, -1], d: [0, 1] };
    cells.forEach(function (row, i) {
      if (spec.rowLabels) S('text', { x: ox - 8, y: oy + cw * (i + 0.5) + 5, 'text-anchor': 'end' }, svg, spec.rowLabels[i]);
      row.forEach(function (c, j) {
        if (spec.colLabels && !i) S('text', { x: ox + cw * (j + 0.5), y: 14, 'text-anchor': 'middle' }, svg, spec.colLabels[j]);
        c = c == null ? {} : typeof c === 'object' ? c : { v: c };
        var x = ox + cw * j, y = oy + cw * i, fill = { goal: 'f-rust', wall: 'f-esp', path: 'f-soft', on: 'f-peach', empty: 'f-sand' }[c.s] || 'f-paper';
        S('rect', { x: x, y: y, width: cw, height: cw, class: fill + ' s thin s-ink' }, svg);
        if (c.v != null) S('text', { x: x + cw / 2, y: y + cw / 2 + (c.a ? -2 : 6), 'text-anchor': 'middle', class: 'tn' + (c.s === 'goal' ? ' tor' : c.s === 'wall' ? ' tp' : '') }, svg, typeof c.v === 'number' ? fmt(c.v) : c.v);
        if (c.a && AR[c.a]) { var d = AR[c.a], mx = x + cw / 2, my = y + cw * (c.v != null ? 0.76 : 0.5), L = cw * 0.2; arrowLine(svg, [[mx - d[0] * L, my - d[1] * L], [mx + d[0] * L, my + d[1] * L]], 's thin s-rust'); }
      });
    });
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + (oy + cw * R + 2));
    return { svg: svg, reads: fr && fr.reads || [], note: fr && fr.note, legendHtml: spec.legend };
  };

  /* ---- flow: boxes on a grid joined by arrows; a lens swaps the sub-labels ---- */
  B.flow = function (spec, W, st) {
    var svg = S('svg', { class: 'cx' }), cols = spec.cols, rowsN = spec.rows, narrow = W < 500;
    var gap = narrow ? 22 : 56, bw = (W - gap * (cols - 1)) / cols, bh = narrow ? 74 : 78, rg = narrow ? 50 : 58;
    var variant = spec.lens ? spec.lens.options[st.lens || 0] : null, pos = {};
    var Hh = rowsN * bh + (rowsN - 1) * rg + 4;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + Hh);
    spec.nodes.forEach(function (n) { pos[n.id] = { x: n.col * (bw + gap), y: 2 + n.row * (bh + rg), w: bw * (n.span || 1) + gap * ((n.span || 1) - 1), h: bh, n: n }; });
    var eg = S('g', {}, svg);
    spec.nodes.forEach(function (n) {
      var p = pos[n.id], sub = variant && variant.subs && variant.subs[n.id] != null ? variant.subs[n.id] : n.sub;
      if (!n.bare) S('rect', { x: p.x + 1, y: p.y + 1, width: p.w - 2, height: p.h - 2, class: (n.em ? 'f-soft s s-rust' : n.dark ? 'f-esp s s-ink' : 'f-paper s thin s-ink') + (n.dashed ? ' dashed' : '') }, svg);
      var chars = Math.floor((p.w - 16) / (narrow ? 7.2 : 7.6)), tl = wrap(n.label, Math.max(6, Math.floor((p.w - 16) / 8.6))), sl = sub ? wrap(sub, chars) : [];
      var total = tl.length * 19 + sl.length * 16, ty = p.y + (p.h - total) / 2 + 15;
      textLines(svg, tl, p.x + p.w / 2, ty, 19, { 'text-anchor': 'middle', class: 'tn' + (n.dark ? ' tp' : '') });
      if (sl.length) textLines(svg, sl, p.x + p.w / 2, ty + tl.length * 19, 16, { 'text-anchor': 'middle', class: n.dark ? 'tp' : n.em ? 'tr' : '' });
    });
    spec.edges.forEach(function (e) {
      var a = pos[e.from], b = pos[e.to], cls = 's ' + (e.color ? 's-' + e.color : 's-ink') + (e.style ? ' ' + e.style : ''), pts, r = e.route || 'h';
      var acx = a.x + a.w / 2, acy = a.y + a.h / 2, bcx = b.x + b.w / 2, bcy = b.y + b.h / 2;
      if (r === 'h') pts = bcx > acx ? [[a.x + a.w, acy], [b.x - 2, bcy]] : [[a.x, acy], [b.x + b.w + 2, bcy]];
      else if (r === 'v') { var vx = (acx > b.x + 12 && acx < b.x + b.w - 12) ? acx : bcx, sx = (vx > a.x + 12 && vx < a.x + a.w - 12) ? vx : acx; pts = bcy > acy ? [[sx, a.y + a.h], [vx, b.y - 2]] : [[sx, a.y], [vx, b.y + b.h + 2]]; }
      else if (r === 'vh') pts = [[acx, bcy > acy ? a.y + a.h : a.y], [acx, bcy], [bcx > acx ? b.x - 2 : b.x + b.w + 2, bcy]];
      else pts = [[bcx > acx ? a.x + a.w : a.x, acy], [bcx, acy], [bcx, bcy > acy ? b.y - 2 : b.y + b.h + 2]];
      arrowLine(eg, pts, cls);
      var lab = variant && variant.edges && variant.edges[e.id] != null ? variant.edges[e.id] : e.label;
      if (lab) {
        var i0 = e.labelSeg || 0, p0 = pts[i0], p1 = pts[i0 + 1], mx = (p0[0] + p1[0]) / 2, my = (p0[1] + p1[1]) / 2, horiz = Math.abs(p1[1] - p0[1]) < 1;
        var ll = wrap(lab, horiz ? Math.max(8, Math.floor(Math.abs(p1[0] - p0[0]) / 6.4)) : Math.max(9, Math.floor((bw / 2 - 14) / 6.3)));
        textLines(svg, ll, horiz ? mx : mx + 8, horiz ? my - 9 - (ll.length - 1) * 16 : my + 5 - (ll.length - 1) * 8, 16, { 'text-anchor': horiz ? 'middle' : 'start', class: 'halo ' + (e.color === 'rust' ? 'tr' : 'ti') });
      }
    });
    return { svg: svg };
  };

  /* ---- mounting: slider, lens, readouts, legend, redraw on resize ---- */
  function mount(host, spec) {
    if (!B[spec.type]) { host.textContent = 'Unknown chart type: ' + spec.type; return; }
    host.classList.add('ck-chart'); host.textContent = '';
    var st = { v: spec.slider ? spec.slider.value : null, lens: 0 }, uid = 'ck' + Math.random().toString(36).slice(2, 8);
    var top = H('div', {}, host), box = H('div', {}, host), reads = H('dl', { class: 'ck-reads', 'aria-live': 'polite' }, host), note = H('p', { class: 'ck-note', 'aria-live': 'polite' }, host), leg = H('ul', { class: 'ck-legend' }, host);
    box.style.minWidth = '0';
    if (spec.lens) {
      var lw = H('div', { class: 'ck-lens', role: 'group', 'aria-label': spec.lens.label || 'Example' }, top);
      spec.lens.options.forEach(function (o, i) {
        var b = H('button', { type: 'button', 'aria-pressed': i === 0 ? 'true' : 'false' }, lw, o.name);
        b.addEventListener('click', function () { st.lens = i; [].forEach.call(lw.children, function (c, j) { c.setAttribute('aria-pressed', j === i ? 'true' : 'false'); }); draw(); });
      });
    }
    if (spec.slider) {
      var sl = spec.slider, ctl = H('div', { class: 'ck-ctl' }, top);
      H('label', { for: uid }, ctl, sl.label);
      var input = H('input', { type: 'range', id: uid, min: sl.min, max: sl.max, step: sl.step || 'any', value: sl.value }, ctl);
      var out = H('output', { for: uid }, ctl);
      var show = function () { var txt = sl.labels ? sl.labels[Math.round((st.v - sl.min) / (sl.step || 1))] : fmt(st.v, sl.decimals) + (sl.unit ? ' ' + sl.unit : ''); out.textContent = txt; input.setAttribute('aria-valuetext', txt); };
      input.addEventListener('input', function () { st.v = +input.value; show(); draw(); });
      show();
    }
    var lastW = 0;
    function draw() {
      var W = Math.max(260, Math.round(box.clientWidth || host.clientWidth || 560));
      lastW = W;
      var o = B[spec.type](spec, W, st);
      o.svg.setAttribute('role', 'img');
      o.svg.setAttribute('aria-label', spec.title + (spec.desc ? '. ' + spec.desc : ''));
      o.svg.setAttribute('width', W);
      box.textContent = ''; box.appendChild(o.svg);
      if (spec.declutter !== false) declutter(o.svg);
      reads.textContent = '';
      (o.reads || []).forEach(function (r) {
        var d = H('div', {}, reads); H('dt', {}, d, r.label);
        var dd = H('dd', { class: r.on ? 'on' : null }, d, r.value); if (r.unit) H('small', {}, dd, r.unit);
      });
      reads.hidden = !(o.reads && o.reads.length);
      note.textContent = o.note || ''; note.hidden = !spec.notes && !o.note;
      leg.textContent = '';
      (o.legend || []).forEach(function (l) {
        var li = H('li', {}, leg), sv = S('svg', { class: 'cx', viewBox: '0 0 28 10', 'aria-hidden': 'true' }, li);
        S('path', { d: 'M1 5H27', class: l.cls }, sv); H('span', {}, li, l.name);
      });
      (o.legendHtml || []).forEach(function (l) {
        var li = H('li', {}, leg), sv = S('svg', { class: 'cx', viewBox: '0 0 28 12', 'aria-hidden': 'true' }, li);
        if (l.mark === 'dot') S('circle', { cx: 14, cy: 6, r: 5.5, class: l.cls }, sv);
        else if (l.mark === 'box') S('rect', { x: 4, y: 0, width: 20, height: 12, class: l.cls }, sv);
        else S('path', { d: 'M1 6H27', class: l.cls }, sv);
        H('span', {}, li, l.name);
      });
      leg.hidden = !leg.children.length;
    }
    draw();
    if (spec.source) H('p', { class: 'ck-srcline' }, host, 'Source: ' + spec.source);
    if (window.ResizeObserver) {
      var t; new ResizeObserver(function () {
        var W = Math.max(260, Math.round(box.clientWidth)); if (Math.abs(W - lastW) < 2) return;
        clearTimeout(t); t = setTimeout(draw, 60);
      }).observe(box);
    }
    host.setAttribute('data-chart-ready', '1');
  }
  function mountAll(root) {
    [].forEach.call((root || document).querySelectorAll('[data-chart]:not([data-chart-ready])'), function (host) {
      var sc = host.querySelector('script[type="application/json"]');
      try { mount(host, JSON.parse(sc ? sc.textContent : host.getAttribute('data-chart'))); }
      catch (e) { host.setAttribute('data-chart-error', e.message); if (window.console) console.error('KitCharts', e); }
    });
  }
  window.KitCharts = { mount: mount, mountAll: mountAll, builders: B, fmt: fmt, declutter: declutter };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { mountAll(); }); else mountAll();
})();
