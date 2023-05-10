from database.database import db
from flask import Blueprint, flash, url_for, redirect, render_template
from flask_login import login_required, logout_user, current_user

private_view = Blueprint("private_view", __name__)

""" These endpoints / views require user login. """

@private_view.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out Successfully!', 'success')
    return redirect(url_for('public_view.login'))

@private_view.route('/create_listing', methods=['GET'])
@login_required
def create_listing():
    return render_template('create_listing.html', user=current_user)

@private_view.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
