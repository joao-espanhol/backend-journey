def add_ingredient(ingredient, recipe=None):
    if recipe is None:
        recipe = {}
    recipe[ingredient] = True
    return recipe


r1 = add_ingredient("hops")
r2 = add_ingredient("malt")
print(r1)
print(r2)
