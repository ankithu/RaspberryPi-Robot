#from picar import back_wheels
#import picar
import time
import driveManager
#import servoHouse
#picar.setup()
#bw = back_wheels.Back_Wheels()
#picar.setup()
#bw.speed = 0
#servoHouse.init()
#bw.forward()
driveManager.init()
def main():

	steeringAngle = 20
	speed = 100
	driveManager.steer(steeringAngle)
	driveManager.forward(speed)
	time.sleep(10)
	driveManager.backward(speed)
	time.sleep(10)
	destroy()
	#bw.speed = 50
	#bw.backward()
	#servoHouse.setSteer(steeringAngle)
	#time.sleep(10)
	#bw.forward()
	#time.sleep(10)
	#destroy()


def destroy():
	driveManager.stop()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		destroy()


