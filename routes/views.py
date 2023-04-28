from database.database import db
from database.models import User
from flask_login import login_required, current_user
from flask import Blueprint, request, flash, url_for, redirect, render_template

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)