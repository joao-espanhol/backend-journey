# Day 08 — Modules, Packages, Imports, `__all__`, `__name__`, pytest intro

**Phase 1 — Solid Python**

Central idea of the whole day: **a module is an object stored in a cache, keyed by a string name.** Almost every behavior below is a consequence of that single fact.

---

## 1. What a module actually is

A module is not "a file". It is a runtime object of type `module`; a `.py` file is one way to produce one. The object has a `__dict__` holding everything defined at the top level of the file.

What `import x` does the **first** time:

1. Look in `sys.modules` (dict cache of already-imported modules). If `x` is there → stop, use it.
2. If not, locate the source through the import machinery (finders searching `sys.path`).
3. Create a fresh, empty module object and **insert it into `sys.modules` before executing it**.
4. Execute the file top to bottom, in that module's own namespace. Every `def`, `class` and top-level statement runs *now*.
5. Bind the name in the importing namespace.

Consequences:

- Top-level code runs **once**, on the first import. Later imports short-circuit at step 1.
- Because the module object is cached *before* execution finishes (step 3), a circular import can hand you a **half-built module** — it exists, but some names are not defined yet. That is the mechanism behind `ImportError: cannot import name X` on circular dependencies.

```python
# recipes.py
print("Running recipes.py")          # top-level: runs on first import only

def start_recipe(recipe_name: str) -> None:
    print(f"Starting {recipe_name} recipe")
```

---

## 2. Import forms: execution vs. binding

Two separate things:

- **What code executes** — the entire target module, always, on first import.
- **What names get bound** — this is the only thing the import form changes.

```python
import brewery.recipes                       # executes recipes.py; binds 'brewery'
from brewery.recipes import calculate_abv    # executes recipes.py; binds 'calculate_abv'
from brewery import recipes as r             # executes recipes.py; binds 'r'
```

`from x import y` does **not** load "less" of the module. The whole file runs; you just receive a single name pointing into the result instead of the module object.

---

## 3. Packages and `__init__.py`

```
brewery/
    __init__.py       # runs when 'brewery' is first imported
    recipes.py
    inventory.py
```

A **regular package** is a directory with `__init__.py`. That file runs the first time the package is imported and *is* the package's module object. Empty is fine.

**Parent-first rule.** To import `brewery.recipes`, Python must import `brewery` first — the submodule is looked up as an attribute of an already-loaded package. So `brewery/__init__.py` always executes before any line of `recipes.py`, including under `python -m brewery.recipes`.

**Absolute vs. relative imports:**

```python
from brewery.recipes import calculate_abv   # absolute
from . import recipes                       # relative — resolves against __package__
```

A relative import only works when the module *has* a package context. Loaded as a loose script, `__package__` is empty → `ImportError: attempted relative import with no known parent package`.

Since PEP 420 a directory without `__init__.py` can still be a **namespace package**. For this course: use regular packages with an explicit `__init__.py`.

---

## 4. `sys.path[0]` — the rule behind most import errors

| Invocation | `sys.path[0]` is |
|---|---|
| `python inventory.py` | the **directory containing the script** |
| `python -m brewery.inventory` | the **current working directory** |

Practical trap encountered today: standing *inside* `brewery/` and running `python inventory.py`, then doing `from brewery import recipes` → `ModuleNotFoundError: No module named 'brewery'`. `sys.path[0]` is `.../brewery/`, and there is no `brewery` **inside** `brewery/`. The package is right there on disk and Python cannot see it, because you are standing inside it.

`cd ..` does not fix it: `python brewery/inventory.py` still keys off the *script's* directory. The fix is to stand in the directory that contains the package and use `-m`:

```bash
cd .../dia_08
python -m brewery.inventory
```

---

## 5. `__name__` and the `"__main__"` idiom

The **loader** assigns `__name__` — a module never names itself — and it does so at step 3, before the body executes. The same string is also the `sys.modules` key.

