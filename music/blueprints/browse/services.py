from typing import List, Iterable

from music.adapters.repository import AbstractRepository
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

class NonExistentArticleException(Exception):
    pass

class UnknownUserException(Exception):
    pass

def add_review(track: Track, review: Review, user: User, repo: AbstractRepository):
    pass

def get_track(track_id: int, repo: AbstractRepository):
    track = repo.repo_instance.get_track(track_id)
    if track is None:
        raise NonExistentArticleException
    return track_to_dict(track)

def get_track_by_title(title, repo: AbstractRepository):
    return repo.repo_instance.get_track_by_title(title)

def get_first_track(repo: AbstractRepository):
    track = repo.get_first_track()

    return track_to_dict(track)

def get_last_track(repo: AbstractRepository):
    track = repo.get_last_track()
    return track_to_dict(track)

def get_album(album_id: int, repo: AbstractRepository):
    album = repo.get_album(album_id)
    if album is None:
        raise NonExistentArticleException
    #return album_to_dict(album)


"""
def get_first_album(repo: AbstractRepository):
    album = repo.get_first_album()

    return track_to_dict(album)

def get_last_album(repo: AbstractRepository):
    album = repo.get_last_album()
    return track_to_dict(album)
"""



def track_to_dict(track: Track):
    article_dict = {
        "id": track.track_id,
        "title": track.title,
        "artist": track.artist,
        "album": track.album,
        "genre": track.genres,
        "track_url": track.track_url,
        #"reviews": reviews_to_dict(track.reviews)
    }
    return article_dict


def tracks_to_dict(tracks: Iterable[Track]):
    return [track_to_dict(track) for track in tracks]

