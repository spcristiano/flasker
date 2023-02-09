from datetime import datetime
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

# creating flask instance
app = Flask(__name__)

# add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Creating secret key
app.config['SECRET_KEY'] = 'my super secret key that no one is required to know'

# Initialize the database
db = SQLAlchemy(app)


# Creating model class for database mapping
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
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
                email=form.email.data
            )
            db.session.add(user)
            db.session.commit()
            name = form.name.data
            form.name.data = ''
            form.email.data = ''
            flash(f'User with name {name} was Added Successfully', 'success') 
        else:
            email = form.email.data
            flash(f'User with this email {email} already exist. Please use another email', 'danger')
        
    # Display all users in the database and order by date added
    all_users = User.query.order_by(User.date_added)
    
    return render_template('add_user.html', form=form, all_users=all_users)
    
    
    
# creating custom error pages


# invalid url

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
#  Internal Server error 
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
    