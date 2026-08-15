# import os
import board
from digitalio import DigitalInOut, Direction
import time
import touchio

# Set this to True to turn the touchpads into a keyboard
ENABLE_KEYBOARD = True

WINDOWS = "W"
MAC = "M"
LINUX = "L"  # and Chrome OS

# Set your computer type to one of the above
OS = WINDOWS

# Used if we do HID output, see below
if ENABLE_KEYBOARD:
    import usb_hid
    from adafruit_hid.mouse import Mouse
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
    mouse = Mouse(usb_hid. devices)
#print(dir(board), os.uname()) # Print a little about ourselves

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

touches = [DigitalInOut(board.CAP0)]
for p in (board.CAP1, board.CAP2, board.CAP3):
    touches.append(touchio.TouchIn(p))

leds = []
for p in (board.LED4, board.LED5, board.LED6, board.LED7):
    led = DigitalInOut(p)
    led.direction = Direction.OUTPUT
    led.value = True
    time.sleep(0.25)
    leds.append(led)
for led in leds:
    led.value = False


cap_touches = [False, False, False, False]
jiggle = False
jigglePeriod = 300
jiggleLast = 0

def read_caps():
    t0_count = 0
    t0 = touches[0]
    t0.direction = Direction.OUTPUT
    t0.value = True
    t0.direction = Direction.INPUT
    # funky idea but we can 'diy' the one non-hardware captouch device by hand
    # by reading the drooping voltage on a tri-state pin.
    t0_count = t0.value + t0.value + t0.value + t0.value + t0.value + \
               t0.value + t0.value + t0.value + t0.value + t0.value + \
               t0.value + t0.value + t0.value + t0.value + t0.value
    cap_touches[0] = t0_count > 2
    cap_touches[1] = touches[1].raw_value > 3000
    cap_touches[2] = touches[2].raw_value > 3000
    cap_touches[3] = touches[3].raw_value > 3000
    return cap_touches

def type_alt_code(code):
    kbd.press(Keycode.ALT)
    for c in str(code):
        if c == '0':
            keycode = Keycode.KEYPAD_ZERO
        elif '1' <= c <= '9':
            keycode = Keycode.KEYPAD_ONE + ord(c) - ord('1')
        else:
            raise RuntimeError("Only number codes permitted!")
        kbd.press(keycode)
        kbd.release(keycode)
    kbd.release_all()

while True:
    caps = read_caps()
    print(caps)
    # light up the matching LED
    for i,c in enumerate(caps):
        leds[i].value = c
    if caps[0]:
        if ENABLE_KEYBOARD:
            kbd.send(0xE3) # Windows Key           
            time.sleep(0.1)
            layout.write('https://www.youtube.com/watch?v=dQw4w9WgXcQ?autoplay=1&mute=1\n')
            time.sleep(1)
    if caps[1]:
        jiggle = not jiggle
        if not jiggle:
            leds[1].value = False
        if ENABLE_KEYBOARD:
            time.sleep(1)
    if caps[2]:
        if ENABLE_KEYBOARD:
            kbd.send(0xE3) # Windows Key           
            time.sleep(0.1)
            layout.write('https://www.youtube.com/watch?v=dQw4w9WgXcQ\n')
            time.sleep(1)
    if caps[3]:
        if ENABLE_KEYBOARD:
            kbd.send(0xE3) # Windows Key           
            time.sleep(0.1)
            layout.write('https://mhn.h-i-r.net/dash\n')
            time.sleep(1)

    # Mouse jiggler
    if jiggle:
        leds[1].value = True
        if time.monotonic() > jiggleLast + jigglePeriod:
            mouse.move(2, 0)
            time.sleep(0.1)
            mouse.move(-2, 0)
            jiggleLast = time.monotonic()
    else:
        leds[1].value = False

    time.sleep(0.1)
