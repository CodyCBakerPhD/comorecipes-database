# Schemas

The shape of each record is defined by a JSON Schema here: [`recipe.schema.json`](recipe.schema.json) for `recipes/` and [`ingredient.schema.json`](ingredient.schema.json) for `ingredients/`.

Every pull request runs the [Validate database](../.github/workflows/validate_database.yml) workflow, which checks each file against its schema and then the rules a schema cannot express: file stems are lowercase snake_case, names are unique, and every `recipe:` cross-link points at a recipe that exists and is not the recipe itself.

To run the same check locally, from the root of the repo:

```sh
pip install pyyaml jsonschema
python scripts/validate_database.py
```

The site is built from whatever is on `main`, so once a change passes here it will show up on the site at its next scheduled deploy (daily), or sooner if the site's "Deploy site to gh-pages" workflow is run by hand from its Actions tab.
