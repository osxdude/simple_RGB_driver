#!/usr/bin/python3
#Controlling a RGB LED with built in PWM.
#Mostly copied from GPIO PWM example:
#http://code.google.com/p/raspberry-gpio-python/wiki/PWM
   
import time
import RPi.GPIO as GPIO
import math
import argparse
   
GPIO.setmode(GPIO.BCM)
red_pin = 3
green_pin = 4
blue_pin = 18
red = red_pin #pin numbers to match LED legs
green = green_pin
blue = blue_pin
   
GPIO.setup(red, GPIO.OUT) #setup all the pins
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100 #Hz
fade = 6

#setup all the colours
RED = GPIO.PWM(red, Freq) #Pin, frequency
RED.start(0) #Initial duty cycle of 0, so off
GREEN = GPIO.PWM(green, Freq)
GREEN.start(0)
BLUE = GPIO.PWM(blue, Freq)
BLUE.start(0)

def colour(R, G, B):
    #colour brightness range is 0-100
    RED.ChangeDutyCycle(R)
    GREEN.ChangeDutyCycle(G)
    BLUE.ChangeDutyCycle(B)

def PosSinWave(amplitude, angle, frequency):
    #angle in degrees
    #creates a positive sin wave between 0 and amplitude*2
    return amplitude + (amplitude * math.sin(math.radians(angle)*frequency) )
    
def smooth(delay):
    while 1:
        for i in range(0, 360, 5):
                RED.ChangeDutyCycle(PosSinWave(50, i, 4))
                GREEN.ChangeDutyCycle(PosSinWave(50, i, 2))
                BLUE.ChangeDutyCycle(PosSinWave(50, i, 3))
                time.sleep(delay)

def hard(mode):
   if mode is 1:
      while Shit:
          RED.ChangeDutyCycle(range(100, 0, 1))
          GREEN.ChangeDutyCycle(range(100, 0, 1))
          BLUE.ChangeDutyCycle(range(100, 0, 1))

def cleanup():
    #Stop all the PWM objects
    RED.stop()
    GREEN.stop()
    BLUE.stop()
    #Tidy up and remaining connections.
    GPIO.cleanup()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='drive an RGB LED')
    parser.add_argument('--static', '-s', action="store_true", help="Specify static changes of the lights")
    parser.add_argument('--off', '-o', action="store_true", help="Turn off the lights...???")
    parser.add_argument('--cleanup', '-gc', action="store_true", help="Cleanup PWM and GPIO (for debug!!)")
    parser.add_argument('--color', '-c', type=int, default=[100, 100, 100], nargs=3, help="Define the color to output")
    parser.add_argument('--pins', '-p', type=int, default=[7, 11, 12], nargs=3, help="Specify pins to send PWM signal (only required if it is changes)")
    parser.add_argument('--colorwave', '-cw', action="store_true", help="Does some cool color effect thing. I don't even know what it does lol")
    parser.add_argument('--smooth', '-m', type=int, nargs=1, help="Changable speed smooth color effect. Same as colorwave at 0.1.")
    parser.add_argument('--hard', '-b', type=int, nargs=1, help="Hard color strobe. 3 for RGB or 7 for rainbow.")
    args = parser.parse_args()
    print args
    try:
        if args.static is True:
            while 1:
                colour(args.color[0], args.color[1], args.color[2])
        if args.colorwave is True:
            smooth(0.1)
        if args.smooth is True:
            smooth(args.smooth[0])
        if args.hard == 3:
            hard(1)
    except KeyboardInterrupt:
        cleanup()
    finally:
        cleanup()

"""  File simple_RGB_driver.py, line 87
    
    ^
    IndentationError: unexpected unindent
        DA FUQQ??!?!?!?!?!?"""