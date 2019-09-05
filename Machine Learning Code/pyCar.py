# -*- coding: utf-8 -*-
from __future__ import print_function

import math
import time
import random
import sys, getopt
# import httplib, json
import http.client as httplib
import json

import requests as rq
import os

# http header
headers = { "charset" : "utf-8", "Content-Type": "application/json" }

def command_read(id):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "car_id" : id }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/RSIoT-2018/rsiot01/php/gesture_r.php", jdata, headers) # read from DB
    response = conn.getresponse()
    jdata_return = response.read().decode('utf-8')
    #print(jdata_return)
    pdata = json.loads(jdata_return)
    return pdata;

def command_write(id, gesture, time_stamp, x, y):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "car_id" : id,
              "gesture": gesture,
              "time_stamp" : time_stamp,
              "x" : x,
              "y" : y}
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/RSIoT-2018/rsiot01/php/gesture_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    pdata = json.loads(response.read().decode('utf-8'))
    return pdata;
    
