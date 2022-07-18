from flask.views import MethodView ,View
import os
import datetime
import functools
from random import randint
from flask import current_app
from flask_mail import Mail, Message
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash


from  apps.users.models import Shop ,Userdata

from dbConfig import db

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session


some_engine = create_engine('postgresql+psycopg2://admin:admin@localhost/ecommerce')
Session = sessionmaker(bind=some_engine)
db_session = Session()
# bp = Blueprint('auth', __name__, url_prefix='/auth')



class ShopAPI(MethodView):

    def get(self, id):
        r_user_id = session.get('r_user_id')
        user = db_session.query(Userdata).get(r_user_id)
        if user.is_admin:
            if id is None:
                shops = db_session.query(Shop).all()
                return render_template("shop/shoplist.html", shops=shops)
            else:
                pass
        

    def post(self):
        # full_name = request.form['full_name']
        # email = request.form['email']
        # username = request.form['username']
        # password = request.form['password']
        # address = request.form['address']
        # gender = request.form['gender']
        # dob = request.form['dob']
        # store_name = request.form['store_name']
        # description = request.form['description']
        # error = None

        # if not username:
        #     error = 'Username is required.'
        # if not password:
        #     error = 'password is required.'
        # if not full_name:
        #     error = 'full name is required.'
        # if not email:
        #     error = 'email is required.'
        # if not address:
        #     error = 'address is required.'
        # if not gender:
        #     error = 'gender is required.'
        # if not store_name:
        #     error = 'store name is required.'
        # if not description:
        #     error = 'description is required.'

        # elif not dob:
        #     error = 'dob is required.'
        # date = datetime.datetime.now()

        # if error is None:
        #     try:
        #         user = Userdata(full_name=full_name, email=email, username=username,
        #                         password=generate_password_hash(password),
        #                         address=address, gender=gender, dob=dob, active=False, is_admin=False,
        #                         is_customer=False, is_shopuser=True, created_at=date,
        #                         updated_at=date)
        #         db_session.add(user)
        #         db_session.commit()
        #         shop_object = Shop(user_id=user.id, store_name=store_name, description=description, 
        #                         active=False,status="Approved",
        #                         created_at=date, updated_at=date)
        #         db_session.add(shop_object)
        #         db_session.commit()

        #     except:
        #         raise
        #         # error = f"User {username} is already registered."
        #     else:
        #         shops = db_session.query(Shop).all()
        #         return render_template("shop/shoplist.html", shops=shops)
        pass
    
    def delete(self, id):
        r_user_id = session.get('r_user_id')
        user = db_session.query(Userdata).get(r_user_id)
        if user.is_admin:
            shops = db_session.query(Shop).all()
            db_session.query(Shop).filter(Shop.id == id).delete()
            db_session.commit()
            return render_template("shop/shoplist.html", shops=shops)

    
    def put(self, user_id):
        r_user_id = session.get('r_user_id')
        user = db_session.query(Userdata).get(r_user_id)
        if user.is_admin:
            shops = db_session.query(Shop).all()
            db_session.query(Shop).filter(Shop.id == id).update({'active': True, 'status': 'Approved'})
            db_session.commit()
            return render_template("shop/shoplist.html", shops=shops)


class AdminShop(View):
    methods = ['GET','POST']

    def dispatch_request(self):
        if request.method == 'POST':
            full_name = request.form['full_name']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            address = request.form['address']
            gender = request.form['gender']
            dob = request.form['dob']
            store_name = request.form['store_name']
            description = request.form['description']
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
                                    address=address, gender=gender, dob=dob, active=False, is_admin=False,
                                    is_customer=False, is_shopuser=True, created_at=date,
                                    updated_at=date)
                    db_session.add(user)
                    db_session.commit()
                    shop_object = Shop(user_id=user.id, store_name=store_name, description=description, 
                                    active=True,status="Approved",
                                    created_at=date, updated_at=date)
                    db_session.add(shop_object)
                    db_session.commit()

                except:
                    raise
                    # error = f"User {username} is already registered."
                else:
                    shops = db_session.query(Shop).all()
                    return render_template("shop/shoplist.html", shops=shops)

            flash(error)

        return render_template('shop/adminShop.html')

