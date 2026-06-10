# Day 02 — Mutable vs Immutable Types (continued)
**Phase 1 — Solid Python**
**Topics:** Strings, sets, frozensets, and consolidation

---

## 1. Strings

Strings are **immutable sequences**. Every "modification" produces a new object — the original is never touched.

```python
name = "joao"
print(id(name))       # some address

name = name.upper()
print(id(name))       # different address — new object, name rebound
```

The variable `name` was **rebound** to a new string object. `.upper()` did not modify `"joao"` — it returned a new string and `name` was rebound to it.

### String interning

CPython interns short strings that look like identifiers (letters, digits, underscores — no spaces). This is an **implementation detail**, not a language guarantee.

```python
a = "hello"
b = "hello"
print(a is b)   # True — CPython interned both to the same object

c = "hello world"
d = "hello world"
print(c is d)   # False (usually) — spaces break interning heuristics
```

**Rule:** always use `==` to compare string values. Never rely on `is` for strings.

### Common string methods

All return **new strings** — none modifies in place.

```python
s = "  Rato de Conves  "

s.strip()                        # "Rato de Conves"
s.lower()                        # "  rato de conves  "
s.upper()                        # "  RATO DE CONVES  "
s.replace("Conves", "Convés")    # returns new string
s.split()                        # ["Rato", "de", "Conves"]
"-".join(["Rato", "de", "Convés"])  # "Rato-de-Convés"
```

### f-strings

Standard string formatting since Python 3.6. Evaluated at runtime.

```python
batch = "B-001"
liters = 50.5

label = f"Batch {batch}: {liters}L"
label = f"Volume: {liters:.2f}L"       # 2 decimal places
label = f"Half batch: {liters / 2:.1f}L"  # expression inside braces
```

### Encoding

Python 3 strings are Unicode. Relevant when reading files or handling HTTP data.

```python
raw = "Cervejaria Rato de Convés"
encoded = raw.encode("utf-8")      # bytes: b'...Conv\xc3\xa9s'
decoded = encoded.decode("utf-8")  # back to str
```

---

## 2. Sets

A `set` is a **mutable, unordered collection of unique, hashable objects**.

```python
ingredients = {"hops", "malt", "yeast", "water"}
```

- **Unordered:** no guaranteed iteration order.
- **Unique:** duplicates silently ignored on construction and `.add()`.
- **Hashable elements only:** lists and dicts cannot be elements.

### Mutation operations

```python
ingredients = {"hops", "malt", "yeast"}

ingredients.add("water")       # adds element
ingredients.add("hops")        # no-op — already present
ingredients.discard("malt")    # removes if present; no error if absent
ingredients.remove("yeast")    # removes; raises KeyError if absent
popped = ingredients.pop()     # removes and returns an arbitrary element
```

### Set operations (return new sets)

```python
recipe_a = {"hops", "malt", "yeast", "water"}
recipe_b = {"hops", "corn", "yeast", "water"}

recipe_a | recipe_b    # union: all elements from both
recipe_a & recipe_b    # intersection: {"hops", "yeast", "water"}
recipe_a - recipe_b    # difference: {"malt"}
recipe_a ^ recipe_b    # symmetric difference: {"malt", "corn"}
```

Operator equivalents using methods (useful when working with non-set iterables or more than two sets):

```python
recipe_a.union(recipe_b)
recipe_a.intersection(recipe_b)
recipe_a.difference(recipe_b)
recipe_a.symmetric_difference(recipe_b)
```

### O(1) membership testing

`x in some_list` is O(n). `x in some_set` is O(1). Use sets when membership testing is the primary operation.

```python
# O(n) per check
valid_ids = [1, 2, 3, 4, 5]
result = [x for x in to_check if x in valid_ids]

# O(1) per check
valid_ids = {1, 2, 3, 4, 5}
result = [x for x in to_check if x in valid_ids]
```

---

## 3. frozenset

A `frozenset` is an **immutable set**. Supports all set operations (union, intersection, etc.) but has no mutation methods.

```python
base = frozenset({"hops", "malt", "yeast", "water"})
base.add("corn")    # AttributeError — no .add() on frozenset
```

Because frozensets are immutable, they are **hashable** — they can be used as dictionary keys or as elements of another set.

```python
recipe_map = {
    frozenset({"hops", "malt"}): "IPA",
    frozenset({"corn", "malt"}): "Lager",
}
```

---

## 4. Type summary

