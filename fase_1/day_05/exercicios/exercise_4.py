# Exercise 4 — The protocol by hand vs. the generator.
# Implement a class IngredientStock that holds a list of ingredient names
# and is iterable using __iter__ and __next__ directly (no generator, no
# yield). Then write a generator function that produces the same iteration
# behavior. In prose: state what the generator handled automatically that you
# had to write manually in the class — be specific about which methods and
# which piece of state.

class IngredientStock:
    def __init__(self, ingredient_list):
        self.ingredient_list = ingredient_list
        self.current = 0
        self.list_size = len(ingredient_list)

    def __iter__(self):
        return self                  # this object is its own iterator

    def __next__(self):
        if self.current >= self.list_size:
            raise StopIteration      # the signal that the loop is done
        value = self.ingredient_list[self.current]
        self.current += 1
        return value

def ingredient_stock(ingredient_list):
    current = 0
    list_size = len(ingredient_list)
    while current < list_size:
        value = ingredient_list[current]
        yield value
        current += 1

stock_1 = IngredientStock(["Ingredient 1", "Ingredient 2", "Ingredient 3", "Ingredient 4"])
ingredients_2 = ["Ingredient A", "Ingredient B", "Ingredient C", "Ingredient D"]
stock_2 = ingredient_stock(ingredients_2)

for ingredient in stock_1:
    print(ingredient)

for ingredient in stock_2:
    print(ingredient)

print(list(stock_1))
print(list(stock_2))