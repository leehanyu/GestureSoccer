# -*- coding: utf-8 -*-

import robot
import IoRTcarLTest as iortl
import time
import math
#import serial

#data = serial.Serial('/dev/ttyACM0', 9300)

def downloadGesture(id):
    gesInfo=robot.command_read(id)
    return gesInfo
'''
def pointing(obj,data):
    x = obj['x']
    y = obj['y']

    datas = data.split(' ')
    x1 = datas(0)
    y1 = datas(1)
    r = datas(2)

    dx = x1-x
    dy = y1-y

    r1 = math.atan2(dy/dx)

    theta = r-r1
    
    if theta>0:
        iortl.cw(theta/100)
    else:
        iortl.ccw(theta/100)    
    
    dist = math.sqrt(dx**2+dy**2)

    iortl.forward(dist/100)
    
    return
'''



if __name__ == "__main__":
    timePre = '0'
    while 1:

        
        obj = downloadGesture(24)
        timeNew = obj['time']
        ges = int(obj['gesture'])
        if timeNew == timePre and ges != 1 and ges != 2:
            iortl.pause()
            continue
        
       
        print("command:{}".format(ges))
        timePre = timeNew
        if ges == 0: #stop
            iortl.pause()
            time.sleep(0.01)
        elif ges == 1:#forward
            iortl.forward()
            time.sleep(0.01)
        elif ges == 2:#backward
            iortl.backward()
            time.sleep(0.01)
        elif ges == 3:#trun left
            iortl.ccw(0.86)
            time.sleep(0.87)
            #iortl.forward()
        elif ges == 4:#turn right
            iortl.cw(0.90)
            time.sleep(0.91)
            #iortl.forward()
        elif ges == 5:#turn left 45
            iortl.ccw(0.43)
            iortl.forward()
            time.sleep(0.44)
        elif ges == 6:#turn right 45
            iortl.cw(0.45)
            iortl.forward()
            time.sleep(0.46)
        elif ges == 7:
            #pointing(obj,data)
            iortl.pause()
            time.sleep(0.01)
        elif ges == 8:#turn left a little
            iortl.ccw(0.15)
            time.sleep(0.16)
            #iortl.forward()
        elif ges == 9:#turn right a little
            iortl.cw(0.15)
            time.sleep(0.16)
            #iortl.forward()
        elif ges == 10:#kick
            #iortl.pause()
            iortl.accelerate(0.20)
            #iortl.pause()
            #iortl.backward(0.10)
            iortl.pause()
            time.sleep(0.21)
        else:
            time.sleep(0.01)
            continue
