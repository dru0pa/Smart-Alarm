import threading
import time
import RPi.GPIO as GPIO

class Button(threading.Thread):
    """A thread that monitors a GPIO button"""

    def __init__(self, channel):
        threading.Thread.__init__(self)
        self._pressed = False
        self.channel = channel

        # set up pin as input
        GPIO.setup(self.channel, GPIO.IN)

        # terminate this thread when main program finishes
        self.daemon = True

        # start thread running
        self.start()

    def pressed(self):
        if self._pressed:
            # clear the pressed flag now we have detected it
            self._pressed = False
            return True
        else:
            return False

    def run(self):
        previous = None
        while 1:
            # read GPIO channel
            current = GPIO.input(self.channel)
            time.sleep(0.01) # wait 10 ms

            # detect change from 1 to 0 (a button press)
            if previous == True and current == False:
                self._pressed = True

                # wait for flag to be cleared
                while self._pressed:
                    time.sleep(0.05) # wait 50 ms

            previous = current

def onButtonPress():
    print('Button has been pressed!')

# specify board pin numbering convention
GPIO.setmode(GPIO.BOARD)

# create a button thread for a button on pin 11
button = Button(20)

while True:
    # ask for a name and say hello
    name = input('Enter a name (or Q to quit): ')
    if name.upper() == 'Q':
        break
    print('Hello', name)

    # check if button has been pressed in the meantime
    if button.pressed():
        onButtonPress()

GPIO.cleanup()