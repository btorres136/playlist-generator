import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from music_table import Music, Base
import os

class database():
  def __init__(self) -> None:
    Session = 0

  def init_db(self) -> None:
    try:
      user = os.environ['POSTGRES_USER']
      passwd = os.environ['POSTGRES_PASSWD']
      db = os.environ['POSTGRES_DB']
      host = os.environ['POSTGRES_HOST']
    except KeyError as err:
      print(f"Given key not found - {err}")

    engine = create_engine('postgresql+psycopg2://'+user+':'+passwd+'@'+host+'/'+db)
    self.Session = sessionmaker(bind=engine)()
    Base.metadata.create_all(engine)

  def add_new_song(self, r_id, r_name, r_artist, r_keep):
    exist = self.Session.query(Music).filter_by(id=r_id).first()
    if exist is None:
      print("Adding: "+r_name+" by: "+r_artist)
      song = Music(r_id,r_name,r_artist, r_keep)
      self.Session.add(song)
      self.Session.commit()
    return exist
  
  def get_session(self):
    return self.Session
