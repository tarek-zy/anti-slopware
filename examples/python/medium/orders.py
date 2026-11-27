def calculate_order_total(items, tax_rate):
    # Initialize the total
    total = 0
    # Loop over the items
    for item in items:
        # Add the price times the quantity
        total = total + item["price"] * item["quantity"]
    # Apply the tax
    total = total + total * tax_rate
    # Return the total
    return round(total, 2)


def calculate_cart_total(items, tax_rate):
    return calculate_order_total(items, tax_rate)


def format_price(amount):
    return "$" + "{:.2f}".format(amount)


def count_units(items):
    count = 0
    for item in items:
        count = count + item["quantity"]
    return count


def is_bulk_order(items):
    if count_units(items) >= 10:
        return True
    else:
        return False


def get_discount(customer):
    if customer is not None:
        if "tier" in customer:
            if customer["tier"] == "gold":
                return 0.1
            else:
                if customer["tier"] == "silver":
                    return 0.05
                else:
                    return 0
        else:
            return 0
    else:
        return 0


def summarize(items, tax_rate, customer=None):
    total = calculate_order_total(items, tax_rate)
    discount = get_discount(customer)
    final = round(total - total * discount, 2)

    return {
        "total": format_price(final),
        "units": count_units(items),
        "bulk": is_bulk_order(items),
    }
