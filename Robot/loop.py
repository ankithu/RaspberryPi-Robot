import vision, PID, driveManager, cameraMan, atexit, printManager
pid = PID.PID()
vision = vision.Vision()
p,i,d = 0.0,0.0,0.0
pid.init(0.0,p,i,d)
vision.init()
speed = 50
driveManager.init()
cameraMan.init()
cameraMan.pan(0)
def exit_handler():
	print (printManager.color.BOLD+'warning'+printManager.color.END+printManager.color.RED+'error code: fatal'+printManager.color.END+printManager.color.BLUE+'program ending. Activating Emergency Motor Shutoff')
	driveManager.stop()

atexit.register(exit_handler)
while True:
	print('calculating steering  adjustment')
	turn = pid.calculate(vision.getLaneOffset())
	##owerLeft = speed + turn
	#powerRight = speed - turn
	print('applying turn adjustment')
	driveManager.steer(turn)
	driveManager.forward(speed)
	#print('applying power adjustment')


