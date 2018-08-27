from SunFounder_PCA9685 import Servo

servos = []
for i in range (0,3):
	servos.append(Servo.Servo(i))  # channel 1
        Servo.Servo(i).setup()
        print 'myservo%s'%i


for i in range (0,3):
	print('setting channel:' +str(i) + ' to its middle')
	servos[i].write(90)

