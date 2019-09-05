import serial
import time
import sys, tty, termios

ser = serial.Serial('/dev/ttyACM0', 9600)

def reset():
    ser.close()
    
def forward(tf=-1.0):
    ser.write('f')
    if tf > 0:
        time.sleep(tf)
        pause()

def accelerate(tf=-1.0):
    ser.write('a')
    if tf > 0:
        time.sleep(tf)
        pause()

def backward(tf=-1.0):
    ser.write('b')
    if tf > 0:
        time.sleep(tf)
        pause()

def left(tf=-1.0):
  ser.write('L')
  if tf > 0:
    time.sleep(tf)
    pause()

def right(tf=-1.0):
  ser.write('R')
  if tf > 0:
    time.sleep(tf)
    pause()

def ccw(tf=-1.0):
    ser.write('l')
    if tf > 0:
        time.sleep(tf)
        pause()

def cw(tf=-1.0):
    ser.write('r')
    if tf > 0:
        time.sleep(tf)
        pause()

def pause():
    ser.write('s')