| Type | Mutable | Ordered | Unique | Hashable |
|------|---------|---------|--------|----------|
| `list` | Yes | Yes | No | No |
| `tuple` | No | Yes | No | Yes (if elements are) |
| `str` | No | Yes | No | Yes |
| `dict` | Yes | Yes (3.7+) | Keys unique | No |
| `set` | Yes | No | Yes | No |
| `frozenset` | No | No | Yes | Yes |

"Hashable" means the type can be used as a dict key or set element.

---

## 5. Mutable default argument — applies to all mutable types

The bug from Day 1 applies equally to sets and dicts.

```python
# Bug: set is created once at function definition time
def add_ingredient(name, recipe=set()):
    recipe.add(name)
    return recipe

r1 = add_ingredient("hops")
r2 = add_ingredient("malt")
print(r1 is r2)  # True — same object
```

Fix:

```python
def add_ingredient(name, recipe=None):
    if recipe is None:
        recipe = set()
    recipe.add(name)
    return recipe
```

Python evaluates default argument expressions **once at function definition time** and stores the resulting objects on the function itself (visible via `function.__defaults__`). Mutable defaults are shared across all calls that don't pass that argument explicitly.

---

## Exercises

### Exercise 1

Write `normalize_ingredient(name: str) -> str` that strips whitespace, lowercases, and replaces internal spaces with hyphens. No imports.

```python
# First attempt (correct, but verbose):
def normalize_ingredient(name: str) -> str:
    name = name.strip().lower()
    words = name.split()
    new_name = ""
    for word in words:
        if new_name == "":
            new_name = word
        else:
            new_name = "-".join([new_name, word])
    return new_name

# Idiomatic version:
def normalize_ingredient(name: str) -> str:
    return "-".join(name.strip().lower().split())
```

**Key point:** `"-".join(iterable)` already iterates internally. A manual accumulator loop is redundant when the built-in does the same job.

---

### Exercise 2

```python
a = "batch"
b = "batch"
c = "".join(["b", "a", "t", "c", "h"])

print(a == b)   # True  — same value
print(a is b)   # True  — CPython interned both literals at compile time
print(a == c)   # True  — same value
print(a is c)   # False — c built at runtime via join(); not interned
```

**Key point:** `a is b` is True because CPython interns string literals that look like identifiers at compile time — both `a` and `b` point to the same object from the start. `c` is produced at runtime by `join()`, so CPython creates a new object; same value, different identity.

---

### Exercise 3

```python
batch_alpha = {"hops", "malt", "yeast", "water", "coriander"}
batch_beta  = {"hops", "malt", "yeast", "water", "orange peel"}

common          = batch_alpha & batch_beta   # {"hops", "malt", "yeast", "water"}
unique_to_alpha = batch_alpha - batch_beta   # {"coriander"}
unique_to_beta  = batch_beta  - batch_alpha  # {"orange peel"}
all_ingredients = batch_alpha | batch_beta   # all five unique elements
```

---

### Exercise 4

```python
s1 = {"a", "b", "c"}
s2 = s1           # s2 is bound to the same object as s1
s2.add("d")       # mutates the shared object in place
print(s1)         # {"a", "b", "c", "d"} — s1 reflects the mutation
print(s1 is s2)   # True — one object, two names

fs  = frozenset(s1)
fs2 = frozenset(s1)
print(fs is fs2)  # False — two separate frozenset() calls, two objects
                  # (CPython may intern in practice, but not guaranteed)
print(fs == fs2)  # True  — same elements, equal by value
```

---

### Exercise 5

```python
# Bug: existing=set() is evaluated once at definition time.
# All calls without an explicit argument share the same set object.

# Fix:
def get_unique_batches(new_codes, existing=None):
    if existing is None:
        existing = set()
    for code in new_codes:
        existing.add(code.strip().upper())
    return existing

first_call  = get_unique_batches(["b-001", "b-002"])  # {"B-001", "B-002"}
second_call = get_unique_batches(["b-003"])            # {"B-003"}
```

**Root cause:** Python stores default argument objects on the function at definition time (`function.__defaults__`). A mutable default is shared across every call that doesn't pass the argument explicitly. Using `None` as the sentinel and constructing the mutable object inside the function body ensures a fresh object is created on each call.

---

## Key takeaways

- String methods return new objects — the original string is never modified. The variable is **rebound**, not the object mutated.
- Use `==` for string value comparison. `is` tests identity; interning is an implementation detail.
- Set membership testing is O(1). Prefer sets over lists when the primary operation is `x in collection`.
- `frozenset` is the immutable counterpart of `set`. It is hashable and can be used as a dict key.
- The mutable default argument bug applies to all mutable types: list, dict, set. The fix is always the same: default to `None`, construct inside the function body.