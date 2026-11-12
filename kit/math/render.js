// Course kit · server-side maths. Reads one JSON object per line: {"tex": "...", "display": true}; writes one JSON line: {"html": "..."} or {"error": "..."}.
// Run by kit/kitmath.py at build time. Nothing here runs in the reader's browser.
const katex = require('./katex.min.js');
const rl = require('readline').createInterface({ input: process.stdin });
rl.on('line', line => {
  let out;
  try {
    const q = JSON.parse(line);
    out = { html: katex.renderToString(q.tex, { displayMode: !!q.display, throwOnError: true, strict: false, output: 'htmlAndMathml', trust: false }) };
  } catch (e) { out = { error: String(e && e.message || e) }; }
  process.stdout.write(JSON.stringify(out) + '\n');
});
