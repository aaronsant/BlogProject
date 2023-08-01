''' blogproject/users/views.py
This file sets up the views for user registration, user login, user logout, account page
and user posts list
'''
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user,login_required

from blogproject import db
from blogproject.models import User, BlogPost
from blogproject.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from blogproject.users.picture_handler import add_profile_pic

users = Blueprint('users',__name__)

#register a new user
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))
    
    return render_template('register.html',form=form)

#login
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if  user.check_password(form.password.data) and user is not None :
            login_user(user)
            flash('Log in Success!')
            
            next = request.args.get('next') #set next as page the user was on before logging in
            
            #if the user was just trying to log in, set next to home page
            if next == None or not next[0]=='/':
                next = url_for('core.index')
                
            return redirect(next)
        
    return render_template('login.html',form=form)
                
#logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))
    
#account
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form =UpdateUserForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')
        
        return redirect(url_for('users.account'))
    
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template("account.html",profile_image=profile_image,form=form)
                
#users list of blog post
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int) # page number
    user = User.query.filter_by(username=username).first_or_404() #grab the user or return error if user not found
    #grab the users blog posts ordered, and 5 posts per page
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user)

