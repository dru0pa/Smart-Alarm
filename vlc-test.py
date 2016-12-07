import vlc
import time

url="http://13873.live.streamtheworld.com:443/FM947_SC"

def end_reached(self):
    global flag
    flag = 1
    print("End reached!")

i=vlc.Instance() #Create VLC instance
p=i.media_player_new() # Create new media player
event_manager = p.event_manager() # Attach event to player (next 3 lines)
event=vlc.EventType()
event_manager.event_attach(event.MediaPlayerEndReached, end_reached)
m=i.media_new(url) # Create new media
p.set_media(m) # Set URL as the player's media
m.release()
p.play() # play it

while flag == 0: # Wait until the end of the first media has been reached...
    time.sleep(0.5)
    print('Loading playlist...')

sub_list = m.subitems() # .. and get the sub itmes in the playlist
sub_list.lock()
sub = sub_list.item_at_index(0) # Get the first sub item
sub_list.unlock()
sub_list.release()
p.set_media(sub) # Set it as the new media in the player
p.play() # and play it
sub.release()
a = 0
while p.is_playing()==0: # This is just a counter that runs until the stream is actually being played
    time.sleep(0.5)
    a += 1
    print(a)
