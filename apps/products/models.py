import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from dbConfig.db import db


class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.id'))
    category_name = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    

    def __repr__(self):
        return f"category_name :'{self.category_name}')"



class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    product_name = db.Column(db.String(255), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    sold_quantity = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer,nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    

    def __repr__(self):
        return f"product name :'{self.product_name}')"
    
    def __init__(self,category_id,product_name,brand,price):
        self.category_id = category_id
        self.product_name = product_name
        self.brand = brand
        self.price = price

    def format(self):
        return {
        'id': self.id,
        'category_id': self.category_id,
        'product_name': self.product_name,
        'brand': self.brand,
        'price': self.price,
        }