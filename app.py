from flask import Flask, Response, render_template
import cv2
import numpy as np
import os
import datetime

recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trained_data\\trainer.yml')
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default_copy.xml")
font=cv2.FONT_HERSHEY_SIMPLEX

id=0
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,640)
cap.set(4,480)

winW = 0.1*cap.get(3)
winH = 0.1*cap.get(4)

names=["None","Sai","Bhavana","Bhaskar","Sujatha","1"]


app = Flask(__name__)


def get_names(cap):
    people = set()
    while True:
        ret,img=cap.read()
        gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        faces=face_cascade.detectMultiScale(gray,1.2,5,minSize=(int(winW),int(winH)))
        for x,y,w,h in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),5)
            id,confidence=recognizer.predict(gray[y:y+h,x:x+w])
            if confidence<100:
                id=names[id]
                confidence="{0}%".format(round(100-confidence))
            else:
                id="unknown"
                confidence="{0}%".format(round(100-confidence))
            
            if id == "Sai":
                people.add(id)
            if id == "Bhavana":        
                people.add(id)
            if id == "Bhaskar":         
                people.add(id)
            if id == "Sujatha":    
                people.add(id)
            
            cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,0),3)
            cv2.putText(img,str(confidence),(x+5,y+h-5),font,1,(255,255,0),2)
        
        cv2.imshow("vid",img)
        cv2.waitKey(10)
        lpeople = list(people)
        if len(lpeople) > 0:
            break
        k = cv2.waitKey(10) & 0xff 
        if k == 27:
            break
    
    return lpeople
    
    


@app.route('/')
def index():
    global cap
    people = get_names(cap)
    #l_people = [p for p in people]
    return render_template("index.html", people=people, len=len(people))



if __name__ == '__main__':
    app.run(port=5000)
