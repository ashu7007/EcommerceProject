"""Models related to user operations"""
import enum
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from sqlalchemy.dialects.postgresql import JSON

from apps import db_sql

# from dbConfig.db import db

db = db_sql


class Userdata(db.Model):
    """Model for users"""
    __tablename__ = 'userdata'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.DateTime, default=None)
    active = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    is_customer = db.Column(db.Boolean, nullable=False)
    is_shopuser = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    shop = db.relationship('Shop', backref='shops', lazy=True)
    order = db.relationship('Orders', backref='user', lazy=True)
    product = db.relationship('Product', backref='shopuser', lazy=True)

    # wishlist = db.relationship("Wishlist", back_populates="user")

    def get_reset_token(self, expires_sec=300):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return user_id

    def __repr__(self):
        return f"User('{self.email}','{self.username}')"


class Wishlist(db.Model):
    """model for Wishlist"""
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.id'))
    product_id = db.Column(db.ARRAY(db.Integer), nullable=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"wishlist'{self.id}')"


class Cart(db.Model):
    """model for cart"""
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.id',ondelete='SET NULL'))
    items = db.Column(JSON)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"Cart'{self.id}')"


class Status(enum.Enum):
    StatusInit = 0
    StatusProcessed = 1
    StatusCancelled = 2
    StatusDelivered = 3


class Payment(enum.Enum):
    pending = 1
    paid = 2


class Orders(db.Model):
    """model for Order"""

    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.id',ondelete='SET NULL'))
    status = db.Column(db.Enum(Status))
    payment = db.Column(db.Enum(Payment))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    orderdetail = db.relationship('OrderDetail', backref='order', lazy=True)

    def __repr__(self):
        return f"Order'{self.id} status{self.status}')"


class OrderDetail(db.Model):
    """model for OrderDetail"""

    __tablename__ = 'orderdetail'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id',ondelete='SET NULL'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='SET NULL'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"OrderDetail'{self.id}')"


class OTP(db.Model):
    """model for otp"""

    __tablename__ = 'otp'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.id',ondelete='SET NULL'))
    otp = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"OTP'{self.id}','{self.otp}')"


class Shop(db.Model):
    """model for shop"""
    __tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.id',ondelete='SET NULL'))
    store_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # user = db.relationship(Userdata, backref='shops')

    def __repr__(self):
        return f"'{self.id}','{self.store_name}'"


class ShopRejection(db.Model):
    """model for shop rejection"""
    __tablename__ = 'shoprejection'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.id',ondelete='SET NULL'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id',ondelete='SET NULL'))
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"'{self.id}','{self.user_id}'"

from apps import app
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
import functools
import os
from flask import Flask, render_template, session, redirect, g, url_for, abort
some_engine = create_engine(os.environ.get('DATABASE_URL'))
Session = sessionmaker(bind=some_engine)
db_session = Session()
@app.before_request
def load_logged_in_user():
    """ logged user"""
    user_id = session.get('r_user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_session.query(Userdata).filter(Userdata.id == user_id).first()


def login_required(view):
    """ function to check logged-in user"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def admin_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if not g.user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return wrapper

def admin_shopuser_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if not g.user.is_admin and not g.user.is_shopuser:
            abort(403)
        return func(*args, **kwargs)
    return wrapper

def shopuser_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if not g.user.is_shopuser:
            abort(403)
        return func(*args, **kwargs)
    return wrapper

def customer_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if not g.user.is_customer:
            abort(403)
        return func(*args, **kwargs)
    return wrapper