"""Operation related to user"""
import os
import datetime
import functools
from random import randint
from flask_mail import Mail, Message
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for, abort, current_app)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from apps.users.models import Userdata, OTP, Shop, ShopRejection, Wishlist, Cart, Orders, OrderDetail, Status, Payment
from apps.products.models import Product, Category

# from dbConfig import db


# some_engine = create_engine('postgresql+psycopg2://admin:admin@localhost/ecommerce')
some_engine = create_engine('postgresql+psycopg2://admin:admin@localhost:5432/testShop')
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=some_engine))
Session = sessionmaker(bind=some_engine)

db_session = Session()

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/shop_orders")
def order_for_shopuser():
    """order received by shop"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_shopuser:
        shop_user = Userdata.query.filter(Userdata.id == user.id).first()
        ids = [product.id for product in shop_user.product]
        orders = OrderDetail.query.filter(OrderDetail.product_id.in_(ids)).all()
        return render_template("user/shopOrders.html", orders=orders)


@bp.route("/admin_dashboard/", methods=['POST', 'GET'])
def admin_dashboard():
    """to show admin dashboard"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    shops = Shop.query.filter(Shop.active == True).all()
    brand = Product.query.distinct(Product.brand)
    customer = Userdata.query.filter(Userdata.is_customer == True).all()

    if user.is_admin and request.method == 'POST':
        if request.form.get('shop_products'):
            products = Product.query.filter(Product.shop_id == request.form.get('shop_products')).all()
            return render_template("admindashboard.html", shops=shops, brand=brand
                                   , customer=customer, products=products)

        if request.form.get('shop_orders'):
            shop = Shop.query.filter(Shop.id == request.form.get('shop_orders')).first()
            shop_user = Userdata.query.filter(Userdata.id == shop.user_id).first()
            ids = [product.id for product in shop_user.product]
            shop_orders = OrderDetail.query.filter(OrderDetail.product_id.in_(ids)).all()
            return render_template("admindashboard.html", shops=shops, brand=brand
                                   , customer=customer, shop_orders=shop_orders)

        if request.form.get('customer_orders'):
            customer_order = Orders.query.filter(Orders.user_id == request.form.get('customer_orders')).all()
            return render_template("admindashboard.html", shops=shops, brand=brand,
                                   customer=customer, customer_order=customer_order, )

    return render_template("admindashboard.html", shops=shops, brand=brand, customer=customer)


@bp.route("/all_product/", methods=['POST', 'GET'])
def all_product():
    """to show all product"""
    # r_user_id = session.get('r_user_id')
    # user = db_session.query(Userdata).get(r_user_id)
    products = Product.query.all()
    return render_template("product/allProduct.html", products=products)

@bp.route("/all_category/", methods=['POST', 'GET'])
def all_category():
    """to show all product"""
    # r_user_id = session.get('r_user_id')
    # user = db_session.query(Userdata).get(r_user_id)
    category = Category.query.all()
    return render_template("product/allcategory.html", category=category)

@bp.route("/all_orders/", methods=['POST', 'GET'])
def all_orders():
    """to show all orders"""

    # r_user_id = session.get('r_user_id')
    # user = db_session.query(Userdata).get(r_user_id)
    orders = Orders.query.all()
    return render_template("product/allorders.html", orders=orders)


@bp.route("/admin_sale/", methods=['POST', 'GET'])
def admin_sale():
    """to show all sale to admin user"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    shops = Shop.query.filter(Shop.active == True).all()
    category = Category.query.all()
    brand = Product.query.distinct(Product.brand)
    if user.is_admin and request.method == 'POST':

        if request.form.get('shop'):
            wise = "shop"
            data = Shop.query.get(request.form.get('shop'))
            product = db_session.query(Product).filter(Product.shop_id == request.form.get('shop'))

        if request.form.get('category'):
            wise = "category"
            data = Category.query.get(request.form.get('category'))
            product = db_session.query(Product).filter(Product.category_id == request.form.get('category'))

        if request.form.get('brand'):
            wise = "brand"
            data = request.form.get('brand')
            product = db_session.query(Product).filter(Product.brand == request.form.get('brand'))

        sold = product.with_entities(func.sum(Product.sold_quantity)).scalar()
        total = product.with_entities(func.sum(Product.stock_quantity)).scalar()
        return render_template("adminSaleDashboard.html", shops=shops, category=category,
                               brand=brand, total_qnt=total, total_sold=sold, wise=wise, data=data)

    return render_template("adminSaleDashboard.html", shops=shops, category=category, brand=brand,
                           total_qnt=None, total_sold=None, wise=None, data=None)


@bp.route("/shop_sale/", methods=['POST', 'GET'])
def shop_sale():
    """to show all sale to shop user"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    total_qnt = 0
    total_sold = 0
    category = Category.query.all()
    brand = Product.query.distinct(Product.brand)

    if user.is_shopuser and request.method == 'POST':
        data = request.form.get('data')

        if data.isdigit():
            product = Product.query.filter(Product.category_id == int(data), Product.user_id == user.id).all()
        else:
            product = Product.query.filter(Product.brand == data, Product.user_id == user.id).all()
        for prod in product:
            total_qnt = total_qnt + prod.stock_quantity
            total_sold = total_sold + prod.sold_quantity
        return render_template("shopdashboard.html", category=category,
                               brand=brand, total_qnt=total_qnt, total_sold=total_sold)
    return render_template("shopdashboard.html", category=category, brand=brand)


