import datetime
import functools
from flask import current_app
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User
from dbConfig import db


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


some_engine = create_engine('postgresql://postgres:postgres@localhost/')
# create a configured "Session" class
Session = sessionmaker(bind=some_engine)
# create a Session
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
        user_type = request.form['user_type']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                user= User(full_name=full_name,email=email,username=username,password=generate_password_hash(password),
                address=address,user_type=user_type,active=True,created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now())
                db_session.add(user)
                db_session.commit()

            except:
                error = f"User {username} is already registered."
            else:
               return redirect(url_for("auth.login"))

        flash(error)

    return render_template('user/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        error = None
        user = db_session.query(User).filter(User.username==user_name).first()
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


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_session.query(User).filter(User.id==user_id).first()

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
