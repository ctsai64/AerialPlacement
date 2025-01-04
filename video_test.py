# last updated 1/1/2024

import cv2
from datetime import datetime

cam = cv2.VideoCapture("/dev/video0")
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
vid_cod = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter("cam_video.mp4", vid_cod, 20.0, (640,480))

while(True):
     # Capture each frame of webcam video
     ret,frame = cam.read()
     cv2.putText(frame, str(datetime.now()), (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)
     cv2.imshow("Camera", frame)
     output.write(frame)
     # Close and break the loop after pressing "x" key
     if cv2.waitKey(1) &0XFF == ord('x'):
         break

# close the already opened camera
cam.release()
# close the already opened file
output.release()
# close the window and de-allocate any associated memory usage
cv2.destroyAllWindows()
