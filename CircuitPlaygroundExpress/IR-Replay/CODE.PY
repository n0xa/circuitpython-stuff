########### Infrared replay proof of concept.
########### Very niche application. Needs work to be more useful
########### Tested on Samsung projector and TVs.
########### Specifically, pulseout frequency and header, one and zero
########### symbols passed to GenericTransmit() won't work on all IR devices
########### Reference the CODES.JSON in TV-B-Gone project for frequency and
########### symbol tables. These may help you reverse-engineer your own TV.
import time
import pulseio
import board
import adafruit_irremote
from adafruit_circuitplayground.express import cpx

pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
pulseout = pulseio.PulseOut(board.IR_TX, frequency=38338, duty_cycle=2 ** 15)
encoder = adafruit_irremote.GenericTransmit(header=[4460, 4500], one=[573, 567], zero=[573, 1680], trail=0)
while True:
    if cpx.button_a:
        print("Button A pressed! \n")
        cpx.red_led = True
        pulses = decoder.read_pulses(pulsein)
        received_code = decoder.decode_bits(pulses)
        print("Recording ", received_code)
        cpx.red_led = False
        # wait so the receiver can get the full message
        time.sleep(10)
    if cpx.button_b:
        print("Button B pressed! \n")
        cpx.red_led = True
        print("Replaying ", received_code)
        encoder.transmit(pulseout, received_code)
        cpx.red_led = False
        time.sleep(0.2)
