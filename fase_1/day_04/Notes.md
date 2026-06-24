# Day 04 — Advanced OOP: classmethod, staticmethod, ABC, dataclasses

**Phase 1 — Solid Python**
Topics: `@classmethod`, `@staticmethod`, Abstract Base Classes (`abc.ABC` + `@abstractmethod`), `@dataclass` (`field(default_factory=...)`, `frozen=True`).

---

## 1. Method types — what gets passed as the implicit first argument

The three method kinds differ only in what Python passes in as the first argument.

| Kind | First arg | Receives | Typical use |
|------|-----------|----------|-------------|
| Instance method | `self` | the object | logic needing this object's data |
| `@classmethod` | `cls` | the class | alternative constructors |
| `@staticmethod` | — | nothing | logic that belongs in the class but touches no state |

### `@classmethod` — alternative constructor

```python
class Batch:
    def __init__(self, recipe_name, volume_liters):
        self.recipe_name = recipe_name
        self.volume_liters = volume_liters

    @classmethod
    def from_dict(cls, data):
        """Build a Batch from a dict with keys 'recipe_name' and 'volume_liters'."""
        # cls, not Batch: a subclass calling from_dict gets its own type back.
        # Hard-coding Batch(...) would downgrade every subclass to a plain Batch.
        return cls(data["recipe_name"], data["volume_liters"])
```

**Why `cls` and not `Batch`:** if `SourBatch(Batch)` inherits `from_dict` and you call
`SourBatch.from_dict(...)`, then `cls` is `SourBatch`, so you get a `SourBatch` back.
Hard-coding `Batch(...)` would always build a plain `Batch`, ignoring the subclass —
and any subclass-specific method would then fail with `AttributeError`.

### `@staticmethod` — no instance, no class

```python
    @staticmethod
    def is_valid_volume(liters):
        # staticmethod: depends only on its arguments, holds no reference
        # to instance or class state.
        return 0 < liters <= 1000
```

**Reject-range vs accept-range logic (trap):**
- Rejecting values *outside* a range → join the two failure conditions with `or`
  (`liters <= 0 or liters > 1000`).
- Accepting values *inside* a range → join with `and`, or use a chained comparison
  (`0 < liters <= 1000`). The `and` is built into the chain.

---

## 2. Abstract Base Classes — enforcement at instantiation time

Day 3 used a *regular class* with `raise NotImplementedError`. The error fires at
**call time** — the object builds fine and fails later, possibly far from the mistake.

`ABC` + `@abstractmethod` moves enforcement to **instantiation time** — the object
cannot be built at all.

```python
from abc import ABC, abstractmethod

class Fermenter(ABC):
    @abstractmethod
    def target_temperature(self): ...

class AleFermenter(Fermenter):
    def target_temperature(self):
        return "18°C - 22°C"

class LagerFermenter(Fermenter):
    def target_temperature(self):
        return "8°C - 12°C"

# Fermenter() raises TypeError at instantiation: it inherits from ABC and has
# an unimplemented @abstractmethod, so it can never be constructed. A subclass
# that fails to implement all abstractmethods also can't be instantiated.
# Contrast with Day 3's regular class + raise NotImplementedError, where the
# error fires only when the method is called.
```

To show the failure without crashing a clean file:

```python
try:
    broken = Fermenter()
except TypeError as e:
    print(f"Cannot instantiate: {e}")
```

Abstract property syntax (order matters — `@property` on top):

```python
class Fermenter(ABC):
    @property
    @abstractmethod
    def target_temp(self): ...
```

---

## 3. Dataclasses

`@dataclass` auto-generates `__init__`, `__repr__`, `__eq__` from annotated fields.
Type annotations are **mandatory** — the machinery reads them to discover fields.

```python
from dataclasses import dataclass, field

@dataclass
class Ingredient:
    name: str
    quantity_kg: float
    cost_per_kg: float
```

### The Day 1 mutable-default bug, in dataclass costume

```python
@dataclass
class Recipe:
    name: str
    style: str
    hops: list = field(default_factory=list)   # correct
    # If written `hops: list = []`, @dataclass would generate an __init__ with a
    # mutable default parameter: def __init__(self, ..., hops=[]). That [] is
    # evaluated ONCE, when __init__ is defined — producing a single list object
    # shared by every Recipe created without explicit hops. This is the Day 1
    # Mutable Default Argument bug: a hop appended to recipe_a then silently
    # appears in recipe_b. default_factory=list instead calls list() fresh on
    # every instantiation, so each instance gets its own independent list.
```

**Three distinct things — keep them separate:**
- `@dataclass` — the decorator; generates the dunder methods.
- `field(...)` — configures one field when bare `name: type = default` isn't enough.
- `default_factory` — an argument to `field()`; a callable invoked fresh per
  instantiation to build that field's default. Pass `list`, not `list()` or `[]`.

### `frozen=True` — immutability and hashability

```python
@dataclass(frozen=True)
class HopAddition:
    name: str
    grams: float
    minutes: int

first_hop = HopAddition("simcoe", 20.3, 0)
second_hop = HopAddition("amarillo", 18.0, 30)
hop_set = {first_hop, second_hop}   # works — frozen instances are hashable

# first_hop.grams = 21.1  -> raises FrozenInstanceError
```

**Why a frozen dataclass can go in a set (the chain):**

`frozen=True` → attributes can't change after construction → hash is guaranteed
stable for the object's lifetime → Python generates a `__hash__` → the object is
hashable → the `set` can compute its bucket → it can be a set member.

A *normal* (mutable) dataclass has `__hash__` set to `None` and raises `TypeError`
when added to a set. This is the same `__hash__`/`__eq__` contract done by hand on
Day 3 (equal objects hash equal; hash derived from stable fields) — `frozen=True`
earns the right to generate `__hash__` *because* it guarantees the fields won't move.

### When a dataclass is the wrong tool

Dataclasses fit objects that are **primarily data**. Poor fit when the class is
primarily **behavior** — rich method logic, complex `__init__` invariants, heavy
inheritance. If you're overriding most generated methods, use a normal class.

---

## Watch points carried into Day 5

- **Conclusion vs mechanism:** state the *cause*, not just the *outcome*. Every
  outcome statement should be followed by "why?" — that's where interview follow-ups
  live.
- Keep `@dataclass` / `field()` / `default_factory` distinct.
- Comment indentation: comments sit at the indentation level of the code they
  describe, inside the relevant block.