import pytest

from sqlalchemy.exc import IntegrityError

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review

def insert_user(empty_session, values=None):
    new_id = 6
    new_name = "Michael"
    new_password = "1234567"

    if values is not None:
        new_id = values[0]
        new_name = values[0]
        new_password = values[0]
    
    empty_session.execute("INSERT INTO users (id, user_name, password) VALUES (:id, :user_name, :password)",
                          {"user_id": new_id, "user_name": new_name, "password": new_password})
    row = empty_session.execute("SELECT id from users where user_name = :user_name",
                                {"user_name": new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (id, user_name, password) VALUES (:id, :user_name, :password)',
                              {'user_id': value[0], 'user_name': value[1], 'password': value[2]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks (track_id, track_title, artist_id, album_id, track_url, track_duration) VALUES '
        '(:track_id, "Food", :artist_id, :album_id, :track_url, :track_duration)',
        {'track_id': 2}, 
        {'artist_id' : 3},
        {'track_url' : "www.wtf.yep :)"},
        {'track_duration' : 3}
        )
    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]

def make_track():
    track = Track(
        2,
        "Not Food"
    )
    return track

def make_album():
    album = Album(2, "Yep")
    return album

def make_user():
    user = User(9, "Michael", "Password123")
    return user

"""
def test_loading_of_users(empty_session): # FAILED TODO
    users = list()
    users.append((10, "Edward", "Abc123123"))
    users.append((13, "Michael", "Password123"))
    insert_users(empty_session, users)

    expected = [
        User(7, "Edward", "Abc123123"),
        User(9, "Michael", "Password123")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session): # PASSED 
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [('michael', 'Password123')]

def test_saving_of_users_with_common_user_name(empty_session): 
    insert_user(empty_session, (6, "Andrew", "Abc123123"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(6, "Andrew", "Abc123123")
        empty_session.add (user)
        empty_session.commit()
"""
def test_saving_of_track(empty_session):
    track = make_track()
    album = make_album()
    empty_session.add(track)
    empty_session.add(album)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT track_id, track_title, artist_id, album_id, track_url, track_duration'))
    assert rows == [(2, "Food", 2, 3, "okay", 4)]
"""
def testing_saving_of_review(empty_session):
    track_key = insert_track(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "Password123"))

    rows = empty_session.query(Track).all()
    track = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "Andrew").one()

    review_text = "Good song."
    review = Review(track, user.user_name, review_text)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, track_id, review From reviews'))

    assert rows == [(user_key, track_key, review_text)]"""