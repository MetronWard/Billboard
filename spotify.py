import json
import shelve
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


class Spotify:

    def __init__(self):
        self.scope = 'playlist-modify-public'
        self.secrets = shelve.open('keys/api_keys')
        self.client_id = self.secrets['client_id']
        self.client_secret = self.secrets['client_secret']
        self.username = self.secrets['username']
        self.uri = self.secrets['redirect_uri']
        logging.debug('Spotify class created')

    def create_playlist(self, songs: list, name: str, public: bool) -> str:
        token = SpotifyOAuth(scope=self.scope,
                             username=self.username,
                             client_id=self.username,
                             redirect_uri=self.uri,
                             client_secret=self.client_secret)
        logging.debug(f'Token created:\nScope = {self.scope}\nUsername = {self.username}\nClient id = {self.client_id}\n'
                      f'Redirect uri = {self.uri}\nClient Secret = {self.client_secret}')
        spotify_object = spotipy.Spotify(auth_manager=token)
        playlist_name = name
        names = spotify_object.user_playlist_create(user=self.username, name=playlist_name, public=public)
        for song in songs:
            result = spotify_object.search(q=song)
            uri = [result['tracks']['items'][0]["uri"]]
            spotify_object.playlist_add_items(playlist_id=names["id"], items=uri)
        return names["external_urls"]["spotify"]


if __name__ == '__main__':
    bot = Spotify()
    get = bot.create_playlist(['Rap god', 'Angel Eyes'], 'Test run', True)
    print(get)
