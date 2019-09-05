# -*- coding: utf-8 -*-
"""
Created on Tue Aug 01 11:53:12 2017

@author: Foredawn_Lin
"""

import gesCamera as ges
import objCamera as obj 
import robot





def downloadGes(id):
    gesInfo=ges.gesCam_read(id)
    return gesInfo

def downloadObj(id):
    objInfo=obj.objCam_read(id)
    return objInfo

def downloadRob(id):
    robInfo=robot.robot_read(id)
    return robInfo
    
def downloadAll(id1,id2,id3):
    return downloadGes(id1),downloadObj(id2),downloadRob(id3)    



if __name__ == "__main__":
#    downloadGes(0)
#    a=z.downloadGes(0)
#        
#    download.downloadGes(0)
#    downloadObj(0)
#    downloadRob(0)
    a=downloadAll(0,0,0)
