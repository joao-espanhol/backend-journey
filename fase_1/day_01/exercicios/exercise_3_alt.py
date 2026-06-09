recipe = {"name": "Pale Ale", "ingredients": []}

print("Empty recipe: ", recipe)


def add_ingredient(ingredient, recipe=None):
    if recipe is None:
        recipe = {"ingredients": []}
    recipe["ingredients"].append(ingredient)
    return recipe


add_ingredient("hops", recipe)
add_ingredient("malt", recipe)
print(recipe)
