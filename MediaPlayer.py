import time
import subprocess
import logging
import Settings
import os

from mplayer import Player

log = logging.getLogger('root')

PANIC_ALARM = '/home/pi/PycharmProjects/AlarmPi/play.mp3'
FX_DIRECTORY = '/home/pi/PycharmProjects/AlarmPi/sounds/'


class MediaPlayer:
    def __init__(self):
        self.settings = Settings.Settings()
        self.player = False
        self.effect = False

    @property
    def playerActive(self):
        if self.player != False:
            return True
        else:
            return False

    def soundAlarm(self, alarmThread):
        log.info("Playing alarm")
        self.playStation()
        log.debug("Verifying Radio is playing")

        # Wait a few seconds and see if the mplayer instance is still running
        time.sleep(self.settings.getInt('radio_delay'))

        if alarmThread.isSnoozing() or alarmThread.getNextAlarm() is None:
            # We've snoozed or cancelled the alarm, so no need to check for player
            log.debug("Media player senses alarm already cancelled/snoozed, so not checking for mplayer instance")
            return

        # Fetch the number of mplayer processes running
        log.debug("Checking process")
        processes = subprocess.Popen('ps aux | grep vlc | egrep -v "grep" | wc -l', stdout=subprocess.PIPE, shell=True)
        num = int(processes.stdout.read())

        if num < 2 and self.player is not False:
            log.error("Radio fail: Could not find mplayer instance, playing panic alarm")
            self.stopPlayer()
            time.sleep(2)
            self.playMedia(PANIC_ALARM)
        else:
            log.debug("Is playing")

    def playStation(self, station=-1):
        if station == -1:
            station = self.settings.getInt('station')

        station = Settings.STATIONS[station]

        #log.info("Playing station %s", station['name'])
        #self.player = Player()
        #self.player.loadlist(station['url'])
        #self.player.loop = 0

        log.debug("playStation: %s", station['name'])
        os.system("python /home/pi/PycharmProjects/AlarmPi/Media-Radio-VLC.py")
        log.info("Playing station 702")

    def playMedia(self, file, loop=-1):
        log.info("playMedia: Playing file %s", file)
        #self.player = Player()
        #self.player.loadfile(file)
        #self.player.loop = loop

        os.system("mplayer %s", file)
        os.system("python /home/pi/PycharmProjects/AlarmPi/Media-Radio-MP3.py")

    def playVoice(self, text):
        # log.debug("playVoice (non-blocking): {0}".format(text))
        if self.settings.get('sfx_enabled') == 0:
            # We've got sound effects disabled, so skip
            log.info("Sound effects disabled, not playing voice")
            return
        path = self.settings.get("tts_path");
        log.info("Playing voice: '%s'" % (text))
        play = subprocess.Popen('echo "%s" | %s' % (text, path), shell=True)

    def playSpeech(self, text):
        path = self.settings.get("tts_path");
        log.info("Playing speech: '%s' through `%s`" % (text, path))
        play = subprocess.Popen('echo "%s" | %s' % (text, path), shell=True)
        play.wait()

    def stopPlayer(self):
        log.debug("stopPlayer: ")
        if self.player:
            self.player.quit()
            self.player = False
            os.system("sudo killall cvlv")
            log.info("Player process terminated")