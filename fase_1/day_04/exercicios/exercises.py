from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Batch:
    def __init__(self, recipe_name, volume_liters):
        self.recipe_name = recipe_name
        self.volume_liters = volume_liters

    @classmethod
    def from_dict(cls, data):
        """Build a Batch from a dict with keys recipe_name and volume_liters"""
        return cls(data["recipe_name"], data["volume_liters"])
        # Here I used cls because if Batch(...) was used, the subclasses from
        # Batch wasn't going to be able to use the class from_dict receiving
        # their classes as an argument. The class is always going to be Batch, no
        # matter what subclass calls it

    @staticmethod
    def is_valid_volume(liters):
        if liters <= 0 or liters > 1000:
            return False
        return True
        # This is an staticmethod because it doesn't interact with the class,
        # depending only on its arguments and holds no reference to
        # the instance or class


rato_ipa = {"recipe_name": "Rato IPA", "volume_liters": 50}
batch = Batch.from_dict(rato_ipa)

print(type(batch))


class Fermenter(ABC):
    @abstractmethod
    def target_temperature(self): ...


class AleFermenter(Fermenter):
    def target_temperature(self):
        return "18°C - 22°C"


class LagerFermenter(Fermenter):
    def target_temperature(self):
        return "8°C - 12°C"


ale_fermenter = AleFermenter()
print(ale_fermenter.target_temperature())
lager_fermenter = LagerFermenter()
print(lager_fermenter.target_temperature())
# broken = Fermenter()
# The code breaks because Fermenter cannot be instantiated, it inherits
# from ABC and has an unimplemented @abstractmethod. Btw, a subclass of an
# Abstract Class cannot be instanciated without implementing all
# of the abstractmethods. Besides that, the error fires at instantiation,
# in contrast with the regular class with the raise NotImplementedError from
# the previous classes, where the error fires when the method is called

@dataclass
class Recipe:
    name: str
    style: str
    hops: list = field(default_factory=list)
    # If written as `hops: list = []`, the default list would be evaluated ONCE,
    # when __init__ is defined — producing a single list object shared by every
    # Recipe created without explicit hops. This is the Day 1 Mutable Default
    # Argument bug: appending to one recipe's hops mutates that one shared list,
    # so a hop added to recipe_a silently appears in recipe_b. default_factory
    # instead calls list() fresh on each instantiation, giving every instance
    # its own independent list.

@dataclass(frozen=True)
class HopAddition:
    name: str
    grams: float
    minutes: int

first_hop = HopAddition("simcoe", 20.3, 0)
second_hop = HopAddition("amarillo", 18.0, 30)

hop_set = {first_hop, second_hop}

# first_hop.grams = 21.1
# frozen=True → attributes can't change after construction → hash is guaranteed
# stable → Python generates a __hash__ → the object is hashable → the set can
# compute its bucket → it can be a set member.