import os
import board
from digitalio import DigitalInOut, Direction
import time
import touchio

# Set this to True to turn the touchpads into a keyboard
ENABLE_KEYBOARD = False

WINDOWS = "W"
MAC = "M"
LINUX = "L"  # and Chrome OS

# Set your computer type to one of the above
OS = WINDOWS

# Used if we do HID output, see below
if ENABLE_KEYBOARD:
    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)

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
            if OS == WINDOWS:
                type_alt_code(234)
            elif OS == MAC:
                kbd.send(Keycode.ALT, Keycode.Z)
            elif OS == LINUX:
                kbd.press(Keycode.CONTROL, Keycode.SHIFT)
                kbd.press(Keycode.U)
                kbd.release_all()
                kbd.send(Keycode.TWO)
                kbd.send(Keycode.ONE)
                kbd.send(Keycode.TWO)
                kbd.send(Keycode.SIX)
                kbd.send(Keycode.ENTER)
    if caps[1]:
        if ENABLE_KEYBOARD:
            if OS == WINDOWS:
                type_alt_code(230)
            elif OS == MAC:
                kbd.send(Keycode.ALT, Keycode.M)
            elif OS == LINUX:
                kbd.press(Keycode.CONTROL, Keycode.SHIFT)
                kbd.press(Keycode.U)
                kbd.release_all()
                kbd.send(Keycode.ZERO)
                kbd.send(Keycode.THREE)
                kbd.send(Keycode.B)
                kbd.send(Keycode.C)
                kbd.send(Keycode.ENTER)
    if caps[2]:
        if ENABLE_KEYBOARD:
            if OS == WINDOWS:
                type_alt_code(227)
            elif OS == MAC:
                kbd.send(Keycode.ALT, Keycode.P)
            elif OS == LINUX:
                kbd.press(Keycode.CONTROL, Keycode.SHIFT)
                kbd.press(Keycode.U)
                kbd.release_all()
                kbd.send(Keycode.ZERO)
                kbd.send(Keycode.THREE)
                kbd.send(Keycode.C)
                kbd.send(Keycode.ZERO)
                kbd.send(Keycode.ENTER)
    if caps[3]:
        if ENABLE_KEYBOARD:
            layout.write('https://www.digikey.com/python\n')
    time.sleep(0.1)
