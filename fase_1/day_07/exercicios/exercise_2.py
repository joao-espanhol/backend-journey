def commit_batch(raw_abv):
    try:
        abv = float(raw_abv)
    except ValueError:
        print(f"could not parse ABV from {raw_abv!r}")
        raise
    else:
        return abv
    finally:
        print("commit_batch finished")

def commit_batch_2(raw_abv):
    try:
        abv = float(raw_abv)
        return abv
    finally:
        return -1.0

class InvalidABVError(Exception):
    """Raised when an ABV value is out of range or unparseable"""

def parse_abv(raw: str) -> float:
    try:
        abv = float(raw)
    except ValueError as e:
        raise InvalidABVError(f"bad ABV: {raw!r}") from e
    else:
        return abv
    finally:
        print("commit_batch finished")