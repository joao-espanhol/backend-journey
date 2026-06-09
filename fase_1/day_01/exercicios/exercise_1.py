a = [1, 2, 3]  # create a list
b = a  # b points to the same object as a
b += [4]  # append 4 in the list
print(a)  # [1, 2, 3, 4]
print(a is b)  # returns true
