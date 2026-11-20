from .discountStrategy import DiscountStrategy

class NoDiscount(DiscountStrategy):  
    def apply(self, total: float) -> float:  # 2. Fulfill the contract
        return total  