# Exercise 1 — Write a basic decorator. Write a decorator audit that,
# when applied to a function, prints the function's name and the arguments
# it was called with before the call, then prints the return value after.
# Preserve the wrapped function's metadata. Apply it to a brewery function
# of your choice (e.g. one that registers a sale). In your submission,
# answer two questions in prose: why *args, **kwargs in the wrapper,
# and why @wraps — at the level of what specifically breaks without each.

from functools import wraps

def audit(func):
    #@wraps(func)
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