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

        self.username = username
        self.user_playlists_raw = self.spot.user_playlists(self.username, limit=50, offset=0)

    def show_graphs(self):
        self.__show_popularity_per_playlist()
        self.__show_tracks_per_playlist()

        plt.show()

    #graph of user playlists ordered by number of tracks
    def __show_tracks_per_playlist(self):
        user_playlists = self.__parse_user_playlists()

        playlistNames = []
        playlistSongs = []

        for p in user_playlists:
            playlistNames.append(p[0])
            playlistSongs.append(p[1])

        fig, chart = plt.subplots()
        chart.set_title("user created playlists ordered by number of tracks")
        chart.bar(playlistNames, playlistSongs)
        plt.draw()

    def __parse_user_playlists(self):
        user_playlists = []
        
        for i, playlist in enumerate(self.user_playlists_raw['items']):
            if playlist['owner']['display_name'] == self.username:
                user_playlists.append([str(playlist['name']), playlist['tracks']['total']])

        user_playlists.sort(key=lambda k: k[1], reverse=True)
        return user_playlists

    #graph of playlists versus playlist popularity averages
    def __show_popularity_per_playlist(self):
        pop_averages = []

        for i, playlist in enumerate(self.user_playlists_raw['items']):
            if playlist['owner']['display_name'] == self.username:
                pop_avg = self.__get_playlist_popularity_average(playlist)
                if pop_avg != 0:
                    pop_averages.append([playlist['name'], pop_avg])

        pop_averages.sort(key=lambda p: p[1], reverse=True)

        playlist_names = []
        pop_avg_values = []

        for playlist in pop_averages:
            playlist_names.append(playlist[0])
            pop_avg_values.append(playlist[1])
        
        fig, chart = plt.subplots()
        chart.set_title("playlists versus playlist popularity average (0-100)")
        chart.bar(playlist_names, pop_avg_values)
        plt.draw()

    def __get_playlist_popularity_average(self, target_playlist):
        total_pop = 0

        tracks = self.spot.user_playlist(self.username, target_playlist['id'], fields="tracks,next")['tracks']['items']
        for track in tracks:
            total_pop += track['track']['popularity']
        
        num_tracks = target_playlist['tracks']['total']
        return round(total_pop/num_tracks)
