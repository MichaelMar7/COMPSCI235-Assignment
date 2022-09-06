from pathlib import Path

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
        self.__tracks = list() # Sorted by id???
        self.__tracks_index = dict()
        self.__artists = set()
        self.__albums = set()
        self.__genres = set()
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

    def add_artist(self, artist: Artist):
        self.__artists.append(artist)

    def add_album(self, album: Album):
        self.__albums.append(album)
    
    def add_genre(self, genre: Genre):
        self.__genres.append(genre)
    
    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)
    
    def get_track(self, id: int) -> Track:
        try:
            return self.__tracks_index[id]
        except KeyError:
            return None
    
    def get_number_of_tracks(self):
        return len(self.__tracks)
    
    def get_artist(self, artist_name):
        return next((artist for artist in self.__artists if artist.full_name == artist_name), None) 
    
    def get_album(self, album_title):
        return next((album for album in self.__albums if album.title == album_title), None) 
    
    def get_genre(self, genre_name):
        return next((genre for genre in self.__genres if genre.name == genre_name), None) 
    
    # B requirements search by methods
    def get_tracks_by_id(self, target_artist: Artist):
        pass

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
    
def populate(data_path: Path, repo: MemoryRepository):
    albums_file_name = str(data_path / "raw_albums_excerpt.csv")
    tracks_file_name = str(data_path / "raw_tracks_excerpt.csv") 
    reader = TrackCSVReader(albums_file_name, tracks_file_name)
    reader.read_csv_files()
    for track in reader.dataset_of_tracks:
        repo.add_track(track)
    for album in reader.dataset_of_albums:
        repo.add_album(album)
    for artist in reader.dataset_of_artists:
        repo.add_track(artist)
    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)
