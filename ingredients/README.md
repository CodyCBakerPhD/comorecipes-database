# Ingredients

One YAML file per registered ingredient, named by its stem (`garlic.yaml`). Registered ingredients carry the package defaults the desktop app uses, and may set `portions_text` to spell out how a `portions` unit of them reads on the site:

```yaml
name: garlic
default_grams_per_package: 40.0
default_package_unit: heads
```

The `name` must match the ingredient exactly as recipes refer to it in their measurements. Most ingredients are not registered; only the ones that need package defaults or a portions label are.

The exact rules are in [`schemas/ingredient.schema.json`](../schemas/ingredient.schema.json).
