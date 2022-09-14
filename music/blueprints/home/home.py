from flask import Blueprint, render_template

import music.blueprints.utilities.utilities as utilities

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    #Takes to home page
    return render_template('home/home.html', random_track=utilities.get_random_track())