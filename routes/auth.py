from database.database import db
from database.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, flash, url_for, redirect, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.profile', name=user.first_name))
            else:
                flash('Incorrect password, try again.', 'danger')
        else:
            flash('Email does not exist!', 'danger')

    return render_template("login.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password = generate_password_hash(request.form.get('password'),method='sha256')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered with an account!', 'danger')
        elif len(email) < 1:
            flash('Email address is required!', 'danger')
        elif len(first_name) < 1:
            flash('First name is required!', 'warning')
        elif len(last_name) < 1:
            flash('Last name is required!', 'warning')
        elif len(password) < 8:
            flash('Password must be 8 or more characters!', 'warning')
        else:
            user = User(email=email,first_name=first_name,last_name=last_name,password=password)
            
            db.session.add(user)
            db.session.commit()

            flash('Account created!', 'success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html")
