############## Flip the slide switch on (to the right 
############## if the USB port is pointing away from you)
############## to start ripping through all the codes.
############## Slide it to off to pause the TV-B-Gone.

############## The magic sequences are in CODES.JSON.

############## Lots of this was borrowed from, with heavy
############## modifications, this blog post on digi-key
# https://www.digikey.com/en/maker/projects/circuit-python-tv-zapper-with-circuit-playground-express/643fe3dad81e43518e99ecaede92a856


import board
import array
import time
from digitalio import DigitalInOut, Direction, Pull
import pwmio
import pulseio

############## Switch to enable TV-B-Gone
switch = DigitalInOut(board.SLIDE_SWITCH)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

# Button to see output debug
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

############## Speaker as haptic feedback
spkr_en = DigitalInOut(board.SPEAKER_ENABLE)
spkr_en.direction = Direction.OUTPUT
spkr_en.value = True
spkr = DigitalInOut(board.SPEAKER)
spkr.direction = Direction.OUTPUT

############## Allow any button to trigger activity!
button_a = DigitalInOut(board.BUTTON_A)
button_a.direction = Direction.INPUT
button_a.pull = Pull.DOWN
button_b = DigitalInOut(board.BUTTON_B)
button_b.direction = Direction.INPUT
button_b.pull = Pull.DOWN

pwm = pwmio.PWMOut(board.REMOTEOUT, frequency=38000, duty_cycle=2 ** 15, variable_frequency=True)
pulse = pulseio.PulseOut(pwm)

while True:
    f = open("/codes.json", "r")
    for line in f:
        while switch.value:
            pass
        print("ping")
        code = eval(line)
        print(code)
        print(code['freq'])
        led.value = True
        # If this is a repeating code, extract details
        try:
            repeat = code['repeat']
            delay = code['repeat_delay']
        except KeyError:   # by default, repeat once only!
            repeat = 1
            delay = 0
        # The table holds the on/off pairs
        table = code['table']
        pulses = []  # store the pulses here
        # Read through each indexed element
        for i in code['index']:
            pulses += table[i]  # and add to the list of pulses
        pulses.pop()  # remove one final 'low' pulse
        # Firin mah lazor
        for i in range(repeat):
            pulse.send(array.array('H', pulses))
            time.sleep(delay)
        led.value = False
        spkr.value = False
        time.sleep(code['delay'])     
        if (button_a.value or button_b.value):
            break
    f.close()
