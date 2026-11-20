from src.modules.digitalProduct import DigitalProduct
from src.modules.physicalProduct import PhysicalProduct
from src.modules.product import Product
from src.modules.supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        weight: float = 0.0,
        download_size: float = 0.0,
    ) -> Product:
        """Create a PhysicalProduct or DigitalProduct based on product_type."""
        normalized_type = product_type.strip().lower()
        if normalized_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, weight, supplier)
        if normalized_type == "digital":
            return DigitalProduct(product_id, name, price, stock, download_size, supplier)
        raise ValueError(f"Unknown product type: {product_type}")
