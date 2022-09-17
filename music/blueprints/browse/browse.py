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
    target_title = request.args.get("track_title") # http://127.0.0.1:5000/browse_tracks?track_title=<target_title>
    target_id = request.args.get("track_id") # http://127.0.0.1:5000/browse_tracks?track_id=<target_id>

    first_track = services.get_first_track(repo.repo_instance)
    last_track = services.get_last_track(repo.repo_instance)
    if first_track is None:
        target_title = first_track.track_title
        target_id = first_track.track_id
    
    # NOTE: the target_title takes priority over target_id if both are in the URL search. If ID instead takes prioity, you can swap the two if statements around
    track = first_track # default track to the first track
    if target_id is not None and services.get_track_by_id(target_id, repo) is not None:
        #print("a") Testing
        track = services.get_track_by_id(target_id, repo)
        #print(track)
    if target_title is not None and services.get_track_by_title(target_title, repo) is not None:
        #print("b") Testing
        track = services.get_track_by_title(target_title, repo)
        #print(track)
    #print(track)
    
    # These are the URL links when we browse
    first_track_url = None #url_for('browse_bp.browse_tracks', track_title=first_track.title)
    last_track_url = None #url_for('browse_bp.browse_tracks', track_title=last_track.title)
    previous_track_url = None
    next_track_url = None

    # Only if repo tracks list is not empty, which is very unlikely except for when we do testing
    if repo.repo_instance.get_number_of_tracks() > 0:
        previous_track = services.get_previous_track(track, repo) # is None if it's on the first track
        next_track = services.get_next_track(track, repo) # is None if it's on the last track
        if previous_track is not None:
            previous_track_url = url_for('browse_bp.browse_tracks', track_title=previous_track.title)
            first_track_url = url_for('browse_bp.browse_tracks', track_title=first_track.title)
        if next_track is not None:
            next_track_url = url_for('browse_bp.browse_tracks', track_title=next_track.title)
            last_track_url = url_for('browse_bp.browse_tracks', track_title=last_track.title)
        
        """Testing
        print(first_track)
        print(last_track)
        print(previous_track)
        print(next_track)

        print(first_track_url)
        print(last_track_url)
        print(previous_track_url)
        print(next_track_url)
        """

        # sidebar random album
        random_album = utilities.get_random_album()
        random_album_tracks = repo.repo_instance.get_tracks_by_album(random_album.title)

        return render_template(
            "browse/tracks.html",
            page_title="Tracks",
            random_track=utilities.get_random_track(),  # random track in sidebar
            random_album=random_album,  # random album in sidebar
            random_album_tracks=random_album_tracks, # all tracks in the album from random_album
            track=track, # selected track
            first_track=first_track, # not used
            last_track=last_track, # not used
            first_track_url=first_track_url, # following are the url for the first, last, previous, and next track
            last_track_url=last_track_url,
            previous_track_url=previous_track_url,
            next_track_url=next_track_url

        )
    return redirect(url_for('home_bp.home'))

"""
Copy above method into here, but use album instead of track, and add a link in the nav for broswe album
"""
@browse_blueprint.route('/browse_albums', methods=['GET'])
def browse_albums():
    pass

"""
I'm going to complete these methods, so ask me if you're going to touch these
"""
@browse_blueprint.route('/browse_tracks_by_artist', methods=['GET'])
def browse_tracks_by_artist():
    target_artist = request.args.get("artist_name")
    cursor = request.args.get("cursor")
    if target_artist is None:
        target_artist = services.get_first_track(repo.repo_instance).artist.full_name
    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    tracks = services.get_tracks_by_artist(target_artist, repo)

    if len(tracks) > 0:
        first_track_url = None
        last_track_url = None
        previous_track_url = None
        next_track_url = None

        if cursor > 0:
            previous_track_url = url_for("browse_bp.browse_tracks_by_artist", artist_name=target_artist, cursor=cursor-1)
            first_track_url = url_for("browse_bp.browse_tracks_by_artist", artist_name=target_artist, cursor=0)
        if cursor+1 < len(tracks):
            next_track_url = url_for("browse_bp.browse_tracks_by_artist", artist_name=target_artist, cursor=cursor+1)
            last_track_url = url_for("browse_bp.browse_tracks_by_artist", artist_name=target_artist, cursor=len(tracks)-1)

        # sidebar random album
        random_album = utilities.get_random_album()
        random_album_tracks = repo.repo_instance.get_tracks_by_album(random_album.title)

        return render_template(
            "browse/tracks.html",
            page_title="Tracks by Album - " + target_artist,
            random_track=utilities.get_random_track(),
            random_album=random_album, 
            random_album_tracks=random_album_tracks,
            track=tracks[cursor],
            first_track_url=first_track_url,
            last_track_url=last_track_url,
            previous_track_url=previous_track_url,
            next_track_url=next_track_url
        )

@browse_blueprint.route('/browse_tracks_by_genre', methods=['GET'])
def browse_tracks_by_genre():
    pass





