# Trinkey QT2040 Multi-Attack
This is a multi-faceted attack relying on CircuitPython HID inject, 
and the Trinkey QT2040's JST SH I2C connector and copious amount 
of USB mass storage.

## Setup
This code was developed on CircuitPython 7.0.0. Newer versions of 
CircuitPython will probably work fine. 
The NEOPIXEL, adafriut_pixelbuf and adafruit_hid libraries for 
CircuitPython 7.0.0 or newer will have to be installed separately.
Download the [CircuitPython Library Bundle](https://circuitpython.org/libraries).
See the lib.txt file for a list of bare minimum library dependencies
for this project.

## Ideal Concept -- Not entirely implemented yet
My idea was to set this device up with an I2C light or motion sensor. 
Upon plugging the device in, the mouse jiggler functionality would start
and move the mouse one pixel left or right every 30 seconds to keep the
computer's screen saver or sleep function from invoking. After the lights
are turned out or no motion nearby has been detected, a timer begins, and
after the timer expires, the keyboard injection is launched. This would
run an executable payload directly from the Trinkey RP2040's own USB 
mass storage, as opposed to downloading the payload over the Internet. 

This payload could be a keystroke logger, remote access trojan or other 
attack. 

## Work In Progress
Currently, only the mouse jiggler and keyboard injection are implemented.
When inserted, the device sits in the idle state after booting up (Green
LED). When you briefly press Button 0, it will invoke the mouse jiggler
(Blue LED). If you press and hold Button 0 for about 1 second, the 
keyboard inject attack will execute. Currently, the keyboard injection
method runs some PowerShell to detect the drive letter that the Trinkey
QT2040's mass storage has been mapped to. A few additional lines of code
can be added to execute a user-supplied executable payload stored there. 
