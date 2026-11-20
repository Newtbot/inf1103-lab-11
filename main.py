from src.modules.product import Product
from src.product.productFactory import ProductFactory
from src.modules.inventory import Inventory 
from src.modules.fileHandler import FileHandler
from src.modules.supplier import Supplier
from src.modules.order import Order
from src.utils.check_user_input import check_user_input, get_positive_price

inventory = Inventory()
fileHandler = FileHandler()

fileHandler.load_data(inventory)

while True:
    print(
        "========================================================\n"
        "INVENTORY MANAGEMENT SYSTEM\n"
        "========================================================\n\n"
        "inventory.json found.\n"
        "Inventory loaded successfully\n\n"
        "----------- MENU -----------\n"
        "1. Display All Products\n"
        "2. Add Product\n"
        "3. Update Stock\n"
        "4. Search Product\n"
        "5. Create Order\n"
        "6. Save Inventory\n"
        "7. Exit\n"
        "----------------------------\n"
    )

    user_option = input("Enter Option: ")
    if check_user_input(user_option) == "1":
        print(
            "--------------------------------------------------------\n"
            "Current Inventory\n"
            "--------------------------------------------------------"
        )
        if not inventory.products:                
            print("Inventory Not found") 
        else:
            inventory.display_products()

    elif check_user_input(user_option) == "2":
        print("\nAdd New Product\n")
        print("Select Product Type:")
        print("1. Physical Product")
        print("2. Digital Product")
        product_type = input("Enter choice (1/2): ").strip()

        if product_type not in ("1", "2"):
            print("Invalid product type selected. Returning to menu.")
            continue   
        product_id = input("Product ID: ").strip().upper()
        product_name = input("Product Name: ").strip()
        price = get_positive_price("Price: ")
        stock = int(input("Stock Quantity: "))
        supplier_id = input("Supplier ID: ").strip()
        supplier_name = input("Supplier Name: ").strip()
        supplier_email = input("Supplier Email: ").strip()
        supplier = Supplier(supplier_id, supplier_name, supplier_email)

        if product_type == "1":
            weight = float(input("Weight: "))
            new_product = ProductFactory.create(
                "physical",
                product_id,
                product_name,
                price,
                stock,
                supplier,
                weight=weight,
            )
        else:
            download_size = float(input("Download Size: "))
            new_product = ProductFactory.create(
                "digital",
                product_id,
                product_name,
                price,
                stock,
                supplier,
                download_size=download_size,
            )
        inventory.add_product(new_product)

    elif check_user_input(user_option) == "3":
        print("Update Stock")
        product_id = input("Product ID: ").strip().upper()

        product_item = inventory.search_product(product_id)
        if product_item:
            product_stock = int(input("New Stock Quantity: "))
            product_item.update_stock(product_stock)
        else:
            print("Product not found.")

    elif check_user_input(user_option) == "4":
        print("Search Stock")
        product_id = input("Product ID: ").strip().upper()
        product_item = inventory.search_product(product_id)            
        if product_item:
            product_item.display_information()
            product_item.supplier.display_information()
        else: 
            print("Product not found")

    elif check_user_input(user_option) == "5":
        print("Create Order")
        order_id = input("Order ID: ").strip().upper()
        order = Order(order_id)
        while True:
            prod_id = input("Product ID to add (or 'DONE'): ").strip().upper()
            if prod_id == "DONE":
                break
            found_prod = inventory.search_product(prod_id)
            if not found_prod:
                print("Product not found.")
                continue
            qty = int(input("Quantity: "))
            order.add_order_line(found_prod, qty)

        if order.order_lines:
            print(f"\nOrder {order.order_id} Summary:")
            for line in order.order_lines:
                print(f"{line.product.name} x {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}")
            print(f"Total: ${order.calculate_total():.2f}\n")
        else:
            print("No items in order.")

    elif check_user_input(user_option) == "6":
        print("Saving inventory......")
        print("Inventory saved successfully to inventory.json.")
        fileHandler.save_data(inventory.products)
    
    elif check_user_input(user_option) == "7":
        fileHandler.save_data(inventory.products)
        print("Saving inventory before exit...")
        print("Inventory saved successfully.\n")
        print(
            "Thank you for using Inventory Management System.\n"
            "Program terminated."
        )
        break

    else:
        print("Please enter a valid integer. Eg. `1` ")
