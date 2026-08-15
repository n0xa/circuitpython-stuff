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

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

spk = pwmio.PWMOut(board.SPEAKER, frequency=120, duty_cycle=50)
#pwm = pwmio.PWMOut(board.IR_LED, frequency=38000, duty_cycle=2 ** 15, variable_frequency=True)
pulseout = pulseio.PulseOut(board.IR_LED, frequency=38000, duty_cycle=2 ** 15)

while True:
    f = open("/codes.json", "r")
    for line in f:
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
            pulseout.send(array.array('H', pulses))
            time.sleep(delay)
        #led.value = False
        time.sleep(code['delay'])     
    f.close()
