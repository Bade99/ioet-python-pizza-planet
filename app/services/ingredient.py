from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import IngredientController
from .decorators import response, response__with_not_found


ingredient = Blueprint('ingredient', __name__)
controller = IngredientController


@ingredient.route('/', methods=POST)
@response
def create_ingredient():
    return controller.create(request.json)


@ingredient.route('/', methods=PUT)
@response
def update_ingredient():
    return controller.update(request.json)


@ingredient.route('/id/<_id>', methods=GET)
@response__with_not_found
def get_ingredient_by_id(_id: int):
    return controller.get_by_id(_id)


@ingredient.route('/', methods=GET)
@response__with_not_found
def get_ingredients():
    return controller.get_all()