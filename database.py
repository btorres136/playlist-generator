from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Music, Artist, Base
import os

class database():
  def __init__(self) -> None:
    Session = 0

  def init_db(self) -> None:
    engine = create_engine('sqlite:///db.sqllite')
    self.Session = sessionmaker(bind=engine)()
    Base.metadata.create_all(engine)

  def add_new_song(self, r_id, r_name, r_artist, r_keep):
    exist = self.Session.query(Music).filter_by(id=r_id).first()
    if exist is None:
      print("Adding song: "+r_name)
      song = Music(r_id,r_name,r_artist, r_keep)
      self.Session.add(song)
      self.Session.commit()
    return exist
  
  def add_new_artist(self, r_id, r_name):
    exist = self.Session.query(Artist).filter_by(id=r_id).first()
    if exist is None:
      print("Adding artist: "+r_name)
      artist = Artist(r_id,r_name)
      self.Session.add(artist)
      self.Session.commit()
    return exist
  
  def get_session(self):
    return self.Session
