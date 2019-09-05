# -*- coding: utf-8 -*-

import pyCar
import time

def uploadGesture(id, gesture, time_stamp, x, y):
    ret = pyCar.command_write(id, gesture, time_stamp, x, y)
    print (ret) 

if __name__ == '__main__':
    '''
    uploadGesture(12, 2, 1, 1.2, 2.4)
    for i in range(1, 100):
        uploadGesture(12, 2, i, 1.2+i, 2.4+i)

    for i in range(100, 200):
        uploadGesture(12, 4, i, 1.2+i, 2.4+i)
    
    for i in range(200, 300):
        uploadGesture(12, 2, i, 1.2+i, 2.4+i)
    '''    
