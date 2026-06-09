a = (1, 2, 3)  # creates a tuple
b = a  # b points to the same address as a
print(id(b))  # adress xxxxxx
print(id(a))  # adress xxxxxx
b += (4,)  # creates a new object
print("Id b: ", id(b))  # adress yyyyyy
print("Id a: ", id(a))  # adress xxxxxx
print(a)  # (1, 2, 3)
print(b)  # (1, 2, 3, 4)
print(a is b)  # False