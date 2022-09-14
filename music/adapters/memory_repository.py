from pathlib import Path

from bisect import bisect, bisect_left, insort_left # when adding tracks and tracks index

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList
from music.adapters.repository import AbstractRepository, RepositoryException
from music.adapters.csvdatareader import TrackCSVReader

"""
TODO:
Allow browsing of albums (change get album form album name to album id and add similar methods from tracks to albums)
"""

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__tracks = list()
        self.__tracks_index = dict()
        #self.__track_title_index = dict()
        self.__artists = set()
        self.__albums = set()
        self.__genres = set()
        self.__users = list()
        self.__reviews = list()

    def add_track(self, track: Track):
        insort_left(self.__tracks,track)
        self.__tracks_index[track.track_id] = track
        #self.__track_title_index[track.track_id] = track.title

    def add_user(self, user: User):
        self.__users.append(user)

    def add_review(self, review: Review):
        # super().add_review(review)
        self.__reviews.append(review)

    def add_artist(self, artist: Artist):
        self.__artists.add(artist)

    def add_album(self, album: Album):
        self.__albums.add(album)
    
    def add_genre(self, genre: Genre):
        self.__genres.add(genre)
    
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
    
    def get_track_by_title(self, target_title):
        return next((track for track in self.__tracks if track.title.lower() == target_title.lower()), None) 

    # B requirements search by methods
    def get_tracks_by_id(self, id_list):
        existing_ids = [id for id in id_list if id in self.__tracks_index]
        tracks = [self.__tracks_index[id] for id in existing_ids]
        return tracks
    
    def get_tracks_by_artists(self, target_artist_name: str):
        artist = self.get_artist(target_artist_name)
        matching_tracks = list()
        if artist is not None:
            matching_tracks = [track for track in self.__track if track.artist == artist]
        return matching_tracks

    def get_tracks_by_album(self, target_album_name: str):
        album = self.get_album(target_album_name)
        matching_tracks = list()
        if album is not None:
            matching_tracks = [track for track in self.__track if track.album == album]
        return matching_tracks

    def get_tracks_by_genre(self, target_genre_name: str):
        genre = self.get_genre(target_genre_name)
        matching_tracks = list()
        if genre is not None:
            matching_tracks = [track for track in self.__track if genre in track.genre]
        return matching_tracks

    def get_first_track(self):
        if len(self.__tracks) > 0:
            return self.__tracks[0]
        return None

    def get_last_track(self):
        if len(self.__tracks) > 0:
            return self.__tracks[-1]
        return None

    def get_previous_track(self, track: Track):
        try:
            index = self.track_index(track)
            for stored_track in reversed(self.__tracks[0:index]):
                if stored_track.track_id < track.track_id:
                    return stored_track.track_id
        except ValueError:
            return None

    def get_next_track(self, track: Track):
        try:
            index = self.track_index(track)
            for stored_track in self.__tracks[index + 1:len(self.__tracks)]:
                if stored_track.track_id > track.track_id:
                    return stored_track.track_id
        except ValueError:
            return None
    
    def track_index(self, track: Track):
        index = bisect_left(self.__tracks, track)
        if index != len(self.__tracks) and self.__tracks[index].track_id == track.track_id:
            return index
        raise ValueError
    
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
        repo.add_artist(artist)
    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)
