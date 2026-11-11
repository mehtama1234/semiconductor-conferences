const state = { taxonomy: null, query: "" };

const esc = (value) => String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
const pretty = (value) => String(value).replaceAll("-", " ").replace(/\b\w/g, c => c.toUpperCase());

function render() {
  const data = state.taxonomy;
  const q = state.query.toLowerCase();
  const themes = data.themes.map(theme => ({
    ...theme,
    subthemes: theme.subthemes.filter(sub => {
      const haystack = [theme.label, theme.theme_id, sub.label, sub.subtheme_id, ...sub.mechanisms.map(m => m.id)].join(" ").toLowerCase();
      return !q || haystack.includes(q);
    })
  })).filter(theme => theme.subthemes.length);
  document.querySelector("#stats").innerHTML = [
    [data.record_count, "records"], [data.observed_subtheme_count, "unique subthemes"], [data.theme_subtheme_assignment_count, "theme assignments"], [data.mechanism_count, "mechanisms"]
  ].map(([n, label]) => `<div class="stat"><strong>${n}</strong><span>${label}</span></div>`).join("");
  document.querySelector("#themes").innerHTML = themes.map(theme => `
    <article class="theme-card">
      <div class="theme-card-head"><div><h3>${esc(theme.label)}</h3><p>${theme.record_count} records · ${theme.subtheme_count} subthemes · ${theme.mechanism_count} mechanisms</p></div><a href="themes/${esc(theme.theme_id)}.html">Read the theme →</a></div>
      <div class="subthemes">${theme.subthemes.map(sub => `
        <details class="subtheme" ${q ? "open" : ""}>
          <summary><span>${esc(sub.label)}</span><em>${sub.record_count} records · ${sub.mechanism_count} mechanisms</em></summary>
          <div class="subtheme-body"><p><a href="subthemes/${esc(sub.subtheme_id)}.html">Read the subject and its paper evidence →</a></p><div class="chips">${Object.entries(sub.conference_counts).map(([k,v]) => `<span>${k.toUpperCase()} ${v}</span>`).join("")}</div><p>The article includes the recorded problem, proposed method, comparison, results, limits, and source locations for every paper in this subject.</p></div>
        </details>`).join("")}</div>
    </article>`).join("") || `<p class="empty">No matching taxonomy records.</p>`;
}

fetch("data/taxonomy-expanded-v1.json").then(r => { if (!r.ok) throw Error(r.status); return r.json(); }).then(data => { state.taxonomy = data; render(); }).catch(() => { document.querySelector('#themes').innerHTML = '<p>Unable to load the index. <a href="guide/expanded-taxonomy-v1.html">Open the complete written taxonomy</a>.</p>'; });
document.querySelector("#search").addEventListener("input", e => { state.query = e.target.value; render(); });
