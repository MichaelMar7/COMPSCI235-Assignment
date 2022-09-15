from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
from functools import wraps

import music.adapters.repository as repo
import music.blueprints.authentication.services as services
import music.blueprints.utilities.utilities as utilities


authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/authentication')

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None
    if form.validate_on_submit():
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            user_name_not_unique = "Your username is taken. Please try again."
    
    return render_template('authentication/credentials.html', random_track=utilities.get_random_track(), form=form, user_name_error_message=user_name_not_unique, handler_url=url_for('authentication_bp.register'))

class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\ a loower case letter and a digit'
        self.message = message
    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('Password', [DataRequired(message='Your password is required'), PasswordValid()])
    submit = SubmitField('Register')

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    password_doesnt_match = None
    if form.validate_on_submit():
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)
            session.clear()
            session['user_name'] = user['user_name']
            return redirect(url_for('home_bp.home'))
        except services.UnknownUserException:
            user_name_not_recognised = "User name is not recognised. Please try again."
        except services.AuthenticationException:
            password_doesnt_match = "Password does not match the given user name. Please try again."
    return render_template('authentication/credentials.html',random_track=utilities.get_random_track(), user_name_error_message=user_name_not_recognised, password_error_message=password_doesnt_match, form=form)

@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.html'))

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view


class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')
