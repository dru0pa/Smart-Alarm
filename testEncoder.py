import time
import gaugette.gpio
import gaugette.rotary_encoder
A_PIN = 4
B_PIN = 5
gpio = gaugette.gpio.GPIO()
encoder = gaugette.rotary_encoder.RotaryEncoder(gpio, A_PIN, B_PIN)
encoder.start()
while True:
    delta = encoder.get_cycles()
    if delta != 0:
        print "rotate %d" % delta
    else:
        time.sleep(0.1)