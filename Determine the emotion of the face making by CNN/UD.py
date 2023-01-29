import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import os
import numpy as np
import cv2
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
import time
import random
emotion_model = Sequential()
emotion_model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
emotion_model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))
emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))
emotion_model.add(Flatten())
emotion_model.add(Dense(1024, activation='relu'))
emotion_model.add(Dropout(0.5))
emotion_model.add(Dense(7, activation='softmax'))
emotion_model.load_weights('model.h5')
cv2.ocl.setUseOpenCL(False)

bieucam = {0: "Tức giận", 1: "Ghê tởm", 2: "Sợ hãi", 3: "Cười", 4: "Bình thường",
                5: "Buồn", 6: "Ngạc nhiên"}
newfoder={0:" / angry / ",1:"/ disgust / ",2:" / fear / ",3:" / happy / ",4:" / neutral / ",5:" / sad / ",6:" / surprise / "}

a=[]
b=[0,0,0,0,0,0,0]

window = Tk()
window.geometry("800x600")
text="ỨNG DỤNG ĐÁNH GIÁ CẢM XÚC CỦA NGƯỜI XEM PHIM BẰNG TENSORFLOW"
text1="Đánh giá"
lbl=Label(window, text=text1,fg="red",font=("Arial",15))
lbl.grid(column=0,row=0)
ten=Label(window, text="Tên Phim:(không dấu)",fg="Blue",font=("Arial",15))
ten.grid(column=0,row=1)
txt1=Entry(window, width=60)
txt1.grid(column=1,row=1)
thoigian=Label(window, text="Thời gian chiếu(Phút):",fg="Blue",font=("Arial",15))
thoigian.grid(column=0,row=2)
txt2=Entry(window, width=60)
txt2.grid(column=1,row=2)



def runct():
    dim = (48, 48)

    cap = cv2.VideoCapture(0)
    tgc=int(txt2.get())*60
    f = open('KQ.txt', 'a')
    for i in range(0,tgc):
        time.sleep(1)
        ret, frame = cap.read()
        if not ret:
            break
        bounding_box = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        num_faces = bounding_box.detectMultiScale(gray_frame,scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)
            emotion_prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(emotion_prediction))
            a.append(maxindex)
            print(maxindex)
            anhluu=cv2.resize(roi_gray_frame, dim, interpolation = cv2.INTER_AREA)
            s="newdata"+newfoder[maxindex]+"IMG"+str(random.randint(1, 50))+".jpg"
            s1=s.replace(" ","")
            cv2.imwrite(s1, anhluu)

    if len(a)>2:
        for i in range(1,len(a)):
            if (a[i]!=a[i-1]) :
                b[a[i-1]]=b[a[i-1]]+1
        b[a[len(a)-1]]=b[a[len(a)-1]]+1
    s2=str(txt1.get())
    f.write(s2+":"+str(b)+" , ")
    lbl0.configure(text=bieucam[0] + ":" + str(b[0]))
    lbl1.configure(text=bieucam[1] + ":" + str(b[1]))
    lbl2.configure(text=bieucam[2] + ":" + str(b[2]))
    lbl3.configure(text=bieucam[3] + ":" + str(b[3]))
    lbl4.configure(text=bieucam[4] + ":" + str(b[4]))
    lbl5.configure(text=bieucam[5] + ":" + str(b[5]))
    lbl6.configure(text=bieucam[6] + ":" + str(b[6]))
btnrun=Button(window,text="chạy",command=runct)
btnrun.grid(column=1,row=3)
lbl0=Label(window, text=bieucam[0]+":",fg="Black",font=("Arial",10))
lbl0.grid(column=0,row=4)
lbl1=Label(window, text=bieucam[1]+":",fg="Black",font=("Arial",10))
lbl1.grid(column=0,row=5)
lbl2=Label(window, text=bieucam[2]+":",fg="Black",font=("Arial",10))
lbl2.grid(column=0,row=6)
lbl3=Label(window, text=bieucam[3]+":",fg="Black",font=("Arial",10))
lbl3.grid(column=0,row=7)
lbl4=Label(window, text=bieucam[4]+":",fg="Black",font=("Arial",10))
lbl4.grid(column=0,row=8)
lbl5=Label(window, text=bieucam[5]+":",fg="Black",font=("Arial",10))
lbl5.grid(column=0,row=9)
lbl6=Label(window, text=bieucam[6]+":",fg="Black",font=("Arial",10))
lbl6.grid(column=0,row=10)
window.mainloop()
