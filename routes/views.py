from database.database import db
from flask import Blueprint, request, flash, url_for, redirect, render_template

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("base.html")

@views.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template("profile.html")