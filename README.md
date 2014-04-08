simple_RGB_driver
=================

This will allow you to use a(n) RGB LED(s) straight from your raspberry pi WITHOUT a servo driver!<br />
Forked from [smithje/RGB_LED_Driver](https://github.com/smithje/RGB_LED_Driver) on github. 90% of the code is completely untouched so usage is similar.
Requires 3 TIP120 (1 per color channel) and appropriate power source for LED strips or 12V LEDs.
Also requires ServoBlaster, go get it at [richardghirst/PiBits/ServoBlaster](https://github.com/richardghirst/PiBits/ServoBlaster) and I wired my stuff as according to this image: http://mitchtech.net/wp-content/uploads/2013/01/raspi_rgb_led.png<br />
I also recommend that you configure ServoBlaster as follows:
```
$ ./servod --cycle-time 10000us --p1pins=7,11,12,0,0,0,0,0
```
This will reduce flicker and also free up the rest of your GPIO pins if you choose to use them and matches the default settings for the thingamajig. This program will still function if you don't but it will be quite flickery…<br />
Honestly I'm just trying to combine two things together if it sucks please do not hate me. It seems surprisingly simple to just...not implement the servo driver originally used in this script.<br />
I also optimized some other code to make it go direct to the /dev/servoblaster instead of running a stupid external command.
I don't know how the RGB values are to be sent just yet.

This isn't tested yet. I'm waiting for hardware to arrive so I can test this. I'm also going to write (I mean fork and modify) some other stuff to get an LCD status output as well as IR input via a 44-key controller remote that I have with a standard LED RGB strip controller.
