import datetime

from dbConfig.db import db



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False,unique=True)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean,nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at =db.Column(db.DateTime, default=datetime.datetime.now)


    def __repr__(self):
        return f"User('{self.email}','{self.username}')"