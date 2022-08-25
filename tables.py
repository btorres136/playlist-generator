from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()

class Artist(Base):
  __tablename__ = 'artist'
  id = Column(String, primary_key=True)
  name = Column(String)

  def __init__(self, r_id, r_name):
    self.id = r_id
    self.name = r_name

class Music(Base):
  __tablename__ = 'music'

  id = Column(String, primary_key=True)
  name = Column(String)
  artist_id = Column(String, ForeignKey(Artist.id))
  keep = Column(Boolean)
    
  artist = relationship('Artist', foreign_keys='Music.artist_id')

  def __init__(self, r_id, r_name, r_artist, r_keep):
    self.id = r_id
    self.name = r_name
    self.artist_id = r_artist
    self.keep = r_keep

