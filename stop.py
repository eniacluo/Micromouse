#!/usr/bin/env python3
import time
from ev3dev.ev3 import *
ir = InfraredSensor('in4')
#ut = ev3.UltrasonicSensor()
left = UltrasonicSensor('in2')
right = UltrasonicSensor('in3')
#touch = ev3.TouchSensor()
motorR = Motor('outC')
motorL = Motor('outB')

motorR.stop(stop_action='hold')
motorL.stop(stop_action='hold')