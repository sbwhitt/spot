import spotipy
import spotipy.util as util
from config import *
from playlists import *

client_id = SPOTIPY_CLIENT_ID
client_secret = SPOTIPY_CLIENT_SECRET
redirect_url = SPOTIPY_REDIRECT_URI

scope = 'playlist-read-private'

username = input('enter spotify username: ')

token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, 
    redirect_uri=redirect_url)

spot = spotipy.Spotify(auth=token)

p = playlists(spot, username)
p.show_graph()
