import abc
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

repo_instance = None


class RepositoryException(Exception): # message (in covid app, when review not attached properly (not used))
    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        # Raises RepositoryException. But since review object is not bidirectional, I'm not sure what to do yet.
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_artist(self, artist: Artist):
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_album(self, album: Album):
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_track_by_id(self, id: int) -> Track:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_number_of_tracks(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_artist(self, artist_name):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_album_by_id(self, album_title):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_genre(self, genre_name):
        raise NotImplementedError
    
    # B requirements search by methods
    @abc.abstractmethod
    def get_tracks_by_id(self, id_list):
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_track(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_track(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_artists(self, target_artist_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_album(self, target_album_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_genre(self, target_genre_name: str):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_first_track(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_last_track(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_previous_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def track_index(self, track: Track):
        raise NotImplementedError
    
    def get_albums_by_id(self, id_list):
        pass

    def get_first_album(self):
        raise NotImplementedError

    def get_last_album(self):
        raise NotImplementedError

    def get_previous_album(self, album: Album):
        raise NotImplementedError

    def get_next_album(self, album: Album):
        raise NotImplementedError
    
    def album_index(self, album: Album):
        raise NotImplementedError