@bp.route("/user_list")
def user_list():
    """to show all users admin user"""

    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_admin:
        users = db_session.query(Userdata).filter(
            (Userdata.is_customer == True) |
            (Userdata.is_shopuser == True)).all()
        return render_template("user/userlist.html", users=users)


@bp.route("/add_user", methods=['GET', 'POST'])
def add_user():
    """to add users"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_admin:
        if request.method == 'POST':
            full_name = request.form['full_name']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            address = request.form['address']
            gender = request.form['gender']
            dob = request.form['dob']
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'password is required.'
            elif not full_name:
                error = 'full name is required.'
            elif not email:
                error = 'email is required.'
            elif not address:
                error = 'address is required.'
            elif not gender:
                error = 'gender is required.'
            elif not dob:
                error = 'dob is required.'
            date = datetime.datetime.now()

            if error is None:
                try:
                    user = Userdata(full_name=full_name, email=email, username=username,
                                    password=generate_password_hash(password),
                                    address=address, gender=gender, dob=dob, active=True, is_admin=False,
                                    is_customer=True,
                                    is_shopuser=False, created_at=date,
                                    updated_at=date)
                    db_session.add(user)
                    db_session.commit()

                except:
                    raise
                    # error = f"User {username} is already registered."
                else:
                    return redirect(url_for("auth.user_list"))
        return render_template('user/addUser.html')


@bp.route("/shop_approval_list")
def shop_approval_list():
    """to show all shop approval shop to admin user"""

    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_admin:
        shops = db_session.query(Shop).all()

        return render_template("user/shoplist.html", shops=shops)
    return redirect(url_for("auth.login"))


@bp.route("/product_list", methods=['GET', 'POST'])
def product_list():
    """to show all products user"""
    category = Category.query.all()
    brand = Product.query.distinct(Product.brand)

    search = request.args.get('search')  # product_name
    sort = request.args.get('sort')  # price , rating
    # filterBy = request.args.get('filterBy')  # category, prices, brand,

    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=6)

    if request.method == 'POST':
        min, max = request.form.get('price').split('-')
        cat = request.form.get('category')
        brd = request.form.get('brand')

        products = Product.query.filter(Product.price > int(min), Product.price < int(max),
                                        Product.category_id == cat, Product.brand == brd).paginate(page=page, per_page=6)
        return render_template("index.html", products=products, user=search,
                               category=category, brand=brand)
    if search:
        products = Product.query.filter(Product.product_name.like("%" + search + "%")).paginate(page=page, per_page=6)

    if sort == 'price':
        if request.args.get('price') == 'high':
            products = Product.query.order_by(Product.price.desc()).paginate(page=page, per_page=6)
        else:
            products = Product.query.order_by(Product.price.asc()).paginate(page=page, per_page=6)

    return render_template("index.html", products=products, user=search,
                           category=category, brand=brand)


@bp.route("/wishlist", methods=['POST', 'GET'])
def wishlist():
    """to show  wishlist user"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_customer:
        wish = db_session.query(Wishlist).filter(Wishlist.user_id == r_user_id).first()
        products = db_session.query(Product).filter(Product.id.in_(wish.product_id)).all()
        if wish:
            return render_template("user/wishlish.html", products=products)
        else:
            return redirect(url_for("auth.product_list"))


