# Green = idle. blue = mouse jiggle enabled. red = typing HID injects
# Tap button to toggle mouse jiggler. Hold to trigger HID Inject

jigglesec = 30 # seconds between small mouse movements 

def inject():
    # this function is called when HID Inject is triggered
    pixel.fill((2, 0, 0))
    kbd.press(Keycode.GUI, Keycode.R)
    kbd.release_all()
    time.sleep(0.2)
    layout.write('powershell')
    time.sleep(0.5)
    kbd.press(Keycode.CONTROL, Keycode.SHIFT, Keycode.ENTER)
    kbd.release_all()
    time.sleep(1.5)    
    kbd.press(Keycode.LEFT_ARROW)
    kbd.release_all()
    time.sleep(0.5)
    layout.write('\n')
    time.sleep(1.0)
    layout.write('$fslabel="CIRCUITPY"\n')
    layout.write('$fs=(Get-Volume -FileSystemLabel $fslabel).DriveLetter; Set-Location $fs":"\n')
import board
import time
import digitalio
import neopixel
import usb_hid 
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
kbd = Keyboard(usb_hid.devices)
m = Mouse(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)
mousemode = 0
cycle = 0
pixel.fill((255,0,0))
time.sleep(.5)
pixel.fill((0,255,0))
time.sleep(.5)
pixel.fill((0,0,255))
time.sleep(.5)
pixel.fill((255,255,255))
time.sleep(.5)


while True:
    if mousemode == 1:
        pixel.fill((0,0,2))
        cycle+=1
        if cycle > 1000 * jigglesec:
            pixel.fill((2,2,2))
            m.move(-10,0,0)
            time.sleep(0.5)
            m.move(10,0,0)
            cycle = 0
    else:
        pixel.fill((0,2,0))        
    if not button.value:
        pixel.fill((2,2,0))
        time.sleep(1.0)
        if not button.value:
            inject()
            mousemode = 1 # hack to turn off mouse jiggler upon inject...
        if mousemode == 1:
	        mousemode = 0
        else: 
            mousemode = 1
