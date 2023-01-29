import numpy as np
import cv2

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
import glob
from keras.layers import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
import time
import random

emotion_model = Sequential()
emotion_model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
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
emotion_model.summary()
emotion_model.load_weights('model.h5')


bounding_box = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

img11 = cv2.imread('loctest.jpg')
(h, w, d) = img11.shape
dim=(w//4,h//4)
img12=cv2.resize(img11,dim)
gray_frame = cv2.cvtColor(img12, cv2.COLOR_BGR2GRAY)
num_faces = bounding_box.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)
for (x, y, w, h) in num_faces:
        cv2.rectangle(img12, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
        roi_gray_frame = gray_frame[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)
        emotion_prediction = emotion_model.predict(cropped_img)
        maxindex = int(np.argmax(emotion_prediction))
print(maxindex)
cv2.imshow('Display Image', img12)
cv2.waitKey(0)

foder={0:"angry",1:"disgust",2:"fear",3:"happy",4:"neutral",5:"sad",6:"surprise"}
t=0
k=0
for j in range(0,7):
        s="testdata/"+foder[j]+"/*jpg"
        path = glob.glob(s)
        cv_img = []
        for img1 in path:
            n = cv2.imread(img1)
            cv_img.append(n)
        for i in range(len(cv_img)):
                img=cv_img[i]
                gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                roi_gray_frame = gray_frame
                cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)
                emotion_prediction = emotion_model.predict(cropped_img)
                maxindex = int(np.argmax(emotion_prediction))
                if (maxindex==j) :
                        t=t+1
        k=k+len(cv_img)
print("---------------------")
print(k)
print(t)
c=(t/k)
print(c*100)
st="newdata/"+foder[1]+"/loc"+str(random.randint(1, 50))+".jpg"
s1=st.replace(" ","")
cv2.imwrite(s1, img12)

