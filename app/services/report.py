from app.common.http_methods import GET
from flask import Blueprint, jsonify, request

from ..controllers import OrderController, IngredientController, BeverageController

from datetime import datetime

from collections import defaultdict

report = Blueprint("report", __name__)


@report.route("", methods=GET)
def get_report():
    # TODO(fran): determine where all this logic should go
    orders, error = OrderController.get_all_between(
        request.args.get("startDate"), request.args.get("endDate")
    )

    report = {}
    if orders:
        ingredients = defaultdict(int)
        beverages = defaultdict(int)
        month_revenues = defaultdict(float)

        clients = {}
        clients_spendings = defaultdict(float)

        for order in orders:
            for detail in order.get("detail", []):
                new_ingredient = detail["ingredient"]
                new_beverage = detail["beverage"]
                if new_ingredient:
                    ingredients[new_ingredient["_id"]] += 1
                elif new_beverage:
                    beverages[new_beverage["_id"]] += 1

            month_revenues[
                datetime.fromisoformat(order["date"]).strftime("%Y-%m")
            ] += order["total_price"]

            clients[order["client_dni"]] = {
                "client_dni": order["client_dni"],
                "client_name": order["client_name"],
                "client_address": order["client_address"],
                "client_phone": order["client_phone"],
            }
            clients_spendings[order["client_dni"]] += order["total_price"]

        sorted_ingredients = sorted(
            ingredients.items(), key=lambda x: x[1], reverse=True
        )
        if sorted_ingredients:
            ingredient_id, ingredient_request_count = sorted_ingredients[0]
            ingredient_data = IngredientController.get_by_id(ingredient_id)[0]
            ingredient_data["count"] = ingredient_request_count
            report["top_ingredient"] = ingredient_data

        sorted_beverages = sorted(
            beverages.items(), key=lambda x: x[1], reverse=True
        )
        if sorted_beverages:
            beverage_id, beverage_request_count = sorted_beverages[0]
            beverage_data = BeverageController.get_by_id(beverage_id)[0]
            beverage_data["count"] = beverage_request_count
            report["top_beverage"] = beverage_data

        ordered_month_revenues = sorted(
            month_revenues.items(), key=lambda x: x[0], reverse=False
        )
        report["month_revenues"] = {
            "months": [month_revenue[0] for month_revenue in ordered_month_revenues],
            "revenues": [month_revenue[1] for month_revenue in ordered_month_revenues],
        }

        top_clients = sorted(clients_spendings.items(), key=lambda x: x[1], reverse=True)[
            :3
        ]
        report["top_clients"] = [
            dict(clients[client[0]], **{"client_spending": client[1]})
            for client in top_clients
        ]

    response = report if not error else {"error": error}
    status_code = 200 if report else 404 if not error else 400
    return jsonify(response), status_code
