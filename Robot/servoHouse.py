import time
from SunFounder_PCA9685 import Servo

def init():
	global steer
	steer = Servo.Servo(0)
	global pan
	pan = Servo.Servo(1)
	global tilt
	tilt = Servo.Servo(2)
	Servo.Servo(0).setup()
	Servo.Servo(1).setup()
	Servo.Servo(2).setup()
	setPan(90)

def setSteer(v):
	v = 90 + v
	steer.write(v)

def setPan(v):
	pan.write(v)

def setTilt(v):
	tilt.write(v)


