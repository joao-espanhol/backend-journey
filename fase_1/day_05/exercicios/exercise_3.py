# Exercise 3 — Generator + exhaustion.
# Write a generator function batch_codes(prefix, count) that lazily
# yields batch codes like "IPA-001", "IPA-002", … up to count. Then,
# before running it, predict in writing what this prints and why,
# at the frame level:

def batch_codes(prefix, count):
    i = 1
    while i <= count:
        yield f"{prefix}-{i}"
        i += 1

x = 5
batches = batch_codes("IPA", x)
for _ in range(x):
    print(next(batches))

print(list(batches))

gen = batch_codes("IPA", 3)
print(list(gen))
print(list(gen))