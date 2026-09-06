# Schemas

The shape of each record is defined by a JSON Schema here: [`recipe.schema.json`](recipe.schema.json) for `recipes/` and [`ingredient.schema.json`](ingredient.schema.json) for `ingredients/`.

Every pull request runs the [Validate database](../.github/workflows/validate_database.yml) workflow, which checks each file against its schema and then the rules a schema cannot express: file stems are lowercase snake_case, names are unique, and every `recipe:` cross-link points at a recipe that exists and is not the recipe itself.

To run the same check locally, from the root of the repo:

```sh
pip install pyyaml jsonschema
python scripts/validate_database.py
```

Once a change is merged to `main` it is validated again and published as a single bundle for the site to read; see [`scripts/`](../scripts/README.md).
