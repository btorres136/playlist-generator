from typing import Callable
from uuid import uuid1

from .types import Type, Platform
import unidecode


class Track:
    def try_with_key_error(self, name: str, getter: Callable, default: str = '') -> None:
        """Wraps a try-except-assign statement."""
        try:
            setattr(self, name, getter())
        except KeyError:
            setattr(self, name, default)

    def __init__(self, data, track_type=Type.TRACK, platform=Platform.SPOTIFY) -> None:
        self.album_track_count = None
        self.track_number = None
        self.release_date = None
        self.disc_number = None
        self.playlist = None
        self.name = None
        self.uri = None
        self.url = None
        self.id = None

        self.platform = platform
        self.track_type = track_type
        self._data = data
        if(platform == Platform.YOUTUBE):
            self.id = data["snippet"]["title"]
            self.album_name = data["snippet"]["channelTitle"] 
            self.artists = data["snippet"]["channelTitle"]
            self.url = "http://www.youtube.com/watch?v="+data["id"]
            self.name = data["snippet"]["title"]
            self.release_date = data["snippet"]["publishedAt"]
            self.cover_art_url = data["snippet"]["thumbnails"]["default"]["url"]
            self.uri = data["id"]
            self.album_track_count = '0'
            self.track_number = '0'
            self.disc_number = '0'
            self.playlist = '0'
        elif(platform == Platform.SPOTIFY):
            try:
                self.album_name = data['album']['name']
            except KeyError:
                try:
                    self.album_name = data['show']['name']
                except KeyError:
                    self.album_name = 'Unknown Show' if track_type == Type.EPISODE else 'Unknown Album'

            try:
                self.artists = _spotify_artist_names(data['artists'])
            except KeyError:
                try:
                    self.artists = [data['show']['publisher']]
                except KeyError:
                    self.artists = ['Unknown Publisher' if track_type == Type.EPISODE else 'Unknown Artist']

            try:
                self.cover_art_url = data['album']['images'][0]['url']
            except (KeyError, IndexError):
                try:
                    self.cover_art_url = data['images'][0]['url']
                except (KeyError, IndexError):
                    self.cover_art_url = 'https://developer.spotify.com/assets/branding-guidelines/icon3@2x.png'

            self.try_with_key_error("id",
                                    lambda: data['id'],
                                    default=str(uuid1()))

            self.try_with_key_error("name",
                                    lambda: data['name'],
                                    default='Unknown Episode' if track_type == Type.EPISODE else 'Unknown Song')

            self.try_with_key_error("url",
                                    lambda: data['external_urls']['spotify'])

            self.try_with_key_error("album_track_count",
                                    lambda: data['album']['total_tracks'])

            self.try_with_key_error("release_date",
                                    lambda: data['album']['release_date'])

            self.try_with_key_error("track_number",
                                    lambda: data['track_number'])

            self.try_with_key_error("disc_number",
                                    lambda: data['disc_number'])

            self.try_with_key_error("playlist",
                                    lambda: data['playlist'])

            self.try_with_key_error("uri",
                                    lambda: data['uri'])

    def __repr__(self) -> str:
        return f'{self.id}\nName: {self.name}\nArtists: {self.artists}\nAlbum: {self.album_name}\n' \
               f'Release Date: {self.release_date}\nTrack: {self.track_number} / {self.album_track_count}\n' \
               f'Disc: {self.disc_number}\nCover Art: {self.cover_art_url}\nLink: {self.url}\nUri: {self.uri}'

    def __str__(self) -> str:
        return f'{unidecode.unidecode(self.artists[0])} - {unidecode.unidecode(self.name)}'


def _spotify_artist_names(artist_data) -> list:
    try:
        return [artist['name'] for artist in artist_data]
    except KeyError:
        return ['Unknown Artist']
