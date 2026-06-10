batch_alpha = {"hops", "malt", "yeast", "water", "coriander"}
batch_beta = {"hops", "malt", "yeast", "water", "orange peel"}

common = batch_beta & batch_alpha
print(common)
unique_to_alpha = batch_alpha - batch_beta
print(unique_to_alpha)
unique_to_beta = batch_beta - batch_alpha
print(unique_to_beta)
all_ingredients = batch_alpha | batch_beta
print(all_ingredients)
