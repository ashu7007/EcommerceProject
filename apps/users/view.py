import os
import datetime
import functools
from random import randint
from flask import current_app
from flask_mail import Mail, Message
from flask import jsonify
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from .models import Userdata, OTP, Shop, ShopRejection, Wishlist
from apps.products.models import Product

from dbConfig import db

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session

# some_engine = create_engine('postgresql://postgres:postgres@localhost/')
some_engine = create_engine('postgresql+psycopg2://admin:admin@localhost/ecommerce')
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=some_engine))
Session = sessionmaker(bind=some_engine)

db_session = Session()

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/shop_approval_list")
def shop_approval_list():
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_admin:
        shops = db_session.query(Shop).all()

        return render_template("user/shoplist.html", shops=shops)
    return redirect(url_for("auth.login"))

@bp.route("/product_list")
def product_list():
    #page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    #products = db_session.query(Product).paginate(page=page, per_page=5)
    
    
    products = db_session.query(Product).all()

    # results = [product.format() for product in products]
    # print(results)
    # print(len(results))
    # return jsonify({
    # 'success':True,
    # 'results':results,
    # 'count':len(results)
    # })
    print(products)
    return render_template("index.html", products=products)

@bp.route("/wishlist", methods=['POST','GET'])
def wishlist():
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_customer:
        wl = db_session.query(Wishlist).filter(Wishlist.user_id==r_user_id).first()
        if wl:
            return render_template("user/wishlish.html", wishlist=wl)
        else:
            return redirect(url_for("auth.product_list"))


@bp.route("/add_wishlist/<prod_id>", methods=['POST','GET'])
def add_wishlist(prod_id):
    
    print("wishlist:",request.method)
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    date = datetime.datetime.now()
    print("wishlist:",prod_id)
    if user.is_customer and prod_id:
        wl = db_session.query(Wishlist).filter(Wishlist.user_id==r_user_id).first()
        print(wl)
        if not wl:
            wishlist = Wishlist(user_id=user.id, product_id=[prod_id],created_at=date,
                                   updated_at=date)
            db_session.add(wishlist)
            db_session.commit()
        else:
            wl_id=wl.product_id
            print(type(wl_id))
            print(wl_id)
            wl_id.append(int(prod_id))
            print(wl_id)
            db_session.query(Wishlist).filter(Wishlist.id == wl.id).update({'product_id': wl_id })
            db_session.commit()
        wl = db_session.query(Wishlist).filter(Wishlist.user_id==r_user_id).first()
        return redirect(url_for("auth.product_list"))
    return redirect(url_for("auth.login"))

@bp.route("/user_list")
def user_list():
    users = db_session.query(Userdata).filter(Userdata.is_customer==True)
    return render_template("user/userlist.html", users=users)


@bp.route("/approval_shop/<id>")
def approval_shop(id):
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_admin:
        shops = db_session.query(Shop).all()
        db_session.query(Shop).filter(Shop.id == id).update({'active': True, 'status': 'Approved'})
        db_session.commit()

        return render_template("user/shoplist.html", shops=shops)
    return redirect(url_for("auth.login"))


