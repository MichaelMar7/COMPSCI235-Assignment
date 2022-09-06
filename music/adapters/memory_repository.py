from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList
from music.adapters.repository import AbstractRepository, RepositoryException
from music.adapters.csvdatareader import TrackCSVReader

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__tracks = list()
        self.__tracks_index = dict()
        self.__users = list()
        self.__reviews = list()

    def add_track(self, track: Track):
        self.__tracks.append(track)
        self.__tracks_index[track.track_id] = track

    def add_user(self, user: User):
        self.__users.append(user)

    def add_review(self, review: Review):
        # super().add_review(review)
        self.__reviews.append(review)
    
    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)
    
    def get_track(self, id: int) -> Track:
        track = None
        try:
            track = self.__tracks_index[id]
        except KeyError:
            pass
        return track
    
    def get_number_of_tracks(self):
        return len(self.__tracks)
    
    # B requirements search by methods
    def get_tracks_by_artists(self, target_artist: Artist):
        pass

    def get_tracks_by_album(self, target_album: Album):
        pass

    def get_tracks_by_genre(self, target_genre: Genre):
        pass

    def get_first_track(self):
        pass

    def get_last_track(self):
        pass

    def get_previous_track(self, track: Track):
        pass

    def get_next_track(self, track: Track):
        pass
    

