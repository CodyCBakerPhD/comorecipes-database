# CoMo Recipes Database

The collection of recipes for our household: one YAML file per recipe in `recipes/` and one per registered ingredient in `ingredients/`.

This repo is the source of truth for the data only. The [CoMo Recipes website](https://github.com/CodyCBakerPhD/comorecipes) is built from `main` here on a daily schedule, and trusts that every record has passed [validation](#validation).



## Format

Each recipe is a YAML file named by its stem (`marinara_sauce.yaml`), which is also the recipe's id on the site.

```yaml
name: Marinara Sauce

tags:
- Italian
- Sauce

measurements:
- amount: '76'
  unit: grams
  ingredient: olive oil
- amount: '32'
  unit: grams
  prefix: minced
  ingredient: garlic

instructions:
- Heat olive oil over medium heat.
- Add garlic and cook until golden.

notes:
- Optional free-form notes shown at the bottom of the page.
```

The 'ingredients' in high-level recipes are officially referred to as 'measurements' in the low-level API. Each measurement has an `amount` (a number, or `enough`), an optional `unit`, the `ingredient`, and optional `prefix`/`suffix` qualifiers ("minced", ", room temperature").

By convention, the ingredients of a recipe are listed in the order they are incorporated.

Registered ingredients in `ingredients/` carry the package defaults the desktop app uses, and may set `portions_text` to spell out how a `portions` unit of them reads on the site:

```yaml
name: garlic
default_grams_per_package: 40.0
default_package_unit: heads
```



### Recipes as ingredients

When an ingredient is another recipe (such as `marinara sauce` in Spaghetti), give the measurement a `recipe` key with that recipe's file stem. The site links the two pages both ways: the ingredient links to the component recipe, and the component recipe lists the recipes it is used in.

```yaml
- amount: '1'
  unit: portions
  ingredient: marinara sauce
  recipe: marinara_sauce
```

Links are only ever declared this way, never inferred from the ingredient name, so an ingredient that merely shares a recipe's name (the raw `celery` in Cornbread Dressing, the `rice` grain in Rice) stays a plain ingredient. The site build fails if the stem does not exist or names the recipe itself.



### Default references

There are several ingredients which are shortened for readability, but are expanded here for reference.

|      Default       |             Full name              |
|:------------------:|:----------------------------------:|
|       sugar        |       granulated white sugar       |
|       flour        |         all-purpose flour          |
|       butter       |          unsalted butter           |
|        milk        |              2% milk               |
|   condensed milk   |      sweetened condensed milk      |
|    brown sugar     |         light brown sugar          |
|      vanilla       |          vanilla extract           |
|      cinnamon      |          ground cinnamon           |
|        sage        |         dried ground sage          |
|       ginger       |        dried ground ginger         |
|      parsley       |        dried parsley flakes        |
|    fresh ginger    |         fresh ginger root          |
|       pepper       |        ground black pepper         |
|       yeast        |          active dry yeast          |
|     olive oil      |       extra virgin olive oil       |
|       cream        |            heavy cream             |
|       squash       |           yellow squash            |
|        rice        |             white rice             |
|     mushrooms      |   baby bella (button) mushrooms    |
|     chickpeas      |          dried chickpeas           |
|  crushed tomatoes  |  canned crushed tomatoes (28 oz.)  |
|    green beans     |         fresh green beans          |
|       onion        |            white onion             |



### Default practices

Onions and garlic will always be chopped.

Fresh tomatoes should be the ripest able to be purchased (usually from Costco), ideally garden grown.

Potatoes are always scrubbed thoroughly or peeled if necessary.



### Quality

All chocolate references assume the highest quality available, such as Ghirardelli.

All cocoa powders assume Dutch processed.

Vanilla extract is assumed to be pure, not synthetic.



## Validation

The shape of each record is defined by a JSON Schema in `schemas/`: [`recipe.schema.json`](schemas/recipe.schema.json) for `recipes/` and [`ingredient.schema.json`](schemas/ingredient.schema.json) for `ingredients/`. Every pull request runs the [Validate database](.github/workflows/validate_database.yml) workflow, which checks each file against its schema and then the rules a schema cannot express: file stems are lowercase snake_case, names are unique, and every `recipe:` cross-link points at a recipe that exists and is not the recipe itself.

To run the same check locally:

```sh
pip install pyyaml jsonschema
python scripts/validate_database.py
```

The site is built from whatever is on `main`, so once a change passes here it will show up on the site at its next scheduled deploy (daily), or sooner if the site's "Deploy site to gh-pages" workflow is run by hand from its Actions tab.
