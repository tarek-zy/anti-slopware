BULK_ORDER_MIN_UNITS = 10


def calculate_order_total(items, tax_rate):
    total = 0
    for item in items:
        total += item["price"] * item["quantity"]
    total = total + total * tax_rate
    return round(total, 2)


def calculate_cart_total(items, tax_rate):
    return calculate_order_total(items, tax_rate)


def format_price(amount):
    return f"${amount:.2f}"


def count_units(items):
    count = 0
    for item in items:
        count += item["quantity"]
    return count


def is_bulk_order(items):
    return count_units(items) >= BULK_ORDER_MIN_UNITS


def get_discount(customer):
    if customer is None or "tier" not in customer:
        return 0
    if customer["tier"] == "gold":
        return 0.1
    if customer["tier"] == "silver":
        return 0.05
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
