import copy


def safe_copy(data: list) -> list:
    data2 = copy.deepcopy(data)
    return list(data2)


list1 = [1, 2, 3, 4]
list2 = safe_copy(list1)

list2.append(5)

print(list1)
print(list2)
