#Python program to implement  
# Webcam Motion Detector 
'''

(75,75)-----------------------------
                                    |
                                    |
                                    |
                                    |
                                    |
                                    |
---------------------------- (580,420)
'''




# importing OpenCV, time and Pandas library 
import cv2, time, pandas, timeit
from statistics import mode
from multiprocessing import Process
from pynput.keyboard import Key, Controller
# importing datetime class from datetime library 
from datetime import datetime 


keyboard = Controller()

def display_video():
     # Assigning our static_back to None 
    static_back = None
    
    
    
    # Capturing video 
    video = cv2.VideoCapture(0) 

    import numpy as np

    # Infinite while loop to treat stack of image as video q
    while True: 
        # Reading frame(image) from video 
        check, frame = video.read() 
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lowerb = np.array([100,120,100])
        upperb = np.array([200,255,255])
        # Initializing motion = 0(no motion) 
        
        mask = cv2.inRange(hsv,lowerb,upperb)

        res = cv2.bitwise_and(frame,frame,mask=mask)
        # Converting color image to gray_scale image 
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY) 
    
        # Converting gray scale image to GaussianBlur  
        # so that change can be find easily 
        gray = cv2.GaussianBlur(gray, (21, 21), 0) 
    
        # In first iteration we assign the value  
        # of static_back to our first frame 
        if static_back is None: 
            static_back = gray 
            continue
    
        # Difference between static background  
        # and current frame(which is GaussianBlur) 
        diff_frame = cv2.absdiff(static_back, gray) 
    
        # If change in between static background and 
        # current frame is greater than 30 it will show white color(255) 
        thresh_frame = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1] 
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 
    
        # Finding contour of moving object 
        cnts,_ = cv2.findContours(thresh_frame.copy(),  
                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        
        positions = []
        cv2.rectangle(frame, (200, 150),(450, 330), (255, 0, 0), 3) # home position
        cv2.rectangle(frame, (0, 150), (100, 330), (255, 0, 0), 3)
        cv2.rectangle(frame, (550, 150), (650, 330), (255, 0, 0), 3)
        cv2.rectangle(frame, (200, 0),(450, 100), (255, 0, 0), 3)
        cv2.rectangle(frame, (200, 380),(450, 480), (255, 0, 0), 3)

        for contour in cnts: 
            if cv2.contourArea(contour) < 100: 
                continue
    
            (x, y, w, h) = cv2.boundingRect(contour) 
            # making green rectangle arround the moving object 
            cv2.rectangle(frame, (x, y), (x + 75, y + 75), (255, 255, 255), 3) 
    
            M = cv2.moments(contour)

                # calculate x,y coordinate of center

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            positions.append(cX)
            positions.append(cY)

            # put text and highlight the center
            cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
            
        # Displaying the black and white image in which if 
        # intensity difference greater than 30 it will appear white 
        cv2.imshow("Threshold Frame", thresh_frame) 
    
        # Displaying color frame with contour of motion of object 
        cv2.imshow("Color Frame", frame) 

        key = cv2.waitKey(1) 
        # if q entered whole process will stop 
        if key == ord('q'): 
            # if something is movingthen it append the end time of movement 
            break
        
    video.release() 
    
    # Destroying all the windows 
    cv2.destroyAllWindows() 


def game_loop(): 
    # Assigning our static_back to None 
    static_back = None
    
    
    
    # Capturing video 
    video = cv2.VideoCapture(0) 

    import numpy as np
    move_start = timeit.default_timer()

    # Infinite while loop to treat stack of image as video q
    while True: 
        # Reading frame(image) from video 
        check, frame = video.read() 
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lowerb = np.array([100,100,100])
        upperb = np.array([255,255,255])
        # Initializing motion = 0(no motion) 
        
        mask = cv2.inRange(hsv,lowerb,upperb)

        res = cv2.bitwise_and(frame,frame,mask=mask)
        # Converting color image to gray_scale image 
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY) 
    
        # Converting gray scale image to GaussianBlur  
        # so that change can be find easily 
        gray = cv2.GaussianBlur(gray, (21, 21), 0) 
    
        # In first iteration we assign the value  
        # of static_back to our first frame 
        if static_back is None: 
            static_back = gray 
            continue
    
        # Difference between static background  
        # and current frame(which is GaussianBlur) 
        diff_frame = cv2.absdiff(static_back, gray) 
    
        # If change in between static background and 
        # current frame is greater than 30 it will show white color(255) 
        thresh_frame = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1] 
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 
    
        # Finding contour of moving object 
        cnts,_ = cv2.findContours(thresh_frame.copy(),  
                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        
        positions = []
        cv2.rectangle(frame, (200, 150),(450, 330), (255, 0, 0), 3) # home position
        cv2.rectangle(frame, (0, 150), (100, 330), (255, 0, 0), 3)
        cv2.rectangle(frame, (550, 150), (650, 330), (255, 0, 0), 3)
        cv2.rectangle(frame, (200, 0),(450, 100), (255, 0, 0), 3)
        cv2.rectangle(frame, (200, 380),(450, 480), (255, 0, 0), 3)

        for contour in cnts: 
            if cv2.contourArea(contour) < 1000: 
                continue
    
            (x, y, w, h) = cv2.boundingRect(contour) 
            # making green rectangle arround the moving object 
            cv2.rectangle(frame, (x, y), (x + 75, y + 75), (255, 255, 255), 3) 
    
            M = cv2.moments(contour)

                # calculate x,y coordinate of center

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            positions.append(cX)
            positions.append(cY)

            # put text and highlight the center
            cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
            
        # Displaying the black and white image in which if 
        # # intensity difference greater than 30 it will appear white 
        cv2.imshow("Threshold Frame", thresh_frame) 
    
        # # Displaying color frame with contour of motion of object 
        cv2.imshow("Color Frame", frame) 
        
        ################GAME LOGIC################################################
        # Logic to hit keypresses:
        # x bound is 200:450
        # y bound is 150:350

        movelist = []
        if len(positions)>=4:
            # cube rotations
            if positions[0] < 100 and positions[2] < 100:
                # print('y')
                movelist.append('y\'')
            elif positions[0] > 400 and positions[2] > 400:
                # print('y\'')
                movelist.append('y')
            elif positions[1] <100 and positions[3] < 100:
                # print('x')
                movelist.append('x\'')
            elif positions[1] > 350 and positions[3] > 350:
                # print('x\'')
                movelist.append('x')

            # Turns (U, U', R, R', L, L')

            elif (positions[0]<300 and positions[1] < 100 and positions[2] in range(200,450)) or (positions[2]<300 and positions[3] < 100 and positions[0] in range(200,450)):
                # print('R')
                movelist.append('R')
            elif (positions[0]>300 and positions[1] < 100 and positions[2] in range(200, 450)) or (positions[2]>300 and positions[3] < 100 and positions[0] in range(200, 450)):
                # print('L\'')
                movelist.append('L\'')
            elif (positions[0]<300 and positions[1] > 380 and positions[2] in range(200,450)) or (positions[2]< 300 and positions[3] > 380 and positions[0] in range(200, 450)):
                # print('R\'')
                movelist.append('R\'')
            elif (positions[0]>300 and positions[1] > 380 and positions[2] in range(200,450)) or (positions[2]> 300 and positions[3] > 380 and positions[0] in range(200, 450)):
                # print('L')
                movelist.append('L')
            elif (positions[0] < 100 and positions[1] in range(150, 330) and positions[2] in range(200, 450)) or \
                (positions[2] < 100 and positions[3] in range(150,330) and positions[0] in range(200, 450)):
                # print('U')
                movelist.append('U\'')
            elif (positions[0] > 500 and positions[1] in range(150,330) and positions[2] in range (200, 450)) or \
                (positions[2] > 500 and positions[3] in range(150,330) and positions[0] in range(200, 450)):
                # print('U\'')
                movelist.append('U')
        
        if len(movelist)>0:
            time_since_last_move = timeit.default_timer() - move_start


        try:
            if time_since_last_move >= 1:
                move = movelist[0]
                make_move(move)
                move_start = timeit.default_timer()
        except:
            print('No Move Made')
            

        key = cv2.waitKey(1) 
        # if q entered whole process will stop 
        if key == ord('q'): 
            # if something is movingthen it append the end time of movement 
            break
    
    # video.release() 
    
    # # Destroying all the windows 
    # cv2.destroyAllWindows() 

def make_move(move):
    # Can create a hashmap with array instead and just call the appropriate keybind, but I'm lazy >.>
    if move=='y':
        keyboard.press(';')
    elif move == 'y\'':
        keyboard.press('a')
    elif move == 'x':
        keyboard.press('b')
    elif move == 'x\'':
        keyboard.press('y')
    elif move == 'U':
        keyboard.press('j')
    elif move == 'U\'':
        keyboard.press('f')
    elif move == 'L':
        keyboard.press('d')
    elif move == 'L\'':
        keyboard.press('e')
    elif move == 'R':
        keyboard.press('i')
    elif move == 'R\'':
        keyboard.press('k')

    print(move)
    

game_loop()
