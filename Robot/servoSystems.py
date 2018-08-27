import time
import servoHouse
#from SunFounder_PCA9685 import Servo
#pan  = Servo.Servo(2)
#tilt  = Servo.Servo(1)
#steer = Servo.Servo(0)
#Servo.Servo(2).setup()
#Servo.Servo(1).setup()
#Servo.Servo(0).setup()
servoHouse.init()
while True:
	for i in range (45,135,1):
		#steer.write(i)
		#tilt.write(i)
		#pan.write(i)
		servoHouse.setSteer(i-90)
		servoHouse.setTilt(i)
		servoHouse.setPan(i)
		time.sleep(0.03)
	for i in range (135,45,-1):
		#tilt.write(i)
		#steer.write(i)
		#pan.write(i)
		servoHouse.setSteer(i-90)
		servoHouse.setTilt(i)
		servoHouse.setPan(i)
		time.sleep(0.03)
