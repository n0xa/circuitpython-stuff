# Example HID Injection Opens the infamous youtube video on Windows.
import board
import digitalio
import time
import random
import usb_hid
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
kbd = Keyboard(usb_hid.devices)
m = Mouse(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

# Set up the button
button = digitalio.DigitalInOut(board.BUTTON)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Button is active LOW

# Set up the NeoPixel LED
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

# Set up the mouse
kbd = Keyboard(usb_hid.devices)

# Colors
RED = (25, 0, 0)
GREEN = (0, 25, 0)
OFF = (0, 0, 0)

print("Firin Mah Lazor")

while True:
    # Main loop: Red LED, wait for button press
    pixel[0] = RED

    kbd.press(Keycode.GUI, Keycode.R)
    kbd.release_all()
    time.sleep(0.2)
    layout.write('https://www.youtube.com/watch?v=dQw4w9WgXcQ\n')

    # Button pressed - turn LED green and debounce
    pixel[0] = GREEN
    time.sleep(1.0)  # 1 second debounce

    # Wait for button press
    while button.value:  # Button not pressed (active LOW)
        time.sleep(0.01)
    
