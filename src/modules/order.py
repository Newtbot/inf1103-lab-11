from src.modules.product import Product 
from src.modules.orderline import OrderLine
from src.payment.discountStrategy import DiscountStrategy
from src.payment.noDiscount import NoDiscount

class Order:
    def __init__(self, order_id: str, discount_strategy: DiscountStrategy | None = None) -> None:
        self._order_id: str = order_id
        self._order_lines: list[OrderLine] = []  
        self._discount_strategy: DiscountStrategy = discount_strategy or NoDiscount()

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        return self._order_lines

    def add_order_line(self, product: Product, quantity: int) -> None: 
        order_line = OrderLine(product, quantity)
        self._order_lines.append(order_line)

    #Add a set_discount() method so the strategy can be changed later.
    #calculate_total() adds up the order line subtotals and passes the result to the strategy’s apply() method.
    def set_discount(self, discount_strategy: DiscountStrategy | None) -> None:
        self._discount_strategy = discount_strategy or NoDiscount()        

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self._order_lines)
        return self._discount_strategy.apply(total)

