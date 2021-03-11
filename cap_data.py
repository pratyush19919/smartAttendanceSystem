import cv2
import time

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cap=cv2.VideoCapture(0)
i=0
while i<30:
    
    _,img=cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.5,2,minSize=(40,40))
    for x,y,w,h in faces:
        crop = img[y-5:y+h+5,x-5:x+w+5]
    cv2.imshow("crop",img)
    gray=cv2.cvtColor(crop,cv2.COLOR_RGB2GRAY)
    time.sleep(3)
    cv2.imwrite("train_data/s1/train"+str(i)+".jpg",gray)
    i=i+1


    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()