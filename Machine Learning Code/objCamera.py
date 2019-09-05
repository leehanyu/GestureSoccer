# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:48:43 2017

@author: Foredawn_Lin
"""

from __future__ import print_function

import math
import time
import random
import sys, getopt
#import httplib, json
import http.client as httplib
import json

import requests as rq
import os

# http header
headers = { "charset" : "utf-8", "Content-Type": "application/json" }

def objCam_read(id):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "id" : id }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/cerlab/php/objCamera_r.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read().decode('utf-8'))
    return pdata;

def objCam_write(id, objPos, binPos,status):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "id" : id,
              "objPos" : objPos,
              "binPos" : binPos,
              "status":status}
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/cerlab/php/objCamera_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read().decode('utf-8'))
    return pdata;
    
