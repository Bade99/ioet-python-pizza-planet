from datetime import datetime
from app.plugins import db
from sqlalchemy.orm import validates
import re


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
        pattern = re.compile("^([A-Z][0-9]+)+$")
        if not pattern.match(client_dni):
            raise ValueError("Invalid DNI")
        return client_dni
    
    @validates("client_phone")
    def validate_client_phone(self, key, client_phone):
        pattern = re.compile("[0-9]{2,3}-?[0-9]{3,4}-?[0-9]{3,4}")
        if not pattern.match(client_phone):
            raise ValueError("Invalid Phone Number")
        return client_phone


class Ingredient(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)


class Size(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)


class OrderDetail(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    ingredient_price = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey("order._id"))
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient._id"))
    ingredient = db.relationship("Ingredient", backref=db.backref("ingredient"))
