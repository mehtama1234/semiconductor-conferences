#!/usr/bin/env python3
"""Course kit · maths typeset at build time. No network and no script at view time.

    import kitmath            (the file is not called math.py: that name would hide Python's own math module)

    eq_html("x(α) = x − α ∇f(x)")            a display block from the lecture formats' plain formula
    eq_html(tex=r"\\frac{\\partial f}{\\partial x}")   a display block from TeX
    inline_html(r"\\nabla f(x^*) = 0")         inline maths from TeX
    tex_from_plain(text)                      the conversion alone (plain Unicode formula -> TeX)

How it works: KaTeX 0.16 (vendored in kit/math/, MIT) is run by Node once, as a line-by-line helper; the result is
HTML plus MathML that needs only kit/math/katex.min.css and the woff2 fonts in kit/math/fonts/.
If Node is not installed the formula falls back to the plain text block, so a build never fails.

Run `python3 kit/kitmath.py "x^2 / (1 + x)"` to see the TeX and check it renders.
"""
import atexit, html, json, re, shutil, subprocess, sys, unicodedata
from pathlib import Path

KIT = Path(__file__).resolve().parent
_proc = None
_cache = {}

SUP = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱᵏᵀᵗᵃᵇᶜᵈᵉᶠᵍʰʲˡᵐᵒᵖʳˢᵘᵛʷˣʸᶻᴺᴷ", "0123456789+-=()nikTtabcdefghjlmoprsuvwxyzNK"))
SUB = dict(zip("₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ", "0123456789+-=()aehijklmnoprstuvx"))
ACC = {"\u0307": "dot", "\u0308": "ddot", "\u0302": "hat", "\u0304": "bar", "\u0303": "tilde"}
OPS = {"sin", "cos", "tan", "exp", "log", "ln", "min", "max", "argmin", "argmax", "det", "tr", "sup", "inf", "lim", "rank", "diag", "sign", "arg", "sinh", "cosh", "tanh", "Pr", "Var", "Cov"}
STOP = {"is", "if", "of", "to", "in", "on", "at", "or", "as", "by", "so", "we", "no", "an", "be", "a", "s.t."}
CHARS = {"−": "-", "…": r"\dots ", "‖": r"\|", "·": r"\cdot ", "×": r"\times ", "ℝ": r"\mathbb{R}", "ℕ": r"\mathbb{N}", "ᵀ": r"^{\top}", "′": "'", "≜": r"\triangleq ",
         "⊤": r"\top ", "∘": r"\circ ", "⟨": r"\langle ", "⟩": r"\rangle ", "½": r"\tfrac12 ", "∑": "Σ", "→": r"\to ", "↦": r"\mapsto ", "⇒": r"\Rightarrow ", "⟹": r"\implies "}


def _balanced(s, i, open_="(", close=")"):
    """Index just past the bracket that closes the one at s[i]."""
    d = 0
    for j in range(i, len(s)):
        if s[j] == open_: d += 1
        elif s[j] == close:
            d -= 1
            if d == 0: return j + 1
    return -1


def _fractions(s):
    """a/b, (a)/(b), ∂f/∂x, d/dt -> \\frac{..}{..}. Operands are a bracketed group or one token with its sub- and superscripts."""
    tok = r"(?:\\[A-Za-z]+(?:\{[^{}]*\})?|[A-Za-z0-9.∂∇α-ωΑ-Ω]+)(?:[_^]\{[^{}]*\})*"
    out = s
    for _ in range(20):
        i = out.find("/")
        while i != -1 and (i == 0 or out[i - 1] in " <" or i + 1 >= len(out) or out[i + 1] in " >"): i = out.find("/", i + 1)
        if i == -1: break
        # left operand
        if out[i - 1] == ")":
            d, j = 0, i - 1
            while j >= 0:
                if out[j] == ")": d += 1
                elif out[j] == "(":
                    d -= 1
                    if d == 0: break
                j -= 1
            if j < 0: break
            m = re.search(r"(?:\\[A-Za-z]+|[A-Za-z0-9∂∇α-ω]+)$", out[:j])        # f(x)/g(x): keep the function name with its bracket
            if m and not re.search(r"[0-9]$", m.group(0)): ls, left = m.start(), out[m.start():i]
            else: ls, left = j, out[j + 1:i - 1]
        else:
            m = re.search(tok + r"$", out[:i])
            if not m: out = out[:i] + "\u2215" + out[i + 1:]; continue
            ls, left = m.start(), m.group(0)
        # right operand
        if out[i + 1] == "(":
            e = _balanced(out, i + 1)
            if e == -1: break
            right, re_ = out[i + 2:e - 1], e
        else:
            m = re.match(tok, out[i + 1:])
            if not m: out = out[:i] + "\u2215" + out[i + 1:]; continue
            right, re_ = m.group(0), i + 1 + m.end()
            if re_ < len(out) and out[re_] == "(" and re.search(r"[A-Za-z}]$", right) and not re.fullmatch(r"d[a-z]|∂[a-z]|\d+", right):
                e = _balanced(out, re_)                                          # 1/f(x): the bracket belongs to f
                if e != -1: right, re_ = out[i + 1:e], e
        out = out[:ls] + r"\frac{" + left + "}{" + right + "}" + out[re_:]
    return out.replace("\u2215", "/")


