#!/usr/bin/python

from cv2 import *
from time import sleep

cap = VideoCapture(0)
print("Calibrating")
for i in range(100):
	good, frame = cap.read()
print("Reading frame")
good, frame = cap.read()
print("Saving frame")
imwrite("frame.jpg",frame)


