import pytest

from flask import session


def test_register(client):
    response_code = client.get("/authentication/register").status_code
    assert response_code == 200

    response = client.post(
        "/authentication/register",
        data={"user_name": "test1", "password": "Password123"}
    )
    assert response.headers["location"] == "/authentication/login"


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, contain an upper case letter, a lower case letter and a digit.'),
        ('test1', 'NewPassword123', b'Your user name is already taken - please supply another')
))
def test_register_with_invalid_input(client, user_name, password, message):
    response1 = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    response2 = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response2.data


def test_login(client, auth):
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    response = auth.register() # user not registered yet so can't login
    response = auth.login()
    assert response.headers["Location"] == '/'

    with client:
        client.get('/')
        assert session['user_name'] == 'test1'


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Music Library' in response.data

"""
def test_login_required_to_comment(client):
    response = client.post('/comment')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_comment(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/comment?article=2')

    response = client.post(
        '/comment',
        data={'comment': 'Who needs quarantine?', 'article_id': 2}
    )
    assert response.headers['Location'] == '/articles_by_date?date=2020-02-29&view_comments_for=2'


@pytest.mark.parametrize(('comment', 'messages'), (
        ('Who thinks Trump is a f***wit?', (b'Your comment must not contain profanity')),
        ('Hey', (b'Your comment is too short')),
        ('ass', (b'Your comment is too short', b'Your comment must not contain profanity')),
))
def test_comment_with_invalid_input(client, auth, comment, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/comment',
        data={'comment': comment, 'article_id': 2}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data
"""


def test_track_without_title_or_id(client):
    response = client.get("/browse_tracks")
    assert response.status_code == 200

    assert b"Food" in response.data
    assert b"Track ID: 2" in response.data


def test_track_with_title(client):
    response = client.get("/browse_tracks?track_title=This%20World")
    assert response.status_code == 200

    assert b"This World" in response.data
    assert b"Track ID: 5" in response.data

def test_track_with_id(client):
    response = client.get("/browse_tracks?track_id=5")
    assert response.status_code == 200

    assert b"This World" in response.data
    assert b"Track ID: 5" in response.data

def test_track_with_title_and_id(client):
    response = client.get("/browse_tracks?track_title=yet to be titled&track_id=5")
    assert response.status_code == 200

    assert b"This World" in response.data
    assert b"Track ID: 5" in response.data

def test_track_with_invalid_title(client):
    response = client.get("/browse_tracks?track_title=fake")
    assert response.status_code == 200
    #assert b"This World" in response.data # Go to a invalid page

def test_track_with_invalid_id(client):
    response = client.get("/browse_tracks?track_id=69")
    assert response.status_code == 200
    #assert b"This World" in response.data # Go to a invalid page


def test_tracks_by_artist(client):
    pass

def test_tracks_by_artist_with_title(client):
    pass

def test_tracks_by_artist_with_title_and_cursor(client):
    pass

def test_tracks_by_artist_with_invalid_title(client):
    pass

def test_tracks_by_artist_with_invalid_cursor(client):
    pass

def test_tracks_by_genre(client):
    pass

def test_tracks_by_genre_with_title(client):
    pass

def test_tracks_by_genre_with_title_and_cursor(client):
    pass

def test_tracks_by_genre_with_invalid_title(client):
    pass

def test_tracks_by_genre_with_invalid_cursor(client):
    pass


def test_album_without_title_or_id(client):
    response = client.get("/browse_albums")
    assert response.status_code == 200

    assert b"AWOL - A Way Of Life" in response.data
    assert b"Album ID: 1" in response.data


def test_album_with_title(client):
    response = client.get("/browse_albums?album_title=mp3")
    assert response.status_code == 200

    assert b"mp3" in response.data
    assert b"Album ID: 58" in response.data

def test_album_with_id(client):
    response = client.get("/browse_albums?album_id=58")
    assert response.status_code == 200

    assert b"mp3" in response.data
    assert b"Album ID: 58" in response.data

def test_album_with_title_and_id(client):
    response = client.get("/browse_albums?album_title=mp3&album_id=5")
    assert response.status_code == 200

    assert b"mp3" in response.data
    assert b"Album ID: 58" in response.data

def test_album_with_invalid_title(client):
    response = client.get("/browse_tracks?album_title=fake")
    assert response.status_code == 200
    #assert b"This World" in response.data # Go to a invalid page

def test_album_with_invalid_id(client):
    response = client.get("/browse_tracks?album_id=9")
    assert response.status_code == 200
    #assert b"This World" in response.data # Go to a invalid page

