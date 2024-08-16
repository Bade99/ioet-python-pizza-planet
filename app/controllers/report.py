from datetime import datetime
from collections import defaultdict
from ..controllers import OrderController, IngredientController, BeverageController


class ReportController:

    @staticmethod
    def get_top_ingredient(ingredients: dict):
        sorted_ingredients = sorted(ingredients.items(), key=lambda x: x[1], reverse=True)
        top_ingredient = None
        if sorted_ingredients:
            ingredient_id, ingredient_request_count = sorted_ingredients[0]
            top_ingredient = IngredientController.get_by_id(ingredient_id)[0]
            top_ingredient["count"] = ingredient_request_count
        return top_ingredient

    @staticmethod
    def get_top_beverage(beverages: dict):
        sorted_beverages = sorted(beverages.items(), key=lambda x: x[1], reverse=True)
        top_beverage = None
        if sorted_beverages:
            beverage_id, beverage_request_count = sorted_beverages[0]
            top_beverage = BeverageController.get_by_id(beverage_id)[0]
            top_beverage["count"] = beverage_request_count
        return top_beverage

    @staticmethod
    def get_month_revenues(months_by_revenue: dict):
        sorted_month_revenues = sorted(months_by_revenue.items(), key=lambda x: x[0])
        return {
            "months": [month_revenue[0] for month_revenue in sorted_month_revenues],
            "revenues": [month_revenue[1] for month_revenue in sorted_month_revenues],
        }

    @staticmethod
    def get_top_clients(clients: dict, clients_spendings: dict):
        top_clients_data = sorted(clients_spendings.items(), key=lambda x: x[1], reverse=True)[:3]
        return [
            dict(clients[client[0]], **{"client_spending": client[1]})
            for client in top_clients_data
        ]

    @classmethod
    def get_report(cls, start_date: str, end_date: str):
        # TODO(fran): this whole logic may be better suited for a db query

        orders, error = OrderController.get_all_between(start_date, end_date)

        if error:
            return None, str(error)

        ingredients = defaultdict(int)
        beverages = defaultdict(int)
        months_by_revenue = defaultdict(float)

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

            months_by_revenue[
                datetime.fromisoformat(order["date"]).strftime("%Y-%m")
            ] += order["total_price"]

            clients[order["client_dni"]] = {
                "client_dni": order["client_dni"],
                "client_name": order["client_name"],
                "client_address": order["client_address"],
                "client_phone": order["client_phone"],
            }
            clients_spendings[order["client_dni"]] += order["total_price"]

        report = {
            "top_ingredient": cls.get_top_ingredient(ingredients),
            "top_beverage": cls.get_top_beverage(beverages),
            "month_revenues": cls.get_month_revenues(months_by_revenue),
            "top_clients": cls.get_top_clients(clients, clients_spendings)
        }

        return report, None
