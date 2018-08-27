import servoHouse

def init():
	servoHouse.init()

def pan(value):
	servoHouse.setPan(value+90)

def tilt(value):
	servoHouse.setTilt(value)

def center():
	servoHouse.setPan(90)
	servoHouse.setTilt(90)
