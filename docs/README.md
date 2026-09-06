# Recipes

One YAML file per recipe in [`recipes/`](../recipes), named by its stem (`marinara_sauce.yaml`), which is also the recipe's id on the site.

```yaml
name: Marinara Sauce

tags:
- Italian
- Sauce

measurements:
- amount: '76'
  unit: grams
  ingredient: extra virgin olive oil
- amount: '32'
  unit: grams
  prefix: minced
  ingredient: garlic

instructions:
- Heat the oil over medium heat.
- Add garlic and cook until golden.

notes:
- Optional free-form notes shown at the bottom of the page.
```

The 'ingredients' in high-level recipes are officially referred to as 'measurements' in the low-level API. Each measurement has an `amount` (a number, or `enough`), an optional `unit`, the `ingredient`, and optional `prefix`/`suffix` qualifiers ("minced", ", room temperature").

By convention, the ingredients of a recipe are listed in the order they are incorporated.

Ingredients are named in full, exactly as they should be bought and used: `unsalted butter`, `extra virgin olive oil`, `2% milk`, `granulated white sugar`. There is no shorthand for the reader to expand, so anything a name leaves out (`flour` where `all-purpose flour` is meant) really is unspecified.

Preparation is just as explicit: the `prefix` says how this recipe wants the ingredient (`minced garlic`, `chopped white onion`, `sliced white onion` where the recipe layers them), and anything that needs a step of its own is a step in `instructions`. There are no household defaults applied silently on top of what a recipe says.

The exact rules are in [`schemas/recipe.schema.json`](../schemas/recipe.schema.json).



## Recipes as ingredients

When an ingredient is another recipe (such as `marinara sauce` in Spaghetti), give the measurement a `recipe` key with that recipe's file stem. The site links the two pages both ways: the ingredient links to the component recipe, and the component recipe lists the recipes it is used in.

```yaml
- amount: '1'
  unit: portions
  ingredient: marinara sauce
  recipe: marinara_sauce
```

Links are only ever declared this way, never inferred from the ingredient name, so an ingredient that merely shares a recipe's name (the raw `celery` in Cornbread Dressing) stays a plain ingredient. Validation fails if the stem does not exist or names the recipe itself.
