import redLaneVisionEngine
import cv2
import driveManager
import time
import pedDetect

class Container:
	count = 0
	lookingForLane = False
	firstTime = True
	noLaneCount = 0
	calibratedStartingX = 221.0
	MAX_ANGLE = 30.0
	MAX_NO_LANE_COUNT = 9
	last_good_angle = 0
	lastTime = 0
	time = 0
def init():
	global img
	img = cv2.VideoCapture(0)
	global JUMP
	JUMP = 200
	global jumpCount
	jumpCount = 0
	global JUMP_MAX
	JUMP_MAX = 10
	global CAMERA_INIT
	CAMERA_INIT = 30
	global vision
	vision = redLaneVisionEngine.vision()
	global WIDTH
	WIDTH = 640
	global HEIGHT
	HEIGHT = 480
	img.set(3,WIDTH)
	img.set(4,HEIGHT)
	global steerSet
	steerSet = [None]*11 #size of  11
	global count
	Container.count = 0
	global lastSteer
	lastSteer = 0
	driveManager.init()
	driveManager.steer(0)
	global MAX_LANE_WIDTH
	MAX_LANE_WIDTH = 200
	global MIN_LANE_HEIGTH
	MIN_LANE_HEIGTH = 40
	

def follow(power):
	_, image = img.read()
	vision.process(image)
	countours = vision.find_contours_output
	minY = 0
	minY2 = 0
	#print(len(countours))
	if (len(countours)>0):
		keyCountour = countours[0]
		#if (len(countours) > 1):
		#	keyCoutnour2 = countours[1]
		keyX = WIDTH/2
		keyW = 0
		keyH = 0
		#keyX2 = WIDTH/2
		for countour in countours:
			x,y,w,h = cv2.boundingRect(countour)
			if (y>minY and w<MAX_LANE_WIDTH and h>MIN_LANE_HEIGTH):
				#minY2 = minY
				minY = y
				#keyCoutnour2 = keyCountour
				keyCountour = countour
				#keyX2 = keyX
				keyX = x
				keyW = w
				keyH = h
			#elif (y>minY2 and w<MAX_LANE_WIDTH and h>MIN_LANE_HEIGTH):
			#	minY2 = y
			#	keyX2 = x
			#	keyCoutnour2 = countour

		#if (abs(keyX-Container.calibratedStartingX) > abs(keyX2-Container.calibratedStartingX)):
		#	keyCountour = keyCoutnour2
		#	keyX,keyY,keyW,keyH = cv2.boundingRect(keyCountour)
		#print(keyX)
		keyDif = (keyX-Container.calibratedStartingX) * 2
		steer = (keyDif/Container.calibratedStartingX)*Container.MAX_ANGLE
		#steer = ((keyX-221.0)/221.0)*45.0
		print('raw steer:' + str(steer))
		print('raw calibratedStartingX:' + str(Container.calibratedStartingX))
		if (Container.count==0):
			lastSteer == steer
		if (Container.count < 11):
			steerSet[Container.count] = steer
		else:
			steerSet[Container.count%11] = steer
			steer = sorted(steerSet)[5]
		
		if (steer > Container.MAX_ANGLE):
			steer = Container.MAX_ANGLE
		elif(steer < -Container.MAX_ANGLE):
			steer = -Container.MAX_ANGLE

		if(lastSteer!=0.0):
			if (abs(steer - lastSteer)>=JUMP):	
				steer = lastSteer
				jumpCount = jumpCount + 1
				if (jumpCount == JUMP_MAX):
					steer = steer
					jumpCount = 0

		#if(steer!=0):	
		print(str(keyX)+'   ,   '+str(steer))
		if(Container.count>=CAMERA_INIT):
			#if (Container.count%20 == 0):
				#if (pedDetect.checkForPeds(image)):
				#	while(pedDetect.checkForPeds(image)):
				#		_, image = img.read()
				#		driveManager.stop()
				#		print('pedestrian detected! stopping until the brat goes away')
			if((keyW>MAX_LANE_WIDTH or keyH<MIN_LANE_HEIGTH) and (Container.noLaneCount>Container.MAX_NO_LANE_COUNT)):
				print('NO LANE! Reported KeyW:' + str(keyW) + ', Reported KeyH:' + str(keyH))
				driveManager.steer(-Container.last_good_angle)
				driveManager.backward(power)
				Container.lookingForLane = True
			elif((keyW>MAX_LANE_WIDTH or keyH<MIN_LANE_HEIGTH)):
				print('NO LANE BUT WAITING FOR CORRECTION! Reported KeyW:' + str(keyW) + ', Reported KeyH:' + str(keyH))
				driveManager.steer(Container.last_good_angle)
				driveManager.forward(power)
				Container.lookingForLane = True
				Container.noLaneCount = Container.noLaneCount + 1
			else:
				if (Container.lookingForLane):
					Container.noLaneCount = 0
					Container.lookingForLane = False
				if(Container.firstTime):
					Container.calibratedStartingX = keyX * 1.0
					Container.firstTime = False
				print('Found Lane, Reported KeyW:' + str(keyW) + ', Reported KeyH:' + str(keyH))
				driveManager.steer(steer)
				driveManager.forward(power)
				Container.lastTime = Container.time
				Container.time = time.time()
				delta = (Container.time - Container.lastTime) * 1.0
				fps = 1.0 / delta
				print('processing speed(fps):' + str(fps))
				Container.last_good_angle = steer
			#time.sleep(0.01)
		Container.count = Container.count + 1

