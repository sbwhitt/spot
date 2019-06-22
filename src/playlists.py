import spotipy
import spotipy.util as util
from config import *
import matplotlib
import matplotlib.pyplot as plt
import math

class playlists:
    def __init__(self, username):
        scope = 'playlist-read-private'
        token = util.prompt_for_user_token(username, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, 
            redirect_uri=SPOTIPY_REDIRECT_URI)
        self.spot = spotipy.Spotify(auth=token)

        self.user_playlists = []
        self.username = username
        self.user_playlists_raw = self.spot.user_playlists(self.username, limit=50, offset=0)

        self.__parse_user_playlists()
    
    def __parse_user_playlists(self):
        for i, playlist in enumerate(self.user_playlists_raw['items']):
            #print(playlist)
            if playlist['owner']['display_name'] == self.username:
                self.user_playlists.append([str(playlist['name']), playlist['tracks']['total']])

        self.user_playlists.sort(key=lambda k: k[1], reverse=True)

    #graph of user playlists ordered by number of tracks
    def show_graph(self):
        playlistNames = []
        playlistSongs = []

        for p in self.user_playlists:
            playlistNames.append(p[0])
            playlistSongs.append(p[1])

        fig, chart = plt.subplots()
        chart.bar(playlistNames, playlistSongs)
        plt.show()

    def print_playlist_popularity_average(self, name):
        target_playlist = ""

        for i, playlist in enumerate(self.user_playlists_raw['items']):
            if playlist['name'] == name:
                target_playlist = playlist
                break
        
        if target_playlist == "":
            print("invalid playlist name")
            return
        
        num_tracks = 0
        total_pop = 0

        tracks = self.spot.user_playlist(self.username, target_playlist['id'], fields="tracks,next")['tracks']['items']
        for track in tracks:
            total_pop += track['track']['popularity']
        
        print("playlist " + name + " popularity average: " + str(math.floor(total_pop/num_tracks)))
