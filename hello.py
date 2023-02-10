from datetime import datetime, date
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea


# creating flask instance
app = Flask(__name__)

# adding a sqlite database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# 
# adding a mysql and pymysql database
# 
# my main password is 'Blackbro1641@' but i had to escape the @ to become %40. This will interprete @ as %40 in the password since special characters are not directly allowed.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Blackbro1641%40@localhost/user_db'

# Creating secret key
app.config['SECRET_KEY'] = 'my super secret key that no one is required to know'

# Initialize the database
db = SQLAlchemy(app)

# Initializing the migrate extension
migrate = Migrate(app, db)


# Creating model class for database mapping

# user model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favourite_color = db.Column(db.String(200))
    username = db.Column(db.String(200),nullable=False, unique=True)
    password_hash = db.Column(db.String(300), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # setting password hashing system
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)
    
    # Creating function strings
    def __repr__(self):
        return '<Name %r>' % self.name

# creating blog post model
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    content = db.Column(db.Text)
    author = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(300))

# creating a form class

#These are some flask wtf fields
# BooleanField
# DateField
# DateTimeField
# DecimalField
# FileField
# HiddenField
# MultipleField
# FieldList
# FloatField
# FormField
# IntegerField
# PasswordField
# RadioField
# SelectField
# SelectMultipleField
# SubmitField
# StringField
# TextAreaField

# These are some flask wft field validators
# DataRequired
# Email
# EqualTo
# InputRequired
# IPAddress
# Length
# MacAddress
# NumberRange
# Optional
# Regexp
# URL
# UUID
# AnyOf
# NoneOf

