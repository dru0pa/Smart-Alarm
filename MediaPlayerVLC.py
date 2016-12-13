import time
import vlc
import Settings
import subprocess
import logging

log = logging.getLogger('root')

PANIC_ALARM = 'play.mp3'
FX_DIRECTORY = 'Sounds/'

global flag
flag = 1

class MediaPlayer:
    def __init__(self):
        self.settings = Settings.Settings()
        self.player = False
        self.effect = False

    def playerActive(self):
        return self.player != False

    def soundAlarm(self, alarmThread):
        log.info("Playing alarm")
        self.playStation()
        log.debug("Alarm process opened")

        # Wait a few seconds and see if the mplayer instance is still running
        time.sleep(self.settings.getInt('radio_delay'))

        if alarmThread.isSnoozing() or alarmThread.getNextAlarm() is None:
            # We've snoozed or cancelled the alarm, so no need to check for player
            log.debug("Media player senses alarm already cancelled/snoozed, so not checking for mplayer instance")
            return

        # Fetch the number of mplayer processes running
        processes = subprocess.Popen('ps aux | grep vlc | egrep -v "grep" | wc -l',
                                     stdout=subprocess.PIPE,
                                     shell=True
                                     )
        num = int(processes.stdout.read())

        if num < 1 and self.player is not False:
            log.error("Could not find mplayer instance, playing panic alarm")
            self.stopPlayer()
            time.sleep(2)
            self.playMedia(PANIC_ALARM, 0)



    def playStation(self, station=-1):

        def end_reached(self):


             print("End reached!")

        if station == -1:
            station = self.settings.getInt('station')

        station = Settings.STATIONS[station]

        log.info("Playing station %s", station['name'])
        self.i = vlc.Instance()  # Create VLC instance
        self.p = self.i.media_player_new()  # Create new media player
        self.event_manager = self.p.event_manager()  # Attach event to player (next 3 lines)
        self.event = vlc.EventType()
        self.event_manager.event_attach(self.event.MediaPlayerEndReached, end_reached)
        self.m = self.i.media_new('http://13873.live.streamtheworld.com:443/FM947_SC')  # Create new media
        self.p.set_media(self.m)  # Set URL as the player's media
        self.m.release()
        self.p.play()  # play it
        self.p.play.loop = 0

    def playMedia(self, file, loop=-1):

        def end_reached(self):
            print("End reached!")

        log.info("Playing file %s", file)
        self.i = vlc.Instance()  # Create VLC instance
        self.m = self.i.media_new('PANIC_ALARM')  # Create new media
        self.event_manager = self.p.event_manager()  # Attach event to player (next 3 lines)
        self.event = vlc.EventType()
        self.event_manager.event_attach(self.event.MediaPlayerEndReached, end_reached)
        self.p.set_media(self.m)  # Set URL as the player's media
        self.m.release()
        self.p.play()  # play it
        self.p.play.loop = loop


    # Play some speech. None-blocking equivalent of playSpeech, which also pays attention to sfx_enabled setting
    def playVoice(self, text):
        if self.settings.get('sfx_enabled') == 0:
            # We've got sound effects disabled, so skip
            log.info("Sound effects disabled, not playing voice")
            return
        path = self.settings.get("tts_path");
        log.info("Playing voice: '%s' through `%s`" % (text, path))
        play = subprocess.Popen('echo "%s" | %s' % (text, path), shell=True)

    # Play some speech. Warning: Blocks until we're done speaking
    def playSpeech(self, text):
        path = self.settings.get("tts_path");
        log.info("Playing speech: '%s' through `%s`" % (text, path))
        play = subprocess.Popen('echo "%s" | %s' % (text, path), shell=True)
        play.wait()

    def stopPlayer(self):
        #if self.player:
        #    self.player.quit()
        #    self.player = False
        #    log.info("Player process terminated")
        if self.player:
             self.stopPlayer()
             self.player = False
             log.info("Player process terminated")
