from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import music.adapters.repository as repo
#import music.utilities.utilities as utilities
import music.blueprints.browse.services as services

#from music.authentication.authentication import login_required


# Configure Blueprint
browse_blueprint = Blueprint("browse_bp", __name__)

@browse_blueprint.route('/browse_tracks', methods=['GET'])
def browse_tracks_by_id():
    target_id = request.args.get("track_name")
    first_track = services.get_first_track(repo.repo_instance)
    last_track = services.get_last_track(repo.repo_instance)
    if first_track is None:
        target_id = first_track["id"]

    return render_template("browse/tracks.html")

@browse_blueprint.route('/browse_tracks', methods=['GET'])
def browse_tracks_by_title():
    target_title = request.args.get("track_name")
    first_track = services.get_first_article(repo.repo_instance)
    last_track = services.get_last_article(repo.repo_instance)
    if first_track is None:
        target_title = first_track["title"]

    return render_template(
        "browse/tracks.html",
        title="Tracks",
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





