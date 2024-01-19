import cv2
import numpy as np
import math
import serial
from collections import deque
import time


# Define queues and filter windows

kernel = np.ones((5, 5), np.uint8) 
kernel2 = np.ones((3, 3), np.uint8) 
pts = deque(maxlen=1000000)
pts2 = deque(maxlen=1000000)
pts3 = deque(maxlen=1000000)

#Setting fonts
font = cv2.FONT_HERSHEY_SIMPLEX                                                

# **********************************************************************************************************
# Define a correction function that corrects the mouse coordinates inwards when the mouse is on the edge
# A circle close to the radius is defined with the centre of the arena as the origin, so that the robot predator moves as far as the boundary of that circle to prevent hitting the edge of the arena.
def line_intersect_circle(p, lsp, esp):
    # p is the circle parameter, lsp and lep is the two end of the line
    x0, y0, r0 = p
    x1, y1 = lsp
    x2, y2 = esp
    if r0 == 0:
        return [[x1, y1]]
    if x1 == x2:
        if abs(r0) >= abs(x1 - x0):
            p1 = x1, round(y0 - math.sqrt(r0 ** 2 - (x1 - x0) ** 2), 5)
            p2 = x1, round(y0 + math.sqrt(r0 ** 2 - (x1 - x0) ** 2), 5)
            inp = [p1, p2]
            # select the points lie on the line segment
            inp = [p for p in inp if p[0] >= min(x1, x2) and p[0] <= max(x1, x2)]
        else:
            inp = []
    else:
        k = (y1 - y2) / (x1 - x2)
        b0 = y1 - k * x1
        a = k ** 2 + 1
        b = 2 * k * (b0 - y0) - 2 * x0
        c = (b0 - y0) ** 2 + x0 ** 2 - r0 ** 2
        delta = b ** 2 - 4 * a * c
        if delta >= 0:
            p1x = round((-b - math.sqrt(delta)) / (2 * a), 5)
            p2x = round((-b + math.sqrt(delta)) / (2 * a), 5)
            p1y = round(k * p1x + b0, 5)
            p2y = round(k * p2x + b0, 5)
            inp = [[p1x, p1y], [p2x, p2y]]
            # select the points lie on the line segment
            inp = [p for p in inp if p[0] >= min(x1, x2) and p[0] <= max(x1, x2)]
        else:
            inp = []
    # Calculate the intersection of a circle and a line segment
    return inp if inp != [] else [x1, y1]                                       


# ***************************************************************************************************************
# Draw the outline of an object
def Decision(frame, flag):
    # BRG converted to HSV
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                            
    # Lower blue threshold 
    lower_blue = np.array([50,120,160])     
    # Upper blue threshold                                      
    higher_blue = np.array([180,200,255])                                      
    # Getting the blue part of the mask
    mask_blue = cv2.inRange(img_hsv, lower_blue, higher_blue)  
    # Median Filter
    mask_blue = cv2.medianBlur(mask_blue, 9)                      
    # outline detectio
    contourslan, hierarchy = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  
    # Draw a outline 
    #cv2.drawContours(frame, contourslan, -1, (0, 0, 255), 1)                                       
    
#*************************************************************    
    # Detection of mice
    lower_black = np.array([40, 10, 10])                       
    higher_black = np.array([130, 110, 50])                   
    
    mask_black = cv2.inRange(img_hsv, lower_black, higher_black)   
    mask_black = cv2.medianBlur(mask_black, 19)                      
    
    contourshei, hierarchy = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  
    #cv2.drawContours(frame, contourshei, -1, (0, 255, 0), 1)                                         
    
    
#*************************************************************     
# Draw a trajectory
    
    for d in contourslan:
        # Calculate the perimeter of the blue object's outline
        zhouchang1 = cv2.arcLength(d,True)                              
        # Find smallest rectangle, return coordinates of upper left corner, width and height of rectangle
        if zhouchang1 > 0:          
            p,q,m,n = cv2.boundingRect(d)                              
            #cv2.putText(frame, 'dangerous',(p, q - 5), font, 0.4, (0, 0, 255), 1) # Show character names
            global centerlan
            # Coordinates of the center point of the blue object rectangle
            centerlan=(int(p+m/2),int(q+n/2))    
            #备注 note                      
            cv2.putText(frame, str(centerlan[0]), (500, 450), font, 0.6, (0, 0, 255), 2)    
            # Save the x-coordinate of the robotic predator
            fp = open("H:/data/lanx61-227-2.text", "a")                
            print(centerlan[0], file=fp)
            fp.close()
            cv2.putText(frame, str(centerlan[1]), (550, 450), font, 0.6, (0, 0, 255), 2) 
            # Save the y-coordinate of the robotic predator
            fp2 = open("H:/data/lany61-227-2.text", "a")               
            print(centerlan[1], file=fp2)
            fp2.close()
            print ("The coordinates of the center point of the blue object are：",centerlan)  
            # Draw a trajectory of robotic predator
            if flag == 1:                                       
                pts2.appendleft(centerlan)
                for i in range(1,len(pts2)):                           
                    if pts2[i-1]is None or pts2[i]is None:
                        continue                                       
                    #cv2.line(frame, pts2[i - 1], pts2[i], (0, 0, 255)) 
        else:
            centerlan=(0,0)
