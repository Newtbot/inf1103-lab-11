from abc import ABC, abstractmethod


# Create an abstract DiscountStrategy class with one abstract method, apply(), 
# that takes an order total and
# returns the discounted total. Then create three strategies:

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass
