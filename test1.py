# import pytest

# from apps import app


# @pytest.fixture
# def client():
#     app.config["TESTING"] = True
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.testing = True
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

#     client = app.test_client()
#     with app.app_context():
#         db.create_all()
#         admin = Userdata(full_name="full_name", email="email@123.com", 
#                             username="admin3", 
#                             password=generate_password_hash("admin"),
#                             address="address", gender="male", dob=date, 
#                             active=True, is_admin=True,
#                             is_customer=False,is_shopuser=False, 
#                             created_at=date,updated_at=date)
#         db.session.add(admin)
#         db.session.commit()
#     yield client

# def test_get_login_page(client):
#         tester = app.test_client(self)
#         response = tester.get('/auth/login',content_type='html/text')
#         self.assertEqual(response.status_code,200)