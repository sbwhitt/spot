import spotipy
import spotipy.util as util
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from config import *

class playlists:
    def __init__(self, username):
        scope = 'playlist-read-private'
        token = util.prompt_for_user_token(username, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, 
            redirect_uri=SPOTIPY_REDIRECT_URI)
        self.spot = spotipy.Spotify(auth=token)

        self.username = username
        self.user_playlists_raw = self.spot.user_playlists(self.username, limit=50, offset=0)

    def show_graphs(self):
        plt.show()

    #combined graph of both tracks and popularity average of user playlists
    def build_tracks_popularity_graph(self):
        tracks = self.__sort_alpha(self.__get_tracks_per_playlist())
        pop = self.__sort_alpha(self.__get_popularity_per_playlist())

        spaces = np.arange(len(tracks[0]))
        width = 0.35

        fig, chart = plt.subplots()

        chart.bar(spaces-width/2, tracks[1], width=width, label="tracks in playlist")
        chart.bar(spaces+width/2, pop[1], width=width, label="popularity average (0-100)")

        chart.set_xticks(spaces)
        chart.set_xticklabels(tracks[0])
        chart.legend()

        plt.draw()
    
    #graph of user playlists ordered by number of tracks
    def build_tracks_graph(self):
        tracks = self.__sort_numeric(self.__get_tracks_per_playlist())
        playlist_names = tracks[0]
        track_values = tracks[1]
        
        fig, chart = plt.subplots()
        chart.bar(playlist_names, track_values)
        chart.set_title("number of tracks per playlist")
        plt.draw()
    
    #graph of playlists versus playlist popularity averages
    def build_popularity_graph(self):
        tracks = self.__sort_numeric(self.__get_popularity_per_playlist())
        playlist_names = tracks[0]
        pop_values = tracks[1]
        
        fig, chart = plt.subplots()
        chart.bar(playlist_names, pop_values)
        chart.set_title("average popularity per playlist (0-100)")
        plt.draw()

    def __get_tracks_per_playlist(self):
        user_playlists = self.__parse_user_playlists()

        playlist_names = []
        playlist_tracks = []

        for p in user_playlists:
            playlist_names.append(p[0])
            playlist_tracks.append(p[1])
        
        return [playlist_names, playlist_tracks]

    def __parse_user_playlists(self):
        user_playlists = []
        
        for i, playlist in enumerate(self.user_playlists_raw['items']):
            if playlist['owner']['display_name'] == self.username:
                user_playlists.append([str(playlist['name']), playlist['tracks']['total']])

        return user_playlists

    def __get_popularity_per_playlist(self):
        pop_averages = []

        for i, playlist in enumerate(self.user_playlists_raw['items']):
            if playlist['owner']['display_name'] == self.username:
                pop_avg = self.__get_playlist_popularity_average(playlist)
                pop_averages.append([playlist['name'], pop_avg])

        playlist_names = []
        pop_avg_values = []

        for playlist in pop_averages:
            playlist_names.append(playlist[0])
            pop_avg_values.append(playlist[1])

        return [playlist_names, pop_avg_values]

    def __get_playlist_popularity_average(self, target_playlist):
        total_pop = 0

        tracks = self.spot.user_playlist(self.username, target_playlist['id'], fields="tracks,next")['tracks']['items']
        for track in tracks:
            total_pop += track['track']['popularity']
        
        num_tracks = target_playlist['tracks']['total']
        return round(total_pop/num_tracks)

    def __sort_alpha(self, array):
        alpha = array[0]
        numeric = array[1]

        combined = []
        for i in range(len(alpha)):
            combined.append([alpha[i], numeric[i]])
        
        combined.sort(key=lambda x: x[0])
        alpha = []
        numeric = []
        for p in combined:
            alpha.append(p[0])
            numeric.append(p[1])
        
        return [alpha, numeric]

    def __sort_numeric(self, array):
        alpha = array[0]
        numeric = array[1]

        combined = []
        for i in range(len(alpha)):
            combined.append([alpha[i], numeric[i]])
        
        combined.sort(key=lambda x: x[1])
        alpha = []
        numeric = []
        for p in combined:
            alpha.append(p[0])
            numeric.append(p[1])
        
        return [alpha, numeric]
