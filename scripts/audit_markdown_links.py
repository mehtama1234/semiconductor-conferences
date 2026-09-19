#!/usr/bin/env python3
"""Audit local Markdown links used by the reader-facing research package."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def audit(root: Path = ROOT) -> dict:
    missing = []
    total = 0
    files = 0
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts or "node_modules" in path.parts:
            continue
        files += 1
        for raw in LINK_RE.findall(path.read_text(encoding="utf-8", errors="ignore")):
            target = raw.strip().strip("<>").split("#", 1)[0].split("?", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            total += 1
            candidate = (path.parent / unquote(target)).resolve()
            if not candidate.exists():
                missing.append({"source": str(path.relative_to(root)), "target": target})
    result = {
        "schema": "markdown-link-audit.v1",
        "status": "passed" if not missing else "failed",
        "markdown_file_count": files,
        "local_link_count": total,
        "missing_links": missing,
        "limits": [
            "The audit checks local file targets, not external URL availability or heading-anchor semantics.",
            "A resolved file does not establish that its scientific content is correct.",
        ],
    }
    (root / "reports/markdown-link-audit-v1.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    result = audit()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "passed" else 1)
