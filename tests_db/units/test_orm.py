import pytest

from sqlalchemy.exc import IntegrityError

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review

def insert_user(empty_session, values=None):
    new_name = "Michael"
    new_password = "1234567"

    if values is not None:
        new_name = values[0]
        new_password = values[0]
    
    empty_session.execute("INSERT INTO users (user_name, password) VALUES (:user_name, :password)",
                          {"user_name": new_name, "password": new_password})
    row = empty_session.execute("SELECT id from users where user_name = :user_name",
                                {"user_name": new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

"""
def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks (track_title, title, first_paragraph, hyperlink, image_hyperlink) VALUES '
        '(:date, "Coronavirus: First case of virus in New Zealand", '
        '"The first case of coronavirus has been confirmed in New Zealand  and authorities are now scrambling to track down people who may have come into contact with the patient.", '
        '"https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus", '
        '"https://resources.stuff.co.nz/content/dam/images/1/z/e/3/w/n/image.related.StuffLandscapeSixteenByNine.1240x700.1zduvk.png/1583369866749.jpg")',
        {'date': article_date.isoformat()}
    )
    row = empty_session.execute('SELECT id from articles').fetchone()
    return row[0]
"""

"""
def make_track():
    track = Track(
        
    )
    return track
"""

def make_user():
    user = User(1, "Michael", "Password123")
    return user


"""
def make_tag():
    tag = Tag("News")
    return tag
"""
