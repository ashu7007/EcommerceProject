# import unittest
# from flask import g
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from flask import Flask , g
from flask_sqlalchemy import SQLAlchemy

# from apps import app


import unittest
from apps import app
from apps.users.models import Userdata, Shop, Wishlist
from apps.products.models import Category, Product



db= SQLAlchemy(app)
date = datetime.datetime.now()


class BaseTestCase(unittest.TestCase):


    def setUp(self):
        app.config['SECRET_KEY'] = "89566"
        self.db_uri = 'postgresql+psycopg2://admin:admin@localhost/testdb'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        self.app = app.test_client()
        db.create_all()

    
    # def test_user_models(self):
        #Create a customer user
        # admin = Userdata(full_name="admin", email="avaish@deqode.com", 
        #                     username="admin", 
        #                     password=generate_password_hash("admin"),
        #                     address="address", gender="male", dob=date, 
        #                     active=True, is_admin=True,
        #                     is_customer=False,is_shopuser=False, 
        #                     created_at=date,updated_at=date)
        # shopuser = Userdata(full_name="shopuser", email="email@123.com", 
        #                     username="shopuser", 
        #                     password=generate_password_hash("demo"),
        #                     address="address", gender="male", dob=date, 
        #                     active=True, is_admin=False,
        #                     is_customer=False,is_shopuser=True, 
        #                     created_at=date,updated_at=date)
        # user = Userdata(full_name="full_name", email="email@123.com", 
        #                     username="user", 
        #                     password=generate_password_hash("demo"),
        #                     address="address", gender="male", dob=date, 
        #                     active=True, is_admin=False,
        #                     is_customer=True,is_shopuser=False, 
        #                     created_at=date,updated_at=date)
        # db.session.add(admin)
        # db.session.add(shopuser)
        # db.session.add(user)
        # db.session.commit()
        # shop_object = Shop(user_id=shopuser.id, store_name="store_name", description="description", active=True,
        #                                 status="Approved",
        #                             created_at=date, updated_at=date)
        # db.session.add(shop_object)
        # db.session.commit()
        # #Check that all users exist
        # category = Category(user_id=11,
        #                                 category_name="category_data",
        #                                 active=True, created_at=date,
        #                                 updated_at=date)
        # p=Product(user_id=11, shop_id=2,
        #                             category_id=1,
        #                             product_name="product_name",
        #                             stock_quantity=50,
        #                             sold_quantity=0, brand="brand", price=42,
        #                             active=True, created_at=date,
        #                             updated_at=date)
        # w= Wishlist(user_id=11, product_id=[58], created_at=date,
        #                             updated_at=date)
        # db.session.add(w)
        # db.session.commit()
        # assert len(Userdata.query.all()) == 1
    
    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()


