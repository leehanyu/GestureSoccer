# -*- coding: utf-8 -*-

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

def robot_read(id):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "id" : id }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/RSIoT-2018/rsiot01/php/car_w.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read().decode('utf-8'))
    return pdata;


# upload carID, command, time, and x, y       
def robot_write(id, command, x, y):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    pdata = { "car_id" : id,
              "command": command,
              "time" : timestamp,
              "x" : x,
              "y" : y}
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/RSIoT-2018/rsiot01/php/car_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read().decode('utf-8'))
    return pdata;
    
