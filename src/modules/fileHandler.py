from pathlib import Path
import csv
import os
import json

from src.modules.inventory import Inventory                                                                                                                                                                                                                                                              
from src.modules.product import Product    
from src.modules.physicalProduct import PhysicalProduct
from src.modules.digitalProduct import DigitalProduct
from src.modules.supplier import Supplier
from src.product.productFactory import ProductFactory                                                                                                                                                                                                                                                             

class FileHandler:
    def __init__(self, filepath: str = "src/model/inventory.json"):
        self.filepath = Path(filepath)


    def file_exist(self):
        return self.filepath.is_file() and self.filepath.suffix.lower() == ".json"

    # def load_data
    def load_data(self, inventory: Inventory):
        if self.file_exist():

            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
            except json.JSONDecodeError:
                return
            for item in raw_data: 
                supplier_info = item.get("supplier", {})
                supplier = Supplier(
                    supplier_id=supplier_info.get("id", "S001"),
                    name=supplier_info.get("name", "Default Supplier"),
                    contact_email=supplier_info.get("contact_email", "supplier@example.com")
                )
                if item["type"] == "physical":
                    #init the physical product class!
                    product = PhysicalProduct(
                        product_id = item["id"],
                        name = item["name"],
                        price = item["price"],
                        stock = item["stock"],
                        weight = item["weight"],
                        supplier = supplier
                    )
                elif item["type"] == "digital": 
                    product = DigitalProduct(
                        product_id = item["id"],
                        name = item["name"],
                        price = item["price"],
                        stock = item["stock"],
                        download_size = item["download_size"],
                        supplier = supplier
                    )
                inventory.add_product(product)
            # try:
            #     with open(self.filepath, "r", encoding="utf-8") as f:
            #         return json.load(f)  # Returns list of dicts 
            # except json.JSONDecodeError:
            #     return []  

    # save data
    def save_data(self, products: list) -> None: 
            data = [prod.to_dict() for prod in products]                                                                                                                                                                                                                             
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file into inventory using ProductFactory."""
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for row in reader:
                if not row:
                    continue
                product_type, product_id, name, price_str, stock_str = row
                try:
                    price = float(price_str)
                    stock = int(stock_str)
                    product = ProductFactory.create(
                        product_type, product_id, name, price, stock, supplier
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as err:
                    print(f"Skipping invalid row {row}: {err}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")




