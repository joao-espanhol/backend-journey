# Your Recipe class here
class Recipe:

    def __init__(self, name, style, abv):
        self.name = name
        self.style = style
        self.abv = abv

    def __str__(self):
        return f"Receita: {self.name} ({self.style}) ABV: {self.abv}"

    def __repr__(self):
        return f"Recipe(name={self.name!r}, style={self.style!r}, abv={self.abv!r})"

    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return False
        return self.name == other.name and self.style == other.style

    def __hash__(self):
        return hash((self.name, self.style))

# Usage:
receita1 = Recipe("Rato IPA", "IPA", abv=6.5)
receita2 = Recipe("Rato IPA", "IPA", abv=6.5)
receita3 = Recipe("Rato Blonde", "Blonde Ale", abv=5.0)

print(str(receita1))  # Should output something user-friendly
print(repr(receita1))  # Should output something like Recipe(nome='Rato IPA', ...)
print(receita1 == receita2)  # True (same data)
print(receita1 == receita3)  # False (different data)

# Should be able to use recipes in a set
recipes_set = {receita1, receita2, receita3}
print(len(recipes_set))  # 2 (receita1 and receita2 are equal)
