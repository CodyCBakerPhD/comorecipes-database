# Scripts

Both are run from the root of the repo and need `pip install pyyaml jsonschema`.

- `validate_database.py` checks every record against the schemas in [`schemas/`](../schemas/README.md) and the rules across records (unique names, `recipe:` cross-links). It runs on every pull request, and again before every publish.
- `build_bundle.py` packs the whole database into one gzipped JSON file.



## Getting the data

After every merge to `main` that touches the data, the [Publish dist bundle](../.github/workflows/dist.yml) workflow validates the records again and publishes them as a single file, `database.json.gz`, on the [`dist`](https://github.com/CodyCBakerPhD/comorecipes-database/tree/dist) branch. That branch is wiped and recreated each time, so it only ever holds the latest bundle. The site reads it at load; anything else can fetch it the same way:

```sh
curl -fsSL https://raw.githubusercontent.com/CodyCBakerPhD/comorecipes-database/dist/database.json.gz | gunzip > database.json
```

```python
import gzip
import json
import urllib.request

url = "https://raw.githubusercontent.com/CodyCBakerPhD/comorecipes-database/dist/database.json.gz"
with urllib.request.urlopen(url) as response:
    database = json.loads(gzip.decompress(response.read()))
```

The bundle holds every record exactly as parsed from its YAML, keyed by file stem, plus the commit it was built from:

```json
{
  "commit": "0123abc...",
  "generated_at": "2026-09-06T12:00:00+00:00",
  "recipes": {"marinara_sauce": {"name": "Marinara Sauce", "tags": ["..."], "measurements": ["..."], "instructions": ["..."]}},
  "ingredients": {"garlic": {"name": "garlic", "default_grams_per_package": 40.0, "default_package_unit": "heads"}}
}
```
