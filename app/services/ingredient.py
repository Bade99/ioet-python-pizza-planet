from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import IngredientController
from .base import execute, execute__with_not_found


ingredient = Blueprint('ingredient', __name__)
controller = IngredientController


@ingredient.route('/', methods=POST)
def create_ingredient():
    return execute(controller.create, request.json)


@ingredient.route('/', methods=PUT)
def update_ingredient():
    return execute(controller.update, request.json)


@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
    return execute__with_not_found(controller.get_by_id, _id)


@ingredient.route('/', methods=GET)
def get_ingredients():
    return execute__with_not_found(controller.get_all)