@bp.route("/place_order")
def place_order():
    """function to place order"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    date = datetime.datetime.now()
    if user.is_customer:
        cart = db_session.query(Cart).filter(Cart.user_id == r_user_id).first()
        order = Orders(user_id=r_user_id, status=Status.StatusInit, payment=Payment.paid,
                       created_at=date, updated_at=date)
        db_session.add(order)
        db_session.commit()
        for item, qnt in cart.items.items():
            product = db_session.query(Product).filter(Product.id == item).first()
            orderdetail = OrderDetail(order_id=order.id, product_id=item,
                                      quantity=qnt, price=product.price,
                                      created_at=date, updated_at=date)
            db_session.add(orderdetail)
            product.sold_quantity=product.sold_quantity+qnt
            db_session.query(Product).filter(Product.id == item).update({'sold_quantity':product.sold_quantity})
            db_session.commit()

        db_session.query(Cart).filter(Cart.id == cart.id).update({'items': {}})
        db_session.commit()
        return redirect(url_for("auth.product_list"))
    return redirect(url_for("auth.login"))


@bp.route("/order_detail/<order_id>")
def order_detail(order_id):
    """to show order detail of user"""

    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user:
        order_detail = db_session.query(OrderDetail).filter(OrderDetail.order_id == order_id).all()
        return render_template("user/orderDetail.html", order_detail=order_detail, order_id=order_id)
    return abort(401, "You have to provide either 'url' or 'text', too")


@bp.route("/cancel_order/<order_id>")
def cancel_order(order_id):
    """to cancel user order"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_customer:
        db_session.query(Orders).filter(Orders.id == order_id).update({'status': Status.StatusCancelled})
        db_session.commit()
        return redirect(url_for("auth.orders"))


@bp.route("/orders")
def orders():
    """to show users orders"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    if user.is_customer:
        orders = Orders.query.all()
        return render_template('user/orderlist.html', orders=orders)
    return redirect(url_for("auth.login"))


@bp.route("/add_wishlist/<prod_id>", methods=['POST', 'GET'])
def add_wishlist(prod_id):
    """to add product on wishlist"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    date = datetime.datetime.now()

    if user.is_customer and prod_id:
        wish_list = db_session.query(Wishlist).filter(Wishlist.user_id == r_user_id).first()
        if not wish_list:
            wishlist = Wishlist(user_id=user.id, product_id=[prod_id], created_at=date,
                                updated_at=date)
            db_session.add(wishlist)
            db_session.commit()
        else:
            wl_id = wish_list.product_id
            wl_id.append(int(prod_id))
            db_session.query(Wishlist).filter(Wishlist.id == wish_list.id).update({'product_id': list(set(wl_id))})
            db_session.commit()
        return redirect(url_for("auth.product_list"))
    return redirect(url_for("auth.login"))


@bp.route("/delete_wishlist/<prod_id>", methods=['POST', 'GET'])
def delete_wishlist(prod_id):
    """to delete product from wishlish"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)

    if user.is_customer and prod_id:
        wish_list = db_session.query(Wishlist).filter(Wishlist.user_id == r_user_id).first()
        wl_id = wish_list.product_id
        wl_id.remove(int(prod_id))
        db_session.query(Wishlist).filter(Wishlist.id == wish_list.id).update({'product_id': list(set(wl_id))})
        db_session.commit()
        return redirect(url_for("auth.wishlist"))


@bp.route("/cart", methods=['POST', 'GET'])
def cart():
    """to show cart of user"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)

    if user.is_customer:
        cart = db_session.query(Cart).filter(Cart.user_id == r_user_id).first()
        # ids = [id for id in cart.items.keys()]
        # qty = [qt for qt in cart.items.values()]
        # products = db_session.query(Product).filter(Product.id.in_(ids)).all()
        if cart:
            return render_template("user/cart.html", cart=cart)
        return render_template("user/cart.html")


