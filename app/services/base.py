from flask import jsonify


def execute(controller_command, *args):
    result, error = controller_command(*args)
    response = result if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code


def execute__with_not_found(controller_command, *args):
    result, error = controller_command(*args)
    response = result if not error else {'error': error}
    status_code = 200 if result else 404 if not error else 400
    return jsonify(response), status_code
