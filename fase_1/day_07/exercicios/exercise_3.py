# Exercise 3 — Comprehensions

# List comprehension: names of batches with abv >= 6.0.
# Dict comprehension: name -> liters for all batches.
# Set comprehension: distinct style values.
# Generator expression: total liters across all batches, passed directly into sum().
# Explain why the generator expression in #4 is preferable to a list comprehension here.
# Nested comprehension: pair every tank name in tanks with every batch name in batches (a list of tuples).
# State which for clause in #6 is the outer loop, and why.

batches = [
    {"name": "Session IPA",      "abv": 4.2, "liters": 120, "style": "IPA"},
    {"name": "Rato Imperial",    "abv": 8.5, "liters": 60,  "style": "Stout"},
    {"name": "Convés Pilsen",    "abv": 4.8, "liters": 200, "style": "Pilsen"},
    {"name": "Maré Alta IPA",    "abv": 6.7, "liters": 90,  "style": "IPA"},
    {"name": "Porto Seguro",     "abv": 9.1, "liters": 40,  "style": "Stout"},
]

tanks = ["Tank A", "Tank B"]

strong = [b["name"] for b in batches if b["abv"] >= 6.0]

liters_by_name = {b["name"]: b["liters"] for b in batches}

styles = {b["style"] for b in batches}

total = sum(b["liters"] for b in batches)

pairs = [(tank, batch["name"])
    for tank in tanks
    for batch in batches]