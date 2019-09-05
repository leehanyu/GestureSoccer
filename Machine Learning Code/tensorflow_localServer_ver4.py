# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 17:29:47 2017

@author: Foredawn_Lin
"""


import sys
# sys.path.insert(0, 'server')
import gestureClient as upload
import getPoint



import socket
import numpy as np
import tensorflow as tf 
import numpy.matlib as mat
from sklearn.decomposition import PCA 

import robot
import time
import pyCar


# upload carID, command, time, and x, y       
def uploadGesture(id, command, x, y):
    ret=pyCar.command_write(id, command, 1, x, y)
#    print (ret) 



 
def dataPlot2D(data,figNum,subplot=False,row=1,coln=2,order=1,c='k'):
    ### input:data: features in row
    ### row: rows created in subplot
    ### coln: colns created in subplot
    ### order: place where the figure is put in subplot
    fig=plt.figure(figNum)
    if subplot==False:
        ax=fig.add_subplot(111)
        plt.scatter(data[:,0],data[:,1],c=c)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        return fig,ax 
    else: 
        ax=fig.add_subplot(row,coln,order)
        ax.scatter(data[:,0],data[:,1],c=c)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        return fig,ax 



def dataPlot3D(self,data,figNum,subplot=False,row=1,coln=2,order=1,c='k'):
    fig=plt.figure(figNum)
    if subplot==False:
        ax=fig.add_subplot(111,projection='3d')
        ax.scatter(data[:,0],data[:,1],data[:,2],c=c)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        return fig,ax 
    else: 
        ax=fig.add_subplot(row,coln,order,projection='3d')
        ax.scatter(data[:,0],data[:,1],data[:,2],c=c)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        return fig,ax 




def splitData(data,numOfComp):
    ### data: data to split 
    ### numOfComp: number of compostion
    return [data[i:i + numOfComp] for i in range(0, len(data), numOfComp)]





# restore graph and model
saver = tf.train.import_meta_graph("./model/563/model.ckpt.meta")

# restore the model
sess = tf.Session()

saver.restore(sess, "./model/563/model.ckpt")
graph = tf.get_default_graph()
# print(sess.run(tf.get_default_graph().get_tensor_by_name("add:0")))

# obtain needed placehoulde in the graph
input_x = graph.get_operation_by_name('nn/input').outputs[0]
test_groundtruth = graph.get_operation_by_name('nn/groundtruth').outputs[0]
# print(input_x)

# oabtain needed tensor 
test_output = graph.get_tensor_by_name('nn/prediction:0')
test_acc = graph.get_tensor_by_name('accuracy/acc:0')



######### gesture server ##########
ges_client=upload.gestureClient()
####### gesture server ends########3




global state              #### 0 as not doing prediction 
HOST = '127.0.0.1'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print ('Listening')
s.listen(1)
conn, addr = s.accept()
turnOnLeap=1; ####### 1 as turn on leap motion 
print ('Connected by ', addr)


# hand_dir=[0,0,0] ### initialize hand direction as global variable 

# for pointing only :
x = 0
y = 0
### list of command associate with gesture type
# !!!!!!!!!!! change the following line if using different car !!!!!!!!!!!!!
carID = 24
command_dict = {0: 'stop', 1: 'forward', 2: 'backward', 3: 'left', 4: 'right', 5: 'forward & left',
                6: 'forward & right', 7: 'pointing', 8: 'turn left a little', 9: 'turn right a little', 10: 'kick'}

while 1:    
    data = conn.recv(5120)
    data = data.decode('utf8')
    state = int(data[0])
    
#    if len(data) > 10:     ##################################################################
    
    if (state == 0):
        command = 0
        uploadGesture(carID, command, x, y);

#        print('no data')
        continue
    
        ######### static gesture ##########        
    data = [float(s) for s in data.split(' ')]
    y_pred_R=-1 ###33 initilize y_prediction of right hand
    data_R=np.array([data[1:31]]) ######################################################################
    pointing_data = data[31:46]
    substract=mat.repmat(data_R[:,0:3],1,int(data_R.shape[1]/3))
    data_R=data_R-substract
    R_new=data_R
#        print('Rnew:', R_new)
    y_pred_R = test_output.eval(session = sess, feed_dict={input_x: R_new})
    # result=outputs.eval(session=sess,feed_dict={X:R_new})
    
    ############### get command ##########  

    # stop              
    if y_pred_R==0:
        command=0 
    # keep forward
    elif y_pred_R==1:
        command=1
    # keep backward
    elif y_pred_R==2:
        command=2
    # keep turning left
    elif y_pred_R==3:
        command=3
    # keep turning right
    elif y_pred_R==4:
        command=4
    # left and forward at 45 degree
    elif y_pred_R==5:
        command=5
    # right and forward at 45 degree
    elif y_pred_R==6:
        command=6
 

    # pointing
    elif y_pred_R==7:
        command=7
        print('it is pointing')
        tip = pointing_data[0:3]
        n1 = pointing_data[3:6]
        n2 = pointing_data[6:9]
        n3 = pointing_data[9:12]
        w = pointing_data[12:15]
        print(tip, n1, n2, n3, w)
        x, y = getPoint.getPoint(tip, n1, n2, n3, w)
        
    # turn left a little
    elif y_pred_R==8:
        command=8
    # turn right a little
    elif y_pred_R==9:
        command=9
    # kick the ball
    elif y_pred_R==10:
        command=10
    else:
        print('no command')
        continue
    

    # gesClientState=1 ### keep running gesture client
      

    # ges_client.runClient(0,0,0,str(command),[0,0,0],gesClientState) ##### id1,id2,id3,"static Data","hand direction=0","gesClient Upload or not state"        

    # upload command to the server here
    # upload carID, command, time, and x, y
    print(command_dict[command])
    uploadGesture(carID, command, x, y);
    x =0
    y =0
    time.sleep(1)
                 
    ######### static ends #############
    state=1; ####### turn off prediction 
    conn.sendall(b'1')  ###### turn off leap motion 
       
            
#    else :  ###########################################3
#        print('No data')
#        # stop the car when no data is received
#        uploadGesture(carID, 0, x, y);
##        time.sleep(1)
##        continue
#    
#    if not data:
#        print('Not data #####################')
#        continue
    
conn.close()