- Imported as a submodule → `__name__ == "brewery.recipes"`.
- Run as the entry point (`python -m brewery.recipes`) → `__name__ == "__main__"`.

```python
if __name__ == "__main__":
    start_recipe("Example")
```

This is a **plain runtime conditional**, not a special construct. During import the `if` statement *is executed* like any other top-level statement; `__name__` is `"brewery.recipes"`, the comparison evaluates to `False`, the body is skipped. Nothing is "skipped by the interpreter" — it is evaluated and found false.

### The cache-key traps

The `sys.modules` key depends on **how the file was reached**, and different keys mean **different module objects for the same file**:

- `import recipes` (found as a top-level module) keys it as `"recipes"`. A later `import brewery.recipes` misses the cache → the same file is loaded **a second time** as a distinct module object. Two sets of functions, two copies of any top-level state.
- `python -m brewery.recipes` stores the module under the key `"__main__"`, not `"brewery.recipes"`. Same consequence: a subsequent `import brewery.recipes` loads the file again.

Module-level singletons, registries and signal registration break exactly here.

---

## 6. `__all__`

`__all__` is a list of strings controlling **exactly one thing**: which names `from module import *` binds.

```python
__all__ = ["public_one", "public_two"]

def public_one(): ...
def public_two(): ...
def public_three(): ...   # public name, NOT in __all__
def _helper(): ...
```

- `from brewery.recipes import *` → binds only `public_one` and `public_two`.
- `public_three` is still reachable: `from brewery.recipes import public_three` works.
- `_helper` is still reachable: `from brewery.recipes import _helper` works.
- `__all__` blocks nothing. It does not hide, protect or restrict — it only curates the wildcard.

Without `__all__`, `import *` grabs every top-level name not starting with an underscore. That leading-underscore convention is the only "privacy" in Python, and it is a convention, not a rule.

---

## 7. pytest — introduction

### Discovery (convention-based)

Running `pytest` with no arguments walks the tree and collects:

- files named `test_*.py` or `*_test.py` (full filename pattern, including `.py`)
- functions named `test_*`
- classes named `Test*` (with no `__init__`), and `test_*` methods inside them

Names outside those patterns are invisible to pytest. The naming is not cosmetic.

### Execution, mechanically

pytest runs in phases:

1. **Collection** — establishes a rootdir, walks the tree, and for every matching file **imports it as a Python module**, using the same import machinery studied today (`sys.modules` cache included). This is why a test file must be importable, and why import errors surface as *collection errors* rather than test failures. From each imported module it gathers the objects matching the naming convention.
2. **Execution** — pytest calls each collected function with no arguments. The verdict comes from what the call does: returns normally → pass; raises `AssertionError` → fail; raises anything else → error. There is no special assertion protocol.
3. **Assertion rewriting** — happens at *import time*, during collection. pytest installs an import hook that rewrites the AST of test modules before compilation, replacing each bare `assert` with instrumented code capturing the operand values. That is why a failure prints `assert 5.2 == 5.25` with real values. Because it is applied at the import step, it only affects files pytest itself imports as test modules.

### Writing tests

```python
import pytest
from brewery.recipes import calculate_abv

def test_typical_batch():
    result = calculate_abv(1.050, 1.010)
    assert result == pytest.approx(5.25)

def test_zero_fermentation_gives_zero_abv():
    assert calculate_abv(1.050, 1.050) == 0.0

def test_invalid_gravity_raises():
    with pytest.raises(ValueError):
        calculate_abv(1.010, 1.050)
```

Commands:

```bash
pytest                                        # discovery from current directory
pytest -v                                     # per-test names
pytest tests/test_recipes.py::test_typical_batch   # one specific test
```

### `pytest.approx` — when floats need it and when they do not

- `1.050 - 1.010` is **not** `0.040` in binary floating point: neither operand is exactly representable, the subtraction lands slightly off, and `* 131.25` scales that error into the result → `approx` required.
- `1.050 - 1.050` is **exact**. Not because `1.050` is exact (it is not), but because subtracting a float from itself is exact regardless: identical bit patterns → difference exactly `0.0`. And `0.0 * 131.25` is exactly `0.0` → plain `==` is fine.

