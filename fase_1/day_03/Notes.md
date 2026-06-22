# Day 03 — Object-Oriented Programming (OOP)
**Phase 1 — Solid Python**
**Backend Journey**

---

## Key Concepts

### Classes and Objects

A class is a blueprint. An object is an instance of that blueprint. Instance attributes live in `__dict__`. Python resolves attribute access by looking in the instance first, then the class hierarchy.

```python
class Cervejar:
    def __init__(self, nome, estilo, volume_litros):
        self.nome = nome
        self.estilo = estilo
        self.volume_litros = volume_litros

lote = Cervejar("Rato IPA", "IPA", 50)
print(lote.__dict__)
# {'nome': 'Rato IPA', 'estilo': 'IPA', 'volume_litros': 50}
```

---

### `__new__` vs `__init__`

- `__new__`: allocates memory for the object (rarely overridden)
- `__init__`: initializes the object after it's created

```python
class MyClass:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

    def __init__(self, value):
        self.value = value
```

---

### `__str__` and `__repr__`

- `__str__`: user-friendly string, called by `str()` and `print()`
- `__repr__`: developer-friendly string, called by `repr()` and the REPL

```python
class Recipe:
    def __init__(self, name, style, abv):
        self.name = name
        self.style = style
        self.abv = abv

    def __str__(self):
        return f"Receita: {self.name} ({self.style}) ABV: {self.abv}"

    def __repr__(self):
        return f"Recipe(name={self.name!r}, style={self.style!r}, abv={self.abv!r})"
```

---

### `__eq__` and `__hash__`

**Rule: if you override `__eq__`, you must override `__hash__`.**

- `__eq__`: defines value-based equality
- `__hash__`: must be consistent with `__eq__` — equal objects must hash identically

```python
class Recipe:
    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return False
        return self.name == other.name and self.style == other.style

    def __hash__(self):
        return hash((self.name, self.style))
```

Without `__hash__`, objects that override `__eq__` become unhashable and cannot be used in sets or as dict keys.

---

### Inheritance and MRO

Each subclass calls `super().__init__()` to delegate upward. Python resolves method calls using the MRO (C3 linearization).

```python
class Beverage:
    def __init__(self, nome, volume_litros):
        self.nome = nome
        self.volume_litros = volume_litros

    def info(self):
        return f"{self.nome}: {self.volume_litros}L"

class Beer(Beverage):
    def __init__(self, nome, volume_litros, abv):
        super().__init__(nome, volume_litros)
        self.abv = abv

    def info(self):
        base = super().info()
        return f"{base} - ABV {self.abv}"

class CraftBeer(Beer):
    def __init__(self, nome, volume_litros, abv, cervejaria):
        super().__init__(nome, volume_litros, abv)
        self.cervejaria = cervejaria

    def info(self):
        base = super().info()
        return f"{base} - By: {self.cervejaria}"

print(CraftBeer.__mro__)
# (<class 'CraftBeer'>, <class 'Beer'>, <class 'Beverage'>, <class 'object'>)
```

---

### Encapsulation Conventions

- `public_attr`: freely accessible
- `_protected_attr`: internal use / subclasses (convention only)
- `__private_attr`: name-mangled to `_ClassName__attr` (rarely needed)

---

### Properties

`@property` exposes a method as an attribute. Use it to validate, compute, or control access to internal state.

```python
class Batch:
    def __init__(self, volume_inicial, litros_produzidos):
        self.volume_inicial = volume_inicial
        self._litros_produzidos = litros_produzidos  # bypasses setter

    @property
    def litros_produzidos(self):
        return self._litros_produzidos

    @litros_produzidos.setter
    def litros_produzidos(self, valor):
        if valor <= 0:
            raise ValueError("Value must be positive")
        if valor > self.volume_inicial:
            raise ValueError("Exceeds volume_inicial")
        self._litros_produzidos = valor

    @property
    def eficiencia(self):
        # Read-only: no setter defined
        return 100 * self._litros_produzidos / self.volume_inicial
```

**Watch out:** assigning directly to the private attribute in `__init__` bypasses the setter. To run validation at construction, use `self.litros_produzidos = litros_produzidos` (no underscore).

---

### Polymorphism

Different types respond to the same method call in their own way. No type-checking needed.

```python
class Beverage:
    def descrever(self):
        raise NotImplementedError  # or use ABC

class Beer(Beverage):
    def descrever(self):
        return "Cerveja gelada"

class Chopp(Beverage):
    def descrever(self):
        return "Chopp da torneira"

bebidas = [Beer(), Chopp()]
for b in bebidas:
    print(b.descrever())
```

**Professional pattern:** use `abc.ABC` and `@abstractmethod` to prevent instantiation of the base class:

```python
from abc import ABC, abstractmethod

class Beverage(ABC):
    @abstractmethod
    def descrever(self):
        pass
```

---

## Common Mistakes

| Mistake | Correct behavior |
|---|---|
| Overriding `__eq__` without `__hash__` | Always override both together |
| Setting `self._attr` in `__init__` when you want validation | Use `self.attr` to route through the property setter |
| `valor < 0` when you mean "must be positive" | Use `valor <= 0` — zero is not positive |
| `NotImplementedError` in base class | Fine for simple cases; prefer `ABC` + `@abstractmethod` in production |

---

## Market Relevance

- Django models use `__str__` to display instances in the admin panel
- Django CBVs are class hierarchies — inheritance with `super()` is everywhere
- DRF serializers and views are abstract base classes
- Properties appear in Django models for computed fields
- `__eq__` and `__hash__` matter when using model instances in sets or as cache keys