def _matrix(s):
    def rows(body):
        if ";" in body: return [re.split(r"[,\s]+", r.strip()) for r in body.split(";")]
        return None
    def nested(m):
        rws = re.findall(r"\[([^\[\]]*)\]", m.group(1))
        return r"\begin{bmatrix}" + r" \\ ".join(" & ".join(c.strip() for c in r.split(",")) for r in rws) + r"\end{bmatrix}"
    s = re.sub(r"\[\s*((?:\[[^\[\]]*\]\s*,?\s*)+)\]", nested, s)
    def semi(m):
        r = rows(m.group(1))
        return r"\begin{bmatrix}" + r" \\ ".join(" & ".join(c for c in row if c) for row in r) + r"\end{bmatrix}" if r else m.group(0)
    return re.sub(r"\[([^\[\]]*;[^\[\]]*)\]", semi, s)


def _words(s):
    """Runs of ordinary words become upright text; known function names become operators; single letters stay maths."""
    toks = re.findall(r"\\[A-Za-z]+|\\.|s\.t\.|[A-Za-z]+|[^A-Za-z\\]+", s)
    kinds = []
    for i, t in enumerate(toks):
        if t.startswith("\\"): kinds.append("cmd")
        elif re.fullmatch(r"[A-Za-z.]+", t):
            prev = toks[i - 1] if i else ""
            if prev in (r"\begin", r"\end", r"\mathbb", r"\text", r"\operatorname") or (prev.endswith("{") and i > 1 and toks[i - 2] in (r"\begin", r"\end", r"\mathbb")): kinds.append("keep")
            elif t in OPS: kinds.append("op")
            elif len(t) >= 3 or t in STOP: kinds.append("word")
            else: kinds.append("var")
        else: kinds.append("sep")
    # a stop word counts as a word only next to a real word ("is zero"), otherwise it is a variable ("a", "in")
    real = [k == "word" and (len(toks[i]) >= 3) for i, k in enumerate(kinds)]
    for i, k in enumerate(kinds):
        if k == "word" and not real[i]:
            near = any(0 <= j < len(toks) and real[j] and all(toks[m] in (" ", "-", ", ") for m in range(min(i, j) + 1, max(i, j))) for j in (i - 2, i + 2))
            if not near: kinds[i] = "var"
    out, i = [], 0
    while i < len(toks):
        if kinds[i] == "op": out.append(r"\operatorname{" + toks[i] + "}"); i += 1
        elif kinds[i] == "word":
            j = i
            while j + 2 < len(toks) and toks[j + 1] in (" ", "-", ", ", ": ") and kinds[j + 2] == "word": j += 2
            run = "".join(toks[i:j + 1])
            before = " " if i and toks[i - 1].endswith(" ") else ""
            after = " " if j + 1 < len(toks) and toks[j + 1].startswith(" ") else ""
            out.append(r"\text{" + before + run + after + "}"); i = j + 1
        else: out.append(toks[i]); i += 1
    return "".join(out)


