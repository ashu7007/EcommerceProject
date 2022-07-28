import unittest
from flask import g
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from apps import app, db_sql as db
from apps.users.models import Userdata

date = datetime.datetime.now()


class BaseTestCase(unittest.TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        user = Userdata(full_name="full_name", email="email@123.com", 
                            username="admin", 
                            password=generate_password_hash("admin"),
                            address="address", gender="male", dob="2022-07-14 17:13:45.138", 
                            active=True, is_admin=True,
                            is_customer=False,is_shopuser=False, 
                            created_at=date,updated_at=date)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()



class UserTest(BaseTestCase):
    
    def test_get_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/auth/login',content_type='html/text')
        self.assertEqual(response.status_code,200)

    def test_login_user(self):
        with self.client:
            response =  self.client.post('/auth/login',data=dict(username=
            'admin', password='admin'), follow_redirects=True)
            self.assertIn(b'admin', response.data)
            self.assertTrue(g.user.is_shopuser == True)
            self.assertEqual(response.status_code,200)
        

    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/auth/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Incorrect username.', response.data)

    def test_get_register_user_page(self):
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

    def test_get_shop_user_register_page(self):
        tester = app.test_client(self)
        response = tester.get('/auth/shop_user_register',content_type='html/text')
        self.assertEqual(response.status_code,200)

    # def test_register_user(self):
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

if __name__ == '__main__':
    unittest.main()