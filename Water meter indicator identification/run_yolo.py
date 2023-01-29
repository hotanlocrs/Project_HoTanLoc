import sys
import os
import subprocess



def run(img):
	subprocess.call([sys.executable, 'YOLO.py', '-i', img, '-cl', 'yolov3.txt', '-w', 'yolov3_800.weights', '-c', 'yolov3.cfg'])
