import base64
from database.database import db
from database.models import Image
from flask_login import current_user
from flask import Blueprint, Response, flash, url_for, redirect, render_template

public_view = Blueprint('public_view', __name__)

""" These endpoints / views do not require user login. """

@public_view.route('/')
def homepage():
    return render_template('homepage.html', user=current_user)
@public_view.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        flash('Cannot Access Login Page While Logged In!', 'danger')
        return redirect(url_for('views.account'))
    
    return render_template('login.html', user=current_user)
@ public_view.route('/sign-up', methods=['GET'])
def sign_up():
    if current_user.is_authenticated:
        flash('Cannot Access Sign Up Page While Logged In!', 'danger')
        return redirect(url_for('views.account'))
    
    return render_template('sign_up.html', user=current_user)

@public_view.route('/image/<int:image_id>')
def get_image(image_id):
    img = Image.query.get(image_id)
    image_data = img.img.split(',')[1]
    return Response(base64.b64decode(image_data),mimetype=img.mimetype)