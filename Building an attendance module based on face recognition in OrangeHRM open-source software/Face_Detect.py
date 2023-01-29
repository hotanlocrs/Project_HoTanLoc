import cv2
from facenet_pytorch import MTCNN
import torch
import numpy as np
device =  torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(thresholds= [0.7, 0.7, 0.8] ,keep_all=True, device = device)
def face_mtcnn(image):
    boxes, _ = mtcnn.detect(image)
    t=[]
    if boxes is not None:
            box=boxes[0]
            bbox = list(map(int,box.tolist()))
            crop_img = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]
            t.append(crop_img)
    return t