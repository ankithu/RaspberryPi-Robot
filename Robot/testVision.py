import visionDelegate
import atexit
import driveManager
driveManager.init()
visionDelegate.init()
power = 30

def cleanup():
	print('exiting lane follower')
	print('protecting motors and servos')
	driveManager.stop()
	driveManager.steer(0)

atexit.register(cleanup)
while(True):
	visionDelegate.follow(power)