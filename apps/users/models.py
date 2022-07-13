import datetime

from dbConfig.db import db



class Userdata(db.Model):
    __tablename__ = 'Userdata'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False,unique=True)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    dob =  db.Column(db.DateTime, default=None)
    user_type = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean,nullable = False)
    created_at = db.Column(db.DateTime)
    updated_at =db.Column(db.DateTime)


    def __repr__(self):
        return f"User('{self.email}','{self.username}')"

class OTP(db.Model):
    __tablename__ = 'otp'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Userdata.id'))
    otp =  db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at =db.Column(db.DateTime)

    def __repr__(self):
        return f"OTP'{self.id}','{self.otp}')"