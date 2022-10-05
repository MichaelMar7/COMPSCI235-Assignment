from datetime import date
from nntplib import ArticleInfo
from typing import List
from flask import session
from pytest import Session
from sqlalchemy import desc, asc

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.review import Review
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.adapters.repository import AbstractRepository

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.commit()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository):
    # Add missing methods
    def __init__(self, session_factory):
        self._session_context_manager = SessionContextManager(session_factory)
    
    def close_session(self):
        self._session_context_manager.close_current_session()

    def reset_session(self):
        self._session_context_manager.reset_session()

    def add_user(self, user: User):
        with self._session_context_manager as scm:
            scm.session.add(user)
            scm.commit()
        
    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_context_manager.session.query(User).filter(User.__user_name == user_name).one()
        except NoResultFound:
            pass 
        return user
    
    def add_track(self, track:Track):
        with self._session_context_manager as scm:
            scm.session.add(track)
            scm.commit()

    def add_album(self, album:Album):
        with self._session_context_manager as scm:
            scm.session.add(album)
            scm.commit()

    def get_track_by_id(self, id: int) -> Track:
        track = None
        try: 
            track = self._session_context_manager.session.query(Track).filter(Track._Track__track_id == id).one()
        except NoResultFound:
            pass
        return track

    def get_number_of_tracks(self):
        number_of_tracks = self._session_context_manager.session.query(Track).count()
        return number_of_tracks
    
    def get_album_by_id(self, album_id):
        album = None
        try:
            album = self._session_context_manager.session.query(Album).filter(Album._Album__album_id == album_id).one()
        except NoResultFound:
            pass 
        return album
    
    def get_number_of_albums(self):
        number_of_albums = self._session_context_manager.session.query(Album).count()
        return number_of_albums

    def get_artist(self, artist_name):
        artist = None
        try:
            artist = self._session_context_manager.session.query(Artist).filter(Artist._Artist__full_name == artist_name).one()
        except NoResultFound:
            pass
        return artist
    
    def get_genre(self, genre_name):
        genre = None
        try:
            genre = self._session_context_manager.session.query(Genre).filter(Genre._Genre__genre_name == genre_name).one()
        except NoResultFound:
            pass 
        return genre 

    #################
    # Track Methods #
    #################
    def get_tracks_by_id(self, id_list):
        tracks = self._session_context_manager.session.query(Track).filter(Track._Track__track_id.in_(id_list)).all()
        return tracks

    def get_tracks_by_artist(self, target_artist_name: str):
        if target_artist_name is None:
            #tracks = self._session_context_manager.session.query(Track).all()
            #return tracks
            return list()
        else:
            """
            TODO: Get ID of artist from table then use to find tracks
            """
            artist = self.get_artist(target_artist_name)
            tracks = self._session_context_manager.session.query(Track).filter(Track._artist == artist.id).all()
            return tracks

    def get_tracks_by_album(self, target_album_name: str):
        if target_album_name is None:
            #tracks = self._session_context_manager.session.query(Track).all()
            #return tracks
            return list()
        else:
            tracks = self._session_context_manager.session.query(Track).filter(Track._album == target_album_name).all()
            return tracks 

    def get_tracks_by_genre(self, target_genre:str):
        if target_genre is None:
            #tracks  = self._session_context_manager.session.query(Track).all()
            #return tracks 
            return list()
        else:
            tracks = self._session_context_manager.session.query(Track).filter(Track._genres == target_genre).all()
            return tracks 

    def get_first_track(self):
        track = self._session_context_manager.session.query(Track).first()
        return track

    def get_last_track(self):
        track = self._session_context_manager.session.query(Track).order_by(desc(Track._Track__id)).first()
        return track

    def get_previous_track(self, track: Track):
        previous_track = self._session_context_manager.session.query(Track).filter(Track._Track__id == track.track_id).one()
        return previous_track

    def get_next_track(self, track: Track):
        next_track = self._session_context_manager.session.query(Track).filter(Track._Track__id == track.track_id).one()
        return next_track

    def track_index(self, track: Track):
        return super().track_index(track)

    #################
    # Album Methods #
    #################

    def get_albums_by_id(self, id_list):
        albums = self._session_context_manager.session.query(Album).filter(Album._Album__id.in_(id_list)).all()
        return albums
    
    def get_first_album(self):
        album = self._session_context_manager.session.query(Album).first()
        return album
    
    def get_last_album(self):
        print(self._session_context_manager.session.query(Album).order_by(desc(Album._Album__id)).all())
        album = self._session_context_manager.session.query(Album).order_by(desc(Album._Album__id)).first()
        return album

    def get_previous_album(self, album: Album):
        previous_album = self._session_context_manager.session.query(Album).filter(Album._Album__id == album.album_id).one() 
        return previous_album

    def get_next_album(self, album: Album):
        next_album = self._session_context_manager.session.query(Album).filter(Album._Album__id == album.album_id).one()
        return next_album
    
    def album_index(self, album: Album):
        return super().album_index(album)

    ##################
    # Review Methods #
    ##################

    def get_reviews_for_track(self):
        reviews = self._session_context_manager.session.query(Review).all()
        return reviews

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_context_manager as scm:
            scm.session.add(review)
            scm.commit()
    
    def add_artist(self, artist:Artist):
        with self._session_context_manager as scm:
            scm.session.add(artist)
            scm.commit()

    def add_genre(self, genre:Genre):
        with self._session_context_manager as scm:
            scm.session.add(genre)
            scm.commit()