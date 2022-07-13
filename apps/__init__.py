import os
from flask import Flask
from flask_bootstrap import Bootstrap
from dbConfig import db


def create_app():
    app = Flask(__name__)
    # app.config.from_pyfile(config_filename)
    app.config['SECRET_KEY'] = 'qwerty'    
    Bootstrap(app)
    
    # DB configuration
    username = 'admin'
    password = 'admin'
    host_url ='localhost'
    port = '5432'
    db_name = 'ecommerce'
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{port}/{db_name}'.format(
        user=username,pw=password,url=host_url,port =port,db_name=db_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning


    # configuration of mail
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    

    db.init_app(app)
    # app.config.from_mapping(SECRET_KEY='dev',)

    from apps.users import view
    app.register_blueprint(view.bp)


    return app