@bp.route("/reject_shop/<id>", methods=('GET', 'POST'))
def reject_shop(id):
    if request.method == "POST":
        message = request.form.get('message')
        r_user_id = session.get('r_user_id')
        user = db_session.query(Userdata).get(r_user_id)
        date = datetime.datetime.now()

        if user.is_admin:
            shops = db_session.query(Shop).all()
            shop = db_session.query(Shop).filter(Shop.id == id).first()
            db_session.query(Shop).filter(Shop.id == id).update({'active': False, 'status': 'Rejected'})
            db_session.commit()
            reject = ShopRejection(user_id=shop.user_id, shop_id=id, description=message, created_at=date,
                                   updated_at=date)
            db_session.add(reject)
            db_session.commit()
            user = db_session.query(Userdata).filter(Userdata.id == shop.user_id).first()
            msg = Message(
                f'Rejection aknowlegment',
                sender='avaish@deqode.com',
                recipients=[user.email]
            )
            msg.body = f'your request for shop rejected because {message}'
            mail = Mail(current_app)
            mail.send(msg)

            return render_template("user/shoplist.html", shops=shops)
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        gender = request.form['gender']
        dob = request.form['dob']
        # user_type = request.form['user_type']
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
        elif not dob:
            error = 'dob is required.'
        date = datetime.datetime.now()

        if error is None:
            try:
                user = Userdata(full_name=full_name, email=email, username=username,
                                password=generate_password_hash(password),
                                address=address, gender=gender, dob=dob, active=False, is_admin=False, is_customer=True,
                                is_shopuser=False, created_at=date,
                                updated_at=date)
                db_session.add(user)
                db_session.commit()

            except:
                raise
                # error = f"User {username} is already registered."
            else:
                otp = randint(1001, 9999)
                otp_object = OTP(user_id=user.id, otp=otp, created_at=date, updated_at=date)
                db_session.add(otp_object)
                db_session.commit()
                msg = Message(
                  f'your otp is {otp}',
                    sender='avaish@deqode.com',
                    recipients=[email]
                )
                msg.body = f'your otp is {otp}'
                mail = Mail(current_app)
                mail.send(msg)
                session['r_user_id'] = user.id
                return render_template('user/confirmEmail.html')
                # return redirect(url_for("auth.login"))

        flash(error)

    return render_template('user/register.html')


