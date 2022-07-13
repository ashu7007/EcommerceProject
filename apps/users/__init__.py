# import os
# from flask import Flask

# from dbConfig import db


# def create_app(config_filename):
#     app = Flask(__name__)
#     app.config.from_pyfile(config_filename)
#     username = 'postgres'
#     password = 'postgres'
#     host_url ='localhost'
#     port = '5432'
#     db_name = 'ecommerce'

#     DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{port}/{db}'.format(user=username,pw=password,url=host_url,port =port,db=db_name)

#     app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning


#     db.init_app(app)

#     from apps.users import view
#     # from yourapplication.views.frontend import frontend
#     app.register_blueprint(view.bp)
#     # app.register_blueprint(frontend)

#     return app





# def create_app(test_config=None):
#     """Create and configure an instance of the Flask application."""
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         # a default secret that should be overridden by instance config
#         SECRET_KEY="dev",
#         # store the database in the instance folder
#         DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
#     )

#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile("config.py", silent=True)
#     else:
#         # load the test config if passed in
#         app.config.update(test_config)

#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     db.init_app(app)

#     # apply the blueprints to the app
#     # app.register_blueprint(auth.bp)
#     # app.register_blueprint(blog.bp)

#     # make url_for('index') == url_for('blog.index')
#     # in another app, you might define a separate main index here with
#     # app.route, while giving the blog blueprint a url_prefix, but for
#     # the tutorial the blog will be the main index
#     app.add_url_rule("/", endpoint="index")

#     return app