"""Shared inventory inclusion rules; retained slots are not necessarily papers."""


def title_eligible(record: dict) -> bool:
    return bool((record.get("title") or "").strip()) and record.get("inventory_inclusion") != "excluded_unresolved_slot"


def partition_titles(records: list[dict]) -> tuple[list[dict], list[dict]]:
    included, excluded = [], []
    for row in records:
        (included if title_eligible(row) else excluded).append(row)
    return included, excluded
