#!/usr/bin/env python3
"""Pack the whole database into one gzipped JSON file.

The bundle is what the site (and anything else) reads instead of the individual YAML files:

    {
      "commit": "<sha of the database this was built from, or null>",
      "generated_at": "<UTC, ISO 8601>",
      "recipes": {"<file stem>": {...}, ...},
      "ingredients": {"<file stem>": {...}, ...}
    }

Records are included exactly as parsed from their YAML, keyed by file stem, so the stems stay
the ids. The gzip header carries no timestamp, so the same data always gives the same bytes.

Usage: python scripts/build_bundle.py OUTPUT [DATABASE_DIR]
Requires: pyyaml
"""

import gzip
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from validate_database import load_records


def source_commit(database_dir: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(database_dir), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    output = Path(sys.argv[1])
    database_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent

    bundle = {
        "commit": source_commit(database_dir),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "recipes": load_records(database_dir / "recipes"),
        "ingredients": load_records(database_dir / "ingredients"),
    }
    encoded = json.dumps(bundle, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    output.write_bytes(gzip.compress(encoded, compresslevel=9, mtime=0))

    print(
        f"Wrote {output}: {len(bundle['recipes'])} recipes and {len(bundle['ingredients'])} ingredients, "
        f"{len(encoded)} bytes of JSON in {output.stat().st_size} bytes gzipped"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
