def check_user_input(user_input):
    #check if its digit. and if its digit return the number
    if user_input.isdigit():
        return user_input
    else:
        return "NaN"


def get_positive_price(prompt: str = "Price: ") -> float:
    """Prompt the user until a valid positive float price is entered."""
    while True:
        try:
            price = float(input(prompt))
            if price <= 0:
                raise ValueError("Price must be greater than zero.")
            return price
        except ValueError as err:
            print(f"Invalid price ({err}). Please enter a number greater than 0.")