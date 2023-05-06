from database.database import db
from database.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request, flash, url_for, redirect, render_template
from flask_login import login_user, login_required, logout_user, current_user
import requests

auth = Blueprint('auth', __name__)
URL = "http://127.0.0.1:5000"

@auth.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.account"))
    return render_template("login.html", user=current_user)

@auth.route('/login', methods=['POST'])
def user_login():
    data = request.json
    for key in ("email", "password"):
        if key not in data:
            return jsonify(message=f"{key} is missing from JSON"),400
    sent_request = requests.post(URL+"/verify_user",json={"email":data["email"],
                            "password":generate_password_hash(data["password"],method='sha256')})
    if sent_request.ok:
        user = User.query.filter_by(email=data["email"]).first()
        login_user(user, remember=True)
        return jsonify(message="User login successful"),200
    return jsonify(message="Incorrect Email or Password"),400
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out Successfully!', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        flash('Cannot Access Sign Up Page While Logged In!', 'danger')
        return redirect(url_for('views.account'))
    errors={}
    if request.method == 'POST':
        email = request.form.get('email').lower()
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            errors['email']='Email already registered with an account!'
        elif len(password) < 4:
            errors['password']='Password must be 4 or more characters!'
        else:
            user = User(email=email,first_name=first_name,last_name=last_name,password=generate_password_hash(password,method='sha256'))
            db.session.add(user)
            db.session.commit()
            print(user)
            flash('Account created!', 'success')
            return redirect(url_for('auth.login'))
    return render_template("sign_up.html",user=current_user,errors=errors)

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

@auth.route('/test_endpoint',methods=['PUT'])
def test_endpoint():
    data = request.json
    if "test" not in data:
        return jsonify(message="Missing test in JSON"),400
    return jsonify(message="POGGERS it works!!"),200

@auth.app_errorhandler(404)
def page_not_found(err):
    return render_template('404.html', user=current_user), 404