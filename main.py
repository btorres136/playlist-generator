import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from savify.savify import Savify
from savify.savify.utils import PathHolder
from savify.savify.logger import Logger
from database import database
from pyyoutube import Api
import os

load_dotenv()
database = database()
database.init_db()

scope = "user-follow-read user-top-read playlist-read-collaborative playlist-read-private user-library-read"

client_id = os.environ['SPOTIPY_CLIENT_ID']
client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
yt_api_key = os.environ['YT_API_KEY']
yt_api = Api(api_key=yt_api_key)

logger = Logger(log_location='./savify_logs', log_level=None) # Silent output

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
s = Savify(spotify_obj=sp, path_holder=PathHolder(downloads_path="../music"), logger=logger)
s_yt = Savify(spotify_obj=sp, path_holder=PathHolder(downloads_path="../music/podcasts/yt"), logger=logger, yt_api=yt_api)

def download_saved_tracks():
  offset = 0
  user_tracks = sp.current_user_saved_tracks(limit=50)
  while len(user_tracks["items"]) != 0:
    user_tracks = sp.current_user_saved_tracks(limit=50, offset=offset)
    for tracks in user_tracks["items"]:
      print(tracks)
    offset += 1

def download_saved_albums():
  offset = 0
  albums = sp.current_user_saved_albums(limit=50)
  while len(albums["items"]) != 0:
    albums = sp.current_user_saved_albums(limit=50, offset=offset)
    for album in albums["items"]:
      for tracks in sp.album_tracks(album["album"]["external_urls"]["spotify"])["items"]:
        artists_array = []
        for artist in tracks["artists"]:
          artists_array.append(artist["id"])
          database.add_new_artist(artist["id"], artist["name"])
        if database.add_new_song(tracks["id"],tracks["name"], artists_array[0], True) is None:
          s.download(tracks["external_urls"]["spotify"])
    offset += 1

def download_recommendations():

  user_follow = sp.current_user_followed_artists()
  recommendations = []

  for artist in user_follow["artists"]["items"]:
    recommendations.append(sp.recommendations(seed_artists=[artist["id"]], limit=100))
    recommendations.append(sp.artist_top_tracks(artist_id=artist["id"]))
      
  for recommendation in recommendations:
    for track in recommendation['tracks']:
      artists_array = []
      for artist in track["artists"]:
        artists_array.append(artist["id"])
        database.add_new_artist(artist["id"], artist["name"])
      if database.add_new_song(track["id"],track["name"], artists_array[0], True) is None:
        s.download(track["external_urls"]["spotify"])

def download_youtube_videos():
  videos = yt_api.search(channel_id="UCmxXHRqQMb7T6aqla9wJHNg", limit=20).to_dict()
  for video in videos["items"]:
    try:
      print("Downloading from youtube: "+video["snippet"]["title"])
      s_yt.download("http://www.youtube.com/watch?v="+video["id"]["videoId"])
    except KeyboardInterrupt:
      exit()
    except:
      print("Something went wrong!")
    
download_saved_albums()
download_saved_tracks()
#download_recommendations()
download_youtube_videos()
