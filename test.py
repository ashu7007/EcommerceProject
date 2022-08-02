# import unittest
# from flask import g
# from werkzeug.security import check_password_hash, generate_password_hash
# import datetime
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# from apps import app
# from apps.users.models import Userdata

# date = datetime.datetime.now()



# # app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db= SQLAlchemy(app)

# class BaseTestCase(unittest.TestCase):
#     """A base test case."""

#     def create_app(self):
#         app.config.from_object('config.TestConfig')
#         return app

#     def setUp(self):
#         db.create_all()
#         admin = Userdata(full_name="full_name", email="email@123.com", 
#                             username="admin3", 
#                             password=generate_password_hash("admin"),
#                             address="address", gender="male", dob=date, 
#                             active=True, is_admin=True,
#                             is_customer=False,is_shopuser=False, 
#                             created_at=date,updated_at=date)

#         # user = Userdata(full_name="full_name", email="email@123.com", 
#         #                     username="user2", 
#         #                     password=generate_password_hash("demo"),
#         #                     address="address", gender="male", dob=date, 
#         #                     active=True, is_admin=False,
#         #                     is_customer=True,is_shopuser=False, 
#         #                     created_at=date,updated_at=date)

#         # shopuser = Userdata(full_name="full_name", email="email@123.com", 
#         #                     username="shop2", 
#         #                     password=generate_password_hash("demo"),
#         #                     address="address", gender="male", dob=date, 
#         #                     active=True, is_admin=False,
#         #                     is_customer=False,is_shopuser=True, 
#         #                     created_at=date,updated_at=date)
#         # db.session.add(admin)
#         # db.session.add(shopuser)
#         # db.session.add(user)
#         # db.session.commit()

#         # shop = Shop(user_id=shopuser.id, store_name="store_name", description="description", active=True,
#         #                            created_at=date, updated_at=date)
#         # db.session.commit()
#         # user = Userdata(full_name="full_name", email="email@123.com", 
#         #                     username="admin10", 
#         #                     password=generate_password_hash("admin"),
#         #                     address="address", gender="male", dob=date, 
#         #                     active=True, is_admin=True,
#         #                     is_customer=False,is_shopuser=False, 
#         #                     created_at=date,updated_at=date)
#         # db.session.add(user)
#         db.session.commit()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()



# class UserTest(BaseTestCase):
    
#     # def test_get_login_page(self):
#     #     tester = app.test_client(self)
#     #     response = tester.get('/auth/login',content_type='html/text')
#     #     self.assertEqual(response.status_code,200)

#     def test_login_user(self):
#         with app.app_context():
#             response = app.test_client(self).post('/auth/login',data=dict(username=
#             'admin10', password='admin1'), follow_redirects=True)
#             # self.assertIn(b'admin10', response.data)
            
#             self.assertTrue(g.user.is_admin == True)
#             self.assertEqual(response.status_code,200)
        

#     # def test_incorrect_login(self):
#     #     tester = app.test_client(self)
#     #     response = tester.post(
#     #         '/auth/login',
#     #         data=dict(username="wrong", password="wrong"),
#     #         follow_redirects=True
#     #     )
#     #     self.assertIn(b'Incorrect username.', response.data)

# if __name__ == '__main__':
#     unittest.main()