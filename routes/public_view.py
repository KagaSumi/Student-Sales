from database.database import db
from database.models import User
from flask_login import current_user
from flask import Blueprint, flash, url_for, redirect, render_template

public_view = Blueprint('public_view', __name__)

""" These endpoints / views do not require user login. """

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
