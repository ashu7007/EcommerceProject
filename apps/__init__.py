import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
# from dbConfig import db
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
# app.config.from_pyfile(config_filename)
app.config['SECRET_KEY'] = 'qwerty'
Bootstrap(app)



# DB configuration
username = 'admin'
password = 'admin'
host_url = 'localhost'
port = '5433'
# db_name = 'ecommerce'
db_name = 'testShop'

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db_name}'.format(
    user=username, pw=password, url=host_url,  db_name=db_name)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db_sql=SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
app.config['FLASK_APP'] = "apps"
app.config['FLASK_ENV'] = "development"
# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db_sql.create_all()
# db.init_app(app)
# app.config.from_mapping(SECRET_KEY='dev',)

from apps.users import view
app.register_blueprint(view.bp)

from apps.shop import views
app.register_blueprint(views.bp)

from apps.products import views
app.register_blueprint(views.prod_bp)


#custom filter
from apps.products.models import Product
from apps.users.models import OrderDetail, Orders

@app.route("/", methods=['POST', 'GET'])
def welcome():
    """Welcome app page"""
    return "<h1>Welcome to the shopping platform </h1>"

@app.template_filter('product_name')
def product_name(id):
    product = Product.query.filter(Product.id==id).first()
    return product.product_name

@app.template_filter('product_price')
def product_price(id):
    product = Product.query.filter(Product.id==id).first()
    return product.price

@app.template_filter('product_brand')
def product_brand(id):
    product = Product.query.filter(Product.id==id).first()
    return product.brand

@app.template_filter('total_price')
def total_price(id):
    orderdetail = OrderDetail.query.filter(OrderDetail.order_id==id).all()
    total=0
    for data in orderdetail:
        total = total+(data.price*data.quantity)
    return total

@app.template_filter('customer_username')
def customer_username(order_id):
    order = Orders.query.filter(Orders.id==order_id).first()
    return order.user.username

@app.template_filter('customer_email')
def customer_email(order_id):
    order = Orders.query.filter(Orders.id==order_id).first()
    return order.user.email

@app.template_filter('customer_address')
def customer_address(order_id):
    order = Orders.query.filter(Orders.id==order_id).first()
    return order.user.address

# if __name__ == "__main__":
#     app.run(debug=True)

# def create_app():
#     app = Flask(__name__)
#     # app.config.from_pyfile(config_filename)
#     app.config['SECRET_KEY'] = 'qwerty'
#     Bootstrap(app)

#     # DB configuration
#     username = 'admin'
#     password = 'admin'
#     host_url = 'localhost'
#     port = '5432'
#     db_name = 'ecommerce'
#     DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{port}/{db_name}'.format(
#         user=username, pw=password, url=host_url, port=port, db_name=db_name)
#     # app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#     db_sql=SQLAlchemy(app)
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

#     # configuration of mail
#     app.config['MAIL_SERVER'] = 'smtp.gmail.com'
#     app.config['MAIL_PORT'] = 465
#     app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
#     app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
#     app.config['MAIL_USE_TLS'] = False
#     app.config['MAIL_USE_SSL'] = True

#     db.init_app(app)
#     # app.config.from_mapping(SECRET_KEY='dev',)

#     from apps.users import view
#     app.register_blueprint(view.bp)

#     from apps.shop import views
#     app.register_blueprint(views.bp)

#     from apps.products import views
#     app.register_blueprint(views.prod_bp)
#     # from apps.shop.views import ShopAPI ,AdminShop
#     # shop_view = ShopAPI.as_view('shop_api')
#     # app.add_url_rule('/shop/', defaults={'id': None},
#     #                 view_func=shop_view, methods=['GET',])
#     #app.add_url_rule('/shop/','shop' ,view_func=shop_view, methods=['POST',])
#     # app.add_url_rule('/shop/<id>','shop', view_func=shop_view,
#     #                 methods=['GET', 'PUT', 'DELETE'])
#     # app.add_url_rule('/addshop', 'addshop',view_func=AdminShop.as_view('admin_shop'))

#     return app