def followLeftOfLane(power):
	_, image = img.read()
	vision.process(image)
	countours = vision.filter_contours_output
	minY = 0
	minY2 = 0
	print(len(countours))
	if (len(countours)>0):
		keyCountour = countours[0]
		if (len(countours) > 1):
			keyCoutnour2 = countours[1]
		keyX = WIDTH/2
		keyW = 0
		keyH = 0
		keyX2 = WIDTH/2
		for countour in countours:
			x,y,w,h = cv2.boundingRect(countour)
			if (y>minY and w<MAX_LANE_WIDTH and h>MIN_LANE_HEIGTH):
				minY2 = minY
				minY = y
				keyCoutnour2 = keyCountour
				keyCountour = countour
				keyX2 = keyX
				keyX = x
				keyW = w
				keyH = h
			elif (y>minY2 and w<MAX_LANE_WIDTH and h>MIN_LANE_HEIGTH):
				minY2 = y
				keyX2 = x
				keyCoutnour2 = countour


		if(keyX<keyX2):
			keyX = keyX2
		#if (abs(keyX-Container.calibratedStartingX) > abs(keyX2-Container.calibratedStartingX)):
		#	keyCountour = keyCoutnour2
		#	keyX,keyY,keyW,keyH = cv2.boundingRect(keyCountour)
		#print(keyX)
		steer = ((keyX - Container.calibratedStartingX)/Container.calibratedStartingX)*Container.MAX_ANGLE
		#steer = ((keyX-221.0)/221.0)*45.0
		print('raw steer:' + str(steer))
		print('raw calibratedStartingX:' + str(Container.calibratedStartingX))
		if (Container.count==0):
			lastSteer == steer
		if (Container.count < 11):
			steerSet[Container.count] = steer
		else:
			steerSet[Container.count%11] = steer
			steer = sorted(steerSet)[5]
		
		if (steer > Container.MAX_ANGLE):
			steer = Container.MAX_ANGLE
		elif(steer < -Container.MAX_ANGLE):
			steer = -Container.MAX_ANGLE

		if(lastSteer!=0.0):
			if (abs(steer - lastSteer)>=JUMP):	
				steer = lastSteer
				jumpCount = jumpCount + 1
				if (jumpCount == JUMP_MAX):
					steer = steer
					jumpCount = 0

		#if(steer!=0):	
		print(str(keyX)+'   ,   '+str(steer))
		if(Container.count>=CAMERA_INIT):
			if (Container.count%20 == 0):
				if (pedDetect.checkForPeds(image)):
					while(pedDetect.checkForPeds(image)):
						driveManager.stop()
						print('pedestrian detected! stopping until the brat goes away')
						_, image = img.read()
			if((keyW>MAX_LANE_WIDTH or keyH<MIN_LANE_HEIGTH) and (Container.noLaneCount>Container.MAX_NO_LANE_COUNT)):
				print('NO LANE! Reported KeyW:' + str(keyW) + ', Reported KeyH:' + str(keyH))
				driveManager.steer(-Container.last_good_angle)
				driveManager.backward(power)
				Container.lookingForLane = True
			elif((keyW>MAX_LANE_WIDTH or keyH<MIN_LANE_HEIGTH)):
				print('NO LANE BUT WAITING FOR CORRECTION! Reported KeyW:' + str(keyW) + ', Reported KeyH:' + str(keyH))
				driveManager.steer(Container.last_good_angle)
				driveManager.forward(power)
				Container.lookingForLane = True
				Container.noLaneCount = Container.noLaneCount + 1
			else:
				if (Container.lookingForLane):
					Container.noLaneCount = 0
					Container.lookingForLane = False
				if(Container.firstTime):
					Container.calibratedStartingX = keyX * 1.0
					Container.firstTime = False
				print('Found Lane, Reported KeyW:' + str(keyW) + ', Reported KeyH:' + str(keyH))
				driveManager.steer(steer)
				driveManager.forward(power)
				Container.lastTime = Container.time
				Container.time = time.time()
				delta = (Container.time - Container.lastTime) * 1.0
				fps = 1.0 / delta
				print('processing speed(fps):' + str(fps))
				Container.last_good_angle = steer
			#time.sleep(0.01)
		Container.count = Container.count + 1

