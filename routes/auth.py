from database.database import db
from database.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, flash, url_for, redirect, render_template
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.profile'))
            else:
                flash('Incorrect password, try again.', 'danger')
        else:
            flash('Email does not exist!', 'danger')

    return render_template("login.html", user=current_user)
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered with an account!', 'danger')
        elif len(email) < 1:
            flash('Email address is required!', 'danger')
        elif len(first_name) < 1:
            flash('First name is required!', 'warning')
        elif len(last_name) < 1:
            flash('Last name is required!', 'warning')
        elif len(password) < 3:
            flash('Password must be 4 or more characters!', 'warning')
        else:
            user = User(email=email,first_name=first_name,last_name=last_name,password=generate_password_hash(password,method='sha256'))
            
            db.session.add(user)
            db.session.commit()

            flash('Account created!', 'success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)
