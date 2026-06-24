class Recipe:
    def __init__(self, nome, estilo, abv, volume_litros):
        self.nome = nome
        self.estilo = estilo
        self.abv = abv
        self.volume_litros = volume_litros

    def __str__(self):
        return f"Name: {self.nome}; Style: {self.estilo} (ABV {self.abv}%) - {self.volume_litros} L"

    def __repr__(self):
        return f"Recipe(nome={self.nome!r}, estilo={self.estilo!r}, abv={self.abv!r}, volume_litros={self.volume_litros!r})"

    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return NotImplemented
        return self.nome == other.nome and self.estilo == other.estilo

    def __hash__(self):
        return hash((self.nome, self.estilo))

class ProductionBatch:
    """A production batch of a recipe."""
    def __init__(self, receita, data_inicio):
        self.receita = receita
        self.data_inicio = data_inicio
        self._status = "planning"
        self._litros_produzidos = 0

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, novo_status):
        valid = ["planning", "fermenting", "finished"]
        if novo_status not in valid:
            raise ValueError(f"Invalid status: {novo_status!r}")
        if valid.index(novo_status) < valid.index(self._status):
            raise ValueError(f"Cannot transition from {self._status!r} to {novo_status!r}")
        self._status = novo_status


    @property
    def litros_produzidos(self):
        return self._litros_produzidos

    @litros_produzidos.setter
    def litros_produzidos(self, valor):
        # Validate: can't exceed recipe volume
        if valor > self.receita.volume_litros:
            raise ValueError("exceeds volume_litros")
        if valor <= 0:
            raise ValueError("negative")
        self._litros_produzidos = valor

    def info(self):
        # Return detailed info about the batch
        return f"{self.receita.nome}: {self.receita.volume_litros}: {self.status}: {self._litros_produzidos}L"

# Usage:
receita = Recipe("Rato IPA", "IPA", 6.5, 50)
lote = ProductionBatch(receita, "2026-06-10")

print(lote.info())
# Output: "Batch of Rato IPA: Planning stage, 0/50L produced"

lote.status = "fermenting"
lote.litros_produzidos = 48
print(lote.info())
# Output: "Batch of Rato IPA: Fermenting stage, 48/50L produced"