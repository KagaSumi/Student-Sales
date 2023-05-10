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

@views.route('/edit_listing/<int:listing_id>', methods=['PUT'])
@login_required
def listing_edit(listing_id):
    data = request.json
    for key in ("title","description","price"):
        if key not in data:
            return jsonify(message=f"{key} is missing from JSON"),400
    edit_request = requests.put(url=URL+"/edit_listing"+listing_id, json={
        "title": data["title"],
        "description": data["description"],
        "price": data["price"]
    })
    if edit_request.ok:
        return jsonify(message="Listing updated successfully"),200
    return jsonify(message="Listing was not updated successfully"),400

@views.route('/delete_listing/<int:listing_id>', methods=["DELETE"])
@login_required
def listing_delete(listing_id):
    delete_request = requests.delete(url=URL+"/delete_listing/"+listing_id,
                                     json={"user_id": current_user.id})
    if delete_request.ok:
        return jsonify(message="Listing Deleted"),200
    return jsonify(message="Listing was not deleted successfully"),400

@views.route('/edit_listing/<int:listing_id>', methods=['GET'])
@login_required
def edit_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing or current_user.id is not listing.user_id:
        flash('Access to this listing is not allowed!', 'danger')
        return redirect(url_for('private_view.profile'))
    return render_template("edit_listing.html", user=current_user, listing=listing)


@views.route('/preview_listing/<int:listing_id>', methods=['GET'])
@login_required
def preview_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing or current_user.id is not listing.user_id:
        flash('Access to listing is not allowed!', 'danger')
        return redirect(url_for('views.profile'))
    return render_template("preview_listing.html", user=current_user, listing=listing)
