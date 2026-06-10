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


ingredient = "       Cascade Hops"
ingredient = normalize_ingredient(ingredient)

print(ingredient)
