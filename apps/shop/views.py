"""module related to shop operations"""
import datetime
from flask import (Blueprint, flash, redirect, render_template, request, session, url_for,abort)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from apps.users.models import Shop, Userdata

some_engine = create_engine('postgresql+psycopg2://admin:admin@localhost:5433/testShop')
Session = sessionmaker(bind=some_engine)
db_session = Session()
bp = Blueprint('shop', __name__, url_prefix='/shop')


@bp.route("/list_shop", methods=['POST', 'GET'])
def list_shop():
    """function to list shop"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_admin:
        shops = db_session.query(Shop).all()
        return render_template("shop/shoplist.html", shops=shops)

    return abort(401, "You have to provide either 'url' or 'text', too")


@bp.route("/create_shop", methods=['POST', 'GET'])
def create_shop():
    """function to create shop"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if request.method == 'POST' and user.is_admin== True:
        full_name = request.form.get('full_name')
        email = request.form.get("email")
        username = request.form.get('username')
        password = request.form.get('password')
        address = request.form.get('address')
        gender = request.form.get('gender')
        dob = request.form.get('dob')
        store_name = request.form.get('store_name')
        description = request.form.get('description')
        error = None

        if not username:
            error = 'Username is required.'
        if not password:
            error = 'password is required.'
        if not full_name:
            error = 'full name is required.'
        if not email:
            error = 'email is required.'
        if not address:
            error = 'address is required.'
        if not gender:
            error = 'gender is required.'
        if not store_name:
            error = 'store name is required.'
        if not description:
            error = 'description is required.'

        elif not dob:
            error = 'dob is required.'
        date = datetime.datetime.now()

        if error is None:
            try:
                user = Userdata(full_name=full_name, email=email, username=username,
                                password=generate_password_hash(password),
                                address=address, gender=gender, dob=dob, active=False,
                                is_admin=False,
                                is_customer=False, is_shopuser=True, created_at=date,
                                updated_at=date)
                db_session.add(user)
                db_session.commit()
                shop_object = Shop(user_id=user.id, store_name=store_name, description=description,
                                   active=True, status="Approved",
                                   created_at=date, updated_at=date)
                db_session.add(shop_object)
                db_session.commit()

            except Exception as e:
                raise e
                # error = f"User {username} is already registered."
            else:
                return redirect(url_for("shop.list_shop"))
                # shops = db_session.query(Shop).all()
                # return render_template("shop/shoplist.html", shops=shops)
        flash(error)
    return render_template('shop/adminShop.html')


@bp.route("/delete_shop/<id>", methods=['POST', 'GET'])
def delete_shop(id):
    """function to delete shop"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_admin:
        db_session.query(Shop).filter(Shop.id == id).delete()
        db_session.commit()
        return redirect(url_for("shop.list_shop"))

    return abort(401, "You have to provide either 'url' or 'text', too")


@bp.route("/update_shop/<id>", methods=['POST', 'GET'])
def update_shop(id):
    """function to update shop"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)

    if request.method == 'POST' and user.is_admin:

        store_name = request.form.get('store_name')
        description = request.form.get('description')

        if not store_name:
            error = 'store name is required.'
        if not description:
            error = 'description is required.'

        db_session.query(Shop).filter(Shop.id == id).update({
            'store_name': store_name,
            'description': description,
            'active': True,
            'status': 'Approved'
        })
        db_session.commit()
        flash(error)
        return redirect(url_for("shop.list_shop"))

    return abort(401, "You have to provide either 'url' or 'text', too")
