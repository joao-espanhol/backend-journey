def get_unique_batches(new_codes, existing=None):
    if existing is None:
        existing = set()
    for code in new_codes:
        existing.add(code.strip().upper())
    return existing


first_call = get_unique_batches(["b-001", "b-002"])
second_call = get_unique_batches(["b-003"])

print(first_call)   # expected: {"B-001", "B-002"}
print(second_call)  # expected: {"B-003"}
