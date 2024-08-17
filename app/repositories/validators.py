import re


def dni_validator(dni):
    pattern = re.compile("^[1-9][0-9]*$")
    if not pattern.match(dni):
        raise ValueError("Invalid DNI")
    return dni


def phone_validator(phone):
    pattern = re.compile("[0-9]{2,3}-?[0-9]{3,4}-?[0-9]{3,4}")
    if not pattern.match(phone):
        raise ValueError("Invalid Phone Number")
    return phone


def price_validator(price, max_price: float, min_price: float = .01):
    if min_price <= price <= max_price:
        return price
    else:
        raise ValueError(f"Price outside of the valid range (min: {min_price}, max: {max_price})")