class NamerForm(FlaskForm):
    name = StringField("What is your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    # email = StringField("Email", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message="Password Must Match")])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password_hash', message="Password Must Match")])
    favourite_color = StringField("Favourite Color")
    submit = SubmitField("Submit")
    
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    # content = StringField('Content',validators=[DataRequired()], widget=TextArea())
    author = StringField('Author', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Post')
    


# '''
# # These are some jinger templating functions
# safe
# capitalize
# lower
# upper
# tittle
# trim
# striptags

# '''
# creating a route decorator

@app.route('/')
def index():
    form = UserForm()
    return render_template('login.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = UserForm()
    
    # Validate form
    # if form.validate_on_submit():
    #     email= form.email.data
    #     password = form.password_hash.data
    #     form.email.data =''
    #     form.password_hash.data = ''
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password_hash']
        
        form.email.data =''
        form.password_hash.data = ''
        
        # query database
        pw_to_check = User.query.filter_by(email=email).first()
        if pw_to_check:
            username = pw_to_check.username
            user_password = pw_to_check.password_hash
            passed = check_password_hash(user_password, password)
            # authenticating the user
            if passed == True:
                flash(f'Dear {username}, welcome to our site', 'success')
                return render_template('dashboard.html', form=form, passed=passed)
            else:
                flash(f'Dear {username}, your password is not correct', 'danger')
                return redirect(url_for('login'))
                # return render_template('login.html', form=form, passed=passed)
                
            # flash(f'Dear {username}, welcome to our site', 'success')
            # return render_template('dashboard.html', form=form, passed=passed)
        else:
            user = email
            flash(f'This user {user} is not yet registered on our website', 'danger')
            return redirect(url_for('index'))
            # return render_template('login.html', form=form, passed=passed)
            
            
            # return redirect(url_for('dashboard', id=id))
            
            
        # return render_template('login.html', form=form, passed=passed)
    
            
        # if pw_to_check:
        #     username = pw_to_check.username
        #     user_password = pw_to_check.password_hash
        #     passed = check_password_hash(user_password, password)
        #     flash(f'Dear {username}, welcome to our site', 'success')
        #     return render_template('dashboard.html', passed=passed)
        # else:
        #     user = form.email.data
        #     flash(f'This {user} is not yet registered on our website', 'danger')
        #     return render_template('login.html', form=form)
    # else:
    #     # user = form.email.data
    #     # flash(f'This {user} is not yet registered on our website', 'danger')
    # return render_template('dashboard.html', form=form, passed=passed)
    return render_template('login.html', form=form, passed=passed)
    


@app.route('/user/<username>')
def profile(username):
    username = 'John'
    first_name = 'Mike'
    stuff =  'This is a <b>Bold Text</b>'
    favourite_pizzars = ['pepperoni','Marka','melein',43, 'mandae',41]
    return render_template('user.html', first_name=first_name, stuff=stuff,favourite_pizzars=favourite_pizzars)



@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form Submitted Successfully', 'success')
    return render_template('name.html', name=name, form=form)

# add new users
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    # validate form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pwd = generate_password_hash(form.password_hash.data, 'sha256')
            user = User(
                name=form.name.data,
                email=form.email.data,
                favourite_color=form.favourite_color.data,
                username=form.username.data,
                password_hash=hashed_pwd
            )
            db.session.add(user)
            db.session.commit()
            
            name = form.name.data
            # clearing form data
            form.name.data = ''
            form.email.data = ''
            form.favourite_color.data = ''
            form.username.data = ''
            form.password_hash.data = ''
            flash(f'User with name {name.capitalize()} was Added Successfully', 'success')
            return redirect(url_for('add_user'))
        else:
            email = form.email.data
            flash(f'User with this email {email} already exist. Please use another email', 'danger')
            return redirect(url_for('add_user'))
            
        
    # Display all users in the database and order by date added
    all_users = User.query.order_by(User.date_added)
    
    return render_template('add_user.html', form=form, all_users=all_users)
    
# update specific user database record
@app.route('/user/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    
    name_to_update = User.query.get_or_404(id)
    # password_to_update = name_to_update.password_hash
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favourite_color = request.form['favourite_color']
        name_to_update.username = request.form['username']
        # name_to_update.password_hash = request.form['password_hash']
        
        
        
        try:
            db.session.commit()
            flash('User details updated successfully', 'success')
            
            # email = name_to_update.email
            return redirect(url_for('update', id=id))
            # return render_template('update.html', form=form, name_to_update=name_to_update)
        except:
            flash('Error updating this user. Please try again', 'danger')
            return redirect(url_for('update', id=id))
            
            # return render_template('update.html', form=form, name_to_update=name_to_update)
        
    # else:
    return render_template('update.html', form=form, name_to_update=name_to_update)
    
        

# update password only
@app.route('/update_password/<int:id>', methods=['GET', 'POST'])
def update_password(id):
    form = UserForm()
    
    name_to_update = User.query.get_or_404(id)
    
    
    if request.method == 'POST':
        hashed_pwd = generate_password_hash(request.form['password_hash'], 'sha256')
        
        # name_to_update.password_hash = request.form['password_hash']
        name_to_update.password_hash = hashed_pwd
        username = name_to_update.username 
        username = username       
        try:
            db.session.commit()
            flash(f'Dear {username} your password have been successfully updated ', 'success')
            return redirect(url_for('update', id=id))
        except:
            flash(f'Dear {username}, There was an error updating your password', 'danger')
            # return render_template('update.html', form=form, password_to_update=password_to_update)
            return redirect(url_for('update', id=id))
    # else:
    #     return render_template('update.html', form=form, name_to_update=name_to_update)
    return render_template('update.html', form=form, name_to_update=name_to_update)
        
      
        
#   Using Json      # 
@app.route('/date')
def get_current_date():
    favourite_pizza ={
        "John": "Peperoni",
        "Mary": "Manaku",
        "Eli": "Saltidi"
    }
    # return {"Date": date.today()}
    return (favourite_pizza)
    
    

        
   # delete specific user database record
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    # form = UserForm()
    
    user_to_delete = User.query.get_or_404(id)
    # if request.method == 'POST':
    #     name_to_update.name = request.form['name']
    #     name_to_update.email = request.form['email']
    #     name_to_update.favourite_color = request.form['favourite_color']
        
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User deleted successfully', 'success')
        
         # Display all users in the database and order by date added
        all_users = User.query.order_by(User.date_added)
        return redirect(url_for('add_user'))
        
        # return render_template('add_user.html', all_users=all_users, form=form)
        
        # return render_template('update.html', form=form, name_to_update=name_to_update)
    except:
        flash('Error deleting this user. Please try again', 'danger')
        # return render_template('add_user.html', all_users=all_users, form=form)
    return render_template('add_user.html', all_users=all_users)
        
        

@app.route('/add_post', methods=['GET', 'POST'])     
def add_post():
    form = PostForm()
    posts = Post.query.order_by(Post.date_posted)
    
    
    #  checking if the form is submitted
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        
        # clering the form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''  
    
        # adding post data to database
        db.session.add(post)
        db.session.commit() 

        # returning a message
        flash('Blog post submitted successfully', 'success') 
        return redirect(url_for('add_post'))
        
        # show all blog posts
    return render_template('add_post.html', form=form, posts=posts)

# showing single post
@app.route('/single_post/<slug>/<int:id>')
def single_post(slug, id):
    form = PostForm()
    posts = Post.query.order_by(Post.date_posted)    
    return render_template('single_post.html', form=form, posts=posts)
    
# editing Post
@app.route('/update_post/<int:id>', methods=['GET', 'POST'])
def update_post(id):
    form = PostForm()
    # query all posts
    posts = Post.query.order_by(Post.date_posted)    
    
    post_to_update = Post.query.get_or_404(id)
    if form.validate_on_submit():
        # post_to_update = Post.query.get_or_404(id)
        if post_to_update:
            post_to_update.title = form.title.data
            post_to_update.content = form.content.data
            post_to_update.author = form.author.data
            post_to_update.slug = form.slug.data
            try:
                db.session.commit()
                flash(f'Post with id {id} was successfully updated', 'success')
                return redirect(url_for('add_post'))
            except:
                flash('Error updating this post. Please try again', 'danger')
                return redirect(url_for('update_post', id=id))
        else:
            return redirect(url_for('add_post'))
    return render_template('update_post.html', form=form, posts=posts, post_to_update=post_to_update)
    
                
                
                
            
        
        
    # if request.method == 'POST':
    #     post_to_update.title = request.form['title']
    #     post_to_update.content = request.form['content']
    #     post_to_update.author = request.form['author']
    #     post_to_update.slug = request.form['slug']
        
        # try:
        #     db.session.commit()
        #     flash('Post successfully updated', 'success')
        #     redirect(url_for('update_post', id=id))
            
            # redirect(url_for('add_post'))
            
            # return render_template('add_post', form=form, posts=posts)
        # except:
            # flash('Error updating this post. Please try again', 'danger')
            # redirect(url_for('update_post', id=id))            
            # return render_template('update_post.html', form=form, posts=posts)
    # else:
        # redirect(url_for('update_post', id=id))            
    
    #     return render_template('add_post.html', form=form, posts=posts)
    # return render_template('update_post.html', form=form, posts=posts, post_to_update=post_to_update)
            
#  delete post
@app.route('/delete_post/<int:id>', methods=['GET', 'POST'])
def delete_posts(id):
    post_to_delete = Post.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash(f'Post with id {id} and title {post_to_delete.title} has been deleted successfully. ', 'success')
        
        posts = Post.query.order_by(Post.date_posted)    
        
        return redirect(url_for('add_post'))
    except:
        flash('Error deleting this post. Please try agian', 'danger')
    return render_template('add_post.html',posts=posts)


# creating custom error pages


# invalid url

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
#  Internal Server error 
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
    
    
if __name__ == '__main__':
    app.run(debug = True)
    