# Press the button to enable (green LED) or disable (red LED) fast mouse-clicking mode.
# I built this so my wife could like-bomb her favorite twitch streamers
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

print("Auto-clicker ready!")

while True:
    # Main loop: Red LED, wait for button press
    pixel[0] = RED
    
    # Wait for button press
    while button.value:  # Button not pressed (active LOW)
        time.sleep(0.01)
    
    # Button pressed - turn LED green and debounce
    pixel[0] = GREEN
    time.sleep(1.0)  # 1 second debounce
    
    # Enter auto-click mode
    print("Auto-clicking started...")
    
    while True:
        # Random delay between 100-500ms
        delay = random.uniform(0.02, 0.1)
        time.sleep(delay)
        
        # Left mouse click
        mouse.click(Mouse.LEFT_BUTTON)
        
        # Check if button is pressed to exit auto-click mode
        if not button.value:  # Button pressed (active LOW)
            print("Auto-clicking stopped")
            pixel[0] = RED
            time.sleep(1.0)  # 1 second debounce
            break  # Return to main loop
