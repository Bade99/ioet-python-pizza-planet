from datetime import datetime
from faker import Faker
import random
from ..controllers import (
    OrderController,
    IngredientController,
    BeverageController,
    SizeController,
)


def populate_db():
    num_customers = 30
    num_ingredients = 10
    num_beverages = num_ingredients
    num_sizes = 5
    num_orders = 200
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 8, 15)

    max_ingredient_price = 10
    max_beverage_price = max_ingredient_price
    max_size_price = 30

    customers = prepare_customers(num_customers)

    sizes = generate_additionals(SizeController, num_sizes, max_size_price)

    ingredients = generate_additionals(
        IngredientController, num_ingredients, max_ingredient_price
    )

    beverages = generate_additionals(
        BeverageController, num_beverages, max_beverage_price
    )

    generate_orders(
        num_orders, start_date, end_date, customers, sizes, ingredients, beverages
    )

    print(
        f"Database populated with {num_sizes} sizes, {num_ingredients} ingredients, {num_beverages} beverages, and {num_orders} orders from {num_customers} new customers."
    )


def prepare_customers(num_customers):
    fake = Faker()
    customers = []
    for _ in range(num_customers):
        customers.append(
            {
                "client_name": fake.name(),
                "client_dni": str(random.randint(1000000, 9999999999)),
                "client_address": fake.address(),
                "client_phone": fake.msisdn()[:10],
            }
        )
    return customers


def generate_additionals(controller, num_additionals, max_additional_price):
    fake = Faker()
    additionals = []
    for _ in range(num_additionals):
        additional, error = controller.create(
            {
                "name": fake.word(),
                "price": str(round(random.uniform(0.5, max_additional_price), 2)),
            }
        )
        additionals.append(str(additional["_id"]))
    return additionals


def generate_orders(
    num_orders, start_date, end_date, customers, sizes, ingredients, beverages
):
    fake = Faker()
    for _ in range(num_orders):
        order = {
            **random.choice(customers),
            "size_id": random.choice(sizes),
            "ingredients": random.sample(
                ingredients, random.randint(0, len(ingredients))
            ),
            "beverages": random.sample(beverages, random.randint(0, len(beverages))),
            "date": fake.date_time_between_dates(start_date, end_date),
            # TODO(fran): this is actually a big security concern, we shouldn't allow a bad actor in the frontend to set an arbitrary date, but it is very useful for this population test, so we should maybe only allow it while testing
        }
        OrderController.create(order)
