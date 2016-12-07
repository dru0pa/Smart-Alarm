import vlc


url="http://13873.live.streamtheworld.com:443/FM947_SC"
i=vlc.Instance()
p=i.media_player_new()
m=i.media_new(url)
p.set_media(m)
m.release()
p.play()

