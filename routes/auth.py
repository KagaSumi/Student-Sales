from database.database import db
from database.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request, flash, url_for, redirect, render_template
from flask_login import login_user, login_required, logout_user, current_user
import requests

auth = Blueprint('auth', __name__)
URL = "http://127.0.0.1:5000"

# This is the endpoints that does the logic for account management


@auth.route('/login', methods=['POST'])
def user_login():
    data = request.json
    for key in ("email", "password"):
        if key not in data:
            return jsonify(message=f"{key} is missing from JSON"), 400
    sent_request = requests.post(URL+"/verify_user", json={"email": data["email"],
                                                           "password": generate_password_hash(data["password"], method='sha256')})
    if sent_request.ok:
        user = User.query.filter_by(email=data["email"]).first()
        login_user(user, remember=True)
        return jsonify(message="User login successful"), 200
    return jsonify(message="Incorrect Email or Password"), 400


@auth.route('/sign-up', methods=['POST'])
def user_sign_up():
    data = request.json
    for key in ("email", "password", "first_name", "last_name", "phone_number"):
        if key not in data:
            return jsonify(message=f"{key} is missing from JSON"), 400
    if User.query.filter_by(email=data["email"].lower()).first():
        return jsonify(message="Email already registered with an account!"), 400
    sent_request = requests.post(URL+"/create_user",
                                 json={"email": data["email"].lower(),
                                       "password": generate_password_hash(data["password"], method='sha256'),
                                       "first_name": data["first_name"],
                                       "last_name": data["last_name"],
                                       "phone_number": data["phone_number"]})
    if sent_request.ok:
        user = User.query.filter_by(email=data["email"]).first()
        login_user(user, remember=True)
        return jsonify(message="User Sign Up successful"), 200
    return jsonify(message="Incorrect Email or Password"), 400


@auth.route('/delete_user')
def delete_user():
    if not current_user.is_authenticated:
        flash('Not Logged In', 'danger')
        return redirect(url_for("auth.login"))
    user = User.query.get(current_user.id)
    logout_user()
    db.session.delete(user)
    db.session.commit()
    flash('User Deleted!', 'success')
    return redirect(url_for('views.homepage'))


@auth.route("/create_listing", methods=['POST'])
@login_required
def listing_create():
    data = request.json
    for key in ('title', 'description', 'price'):
        if key not in data:
            return jsonify(message=f'{key} is missing from JSON'), 400
    sent_request = requests.post(url=URL+"/create_listing_new", json={
        "title": data["title"],
        "description": data["description"],
        "price": data["price"],
        "user_id": current_user.id
    })
    if sent_request.ok:
        return jsonify(message="Listing Created"), 200
    return jsonify(message="Error in Creating Listing"), 400


@ auth.app_errorhandler(404)
def page_not_found(err):
    return render_template('404.html', user=current_user), 404
