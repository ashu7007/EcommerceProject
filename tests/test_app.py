import pytest
import datetime
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# from apps import app
# from apps.users.models import Userdata

# First party modules
from apps import app

date = datetime.datetime.now()

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_login_user(client,app):
        """to test login func"""
        response = client.post('/auth/login',
                               data=dict(username='admin', password='admin'), follow_redirects=True)
        self.assertIn(b'admin', response.data)
        # self.assertTrue(g.user.is_shopuser == True)
        self.assertEqual(response.status_code, 200)