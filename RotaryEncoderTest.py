import gaugette.rotary_encoder
import gaugette.switch
import time
import gaugette.gpio
import gaugette.rotary_encoder

A_PIN = 5
B_PIN = 6

# A_PIN = 6
# B_PIN = 5

SW_PIN = 20


gp_io = gaugette.gpio.GPIO()
encoder = gaugette.rotary_encoder.RotaryEncoder(gp_io, A_PIN, B_PIN)
encoder.start()
switch = gaugette.switch.Switch(gp_io, SW_PIN)
last_state = None

while True:
    delta = encoder.get_cycles()
    if delta != 0:
        print "rotate %d" % delta

    sw_state = switch.get_state()
    if sw_state != last_state:
        print "switch %d" % sw_state
        last_state = sw_state