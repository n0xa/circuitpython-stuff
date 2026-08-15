# boot.py for "stealth HID mode" on the Trinkey QT2040
# if copied to the root folder, will flash yellow for a few
# seconds after boot. Tap the button during this phase and
# the CircuitPy drive, serial and other interfaces will show
# up. Otherwise, this device will only surface HID interfaces
import time
import board
import neopixel
import storage
import usb_cdc
import usb_hid
import usb_midi
from digitalio import DigitalInOut, Direction, Pull

BLINK_SECONDS = 4
BLINK_INTERVAL = 0.25
YELLOW = (255, 220, 0) 
GREEN = (0, 30, 0)
OFF = (0, 0, 0)

button = DigitalInOut(board.BUTTON)
button.direction = Direction.INPUT
button.pull = Pull.UP  # button pulls low when pressed

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

drive_enabled = False
elapsed = 0.0
blink_state = False

while elapsed < BLINK_SECONDS:
    blink_state = not blink_state
    pixel.fill(YELLOW if blink_state else OFF)
    time.sleep(BLINK_INTERVAL)
    elapsed += BLINK_INTERVAL
    if not button.value:
        drive_enabled = True
        break

pixel.fill(GREEN if drive_enabled else OFF)
time.sleep(0.3) 

print("Drive enabled:", drive_enabled)
if not drive_enabled:
    storage.disable_usb_drive()
    usb_cdc.disable()
    usb_midi.disable()

button.deinit()
pixel.deinit() 

usb_hid.enable((usb_hid.Device.KEYBOARD, usb_hid.Device.MOUSE))
