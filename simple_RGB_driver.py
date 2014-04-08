"""
Forked from smithje/RGB_LED_Driver on github. 90% of the code is completely untouched so usage is similar. I don't know how the RGB values are to be sent just yet.
This will allow you to use a(n) RGB LED(s) straight from your raspberry pi WITHOUT a servo driver!
Requires 3 TIP120 (1 per color channel) and a +12VDC power source
Also requires ServoBlaster, go get it at richardghirst/PiBits.git/ServoBlaster
I wired my stuff as according to this image: http://mitchtech.net/wp-content/uploads/2013/01/raspi_rgb_led.png
I also recommend that you configure ServoBlaster as follows:
$ ./servod --cycle-time 10000us --p1pins=7,11,12,0,0,0,0,0
This will reduce flicker and also free up the rest of your GPIO pins if you choose to use them and matches the default settings for the thingamajig. This program will still function if you don't but it will be quite flickery...
Honestly I'm just trying to combine two things together if it sucks please do not hate me. It seems surprisingly simple to just...not implement the servo driver originally used in this script.
I also optimized some other code to make it go direct to the /dev/servoblaster instead of running a stupid external command.

This isn't tested yet. I'm waiting for hardware to arrive so I can test this. I'm also going to write (I mean fork and modify) some other stuff to get an LCD status output as well as IR input via a 44-key controller remote that I have with a standard LCD controller.
"""

import time
"""import os"""
 
