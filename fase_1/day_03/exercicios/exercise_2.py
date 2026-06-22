class Beverage:
    """Base class for all beverages."""
    def __init__(self, nome, volume_litros):
        self.nome = nome
        self.volume_litros = volume_litros

    def info(self):
        return f"{self.nome}: {self.volume_litros}L"

class Beer(Beverage):
    """A beer with an ABV."""
    # Your code here
    def __init__(self, nome, volume_litros, abv):
        super().__init__(nome, volume_litros)
        self.abv = abv

    def info(self):
        base = super().info()
        return f"{base} - ABV {self.abv}"

class CraftBeer(Beer):
    """A craft beer with a brewery."""
    # Your code here
    def __init__(self, nome, volume_litros, abv, cervejaria):
        super().__init__(nome, volume_litros, abv)
        self.cervejaria = cervejaria

    def info(self):
        base = super().info()
        return f"{base} - By: {self.cervejaria}"

# Usage:
ipa = Beer("Rato IPA", 50, abv=6.5)
print(ipa.info())  # "Rato IPA: 50L — ABV 6.5%"

craft = CraftBeer("Rato Blonde", 30, abv=5.0, cervejaria="Rato de Convés")
print(craft.info())  # "Rato Blonde: 30L — ABV 5.0% — By: Rato de Convés"