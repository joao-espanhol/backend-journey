# Day 07 — Exceptions, Comprehensions, Type Hints

Phase 1 — Solid Python

## 1. Exceptions

### Hierarchy

Exceptions are objects. `except SomeClass` catches that class and every
subclass of it. Root is `BaseException`; almost everything relevant lives
under `Exception`. Never use a bare `except:` — it also catches
`SystemExit` and `KeyboardInterrupt`, breaking clean shutdown and Ctrl-C.

```
BaseException
 ├── SystemExit
 ├── KeyboardInterrupt
 ├── GeneratorExit
 └── Exception
      ├── ArithmeticError -> ZeroDivisionError
      ├── LookupError -> KeyError, IndexError
      ├── ValueError
      ├── TypeError
      └── OSError ...
```

### try / except / else / finally

- `try`: only the risky operation.
- `except SpecificClass`: most specific first; first match wins.
- `else`: runs only if `try` raised nothing — success-path logic goes
  here, not at the bottom of `try`, so an exception raised by the
  success logic itself isn't accidentally caught by `except`.
- `finally`: always runs — success, exception, or return.

### finally / __exit__ trap

Both `finally` and `__exit__` are guaranteed-execution blocks. If either
contains a `return`, it unconditionally **overrides** whatever the
protected code was about to produce — a normal return value or a
propagating exception — and does it **silently**, with no signal
anything was discarded. `return True` in `__exit__` (Day 6) and
`return -1.0` in `finally` are the same mechanism in two syntactic
forms.

```python
def commit_batch(raw_abv):
    try:
        abv = float(raw_abv)
        return abv
    finally:
        return -1.0   # always wins, success or failure alike
```

### The (exc_type, exc_value, traceback) triple

Python tracks three things for a live exception: the class, the
instance, and the traceback. `__exit__(exc_type, exc_value, traceback)`
receives exactly this triple as arguments — the same thing an
`except X as e` clause exposes as `X`, `e`, and `e.__traceback__`. When
no exception occurred, `__exit__` gets `(None, None, None)`.

### Custom exceptions and chaining

```python
class BreweryError(Exception):
    """Base for all brewery domain errors."""

class TankCapacityError(BreweryError):
    """Raised when the batch overflows the tank capacity."""

class InvalidABVError(BreweryError):
    """Raised when an ABV value is out of range or unparseable."""

def parse_abv(raw: str) -> float:
    try:
        return float(raw)
    except ValueError as e:
        raise InvalidABVError(f"bad ABV: {raw!r}") from e
```

`from e` sets `__cause__` — explicit, intentional chaining. Without
`from`, Python still records the original exception implicitly under
`__context__`. `from None` suppresses the chain when the original is
noise.

## 2. Comprehensions

```python
strong = [b["name"] for b in batches if b["abv"] >= 6.0]        # list
liters_by_name = {b["name"]: b["liters"] for b in batches}      # dict
styles = {b["style"] for b in batches}                          # set
total = sum(b["liters"] for b in batches)                       # genexp
pairs = [(tank, b["name"]) for tank in tanks for b in batches]  # nested
```

- `if` at the end of a comprehension = filter. Ternary at the front =
  transform (every item included, value chosen).
- Nested comprehension `for` clauses read outer-to-inner, exactly as
  nested loops would: the first `for` is the outer loop.
- Generator expressions are lazy — one element at a time, nothing
  materialized. Prefer them over list comprehensions when the result
  is consumed once by a function that walks it (`sum`, `any`, `all`,
  `min`, `max`, `join`, a `for` loop) — building the full list first
  just allocates memory for elements you immediately discard.
- Comprehension variables don't leak into the enclosing scope
  (Python 3).

## 3. Type hints (PEP 484) and mypy

Type hints are **not enforced at runtime** — they're stored in
`__annotations__` and otherwise ignored by the interpreter. A function
can violate its own annotation and still run without error:

```python
def check_liters(name: str | None = None) -> str:
    ...
    return b["liters"]   # int, not str — runs fine, mypy flags it
```

mypy is a separate static checker that reads annotations and reports
mismatches without executing the code:

```bash
pip install mypy --break-system-packages
mypy your_file.py
```

Errors are reported against mypy's *inferred* type, which may be
broader than what you intended (e.g. `object` instead of `int` when a
generator's yield type isn't pinned down).

`X | None` (3.10+) or `Optional[X]` means "an `X`, or `None`."