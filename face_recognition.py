import cv2
import numpy as np
import os
import datetime
import time

recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trained_data\\trainer.yml')
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default_copy.xml")
font=cv2.FONT_HERSHEY_SIMPLEX

id=0

names=["None","Sai","Bhavana","Bhaskar","Sujatha","1"]


cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,640)
cap.set(4,480)

winW=0.1*cap.get(3)
winH=0.1*cap.get(4)
people = set()
def att(name):
    with open("att.csv","r+") as f:
        myDataList=f.readlines()
        namesList=[]
        for i in myDataList:
            entry=i.split(",")
            namesList.append(entry[0])
        if name not in namesList:
            now=datetime.datetime.now()
            dtstring=now.strftime("%H/%M/%S")
            f.writelines(f'\n{name},{dtstring}')

while True:
    ret,img=cap.read()
    gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.2,5,minSize=(int(winW),int(winH)))
    for x,y,w,h in faces:
        
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),5)
        id,confidence=recognizer.predict(gray[y:y+h,x:x+w])
        if 30<confidence<65:
            id=names[id]
            confidence="{0}%".format(round(100-confidence))
        else:
            id="unknown"
            confidence="{0}%".format(round(100-confidence))
        
        if id == "Sai":
            att(id)
            people.add(id)
        if id == "Bhavana":
            att(id)        
            people.add(id)
        if id == "Bhaskar":
            att(id)            
            people.add(id)
        if id == "Sujatha":
            att(id)        
            people.add(id)
        

        cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,0),3)
        cv2.putText(img,str(confidence),(x+5,y+h-5),font,1,(255,255,0),2)
       
    cv2.imshow("vid",img)
    k = cv2.waitKey(10) & 0xff 
    if k == 27:
        break
l_people=list(people)
#print(l_people)
    
cap.release()
cv2.destroyAllWindows()