#*****************************************************************

    for b in contourshei:
        # Calculate the perimeter of the black mouse's outline
        zhouchang2 = cv2.arcLength(b,True)     
        # Find smallest rectangle, return coordinates of upper left corner, width and height of rectangle                         
        if zhouchang2 > 0:          
            z,t,y,h = cv2.boundingRect(b)                             
            #cv2.putText(frame, 'mouse',(z, t - 5), font, 0.4, (0, 0, 0), 1) # Show character names
            global centerhei
            # Coordinates of the center point of the black mouse rectangle
            centerhei=(int(z+y/2),int(t+h/2))                         
            cv2.putText(frame, str(centerhei[0]), (500, 430), font, 0.6, (0, 255, 0), 2)    # note
            # Save the x-coordinate of the mouse
            fp = open("H:/data/heix61-227-2.text", "a")               
            print(centerhei[0], file=fp)
            fp.close()
            cv2.putText(frame, str(centerhei[1]), (550, 430), font, 0.6, (0,255, 0), 2)    #note
            # Save the y-coordinate of the mouse
            fp = open("H:/data/heiy61.text", "a")                     
            print(centerhei[1], file=fp)
            fp.close()
            print ("The coordinates of the mouse center point are：",centerhei)   
            # Draw a trajectory of mouse
            if flag == 1:                                       
                pts3.appendleft(centerhei)
                for i in range(1,len(pts3)):                           
                    if pts3[i-1]is None or pts3[i]is None:
                        continue                                       
                    #cv2.line(frame, pts3[i - 1], pts3[i], (0, 255, 0)) 
        else:
            centerhei=(0,0)

#******************************************************************** 
# Mice velocity calculations   
         
        pts.appendleft(centerhei)
        if len(pts)>=2:
            if pts[1] is None:
                continue
            # Pixel distance moved with the mouse along the x-axis
            xpix=pts[0][0]-pts[1][0]    
            # Pixel distance moved with the mouse along the y-axis
            ypix=pts[0][1]-pts[1][1]         
            a=math.pow(xpix, 2)
            b=math.pow(ypix, 2)
            c=a+b
            # Pixel-by-pixel distance of mouse movement
            s=math.sqrt(c)                    
            # pix/s/(pix/cm)=cm/s  i.e. the velocity of mouse movement
            vel=s/0.033/5.35                   
            v=round(vel,2)
            print ("The velocity of the mice is：",v) 
            cv2.putText(frame, str(v), (520,410), font, 0.6, (0, 0, 0), 2)
            #  Save the velocity of mice
            fp = open("H:/data/velocity61-227-2.text", "a")  
            print(v, file=fp)
            fp.close()
        
           
#**********************************************************************
# Distance determination
    
    x=centerhei[0]-centerlan[0]
    y=centerhei[1]-centerlan[1]
    xx=math.pow(x, 2)
    yy=math.pow(y, 2)
    # Distance between mice and threats
    bxdistance=math.sqrt(xx+yy)                                 
    distance=round(bxdistance,2) 
    #  Calculate the actual distance in cm according to the scale of reality                               
    realdis=distance/5.35                                       
    reald=round(realdis,2)                                     
    cv2.putText(frame, str(reald), (520,470), font, 0.6, (255, 0, 0), 2)
    # Preservation of relative distance
    fp3 = open("H:/data/distance61-227-2.text", "a")            
    print(reald, file=fp3)
    fp3.close()
    print("The distance between the mouse and the threat is：",reald)
        
            
    mx=centerhei[0]
    my=centerhei[1]
    borderx=centerlan[0]
    bordery=centerlan[1]
    # size = frame.shape
    # print("The video frame size is：",size)
    #cv2.imshow('mouse', mask_black)
    #cv2.imshow('threat', mask_blue) 
    cv2.imshow('result', frame)
    # Returns the coordinates and relative distances of the mouse and robotic predator
    return distance, borderx, bordery, mx, my
#***************************************************************************

# ==============================================================================================
#   **************************** Main Function Entry***********************************
# ==============================================================================================
#  Setting Serial Port Parameters
ser = serial.Serial()
#  Setting the bit rate to 115200bps
ser.baudrate = 115200   
#  By default, the microcontroller's serial port is connected to the "COM3" port 
ser.port = 'COM3' 
#  Open the serial port       
ser.open()               
 
