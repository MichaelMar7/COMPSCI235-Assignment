from sqlalchemy import select, inspect

from music.adapters.orm import metadata
"""
def test_database_populate_inspect_table_names(database_engine):

    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['albums', 'artists', 'artists_unique', 'genres', 'genres_unique','reviews', 'track_genres', 'tracks', 'users']

def test_database_populate_select_all_users(database_engine):

    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[8]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['thorke', 'fmercury', 'mjackson']

def test_database_populate_select_all_reviews(database_engine):

    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['id'], row['username'], row['track'], row['review']))
        
        assert len(all_reviews) == 0 

def test_database_populate_select_all_tracks(database_engine):

    inspector = inspect(database_engine)
    name_of_tracks_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_tracks_table]])
        result = connection.execute(select_statement)

        all_tracks = []
        for row in result:
            all_tracks.append((row['id'],row['title']))

        tracks = len(all_tracks)
        assert tracks == 2000"""