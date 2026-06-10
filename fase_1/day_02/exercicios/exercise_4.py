# s1 points to a set
s1 = {"a", "b", "c"}
# s2 points to the same set
s2 = s1
# the set expands and have a new item "d"
s2.add("d")
# The set is printed {"a", "b", "c", "d"}
print(s1)
# Prints True
print(s1 is s2)

# Creates a frozenset with the items of s1
fs = frozenset(s1)
# creates another frozenset with the items of s1
# Here, fs and fs2 points to diferent objects
fs2 = frozenset(s1)
# False
print(fs is fs2)
# True
print(fs == fs2)
