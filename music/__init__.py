"""Initialize Flask app."""

from pathlib import Path
from flask import Flask, render_template

import random

import sqlalchemy
from music.adapters import memory_repository

import music.adapters.repository as repo
from music.adapters.memory_repository import MemoryRepository, populate
from music.adapters import database_repository
from music.adapters.orm import metadata, map_model_to_tables

#imports from SQLAlchemy 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

"""""" # Stays here for now
# TODO: Access to the tracks should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from music.domainmodel.track import Track


# TODO: Access to the tracks should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
def create_some_track():
    some_track = Track(1, "Heat Waves")
    some_track.track_duration = 250
    some_track.track_url = 'https://spotify/track/1'
    return some_track
""""""


def create_app(test_config=None):

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path("music") / "adapters" / "data"

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        repo.repo_instance = MemoryRepository()
        database_mode = False
        populate(data_path, repo.repo_instance, database_mode)
    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_arg={"check_same_thread":False}, poolclass=NullPool, echo=database_echo)

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = database_repository.SqlAlchemyReposity(session_factory)

        if app.config['TESTING'] == 'TRUE' or len(database_engine.table_names()) == 0:
            for table in reversed(metadata.sorted_tables):
                database_engine.execute(table.delete())
            map_model_to_tables()
            database_mode = True 
            populate(data_path, repo.repo_instance, database_mode)
            print("REPOPULATING DATABASE ... FINISHED")
        else:
            map_model_to_tables()

    with app.app_context():
        pass
        # Register blueprints.
        """These will be for each blueprint of the app"""
        
        from .blueprints.home import home
        app.register_blueprint(home.home_blueprint)

        from .blueprints.browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from .blueprints.authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        @app.before_first_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyReposity):
                repo.repo_instance.reset_session()

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyReposity):
                repo.repo_instance.close_session()
    return app

# blueprint methods testing
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