Rule: `==` is safe only when the arithmetic path is provably exact (self-subtraction, multiplication by zero, small integers held as floats). Everywhere else, `approx`.

### `pytest.raises` and `match`

`pytest.raises(ValueError)` asserts only the **exception type**. If a function raises `ValueError` from more than one guard, the test cannot tell which one fired — a refactor could make the wrong guard fire and the test would still pass.

```python
with pytest.raises(ValueError, match="negative"):
    calculate_abv(1.050, -1.000)
```

`match` runs a regex against the exception message. Use it whenever a function has more than one raise path of the same type.

---

## 8. Validation guard ordering

```python
def calculate_abv(original_gravity: float, final_gravity: float) -> float:
    # 1. Domain validation of each input, first
    if original_gravity < 0.0 or final_gravity < 0.0:
        raise ValueError("gravity readings cannot be negative")
    # 2. Relational validation, only after both inputs are known valid
    if final_gravity > original_gravity:
        raise ValueError("final gravity cannot exceed original gravity")
    return (original_gravity - final_gravity) * 131.25
```

With the guards in the reverse order, `calculate_abv(-2.0, -1.0)` raises *"final gravity cannot exceed original gravity"* — a false statement. The relation is fine; the inputs are not. A relational check only means something once both operands are known to be valid.

General rule: **validate the domain of each input first, then the relationship between them.** This carries directly into DRF serializer validation (field-level `validate_<field>` before object-level `validate`).

---

## Exercises

### Exercise 1 — Package structure and `__name__`
1. Create a package `brewery/` containing `__init__.py`, `recipes.py` and `inventory.py`.
2. In `recipes.py`, define one function and call it inside an `if __name__ == "__main__":` guard.
3. Explain what value Python assigns to `recipes.__name__` when (a) `inventory.py` does `from brewery import recipes`, and (b) you run `python -m brewery.recipes` — tracing *why*, referencing the load mechanism.
4. State what happens to a top-level statement placed *outside* the guard when `recipes` is imported, and explain why in terms of import execution.

### Exercise 2 — `__all__`
1. Define three functions with public names plus one helper named `_something`.
2. Define `__all__` exposing only two of the three public functions.
3. Predict which names `from brewery.recipes import *` binds; then state whether the excluded function and `_something` remain reachable by other import forms.
4. State precisely what `__all__` controls and what it does not.

### Exercise 3 — Import execution and caching
1. Add a top-level side effect at the top of `recipes.py`.
2. Write a script that imports `recipes` and also imports something *from* `recipes`, with a second module importing `recipes` too.
3. State how many times the side effect prints and name the mechanism responsible.
4. Contrast `import brewery.recipes` with `from brewery.recipes import calculate_abv`: what executes, what gets bound.

### Exercise 4 — pytest
1. Implement `calculate_abv(original_gravity, final_gravity) -> float` returning `(og - fg) * 131.25`, raising `ValueError` when `fg > og`.
2. Create a test file with a name pytest discovers, and explain why that name is required.
3. Write at least three tests: typical case, boundary case, and one asserting `ValueError` with `pytest.raises`.
4. Give the exact command and explain mechanically how pytest finds and executes the tests.

---

## Review

**Solid:** `__all__`; the caching mechanism (stated correctly on the first pass); execution vs. binding; pytest discovery.

**Carried forward:** `pytest.raises` without `match` — known but not yet used. Apply it in the Day 10 mini-project tests.

**Where this reappears:** Django app loading is this import mechanism at scale. `AppConfig.ready()` is a top-level-execution hook, and the "import once, get one object" guarantee is what makes signal registration work. Interview questions: "explain circular imports" (half-built module from cache-insert-before-execute) and "why did my module load twice" (two cache keys for one file).