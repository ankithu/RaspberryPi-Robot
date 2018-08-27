import servoHouse
from picar import back_wheels
import picar

def init():
	picar.setup()
	global bw
	bw  = back_wheels.Back_Wheels()
	picar.setup()
	servoHouse.init()

def forward(speed):
	bw.speed = speed
	bw.backward()

def backward(speed):
	bw.speed = speed
	bw.forward()

def stop():
	bw.stop()

def steer(ang):
	servoHouse.setSteer(ang)
