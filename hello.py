from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate


"""
Flask Web 开发实战
"""
from flask_bootstrap import Bootstrap
"""
Flask Web 开发实战
"""


# Create a flask instance
app = Flask(__name__)
# Add Database
# Old SQLite DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# New MySQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yql031220@localhost/our_users'
# Secret Key
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"
# Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


"""
Flask Web 开发实战
"""
bootstrap = Bootstrap(app)
"""
Flask Web 开发实战
"""


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    data_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name


# Crate a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")


# Update Database Record
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User Update Successfully!")
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update)
        except:
            flash("Error! Looks like there was a problem... try again!")
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template('update.html',
                               form=form,
                               name_to_update=name_to_update)


# Crate a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


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


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''

        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.data_added)
    return render_template('add_user.html', name=name,
                           form=form, our_users=our_users)


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


# Create a Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")
    return render_template("name.html", name=name, form=form)
