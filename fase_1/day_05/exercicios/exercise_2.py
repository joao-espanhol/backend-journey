# Exercise 2 — Decorator with arguments. Write retry(attempts) — a
# decorator that takes an integer attempts and re-runs the decorated
# function up to that many times if it raises an exception. It returns
# the result on the first success and re-raises the exception if every
# attempt fails. Apply it to a brewery function that might fail (e.g.
# a flaky inventory check that raises sometimes). In prose: explain what
# each of the three layers captures in its closure, and why @retry(attempts=3)
# calls retry before it decorates anything.

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
                    if i == attempts-1:
                        print(e)
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
        raise Exception("Estoque indisponível!")

    return "Estoque encontrado!"

try:
    print(verify_stock())
except Exception as e:
    print(e)
