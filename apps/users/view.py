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
from sqlalchemy.orm import sessionmaker,scoped_session


#some_engine = create_engine('postgresql://postgres:postgres@localhost/')
some_engine = create_engine('postgresql+psycopg2://admin:admin@localhost/ecommerce')
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=some_engine))
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
        if not password:
            error = 'password is required.'
        if not full_name:
            error = 'full name is required.'
        if not email:
            error = 'email is required.'
        if not address:
            error = 'address is required.'
        if not gender:
            error = 'gender is required.'
        if not user_type or user_type not in ['customer','Shopuser']:
            error = 'user_type should be customer or Shopuser .'
        elif not dob:
            error = 'dob is required.'
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

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None and user.active:
            session.clear()
            print('setting session',user.id)
            session['r_user_id'] = user.id
            # return redirect(url_for('index'))
            return render_template('index.html')
        else:
            error= "Please verify your email to login"
        flash(error)

    return render_template('user/login.html')



@bp.route('/verify', methods=('POST',))
def verify():
    if request.method == 'POST':
        r_user_id = session.get('r_user_id')
        otp = int(request.form['otp'])
        error = None
        otp_db = db_session.query(OTP).filter(OTP.user_id == r_user_id).order_by(desc(OTP.created_at)).first()
        if otp == otp_db.otp:
            db_session.query(Userdata).filter(Userdata.id == r_user_id).update({'active': True})
            #db_session.query(OTP).filter(OTP.user_id == r_user_id).order_by(desc(OTP.created_at)).first().delete()
            db_session.query(OTP).filter(OTP.id==otp_db.id).delete()
            db_session.commit()
            return redirect(url_for("auth.login"))
        return "incorrect Otp"


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route('/update_profile',methods=['GET','POST'])
def update_profile():
    print(request.method)
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        address = request.form.get('address')
        gender = request.form.get('gender')
        dob = request.form.get('dob')
        user_type = request.form.get('user_type')
        error = None

        print([full_name,email,username,gender])
        if not username:
            error = 'username is required.'
        # if not password:
        #     error = 'password is required.'
        if not full_name:
            error = 'full name is required.'
        # if not email:
        #     error = 'email is required.'
        if not address:
            error = 'address is required.'
        if not gender:
            error = 'gender is required.'
        if not user_type or user_type not in ['customer','Shopuser']:
            error = 'user_type should be customer or Shopuser .'
        elif not dob:
            error = 'dob is required.'
        date =datetime.datetime.now()
        print(error)
        if error is None:
            try:
                user = db_session.query(Userdata).filter(Userdata.username == username)
                print(user)
                update_object = {}
                if full_name and user.full_name != full_name:
                    update_object["full_name"] = full_name
                if username and user.username != username:
                    update_object["username"] = username
                if password and not check_password_hash(user.password, password):
                    update_object["password"] = password
                if address and user.address != address:
                    update_object["address"] = address
                if gender and user.gender != gender:
                    update_object["gender"] = gender
                if dob and user.dob != dob:
                    update_object["dob"] = dob
                if user_type and user.user_type != user_type:
                    update_object["user_type"] = user_type
                print(update_object)
                user = db_session.query(Userdata).filter(Userdata.username == username).update(update_object)
                db_session.commit()
               
            except :
                raise 
                # error = f"User {username} is already registered."
            else:
            #     otp = randint(1001,9999)
            #     otp_object= OTP(user_id=user.id,otp=otp,created_at=date,updated_at=date)
            #     db_session.add(otp_object)
            #     db_session.commit()
            #     msg = Message(
            #     f'your otp is {otp}',
            #     sender ='avaish@deqode.com',
            #     recipients = [email]
            #    )
            #     msg.body = f'your otp is {otp}'
            #     mail = Mail(current_app)
            #     mail.send(msg)
            #     session['r_user_id'] = user.id
            #     return render_template('user/confirmEmail.html')
                return render_template('index.html')
    
    r_user_id = session.get('r_user_id')
    print("user",r_user_id)
    user = db_session.query(Userdata).get(r_user_id)
    
    print(user)
 

    return render_template('user/updateProfile.html',user=user)
    


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('r_user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_session.query(Userdata).filter(Userdata.id==user_id).first()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
