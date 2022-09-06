import abc
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

repo_instance = None


class RepositoryException(Exception):
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
        # Do extra stuff
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_track(self, id: int) -> Track:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_number_of_tracks(self):
        raise NotImplementedError
    
    # B requirements search by methods
    @abc.abstractmethod
    def get_first_track(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_track(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_artists(self, target_artist: Artist):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_album(self, target_album: Album):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_genre(self, target_genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_previous_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_track(self, track: Track):
        raise NotImplementedError
