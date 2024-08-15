from dotenv import load_dotenv
load_dotenv()

import pytest
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app import flask_app
from app.plugins import db
# flake8: noqa
from app.repositories.models import Ingredient, Beverage, Order, OrderDetail, Size

from app.scripts.populate import populate_db

manager = FlaskGroup(flask_app)

migrate = Migrate()
migrate.init_app(flask_app, db)


@manager.command('test', with_appcontext=False)
def test():
    import subprocess
    subprocess.call(['pytest', '-v', './app/test'])

@manager.command('populate', with_appcontext=True)
def populate():
    return populate_db()

if __name__ == '__main__':
    manager()
