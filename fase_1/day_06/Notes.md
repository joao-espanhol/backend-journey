# Day 06 — Context Managers
**Phase 1 — Solid Python**

---

## 1. What `with` actually does

`with EXPR as VAR` is a desugaring — not magic syntax. Python executes it as:

```python
mgr = EXPR
VAR = type(mgr).__enter__(mgr)
try:
    BODY
finally:
    type(mgr).__exit__(mgr, exc_type, exc_value, traceback)
```

**Three rules to lock in:**

1. `as VAR` binds the **return value of `__enter__`**, not the context manager itself.
2. Dunder methods are looked up on the **type**, not the instance.
3. `__exit__` runs in a `finally` — unconditionally, regardless of how the block exits.

---

## 2. Building a context manager by hand

```python
class BrewSession:
    def __init__(self, tank_id: str):
        self.tank_id = tank_id

    def __enter__(self):
        print(f"Acquiring tank {self.tank_id}")
        return self  # what `as` binds

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Releasing tank {self.tank_id}")
        if exc_type is not None:
            print(f"  Exception: {exc_type.__name__}: {exc_value}")
        return False  # do not suppress exceptions
```

---

## 3. The `__exit__` contract

`__exit__` receives three arguments:

| Argument    | Clean exit | Exception raised       |
|-------------|------------|------------------------|
| `exc_type`  | `None`     | Exception class        |
| `exc_value` | `None`     | Exception instance     |
| `traceback` | `None`     | Traceback object       |

**Return value controls exception suppression:**

- **Truthy** → exception is **swallowed**. Execution continues after the block.
- **Falsy** (including `None`) → exception **propagates** normally.

Returning `True` to silence an error you did not deliberately decide to handle is a bug.
The correct default: clean up, return `False`, let the caller deal with the failure.

---

## 4. `contextlib.contextmanager` — the synthesis bridge

Decorators + generators from Day 5 converge here.

```python
from contextlib import contextmanager

@contextmanager
def brew_session(tank_id):
    print(f"Acquiring tank {tank_id}")   # runs as __enter__
    try:
        yield tank_id                     # yielded value is what `as` binds
    finally:
        print(f"Releasing tank {tank_id}") # runs as __exit__
```

**How the machinery works:**

- `@contextmanager` is a decorator — a higher-order function that takes your generator
  function and returns a wrapper object with `__enter__` and `__exit__`.
- `__enter__` calls `next()` on the generator, running it up to the `yield`, and returns
  the yielded value.
- `__exit__` throws the body's exception *into* the generator at the `yield` point.
  The `finally` block catches the unwind and runs teardown.

**One yield rule:** the generator must yield exactly once.
Everything before `yield` is setup. Everything after is teardown.

---

## 5. Key distinctions

| Concept | What it is |
|---|---|
| Context manager | The object with `__enter__` / `__exit__` |
| Resource (`as` target) | The return value of `__enter__` — not necessarily the manager itself |
| `@contextmanager` | The decorator (factory) |
| The wrapper object it returns | The product used by `with` |

---

## Exercises

### Exercise 1 — `Timer` class

```python
import time

class Timer:
    def __enter__(self):
        self.start_time = time.perf_counter_ns()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.end_time = time.perf_counter_ns()
        self.elapsed_ms = (self.end_time - self.start_time) / 1_000_000
        return False

with Timer() as timer:
    time.sleep(0.5)

print("Elapsed time (ms):", timer.elapsed_ms)
```

`as` binds the return value of `__enter__` — here, `self`. To make `t` useful, store
information on the instance (e.g. `elapsed_ms`) so it can be read after the block ends.

**Note:** define attributes only where they first have a real value. `elapsed_ms` belongs
in `__exit__`, not in `__enter__` as a placeholder.

---

### Exercise 2 — Diagnosing `FileWriter`

```python
class FileWriter:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.f = open(self.path, "w")
        return self.f

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()
        return False  # fixed: was `return True`
```

**The bug:** `return True` in `__exit__` suppresses all exceptions unconditionally.
If the `with` body raises a `KeyError`, the file is closed, the exception is swallowed,
and execution continues silently — as if nothing went wrong. The caller never learns
about the failure.

**The fix:** return `False` (or nothing). The file is still closed; the exception propagates.

---

### Exercise 3 — `BrewSession` as a generator-based context manager

```python
from contextlib import contextmanager

@contextmanager
def brew_session(tank_id):
    print(f"Acquiring tank {tank_id}")
    try:
        yield tank_id
    finally:
        print(f"Releasing tank {tank_id}")

with brew_session(1) as tank:
    raise ValueError("Oops")
```

When the `with` body raises, `@contextmanager` throws the exception back into the
generator **at the `yield` statement**. The `finally` keyword guarantees the release
line runs whether the block exits cleanly or raises.

---

## Connection to Day 5

| Day 5 concept | How it appears in Day 6 |
|---|---|
| Generator / `yield` | The body of a `@contextmanager` function |
| Decorator as factory | `@contextmanager` wraps the generator function and returns a protocol-compliant object |
| Suspended frame | The generator pauses at `yield`; the `with` body runs in between |

---

## What appears in interviews

- "What does `with` desugar to?" — be able to write the `mgr/__enter__/try/finally/__exit__` skeleton.
- "What does `__exit__` return and why does it matter?" — truthy suppresses, falsy propagates.
- "How does `@contextmanager` work?" — `next()` to enter, exception thrown at `yield` to exit.
- "What does `as` bind to?" — the return value of `__enter__`, not the context manager.