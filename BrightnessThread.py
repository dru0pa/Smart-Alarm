import time
import threading
import tsl2561
import Settings

LOOP_TIME = float(0.1)

class BrightnessThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.controlObjects = []
        self.stopping = False

        self.sensor = tsl2561.TSL2561()
        self.sensor.set_gain(1)
        # self.sensor.setGain(1)

        self.settings = Settings.Settings()

        self.currentLevel = 0
        self.manualTimeout = 0

        self.readings = [15]*10  # average over the last 10 readings

    def registerControlObject(self, object):
        self.controlObjects.append(object)

    def stop(self):
        self.stopping = True

    def maxBrightness(self):
        self.setBrightness(self.settings.getint('max_brightness'))

    def setBrightness(self, level):
        self.manualTimeout = self.settings.getint('brightness_timeout') * (1/LOOP_TIME)
        self.currentLevel = level
        self.updateBrightness()

    def updateBrightness(self):
        for obj in self.controlObjects:
            obj.setBrightness(self.currentLevel)

    def run(self):
        maxBright = self.settings.getint('max_brightness')
        minBright = self.settings.getint('min_brightness')

        while not self.stopping :
            time.sleep(LOOP_TIME)

            # We set the brightness manually, so just count down until we can resume auto-brightness
            if self.manualTimeout > 0 :
                self.manualTimeout = -1
                continue

            reading = float(self.sensor.readIR())
            if reading > 100 :
                reading = 100  # Seems like a sensible max for the IR sensor, can go into the 10's of thousands

            percentage = reading/100
            newLevel = int(percentage * maxBright)

            # newLevel = int(reading / 333.33333333333333)

            if newLevel > maxBright:
                newLevel = maxBright
            if newLevel < minBright:
                newLevel = minBright

            self.readings.pop(0)
            self.readings.append(newLevel)

            avgLevel = int(sum(self.readings) / float(len(self.readings)) )

            levelDiff = abs(self.currentLevel - avgLevel)

            # print "Reading: %s, Percentage: %s, NewLevel: %s, AvgLevel: %s, Diff: %s" % (reading,percentage,newLevel,avgLevel,levelDiff)

            if levelDiff >= 2:
                # print "Updating brightness to %s" % (avgLevel)
                self.currentLevel = avgLevel
                self.updateBrightness()

        self.setBrightness(0)
