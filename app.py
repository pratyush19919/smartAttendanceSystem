from flask import Flask,render_template,url_for,redirect,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from train_data import get_faces_id


import cv2
import numpy as np
import os




app = Flask(__name__)
faces_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
conn = sqlite3.connect("user_database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////user_database.db"

app.config["SECRET_KEY"] = "ThisisSecret"
Bootstrap(app) 

app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

recognizer = cv2.face.LBPHFaceRecognizer_create()


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
        # return "<h1>" + form.username.data + " " + form.password.data + User.password + User.username +"</h1>"
        user = User.query.filter_by(username = form.username.data).first()
        
        if user:
            if user.password == form.password.data:
                if user.username == "admin":
                    return render_template("admin.html")
        
                else:
                    return render_template("teacher.html")
        else:   
            
            return "<h1>Invalid Username or Password</h1>"
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


@app.route('/dashboard', methods=["POST","GET"])
def cap_data():
    if request.method=="POST":
        id_student = request.form.get("id_student")
        name = request.form.get("name")
        
        dirName="Images/"+name+id_student
        
        os.mkdir(dirName)

    
    
    cap = cv2.VideoCapture(0)
    count = 0
    while True:

        ret, frame = cap.read()
        if  frame is not None:
            count += 1
            faces = faces_cascade.detectMultiScale(frame, 1.3, 5)
            
        
            
        
            
            # Crop all faces found
        for (x,y,w,h) in faces:
            x=x-10
            y=y-10
            cropped_face = frame[y:y+h+50, x:x+w+50]

            face = cv2.resize(cropped_face, (400, 400))
            gray=cv2.cvtColor(face,cv2.COLOR_RGB2GRAY)
            #face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            # Save file in specified directory with unique name
            file_name_path = dirName + "/" + str(count) + '.jpg'
            cv2.imwrite(file_name_path, gray)

            # Put count on images and display live count
            cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            cv2.imshow('Face Cropper', face)
        else:
            print("Face not found")
            pass
                 

        if cv2.waitKey(1) == 13 or count == 200: #13 is the Enter Key
            break

        


    cap.release()
    cv2.destroyAllWindows()      
    print("Collecting Samples Complete")
        
    return render_template('train.html',name = name,id="id_student")

@app.route('/train',methods=["GET","POST"])
def train_face():
    if request.method == "POST":
        name = request.form.get("name")

    faces, ids = get_faces_id("Images/") 
    for i in range(0, len(ids)):
        ids[i] = int(ids[i]) 

    recognizer.train(faces, np.array(ids))
    recognizer.write("trained_data/trainer.yml")

    return "<h1>Face trained </h1>"


@app.route("/class1")
def class1():
    return render_template("class1.html")

@app.route("/class2")
def class2():
    return render_template("class2.html")

@app.route("/take_att")
def take_att():
    return "Attendance taken"


        


if __name__ == "__main__":
    app.run(debug = True)
    db.create_all()