# First send an initial direction and velocity of 0 to make the robot predator stationary
data = 'A'+str('0')+'B'+str('0')+'C'+str('0')+'D'+str('0')+'\r\n'
ser.write(data.encode())

# Capture video via local camera
cap = cv2.VideoCapture(0)

flag = 0  
#  Loop to get frame
while(cap.isOpened()):
    
    ret, frame = cap.read()
    #  Record start time
    time_start = time.time()     
    dist,borx,bory,micexx,miceyy=Decision(frame, flag)
    #   Record stop time
    time_end = time.time()   
    # The calculated time difference is the execution time of the program in seconds/sec
    time_sum = time_end - time_start  
    print(time_sum)
    print('jl',dist)
    print('x',borx)
    print('y',bory)
    # print('xx',micex)
    # print('yy',micey)
    
    # Set the threat velocity in cm/s
    speed_fin=35
    # Correction of mouse coordinates(border)
    hh=math.pow(micexx-330, 2)
    tt=math.pow(miceyy-230, 2)   
    if hh+tt >= 41209:
        center=line_intersect_circle((330,230,203),(330,230),(micexx,miceyy))
        print(center)

        micex=round(center[0][0],2)
        micey=round(center[0][1],2)
    else:
        micex=micexx
        micey=miceyy
        
    # Calculate the speed required horizontally and vertically, i.e., decompose the sum velocity.
    Ayy=micey-bory
    Axx=micex-borx
    
    if Axx == 0:
        Ax=0.0000000001
    else:
        Ax=Axx
        
    if Ayy == 0:
        Ay=0.0000000001
    else:
        Ay=Ayy
    
    T=abs(Ay/Ax)   
    # Velocity magnitude in the x-axis direction                                       
    speed_dangerous=math.pow(speed_fin, 2)                
    speed_T=math.pow(T, 2)           
    # Velocity magnitude in the y-axis direction                                          
    Vx=math.sqrt(speed_dangerous/(speed_T+1))             
    Vy=T*Vx                                                
   
    #  Converts the speed to the pulse frequency required by the servomotor
    rpm_xx=round(72000000/Vx/10/16000*7.5)
    rpm_yy=round(72000000/Vy/10/16000*7.5)
    if rpm_xx >= 1000:
        rpm_x=999
    else:
        rpm_x=rpm_xx
    
    if rpm_yy >= 1000:
        rpm_y=999
    else:
        rpm_y=rpm_yy
    


    # If the location of the mice is not within the safe area, the threat is initiated 
    # X vertical velocity; 
    # y vertical orientation
    # P lateral velocity
    # Q lateral orientation
    # The threat has caught up with the mouse and is no longer moving horizontally or vertically, stopping the chase
    if dist < 40 :
        print('The mice have been caught up！！！')
        X=0
        Y=0
        P=0
        Q=0                                    
        print('X =',X)
        print('Y =',Y)
        print('P =',P)
        print('Q =',Q)           
        #  Packages the centroid coordinates according to the protocol and sends them to the serial port      
        data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
        ser.write(data.encode())
    else: 
        flag = 1                               
        print('Attention!')  
       
        # first quadrant (of the coordinate plane, where both x and y are positive)
        if micex>borx and micey<bory:                            
            print('The threat to start a chase in the first quadrant')
            X=rpm_y
            Y=1
            P=rpm_x
            Q=0
            print('X =',X)
            print('Y =',Y)
            print('P =',P)
            print('Q =',Q)
            data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
            ser.write(data.encode())
        # second quadrant (of the coordinate plane, where both x and y are positive) 
        elif micex<borx and micey<bory:                          
            print('The threat to start a chase in the second quadrant')
            X=rpm_y
            Y=1
            P=rpm_x
            Q=1
            print('X =',X)
            print('Y =',Y)
            print('P =',P)
            print('Q =',Q)
            data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
            ser.write(data.encode()) 
        # third quadrant (of the coordinate plane, where both x and y are positive)
        elif micex<borx and micey>bory:                          
           print('The threat to start a chase in the third quadrant')
           X=rpm_y
           Y=0
           P=rpm_x
           Q=1
           print('X =',X)
           print('Y =',Y)
           print('P =',P)
           print('Q =',Q)
           data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
           ser.write(data.encode())
        # fourth quadrant (of the coordinate plane, where both x and y are positive)
        elif micex>borx and micey>bory:                          
           print('The threat to start a chase in the fourth quadrant')
           X=rpm_y
           Y=0
           P=rpm_x
           Q=0
           print('X =',X)
           print('Y =',Y)
           print('P =',P)
           print('Q =',Q)
           data = 'A'+str(X)+'B'+str(Y)+'C'+str(P)+'D'+str(Q)+'\r\n'
           ser.write(data.encode())
      
    if cv2.waitKey(1) & 0xFF==27:
        break
#  Close the serial port
ser.close()                                     
cv2.destroyAllWindows()
cap.release()

