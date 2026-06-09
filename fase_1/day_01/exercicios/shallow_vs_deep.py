import copy

original = [[1, 2], [3, 4]]
shallow = original.copy()

# [[1, 2, 99], [3, 4]] — original is affected
# because shallow[0] and original[0] point to the same
# inner list
shallow[0].append(99)
print(original)

deep = copy.deepcopy(original)
deep[0].append(0)
print(original)   # [[1, 2, 99], [3, 4]] — original is NOT affected
print(deep)       # [[1, 2, 99, 0], [3, 4]] — deep is a completely separatecopy
