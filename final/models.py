from sqlalchemy import Column, Integer, String,ForeignKey,Table,DateTime
from sqlalchemy.orm import Session,relationship
from datetime import datetime

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, autoincrement=True)
    name  = Column(String )
    email = Column(String, unique = True )

    playlists = relationship("Playlist", back_populates="user")


track_playlist_association = Table(
    "track_playlist_association",
    Base.metadata,
    Column("track_id", String, ForeignKey("track_table.track_id")),
    Column("playlist_id", String, ForeignKey("playlist_table.playlist_id"))
)

class Playlist(Base):
    __tablename__ = "playlist_table"

    playlist_id = Column(String, primary_key= True )
    playlist_name = Column(String)
    description = Column(String )
    snapshot_id = Column(String)
    user_id = Column(Integer, ForeignKey("users.id") )
    tracks = relationship("Track", secondary=track_playlist_association, back_populates="playlists")
    images = relationship("Images", back_populates="playlists")
    user = relationship("User", back_populates="playlists")
    owner = relationship("Owner", back_populates="playlist")

class Track(Base):
    __tablename__ = "track_table"

    track_id = Column(String, primary_key= True )
    track_name = Column(String )
    album_name = Column(String )
    artist = Column(String )
    track_url = Column(String )
    playlists = relationship("Playlist", secondary=track_playlist_association, back_populates="tracks")

class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)

    playlist_id = Column(String, ForeignKey("playlist_table.playlist_id") )
    url = Column(String )
    height = Column(Integer )
    width = Column(Integer )

    playlists = relationship("Playlist", back_populates="images")

class Owner(Base):
    __tablename__ = "owner"

    owner_id = Column(String, primary_key= True )
    playlist_id = Column(String, ForeignKey("playlist_table.playlist_id") )
    url = Column(String )
    name = Column(String )

    playlist = relationship("Playlist", back_populates="owner")

