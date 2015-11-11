#!/usr/bin/python
#v0.7
from cv2 import *
from imutils import *
import os.path
from send import SendMail

def calibrate():
	i = 0
	while i < 100:
    		ret, frame = cap.read()
    		i = i + 1

def record():
	for j in range(100):
                if not os.path.isfile(str(j)+'.avi'):
                    out = VideoWriter(str(j)+'.avi',fourcc, 20.0, (640,480))
                    break
                elif j > 10:
                    print("Warning, there are over 10 video files.")
	for i in range(200):
		ret,frame=cap.read()
		out.write(frame)
		if i == 20:
			imwrite('preview'+str(j)+'.jpg',frame)
	out.release()
	print("Done recording.")
	SendMail('preview'+str(j)+'.jpg')
	print("Sent mail")


firstFrame = None
cap = VideoCapture(0)
fourcc = cv.CV_FOURCC(*'XVID')

print("Calibrating")
calibrate()
print("Camera online.")
z = 0
while(cap.isOpened()):

	good, frame = cap.read()
	if good:
		frame = cvtColor(frame,COLOR_BGR2GRAY)
		frame = GaussianBlur(frame, (21,21),0)
		if firstFrame is None:
			firstFrame = frame
			continue
	
		frameChange = absdiff(firstFrame,frame)
		thresh = threshold(frameChange, 25, 255, THRESH_BINARY)[1]
		thresh = dilate(thresh, None, iterations = 2)

        	(cnts, _) = findContours(thresh.copy(), RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
        
		for c in cnts:
			if contourArea(c) < 400:
				continue
			print("!ALERT!\nRecording...")
			record()
			firstFrame = None
			print("Monitoring...")
			break
	
		if waitKey(1) & 0xFF == ord('q'):
			break

	else:
		break
	
	z = z+1
	if z == 400:
		print("New first frame.")
		firstFrame = None
		z=0

cap.release()
