import spotipy
import spotipy.util as util
from config import *
import matplotlib
import matplotlib.pyplot as plt

class top:
    def __init__(self, username):
        scope = 'user-top-read'
        token = util.prompt_for_user_token(username, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, 
            redirect_uri=SPOTIPY_REDIRECT_URI)
        self.spot = spotipy.Spotify(auth=token)
    
    def show_graphs(self):
        plt.show()

    def build_top_artist_graph(self, num_artists=10):
        artists = self.__parse_top_artists(50 if num_artists > 50 else num_artists)

        fig, chart = plt.subplots()
        
        chart.barh(artists[0], artists[1], label="top artist at bottom")
        chart.set_title("top artists by affinity versus artist popularity (0-100)")
        chart.legend()

        plt.draw()

    def __parse_top_artists(self, num_artists):
        user_top_artists = self.spot.current_user_top_artists(limit=num_artists)

        artist_names = []
        artist_popularities = []
        for artist in user_top_artists['items']:
            artist_names.append(artist['name'])
            artist_popularities.append(artist['popularity'])
        
        return [artist_names, artist_popularities]
