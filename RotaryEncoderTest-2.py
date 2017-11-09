import time
import gaugette.gpio
import gaugette.rotary_encoder

A_PIN = 5
B_PIN = 6

gp_io = gaugette.gpio.GPIO()
encoder = gaugette.rotary_encoder.RotaryEncoder(gp_io, A_PIN, B_PIN)
encoder.start()
print "A"
while True:
    delta = encoder.get_cycles()
    print "B"
    if delta != 0:
        print "rotate %d" % delta
    else:
        time.sleep(0.1)