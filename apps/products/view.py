import os
import datetime
import functools
from random import randint
from flask import current_app
from flask_mail import Mail, Message
from flask_login import login_required
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from dbConfig import db

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session

# some_engine = create_engine('postgresql://postgres:postgres@localhost/')
some_engine = create_engine('postgresql+psycopg2://admin:admin@localhost/ecommerce')
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=some_engine))
Session = sessionmaker(bind=some_engine)

db_session = Session()

product_bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/', methods=('GET'))
@login_required
def index():
    return render_template('index.html')