def followTwoLane(power):
	_, image = img.read()
	vision.process(image)
	countours = vision.filter_contours_output
	minY = 0
	secMinY = 0
	keyX1 = WIDTH/2
	keyX2 = WIDTH/2
	if (len(countours)>1):
		keyCountour = countours[0]
		secondKeyCountour = countours[1]
		x,y,w,h = cv2.boundingRect(keyCountour)
		x2,y2,w2,h2 = cv2.boundingRect(secondKeyCountour)
		if (y2 > y):
			keyCountour = secondKeyCountour
			secondKeyCountour = countours[0]
			minY = y2
			secMinY = y
		else:
			minY = y
			secMinY = y2
		for countour in countours:
			x,y,w,h = cv2.boundingRect(countour)
			if(y>minY):
				secMinY = minY
				minY = y
				secondKeyCountour = keyCountour
				keyCountour = countour
				keyX2 = keyX
				keyX1 = x
			elif(y>secMinY):
				keyX2 = x
				secMinY = y
				secondKeyCountour = countour
		keyX = (keyX2+keyX1)/2
		#print(keyX)
		steer = -(250-keyX)/5.55
		if (Container.count==0):
			lastSteer == steer
		if (Container.count < 11):
			steerSet[Container.count] = steer
		else:
			steerSet[Container.count%11] = steer
			steer = sorted(steerSet)[5]
		
		if (steer > 45):
			steer = 45
		elif(steer < -45):
			steer = -45

		if(lastSteer!=0.0):
			if (abs(steer-lastSteer)>=JUMP):	
				steer = lastSteer
				jumpCount = jumpCount + 1
				if (jumpCount == JUMP_MAX):
					steer = steer
					jumpCount = 0

		_,_,w1,h1 = cv2.boundingRect(keyCountour)
		_,_,w2,h2 = cv2.boundingRect(secondKeyCountour)
		keyW = (w1+w2)/2
		keyH = (h1+h2)/2

		#if(steer!=0):	
		print(str(keyX)+'   ,   '+str(steer))
		if(Container.count>=CAMERA_INIT):
			if (Container.count%20 == 0):
				if (pedDetect.checkForPeds(image)):
					while(pedDetect.checkForPeds(image)):
						_, image = img.read()
						driveManager.stop()
						print('pedestrian detected! stopping until the brat goes away')
			#if((keyW>MAX_LANE_WIDTH or keyH<MIN_LANE_HEIGTH) and (Container.noLaneCount>Container.MAX_NO_LANE_COUNT)):
			#	print('NO LANE! Reported KeyW:' + str(keyW) + ', Reported KeyH:' + str(keyH))
			#	driveManager.steer(-Container.last_good_angle)
			#	driveManager.backward(power)
			#	Container.lookingForLane = True
			#elif((keyW>MAX_LANE_WIDTH or keyH<MIN_LANE_HEIGTH)):
			#	print('NO LANE BUT WAITING FOR CORRECTION! Reported KeyW:' + str(keyW) + ', Reported KeyH:' + str(keyH))
			#	driveManager.steer(Container.last_good_angle)
			#	driveManager.forward(power)
			#	Container.lookingForLane = True
			#	Container.noLaneCount = Container.noLaneCount + 1
			if 1==0:
				print('sike')
			else:
				if (Container.lookingForLane):
					Container.noLaneCount = 0
					Container.lookingForLane = False
				if(Container.firstTime):
					Container.calibratedStartingX = keyX * 1.0
					Container.firstTime = False
				print('Found Lane, Reported KeyW:' + str(keyW) + ', Reported KeyH:' + str(keyH))
				driveManager.steer(steer)
				driveManager.forward(power)
				Container.lastTime = Container.time
				Container.time = time.time()
				delta = (Container.time - Container.lastTime) * 1.0
				fps = 1.0 / delta
				print('processing speed(fps):' + str(fps))
				Container.last_good_angle = steer
			#time.sleep(0.01)
		Container.count = Container.count + 1
	
