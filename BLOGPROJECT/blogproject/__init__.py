'''
blogproject/__init__.py
This file initializes the app, configures the SQLite database and migrations, configures the
login functionallity for the program, and sets up the flask blueprints to handle the views
'''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
 
#setting the secret key for security
app.config['SECRET_KEY'] ='mysecret' 

################ SQLALCHEMY DATABASE SETUP ##################
basedir = os.path.abspath(os.path.dirname(__file__))

#configure SQLite database relative to the app folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
###########################################################

################## LOGIN CONFIGURATION #####################
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'
###########################################################

############## BLUEPRINT CONFIGURATIONS ##################
from blogproject.core.views import core
from blogproject.users.views import users
from blogproject.blog_posts.views import blog_posts
from blogproject.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(error_pages)


