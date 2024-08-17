from typing import Callable
from functools import wraps
from flask import jsonify


def response(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result, error = func(*args, **kwargs)
        response = result if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code
    return wrapper


def response__with_not_found(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result, error = func(*args, **kwargs)
        response = result if not error else {'error': error}
        status_code = 200 if result else 404 if not error else 400
        return jsonify(response), status_code
    return wrapper
