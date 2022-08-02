import unittest
from flask import g

from apps import app




class UserTest(unittest.TestCase):
    
    def test_get_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/auth/login',content_type='html/text')
        self.assertEqual(response.status_code,200)

    def test_login_user(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        self.assertIn(b'admin', response.data)
        # self.assertTrue(g.user.is_shopuser == True)
        self.assertEqual(response.status_code,200)
        

    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/auth/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Incorrect username.', response.data)

    def test_get_register_page(self):
        tester = app.test_client(self)
        response = tester.get('/auth/register',content_type='html/text')
        self.assertEqual(response.status_code,200)

    # def test_register_user(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/register',
    #      data=dict(full_name ="demo",
    #     email = "test@123.com",
    #     username = "test@123",
    #     password ="test@123" ,
    #     conPassword ="test@123", 
    #     address = "test",
    #     gender = "male",
    #     dob ="2022-07-14 17:13:45.138" ), follow_redirects=True)
    #     self.assertEqual(response.status_code,200)

    # def test_register_user_failure(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/register',
    #      data=dict(full_name ="demo",
    #     email = "test@123.com",
    #     username = "test@123",
    #     password ="test@123" ,
    #     conPassword ="test@123", 
    #     address = "test",
    #     gender = "male",
    #     dob ="2022-07-14 17:13:45.138" ), follow_redirects=True)
    #     self.assertEqual(response.status_code,200)

    def test_get_shop_user_register_page(self):
        tester = app.test_client(self)
        response = tester.get('/auth/shop_user_register',content_type='html/text')
        self.assertEqual(response.status_code,200)

    # def test_shop_user_register(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/shop_user_register',
    #      data=dict(full_name ="demo",
    #                 email = "test@123.com",
    #                 username = "test@123",
    #                 password ="test@123" ,
    #                 conpassword ="test@123", 
    #                 address = "test",
    #                 gender = "male",
    #                 dob ="2022-07-14 17:13:45.138",
    #                 store_name = 'store_name',
    #                 description = 'description'), follow_redirects=True)
    #     self.assertEqual(response.status_code,200)


    # def test_shop_user_register_failure(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/shop_user_register',
    #      data=dict(full_name ="demo",
    #                 email = "test@123.com",
    #                 username = "test@123",
    #                 password ="test@123" ,
    #                 conpassword ="test@123", 
    #                 address = "test",
    #                 gender = "male",
    #                 dob ="2022-07-14 17:13:45.138",
    #                 store_name = 'store_name',
    #                 description = 'description'), follow_redirects=True)
    #     self.assertEqual(response.status_code,200)


    #  def test_verify_otp(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/verify',
    #      data=dict(otp ="4512"), follow_redirects=True)
    #     self.assertEqual(response.status_code,200)
    

    
    def test_logout(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    
    # def test_all_product(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/login',
    #      data=dict(username='admin', password='admin'), follow_redirects=True)
    #     response = tester.get('/auth/all_product', follow_redirects=True)
    #     self.assertEqual(response.status_code,200)


    def test_all_category(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/all_category', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_forgot_password_page(self):
        tester = app.test_client(self)
        response = tester.get('/auth/forgot_password', follow_redirects=True)
        self.assertEqual(response.status_code,200)


    def test_reset_token_page(self):
        tester = app.test_client(self)
        response = tester.get('/auth/reset_token/54754754475', follow_redirects=True)
        self.assertEqual(response.status_code,404)

    
    def test_update_profile_page(self):
        tester = app.test_client(self)
        response = tester.get('/auth/update_profile', follow_redirects=True)
        self.assertEqual(response.status_code,200)


    def test_order_for_shopuser_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='shop4', password='demo'), follow_redirects=True)
        response = tester.get('/auth/shop_orders', follow_redirects=True)
        self.assertEqual(response.status_code,200)
    
    def test_order_for_shopuser_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='shop4', password='demo'), follow_redirects=True)
        response = tester.get('/auth/shop_orders', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    
    def test_admin_dashboard_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/admin_dashboard', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_admin_sale_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/admin_sale', follow_redirects=True)
        self.assertEqual(response.status_code,200)
    
    def test_shop_sale_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='shop4', password='demo'), follow_redirects=True)
        response = tester.get('/auth/shop_sale', follow_redirects=True)
        self.assertEqual(response.status_code,200)
    
    def test_user_list_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/user_list', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_add_user_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/add_user', follow_redirects=True)
        self.assertEqual(response.status_code,200)
        
    def test_shop_approval_list_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/shop_approval_list', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_product_list_page(self):
        tester = app.test_client(self)
        response = tester.get('/auth/product_list', follow_redirects=True)
        self.assertEqual(response.status_code,200)
    
    def test_product_list_price_filter(self):
        tester = app.test_client(self)
        response = tester.post('/auth/product_list', 
        data=dict(price='0-250'),
        follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_wishlist_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/wishlist', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_place_order_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/place_order', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    
    def test_order_detail_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/order_detail/2', follow_redirects=True)
        self.assertEqual(response.status_code,200)


    def test_cancel_order_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/cancel_order/0', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_order_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/orders', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_add_wishlist_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/add_wishlist/1', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_delete_wishlist_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/delete_wishlist/1', follow_redirects=True)
        self.assertEqual(response.status_code,200)
    
    def test_cart_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/cart', follow_redirects=True)
        self.assertEqual(response.status_code,200)


    def test_add_cart_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/add_cart/1/index', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_delete_cart_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='Ashutosh', password='demo'), follow_redirects=True)
        response = tester.get('/auth/delete_cart/1', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_approval_shop_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/approval_shop/1', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_reject_shop_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/reject_shop/1', follow_redirects=True)
        self.assertEqual(response.status_code,200)
    
    # def test_reject_shop(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/login',
    #      data=dict(username='admin', password='admin'), follow_redirects=True)
    #     response = tester.post('/auth/reject_shop/3',data=dict(message='admin not permitted')
    #     , follow_redirects=True)
    #     self.assertEqual(response.status_code,200)

