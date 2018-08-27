import time
from SunFounder_PCA9685 import Servo

motorA = Servo.Servo(4)
motorB = Servo.Servo(5)

Servo.Servo(4).setup()
Servo.Servo(5).setup()

motorA.write(0)
motorB.write(0)


