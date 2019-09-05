# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 21:29:47 2017

@author: hzhan
"""

import os, inspect, sys, threading
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import socket
import time


request_state = 1
send_state = 0          # 1 Data send
# pointing_state = 0      # 0 : command is not pointing, 1 : command is pointing
static_data = []
pointing_data = []


# Data formulation:
# first digit: tensorflow state: 1->start; 0->end
# the rest data: x y z coordinates 

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        global request_state
        # global new_data_type
        global static_data       # Should only be a array of length 10 or 20
        # global dynamic_data    # Should be the array of positions of index finger tip
        global pointing_data     # only use these for pointing
#        print('on frame:', request_state)
        
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        hands_list = frame.hands
        #print "request_state", request_state
#        request_state = 1
        if frame.hands.is_empty:
            stateLock.acquire()
            request_state = 1
            stateLock.release()
#            send_handler()
            print('Waiting for command (No hand)')
            time.sleep(1)
            
        else:
            if request_state != 0:
#                print('reading...')
                if len(hands_list) == 1:
#                    print('1')
                    for hand in frame.hands:
#                        print('2')
#                        if hand.is_right:
#                            print('3')
                        for finger in hand.fingers:
#                            print('4')
                        #######################################################
                            if finger.type == 1 :
                                for i in range(4) :
                                    bone = finger.bone(i)
                                    joint_vector = bone.next_joint
                                    dataLock.acquire()
#                                    print('pointing')
                                    pointing_data.append(round(joint_vector.x, 2))
                                    pointing_data.append(round(joint_vector.y, 2))
                                    pointing_data.append(round(joint_vector.z, 2))
                                    dataLock.release()
                        #######################################################
                            for i in [0,3]:
                                bone = finger.bone(i)
                                joint_vector = bone.next_joint
                                # Add the data to the static data list
                                dataLock.acquire()
#                                print('static')
                                static_data.append(round(joint_vector.x,2))
                                static_data.append(round(joint_vector.y,2))
                                static_data.append(round(joint_vector.z,2))
                                dataLock.release()
                        #######################################################
                        wristPos = hand.arm.wrist_position
                        dataLock.acquire()
#                        print('wrist')
                        pointing_data.append(round(wristPos.x, 2))
                        pointing_data.append(round(wristPos.y, 2))
                        pointing_data.append(round(wristPos.z, 2))
                        dataLock.release()
                        #######################################################
    
                                
                    # set state variable and lock
                    stateLock.acquire()
#                    print('state lock')
    #                # new_data_type = 2  # Make new data ready
                    request_state = 0   # Make request state to false
                    send_handler()
                    # release lock
                    stateLock.release()
                    
                else:
                    stateLock.acquire()
                    request_state = 1
                    stateLock.release()
                    send_handler()
                    print('Using one hand')
                    time.sleep(1)
             
                
                        
        
 
    
            
def leap_node():
    
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    
    # Allow user to veiw raw data and put into head mounted mode
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)


    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    while 1:
        pass
    


def request_handler():
    global request_state
    while 1:
        #print "request"
#        print('request handler')

        request_state = sock.recv(3072)
        print('recieved')
        #print 'recieved request', request_state
        stateLock.acquire()

#        request_state = request_state.decode('utf8')
#        print('handler:', request_state)
        stateLock.release()
        

def send_handler():
    global static_data
    global pointing_data
    dataLock.acquire()
    static_data_string = str(static_data)
    static_data_string = static_data_string.replace('[', '')
    static_data_string = static_data_string.replace(']', '')
    static_data_string = static_data_string.replace(',', '')
    
    pointing_data_string = str(pointing_data)
    pointing_data_string = pointing_data_string.replace('[', '')
    pointing_data_string = pointing_data_string.replace(']', '')
    pointing_data_string = pointing_data_string.replace(',', '')
    # static_data_string = '1' + ' ' + static_data_string
    if len(static_data_string) > 10:
        static_data_string = '1' + ' ' + static_data_string + ' '+ pointing_data_string
        sock.sendall(static_data_string)  # send static data
        # reset all data
        static_data = []
        pointing_data = []
        dataLock.release()
    else:
        static_data_string = '0' + ' ' + static_data_string + ' ' + pointing_data_string
        sock.sendall(static_data_string)  # send static data
#        sock.sendall(pointing_data_string)
        # reset all data
        static_data = []
        pointing_data = []
        dataLock.release()
        


class leapThread(threading.Thread):
    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
    
    def run(self):
        # Run leap node when thread start
        print('leap node running')
        leap_node()
        
class requestThread(threading.Thread):
    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
    
    def run(self):
        # Run request handler
        print('request handler running')
        request_handler()


#### Set up client to listen to server data requist
Host = '127.0.0.1'
Port = 50007
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((Host, Port))

dataLock = threading.Lock()
stateLock = threading.Lock()


threads = []

# Create threads
leap_thread = leapThread(1, 'leap_thread')
request_thread = requestThread(2, 'request_thread')


# Start the threads
leap_thread.start()
request_thread.start()

threads.append(leap_thread)
threads.append(request_thread)


for t in threads:
    t.join()
    

sock.close()


        

