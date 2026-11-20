#only handle product obj?
# - __product_id:String
# - __name:String
# - __price:float
# - __stock:int
# + update_stock(quantity : int):void
# + display_information():voidclass Product: 

#__ = private 
# + = public 
# # = protected

#void is there to represent it doesnt return the data..

from abc import ABC, abstractmethod
from .supplier import Supplier 

#Your Product constructor should accept a Supplier object, not just the supplier's name or ID. 
# Store the reference so that the Product can access the supplier's information when required

# The Supplier object is created independently and then supplied to the Product when the Product is
#created
class Product(ABC):
    def __init__(self, product_id: str, name: str , price: float, stock: int, supplier: Supplier ):
        if price <= 0:
            raise ValueError("Product price must be greater than zero.")
        if stock < 0:
            raise ValueError("Product stock quantity cannot be negative.")
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self._supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self._supplier

    @abstractmethod
    def get_fulfillment_info(self) -> str:
        pass

    #methods go here
    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Product stock quantity cannot be negative.")
        self.__stock = quantity


    def display_information(self) -> None:
            # Prints common info; end=" | " lets the child continue on the same line
            print(
                f"ID: {self.product_id} | "
                f"Name: {self.name} | "
                f"Price: ${float(self.price):.2f} | "
                f"Stock: {self.stock}",
                end=" | "
            )

    def to_dict(self) -> dict:                                                                                                                                                                                                                                                         
        return {                                                                                                                                                                                                                                                                       
                "id": self.product_id,                                                                                                                                                                                                                                                   
                "name": self.name,                                                                                                                                                                                                                                                       
                "price": self.price,                                                                                                                                                                                                                                                     
                "stock": self.stock,                                                                                                                                                                                                                                                     
            } 
