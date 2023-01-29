import cv2
import os
import numpy as np
import pickle
from scipy import spatial
import Face_Detect
import Face_Rec
import Comparison

def _load_pickle(file_path):
  with open(file_path, 'rb') as f:
    obj = pickle.load(f)
  return obj
def _save_pickle(obj, file_path):
  with open(file_path, 'wb') as f:
    pickle.dump(obj, f)

def check_image(image,em_loc,y_label):
  faces = Face_Detect.face_mtcnn(image)
  name=""
  if len(faces)==1:
    face=faces[0]
    vec_face=Face_Rec.Arc_Face_embed(face)
    if len(vec_face)>0:
      vec=[]
      vec.append(vec_face)
      name=Comparison.faiss_t(em_loc,vec,y_label)
  return name





def add_u(name,image):
  em_loc = _load_pickle("Data/embed_blob_faces.pkl")
  y_label=_load_pickle("Data/y_labels.pkl")
  faces=Face_Detect.face_mtcnn(image)
  if len(faces)>0:
    embed = Face_Rec.Arc_Face_embed(faces[0])
    if (len(embed)!=0):
      em_loc.append(embed)
      y_label.append(name)
  _save_pickle(em_loc, "Data/embed_blob_faces.pkl")
  _save_pickle(y_label, "Data/y_labels.pkl")

def remove_u(name):
  em_loc = _load_pickle("Data/embed_blob_faces.pkl")
  y_label=_load_pickle("Data/y_labels.pkl")
  i=0
  while (i<len(y_label)):
    if y_label[i]==name:
      y_label.pop(i)
      em_loc.pop(i)
      i=i-1
    i=i+1
  _save_pickle(em_loc, "Data/embed_blob_faces.pkl")
  _save_pickle(y_label, "Data/y_labels.pkl")
