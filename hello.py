from flask import Flask, render_template

# Create a flask instance
app = Flask(__name__)


# Create a route decorator
@app.route('/')
# def index():
#     return "<h1>Hello World!</h1>"
def index():
    first_name = "John"
    # stuff = "This is <strong>Bold</strong> Text"
    stuff = "This is Bold Text"

    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template("index.html",
                           first_name=first_name,
                           stuff=stuff,
                           favorite_pizza=favorite_pizza)


'''
safe capitalize lower upper title trim striptags
'''


# localhost:5000/user/John
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)


# Crate Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# Internal Server URL
@app.errorhandler(500)
def page_not_found(error):
    return render_template("500.html"), 500
