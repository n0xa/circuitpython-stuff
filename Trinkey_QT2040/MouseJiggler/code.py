# Press the button to enable (green LED) or disable (red LED) fast mouse-jiggler mode.
# Surely you wouldn't use this to keep your Microsoft Teams status as Active while 
# you step away from your workstation for a while...
import board
import digitalio
import time
import random
import usb_hid
import neopixel
from adafruit_hid.mouse import Mouse

# Set up the button
button = digitalio.DigitalInOut(board.BUTTON)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Button is active LOW

# Set up the NeoPixel LED
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

# Set up the mouse
mouse = Mouse(usb_hid.devices)

# Colors
RED = (25, 0, 0)
GREEN = (0, 25, 0)
OFF = (0, 0, 0)

while True:
    # Main loop: Red LED, wait for button press
    pixel[0] = RED
    
    # Wait for button press
    while button.value:  # Button not pressed (active LOW)
        time.sleep(0.01)
    
    # Button pressed - turn LED green and debounce
    pixel[0] = GREEN
    time.sleep(1.0)  # 1 second debounce
        
    while True:
        # move mouse right 5 pixels, left 5 pixels
        mouse.move(x=5)
        time.sleep(0.1)
        mouse.move(x=-5)

        # Random delay between 30-120 seconds
        delay = random.uniform(30, 120)
        for i in range(delay * 10000):
            time.sleep(0.1)
            # Check if button is pressed to exit auto-click mode
            if not button.value:  # Button pressed (active LOW)
                pixel[0] = OFF
                break       
        
        # Check if button is pressed to exit auto-click mode
        if not button.value:  # Button pressed (active LOW)
            pixel[0] = RED
            time.sleep(1.0)  # 1 second debounce
            break  # Return to main loop