class UserTest(BaseTestCase):
    """to test user specific test case"""

    def test_get_login_page(self):
        """to test login page"""
        tester = app.test_client(self)
        response = tester.get('/auth/login',content_type='html/text')
        self.assertEqual(response.status_code,200)

    def test_login_admin(self):
        """to test login for admin"""
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            self.assertIn(b'admin', response.data)
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(response.status_code,200)

    def test_login_shop(self):
        """to test login for shop user"""

        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'shopuser', password='demo'), follow_redirects=True)
            self.assertIn(b'shopuser', response.data)
            self.assertTrue(g.user.is_shopuser == True)
            self.assertEqual(response.status_code,200)
    
    def test_login_customer(self):
        """to test login for customer"""

        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'user', password='demo'), follow_redirects=True)
            self.assertIn(b'user', response.data)
            self.assertTrue(g.user.is_customer == True)
            self.assertTrue(g.user.is_admin == False)
            self.assertEqual(response.status_code,200)


    def test_get_login_page(self):
        """to test login page"""
        tester = app.test_client(self)
        response = tester.get('/auth/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_admin_user(self):
        """to test login func"""
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            self.assertIn(b'admin', response.data)
            # self.assertTrue(g.user.is_shopuser == True)
            self.assertEqual(response.status_code, 200)

    def test_login_customer_user(self):
        """to test login func"""
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='user', password='demo'), follow_redirects=True)
            self.assertIn(b'user', response.data)
            self.assertTrue(g.user.is_customer == True)
            self.assertEqual(response.status_code, 200)

    def test_login_shop_user(self):
        """to test login func"""
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='shop', password='demo'), follow_redirects=True)
        self.assertIn(b'shop', response.data)
        # self.assertTrue(g.user.is_shopuser == True)
        self.assertEqual(response.status_code, 200)

    def test_incorrect_login(self):
        """to test incorrect login"""
        tester = app.test_client(self)
        response = tester.post(
            '/auth/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Incorrect username.', response.data)

    def test_get_register_page(self):
        """to test get register page"""

        tester = app.test_client(self)
        response = tester.get('/auth/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        """to test register user func"""
        tester = app.test_client(self)
        response = tester.post('/auth/register',
         data=dict(full_name ="demo",
        email = "test@123.com",
        username = "test@1232332",
        password ="test@123" ,
        conPassword ="test@123", 
        address = "test",
        gender = "male",
        dob ="2022-07-14 17:13:45.138" ), follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_register_user_failure(self):
        """to test register user failure"""

        tester = app.test_client(self)
        response = tester.post('/auth/register',
         data=dict(full_name ="demo",
        email = "test@123.com",
        username = "test@123",
        password ="test@123" ,
        conPassword ="test@123", 
        address = "test",
        gender = "male",
        dob ="2022-07-14 17:13:45.138" ), follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_get_shop_user_register_page(self):
        """to test get shop register page"""
        tester = app.test_client(self)
        response = tester.get('/auth/shop_user_register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_shop_user_register(self):
        tester = app.test_client(self)
        response = tester.post('/auth/shop_user_register',
         data=dict(full_name ="demo",
                    email = "test@123.com",
                    username = "test@123",
                    password ="test@123" ,
                    conpassword ="test@123", 
                    address = "test",
                    gender = "male",
                    dob ="2022-07-14 17:13:45.138",
                    store_name = 'store_name',
                    description = 'description'), follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_shop_user_register_failure(self):
        """to test shop user registeration  functionality"""
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/shop_user_register',
            data=dict(full_name ="demo",
                        email = "test@123.com",
                        username = "test@123",
                        password ="test@123" ,
                        conpassword ="test@123", 
                        address = "test",
                        gender = "male",
                        dob ="2022-07-14 17:13:45.138",
                        store_name = 'store_name',
                        description = 'description'), follow_redirects=True)
            self.assertEqual(response.status_code,200)
            self.assertIn(b'already',response.data)

    def test_verify_otp(self):
        """to test verify otp functionality"""

        tester = app.test_client(self)
        response = tester.post('/auth/verify',
         data=dict(otp ="4512"), follow_redirects=True)
        self.assertEqual(response.status_code,400)
        self.assertIn(b'no otp', response.data)

    def test_logout(self):
        """to test logout functionality"""
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.get('/auth/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    # def test_all_product(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/login',
    #      data=dict(username='admin', password='admin'), follow_redirects=True)
    #     response = tester.get('/auth/all_product', follow_redirects=True)
    #     self.assertEqual(response.status_code,200)

    def test_all_category(self):
        """to test all category"""

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/all_category', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_page(self):
        """to test forgot password page"""

        tester = app.test_client(self)
        response = tester.get('/auth/forgot_password', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_page_post(self):
        """to test forgot password page"""

        tester = app.test_client(self)
        response = tester.post('/auth/forgot_password',data=dict(username="user")
        , follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_page_post_error(self):
        """to test forgot password page"""

        tester = app.test_client(self)
        response = tester.post('/auth/forgot_password',data=dict(username="us1er")
        , follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_reset_token_page(self):
        """to test token reset"""

        tester = app.test_client(self)
        response = tester.get('/auth/reset_token/54754754475', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_reset_password_page(self):
        """to test token reset"""

        tester = app.test_client(self)
        response = tester.get('/auth/reset_password/1234', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_reset_password_post(self):
        """to test token reset"""

        tester = app.test_client(self)
        response = tester.post('/auth/reset_password/', 
                                data=dict(password="demo",
                                confirm_pass="demo"),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_update_profile_page(self):
        """to test update profile page"""
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = tester.get('/auth/update_profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_update_profile_page_post(self):
        """to test update profile page"""
        data = dict(full_name="update")
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = tester.post('/auth/update_profile',data=data,
         follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_update_profile_page_post(self):
        """to test update profile page"""
        data = dict()
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = tester.post('/auth/update_profile',data=data,
         follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # def test_order_for_shopuser_page(self):
    #     '''to test shop orders page'''
    #
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/login',
    #                            data=dict(username='shop4', password='demo'), follow_redirects=True)
    #     response = tester.get('/auth/shop_orders', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    def test_order_for_shopuser_page(self):
        '''to test shop orders page'''
        with app.app_context():
            tester = app.test_client(self)
            res = tester.post('/auth/login',
                                data=dict(username='shopuser', password='demo'), follow_redirects=True)
            response = tester.get('/auth/order_for_shopuser', follow_redirects=True)
            self.assertIn(b'order',response.data)
            self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_page(self):
        '''to test admin dashboard page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/admin_dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_post(self):
        '''to test admin dashboard page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/auth/admin_dashboard', 
                                data=dict(shop_products=2)
                                    ,follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = tester.post('/auth/admin_dashboard', 
                                data=dict(shop_orders=2)
                                    ,follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = tester.post('/auth/admin_dashboard', 
                                data=dict(customer_orders=2)
                                    ,follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_admin_sale_page(self):
        '''to test admin sale page'''
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.get('/auth/admin_sale', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_admin_sale_page_post(self):
        '''to test admin sale page'''
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.post('/auth/admin_sale',
                                    data=dict(shop=2),
                                     follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            response = tester.post('/auth/admin_sale',
                                    data=dict(category=2),
                                     follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            response = tester.post('/auth/admin_sale',
                                    data=dict(brand=2),
                                     follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_shop_sale_page(self):
        '''to test shop sale page'''
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='shopuser', password='demo'), follow_redirects=True)
            response = tester.get('/auth/shop_sale', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_shop_sale_page_post(self):
        '''to test shop sale page'''
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='shopuser', password='demo'), follow_redirects=True)
            response = tester.post('/auth/shop_sale',
                                    data=dict(data=2),
                                     follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            response = tester.post('/auth/shop_sale',
                                    data=dict(data="brand"),
                                     follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_user_list_page(self):
        '''to test user list page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/user_list', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_user_page(self):
        '''to test add user page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/add_user', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    # def test_add_user_page_post(self):
    #     '''to test add user page'''
    #     with app.app_context():
    #         data = dict(
    #                     full_name ="demo",
    #                     email = "test@123.com",
    #                     username = "te543t@123200",
    #                     password ="demo" ,
    #                     address = "test",
    #                     gender = "male",
    #                     dob ="2022-07-14 17:13:45.138" 
    #                                 )
    #         tester = app.test_client(self)
    #         response = tester.post('/auth/login',
    #                             data=dict(username='admin', password='admin')
    #                             , follow_redirects=True)
    #         response = tester.post('/auth/add_user',
    #                                 data=data
    #                                 ,follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)
            

    def add_user_miss_fullname(self):
        with app.app_context():
            data = dict(
                        full_name ="demo",
                        email = "test@123.com",
                        
                        password ="demo" ,
                        address = "test",
                        gender = "male",
                        dob ="2022-07-14 17:13:45.138" 
                                    )
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='admin', password='admin')
                                , follow_redirects=True)
            response = tester.post('/auth/add_user',
                                    data=data, follow_redirects=True)
            self.assertIn(b"Username is required",response.data)
            self.assertEqual(response.status_code, 200)

    # def add_user_miss_email(self):
    #     with app.app_context():
    #         data = dict(
    #                     full_name ="demo",
                        
    #                     username = "tse54t@123200",
    #                     password ="demo" ,
    #                     address = "test",
    #                     gender = "male",
    #                     dob ="2022-07-14 17:13:45.138" 
    #                                 )
    #         tester = app.test_client(self)
    #         response = tester.post('/auth/login',
    #                             data=dict(username='admin', password='admin')
    #                             , follow_redirects=True)
    #         response = tester.post('/auth/add_user',
    #                                 data=data, follow_redirects=True)
    #         self.assertIn(b"full name is required",response.data)
    #         self.assertEqual(response.status_code, 200)

    # def add_user_miss_fullname(self):
    #     with app.app_context():
    #         data = dict(
    #                     full_name ="demo",
    #                     email = "test@123.com",
    #                     username = "tse54t@123200",
    #                     password ="demo" ,
    #                     address = "test",
    #                     gender = "male",
    #                     dob ="2022-07-14 17:13:45.138" 
    #                                 )
    #         tester = app.test_client(self)
    #         response = tester.post('/auth/login',
    #                             data=dict(username='admin', password='admin')
    #                             , follow_redirects=True)
    #         response = tester.post('/auth/add_user',
    #                                 data=data, follow_redirects=True)
    #         self.assertIn(b"full name is required",response.data)
    #         self.assertEqual(response.status_code, 200)
    def test_shop_approval_list_page(self):
        '''to test approved shop list page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/shop_approval_list', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_product_list_page(self):
        '''to test product list page'''

        tester = app.test_client(self)
        response = tester.get('/auth/product_list', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_product_list_search(self):
        '''to test product list page'''

        tester = app.test_client(self)
        response = tester.get('/auth/product_list?search=""', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = tester.get('/auth/product_list?sort=price', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = tester.get('/auth/product_list?sort=price&price=high', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_product_list_price_filter(self):
        '''to test product price list filter'''
        tester = app.test_client(self)
        response = tester.post('/auth/product_list',
                               data=dict(price='0-250'),
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_wishlist_page(self):
        '''to test wishlist page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.get('/auth/wishlist', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_wishlist_page_no_wishlist(self):
        '''to test wishlist page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='sample user', password='demo'), follow_redirects=True)
        response = tester.get('/auth/wishlist', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_place_order_page(self):
        '''to test placed order page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.get('/auth/place_order', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_place_order_page_post(self):
        '''to test placed order page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.post('/auth/place_order', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_order_detail_page(self):
        '''to test  order detail page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.get('/auth/order_detail/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_cancel_order_page(self):
        '''to test cancel order page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.get('/auth/cancel_order/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_order_page(self):
        '''to test  order page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/orders', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_wishlist_page(self):
        '''to test add wishlist page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.get('/auth/add_wishlist/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_wishlist_page(self):
        '''to test delete wishlist page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.get('/auth/delete_wishlist/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # def test_cart_page(self):
    #     '''to test  cart page'''

    #     tester = app.test_client(self)
    #     response = tester.post('/auth/login',
    #                            data=dict(username='user', password='demo'), follow_redirects=True)
    #     response = tester.get('/auth/cart', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    def test_add_cart_page(self):
        '''to test add cart page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.get('/auth/add_cart/1/index', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_cart_page(self):
        '''to test delete cart page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.get('/auth/delete_cart/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_approval_shop_page(self):
        '''to test approval shop page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/approval_shop/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_reject_shop_page(self):
        '''to test reject shop page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/reject_shop/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_reject_shop(self):
        '''to test reject shop endpoint'''
        with app.app_context():
            tester = app.test_client(self)
            resp = tester.post('/auth/login',
            data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.post('/auth/reject_shop/2',data=dict(message='admin not permitted')
            , follow_redirects=True)
            self.assertEqual(response.status_code,200)

class ShopTest(unittest.TestCase):
    """to test shop specific test case"""

    def login(self, username='admin', password='admin'):
        """to test login """
        return app.test_client(self).post('/auth/login',data=dict(username=
            username, password=password), follow_redirects=True)

    # def logout(self):
    #     return self.app.get('/logout', follow_redirects=True)

    def test_list_shop_page_admin_get(self):
        '''to test listing shop page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).get('/shop/list_shop', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_list_shop_page_shop_get(self):
        '''to test listing shop page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'shopuser', password='demo'), follow_redirects=True)
            self.assertTrue(g.user.is_shopuser == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).get('/shop/list_shop', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_list_shop_page_user_get(self):
        '''to test listing shop page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'user', password='demo'), follow_redirects=True)
            self.assertTrue(g.user.is_customer == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).get('/shop/list_shop', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_list_shop_page_admin_post(self):
        '''to test listing shop page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).post('/shop/list_shop', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_list_shop_page_shop_post(self):
        '''to test listing shop page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'shopuser', password='demo'), follow_redirects=True)
            self.assertTrue(g.user.is_shopuser == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).post('/shop/list_shop', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_list_shop_page_user_post(self):
        '''to test listing shop page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'user', password='demo'), follow_redirects=True)
            self.assertTrue(g.user.is_customer == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).post('/shop/list_shop', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_list_shop_customer(self):
        '''to test listing shop page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'user', password='demo'), follow_redirects=True)
            self.assertEqual(response.status_code,200)
            self.assertTrue(g.user.is_customer == True)
            if g.user.is_customer == True:
                response = app.test_client(self).get('/shop/list_shop', follow_redirects=True)
                # self.assertEqual(response.status_code, 403)
                self.assertEqual(response.status_code, 200)

    def test_create_shop_page(self):
        '''to test shop creation page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).get('/shop/create_shop', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    # def test_create_shop_page_shop(self):
    #     '''to test shop creation page'''
    #     with app.app_context():
    #         response = app.test_client(self).post('/auth/login',data=dict(username=
    #         'shopuser', password='demo'), follow_redirects=True)
    #         self.assertTrue(g.user.is_shopuser == True)
    #         self.assertEqual(response.status_code,200)
    #         response = app.test_client(self).get('/shop/create_shop', follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)

    # def test_create_shop_page_user(self):
    #     '''to test shop creation page'''
    #     with app.app_context():
    #         response = app.test_client(self).post('/auth/login',data=dict(username=
    #         'user', password='demo'), follow_redirects=True)
    #         self.assertTrue(g.user.is_customer == True)
    #         self.assertEqual(response.status_code,200)
    #         response = app.test_client(self).get('/shop/create_shop', follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)


    def test_create_shop_post(self):
        """Post reqest to create shop by admin"""
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).post('/shop/create_shop', 
            data=dict(full_name ="demo",
                        email = "test@123.com",
                        username = "1@12e1",
                        password ="test@123" ,
                        conpassword ="test@123", 
                        address = "test",
                        gender = "male",
                        dob ="2022-07-14 17:13:45.138",
                        store_name = 'storess_name1156',
                        description = 'description'), follow_redirects=True)
            self.assertEqual(response.status_code,200)

    def test_create_shop_post_miss_fullname(self):
        """Post reqest to create shop by admin"""
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).post('/shop/create_shop', 
            data=dict(
                        email = "test@123.com",
                        username = "123456test@12e1",
                        password ="test@123" ,
                        conpassword ="test@123", 
                        address = "test",
                        gender = "male",
                        dob ="2022-07-14 17:13:45.138",
                        store_name = 'store_name1156',
                        description = 'description'), follow_redirects=True)
            self.assertEqual(response.status_code,200)
            self.assertIn(b'required',response.data)

    def test_create_shop_post_miss_email(self):
        """Post reqest to create shop by admin"""
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).post('/shop/create_shop', 
            data=dict(full_name ="demo",
                        
                        username = "123456test@12e1",
                        password ="test@123" ,
                        conpassword ="test@123", 
                        address = "test",
                        gender = "male",
                        dob ="2022-07-14 17:13:45.138",
                        store_name = 'store_name1156',
                        description = 'description'), follow_redirects=True)
            self.assertEqual(response.status_code,200)
            self.assertIn(b'required',response.data)
    
    def test_create_shop_post_miss_fullname(self):
        """Post reqest to create shop by admin"""
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).post('/shop/create_shop', 
            data=dict(
                        email = "test@123.com",
                        username = "123456test@12e1",
                        password ="test@123" ,
                        conpassword ="test@123", 
                        address = "test",
                        gender = "male",
                        dob ="2022-07-14 17:13:45.138",
                        store_name = 'store_name1156',
                        description = 'description'), follow_redirects=True)
            self.assertEqual(response.status_code,200)
            self.assertIn(b'required',response.data)

    def test_create_shop_post_by_user(self):
        """Post reqest to create shop by user"""
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'user', password='demo'), follow_redirects=True)
            self.assertTrue(g.user.is_customer == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).post('/shop/create_shop', 
            data=dict(full_name ="demo",
                        email = "test@123.com",
                        
                        password ="test@123" ,
                        conpassword ="test@123", 
                        address = "test",
                        gender = "male",
                        dob ="2022-07-14 17:13:45.138",
                        store_name = 'store_name1156',
                        description = 'description'), follow_redirects=True)
            # self.assertEqual(response.status_code,403)
            self.assertIn(b'required',response.data)
            self.assertEqual(response.status_code,200)

    def test_delete_shop_page_admin(self):
        '''to test shop deletion page'''
        with app.app_context():
            response = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).get('/shop/delete_shop/3', follow_redirects=True)
            print(response.data)
            self.assertEqual(response.status_code, 200)

    def test_delete_shop_page_user(self):
        '''to test shop deletion page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'user', password='demo'), follow_redirects=True)
            self.assertTrue(g.user.is_customer == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).get('/shop/delete_shop/3', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_delete_shop_page_shopuser(self):
        '''to test shop deletion page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'shopuser', password='demo'), follow_redirects=True)
            self.assertTrue(g.user.is_shopuser == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).get('/shop/delete_shop/3', follow_redirects=True)
            self.assertEqual(response.status_code, 200)


    def test_delete_shop_page_admin_post(self):
        '''to test shop deletion page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).post('/shop/delete_shop/3', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_delete_shop_page_user_post(self):
        '''to test shop deletion page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'user', password='demo'), follow_redirects=True)
            self.assertTrue(g.user.is_customer == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).post('/shop/delete_shop/3', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_delete_shop_page_shopuser_post(self):
        '''to test shop deletion page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'shopuser', password='demo'), follow_redirects=True)
            self.assertTrue(g.user.is_shopuser == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).post('/shop/delete_shop/3', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_delete_shop_by_customer(self):
        '''to test shop deletion by customer page'''
        with app.app_context():
            app.test_client(self).post('/auth/login',data=dict(username=
            'user', password='demo'), follow_redirects=True)
            self.assertTrue(g.user.is_admin == False)
            # self.assertEqual(response.status_code,200)
            response = app.test_client(self).get('/shop/delete_shop/101', follow_redirects=True)
            # self.assertEqual(response.status_code, 401)
            self.assertEqual(response.status_code, 200)


    def test_update_shop(self):
        '''to test shop update by admin'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(response.status_code,200)
            response = app.test_client(self).post('/shop/update_shop/1',
                                data=dict(
                                    store_name='store_name1111'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_update_shop_customer(self):
        '''to test shop update by user'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'user', password='demo'), follow_redirects=True)
            self.assertEqual(response.status_code,200)
            self.assertTrue(g.user.is_admin == False)
            if g.user.is_customer == False:
                response = app.test_client(self).post('/shop/update_shop/2',
                                    data=dict(
                                        store_name='store_name11Usser'), follow_redirects=True)
                self.assertEqual(response.status_code, 403)

    # def test_update_shop_page(self):
    #     '''to test shop updation page'''
    #     with app.app_context():
    #         rs = self.login(username='admin',password='admin')
    #         self.assertTrue(g.user.is_admin == True)
    #         self.assertEqual(rs.status_code,200)
    #         response = app.test_client(self).get('/shop/update_shop/30', follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)


class ProductTest(BaseTestCase):
    """class to test product specific test"""

    def login(self, username='admin', password='admin'):
        """to test login """
        return app.test_client(self).post('/auth/login',data=dict(username=
            username, password=password), follow_redirects=True)

    def test_all_product_get(self):
        '''to test all product listing page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            response = app.test_client(self).get('/auth/all_product', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_all_product_post(self):
        '''to test all product listing page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            response = app.test_client(self).post('/auth/all_product', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_all_category(self):
        '''to test all category listing page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            response = app.test_client(self).get('/auth/all_category', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_all_category_post(self):
        '''to test all category listing page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            response = app.test_client(self).post('/auth/all_category', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_all_orders(self):
        '''to test all order listing page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            response = app.test_client(self).get('/auth/all_orders', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_all_orders_post(self):
        '''to test all order listing page'''
        with app.app_context():
            response = app.test_client(self).post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            response = app.test_client(self).post('/auth/all_orders', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_shop_dashboard_page_post(self):
        '''to test shop dashboard page'''
        with app.app_context():
            rs = self.login(username='admin',password='admin')
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(rs.status_code,200)
            response = app.test_client(self).post('/product', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_shop_dashboard_page_shop_post(self):
        '''to test shop dashboard page'''
        with app.app_context():
            rs = self.login(username='shopuser',password='demo')
            self.assertTrue(g.user.is_admin == False)
            self.assertEqual(rs.status_code,200)
            response = app.test_client(self).post('/product', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_shop_dashboard_page_post(self):
        '''to test shop dashboard page'''
        with app.app_context():
            rs = self.login(username='user',password='demo')
            self.assertTrue(g.user.is_admin == False)
            self.assertEqual(rs.status_code,200)
            response = app.test_client(self).post('/product', follow_redirects=True)
            # self.assertEqual(response.status_code, 403)
            self.assertEqual(response.status_code, 200)

    def test_shop_dashboard_page_admin(self):
        '''to test shop dashboard page'''
        with app.app_context():
            rs = self.login(username='admin',password='admin')
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(rs.status_code,200)
            response = app.test_client(self).get('/product', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_shop_dashboard_page_user(self):
        '''to test shop dashboard page'''
        with app.app_context():
            rs = self.login(username='user',password='demo')
            self.assertTrue(g.user.is_customer == True)
            self.assertEqual(rs.status_code,200)
            response = app.test_client(self).get('/product', follow_redirects=True)
            # self.assertEqual(response.status_code, 401)
            self.assertEqual(response.status_code, 200)

    def test_shop_dashboard_page_shopuser(self):
        '''to test shop dashboard page'''
        with app.app_context():
            rs = self.login(username='shopuser',password='demo')
            self.assertTrue(g.user.is_admin == False)
            self.assertEqual(rs.status_code,200)
            response = app.test_client(self).get('/product', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_add_category_page(self):
        '''to test add category page'''
        with app.app_context():
            rs = self.login(username='admin',password='admin')
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(rs.status_code,200)
            response = app.test_client(self).get('/product/add_category', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_add_category_post(self):
        '''to test add category page'''
        with app.app_context():
            rs = self.login(username='admin',password='admin')
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(rs.status_code,200)
            response = app.test_client(self).post('/product/add_category',
                        data=dict( category="test1"),
                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_add_category_customer_post(self):
        '''to test add category page'''
        with app.app_context():
            rs = self.login(username='user',password='demo')
            self.assertTrue(g.user.is_admin == False)
            self.assertEqual(rs.status_code,200)
            response = app.test_client(self).post('/product/add_category',
                        data=dict( category="test1"),
                        follow_redirects=True)
            # self.assertEqual(response.status_code, 401)
            self.assertEqual(response.status_code, 200)
    
    def test_add_category_shopuser_post(self):
        '''to test add category page'''
        with app.app_context():
            rs = self.login(username='shopuser',password='demo')
            self.assertTrue(g.user.is_admin == False)
            self.assertEqual(rs.status_code,200)
            response = app.test_client(self).post('/product/add_category',
                        data=dict( category="test1"),
                        follow_redirects=True)
            # self.assertEqual(response.status_code, 401)
            self.assertEqual(response.status_code, 200)


    def test_update_category_page(self):
        '''to test  update category page'''
        with app.app_context():
            rs = self.login(username='admin',password='admin')
            self.assertTrue(g.user.is_admin == True)
            self.assertEqual(rs.status_code,200)
            response = app.test_client(self).get('/product/update_category/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_update_category_post_error(self):
        '''to test  update category page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/product/update_category/1', 
                                data=dict( ),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'category is required',response.data)

    def test_update_category_post(self):
        '''to test  update category page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/product/update_category/1', 
                                data=dict( category="cloths"),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_update_category_user_post(self):
        '''to test  update category page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.post('/product/update_category/1', 
                                data=dict( category="cloths"),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 403)
    
    def test_update_category_shopuser_post(self):
        '''to test  update category page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='shopuser', password='demo'), follow_redirects=True)
        response = tester.post('/product/update_category/1', 
                                data=dict( category="cloths"),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 403)

    def test_create_product(self):
        '''to test product update'''
        with app.app_context():
            rs = self.login(username='shopuser',password='demo')
            self.assertTrue(g.user.is_admin == False)
            self.assertEqual(rs.status_code,200)
            response = app.test_client(self).get('/product/create_product', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_create_product_shop_post(self):
        '''to test product update'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='shopuser', password='demo'), follow_redirects=True)
        response = tester.post('/product/create_product',
                                data=dict(category_id=2,
                                    product_name="product_name",
                                    stock_quantity=50,
                                    sold_quantity=0, brand="brand", price=500,
                                    ),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_create_product_user_post(self):
        '''to test product update'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.post('/product/create_product',
                                data=dict(category_id=2,
                                    product_name="product_name",
                                    stock_quantity=50,
                                    sold_quantity=0, brand="brand", price=500,
                                    ),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 403)
    
    def test_create_product_admin_post(self):
        '''to test product update'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/product/create_product',
                                data=dict(category_id=2,
                                    product_name="product_name",
                                    stock_quantity=50,
                                    sold_quantity=0, brand="brand", price=500,
                                    ),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_product_exception(self):
        '''to test product exception'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/product/create_product',
                                data=dict(category_id=-1,
                                    product_name="product_name",
                                    stock_quantity=50,
                                    sold_quantity=0, brand="brand", price=500,
                                    ),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_product_category_error(self):
        '''to test product update'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/product/create_product',
                                data=dict(
                                    product_name="product_name",
                                    stock_quantity=50,
                                    sold_quantity=0, brand="brand", price=500,
                                    ),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'category is required',response.data)
    
    def test_create_product_product_error(self):
        '''to test product update'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/product/create_product',
                                data=dict(category_id=2,
                                   
                                    stock_quantity=50,
                                    sold_quantity=0, brand="brand", price=500,
                                    ),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'product name is required',response.data)

    def test_create_product_stock_error(self):
        '''to test product update'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/product/create_product',
                                data=dict(category_id=2,
                                    product_name="product_name",
                                    
                                    sold_quantity=0, brand="brand", price=500,
                                    ),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'stock is required',response.data)

    def test_create_product_brand_error(self):
        '''to test product update'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/product/create_product',
                                data=dict(category_id=2,
                                    product_name="product_name",
                                    stock_quantity=50,
                                    sold_quantity=0, price=500,
                                    ),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'brand is required',response.data)


    def test_create_product_price_error(self):
        '''to test product update'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/product/create_product',
                                data=dict(category_id=2,
                                    product_name="product_name",
                                    stock_quantity=50,
                                    sold_quantity=0, brand="brand"
                                    ),
                                follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'price is required',response.data)


    def test_delete_product_shop_get(self):
        '''to test product delete'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='shopuser', password='demo'), follow_redirects=True)
        response = tester.get('/product/delete/45', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_product_shop_post(self):
        '''to test product delete'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='shopuser', password='demo'), follow_redirects=True)
        response = tester.post('/product/delete/44', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_product_admin_get(self):
        '''to test product delete'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/product/delete/43', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_product_admin_post(self):
        '''to test product delete'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/product/delete/42', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_product_user_get(self):
        '''to test product delete'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.get('/product/delete/41', follow_redirects=True)
        self.assertEqual(response.status_code, 403)

    def test_delete_product_user_post(self):
        '''to test product delete'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        response = tester.post('/product/delete/40', follow_redirects=True)
        self.assertEqual(response.status_code, 403)

    def test_update_product_get_user(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='user', password='demo'), follow_redirects=True)
            response = tester.get('/product/update_product/32', follow_redirects=True)
            self.assertEqual(response.status_code, 403)

    def test_update_product_get_shopuser(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='shopuser', password='demo'), follow_redirects=True)
            response = tester.get('/product/update_product/32', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            # self.assertEqual(response.status_code, 401)

    def test_update_product_get_admin(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.get('/product/update_product/32', follow_redirects=True)
            # self.assertEqual(response.status_code, 401)
            self.assertEqual(response.status_code, 200)

    def test_update_product_post_shop(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='shopuser', password='demo'), follow_redirects=True)
            response = tester.post('/product/update_product/32',
                                    data=dict(category_id=2,
                                        product_name="Chcho",
                                        stock_quantity=50,
                                        sold_quantity=0, brand="brand", price=500,
                                        ),follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_update_product_post_admin(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.post('/product/update_product/32',
                                    data=dict(category_id=2,
                                        product_name="Chcho",
                                        stock_quantity=50,
                                        sold_quantity=0, brand="brand", price=500,
                                        ),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_update_product_post_user(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='user', password='demo'), follow_redirects=True)
            response = tester.post('/product/update_product/32',
                                    data=dict(category_id=2,
                                        product_name="Chcho",
                                        stock_quantity=50,
                                        sold_quantity=0, brand="brand", price=500,
                                        ),follow_redirects=True)
            self.assertEqual(response.status_code, 403)

    def test_update_product_condition1(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.post('/product/update_product/32',
                                    data=dict(category_id=2,
                                        product_name="Chcho44",
                                        stock_quantity=50,
                                        sold_quantity=0, brand="brand", price=500,
                                        ),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_update_product_condition2(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            response = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.post('/product/update_product/32',
                                    data=dict(category_id=2,
                                        product_name="Chcho44",
                                        stock_quantity=50,
                                        sold_quantity=0, brand="brand33", price=500,
                                        ),follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_create_product_miss_cateory(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            res = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.get('/product/create_product',
                                    data=dict(
                                        product_name="Chcho",
                                        stock_quantity=50,
                                        sold_quantity=0, brand="brand", price=500,
                                        ),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'category',response.data)
    
    def test_create_product_miss_product(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            res = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.get('/product/create_product',
                                    data=dict(
                                        category_id=2,
                                        stock_quantity=50,
                                        sold_quantity=0, brand="brand", price=500,
                                        ),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'product',response.data)


    def test_create_product_miss_stock_quantity(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            res = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.get('/product/create_product',
                                    data=dict(
                                        category_id=2,
                                        product_name="Chcho",
                                        
                                        sold_quantity=0, brand="brand", price=500,
                                        ),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'stock',response.data)  

    def test_create_product_miss_sold(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            res = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.get('/product/create_product',
                                    data=dict(
                                        category_id=2,
                                        product_name="Chcho",
                                         stock_quantity=50,
                                         brand="brand", price=500,
                                        ),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'sold',response.data)       


    def test_create_product_miss_brand(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            res = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.get('/product/create_product',
                                    data=dict(
                                        category_id=2,
                                        product_name="Chcho",
                                         stock_quantity=50,
                                          sold_quantity=0
                                        , price=500,
                                        ),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'brand',response.data)  

    def test_create_product_miss_price(self):
        '''to test product update'''
        with app.app_context():
            tester = app.test_client(self)
            res = tester.post('/auth/login',
                                data=dict(username='admin', password='admin'), follow_redirects=True)
            response = tester.get('/product/create_product',
                                    data=dict(
                                        category_id=2,
                                        product_name="Chcho",
                                         stock_quantity=50,
                                          sold_quantity=0,
                                        brand="brand",
                                        ),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'price',response.data) 

if __name__ == '__main__':
    unittest.main()