@bp.route("/shop_user_register", methods=['GET', 'POST'])
def shop_user_register():
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
                shop_object = Shop(user_id=user.id, store_name=store_name, description=description, active=False,
                                   created_at=date, updated_at=date)
                db_session.add(shop_object)
                db_session.commit()

            except:
                raise
                # error = f"User {username} is already registered."
            else:
                otp = randint(1001, 9999)
                otp_object = OTP(user_id=user.id, otp=otp, created_at=date, updated_at=date)
                db_session.add(otp_object)
                db_session.commit()

                # send OTP to user
                msg = Message(
                    f'your otp is {otp}',
                    sender='avaish@deqode.com',
                    recipients=[email]
                )
                msg.body = f'your otp is {otp}'
                mail = Mail(current_app)
                mail.send(msg)

                # send email link to admin for approval
                msg = Message('Approval Needed for shop',
                              sender=os.environ.get("MAIL_USERNAME"),
                              recipients=[os.environ.get("MAIL_USERNAME")])
                mail = Mail(current_app)
                format_url = url_for('auth.shop_approval_list', _external=True)
                msg.body = f"To reset your password, visit the following link: {format_url}"
                mail.send(msg)

                session['r_user_id'] = user.id
                return render_template('user/confirmEmail.html')
                # return redirect(url_for("auth.login"))

        flash(error)

    return render_template('user/shopUserRegister.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        error = None
        user = db_session.query(Userdata).filter(Userdata.username == user_name).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        elif error is None and user.active and user.is_customer:
            session.clear()
            session['r_user_id'] = user.id
            return redirect(url_for("auth.product_list"))

        elif error is None and user.active and user.is_admin:
            session.clear()
            session['r_user_id'] = user.id
            # shops = db_session.query(Shop).all()
            return redirect(url_for("shop.list_shop"))
            # return render_template("user/shoplist.html", shops=shops)

        elif error is None and user.active and user.is_shopuser:
            shop = db_session.query(Shop).filter(Shop.user_id == user.id).first()
            if shop.active:
                session.clear()
                session['r_user_id'] = user.id
                return redirect(url_for("product.shop_dashboard"))
            else:
                error = "your shop is not approved yet"

        else:
            error = "Please verify your email to login"
        flash(error)

    return render_template('user/login.html')


@bp.route('/verify', methods=('POST',))
def verify():
    if request.method == 'POST':
        r_user_id = session.get('r_user_id')
        otp = int(request.form['otp'])
        error = None
        otp_db = db_session.query(OTP).filter(OTP.user_id == r_user_id).order_by(desc(OTP.created_at)).first()
        if otp == otp_db.otp:
            db_session.query(Userdata).filter(Userdata.id == r_user_id).update({'active': True})
            # db_session.query(OTP).filter(OTP.user_id == r_user_id).order_by(desc(OTP.created_at)).first().delete()
            db_session.query(OTP).filter(OTP.id == otp_db.id).delete()
            db_session.commit()
            return redirect(url_for("auth.login"))
        return "incorrect Otp"


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# @app.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('login'))
#     return render_template('reset_request.html', title='Reset Password', form=form)


@bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    user_id = Userdata.verify_reset_token(token)
    user = db_session.query(Userdata).get(user_id)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_pass = request.form.get('confirm_pass')

        if password is None:
            error = 'password is required field.'
        if confirm_pass is None:
            error = 'confimr password is required field.'
        elif password != confirm_pass:
            error = 'password dont match.'

        db_session.query(Userdata).filter(Userdata.id == user.id).update({'password': generate_password_hash(password)})
        db_session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('user/resetpassword.html')


@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        user = db_session.query(Userdata).filter_by(username=username).first()
        token = user.get_reset_token()
        msg = Message('Password Reset Request',
                      sender=os.environ.get("MAIL_USERNAME"),
                      recipients=[user.email])
        mail = Mail(current_app)
        format_url = url_for('auth.reset_token', token=token, _external=True)
        msg.body = f"To reset your password, visit the following link: {format_url}"
        mail.send(msg)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('user/forgetpass.html')


@bp.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        # email = request.form.get('email')
        # username = request.form.get('username')
        # password = request.form.get('password')
        address = request.form.get('address')
        gender = request.form.get('gender')
        dob = request.form.get('dob')
        error = None

        # if not username:
        #     error = 'username is required.'
        # if not password:
        #     error = 'password is required.'
        if not full_name:
            error = 'full name is required.'
        # if not email:
        #     error = 'email is required.'
        if not address:
            error = 'address is required.'
        if not gender:
            error = 'gender is required.'
        # if not user_type or user_type not in ['customer','Shopuser']:
        #     error = 'user_type should be customer or Shopuser .'
        elif not dob:
            error = 'dob is required.'
        date = datetime.datetime.now()
        print(error)
        if error is None:
            try:
                r_user_id = session.get('r_user_id')
                user = db_session.query(Userdata).get(r_user_id)
                print(user)
                update_object = {}
                if full_name and user.full_name != full_name:
                    update_object["full_name"] = full_name
                # if username and user.username != username:
                #     update_object["username"] = username
                # if password and not check_password_hash(user.password, password):
                #     update_object["password"] = password
                if address and user.address != address:
                    update_object["address"] = address
                if gender and user.gender != gender:
                    update_object["gender"] = gender
                if dob and user.dob != dob:
                    update_object["dob"] = dob
                print(update_object)
                user = db_session.query(Userdata).filter(Userdata.id == r_user_id).update(update_object)
                db_session.commit()

            except:
                raise
                # error = f"User {username} is already registered."
            else:
                #     otp = randint(1001,9999)
                #     otp_object= OTP(user_id=user.id,otp=otp,created_at=date,updated_at=date)
                #     db_session.add(otp_object)
                #     db_session.commit()
                #     msg = Message(
                #     f'your otp is {otp}',
                #     sender ='avaish@deqode.com',
                #     recipients = [email]
                #    )
                #     msg.body = f'your otp is {otp}'
                #     mail = Mail(current_app)
                #     mail.send(msg)
                #     session['r_user_id'] = user.id
                #     return render_template('user/confirmEmail.html')
                return render_template('index.html')

    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    return render_template('user/updateProfile.html', user=user)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('r_user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_session.query(Userdata).filter(Userdata.id == user_id).first()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
