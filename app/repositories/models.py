from datetime import datetime
from app.plugins import db
from sqlalchemy.orm import validates
from .validators import dni_validator, phone_validator, price_validator


class Order(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(80))
    client_dni = db.Column(db.String(10))
    client_address = db.Column(db.String(128))
    client_phone = db.Column(db.String(15))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float)
    size_id = db.Column(db.Integer, db.ForeignKey("size._id"))

    size = db.relationship("Size", backref=db.backref("size"))
    detail = db.relationship("OrderDetail", backref=db.backref("order_detail"))

    @validates("client_dni")
    def validate_client_dni(self, key, client_dni):
        return dni_validator(client_dni)

    @validates("client_phone")
    def validate_client_phone(self, key, client_phone):
        return phone_validator(client_phone)

    @validates("total_price")
    def validate_total_price(self, key, total_price):
        return price_validator(total_price, float("inf"))


class Ingredient(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    @staticmethod
    def max_price():
        return 10

    @validates("price")
    def validate_ingredient_price(self, key, price):
        return price_validator(price, self.max_price())


class Beverage(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    @staticmethod
    def max_price():
        return 10

    @validates("price")
    def validate_beverage_price(self, key, price):
        return price_validator(price, self.max_price())


class Size(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    @staticmethod
    def max_price():
        return 30

    @validates("price")
    def validate_size_price(self, key, price):
        return price_validator(price, self.max_price())


class OrderDetail(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order._id"))
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient._id"))
    beverage_id = db.Column(db.Integer, db.ForeignKey("beverage._id"))
    price = db.Column(db.Float)

    ingredient = db.relationship("Ingredient", backref=db.backref("ingredient"))
    beverage = db.relationship("Beverage", backref=db.backref("beverage"))
