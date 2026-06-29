# Exercise 3. Rewrite your BrewSession (the version that releases the tank)
# as a generator-based context manager using @contextmanager. The yielded
# value should be the tank_id. Ensure the tank is released even if the body
# raises. Then answer: where, mechanically, does the exception from the body
# re-enter your generator function, and which keyword guarantees your release
# line still runs?
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