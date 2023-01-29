from flask import Flask, render_template, Response
import os
import math
import pickle
import numpy as np
import cv2
import pymysql
import main
import CheckPim
import Check_id

def _load_pickle(file_path):
  with open(file_path, 'rb') as f:
    obj = pickle.load(f)
  return obj
def _save_pickle(obj, file_path):
  with open(file_path, 'wb') as f:
    pickle.dump(obj, f)
cap = cv2.VideoCapture(0)
app = Flask(__name__)

def generate_frames():
    ktk = 0
    thongbao=" "
    day=[]
    em_loc = _load_pickle("Data/embed_blob_faces.pkl")
    y_label = _load_pickle("Data/y_labels.pkl")
    name_id= _load_pickle("Data/name_id.pkl")
    while (True):
        kt1=CheckPim.kt()
        name1=""
        if (kt1==1) :
            # print(kt1)
            em_loc = _load_pickle("Data/embed_blob_faces.pkl")
            y_label = _load_pickle("Data/y_labels.pkl")
            name_id = _load_pickle("Data/name_id.pkl")
        ret, frame = cap.read()
        name=main.check_image(frame,em_loc,y_label)
        if name!="":
            day.append(name)
        if len(day)>22:
            kt=1
            for i in range(len(day)-20,len(day)):
                if (day[len(day)-1]!= day[i]):
                    kt=0
            if kt:
                for tq in name_id:
                    if tq[0]==int(name):
                        thongbao=Check_id.check_id(int(name))+" Name : "+tq[1]
                        ktk=0
                day=[]
        if ktk>60:
            thongbao=" "
        ktk=ktk+1
        for tq in name_id:
            if name!="":
                if tq[0] == int(name):
                    name1=tq[1]
        frame=cv2.flip(frame,1)
        cv2.putText(frame, name1, (20,30), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1.5,color=(250, 1, 1))
        cv2.putText(frame, thongbao, (20, 100), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1.5, color=(1, 250, 1))
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
