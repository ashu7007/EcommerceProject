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
# username = 'admin'
# password = 'admin'
# host_url = 'localhost'
# port = '5432'
# db_name = 'testShop'

# DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db_name}'.format(
#     user=username, pw=password, url=host_url,  db_name=db_name)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
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
app.add_url_rule('/auth/login', view_func=view.Login.as_view(name='auth.login'))
app.add_url_rule('/auth/verify', view_func=view.VerifyOTP.as_view(name='auth.verify'))
app.add_url_rule('/auth/register', view_func=view.Register.as_view(name='auth.register'))
app.add_url_rule('/auth/shop_user_register', view_func=view.RegisterShopUser.as_view(name='auth.shop_user_register'))
app.add_url_rule('/auth/logout', view_func=view.Logout.as_view(name='auth.logout'))
app.add_url_rule('/auth/reset_password/<token>', view_func=view.ResetPassword.as_view(name='auth.reset_token'))
app.add_url_rule('/auth/forgot_password', view_func=view.ForgotPassword.as_view(name='auth.forgot_password'))
app.add_url_rule('/auth/update_profile', view_func=view.UpdateProfile.as_view(name='auth.update_profile'))
app.add_url_rule('/auth/reject_shop/<id>', view_func=view.RejectShop.as_view(name='auth.reject_shop'))
app.add_url_rule('/auth/approval_shop/<id>', view_func=view.ApprovalShop.as_view(name='auth.approval_shop'))
app.add_url_rule('/auth/delete_cart/<prod_id>', view_func=view.DeleteCart.as_view(name='auth.delete_cart'))
app.add_url_rule('/auth/add_cart/<prod_id>/<page>', view_func=view.AddCart.as_view(name='auth.add_cart'))
app.add_url_rule('/auth/cart', view_func=view.CartView.as_view(name='auth.cart'))
app.add_url_rule('/auth/delete_wishlist/<prod_id>', view_func=view.DeleteWishlist.as_view(name='auth.delete_wishlist'))
app.add_url_rule('/auth/add_wishlist/<prod_id>', view_func=view.AddWishlist.as_view(name='auth.add_wishlist'))
app.add_url_rule('/auth/orders', view_func=view.OrdersView.as_view(name='auth.orders'))
app.add_url_rule('/auth/cancel_order/<order_id>', view_func=view.CancelOrder.as_view(name='auth.cancel_order'))
app.add_url_rule('/auth/order_detail/<order_id>', view_func=view.OrderDetailView.as_view(name='auth.order_detail'))
app.add_url_rule('/auth/place_order', view_func=view.PlaceOrder.as_view(name='auth.place_order'))
app.add_url_rule('/auth/wishlist', view_func=view.WishlistView.as_view(name='auth.wishlist'))
app.add_url_rule('/auth/product_list', view_func=view.ProductList.as_view(name='auth.product_list'))
app.add_url_rule('/auth/shop_approval_list', view_func=view.ShopApprovalList.as_view(name='auth.shop_approval_list'))
app.add_url_rule('/auth/add_user', view_func=view.AddUser.as_view(name='auth.add_user'))
app.add_url_rule('/auth/user_list', view_func=view.UserList.as_view(name='auth.user_list'))
app.add_url_rule('/auth/shop_sale/', view_func=view.ShopSale.as_view(name='auth.shop_sale'))
app.add_url_rule('/auth/admin_sale', view_func=view.AdminSale.as_view(name='auth.admin_sale'))
app.add_url_rule('/auth/all_orders', view_func=view.AllOrders.as_view(name='auth.all_orders'))
app.add_url_rule('/auth/all_category', view_func=view.AllCategory.as_view(name='auth.all_category'))
app.add_url_rule('/auth/all_product', view_func=view.AllProduct.as_view(name='auth.all_product'))
app.add_url_rule('/auth/admin_dashboard', view_func=view.AdminDashboard.as_view(name='auth.admin_dashboard'))
app.add_url_rule('/auth/order_for_shopuser', view_func=view.OrderForShopuser.as_view(name='auth.order_for_shopuser'))

from apps.shop import views
# app.register_blueprint(views.bp)
app.add_url_rule('/shop/list_shop', view_func=views.ListShop.as_view(name='shop.list_shop'))
app.add_url_rule('/shop/create_shop', view_func=views.CreateShop.as_view(name='shop.create_shop'))
app.add_url_rule('/shop/delete_shop/<id>', view_func=views.AdminDeleteShop.as_view(name='shop.delete_shop'))
app.add_url_rule('/shop/update_shop/<id>', view_func=views.UpdateShop.as_view(name='shop.update_shop'))

from apps.products import views
# app.register_blueprint(views.prod_bp)
app.add_url_rule('/product', view_func=views.ShopDashboard.as_view(name='product.shop_dashboard'))
app.add_url_rule('/product/add_category', view_func=views.AddCategory.as_view(name='product.add_category'))
app.add_url_rule('/product/update_category/<cat_id>', view_func=views.UpdateCategory.as_view(name='product.update_category'))
app.add_url_rule('/product/create_product', view_func=views.CreateProduct.as_view(name='product.create_product'))
app.add_url_rule('/product/delete/<id>', view_func=views.DeleteProduct.as_view(name='product.delete'))
app.add_url_rule('/product/update_product/<id>', view_func=views.UpdateProduct.as_view(name='product.update_product'))


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
