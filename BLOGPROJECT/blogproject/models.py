'''
blogproject/models.py
This file configures the User and BlogPost models for the SQLite database 
'''
from blogproject import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

#set the user_loader callback in order to reload user from session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin): #UserMixin to allow user authentication and login functionallity
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    
    posts = db.relationship('BlogPost',backref='author',lazy=True) #Creating a relationship between blog post and its author
    
    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
    
    #check password against hashed password
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self):
        return f"Username: {self.username}"

    
class BlogPost(db.Model):
    
    #configure relationship between each blog post and its author
    users = db.relationship(User)
     
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)
     
    def __init__(self,title,text,user_id):
         self.title = title
         self.text = text
         self.user_id = user_id
         
    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} -- {self.title}"
    
    