class RGB_Driver(object):
 
    def pwm(pin, angle):
        print "servo[" + str(pin) + "][" + str(angle) + "]"
        with open('/dev/servoblaster','w') as s:
            f.write(str(pin) + "=" + str(angle))
        """cmd = "echo " + str(pin) + "=" + str(angle) + " > /dev/servoblaster""""
        """os.system(cmd)"""

    def __init__(self, pwm = None, red_pin = 0, green_pin = 1, blue_pin = 2):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        if pwm is None:
            self.pwm = self.setup_pwm()
        else:
            self.pwm = pwm

    @staticmethod
    def convert_eight_to_twelve_bit(eight_bit):
      """The PWM chip has 10 bit resolution, so we need to
            convert regular 8 bit rgb codes
        >>> RGB_Driver.convert_eight_to_ten_bit(0)
        0
        >>> RGB_Driver.convert_eight_to_ten_bit(255)
        4080
        >>> RGB_Driver.convert_eight_to_ten_bit(128)
        2048
        """
    return eight_bit<<4
		
		   
	def set_rgb(self, red_value, green_value, blue_value):
		"""The rgb values must be between 0 and 4095"""
		#print "R: %d, G: %d, B: %d" % (red_value, green_value, blue_value)
		pwm(self.red_pin, red_value)
		pwm(self.green_pin, green_value)
		pwm(self.blue_pin, blue_value)

	@staticmethod
	def sanitize_int(x):
		if x<0:
			return 0
		elif x>4095:
			return 4095
		else:
			return int(x)


	@staticmethod
	def randrange(start, stop, step=1):
		"""A slightly modified version of randrange which allows start==stop"""
		if start == stop:
			return start
		else:
			return randrange(start, stop, step) 

	def fade_rgb(self, from_red, from_green, from_blue, to_red, to_green, to_blue, steps, delay):
		"""Fade from one rgb value to another in steps, waiting for delay ms between each step
            all rgb values must be 10 bit ints (between 0 and 1023)"""
		red_step = float(to_red - from_red)/steps
		green_step = float(to_green - from_green)/steps
		blue_step = float(to_blue - from_blue)/steps
		
		for step in range(0, steps+1):
			red_value = self.sanitize_int(from_red + red_step*step)
			green_value = self.sanitize_int(from_green + green_step*step)
			blue_value = self.sanitize_int(from_blue + blue_step*step)
			self.set_rgb(red_value, green_value, blue_value)
			time.sleep(delay)

    @staticmethod
    def get_next_random_value(current_value, minimum_allowed, maximum_allowed, max_walk):
        """Generate the next random value, given the current, max, and min values of that channel
            as well as the maximum change (walk) allowed"""
        min = current_value - max_walk
        if min<minimum_allowed:
            min = minimum_allowed
        elif min<0:
            min = 0

        max = current_value + max_walk
        if max>maximum_allowed:
            max = maximum_allowed
        elif max>4095:
        max=4095

        return RGB_Driver.randrange(min, max)


    def random_walk(self, min_red, min_green, min_blue, max_red, max_green, max_blue, random_time, delay, max_walk):
    begin = time.time()
    red = self.randrange(min_red, max_red)
        green = self.randrange(min_green, max_green)
    blue = self.randrange(min_blue, max_blue)
    self.set_rgb(red, green, blue)
    time.sleep(delay)
        while time.time()-begin<random_time:
            red = self.get_next_random_value(red, min_red, max_red, max_walk)
            green = self.get_next_random_value(green, min_green, max_green, max_walk)
            blue = self.get_next_random_value(blue, min_blue, max_blue, max_walk)
            self.set_rgb(red, green, blue)
            time.sleep(delay)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='drive a rgb led strip through a pwm module')

    parser.add_argument('-r', '--red', nargs=2, type=int, default=[0, 0], help="The beginning and end values for red in fade mode.  Max and min values for red in random mode.")
    parser.add_argument('-g', '--green', nargs=2, type=int, default=[0, 0], help="The beginning and end values for green in fade mode.  Max and min values for green in random mode..")
    parser.add_argument('-b', '--blue', nargs=2, type=int, default=[0, 0], help="The beginning and end values for blue in fade mode.  Max and min values for blue in random mode..")
    parser.add_argument('-s', '--steps', type=int, default=100, help="Number of steps in the fade.  Not used with --random")
    parser.add_argument('-d', '--delay', type=float, default=0.005, help="Number of seconds between the steps or random changes, can be a float")
    parser.add_argument('-o', '--turn-off', action='store_true', help="Turn off when the fade or random event is over.")
    parser.add_argument('--red-pin', type=int, choices=range(0,16), default=0, help="The red pwm pin")
    parser.add_argument('--green-pin', type=int, choices=range(0,16), default=1, help="The green pwm pin")
    parser.add_argument('--blue-pin', type=int, choices=range(0,16), default=2, help="The blue pwm pin")
    parser.add_argument('--repeat', type=int, default=1, help="Repeat the fade this many times.  Unused with --random.")
    parser.add_argument('--reverse', action="store_true", help="Reverse the fade, to return back to the initial state.  Unused with --random.")
    parser.add_argument('--random', action="store_true", help="Move around randomly between the max and min values specified with --red --green and --blue.  Use with --time and --max-random-walk")
    parser.add_argument('--time', type=int, default=10, help="Used with --random.  Move randomly for this many seconds")
    parser.add_argument('--max-random-walk', type=int, default=10, help="The max that each channel will be allowed to change between steps in random mode.")
    args = parser.parse_args()




    driver = RGB_Driver(red_pin = args.red_pin, green_pin = args.green_pin, blue_pin = args.blue_pin)
    try:
        if args.random is False:
            for repeat in xrange(0, args.repeat):
                print "Repetition %d" % repeat
                driver.fade_rgb(args.red[0], args.green[0], args.blue[0], args.red[1], args.green[1], args.blue[1], args.steps, args.delay)
        if args.reverse:
                driver.fade_rgb(args.red[1], args.green[1], args.blue[1], args.red[0], args.green[0], args.blue[0], args.steps, args.delay)
        else:
            # We need to sort the values to make sure randrange works correctly
            args.red.sort()
            args.green.sort()
            args.blue.sort()
            driver.random_walk(args.red[0], args.green[0], args.blue[0], args.red[1], args.green[1], args.blue[1], args.time, args.delay, args.max_random_walk)
    finally:
        if args.turn_off:
            driver.set_rgb(0, 0, 0)
