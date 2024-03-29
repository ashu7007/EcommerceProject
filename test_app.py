import os
import unittest

from apps import app, db_sql


class UserTest(unittest.TestCase):
    """to test functionality of user specific operation"""
    # def setUp(self):
    #     self.db_uri = 'sqlite:////tmp/test.db'
    #     app.config['TESTING'] = True
    #     app.config['WTF_CSRF_ENABLED'] = False
    #     app.config['SQL_ALCHEMY_DATABASE_URI'] = self.db_uri
    #     self.app = app.test_client()
    #     db_sql.create_all()

    # def tearDown(self):
    #     db_sql.session.remove()
    #     db_sql.drop_all()

    def test_get_login_page(self):
        """to test login page"""
        tester = app.test_client(self)
        response = tester.get('/auth/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_admin_user(self):
        """to test login func"""
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        self.assertIn(b'admin', response.data)
        # self.assertTrue(g.user.is_shopuser == True)
        self.assertEqual(response.status_code, 200)

    def test_login_customer_user(self):
        """to test login func"""
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='user', password='demo'), follow_redirects=True)
        self.assertIn(b'jay123', response.data)
        # self.assertTrue(g.user.is_shopuser == True)
        self.assertEqual(response.status_code, 200)

    def test_login_shop_user(self):
        """to test login func"""
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='shopuser', password='demo'), follow_redirects=True)
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
        username = "test@123",
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
        self.assertEqual(response.status_code,400)

    def test_verify_otp(self):
        """to test verify otp functionality"""

        tester = app.test_client(self)
        response = tester.post('/auth/verify',
         data=dict(otp ="4512"), follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_logout(self):
        """to test logout functionality"""

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

    def test_reset_token_page(self):
        """to test token reset"""

        tester = app.test_client(self)
        response = tester.get('/auth/reset_token/54754754475', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_update_profile_page(self):
        """to test update profile page"""
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='jay123', password='demo'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = tester.get('/auth/update_profile', follow_redirects=True)
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

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='shop6', password='demo'), follow_redirects=True)
        response = tester.get('/auth/order_for_shopuser', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_page(self):
        '''to test admin dashboard page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/admin_dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_admin_sale_page(self):
        '''to test admin sale page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/admin_sale', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_shop_sale_page(self):
        '''to test shop sale page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='shop6', password='demo'), follow_redirects=True)
        response = tester.get('/auth/shop_sale', follow_redirects=True)
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
                               data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/wishlist', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_place_order_page(self):
        '''to test placed order page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/place_order', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_order_detail_page(self):
        '''to test  order detail page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/order_detail/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_cancel_order_page(self):
        '''to test cancel order page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/cancel_order/0', follow_redirects=True)
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
                               data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/add_wishlist/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_wishlist_page(self):
        '''to test delete wishlist page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/delete_wishlist/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_cart_page(self):
        '''to test  cart page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/cart', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_cart_page(self):
        '''to test add cart page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='jay123', password='demo'), follow_redirects=True)
        response = tester.get('/auth/add_cart/1/index', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_cart_page(self):
        '''to test delete cart page'''

        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='jay123', password='demo'), follow_redirects=True)
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

    # def test_reject_shop(self):
    #'''to test reject shop endpoint'''
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/login',
    #      data=dict(username='admin', password='admin'), follow_redirects=True)
    #     response = tester.post('/auth/reject_shop/3',data=dict(message='admin not permitted')
    #     , follow_redirects=True)
    #     self.assertEqual(response.status_code,200)


class ProductTest(unittest.TestCase):
    """class to test product specific test"""

    def test_all_product(self):
        '''to test all product listing page'''
        tester = app.test_client(self)
        # response = tester.post('/auth/login',
        #  data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/all_product', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_all_category(self):
        '''to test all category listing page'''
        tester = app.test_client(self)
        # response = tester.post('/auth/login',
        #  data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/all_category', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_all_orders(self):
        '''to test all order listing page'''
        tester = app.test_client(self)
        # response = tester.post('/auth/login',
        #  data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/all_orders', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_shop_dashboard_page(self):
        '''to test shop dashboard page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/product', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_category_page(self):
        '''to test add category page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/product/add_category', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_add_category_post(self):
        '''to test add category page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/product/add_category',
                    data=dict( category_name="test1"),
                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    # def test_add_category_customer_post(self):
    #     '''to test add category page'''
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/login',
    #                            data=dict(username='jay@123', password='demo'), follow_redirects=True)
    #     response = tester.post('/product/add_category',
    #                 data=dict( category_name="test1"),
    #                 follow_redirects=True)
    #     self.assertEqual(response.status_code, 401)
    
    # def test_add_category_shopuser_post(self):
    #     '''to test add category page'''
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/login',
    #                            data=dict(username='shop6', password='demo'), follow_redirects=True)
    #     response = tester.post('/product/add_category',
    #                 data=dict( category_name="test1"),
    #                 follow_redirects=True)
    #     self.assertEqual(response.status_code, 401)


    def test_update_category_page(self):
        '''to test  update category page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/product/update_category/1', follow_redirects=True)
        self.assertEqual(response.status_code, 401)


    # def test_update_category_post(self):
    #     '''to test  update category page'''
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/login',
    #                            data=dict(username='admin', password='admin'), follow_redirects=True)
    #     response = tester.post('/product/update_category/5', 
    #                             data=dict( category_name="cloths"),
    #                             follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)


    def test_create_product(self):
        '''to test product update'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='shop4', password='demo'), follow_redirects=True)
        response = tester.get('/product/create_product', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # def test_create_product_post(self):
    #     '''to test product update'''
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/login',
    #                            data=dict(username='shop4', password='demo'), follow_redirects=True)
    #     response = tester.post('/product/create_product',
    #                             data=dict(category_id=4,
    #                                 product_name="product_name",
    #                                 stock_quantity=50,
    #                                 sold_quantity=0, brand="brand", price=500,
    #                                 ),
    #                             follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        '''to test product delete'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='shop4', password='demo'), follow_redirects=True)
        response = tester.get('/product/delete/15', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        '''to test product update'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='shop4', password='demo'), follow_redirects=True)
        response = tester.get('/product/update_product/16', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_update_product_post(self):
        '''to test product update'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='shop4', password='demo'), follow_redirects=True)
        response = tester.post('/product/update_product/16',
                                data=dict(category_id=4,
                                    product_name="Chcho",
                                    stock_quantity=50,
                                    sold_quantity=0, brand="brand", price=500,
                                    ),follow_redirects=True)
        self.assertEqual(response.status_code, 200)


class ShopTest(unittest.TestCase):
    """to test shop specific test case"""

    def test_list_shop_page(self):
        '''to test listing shop page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/shop/list_shop', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_list_shop_customer(self):
        '''to test listing shop page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='jay123', password='demo'), follow_redirects=True)
        response = tester.get('/shop/list_shop', follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_create_shop_page(self):
        '''to test shop creation page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/shop/create_shop', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_shop_post(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/shop/create_shop', 
         data=dict(full_name ="demo",
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

    def test_delete_shop_page(self):
        '''to test shop deletion page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/shop/delete_shop/13', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_delete_shop_by_customer(self):
        '''to test shop deletion by customer page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='jay123', password='demo'), follow_redirects=True)
        response = tester.get('/shop/delete_shop/101', follow_redirects=True)
        self.assertEqual(response.status_code, 401)


    def test_update_shop(self):
        '''to test shop update by admin'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/shop/update_shop/30',
                               data=dict(
                                   store_name='store_name1111'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_update_shop_customer(self):
        '''to test shop update by admin'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='jay123', password='demo'), follow_redirects=True)
        response = tester.post('/shop/update_shop/30',
                               data=dict(
                                   store_name='store_name1111'), follow_redirects=True)
        self.assertEqual(response.status_code, 401)

    def test_update_shop_page(self):
        '''to test shop updation page'''
        tester = app.test_client(self)
        response = tester.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/shop/update_shop/30', follow_redirects=True)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
