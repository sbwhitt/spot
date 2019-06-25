import playlists as play
import tracks as track
import top as tp
import json

#you will have to register a spotify app to get the proper credentials to make authenticated calls
#after inputing username, you will be redirected to a url, copy that url and paste into console to authenticate

#examples of retrieving graphed/printed info below, uncomment one object block and run this file to view results
#i recommend using only one object at a time, but can do both, will have to authenticate multiple times if you do

#must call build graph functions before finally calling show_graphs

username = input("enter spotify username: ")

'''
tracks = track.tracks(username)
tracks.print_user_tracks_info()
tracks.build_top_artists_graph()
tracks.show_graphs()
'''

'''
p = play.playlists(username)
p.build_tracks_popularity_graph()
p.build_tracks_graph()
p.build_popularity_graph()
p.show_graphs()
'''


t = tp.top(username)
#t.build_top_artist_graph(25)
#t.build_top_tracks_graph(25)
t.build_top_genres_graph()
t.show_graphs()

