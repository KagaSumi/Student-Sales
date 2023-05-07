import os
import requests
from database.database import db
from werkzeug.utils import secure_filename
from database.models import User, Listing
from flask_login import login_required, current_user
from flask import Blueprint, request, Response, flash, url_for, redirect, render_template, jsonify
views = Blueprint('views', __name__)


@views.route('/')
def homepage():
    return render_template('homepage.html', user=current_user)


@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        user.email = request.form.get('email')
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        db.session.commit()
        flash("User Updated Successfully!", "success")
        return redirect(request.url)
    return render_template('account.html', user=current_user)


@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


# @views.route("/create_listing", methods=['POST'])
# @login_required
# def listing_create():
#     data = request.json
#     for key in ('title', 'description', 'price'):
#         if key not in data:
#             return jsonify(message=f'{key} is missing from JSON'), 400
#     sent_request = requests.post("/create_listing_new", json={
#         "title": data["title"],
#         "description": data["description"],
#         "price": data["price"],
#         "user_id": current_user.id
#     })
#     if sent_request.ok:
#         return jsonify(message="Listing Created"), 200
#     return jsonify(message="Error in Creating Listing"), 400


@views.route('/create_listing', methods=['GET'])
@login_required
def create_listing():
    return render_template('create_listing.html', user=current_user)


@views.route('/edit_listing/<int:listing_id>', methods=['GET', 'POST'])
@login_required
def edit_listing(listing_id):
    errors = {}
    listing = Listing.query.get(listing_id)

    if not listing or current_user.id is not listing.user_id:
        flash('Access to listing is not allowed!', 'danger')
        return redirect(url_for('views.profile'))

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


@views.route('/preview_listing/<int:listing_id>', methods=['GET'])
@login_required
def preview_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing or current_user.id is not listing.user_id:
        flash('Access to listing is not allowed!', 'danger')
        return redirect(url_for('views.profile'))
    return render_template("preview_listing.html", user=current_user, listing=listing)
