
#PercentageDiscount – takes a percentage when created, 
# e.g. PercentageDiscount(10) takes 10% off

from .discountStrategy import DiscountStrategy

class PercentageDiscount(DiscountStrategy):
    def __init__(self, discount_percent: float):
        self.discount_percent = discount_percent  # Save it when created: PercentageDiscount(10)

    def apply(self, total: float) -> float:       # Matches the blueprint signature!
        discount_amount = total * (self.discount_percent / 100)
        return total - discount_amount