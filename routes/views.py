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

@views.route('/edit_listing', methods=['GET', 'POST'])
@login_required
def edit_listing():
    errors = {}
    listing_id = request.args.get('listing_id')
    listing = Listing.query.get(listing_id)

    if request.method == 'POST':
        if 'preview_listing' in request.form:
            return redirect(url_for('views.preview_listing', listing_id=listing_id))

        if 'update_listing' in request.form:
            listing.title = request.form['title']
            listing.description = request.form['description']
            if not listing.description:
                listing.description = 'None'
            listing.price = request.form['price']
            if not listing.price:
                listing.price = 0
            if not errors:
                db.session.commit()
                flash("Listing Updated Successfully!", "success")
                return redirect(request.url)

        if 'delete_listing' in request.form:
            db.session.delete(listing)
            db.session.commit()
            flash("Listing Deleted Successfully!", "success")
            return redirect(url_for('views.profile'))

    return render_template("edit_listing.html", user=current_user, listing=listing, errors=errors)

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

@views.route('/preview_listing')
@login_required
def preview_listing():
    listing_id = request.args.get('listing_id')
    listing = Listing.query.get(listing_id)
    return render_template("preview_listing.html", user=current_user, listing=listing)
