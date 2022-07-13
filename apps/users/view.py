import datetime
import functools
from random import randint
from flask import current_app
from flask_mail import Mail, Message
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from .models import Userdata, OTP
from dbConfig import db


from sqlalchemy import create_engine,desc
from sqlalchemy.orm import sessionmaker


#some_engine = create_engine('postgresql://postgres:postgres@localhost/')
some_engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/ecommerce')

Session = sessionmaker(bind=some_engine)

db_session = Session()

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/")
def user_test():
    return "Hello app is working"



@bp.route("/register",methods=['GET','POST'])
def register():
    #form = RegistrationForm(request.form)
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        gender = request.form['gender']
        dob = request.form['dob']
        user_type = request.form['user_type']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        date =datetime.datetime.now()

        if error is None:
            try:
                user= Userdata(full_name=full_name,email=email,username=username,password=generate_password_hash(password),
                    address=address,gender=gender,dob=dob,
                 user_type=user_type,active=False,created_at=date,
                 updated_at=date)
                db_session.add(user)
                db_session.commit()
               
            except :
                raise 
                # error = f"User {username} is already registered."
            else:
                otp = randint(1001,9999)
                otp_object= OTP(user_id=user.id,otp=otp,created_at=date,updated_at=date)
                db_session.add(otp_object)
                db_session.commit()
                msg = Message(
                f'your otp is {otp}',
                sender ='avaish@deqode.com',
                recipients = [email]
               )
                msg.body = f'your otp is {otp}'
                mail = Mail(current_app)
                mail.send(msg)
                session['r_user_id'] = user.id
                return render_template('user/confirmEmail.html')
                # return redirect(url_for("auth.login"))

        flash(error)

    return render_template('user/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        error = None
        user = db_session.query(Userdata).filter(Userdata.username==user_name).first()
        print("this is user object",user)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            # return redirect(url_for('index'))
            return render_template('index.html')

        flash(error)

    return render_template('user/login.html')



@bp.route('/verify', methods=('POST',))
def verify():
    print(request.data)
    if request.method == 'POST':
        r_user_id = session.get('r_user_id')
        print(r_user_id)
        otp = request.form['otp']
        error = None
        db_session.query(OTP).filter(OTP.user_id == r_user_id).order_by(desc(OTP.created_at)).first()
        db_session.query(Userdata).filter(Userdata.id == r_user_id).update({'active': True})
        #db_session.query(OTP).filter(OTP.user_id == r_user_id).order_by(desc(OTP.created_at)).first().delete()
        db_session.commit()
    
    return render_template('index.html')




@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_session.query(Userdata).filter(Userdata.id==user_id).first()

@bp.route('/logout')
def logout():
    session.clear()
    # return redirect(url_for('index'))
    return "logged out"


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
