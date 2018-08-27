import servoHouse
import time

servoHouse.init()
for i in range (45, 135, 5):
	servoHouse.setTilt(i)
	for ii in range(45, 135, 1):
		servoHouse.setPan(ii)
		time.sleep(0.03)

