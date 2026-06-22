class Batch:
    def __init__(self, recipe_nome, volume_inicial, litros_produzidos):
        self.recipe_nome = recipe_nome
        self.volume_inicial = volume_inicial
        self._litros_produzidos = litros_produzidos

    @property
    def litros_produzidos(self):
        # Your getter here
        return self._litros_produzidos

    @litros_produzidos.setter
    def litros_produzidos(self, valor):
        # Your setter here — validate that valor is positive
        # and doesn't exceed volume_inicial
        if valor > self.volume_inicial:
            raise ValueError("exceeds volume_inicial")
        if valor <= 0:
            raise ValueError("negative")
        self._litros_produzidos = valor

    @property
    def eficiencia(self):
        # Compute efficiency as produced / target * 100
        # Should be a read-only property (no setter)
        return 100*self._litros_produzidos / self.volume_inicial

# Usage:
lote = Batch("Rato IPA", 50, 45)
print(lote.litros_produzidos)  # 45
print(lote.eficiencia)  # 90.0

lote.litros_produzidos = 50  # OK
lote.litros_produzidos = 60  # Should raise ValueError (exceeds volume_inicial)
lote.litros_produzidos = -5  # Should raise ValueError (negative)