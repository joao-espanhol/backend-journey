# Day 05 — Decorators & Generators
**Phase 1 — Solid Python**

---

## Part 1 — Decorators

### Functions are objects

In Python, a function is an object. It has a value, can be bound to a name, passed as an argument, returned from another function, or stored in a container.

```python
def shout(text):
    return text.upper()

yell = shout        # two names, one object — no call happens
print(yell("hops")) # HOPS
```

The parentheses are what *call* the function. Without them, you're just referencing the object.

---

### Closures

A closure is an inner function that captures and remembers variables from the scope that defined it, even after that scope has finished executing.

```python
def make_multiplier(factor):
    def multiply(value):
        return value * factor   # factor comes from the enclosing scope
    return multiply

double = make_multiplier(2)
print(double(10))   # 20
```

When `make_multiplier(2)` returns, its local frame would be destroyed — but `multiply` references `factor`, so Python preserves it in a **cell object** attached to the returned function. You can inspect it: `double.__closure__` is a tuple of those cells.

The inner function carries its environment with it. That captured environment *is* the closure.

---

### The decorator

A decorator is a callable that takes a function and returns a function — almost always a new one that wraps the original.

```python
from functools import wraps

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper

@log_call
def brew(recipe):
    return f"Batch of {recipe} started"
```

`@log_call` is syntactic sugar for:

```python
brew = log_call(brew)
```

**Step by step:**
1. `log_call(brew)` runs, receives the original `brew` as `func`
2. Builds `wrapper`, which captures `func` in its closure
3. Returns `wrapper`
4. The name `brew` is rebound to `wrapper`
5. The original `brew` survives inside `wrapper.__closure__`

When you call `brew("IPA")`, you are calling `wrapper("IPA")`.

**Why `*args, **kwargs`?**
Makes `wrapper` transparent to any function signature. Without it, the wrapper only works for functions shaped exactly like its hard-coded parameters — applying it to a function with a different signature causes `TypeError`.

**Why `@wraps(func)`?**
Without it, after decoration `brew.__name__` is `"wrapper"` and `brew.__doc__` is `None`. That breaks `help()`, debuggers, and documentation tools. `@wraps` copies `__name__`, `__doc__`, `__qualname__`, `__module__` from the original onto `wrapper`, and stores the original at `wrapper.__wrapped__`.

**Key distinction:** `log_call` is the *factory* — it runs once during decoration and exits. `wrapper` is the *product* — it's what `brew` points to afterward. Confusing factory with product is the most common mental error with decorators.

---

### Decorators that take arguments

A decorator that takes arguments is a function that returns a decorator. Three layers.

```python
from functools import wraps

def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def ping():
    print("ping")
```

`@repeat(times=3)` calls `repeat` first, which returns `decorator`, which then decorates `ping`. Desugared:

```python
ping = repeat(times=3)(ping)
```

Each layer captures one thing in its closure:
- Outer (`repeat`): captures `times`
- Middle (`decorator`): captures `func`
- Inner (`wrapper`): does the work using both

---

## Part 2 — Generators

### The problem they solve

A normal function that builds a list materializes everything in memory before returning. For large or infinite sequences, that's wasteful or impossible. A generator produces values **lazily** — one at a time, on demand.

---

### `yield` and the suspended frame

A function containing `yield` is a *generator function*. Calling it returns a generator object without executing any of the body.

```python
def batch_numbers(start, count):
    n = start
    for _ in range(count):
        yield n     # emit value, then freeze the entire frame here
        n += 1
```

**The mechanism:**
- Each `next()` runs the body until it hits `yield`, emits the value, and **suspends the entire frame** — locals, loop counter, instruction pointer, all frozen
- The next `next()` resumes from that exact point
- When the body ends, Python raises `StopIteration`

A normal function's frame is destroyed on `return`. A generator's frame is parked between yields and resumed on demand.

---

### The iterator protocol

A `for` loop is sugar over a protocol:

1. `it = iter(obj)` → calls `obj.__iter__()`, returns an iterator
2. Repeatedly calls `next(it)` → calls `it.__next__()`
3. Stops when `__next__` raises `StopIteration`

**Iterable:** has `__iter__`
**Iterator:** has `__next__` (and an `__iter__` that returns itself)
**Generator object:** is an iterator — gets both methods automatically

**Manual implementation:**

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value
```

**Generator equivalent:**

```python
def countdown(start):
    while start > 0:
        yield start
        start -= 1
```

The generator handles automatically:
- `__iter__` and `__next__` methods
- State-keeping (replaces `self.current`)
- `StopIteration` signal

---

### Generator expressions

Like list comprehensions, but lazy:

```python
squares = (x * x for x in range(1_000_000))   # builds a generator; computes nothing yet
```

vs.

```python
squares = [x * x for x in range(1_000_000)]   # allocates 1M elements immediately
```

---

### The one-shot gotcha

A generator can be consumed **only once**. After exhaustion, iterating again yields nothing.

```python
codes = (f"RC-{i}" for i in range(3))
list(codes)   # ['RC-0', 'RC-1', 'RC-2']
list(codes)   # []  — frame is spent, nothing to resume
```

Once the body runs off the end, there is no suspended point left. The frame is gone.

---

## Exercises — Day 05

### Exercise 1 — Basic decorator

```python
from functools import wraps

def audit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling function {func.__name__}, with arguments {args} and {kwargs}")
        result = func(*args, **kwargs)
        print(f"Resulted: {result}")
        return result
    return wrapper

@audit
def register_sale(name, unit_value, quantity):
    return f"Selling {quantity} {name}s for ${unit_value*quantity}"

print(register_sale(name="IPA", unit_value=10.0, quantity=2))
```

---

### Exercise 2 — Decorator with arguments

```python
from functools import wraps

def retry(attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    if i == attempts - 1:
                        raise
        return wrapper
    return decorator

counter = 0

@retry(2)
def verify_stock():
    global counter
    counter += 1
    print(f"{counter} try")
    if counter < 3:
        raise Exception("Stock unavailable!")
    return "Stock found!"

try:
    print(verify_stock())
except Exception as e:
    print(e)
```

---

### Exercise 3 — Generator + exhaustion

```python
def batch_codes(prefix, count):
    i = 1
    while i <= count:
        yield f"{prefix}-{i}"
        i += 1

gen = batch_codes("IPA", 3)
print(list(gen))   # ['IPA-1', 'IPA-2', 'IPA-3']
print(list(gen))   # [] — frame is spent
```

---

### Exercise 4 — Protocol by hand vs. generator

```python
class IngredientStock:
    def __init__(self, ingredient_list):
        self.ingredient_list = ingredient_list
        self.current = 0
        self.list_size = len(ingredient_list)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.list_size:
            raise StopIteration
        value = self.ingredient_list[self.current]
        self.current += 1
        return value

def ingredient_stock(ingredient_list):
    current = 0
    list_size = len(ingredient_list)
    while current < list_size:
        yield ingredient_list[current]
        current += 1
```

The generator handled automatically: `__iter__`, `__next__`, the state variable (`self.current`), and `StopIteration`.

---

## Key distinctions to hold

| Term | What it means |
|---|---|
| Closure | Inner function that captures variables from its enclosing scope via cell objects |
| Encapsulation | OOP principle — grouping data and methods, controlling access |
| Factory | The outer decorator function; runs once during decoration |
| Product | The `wrapper`; what the original name points to after decoration |
| Iterable | Has `__iter__` |
| Iterator | Has `__next__` (and `__iter__` returning self) |
| Generator | An iterator that automates the protocol using `yield` |