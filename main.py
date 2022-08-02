import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from savify.savify import Savify
from savify.savify.utils import PathHolder
from savify.savify.logger import Logger
from database import database
from music_table import Music
import os

load_dotenv()
database = database()
database.init_db()

scope = "user-follow-read user-top-read"

client_id = os.environ['SPOTIPY_CLIENT_ID']
client_secret = os.environ['SPOTIPY_CLIENT_SECRET']

logger = Logger(log_location='./savify_logs', log_level=None) # Silent output

s = Savify(api_credentials=(client_id, client_secret), path_holder=PathHolder(downloads_path="../music"), logger=logger)



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user_follow = sp.current_user_followed_artists()
recommendations = []
for artist in user_follow["artists"]["items"]:
  recommendations.append(sp.recommendations(seed_artists=[artist["id"]], limit=100))

for recommendation in recommendations:
  for track in recommendation['tracks']:
    artists_string = ''
    for artists in track["artists"]:
      artists_string += artists["name"]
    if database.add_new_song(track["id"],track["name"], artists_string, True) is None:
      s.download(track["external_urls"]["spotify"])