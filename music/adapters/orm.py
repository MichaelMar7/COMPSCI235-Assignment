#from symbol import arith_expr
#from tkinter import N
#from colorama import Fore

from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey, column
)
from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.domainmodel.track import Track

metadata = MetaData()

users_table = Table(
    'users', metadata, 
    Column('id', Integer, primary_key=True, autoincrement=True),
    #Column('user_id', Integer, nullable=False),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)
reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track', ForeignKey('tracks.id')),
    Column('username', String(1024), nullable=False),
    Column('review', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False)
)
tracks_table = Table(
    'tracks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    #Column('track_id', Integer, nullable=False),
    Column('track_title', String(255), nullable=False),
    Column('artist_id', ForeignKey('artists.id')),
    Column('album_id', ForeignKey('albums.id')),
    Column('track_url', String(255), nullable=False),
    Column('track_duration', Integer, nullable=False)
)
artists_table = Table(
    'artists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    #Column('artist_id', Integer, nullable=False),
    Column('full_name', String(255), nullable=False)
)
genres_table = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    #Column('genre_id', Integer, nullable=False),
    Column('genre_name', String(255), nullable=False)
)
albums_table = Table(
    'albums', metadata, 
    Column('id', Integer, primary_key=True, autoincrement=True),
    #Column('album_id', Integer, nullable=False),
    Column('title', String(1024), nullable=False)
)

def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review, backred='_Review__user')
    })
    mapper(Review, reviews_table, properties={
        '_Review__review': reviews_table.c.review,
        '_Review__timestamp': reviews_table.c.timestamp
    })
    mapper(Track, tracks_table, properties={
        '_Track__track_id': tracks_table.c.id,
        '_Track__track_title': tracks_table.c.track_title,
        #'_Track__review': relationship(Review, backref='_Review__track')
    })
    mapper(Artist, artists_table, properties={
        '_Artist__artist_id': artists_table.c.id,
        '_Artist__full_name': artists_table.c.full_name
    })
    mapper(Genre, genres_table, properties={
        '_Genre__genre_id': genres_table.c.id,
        '_Genre__genre_name': genres_table.c.genre_name
    })
    mapper(Album, albums_table, properties={
        '_Album__album_id': albums_table.c.id,
        '_Album__title': albums_table.c.title
    })