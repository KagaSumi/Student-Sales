from database.database import db
from database.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request, flash, url_for, redirect, render_template
from flask_login import login_user, login_required, logout_user, current_user
import requests

private_view = Blueprint("private_view", __name__)

# This should be used for any pages that require the user to be logged in for


@private_view.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out Successfully!', 'success')
    return redirect(url_for('auth.login'))


@private_view.route('/create_listing', methods=['GET'])
@login_required
def create_listing():
    return render_template('create_listing.html', user=current_user)


@private_view.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
