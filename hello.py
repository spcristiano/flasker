from datetime import datetime
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


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
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favourite_color = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Creating function strings
    def __repr__(self):
        return '<Name %r>' % self.name


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
    email = StringField("Email", validators=[DataRequired()])
    favourite_color = StringField("Favourite Color")
    submit = SubmitField("Submit")


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
    first_name = 'John'
    stuff =  'This is a <b>Bold Text</b>'
    favourite_pizzars = ['pepperoni','Marka','melein',43, 'mandae',41]
    return render_template('index.html', first_name=first_name, stuff=stuff,favourite_pizzars=favourite_pizzars)


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
            user = User(
                name=form.name.data,
                email=form.email.data,
                favourite_color=form.favourite_color.data
            )
            db.session.add(user)
            db.session.commit()
            name = form.name.data
            form.name.data = ''
            form.email.data = ''
            form.favourite_color.data = ''
            flash(f'User with name {name.capitalize()} was Added Successfully', 'success') 
        else:
            email = form.email.data
            flash(f'User with this email {email} already exist. Please use another email', 'danger')
        
    # Display all users in the database and order by date added
    all_users = User.query.order_by(User.date_added)
    
    return render_template('add_user.html', form=form, all_users=all_users)
    
# update specific user database record
@app.route('/user/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    
    name_to_update = User.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favourite_color = request.form['favourite_color']
        
        try:
            db.session.commit()
            flash('User details updated successfully', 'success')
            
            # email = name_to_update.email
            
            return render_template('update.html', form=form, name_to_update=name_to_update)
        except:
            flash('Error updating this user. Please try again', 'danger')
            return render_template('update.html', form=form, name_to_update=name_to_update)
        
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update)
        

        
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