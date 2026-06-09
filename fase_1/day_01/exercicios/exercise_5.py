import copy as cp

# Case A
t = ([1, 2], [3, 4])
copy = list(t)
copy[0].append(99)
print(t)
# ([1, 2, 99], [3, 4])

# Case B
t = ([1, 2], [3, 4])
deep = cp.deepcopy(t)
deep[0].append(99)
print(t)
# ([1, 2], [3, 4])
