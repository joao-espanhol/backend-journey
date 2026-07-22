print("Running recipes.py")

__all__ = ["public_one", "public_two"]

def start_recipe(recipe_name: str) -> None:
    print(f"Starting {recipe_name} recipe")


def public_one(): pass
def public_two(): pass
def public_three(): pass
def _helper(): pass

def calculate_abv(original_gravity: float, final_gravity: float) -> float:
    if final_gravity > original_gravity:
        raise ValueError("final gravity cannot exceed original gravity")
    if final_gravity < 0.0 or original_gravity < 0.0:
        raise ValueError("Fg or OG cannot be less than 0")
    return (original_gravity - final_gravity) * 131.25

if __name__ == "__main__":
    start_recipe("Example")