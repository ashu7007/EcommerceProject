import os
import datetime
import functools
from random import randint
from flask import current_app
from flask_mail import Mail, Message
# from flask_login import login_required
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from dbConfig import db

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session

from apps.products.models import Product,Category
from apps.users.models import Userdata

# some_engine = create_engine('postgresql+psycopg2://admin:admin@localhost/ecommerce')
some_engine = create_engine('postgresql+psycopg2://admin:admin@localhost:5432/testShop')
Session = sessionmaker(bind=some_engine)
db_session = Session()

prod_bp = Blueprint('product', __name__, url_prefix='/product')


@prod_bp.route('/', methods=('GET','POST'))
# @login_required
def shop_dashboard():
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_shopuser or user.is_admin:
        products = db_session.query(Product).filter(Product.user_id==user.id).all()
        category = Category.query.all()
        return render_template('shop/shopDashboard.html',product=products,category=category)


# @bp.route("/list_shop", methods=['POST','GET'])
# def list_shop():
#     r_user_id = session.get('r_user_id')
#     user = db_session.query(Userdata).get(r_user_id)
#     if user.is_shopuser or user.is_admin:
#         shops = db_session.query(Shop).all()
#         return render_template("shop/shoplist.html", shops=shops)


@prod_bp.route("/create_product", methods=['POST','GET'])
def create_product():
    r_user_id = session.get('r_user_id')
    user = Userdata.query.get(r_user_id)
    if request.method == 'POST' and (user.is_shopuser or user.is_admin):

        category_id = request.form.get('category_id')
        product_name = request.form.get('product_name')
        stock_quantity = request.form.get('stock_quantity')
        brand = request.form.get('brand')
        price = request.form.get('price')
        
        error = None

        if not category_id:
            error = 'category is required.'
        if not product_name:
            error = 'password is required.'
        if not stock_quantity:
            error = 'full name is required.'
        if not brand:
            error = 'address is required.'
        if not price:
            error = 'gender is required.'
        date = datetime.datetime.now()

        if error is None:
            try:
                product_name = request.form.get('product_name')
                stock_quantity = request.form.get('stock_quantity')
                sold_quantity = request.form.get('sold_quantity')
                brand = request.form.get('brand')
                price = request.form.get('price')
                shop_id = user.shop[0].id
                product = Product(user_id=user.id, shop_id=shop_id,
                                category_id=category_id,
                                product_name=product_name,
                                stock_quantity=stock_quantity, 
                                sold_quantity=0, brand=brand,
                                price=price,
                                active=True, created_at=date,
                                updated_at=date)
                db_session.add(product)
                db_session.commit()

            except:
                raise
                # error = f"User {username} is already registered."
            else:
                return redirect(url_for("product.shop_dashboard"))

        flash(error)
    #return redirect(url_for("product.shop_dashboard"))
    category = Category.query.all()
    return render_template('product/createproduct.html',category=category)


@prod_bp.route('/delete/<id>', methods=('GET','POST'))
def delete(id):
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)

    if user.is_shopuser or user.is_admin:
        error = None
        db_session.query(Product).filter(Product.id ==id).delete()
        db_session.commit()
        return redirect(url_for("product.shop_dashboard"))
    return redirect(url_for("product.shop_dashboard"))


@prod_bp.route('/update_product/<id>', methods=('GET','POST'))
def update_product(id):
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)

    if user.is_shopuser or user.is_admin:
        category_id = request.form.get('category_id')
        product_name = request.form.get('product_name')
        stock_quantity = request.form.get('stock_quantity')
        brand = request.form.get('brand')
        price = request.form.get('price')
        
        error = None

        if not category_id:
            error = 'category is required.'
        if not product_name:
            error = 'password is required.'
        if not stock_quantity:
            error = 'full name is required.'
        if not brand:
            error = 'address is required.'
        if not price:
            error = 'gender is required.'
        date = datetime.datetime.now()
        product = db_session.query(Product).get(id)
        update_object = {}
        if category_id and product.category_id != category_id:
            update_object["category_id"] = category_id
        if product_name and product.product_name != product_name:
            update_object["product_name"] = product_name
        if stock_quantity and product.stock_quantity != stock_quantity:
            update_object["stock_quantity"] = stock_quantity
        if brand and product.brand != brand:
            update_object["brand"] = brand
        if price and product.price != price:
            update_object["price"] = price

        db_session.query(Product).filter(Product.id == id).update(update_object)
        db_session.commit()
        return redirect(url_for("product.shop_dashboard"))
    return redirect(url_for("product.shop_dashboard"))
