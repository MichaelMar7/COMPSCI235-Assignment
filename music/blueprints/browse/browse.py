from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import music.adapters.repository as repo
import music.blueprints.utilities.utilities as utilities
import music.blueprints.browse.services as services

#from music.authentication.authentication import login_required


# Configure Blueprint
browse_blueprint = Blueprint("browse_bp", __name__)

"""
@browse_blueprint.route('/browse_tracks', methods=['GET'])
def browse_tracks_by_id():
    target_id = request.args.get("track_name")
    first_track = services.get_first_track(repo.repo_instance)
    last_track = services.get_last_track(repo.repo_instance)
    if first_track is None:
        target_id = first_track["id"]

    return render_template("browse/tracks.html", random_track=utilities.get_random_track(), track_by_title_demo=services.get_track_by_title(repo, "Piano "))
"""

@browse_blueprint.route('/browse_tracks', methods=['GET'])
def browse_tracks():
    target_title = request.args.get("track_title")
    target_id = request.args.get("track_id")
    first_track = services.get_first_track(repo.repo_instance)
    last_track = services.get_last_track(repo.repo_instance)
    if first_track is None:
        target_title = first_track["title"]
    track = first_track
    if target_title is not None and services.get_track_by_title(target_title, repo) is not None:
        track = services.get_track_by_title(target_title, repo)
    #if services.get_track(target_id, repo) is not None and target_id is not None:
    #    track = services.get_track(target_id, repo)

    # sidebar random album
    random_album = utilities.get_random_album()
    random_album_tracks = repo.repo_instance.get_tracks_by_album(random_album.title)

    return render_template(
        "browse/tracks.html",
        title="Tracks",
        random_track=utilities.get_random_track(), 
        random_album=random_album, 
        random_album_tracks=random_album_tracks,
        track_by_title_demo=track
    )

@browse_blueprint.route('/browse_albums', methods=['GET'])
def browse_albums():
    pass

@browse_blueprint.route('/browse_tracks_by_artist', methods=['GET'])
def browse_tracks_by_artist():
    pass

@browse_blueprint.route('/browse_tracks_by_genre', methods=['GET'])
def browse_tracks_by_genre():
    pass





