from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# creating flask instance
app = Flask(__name__)

# Creating secret key
app.config['SECRET_KEY'] = 'my super secret key that no one is required to know'


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
    return render_template('name.html', name=name, form=form)
    
# creating custom error pages

# invalid url

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
#  Internal Server error 
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
    