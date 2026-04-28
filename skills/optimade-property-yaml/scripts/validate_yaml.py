#!/usr/bin/env python3
"""Lightweight structural checks for one OPTIMADE property source YAML file.

This is not full OPTIMADE semantic validation. It checks the minimum shape this
skill expects before a generated source file is handed to upstream tooling.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - exercised by users without PyYAML
    print("ERROR: PyYAML is required. Install it with: python3 -m pip install PyYAML", file=sys.stderr)
    sys.exit(2)

REQUIRED_TOP_LEVEL = [
    "$$schema",
    "$id",
    "title",
    "x-optimade-type",
    "x-optimade-definition",
    "type",
    "description",
]

REQUIRED_DEFINITION_KEYS = ["kind", "version", "format", "name", "label"]


def _find_inherit_errors(obj: Any, path: str, errors: list[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            child_path = f"{path}.{key}" if path else str(key)
            if key == "$$inherit" and not isinstance(value, str):
                errors.append(f"{child_path}: $$inherit value must be a string")
            _find_inherit_errors(value, child_path, errors)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            _find_inherit_errors(value, f"{path}[{index}]", errors)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        return [f"YAML parse error: {exc}"]
    except OSError as exc:
        return [f"Could not read file: {exc}"]

    if not isinstance(data, dict):
        return ["Top-level YAML document must be a mapping/object"]

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"Missing required top-level key: {key}")

    for key in ("$id", "title", "x-optimade-type", "description"):
        if key in data and (not isinstance(data[key], str) or not data[key].strip()):
            errors.append(f"{key} must be a non-empty string")

    definition = data.get("x-optimade-definition")
    if not isinstance(definition, dict):
        errors.append("x-optimade-definition must be a mapping/object")
    else:
        for key in REQUIRED_DEFINITION_KEYS:
            if key not in definition:
                errors.append(f"Missing x-optimade-definition.{key}")
        if definition.get("kind") != "property":
            errors.append('x-optimade-definition.kind must be "property"')
        for key in REQUIRED_DEFINITION_KEYS:
            if key in definition and (not isinstance(definition[key], str) or not definition[key].strip()):
                errors.append(f"x-optimade-definition.{key} must be a non-empty string")

    unit_definitions = data.get("x-optimade-unit-definitions")
    if unit_definitions is not None:
        if not isinstance(unit_definitions, list):
            errors.append("x-optimade-unit-definitions must be a list when present")
        else:
            _find_inherit_errors(unit_definitions, "x-optimade-unit-definitions", errors)

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lightweight structural validator for one OPTIMADE property-definition source YAML file."
    )
    parser.add_argument("yaml_path", help="Path to the source YAML file to validate")
    args = parser.parse_args(argv)

    path = Path(args.yaml_path)
    errors = validate(path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
