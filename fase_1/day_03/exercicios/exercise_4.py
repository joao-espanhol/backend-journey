class Beverage:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def descrever(self):
        raise NotImplementedError

    def calcular_imposto(self):
        raise NotImplementedError

class Beer(Beverage):
    def __init__(self, nome, preco, abv):
        super().__init__(nome, preco)
        self.abv = abv

    def descrever(self):
        # Your implementation
        return f"{self.nome} ({self.abv}% ABV)"

    def calcular_imposto(self):
        # Beer tax: 5% on base price
        return self.preco * 0.05

class Chopp(Beverage):
    def __init__(self, nome, preco, temperatura):
        super().__init__(nome, preco)
        self.temperatura = temperatura

    def descrever(self):
        # Your implementation
        return f"{self.nome} ({self.temperatura}°C)"

    def calcular_imposto(self):
        # Chopp tax: 8% on base price
        return self.preco * 0.08

# Usage:
bebidas = [
    Beer("Rato IPA", 100, 6.5),
    Chopp("Chopp Brahma", 150, 4),
    Beer("Rato Blonde", 90, 5.0)
]

for bebida in bebidas:
    print(f"{bebida.descrever()} — Imposto: R${bebida.calcular_imposto():.2f}")

# Expected output:
# Rato IPA (6.5% ABV) — Imposto: R$5.00
# Chopp Brahma (4°C) — Imposto: R$12.00
# Rato Blonde (5.0% ABV) — Imposto: R$4.50