@bp.route("/add_cart/<prod_id>/<page>", methods=['POST', 'GET'])
def add_cart(prod_id, page):
    """to add product in cart"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)
    date = datetime.datetime.now()

    wl = db_session.query(Wishlist).filter(Wishlist.user_id == r_user_id).first()

    if wl and int(prod_id) in wl.product_id:
        wl_id = wl.product_id
        wl_id.remove(int(prod_id))
        db_session.query(Wishlist).filter(Wishlist.id == wl.id).update({'product_id': list(set(wl_id))})
        db_session.commit()

    if user.is_customer and prod_id:
        cart = db_session.query(Cart).filter(Cart.user_id == r_user_id).first()
        if not cart:
            items = {}
            items[prod_id] = 1
            add_cart = Cart(user_id=user.id, items=items, created_at=date,
                            updated_at=date)
            db_session.add(add_cart)
            db_session.commit()
        else:
            items = cart.items
            if items.get(prod_id):
                items[prod_id] = items[prod_id] + 1
            else:
                items[prod_id] = 1
            db_session.query(Cart).filter(Cart.id == cart.id).update({'items': items})
            db_session.commit()
        if page == "wish":
            return redirect(url_for("auth.wishlist"))
        if page == "cart":
            return redirect(url_for("auth.cart"))
        if page == "index":
            return redirect(url_for("auth.product_list"))
    return redirect(url_for("auth.login"))


@bp.route("/delete_cart/<prod_id>", methods=['POST', 'GET'])
def delete_cart(prod_id):
    """to delete product from cart"""
    r_user_id = session.get('r_user_id')
    user = db_session.query(Userdata).get(r_user_id)

    # if user.is_customer and prod_id:
    #     cart = db_session.query(Cart).filter(Cart.user_id==r_user_id).first()
    #     cart_items=cart.items
    #     del cart_items[prod_id]
    #     db_session.query(Cart).filter(Cart.id == cart.id).update({'items': cart_items})
    #     db_session.commit()
    #     return redirect(url_for("auth.cart"))
    if user.is_customer and prod_id:
        cart = db_session.query(Cart).filter(Cart.user_id == r_user_id).first()
        items = cart.items
        if items.get(prod_id) > 0:
            items[prod_id] = items[prod_id] - 1
            if items.get(prod_id) <= 0:
                del items[prod_id]
        else:
            del items[prod_id]
        db_session.query(Cart).filter(Cart.id == cart.id).update({'items': items})
        db_session.commit()
        return redirect(url_for("auth.cart"))
    return redirect(url_for("auth.login"))


@bp.route("/approval_shop/<id>")
def approval_shop(id):
    """function to approve shop"""
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
    """to reject shop application"""
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
    """function to register user"""
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        conpassword = request.form['conPassword']
        address = request.form['address']
        gender = request.form['gender']
        dob = request.form['dob']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'password is required.'
        elif conpassword != password:
            error = 'password not match.'
        elif not full_name:
            error = 'full name is required.'
        elif not email:
            error = 'email is required.'
        elif not address:
            error = 'address is required.'
        elif not gender:
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
    """to register shop user"""
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
    """to login user"""
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
            return redirect(url_for("shop.list_shop"))

        elif error is None and user.active and user.is_shopuser:
            shop = db_session.query(Shop).filter(Shop.user_id == user.id).first()
            if shop.active:
                session.clear()
                session['r_user_id'] = user.id
                return redirect(url_for("product.shop_dashboard"))
            error = "your shop is not approved yet"

        else:
            error = "Please verify your email to login"
        flash(error)

    return render_template('user/login.html')


@bp.route('/verify', methods=('POST',))
def verify():
    """ function to verify otp"""
    if request.method == 'POST':
        r_user_id = session.get('r_user_id')
        otp = int(request.form['otp'])
        otp_db = db_session.query(OTP).filter(OTP.user_id == r_user_id).order_by(desc(OTP.created_at)).first()
        if otp == otp_db.otp:
            db_session.query(Userdata).filter(Userdata.id == r_user_id).update({'active': True})
            # db_session.query(OTP).filter(OTP.user_id == r_user_id).order_by(desc(OTP.created_at)).first().delete()
            db_session.query(OTP).filter(OTP.id == otp_db.id).delete()
            db_session.commit()
            return redirect(url_for("auth.login"))
        return "incorrect Otp"
    return abort(401, "You have to provide either 'url' or 'text', too")


@bp.route('/logout')
def logout():
    """to logout user"""
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
    """to reset token"""
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
        elif confirm_pass is None:
            error = 'confimr password is required field.'
        elif password != confirm_pass:
            error = 'password dont match.'

        if not error:
            db_session.query(Userdata).filter(Userdata.id == user.id).update({'password': generate_password_hash(password)})
            db_session.commit()
            flash('Your password has been updated! You are now able to log in', 'success')
            return redirect(url_for('auth.login'))
    return render_template('user/resetpassword.html')


@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """to reset password"""
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
    """update user profile"""
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
                update_object["updated_at"] = date
                db_session.query(Userdata).filter(Userdata.id == r_user_id).update(update_object)
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
