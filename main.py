from cv2 import *
from imutils import *
import os.path
from send import SendMail

cap = VideoCapture(0)
firstFrame = None
text = "all clear"

fourcc = cv.CV_FOURCC(*'XVID')

i = 0
while i < 100:
    ret, frame = cap.read()
    i = i + 1

print("Camera online.")
while(cap.isOpened()):

    ret, frame = cap.read()

    if ret == True:
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
            if contourArea(c) < 300:
                continue
            print("!ALERT!\nRecording...")
            for j in range(100):
                if not os.path.isfile(str(j)+'.avi'):
                    out = VideoWriter(str(j)+'.avi',fourcc, 20.0, (640,480))
                    break
                elif j > 10:
                    print("Warning, there are over 10 video files.")
            i = 0
            while i < 200:
                ret,frame=cap.read()
                out.write(frame)
                i = i + 1
		if i == 20:
			imwrite('preview'+str(j)+'.jpg',frame)
            out.release()
            firstFrame = None
	    print("Done recording.")
	    SendMail('preview'+str(j)+'.jpg')



    	#imshow("Security Feed", frame)
        if waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break


cap.release()
