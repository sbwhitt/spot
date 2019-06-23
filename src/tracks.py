import spotipy
import spotipy.util as util
from config import *
import matplotlib
import matplotlib.pyplot as plt
import operator

class tracks:
    def __init__(self, username):
        scope = 'user-library-read'
        token = util.prompt_for_user_token(username, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, 
            redirect_uri=SPOTIPY_REDIRECT_URI)
        spot = spotipy.Spotify(auth=token)

        self.user_artists = []
        self.user_tracks = []
        self.spot = spot
        self.username = username
        self.total_pop = 0

        self.__parse_user_tracks()

    def show_graphs(self):
        plt.show()

    #graph of most user saved tracks of top <num_artists> artists
    def build_top_artists_graph(self, num_artists=10):
        tracks_dict = {}
        for track in self.user_tracks:
            if tracks_dict.get(track[0]):
                tracks_dict[track[0]] = tracks_dict.get(track[0]) + 1
            else:
                tracks_dict[track[0]] = 1

        user_tracks_sorted = sorted(tracks_dict.items(), key=operator.itemgetter(1), reverse=True)
        
        artist_names = []
        num_artist_tracks = []

        for i in range(num_artists):
            track = user_tracks_sorted[i]
            artist_names.append(track[0])
            num_artist_tracks.append(track[1])

        fig, chart = plt.subplots()
        chart.barh(artist_names, num_artist_tracks)
        plt.draw()

    def __parse_user_tracks(self):
        track_offset = 0
        track_limit = 50

        while (True):
            next_tracks_raw = self.spot.current_user_saved_tracks(limit=track_limit, offset=track_offset)['items']
            if not next_tracks_raw:
                break
            
            for track in next_tracks_raw:
                self.user_tracks.append([
                    track['track']['artists'][0]['name'], 
                    track['track']['name'], 
                    track['track']['popularity']
                ])
                self.total_pop += track['track']['popularity']
            track_offset += track_limit

        return self.user_tracks
    
    def print_user_tracks_info(self):
        num_saved_tracks = len(self.user_tracks)

        print('total number of saved tracks: ' + str(num_saved_tracks))
        print('average popularity of saved tracks (from 0 to 100): ' + str(round(self.total_pop/num_saved_tracks)))
