# boot.py for "stealth HID mode" on the Adafruit PyRuler
# if copied to the root folder, will flash an LED for a few
# seconds after boot. Tap the capacitive touch pad associated
# with the flashing LED during this phase and the CircuitPy
# drive, serial and other interfaces will show up. Otherwise,
# this device will only surface HID interfaces
import time
import board
import touchio
import storage
import usb_cdc
import usb_hid
import usb_midi
from digitalio import DigitalInOut, Direction

BLINK_SECONDS = 4
BLINK_INTERVAL = 0.25
TOUCH_THRESHOLD = 3000  # same threshold code.py already uses for CAP1-3

touch = touchio.TouchIn(board.CAP1)
led = DigitalInOut(board.LED5)  # LED5 is CAP1's LED
led.direction = Direction.OUTPUT

drive_enabled = False
elapsed = 0.0
blink_state = False

while elapsed < BLINK_SECONDS:
    blink_state = not blink_state
    led.value = blink_state
    time.sleep(BLINK_INTERVAL)
    elapsed += BLINK_INTERVAL
    if touch.raw_value > TOUCH_THRESHOLD:
        drive_enabled = True
        break

led.value = drive_enabled  
time.sleep(0.3)            

print("Drive enabled:", drive_enabled)
if not drive_enabled:
    storage.disable_usb_drive()
    usb_cdc.disable()
    usb_midi.disable()

touch.deinit()
led.deinit()  # release LED5 so code.py's DigitalInOut(board.LED5) doesn't collide

usb_hid.enable((usb_hid.Device.KEYBOARD, usb_hid.Device.MOUSE))
