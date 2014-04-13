simple_RGB_driver
=================

This will allow you to use a(n) RGB LED(s) straight from your raspberry pi WITHOUT a servo driver!<br />
Forked from [smithje/RGB_LED_Driver](https://github.com/smithje/RGB_LED_Driver) on github. 90% of the code is completely untouched so usage is similar.
Requires 3 TIP120 (1 per color channel) and appropriate power source for LED strips or 12V LEDs.
I wired my stuff as according to this image: http://mitchtech.net/wp-content/uploads/2013/01/raspi_rgb_led.png<br />
Honestly I'm just trying to combine two things together if it sucks please do not hate me. It seems surprisingly simple to just...not implement the servo driver originally used in this script.<br />
I can’t code.<br />
I also optimized some other code to make it go direct to the /dev/servoblaster instead of running a stupid external command.
I don't know how the RGB values are to be sent just yet.

This isn't tested yet. I'm waiting for hardware to arrive so I can test this. I'm also going to write (I mean fork and modify) some other stuff to get an LCD status output as well as IR input via a 44-key controller remote that I have with a standard LED RGB strip controller.
