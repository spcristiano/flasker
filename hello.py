from flask import Flask, render_template


# creating flask instance
app = Flask(__name__)

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



# creating custom error pages

# invalid url

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
#  Internal Server error 
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
    