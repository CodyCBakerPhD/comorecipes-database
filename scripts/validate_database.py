#!/usr/bin/env python3
"""Validate every record in the recipe database.

Each YAML file in recipes/ and ingredients/ is checked against the JSON Schema for its
kind (schemas/), then the checks a schema cannot express run across the whole database:
file stems are snake_case ids, names are unique, and every `recipe:` cross-link points
at a recipe that exists and is not the recipe itself.

Usage: python scripts/validate_database.py [DATABASE_DIR]
Requires: pyyaml, jsonschema
"""

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

STEM_PATTERN = re.compile(r"^[a-z0-9_]+$")


def load_records(directory: Path) -> dict[str, object]:
    """File stem to parsed YAML, for every .yaml file in the directory."""
    return {path.stem: yaml.safe_load(path.read_text(encoding="utf-8")) for path in sorted(directory.glob("*.yaml"))}


def schema_errors(kind: str, records: dict[str, object], schema: dict) -> list[str]:
    validator = Draft202012Validator(schema)
    errors = []
    for stem, record in records.items():
        if not STEM_PATTERN.match(stem):
            errors.append(f"{kind}/{stem}.yaml: file stem must be lowercase snake_case (a-z, 0-9, _)")
        for error in sorted(validator.iter_errors(record), key=lambda e: list(e.absolute_path)):
            location = "/".join(str(part) for part in error.absolute_path) or "(root)"
            errors.append(f"{kind}/{stem}.yaml at {location}: {error.message}")
    return errors


def unique_name_errors(kind: str, records: dict[str, object]) -> list[str]:
    stems_by_name: dict[str, list[str]] = {}
    for stem, record in records.items():
        name = record.get("name") if isinstance(record, dict) else None
        if isinstance(name, str):
            stems_by_name.setdefault(name, []).append(stem)
    return [
        f"{kind}: name {name!r} is used by more than one file: {', '.join(stems)}"
        for name, stems in stems_by_name.items()
        if len(stems) > 1
    ]


def cross_link_errors(recipes: dict[str, object]) -> list[str]:
    errors = []
    for stem, recipe in recipes.items():
        measurements = recipe.get("measurements") if isinstance(recipe, dict) else None
        if not isinstance(measurements, list):
            continue
        for index, measurement in enumerate(measurements):
            if not isinstance(measurement, dict) or "recipe" not in measurement:
                continue
            target = measurement["recipe"]
            ingredient = measurement.get("ingredient")
            if target == stem:
                errors.append(f"recipes/{stem}.yaml at measurements/{index}: ingredient {ingredient!r} says it is made from itself")
            elif target not in recipes:
                errors.append(
                    f"recipes/{stem}.yaml at measurements/{index}: ingredient {ingredient!r} says it is made from "
                    f"recipe {target!r}, but recipes/{target}.yaml does not exist"
                )
    return errors


def main() -> int:
    database_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    schemas_dir = database_dir / "schemas"

    errors = []
    records_by_kind = {}
    for kind in ("recipes", "ingredients"):
        records = load_records(database_dir / kind)
        records_by_kind[kind] = records
        schema = json.loads((schemas_dir / f"{kind[:-1]}.schema.json").read_text(encoding="utf-8"))
        errors += schema_errors(kind, records, schema)
        errors += unique_name_errors(kind, records)
    errors += cross_link_errors(records_by_kind["recipes"])

    counts = ", ".join(f"{len(records)} {kind}" for kind, records in records_by_kind.items())
    if errors:
        print(f"Found {len(errors)} problem(s) in {counts}:\n")
        print("\n".join(errors))
        return 1
    print(f"All records valid ({counts}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
