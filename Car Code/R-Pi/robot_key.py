import IoRTcarL as iortl

def getch():
  import sys, tty, termios
  old_settings = termios.tcgetattr(0)
  new_settings = old_settings[:]
  new_settings[3] &= ~termios.ICANON
  try:
    termios.tcsetattr(0, termios.TCSANOW, new_settings)
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(0, termios.TCSANOW, old_settings)
  return ch

#ser = serial.Serial('/dev/ttyACM0', 9600)

while 1:
  c = getch()
  if c == 'w' or c == 'W':
    iortl.forward()
  elif c == 'x' or c == 'X':
    iortl.backward()
  elif c == 'd' or c == 'D':
    iortl.cw()
  elif c == 'a' or c == 'A':
    iortl.ccw()
  elif c == 'z' or c == 'Z':
    iortl.accelerate()
  elif c == 's' or c == 'S':
    iortl.pause()
  else:
    continue
  print(iortl.ser.readline())
