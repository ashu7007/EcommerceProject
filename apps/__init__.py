import os
from flask import Flask

from dbConfig import db


def create_app():
    app = Flask(__name__)
    # app.config.from_pyfile(config_filename)
    app.config['SECRET_KEY'] = 'the random string'    

    # DB configuration
    username = 'postgres'
    password = 'postgres'
    host_url ='localhost'
    port = '5432'
    db_name = 'ecommerce'

    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{port}/{db_name}'.format(user=username,pw=password,url=host_url,port =port,db_name=db_name)

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning



    db.init_app(app)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    # )

    from apps.users import view
    # from yourapplication.views.frontend import frontend
    app.register_blueprint(view.bp)
    # app.register_blueprint(frontend)

    return app