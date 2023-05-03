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

@views.route('/create_listing', methods=['GET', 'POST'])
@login_required
def create_listing():
    errors = {}
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if not description:
            description = 'None'
        price = request.form.get('price')
        if not price:
            price = 0

        listing = Listing(title=title, description=description,
                          price=price, user_id=current_user.id)
        db.session.add(listing)

        if not errors:
            db.session.commit()
            print(listing)
            flash('New Listing Created!', 'success')
            return redirect(url_for('views.profile', listing=listing))

    return render_template('create_listing.html', user=current_user, errors=errors)