class ProductTest(unittest.TestCase):
    
    def test_all_product(self):
        tester = app.test_client(self)
        # response = tester.post('/auth/login',
        #  data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/all_product', follow_redirects=True)
        self.assertEqual(response.status_code,200)
    

    def test_all_category(self):
        tester = app.test_client(self)
        # response = tester.post('/auth/login',
        #  data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/all_category', follow_redirects=True)
        self.assertEqual(response.status_code,200)


    def test_all_orders(self):
        tester = app.test_client(self)
        # response = tester.post('/auth/login',
        #  data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/auth/all_orders', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_shop_dashboard_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/product', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_add_category_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/product/add_category', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_update_category_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/product/update_category/1', follow_redirects=True)
        self.assertEqual(response.status_code,401)
    
    def test_create_product(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='shop4', password='demo'), follow_redirects=True)
        response = tester.get('/product/create_product', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_delete_product(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='shop4', password='demo'), follow_redirects=True)
        response = tester.get('/product/delete/0', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_update_product(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='shop4', password='demo'), follow_redirects=True)
        response = tester.get('/product/update_product/0', follow_redirects=True)
        self.assertEqual(response.status_code,401)


class ShopTest(unittest.TestCase):
    
    def test_list_shop_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/shop/list_shop', follow_redirects=True)
        self.assertEqual(response.status_code,200)
    
    def test_create_shop_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/shop/create_shop', follow_redirects=True)
        self.assertEqual(response.status_code,200)

    # def test_create_shop_post(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/auth/login',
    #      data=dict(username='admin', password='admin'), follow_redirects=True)
    #     response = tester.post('/shop/create_shop', 
    #      data=dict(full_name ="demo",
    #                 email = "test@123.com",
    #                 username = "test@123456",
    #                 password ="test@123" ,
    #                 conpassword ="test@123", 
    #                 address = "test",
    #                 gender = "male",
    #                 dob ="2022-07-14 17:13:45.138",
    #                 store_name = 'store_name1156',
    #                 description = 'description'), follow_redirects=True)
    #     self.assertEqual(response.status_code,200)

    def test_delete_shop_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        esponse = tester.get('/shop/delete_shop/36', follow_redirects=True)
        self.assertEqual(response.status_code,200)


    def test_update_shop(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.post('/shop/update_shop/30', 
         data=dict(
                    store_name = 'store_name1111' ), follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def test_update_shop_page(self):
        tester = app.test_client(self)
        response = tester.post('/auth/login',
         data=dict(username='admin', password='admin'), follow_redirects=True)
        response = tester.get('/shop/update_shop/30', follow_redirects=True)
        self.assertEqual(response.status_code,401)

if __name__ == '__main__':
    unittest.main()