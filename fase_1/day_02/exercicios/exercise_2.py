a = "batch"
b = "batch"
c = "".join(["b", "a", "t", "c", "h"])

print(a == b)   # True bc they have the same value
print(a is b)   # True bc python reuses short strings that look like
# identifiers and therefore have the same id
print(a == c)   # True bc they have the same value
print(a is c)   # I thought it was going to be true but suspected it was false
# bc of the formation of the string
