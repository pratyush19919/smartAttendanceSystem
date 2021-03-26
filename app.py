from flask import Flask,render_template,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length
import sqlite3
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
conn = sqlite3.connect("user_database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////user_database.db"

app.config["SECRET_KEY"] = "ThisisSecret"
Bootstrap(app) 

app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(120),unique=True)
    email = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(120))

class loginForm(FlaskForm):
    username = StringField("username" , validators=[InputRequired(),Length(min=4,max=25)])
    password = PasswordField("password" , validators=[InputRequired(),Length(min=8,max=75)])
    remember = BooleanField("remember me")

class registerForm(FlaskForm):
    email = StringField("email" , validators=[ InputRequired(),Length(max=50)])
    username = StringField("username" , validators=[InputRequired(),Length(min=4,max=25)])
    password = PasswordField("password" , validators=[InputRequired(),Length(min=8,max=75)])
@app.route('/',methods=["POST","GET"])
def index():
    form = loginForm()

    if form.validate_on_submit():
        return "<h1>" + form.username.data + " " + form.password.data + User.password + User.username +"</h1>"
        # user = User.query.filter_by(username = form.username.data).first()
        # if user:
        #     if User.password == form.password.data:
        #         return redirect(url_for(dashboard))
        #     else:
        #         return "<h1>Invalid Username or Password</h1>"
    return render_template("index.html",form=form)


@app.route('/signup',methods=["POST","GET"])
def signup():
    form = registerForm()
    if form.validate_on_submit():
        # return "<h1>" + form.username.data + " " + form.email.data +" " +  form.password.data + "</h1>"
        new_user = User(username=form.username.data,email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return "<h1> New User has been created </h1>"
    return render_template("signup.html",form= form)


@app.route('/dashboard')
def dashboard():
    return 'Hello, World!'


if __name__ == "__main__":
    app.run(debug = True)
    db.create_all()
    