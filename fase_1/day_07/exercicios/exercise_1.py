# Define BreweryError(Exception) and two subclasses: TankCapacityError and
# InvalidABVError. Write add_batch_to_tank(current_liters, capacity,
# batch_liters) that raises TankCapacityError when the batch would overflow
# the tank, and otherwise returns the new total. Then write a caller that uses
# all four of try / except / else / finally. In your explanation, justify
# specifically why the success-path logic belongs in else rather than at
# the bottom of try.

class BreweryError(Exception):
    """Base for all brewery domain errors."""

class TankCapacityError(BreweryError):
    """Raised when the batch overflows the tank capacity"""

class InvalidABVError(BreweryError):
    """Raised when an ABV value is out of range or unparseable"""

def batch_to_tank(current_liters, capacity, batch_liters):
    if (current_liters + batch_liters) > capacity:
        raise TankCapacityError("The batch overflows the tank")
    else:
        print("Batch added to the tank")
        total_liters = current_liters + batch_liters
        return total_liters

def caller():
    current_liters = 5
    capacity = 10
    batch_liters = 5
    try:
        batch_to_tank(current_liters, capacity, batch_liters)
    except TankCapacityError:
        print("There is no capacity in the tank")
        raise
    else:
        print("Racking the batch")
        return
    finally:
        print("Batch racked")

racking = caller()