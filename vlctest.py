import vlc
import time

instance = vlc.Instance()

#Create a MediaPlayer with the default instance
player = instance.media_player_new()

#Load the media file
media = instance.media_new('http://13873.live.streamtheworld.com:443/FM947_SC')

#Add the media to the player
player.set_media(media)

#Play for 10 seconds then exit
player.play()
time.sleep(30)

#set the player position to be 50% in
#player.set_position(50)

#Reduce the volume to 70%
player.audio_set_volume(70)

#Build vlc option string
#options = 'sout=#duplicate{dst=rtp{access=udp,mux=ts,dst=224.0.0.1,port=1233},dst=display}'

#Load media with streaming options
#media = instance.media_new('play.mp3', options)

#player.play()

#http://13873.live.streamtheworld.com:443/FM947_SC

