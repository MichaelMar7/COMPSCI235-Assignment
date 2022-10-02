from datetime import date
from typing import List
from flask import session
from pytest import Session
from sqlalchemy import desc, asc

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.review import Review
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

class SqlAlchemyReposity(AbstractRepository):
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

    def get_track(self, id: id) -> Track:
        track = None
        try: 
            track = self._session_context_manager.session.query(Track).filter(Track._track_id == id).one()
        except NoResultFound:
            pass
        return Track

    def get_tracks_by_artist(self, target_artist_name: str):
        if target_artist_name is None:
            tracks = self._session_context_manager.session.query(Track).all()
            return tracks
        else:
            tracks = self._session_context_manager.session.query(Track).filter(Track._artist == target_artist_name).all()
            return tracks

    def get_first_track(self):
        track = self._session_context_manager.session.query(Track).first()
        return track

    def get_last_track(self):
        track = self._session_context_manager.session.query(Track).order_by(desc(Track._track_id)).first()
        return track
    
    def get_tracks_by_album(self, target_album:str):
        if target_album is None:
            tracks = self._session_context_manager.session.query(Track).all()
            return tracks
        else:
            tracks = self._session_context_manager.session.query(Track).filter(Track._album == target_album).all()
            return tracks 
    
    def get_tracks_by_genre(self, target_genre:str):
        if target_genre is None:
            tracks  = self._session_context_manager.session.query(Track).all()
            return tracks 
        else:
            tracks = self._session_context_manager.session.query(Track).filter(Track._genres == target_genre).all()
            return tracks 

    def get_reviews_for_track(self):
        reviews = self._session_context_manager.session.query(Review).all()
        return reviews

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_context_manager as scm:
            scm.session.add(review)
            scm.commit()

