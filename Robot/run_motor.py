import time
from SunFounder_TB6612 import TB6612
import RPi.GPIO as GPIO
import time
from SunFounder_PCA9685 import Servo
print "********************************************"
print "*                                          *"
print "*           SunFounder TB6612              *"
print "*                                          *"
print "*          Connect MA to BCM17             *"
print "*          Connect MB to BCM18             *"
print "*         Connect PWMA to BCM27            *"
print "*         Connect PWMB to BCM22            *"
print "*                                          *"
print "********************************************"
a = Servo.Servo(4)
b = Servo.Servo(5)
Servo.Servo(4).setup()
Servo.Servo(5).setup()
#GPIO.setmode(GPIO.BCM)
#GPIO.setup((27, 22), GPIO.OUT)
#a = GPIO.PWM(27, 60)
#b = GPIO.PWM(22, 60)
#a.start(0)
#b.start(0))

def a_speed(value):
	a.write(value)

def b_speed(value):
	b.write(value)

motorB = TB6612.Motor(17)
motorA = TB6612.Motor(18)
motorA.debug = True
motorB.debug = True
motorA.pwm = a_speed
motorB.pwm = b_speed

delay = 0.05
motorA.forward()
motorA.seped = 100
motorB.forward()
motorB.speed = 100
