import cv2

i=0
while i<30:
    img=cv2.imread("train_data/s4/train"+str(i)+".jpg")
    gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    cv2.imwrite("train_data/s4/train"+str(i)+".jpg",gray)
    i=i+1