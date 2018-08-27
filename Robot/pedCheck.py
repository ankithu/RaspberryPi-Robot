import pedDetect
import cv2
img = cv2.VideoCapture(0)
while(True):
	
	_,image = img.read()
	print(pedDetect.checkForPeds(image))