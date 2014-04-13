simple_RGB_driver
=================

This will allow you to use a(n) RGB LED(s) straight from your raspberry pi WITHOUT a servo driver!<br />
Forked from some code on a website (It’s in the comments in the script)<br />
Requires 3 TIP120 (1 per color channel) and appropriate power source for LED strips or 12V LEDs.
I wired my stuff as according to this image: http://mitchtech.net/wp-content/uploads/2013/01/raspi_rgb_led.png<br />
I chose a different thing than I was originally going to do of which is much more efficient and uses PWM integrated into the Python GPIO library instead of some stupid external bullcrap.<br />
I can’t code. This sucks a lot. I just piece things together and see if it works and call it a day.<br />

This isn't tested yet. I'm waiting for hardware to arrive so I can test this. I'm also going to write (I mean fork and modify) some other stuff to get an LCD status output as well as IR input via a 44-key controller remote that I have with a standard LED RGB strip controller. Good luck to me.
