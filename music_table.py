from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Music(Base):
    __tablename__ = 'music'

    id = Column(String, primary_key=True)
    name = Column(String)
    artist = Column(String)
    keep = Column(Boolean)

    def __init__(self, r_id, r_name, r_artist, r_keep):
      self.id = r_id
      self.name = r_name
      self.artist = r_artist
      self.keep = r_keep