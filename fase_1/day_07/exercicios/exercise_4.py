# Write total_liters(batches: list[dict]) -> float that sums the liters field across the batch list (you can reuse the batches data from Exercise 3).
# Write a second function that takes at least one parameter typed X | None (your choice of X — e.g. an optional filter on style).
# Write a third function whose body deliberately violates its own return type annotation — e.g. annotated -> float but actually returns a str.
# Run mypy on the file. Report what mypy outputs for the function in #3.
# Fix the function in #3 so it satisfies its annotation.
# Explain why the broken version from #3 ran without error when you executed it in plain Python, despite mypy flagging it.

batches = [
    {"name": "Session IPA",      "abv": 4.2, "liters": 120, "style": "IPA"},
    {"name": "Rato Imperial",    "abv": 8.5, "liters": 60,  "style": "Stout"},
    {"name": "Convés Pilsen",    "abv": 4.8, "liters": 200, "style": "Pilsen"},
    {"name": "Maré Alta IPA",    "abv": 6.7, "liters": 90,  "style": "IPA"},
    {"name": "Porto Seguro",     "abv": 9.1, "liters": 40,  "style": "Stout"},
]

tanks = ["Tank A", "Tank B"]

def total_liters(batches: list[dict]) -> float:
    liters = sum(b["liters"] for b in batches)
    return liters

def check_abv(batch_name: str | None = None):
    if batch_name is not None:
        return next(
            (b["abv"] for b in batches if b["name"] == batch_name),
            None
        )
    else:
        return None

#def check_liters(batch_name: str | None = None) -> str:
    if batch_name is not None:
        return next(
            (b["liters"] for b in batches if b["name"] == batch_name),
            None
        )
    else:
        return None

def check_liters_fixed(batch_name: str | None = None) -> float:
    if batch_name is not None:
        return next(
            (b["liters"] for b in batches if b["name"] == batch_name),
            -1.0
        )
    else:
        return -1.0

print(check_abv("Porto Seguro"))
#print(check_liters("Porto Seguros"))