#! /usr/bin/env python2
#import vision_lib
from detection import *
from filtering import *
from draw import *
from optical_flow import *
import numpy as np
import cv2
import vision_lib


cap = cv2.VideoCapture(0) # 0 means /dev/video0, 1 for /dev/video1, ...   
test=True
while test :
    #get image flow
    _, frame= cap.read()

    # color grey

    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    previous_image=None
    previous_time=None
    previous_values=None

        #time.sleep(0.3)

    if previous_image is None:
        previous_image=frame
        #previous_time=now = msg.header.stamp
        previous_values=vision_lib.optical_flow.values(frame,100)
        
        
        # if time is required in your cumputation, consider the current time
        # as the one recorded in the message timestamps. This enables a coherent
        # time sequence when the images come from a ros bag, since ros bag execution
        # can be paused, run step by step, ...
        
    #now = msg.header.stamp
    #delta=(now)-(self.previous_time)
        
    current_values=vision_lib.optical_flow.values(frame,100)
    #print current_values
    frame_copy=frame.copy()
    vision_lib.optical_flow.draw_function(frame_copy,current_values , 205, 405 , 0, 255, (255,255,255), 1)
    vision_lib.optical_flow.draw_function(frame_copy,previous_values , 200, 400 , 0, 255, (0,0,255), 1)

    shifts=[]
    for x in range(frame.shape[1]):
        shifts.append(40*vision_lib.optical_flow.local_shift(x,current_values,previous_values,'left', 10, 10))
    
    vision_lib.optical_flow.draw_function(frame_copy,np.array(shifts), 0, 200 , 0, 255, (0,0,255), 1)
    print(shifts)

    previous_image=frame
    previous_values=current_values
    #previous_time= now

    
    #show image

    cv2.imshow('img',frame_copy)

    #quit 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()