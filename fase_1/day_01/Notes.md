# Day 1 — Phase 1: Solid Python
**Topic: Mutable vs Immutable Types**

---

## Theory

### 1. Identity vs Value

Before talking about mutability, you need to understand two distinct concepts Python separates: **identity** and **value**.

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)   # True  — same value
print(a is b)   # False — different objects in memory
```

`==` compares value. `is` compares identity — whether two names point to the exact same object. Use `id()` to see the actual memory address:

```python
print(id(a))  # e.g. 140234567890
print(id(b))  # different number
```

---

### 2. Immutable Types

An object is **immutable** if its value cannot change after creation. Python's immutable built-ins: `int`, `float`, `bool`, `str`, `tuple`, `frozenset`, `bytes`.

```python
x = 42
print(id(x))   # some address, say 9788416

x = x + 1     # this does NOT modify the object at 9788416
               # it creates a NEW int object (43) and rebinds x to it
print(id(x))   # different address
```

When you do `x += 1`, you are not changing `42` into `43`. You are making `x` point to a new object. The original `42` still exists in memory (Python caches small integers).

Strings behave the same way:

```python
s = "hello"
print(id(s))

s = s + " world"   # creates a NEW string object
print(id(s))        # different address
```

Every string "modification" creates a new object. This has performance implications — concatenating strings in a loop with `+` is O(n²). The correct approach is `"".join(list_of_strings)`.

Tuples are immutable sequences:

```python
t = (1, 2, 3)
t[0] = 99      # TypeError: 'tuple' object does not support item assignment
```

But there's a subtlety worth locking in:

```python
t = (1, [2, 3], 4)
t[1].append(99)    # this works
print(t)           # (1, [2, 3, 99], 4)
```

The tuple itself is immutable — you cannot reassign `t[1]`. But the list inside the tuple is still mutable, and the tuple only holds a reference to it. The tuple's content (the reference) didn't change; the object the reference points to did.

---

### 3. Mutable Types

An object is **mutable** if you can modify its content without creating a new object. Python's mutable built-ins: `list`, `dict`, `set`, `bytearray`, and most user-defined class instances.

```python
lst = [1, 2, 3]
print(id(lst))   # e.g. 140234999999

lst.append(4)
print(id(lst))   # SAME address — same object, modified in place
```

With mutable objects, multiple names can point to the same object, and a change through one name is visible through all others.

```python
a = [1, 2, 3]
b = a           # b points to the SAME list, not a copy

b.append(99)
print(a)        # [1, 2, 3, 99] — a is affected
print(a is b)   # True
```

The fix when you need an independent copy:

```python
b = a.copy()        # shallow copy
b = list(a)         # also shallow copy
b = a[:]            # also shallow copy

import copy
b = copy.deepcopy(a)  # deep copy — needed for nested structures
```

**Shallow vs deep copy:** a shallow copy creates a new outer container but the elements inside are still shared references. If your list contains other mutable objects (lists of lists, etc.), shallow copy is not enough.

```python
original = [[1, 2], [3, 4]]
shallow = original.copy()

shallow[0].append(99)
print(original)   # [[1, 2, 99], [3, 4]] — original is affected

import copy
deep = copy.deepcopy(original)
deep[0].append(0)
print(original)   # [[1, 2, 99], [3, 4]] — original is NOT affected
```

---

### 4. The Mutable Default Argument — diagnostic bug

This is one of the most famous Python footguns. The default value is created **once**, when the function is defined — not each time it is called.

```python
def add_item(item, items=[]):   # DEFAULT ARGUMENT IS EVALUATED ONCE
    items.append(item)
    return items

print(add_item("hop"))    # ['hop']
print(add_item("malt"))   # ['hop', 'malt']  ← not what you expected
print(add_item("water"))  # ['hop', 'malt', 'water']
```

The same list object is reused across all calls that don't pass an explicit `items` argument. The correct pattern:

```python
def add_item(item, items=None):
    if items is None:
        items = []          # new list created on EACH call that needs it
    items.append(item)
    return items

print(add_item("hop"))    # ['hop']
print(add_item("malt"))   # ['malt']   ← correct
```

**Rule: never use a mutable object as a default argument.** Use `None` as the sentinel and create the mutable object inside the function body. This applies to lists, dicts, sets — any mutable type.

You can inspect the bug yourself:

```python
def buggy(items=[]):
    items.append(1)
    return items

print(buggy.__defaults__)   # ([],) — before any call
buggy()
print(buggy.__defaults__)   # ([1],) — the default list was mutated
```

---

### 5. `+=` Behavior by Type

`+=` on a list calls `__iadd__`, which internally calls `list.extend()`. It modifies the existing object in place. On a tuple, since tuples are immutable, Python falls back to creating a new object and rebinding the name.

| Type | `+=` behavior | Same object? |
|------|--------------|--------------|
| `list` | mutates in place (`__iadd__` → `extend`) | Yes |
| `tuple` | creates new object, rebinds the name | No |

```python
# list
a = [1, 2, 3]
b = a
b += [4]
print(a is b)   # True — same object

# tuple
a = (1, 2, 3)
b = a
b += (4,)
print(a is b)   # False — b points to a new object
```

---

### 6. `dict` and `set` Mutability

Dicts and sets are mutable. The same aliasing behavior applies:

```python
recipe = {"name": "IPA", "hops": ["cascade", "centennial"]}
copy = recipe

