import pytest

# First party modules
from apps import app, db_sql
from apps.users.models import Userdata


@pytest.fixture
def client():
    # app = create_app()

    app.config["TESTING"] = True
    app.testing = True

    # This creates an in-memory sqlite db
    # See https://martin-thoma.com/sql-connection-strings/
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    client = app.test_client()
    with app.app_context():
        db_sql.create_all()
        admin = Userdata(full_name="full_name", email="email@123.com", 
                            username="admin3", 
                            password=generate_password_hash("admin"),
                            address="address", gender="male", dob=date, 
                            active=True, is_admin=True,
                            is_customer=False,is_shopuser=False, 
                            created_at=date,updated_at=date)
        db.session.add(admin)
        db.session.commit()
    yield client