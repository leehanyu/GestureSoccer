# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 12:25:13 2017

@author: Foredawn_Lin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 01 14:30:57 2017

@author: Foredawn_Lin
"""

import upload_API as upload 
import download_API as download
import datetime 


class gestureClient():
    baseTime=datetime.datetime(2017,8,1,12,00,00,000)   ### setup self-reference time for robotClient 
    statusFilePath='C:/Users/Foredawn_Lin/Desktop/CMU/Gesture project/TongCode/newCode/CameraClient/Camera/stateInfo.txt'
    gestureFilePath='C:/Users/Foredawn_Lin/Desktop/CMU/Gesture project/TongCode/newCode/CameraClient/Camera/handInfo.txt'
    status=0                           
    def _init_(self,value):
        self.status=value
    
    def __clientInfo(self,id1,id2,id3):
        return download.downloadAll(id1,id2,id3)
    
    def __getTimeStamp(self,gesInfo,objInfo,robInfo):
        gesTime=datetime.datetime.strptime(str(gesInfo['pos_array'][0]['ts']), "%Y-%m-%d %H:%M:%S.%f")
        gesTimeDiff=(gesTime-self.baseTime).total_seconds()
        objTime=datetime.datetime.strptime(str(objInfo['pos_array'][0]['ts']), "%Y-%m-%d %H:%M:%S.%f")
        objTimeDiff=(objTime-self.baseTime).total_seconds()
        robTime=datetime.datetime.strptime(str(robInfo['pos_array'][0]['ts']), "%Y-%m-%d %H:%M:%S.%f")
        robTimeDiff=(robTime-self.baseTime).total_seconds()
        return gesTimeDiff,objTimeDiff,robTimeDiff
    
    def __getStatus(self,gesInfo,objInfo,robInfo):
        return int(gesInfo['pos_array'][0]['status']),int(objInfo['pos_array'][0]['status']),int(robInfo['pos_array'][0]['status'])
    
    def __readStatusTextInfo(self):        
        File=open(self.statusFilePath,'r')
        for lines in File:
            status=int(lines)
        File.close()
        return status
    
    def __readGestrueTextInfo(self):
        File=open(self.gestureFilePath,'r')
        ges_name=[]
        ges_pos=[]
        i=0    
        for lines in File:
            if i==0:
                ges_name=lines.rstrip('\n')
            elif i==1:
                ges_pos=lines.split(',')
                for j in range(len(ges_pos)):
                    ges_pos[j]=float(ges_pos[j])
            i=i+1
        File.close()    
        #######3 fix uploading pos [None] bug temporary solution##########
        if len(ges_name) ==0:
            ges_name="00"
        if len(ges_pos)==0:
            ges_pos=[0,0,0]
        return ges_name,ges_pos 
        
    def __uploadGesInfo(self,id1,gesName,gesPos):           
        upload.uploadGes(id1,gesPos,gesName,self.status)        
        
    def __writeStatusTextInfo(self):
        File5=open(self.statusFilePath,'w')
        string=str(self.status)
        File5.write(string)
        File5.close()
        
    def __changeStatus(self,value2):
        self.status=value2
    
    def reset(self,robID):
        self.changeStatus(0)
        self.uploadStatus(robID)
    
    def runClient(self,id1,id2,id3,gesName,gesPos,state):
        GesInfo,ObjInfo,RobInfo=self.__clientInfo(id1,id2,id3)
        gesTime,objTime,robTime=self.__getTimeStamp(GesInfo,ObjInfo,RobInfo)
        gesState,objState,robState=self.__getStatus(GesInfo,ObjInfo,RobInfo)
        #print (1)
        if gesState==0 and self.status==0:
            #print gesTime,robTime,objTime,gesState,objState
             if robTime>gesTime and robState==0: # and objTime>gesTime and objState==0:
                self.__changeStatus(1)
                #gesName,gesPos=self.__readGestrueTextInfo()
                self.__uploadGesInfo(id1,gesName,gesPos) 
                #self.__writeStatusTextInfo()            ####python fire gesture start signal 
        elif gesState==1 and self.status==1:
             #print ("im here")
             if robTime<gesTime and robState==0:
                #self.status=self.__readStatusTextInfo()   #### C++ fire rob stop signal 
                self.status=state
                #gesName,gesPos=self.__readGestrueTextInfo()
                self.__uploadGesInfo(id1,gesName,gesPos)
                if self.status==0:
                    self.__changeStatus(0)
                    #self.__uploadGesInfo(id1,gesName,gesPos)
                    #self.__writeStatusTextInfo()

#gestureCam=gestureClient()                  
#while 1:
#    gestureCam.runClient(0,0,0)