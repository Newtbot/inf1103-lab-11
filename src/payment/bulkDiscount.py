# BulkDiscount – takes a threshold and an amount,
#  e.g. BulkDiscount(200, 20) takes 20 off any total of 200 or more

from .discountStrategy import DiscountStrategy

class BulkDiscount(DiscountStrategy): 
    def __init__(self, threshold: float, amount: float):
        self.threshold = threshold
        self.amount = amount

    def apply(self, total: float) -> float: 
        if total >= self.threshold: 
            return max(0.0, total - self.amount)  # max() prevents negative prices
        return total