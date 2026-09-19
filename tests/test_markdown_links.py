import json
from pathlib import Path

from scripts.audit_markdown_links import audit


ROOT = Path(__file__).resolve().parents[1]


def test_markdown_local_links_resolve() -> None:
    result = audit(ROOT)
    assert result["status"] == "passed"
    assert result["local_link_count"] >= 470
    assert result["missing_links"] == []
    stored = json.loads((ROOT / "reports/markdown-link-audit-v1.json").read_text())
    assert stored["status"] == "passed"
