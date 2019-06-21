import matplotlib
import matplotlib.pyplot as plt

class playlists:
    def __init__(self, spot, username):
        self.user_playlists = []
        self.username = username
        self.user_playlists_raw = spot.user_playlists(self.username, limit=50, offset=0)
    
    def __parse_user_playlists(self):
        for i, playlist in enumerate(self.user_playlists_raw['items']):
            if playlist['owner']['display_name'] == self.username:
                self.user_playlists.append([str(playlist['name']), playlist['tracks']['total']])

        self.user_playlists.sort(key=lambda k: k[1], reverse=False)

    def show_graph(self):
        self.__parse_user_playlists()

        playlistNames = []
        playlistSongs = []

        for p in self.user_playlists:
            playlistNames.append(p[0])
            playlistSongs.append(p[1])

        fig, chart = plt.subplots()
        chart.bar(playlistNames, playlistSongs)
        plt.show()
