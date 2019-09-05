# -*- coding: utf-8 -*-
"""
Created on Sun Oct 08 17:58:23 2017

@author: hzhan
"""

import os, inspect, sys, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import cv2
import ctypes
import numpy
import re

# Change this when taking sample each time
sampleNumber = 0;

# Change this when changing gesture
# Name: stop, keep forward, keep backward, keep left, keep right, forward and left45, forward and right45,   pointing
# Lable:  0          1             2            3           4              5                   6                7  
# Name: pointup ccw,  pointdown cw, kick
# Lable:    8               9        10
tag = '10'
person = '13'


data_list = []
data_list_print = []
startTimeSet = False
start_time = 0
sampleIndex = 0
data_number = 0

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

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
        global startTimeSet
        global start_time
        global data_list
        global data_list_print
        global sampleIndex
        global data_number
        
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        
        # Set up timer to track for gesture time
        if not startTimeSet:
            start_time = frame.timestamp
            startTimeSet = True
        
        frame_time_ms = (frame.timestamp - start_time) // 1000
        hand_joint_list = []
        
        print(frame_time_ms)
        if frame_time_ms > 5000 & frame_time_ms % 100 == 0:       # Start to collect data after 5 seconds for right hand pose
            if (len(frame.hands) == 1):
                # Get hands
                # Collect position data for fingers
                sampleIndex += 1
                for hand in frame.hands:
                    for finger in hand.fingers:
                        for i in [0,3]:  # only collectfinger tip and bottom
                            bone = finger.bone(i)
                            bone_data_print = "bone tip position: %s, sampleIndex: %s" %(bone.next_joint, tag)
                            bone_data = "%s" %(bone.next_joint)
                            print("appended")
                            data_list_print.append(bone_data_print)
                            hand_joint_list.append(bone_data)
                    hand_joint_list.append("%s" %tag)
                    data_list.append(hand_joint_list)
                    data_number += 1
                        
        if not frame.hands.is_empty:
            print ""


    def on_images(self, controller):
    #   get image from Leap Motion
        print "Images available"
        images = controller.images
        image = images[0]
        
        image_buffer_ptr = image.data_pointer
        ctype_array_def = ctypes.c_ubyte * image.width * image.height

        # as ctypes array
        as_ctype_array = ctype_array_def.from_address(int(image_buffer_ptr))
        # as numpy array
        numpy_array = numpy.ctypeslib.as_array(as_ctype_array)

        cv2.imshow("left_image", numpy_array)
        cv2.waitKey(delay = 10)



def save_data():
    global data_list
    global sampleNumber
    global tag
    
    group_string = ""
    file_name = "./static_data/data_%s_%s.txt" %(tag, person)
    if os.path.isfile(file_name):
        os.remove(file_name)
    data_file = open(file_name, "a")
    
    for joint_group in range(0, len(data_list)):
        joint_list = data_list[joint_group]
        for pos in range(0, len(joint_list)):
            joint_list[pos] = joint_list[pos].replace("(", "")
            joint_list[pos] = joint_list[pos].replace(")", "")
            joint_list[pos] = joint_list[pos].replace(",", "")
            group_string = group_string + joint_list[pos] + " "
        group_string = group_string + "\n"
        data_file.write(group_string)
        group_string = ""
    data_file.close()
        
        
 
            
def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    
    # Allow user to veiw raw data and put into head mounted mode
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)


    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    
    global data_list
    global data_number

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
        
        
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)
        
        # Print to the console
        for index in range(0, len(data_list_print)):
            print data_list_print[index]
        print data_number
        
        # Save as txt file in right format
        save_data()


if __name__ == "__main__":
    main()