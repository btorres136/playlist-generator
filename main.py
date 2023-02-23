#!/usr/bin/python3

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from savify.savify import Savify
from savify.savify.utils import PathHolder
from savify.savify.logger import Logger
from savify.savify.types import *
from pyyoutube import Api
import os

load_dotenv()

scope = "user-follow-read user-top-read playlist-read-collaborative playlist-read-private user-library-read"

client_id = os.environ['SPOTIPY_CLIENT_ID']
client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
yt_api_key = os.environ['YT_API_KEY']
yt_api = Api(api_key=yt_api_key)

logger = Logger(log_location='./savify_logs', log_level=None) # Silent output

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
s = Savify(spotify_obj=sp, path_holder=PathHolder(downloads_path="../../music"), logger=logger)

def download_playlist():
  offset = 0
  user_playlist = sp.current_user_playlists(limit=50)
  while len(user_playlist["items"]) != 0:
    user_playlist = sp.current_user_playlists(limit=50,offset=offset)
    for playlist in user_playlist["items"]:
      s.download(playlist["external_urls"]["spotify"], query_type=Type.PLAYLIST, create_m3u=True)
    offset += 50 

def download_saved_tracks():
  offset = 0
  user_tracks = sp.current_user_saved_tracks(limit=50)
  while len(user_tracks["items"]) != 0:
    user_tracks = sp.current_user_saved_tracks(limit=50, offset=offset)
    for track in user_tracks["items"]:
      s.download(track["track"]["external_urls"]["spotify"])
    offset += 50

def download_saved_albums():
  offset = 0
  albums = sp.current_user_saved_albums(limit=50)
  while len(albums["items"]) != 0:
    albums = sp.current_user_saved_albums(limit=50, offset=offset)
    for data in albums["items"]:
      s.download(data["album"]["external_urls"]["spotify"], query_type= Type.ALBUM)
    offset += 50
 
download_saved_tracks()
download_playlist()
download_saved_albums()

s.cleanup()
