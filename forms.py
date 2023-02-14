# Import Statement
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, RadioField,ValidationError, TextAreaField, EmailField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from wtforms_validators import  AlphaNumeric, Integer
from wtforms.widgets import TextArea


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
    name = StringField("Name", validators=[DataRequired(message='Name field is required. Please input your name')])
    username = StringField("Username", validators=[DataRequired(message='Username field is required. Please input your username'), AlphaNumeric(message='This field can only contain alphabets and numbers')])
    # email = StringField("Email", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(message='Email field is required. Please input your email'), Email(message='Please insert an email in this field')])
    password_hash = PasswordField("Password", validators=[DataRequired(message='Password field is required. Please input your password'), EqualTo('password_hash2', message="Password do not match. This password must match the confirm password field"), Length(message='Password must be at least 6 characters long',min=6)],id='password_hash')
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password_hash', message="Password do not match. This confirm password field must match the password field")],id='password_hash2')
    favourite_color = StringField("Favourite Color")
    show_password = BooleanField('Show Password', id='flexSwitchCheckDefault')
    submit = SubmitField("Submit")
    
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='This title field is required. Please give your post a title')])
    # content = TextAreaField('Content',validators=[DataRequired()], default='Write your post here')
    content = StringField('Content',validators=[DataRequired(message='This content field is requred. Please write your post here')], widget=TextArea())
    # author = StringField('Author', validators=[DataRequired(message='This author field is required. Please write the author of this post')])
    slug = StringField('Slug', validators=[DataRequired(message='This slug field is required. Please give your message a slug to for more usability.')])
    submit = SubmitField('Post')
    
