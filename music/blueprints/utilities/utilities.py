import music.adapters.repository as repo

import random


def get_first_track():
    for track in get_100_tracks(100, 1000):
        if track is not None:
            return track

def get_100_tracks(min, max):
    return repo.repo_instance.get_tracks_by_id([x for x in range(min, max)])

def get_track_count():
    return repo.repo_instance.get_number_of_tracks()

def get_random_track():
    while True:
        index = random.randint(0, 10000)
        for track in get_100_tracks(index, index+1):
            if track is not None:
                return track