copy["name"] = "Pale Ale"
print(recipe["name"])   # "Pale Ale" — same object

# Shallow copy of the dict:
copy2 = recipe.copy()   # or dict(recipe)
copy2["name"] = "Stout"
print(recipe["name"])   # "Pale Ale" — outer dict is independent

copy2["hops"].append("fuggles")
print(recipe["hops"])   # ["cascade", "centennial", "fuggles"] — inner list is shared
```

`frozenset` is the immutable counterpart to `set`. It's hashable (can be used as a dict key), `set` is not.

```python
fs = frozenset([1, 2, 3])
d = {fs: "this works"}

s = {1, 2, 3}
d = {s: "this fails"}   # TypeError: unhashable type: 'set'
```

---

### 7. Hashability

A **hash** is an integer computed from an object's value. Python uses it internally as a fast lookup key for dicts and sets — O(1) lookup instead of scanning every entry.

For this to work: **if two objects are equal, they must have the same hash.** A mutable object can't guarantee this across its lifetime, so Python refuses to hash it.

```python
hash([1, 2, 3])          # TypeError: unhashable type: 'list'
hash({1, 2, 3})          # TypeError: unhashable type: 'set'

hash((1, 2, 3))          # works — immutable
hash(frozenset([1, 2]))  # works — immutable
hash("hello")            # works
hash(42)                 # works

hash((1, [2, 3]))        # TypeError — tuple contains a mutable list
```

A tuple is only hashable if all its elements are hashable.

---

### 8. Design Principle: Mutating in Place

If a function's purpose is to mutate an object in place, the return value is usually noise. Storing it in a new variable actively misleads readers — it implies two independent objects when there's only one.

```python
# clear intent — mutates in place, no return needed
def add_ingredient(recipe, ingredient):
    recipe["ingredients"].append(ingredient)

pale_ale = {"name": "Pale Ale", "ingredients": []}
add_ingredient(pale_ale, "hops")
add_ingredient(pale_ale, "malt")
print(pale_ale)  # {"name": "Pale Ale", "ingredients": ["hops", "malt"]}
```

---

## Exercises

### Exercise 1

```python
a = [1, 2, 3]
b = a
b += [4]
print(a)
print(a is b)
```

**Output:**
```
[1, 2, 3, 4]
True
```

`+=` on a list calls `__iadd__` which extends the list in place. `b` and `a` still point to the same object.

---

### Exercise 2

```python
a = (1, 2, 3)
b = a
b += (4,)
print(a)
print(a is b)
```

**Output:**
```
(1, 2, 3)
False
```

Tuples are immutable. `+=` cannot extend in place, so Python creates a new object and rebinds `b` to it. `a` is unchanged.

---

### Exercise 3 — Fix the mutable default argument

**Buggy version:**
```python
def add_ingredient(ingredient, recipe={}):
    recipe[ingredient] = True
    return recipe
```

**Fixed version:**
```python
def add_ingredient(ingredient, recipe=None):
    if recipe is None:
        recipe = {}
    recipe[ingredient] = True
    return recipe

r1 = add_ingredient("hops")
r2 = add_ingredient("malt")
print(r1)   # {'hops': True}
print(r2)   # {'malt': True}
```

**Intentional in-place mutation (correct design for a recipe):**
```python
def add_ingredient(recipe, ingredient):
    recipe["ingredients"].append(ingredient)

pale_ale = {"name": "Pale Ale", "ingredients": []}
add_ingredient(pale_ale, "hops")
add_ingredient(pale_ale, "malt")
print(pale_ale)
```

---

### Exercise 4

```python
import copy


def safe_copy(data: list) -> list:
    return copy.deepcopy(data)


list1 = [1, 2, 3, 4]
list2 = safe_copy(list1)

list2.append(5)

print(list1)   # [1, 2, 3, 4]
print(list2)   # [1, 2, 3, 4, 5]
```

`deepcopy` recursively copies all nested objects. Modifying `list2` does not affect `list1`.

---

### Exercise 5

```python
import copy

# Case A — shallow copy
t = ([1, 2], [3, 4])
copy_t = list(t)
copy_t[0].append(99)
print(t)
# ([1, 2, 99], [3, 4])
# list(t) creates a new outer container but the inner lists are shared.
# copy_t[0] and t[0] point to the same list object.
# Appending through copy_t[0] is visible through t[0].
# The tuple is NOT broken — t still has 2 elements of type list.
# What changed is the content of the mutable list that t[0] points to.

# Case B — deep copy
t = ([1, 2], [3, 4])
deep = copy.deepcopy(t)
deep[0].append(99)
print(t)
# ([1, 2], [3, 4])
# deepcopy created independent copies of the inner lists.
# Modifying deep[0] has no effect on t[0].
```

---

## Key Rules to Memorize

- **Never use a mutable object as a default argument.** Use `None` + create inside the function.
- **`b = a` on a mutable object is aliasing, not copying.** Use `.copy()` or `deepcopy()`.
- **`+=` on a list mutates in place. `+=` on a tuple creates a new object.**
- **A tuple containing mutable objects is immutable in structure but not in content.**
- **Hashable = safe to use as a dict key or set member. Mutable types are not hashable.**
- **If a function mutates in place, don't return the object and store it in a new variable.**