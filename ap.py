# from flask import Flask,render_template
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return render_template("index.html")

# if (__name__)==("__main__"):
#     app.run(debug=True)
from flask import Flask, render_template,redirect,request,url_for
from PIL import Image

import cv2
import numpy as np
import os

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
names = []
# recognizer = cv2.face.LBPHFaceRecognizer_create()
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/send',methods=["GET","POST"])
def cap_data():
    
    
    # if request.method=="POST":
    #     id_student = request.form.get("id_student")
    #     name = request.form.get("name")
        
    #     dirName="Images/"+name
        
    #     os.mkdir(dirName)

    names.append(name)
    
    # cap = cv2.VideoCapture(0)
    # count = 0
    # while True:

    #     ret, frame = cap.read()
    #     if  frame is not None:
    #         count += 1
    #         faces = face_classifier.detectMultiScale(frame, 1.3, 5)
            
        
            
        
            
    #         # Crop all faces found
    #     for (x,y,w,h) in faces:
    #         x=x-10
    #         y=y-10
    #         cropped_face = frame[y:y+h+50, x:x+w+50]

    #         face = cv2.resize(cropped_face, (400, 400))
    #         #face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

    #         # Save file in specified directory with unique name
    #         file_name_path = dirName + "/"+ str(count) + '.jpg'
    #         cv2.imwrite(file_name_path, face)

    #         # Put count on images and display live count
    #         cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
    #         cv2.imshow('Face Cropper', face)
    #     else:
    #         print("Face not found")
    #         pass
                 

    #     if cv2.waitKey(1) == 13 or count == 200: #13 is the Enter Key
    #         break

        


    # cap.release()
    # cv2.destroyAllWindows()      
    # print("Collecting Samples Complete")
        
    return render_template('train.html')

@app.route('/train',methods=["GET","POST"])
def train_face():
    if request.method=="POST":
        name = request.form.get("name")
    
    for i in range(1,201):
        path = "Images/" + name + "/"+ str(i) + '.jpg'

    

    


    


if __name__ == '__main__':
  app.run(debug=True)



