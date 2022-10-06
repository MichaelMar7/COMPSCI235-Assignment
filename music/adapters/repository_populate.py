from pathlib import Path

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader, load_reviews, load_users

# TODO: Association between Track and Genre?

def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    """
    Reads csv files and adds all objects from the csv_reader object to this repo from csv_reader object's lists to the repo's lists.
    """
    albums_file_name = str(data_path / "raw_albums_excerpt.csv")
    tracks_file_name = str(data_path / "raw_tracks_excerpt.csv") 
    reader = TrackCSVReader(albums_file_name, tracks_file_name)
    reader.read_csv_files()
    for track in reader.dataset_of_tracks:
        repo.add_track(track)
    for album in reader.dataset_of_albums:
        repo.add_album(album)
    if database_mode == False:
        for artist in reader.dataset_of_artists:
            repo.add_artist(artist)
        for genre in reader.dataset_of_genres:
            repo.add_genre(genre)
    users = load_users(data_path, repo)
    load_reviews(data_path, repo, users)