def _line(s):
    s = unicodedata.normalize("NFD", s)
    s = re.sub(r"([A-Za-zα-ω])([\u0307\u0308\u0302\u0304\u0303])", lambda m: "\\" + ACC[m.group(2)] + "{" + m.group(1) + "}", s)
    s = unicodedata.normalize("NFC", s)
    for a, b in (("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("$", r"\$")): s = s.replace(a, b)
    for a, b in CHARS.items(): s = s.replace(a, b)
    s = re.sub("[" + "".join(SUP) + "]+", lambda m: "^{" + "".join(SUP[c] for c in m.group(0)) + "}", s)
    s = re.sub("[" + "".join(SUB) + "]+", lambda m: "_{" + "".join(SUB[c] for c in m.group(0)) + "}", s)
    s = re.sub(r"([∫Σ∏]) from (.+?) to (.+?) of ", lambda m: {"∫": r"\int", "Σ": r"\sum", "∏": r"\prod"}[m.group(1)] + "_{" + m.group(2) + "}^{" + m.group(3) + "} ", s)
    s = re.sub(r"\b(max|min|argmax|argmin|sup|inf) over (.+?) of ", lambda m: {"argmax": r"\arg\max", "argmin": r"\arg\min"}.get(m.group(1), "\\" + m.group(1)) + "_{" + m.group(2) + "} ", s)
    s = s.replace("Σ", r"\sum ").replace("∏", r"\prod ")
    s = re.sub(r"_(\\(?:dot|ddot|hat|bar|tilde)\{[^{}]*\})", r"_{\1}", s)
    s = re.sub(r"_\(([^()]*)\)", r"_{\1}", s); s = re.sub(r"\^\(([^()]*)\)", r"^{\1}", s)
    s = re.sub(r"_([A-Za-z0-9α-ω]+)", r"_{\1}", s); s = re.sub(r"\^(-?[A-Za-z0-9α-ω]+)", lambda m: "^{" + (r"\top" if m.group(1) == "T" else m.group(1)) + "}", s)
    s = re.sub(r"(?<=[A-Za-z0-9α-ω)}\]])\*(?![A-Za-z0-9 ])", "^{*}", s); s = re.sub(r"(?<=[A-Za-z0-9α-ω)}\]])\*(?=[A-Za-z(])", "^{*}", s); s = re.sub(r" \* ", r" \\cdot ", s)
    s = re.sub(r"\}\^\{\*\}\^\{", "}^{*", s); s = re.sub(r"\^\{\*\}_\{([^{}]*)\}", r"^{*}_{\1}", s)
    for name in ("√", "sqrt"):                                                  # roots
        while True:
            i = s.find(name + "(")
            if i == -1: break
            e = _balanced(s, i + len(name))
            if e == -1: break
            s = s[:i] + r"\sqrt{" + s[i + len(name) + 1:e - 1] + "}" + s[e:]
    s = re.sub(r"√([A-Za-z0-9α-ω]+)", r"\\sqrt{\1}", s)
    s = _matrix(_fractions(s))
    s = re.sub(r" {3,}", r" \\quad ", s.strip())
    return _words(s)


def tex_from_plain(text):
    """The lecture formats write formulas as plain Unicode ("xᵏ⁺¹ = xᵏ + αᵏ dᵏ", "∫ from t₀ to t_f of g dt"). Returns TeX for KaTeX."""
    lines = [ln for ln in text.strip().splitlines() if ln.strip()]
    lab = re.compile(r"^([A-Za-z][A-Za-z' -]{2,34}):\s{2,}(.*)$")
    def one(ln, amp):
        m = lab.match(ln.strip())
        if m: return r"\text{" + m.group(1) + r":}\quad " + amp + _line(m.group(2))
        return (amp if amp and any(lab.match(x.strip()) for x in lines) else "") + _line(ln)
    if len(lines) == 1: return one(lines[0], "")
    if any(lab.match(ln.strip()) for ln in lines): tex = [one(ln, "& ") for ln in lines]
    else:
        tex = [_line(ln) for ln in lines]
        rel = re.compile(r"(?<![<>=!\\{^_])(=|≤|≥|≈)")
        lhs = [len(rel.split(t, 1)[0]) for t in tex if rel.search(t)]
        even = len(lhs) == len(tex) and max(lhs) <= 28                     # align at the relation only when the left sides are short
        tex = [rel.sub(lambda m: "&" + m.group(1), t, count=1) for t in tex] if even else ["& " + t for t in tex]
    return r"\begin{aligned}" + r" \\ ".join(tex) + r"\end{aligned}"


def available():
    return shutil.which("node") is not None and (KIT / "math" / "katex.min.js").exists()


def render(tex, display=True):
    """KaTeX HTML for one formula, or None if it cannot be typeset here."""
    global _proc
    key = (tex, display)
    if key in _cache: return _cache[key]
    if not available(): return None
    if _proc is None or _proc.poll() is not None:
        _proc = subprocess.Popen(["node", str(KIT / "math" / "render.js")], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8")
        atexit.register(lambda: _proc and _proc.poll() is None and _proc.kill())
    _proc.stdin.write(json.dumps({"tex": tex, "display": display}) + "\n"); _proc.stdin.flush()
    res = json.loads(_proc.stdout.readline() or "{}")
    _cache[key] = res.get("html")
    if res.get("error"): print("math: could not typeset", repr(tex[:80]), "-", res["error"][:120], file=sys.stderr)
    return _cache[key]


def eq_html(text=None, tex=None, label=None):
    """A display formula in the kit's equation block. `text` is the plain formula (also the screen-reader label); `tex` overrides the conversion."""
    plain = text if text is not None else tex
    t = tex or tex_from_plain(text)
    out = render(t, True)
    lab = html.escape(label or plain, quote=True)
    if out is None:
        return f'<pre class="ck-eq" role="math" aria-label="{lab}">{html.escape(plain, quote=False)}</pre>'
    return f'<div class="ck-eq ck-math" role="math" aria-label="{lab}" data-tex="{html.escape(t, quote=True)}">{out}</div>'


def inline_html(tex):
    out = render(tex, False)
    return out if out is not None else f"<code>{html.escape(tex, quote=False)}</code>"


def head_link(kit="../kit"):
    return f'<link rel="stylesheet" href="{kit}/math/katex.min.css">\n'


if __name__ == "__main__":
    for a in sys.argv[1:] or ["x(α) = x − α ∇f(x)"]:
        t = tex_from_plain(a); print(a, "\n  ->", t, "\n  ", "ok" if render(t) else "NOT RENDERED")
