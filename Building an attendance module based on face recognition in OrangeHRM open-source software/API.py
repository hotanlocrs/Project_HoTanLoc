import cv2
from flask import Flask, request
import main
import pickle
def _load_pickle(file_path):
  with open(file_path, 'rb') as f:
    obj = pickle.load(f)
  return obj
em_loc = _load_pickle("Data/embed_blob_faces.pkl")
y_label = _load_pickle("Data/y_labels.pkl")
name_id= _load_pickle("Data/name_id.pkl")
app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def home_page():
    name=""
    if request.method =="POST":
        image = request.files['image']
        image.save("DataAPI/loc.jpg")
        frame = cv2.imread("DataAPI/loc.jpg")
        t=main.check_image(frame,em_loc,y_label)
        for i in range(0,len(name_id)):
            if name_id[i][0]==int(t):
                name=name_id[i][1]
        return t+":"+name
    return "0"
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)