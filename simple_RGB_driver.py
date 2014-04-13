#!/usr/bin/python3
#Controlling a RGB LED with built in PWM.
#Mostly copied from GPIO PWM example:
#http://code.google.com/p/raspberry-gpio-python/wiki/PWM
   
import time
import RPi.GPIO as GPIO
import math
import argparse

   
GPIO.setmode(GPIO.BOARD)
red_pin = 7
green_pin = 11
blue_pin = 12
red = red_pin #pin numbers to match LED legs
green = green_pin
blue = blue_pin
   
GPIO.setup(red, GPIO.OUT) #setup all the pins
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100 #Hz

#setup all the colours
RED = GPIO.PWM(red, Freq) #Pin, frequency
RED.start(0) #Initial duty cycle of 0, so off
GREEN = GPIO.PWM(green, Freq)
GREEN.start(0)
BLUE = GPIO.PWM(blue, Freq)
BLUE.start(0)

def colour(R, G, B, on_time):
    #colour brightness range is 0-100
    RED.ChangeDutyCycle(R)
    GREEN.ChangeDutyCycle(G)
    BLUE.ChangeDutyCycle(B)
    time.sleep(on_time)

def off():
    RED.ChangeDutyCycle(0)
    GREEN.ChangeDutyCycle(0)
    BLUE.ChangeDutyCycle(0)

def fade(from_red, from_green, from_blue, to_red, to_green, to_blue, steps, delay):
    red_step = float(to_red - from_red)/steps
    green_step = float(to_green - from_green)/steps
    blue_step = float(to_blue - from_blue)/steps
    for step in range(0, steps+1):
        red_value = from_red + red_step*step
        green_value = from_green + green_step*step
        blue_value = from_blue + blue_step*step
        colour(red_value, green_value, blue_value, delay)

def PosSinWave(amplitude, angle, frequency):
    #angle in degrees
    #creates a positive sin wave between 0 and amplitude*2
    return amplitude + (amplitude * math.sin(math.radians(angle)*frequency) )
    while 1:
        for i in range(0, 720, 5):
            colour(PosSinWave(50, i, 0.5), PosSinWave(50, i, 1), PosSinWave(50, i, 2), 0.1)

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
    parser.add_argument('--color', '-c', required=True, type=int, default=[100, 100, 100], nargs=3, help="Define the color to output")
    parser.add_argument('--color-to', '-c2', type=int, default=[0, 0, 0], nargs=3, help="Define the second color for the fade function")
    parser.add_argument('--fade', '-f', type=int, nargs=2, help="Enable fade mode. First number is steps, second number is delay")
    parser.add_argument('--pins', '-p', type=int, default=[7, 11, 12], nargs=3, help="Specify pins to send PWM signal (only required if it is changes)")
    parser.add_argument('--colorwave', '-cw', action="store_true", help="Does some cool color effect thing. I don't even know what it does lol")
    args = parser.parse_args()
    try:
        if args.static is True:
            colour(args.color[0], args.color[1], args.color[2], 0)
            new = input('R G B -->')
            colour(new, 0)
        if args.fade is True:
            fade(args.color[0], args.color[1], args.color[2], args.color-to[0], args.color-to[1], args.color-to[2], args.fade[0], args.fade[1])
        if args.cleanup is True:
            cleanup()
    finally:
        parser.parse_args('help')

"""  File simple_RGB_driver.py, line 87
    
    ^
    IndentationError: unexpected unindent
        DA FUQQ??!?!?!?!?!?"""