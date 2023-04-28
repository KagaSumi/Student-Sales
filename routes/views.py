from database.database import db
from flask import Blueprint, request, flash, url_for, redirect, render_template
from database.models import User

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@views.route('/profile', methods=['GET'])
def profile():
    first_name = request.args.get('name')
    print(f'this:::::::{first_name}')
    return render_template('profile.html', username=first_name)