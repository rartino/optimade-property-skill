#!/usr/bin/env python3
"""Select source YAML examples relevant to a query."""

from __future__ import annotations

import argparse
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def candidate_roots(root: Path) -> list[Path]:
    return [
        root / "skills" / "optimade-property-yaml" / "references" / "examples",
        root / "external" / "OPTIMADE",
        root / "external" / "optimade-property-tools",
    ]


def score_file(path: Path, terms: list[str]) -> int:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        text = ""
    name = path.name.lower()
    parts = [part.lower() for part in path.parts]
    score = 0
    for term in terms:
        if term in name:
            score += 50
        score += 10 * sum(1 for part in parts if term in part)
        score += text.count(term)
    return score


def main() -> int:
    parser = argparse.ArgumentParser(description="Find relevant OPTIMADE source YAML examples.")
    parser.add_argument("query", nargs="+", help="Search query terms")
    args = parser.parse_args()

    terms = " ".join(args.query).lower().split()
    root = repo_root()
    scored: list[tuple[int, Path]] = []
    for search_root in candidate_roots(root):
        if not search_root.exists():
            continue
        for path in search_root.rglob("*"):
            if path.suffix.lower() not in {".yaml", ".yml"} or not path.is_file():
                continue
            score = score_file(path, terms)
            if score > 0:
                scored.append((score, path))

    for score, path in sorted(scored, key=lambda item: (-item[0], str(item[1])))[:10]:
        print(f"{score:5d} {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
